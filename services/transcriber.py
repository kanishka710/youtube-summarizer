"""Audio download and Groq Whisper transcription fallback."""

import os
import uuid

import yt_dlp
from groq import Groq

from services.config import WHISPER_MODEL, get_groq_api_key


def transcribe_audio(video_url: str) -> str:
    """Download video audio and transcribe it with Groq Whisper."""
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    unique_id = uuid.uuid4().hex
    temp_filename = os.path.join(temp_dir, f"audio_{unique_id}")
    final_filepath = f"{temp_filename}.mp3"

    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": f"{temp_filename}.%(ext)s",
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
    }
    if os.path.exists("cookies.txt"):
        ydl_opts["cookiefile"] = "cookies.txt"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        client = Groq(api_key=get_groq_api_key())
        with open(final_filepath, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(final_filepath, file.read()),
                model=WHISPER_MODEL,
            )
        return transcription.text
    finally:
        if os.path.exists(final_filepath):
            os.remove(final_filepath)
