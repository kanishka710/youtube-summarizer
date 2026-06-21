from fastapi import FastAPI
from services.extractor import get_video_id, fetch_transcript
from services.llm import generate_summary
from services.transcriber import transcribe_audio # Assuming you put the Groq code here
from services.cache import get_cached_summary, set_cached_summary

app = FastAPI()

@app.get("/summarize")
def summarize(url: str,language: str = "English"):
    video_id = get_video_id(url)
    
    # 1. CHECK CACHE
    cached = get_cached_summary(video_id, language)
    if cached:
        return {"status": "success", "source": "cache", "summary": cached}
    
    # 2. COMPUTE (If cache miss)
    # Attempt to get subtitles
    transcript = fetch_transcript(url)
    # Fallback: If fetch_transcript returned an error, use Groq/Whisper
    if "Error" in transcript:
        transcript = transcribe_audio(url)
    
    # Generate the summary using Gemini
    summary = generate_summary(transcript, target_language=language)
    
    # 3. STORE RESULT
    set_cached_summary(video_id, language, summary)

    return {"status": "success", "source": "llm", "summary": summary}