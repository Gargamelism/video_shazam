import argparse
import json
import os
import sys
from dotenv import load_dotenv
from dataclasses import asdict
from pprint import pprint

from json_helper import encoder
from song_resolve.song_resolve import resolve_songs_from_file, resolve_songs_from_folder, resolve_songs_from_tunefind
from song_resolve.song_resolvers.SongData import SongData
from helpers.SpotifyHelper import SpotifyHelper
from helpers.string_helper import get_distance


def parse_args():
    # Rest of the code...
    parser = argparse.ArgumentParser(description="Retrieve songs played in video")
    parser.add_argument("-i", "--input", type=str, help="input file or folder when there are multiple files")
    parser.add_argument("-o", "--output-file", default="out/output.json", type=str, help="output file path")
    parser.add_argument("-s", "--segments", default=-1, type=int, help="how many segments to analyze")
    parser.add_argument("-a", "--analysis-time", default=5, type=int, help="how many seconds to analyze for")
    parser.add_argument("-n", "--songs-file", required=False, type=str, help="file with songs to create a playlist")
    parser.add_argument("-t", "--tunefind", required=False, help="search for songs on tunefind")
    parser.add_argument("-p", "--playlist", required=False, help="spotify playlist to add songs to")

    if not sys.argv[1:]:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()


def main():
    # Load environment variables from .env file
    load_dotenv()

    args = parse_args()

    all_songs: list[SongData] = []

    if args.songs_file:
        with open(args.songs_file, "r") as songs_file:
            all_songs = [SongData(**song) for song in json.load(songs_file)]
    else:
        if args.input:
            if os.path.isfile(args.input):
                all_songs = resolve_songs_from_file(all_songs, args.input, args.analysis_time, args.segments)
            if os.path.isdir(args.input):
                all_songs = resolve_songs_from_folder(all_songs, args.input, args.analysis_time, args.segments)

        elif args.tunefind:
            all_songs = resolve_songs_from_tunefind(all_songs, args.tunefind)

        with open(args.output_file, "w") as output_file:
            json.dump([asdict(song) for song in all_songs], output_file, default=encoder, indent=4)

    if args.playlist:
        track_ids = [song.track_id for song in all_songs if song.track_id]

        spotify_helper = SpotifyHelper(
            os.getenv("SPOTIFY_CLIENT_ID"), os.getenv("SPOTIFY_CLIENT_SECRET"), os.getenv("SPOTIFY_REDIRECT_URI")
        )

        spotify_helper.playlist_add_tracks(args.playlist, track_ids)

    # Print final message
    print("Processing complete!")


if __name__ == "__main__":
    main()
