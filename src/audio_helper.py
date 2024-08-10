import moviepy.editor as moviepy
import os
from tempfile import TemporaryDirectory, NamedTemporaryFile


def extract_audio(video_file: str) -> NamedTemporaryFile:
    video_file_name, _ = os.path.splitext(video_file)
    audio_file = NamedTemporaryFile(prefix=video_file_name, suffix=".mp3", delete=False)
    audio_file.close()

    print(f"Extracting audio from {video_file} to {audio_file}")

    video = moviepy.VideoFileClip(video_file)
    audio = video.audio

    audio.write_audiofile(audio_file.name)
    return audio_file


def split_audio(audio_file: NamedTemporaryFile, segment_duration_secs: int, segments_count: int = -1) -> TemporaryDirectory:
    split_audio_folder = f"{os.path.splitext(audio_file.name)[0]}_split"
    tmp_dir = TemporaryDirectory(prefix=split_audio_folder)

    audio = moviepy.AudioFileClip(audio_file.name)
    audio_duration = audio.duration

    count = 0
    for i in range(0, int(audio_duration), segment_duration_secs):
        end = min(i + segment_duration_secs, audio_duration)
        audio.subclip(i, end).write_audiofile(os.path.join(tmp_dir.name, f"{i}.mp3"))

        count += 1
        if segments_count != -1 and count > segments_count:
            break

    return tmp_dir
