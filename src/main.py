import argparse
import json
import os
from dotenv import load_dotenv

from json_helper import encoder
from song_resolve.song_resolve import resolve_songs_from_file, resolve_songs_from_folder
from SpotifyHelper import SpotifyHelper


def parse_args():
    # Rest of the code...
    parser = argparse.ArgumentParser(description="Retrieve songs played in video")
    parser.add_argument("-i", "--input", type=str, help="input file or folder when there are multiple files")
    parser.add_argument("-o", "--output-file", type=str, help="output file path")
    parser.add_argument("-s", "--segments", default=-1, type=int, help="how many segments to analyze")
    parser.add_argument("-a", "--analysis-time", default=5, type=int, help="how many seconds to analyze for")
    parser.add_argument("-n", "--songs-file", required=False, type=str, help="file with songs to create a playlist")
    return parser.parse_args()


def main():
    # Load environment variables from .env file
    load_dotenv()

    args = parse_args()

    all_songs = {}

    if args.songs_file:
        with open(args.songs_file, "r") as songs_file:
            all_songs = json.load(songs_file)
    else:
        if os.path.isfile(args.input):
            all_songs = resolve_songs_from_file(all_songs, args.input, args.analysis_time, args.segments)
        if os.path.isdir(args.input):
            all_songs = resolve_songs_from_folder(all_songs, args.input, args.analysis_time, args.segments)

        with open(args.output_file, "w") as output_file:
            json.dump(all_songs, output_file, default=encoder, indent=4)

    spotify_helper = SpotifyHelper(
        os.getenv("SPOTIFY_CLIENT_ID"), os.getenv("SPOTIFY_CLIENT_SECRET"), os.getenv("SPOTIFY_REDIRECT_URI")
    )

    for original_file, songs in all_songs.items():
        for song in songs:
            spotify_track = spotify_helper.get_track(song["title"], song["artist"])
            print(f"Found track {spotify_track}")

    # Print final message
    print("Processing complete!")


if __name__ == "__main__":
    main()
