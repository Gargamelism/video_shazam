import os
from progressbar import ProgressBar

from audio_helper import extract_audio
from song_resolve.song_resolvers.VideoSongResolver import VideoSongResolver
from song_resolve.song_resolvers.TuneFindSongResolver import TuneFindSongResolver
from song_resolve.song_resolvers.SongData import SongData


def resolve_songs_from_file(all_songs: list[SongData], video_file: str, analysis_time: int, segments: int) -> list[SongData]:
    print("Extracting audio from video...")
    audio_file = extract_audio(video_file)
    if audio_file is None:
        print(f"Video file is not valid! {video_file}")
        return all_songs

    print("Audio extracted successfully!")

    song_resolver = VideoSongResolver(audio_file, analysis_time, segments)
    songs = song_resolver.get_songs()

    if len(songs) > 0:
        return all_songs + songs

    return all_songs


def resolve_songs_from_folder(all_songs: list[SongData], video_folder: str, analysis_time: int, segments: int) -> list[SongData]:
    for root, _, files in os.walk(video_folder):
        bar = ProgressBar(max_value=len(files)).start()
        for file in files:
            all_songs = resolve_songs_from_file(all_songs, os.path.join(root, file), analysis_time, segments)
            bar.increment()
        bar.finish()

    return all_songs


def resolve_songs_from_tunefind(all_songs: list[SongData], tunefind_url: str) -> list[SongData]:
    tunefind_resolver = TuneFindSongResolver(tunefind_url, all_songs)
    all_songs = tunefind_resolver.get_songs()
    return all_songs
