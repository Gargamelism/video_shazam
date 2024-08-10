import moviepy.editor as moviepy
import os


def extract_audio(video_file: str) -> str:
    video_file_name, _ = os.path.splitext(video_file)
    audio_file = f"{video_file_name}.mp3"
    print(f"Extracting audio from {video_file} to {audio_file}")
    if os.path.exists(audio_file):
        return audio_file

    video = moviepy.VideoFileClip(video_file)
    audio = video.audio

    audio.write_audiofile(audio_file)
    return audio_file


def split_audio(audio_file: str, segment_duration: int) -> str:
    split_audio_folder = f"{os.path.splitext(audio_file)[0]}_split"
    if os.path.exists(split_audio_folder):
        return split_audio_folder

    os.makedirs(split_audio_folder, exist_ok=True)

    audio = moviepy.AudioFileClip(audio_file)
    audio_duration = audio.duration

    for i in range(0, int(audio_duration), segment_duration):
        end = min(i + segment_duration, audio_duration)
        audio.subclip(i, end).write_audiofile(f"{split_audio_folder}/{i}.mp3")

    return split_audio_folder
