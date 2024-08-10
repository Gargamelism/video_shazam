import argparse
from dotenv import load_dotenv
from pprint import pprint

from audio_helper import extract_audio
from SongResolver import SongResolver


def parse_args():
    # Rest of the code...
    parser = argparse.ArgumentParser(description="Retrieve songs played in video")
    parser.add_argument("-i", "--input_file", type=str, help="input file path")
    parser.add_argument("-o", "--output_file", type=str, help="output file path")
    parser.add_argument("-s", "--segments", default=2, type=int, help="how many segments to analyze")
    parser.add_argument("-a", "--analysis_time", default=5, type=int, help="how many seconds to analyze for")
    return parser.parse_args()


def main():
    # Load environment variables from .env file
    load_dotenv()

    args = parse_args()

    print("Extracting audio from video...")
    audio_file = extract_audio(args.input_file)
    print("Audio extracted successfully!")

    song_resolver = SongResolver(audio_file, args.analysis_time)
    songs = song_resolver.get_songs()
    pprint(songs)
    open(args.output_file, "w").write("\n".join([str(song) for song in songs]))

    # Print final message
    print("Processing complete!")


if __name__ == "__main__":
    main()
