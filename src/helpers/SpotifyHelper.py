import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from urllib import parse
from progressbar import ProgressBar

from helpers.string_helper import get_distance


class SpotifyHelper:
    _scope = "playlist-modify-public"

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

    def get_playlist(self, playlist_name: str):
        user_playlists = self.spotipy.current_user_playlists(offset=0, limit=50)
        total_playlists = user_playlists.get("total")
        limit = user_playlists.get("limit")
        offset = user_playlists.get("offset")
        all_playlists = user_playlists.get("items")

        while total_playlists > offset + limit:
            offset += limit
            user_playlists = self.spotipy.current_user_playlists(offset=offset, limit=limit)
            all_playlists += user_playlists.get("items")

        for playlist in all_playlists:
            if playlist_name.lower() in playlist.get("name").lower():
                return playlist

    def playlist_add_tracks(self, playlist_id: str, tracks: list[str]):
        self.spotipy.playlist_add_items(playlist_id, tracks)
        return True

    def playlist_remove_all_occurrences_of_items(self, playlist_id: str, tracks: list[str]):
        self.spotipy.playlist_remove_all_occurrences_of_items(playlist_id, tracks)
        return True
