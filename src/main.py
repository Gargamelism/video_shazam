import argparse
from dotenv import load_dotenv
from pprint import pprint
from dataclasses import asdict
import json

from audio_helper import extract_audio
from SongResolver import SongResolver
from json_helper import encoder


def resolve_songs(all_songs, video_file, analysis_time, segments):
    print("Extracting audio from video...")
    audio_file = extract_audio(video_file)
    print("Audio extracted successfully!")

    song_resolver = SongResolver(audio_file, analysis_time, segments)
    songs = song_resolver.get_songs()

    pprint(songs)
    if len(songs) > 0:
        all_songs[songs[0].original_file] = [asdict(song) for song in songs]

    return all_songs


def parse_args():
    # Rest of the code...
    parser = argparse.ArgumentParser(description="Retrieve songs played in video")
    parser.add_argument("-i", "--input", type=str, help="input file or folder when there are multiple files")
    parser.add_argument("-o", "--output_file", type=str, help="output file path")
    parser.add_argument("-s", "--segments", default=2, type=int, help="how many segments to analyze")
    parser.add_argument("-a", "--analysis_time", default=5, type=int, help="how many seconds to analyze for")
    return parser.parse_args()


def main():
    # Load environment variables from .env file
    load_dotenv()

    args = parse_args()

    all_songs = {}
    all_songs = resolve_songs(all_songs, args.input, args.analysis_time, args.segments)

    with open(args.output_file, "w") as output_file:
        json.dump(all_songs, output_file, default=encoder)

    # Print final message
    print("Processing complete!")


if __name__ == "__main__":
    main()
