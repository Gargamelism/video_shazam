import os
from dataclasses import dataclass
from progressbar import ProgressBar
from datetime import timedelta

from audio_helper import split_audio
from shazam_helper import identify_song


@dataclass
class SongData:
    title: str
    artist: str
    file: str
    time: str
    accuracy: float


class SongResolver:
    def __init__(self, audio_file_path: str, segment_duration_secs: int) -> None:
        self._autio_file_path = audio_file_path
        self._segment_duration_secs = segment_duration_secs

    def get_songs(self):
        split_audio_folder = split_audio(self._autio_file_path, self._segment_duration_secs)
        self._songs = self.__walk_mp3_files(split_audio_folder, 1)
        return self._songs

    def __walk_mp3_files(self, audio_clips_path, segment_duration):
        songs = []

        for root, _, audio_clips in os.walk(audio_clips_path):
            bar = ProgressBar(max_value=len(audio_clips)).start()

            for audio_clip in audio_clips:
                if audio_clip.endswith(".mp3"):
                    audio_clips_path = os.path.join(root, audio_clip)
                    song_data = identify_song(audio_clips_path)

                    bar.increment()

                    if not song_data:
                        continue

                    print(song_data)
                    print(
                        {
                            "title": song_data["track"]["title"],
                            "subtitle": song_data["track"]["subtitle"],
                            "location": song_data["location"],
                        }
                    )

                    original_file = os.path.split(root)[1]
                    timestamp_seconds = int(os.path.splitext(audio_clip)[0])
                    timestamp = timedelta(seconds=timestamp_seconds)
                    songs.append(
                        SongData(
                            title=song_data["track"]["title"],
                            artist=song_data["track"]["subtitle"],
                            file=original_file,
                            time=timestamp,
                            accuracy=song_data["location"]["accuracy"],
                        )
                    )

            bar.finish()

        return songs
