import os
from dataclasses import dataclass
from progressbar import ProgressBar
from datetime import timedelta
from tempfile import NamedTemporaryFile, TemporaryDirectory

from audio_helper import split_audio
from shazam_helper import identify_song


@dataclass
class SongData:
    title: str
    artist: str
    original_file: str
    time: str
    accuracy: float

    def __eq__(self, other):
        return self.title == other.title and self.artist == other.artist

    def __hash__(self):
        return hash((self.title, self.artist))


class SongResolver:

    def __init__(self, audio_file: NamedTemporaryFile, segment_duration_secs: int, segments_count: int) -> None:
        self._original_audio_file = audio_file
        self._segment_duration_secs = segment_duration_secs
        self._segments_count = segments_count

    def get_songs(self) -> list[SongData]:
        self._split_audio_folder = split_audio(self._original_audio_file, self._segment_duration_secs, self._segments_count)
        self._songs = self.__walk_mp3_files(self._split_audio_folder)
        self._songs = list(set(self._songs))

        self._clean(self._split_audio_folder, self._original_audio_file)

        return self._songs

    def __walk_mp3_files(self, audio_clips_dir: TemporaryDirectory) -> list[SongData]:
        songs = []

        for root, _, audio_clips in os.walk(audio_clips_dir.name):
            bar = ProgressBar(max_value=len(audio_clips)).start()

            for audio_clip in audio_clips:
                if audio_clip.endswith(".mp3"):
                    audio_clip_path = os.path.join(root, audio_clip)
                    song_data = identify_song(audio_clip_path)

                    bar.increment()

                    if not song_data:
                        continue

                    original_file = os.path.split(root)[1]
                    timestamp_seconds = int(os.path.splitext(audio_clip)[0])
                    timestamp = timedelta(seconds=timestamp_seconds)

                    try:
                        song_data = SongData(
                            title=song_data["track"]["title"],
                            artist=song_data["track"]["subtitle"],
                            original_file=original_file,
                            time=timestamp,
                            accuracy=song_data["location"]["accuracy"],
                        )
                        songs.append(song_data)
                    except Exception as e:
                        print(f"Error processing song data: {e}")
                        print(f"Song data: {song_data}")

            bar.finish()

        return songs

    def _clean(self, split_audio_folder: TemporaryDirectory, audio_file: NamedTemporaryFile) -> None:
        try:
            split_audio_folder.cleanup()
            os.remove(audio_file.name)
        except Exception as e:
            print(f"Error cleaning up: {e}")
