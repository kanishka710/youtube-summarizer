from fastapi import FastAPI, HTTPException
from services.extractor import get_video_id, fetch_transcript
from services.llm import generate_summary
from services.transcriber import transcribe_audio
from services.cache import get_cached_summary, set_cached_summary

app = FastAPI()

@app.get("/summarize")
def summarize(url: str,language: str = "English"):
    try:
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
            try:
                transcript = transcribe_audio(url)
            except Exception as e:
        # If the fallback also fails, tell the user WHY instead of crashing
                return {"status": "error", "message": "Could not extract transcript. The video may be private or protected by anti-bot measures."}
        
        # Generate the summary using Gemini
        summary = generate_summary(transcript, target_language=language)
        
        # 3. STORE RESULT
        set_cached_summary(video_id, language, summary)

        return {"status": "success", "source": "llm", "summary": summary}
    except Exception as e:
        # Log the error and tell the user exactly what happened
        print(f"Error encountered: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process video: {str(e)}")