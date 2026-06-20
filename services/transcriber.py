import os
import uuid
import yt_dlp
from groq import Groq

def transcribe_audio(video_url: str):
    # Ensure the temp folder exists
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        
    unique_id = uuid.uuid4().hex
    # Path inside the temp directory
    temp_filename = os.path.join(temp_dir, f"audio_{unique_id}")
    final_filepath = f"{temp_filename}.mp3"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        'outtmpl': f'{temp_filename}.%(ext)s',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        with open(final_filepath, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(final_filepath, file.read()),
                model="whisper-large-v3",
            )
        return transcription.text
    finally:
        # Cleanup
        if os.path.exists(final_filepath):
            os.remove(final_filepath)