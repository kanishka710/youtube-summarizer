import os
import yt_dlp
from groq import Groq

def transcribe_audio(video_url: str):
    # 1. Download audio using yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        'outtmpl': 'temp_audio.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # 2. Send to Groq for Whisper transcription
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    with open("temp_audio.mp3", "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=("temp_audio.mp3", file.read()),
            model="whisper-large-v3",
        )
    
    os.remove("temp_audio.mp3") # Clean up
    return transcription.text