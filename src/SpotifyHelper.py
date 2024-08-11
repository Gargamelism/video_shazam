import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from urllib import parse


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
        query = f"{track_name} track:{track_name}"
        if artist_name:
            query += f" artist:{artist_name}"

        quoted_query = parse.quote(query)
        query_result = self.spotipy.search(q=quoted_query, type="track", limit=1)
        return query_result

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
