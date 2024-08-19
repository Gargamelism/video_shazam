import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from urllib import parse
from progressbar import ProgressBar

from helpers.string_helper import get_distance
from helpers.list_helper import chunks


class SpotifyHelper:
    _scope = "playlist-modify-public"
    PLAYLISTS_LIMIT_CHANGE_LIMIT = 100

    def __init__(self, client_id, client_secret, redirect_uri):
        self.spotipy = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret),
            auth_manager=SpotifyOAuth(
                client_id=client_id, client_secret=client_secret, scope=self._scope, redirect_uri=redirect_uri
            ),
        )

    def get_track(self, track_name, artist_name):
        query = f"{track_name}"
        if artist_name:
            query += f" artist:{artist_name}"

        quoted_query = parse.quote(query)

        track_items = self._get_all_tracks(quoted_query)
        sortered_items = sorted(track_items, key=lambda x: get_distance(track_name.lower(), x.get("name").lower()))

        with open("out/search_results.json", "a") as search_results_file:
            if sortered_items:
                spotify_track = sortered_items[0]
                if get_distance(track_name.lower(), spotify_track.get("name").lower()) > 0:
                    search_results_file.write(
                        json.dumps(
                            {
                                "song": track_name,
                                "artist": artist_name,
                                "lowest_distance": get_distance(track_name.lower(), sortered_items[0].get("name").lower()),
                                "search_results": sortered_items[0],
                            },
                            indent=4,
                        )
                    )

        return sortered_items

    def _get_all_tracks(self, query: str):
        limit = 50
        result_type = "track"
        market = "IL"
        print(f"Searching for {parse.unquote(query)}")

        query_result = self.spotipy.search(q=query, type=result_type, limit=limit, market=market)
        total_results = query_result.get("tracks").get("total")
        items = query_result.get("tracks").get("items")
        bar = ProgressBar().start()

        print(f"Found {total_results} results")

        while len(items) < total_results:
            query_result = self.spotipy.search(q=query, type=result_type, limit=limit, offset=len(items), market=market)
            current_items = query_result.get("tracks").get("items")

            # total_results changes sometimes after the first iteration
            total_results = query_result.get("tracks").get("total")
            items += current_items
            bar.increment()

        bar.finish()

        return items

    def _get_playlist(self, playlist_name: str):
        limit = 50
        user_playlists = self.spotipy.current_user_playlists(offset=0, limit=limit)
        total_playlists = user_playlists.get("total")
        all_playlists = user_playlists.get("items")

        while len(all_playlists) < total_playlists:
            user_playlists = self.spotipy.current_user_playlists(offset=len(all_playlists), limit=limit)
            total_playlists = user_playlists.get("total")
            all_playlists += user_playlists.get("items")

        for playlist in all_playlists:
            if playlist_name.lower() in playlist.get("name").lower():
                return playlist

    def playlist_add_tracks(self, playlist_name: str, tracks: list[str]):
        playlist = self._get_playlist(playlist_name)
        if not playlist:
            print(f"Created playlist {playlist_name}")
            playlist = self.spotipy.user_playlist_create(self.spotipy.me().get("id"), playlist_name, public=True)

        print("Removing duplicate tracks")
        self._playlist_remove_all_occurrences_of_items(playlist.get("id"), tracks)

        print("Adding tracks to playlist")
        for tracks_chunk in chunks(tracks, self.PLAYLISTS_LIMIT_CHANGE_LIMIT):
            self.spotipy.playlist_add_items(playlist.get("id"), tracks_chunk)
        return True

    def _playlist_remove_all_occurrences_of_items(self, playlist_id: str, tracks: list[str]):
        for tracks_chunk in chunks(tracks, self.PLAYLISTS_LIMIT_CHANGE_LIMIT):
            self.spotipy.playlist_remove_all_occurrences_of_items(playlist_id, tracks_chunk)

        return True
