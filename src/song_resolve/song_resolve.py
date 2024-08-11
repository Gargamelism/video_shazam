import os
from dataclasses import asdict
from progressbar import ProgressBar

from audio_helper import extract_audio
from SongResolver import SongResolver


def resolve_songs_from_file(all_songs, video_file, analysis_time, segments):
    print("Extracting audio from video...")
    audio_file = extract_audio(video_file)
    if audio_file is None:
        print(f"Video file is not valid! {video_file}")
        return all_songs

    print("Audio extracted successfully!")

    song_resolver = SongResolver(audio_file, analysis_time, segments)
    songs = song_resolver.get_songs()

    if len(songs) > 0:
        all_songs[songs[0].original_file] = [asdict(song) for song in songs]

    return all_songs


def resolve_songs_from_folder(all_songs, video_folder, analysis_time, segments):
    for root, _, files in os.walk(video_folder):
        bar = ProgressBar(max_value=len(files)).start()
        for file in files:
            all_songs = resolve_songs_from_file(all_songs, os.path.join(root, file), analysis_time, segments)
            bar.increment()
        bar.finish()

    return all_songs
