import subprocess

def extract_audio(video_path: str, audio_path: str):
    subprocess.run(["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path], check=True)