from fastapi import FastAPI
from services.extractor import fetch_transcript
from services.llm import generate_summary
from services.transcriber import transcribe_audio # Assuming you put the Groq code here

app = FastAPI()

@app.get("/summarize")
def summarize(url: str):
    # 1. Attempt to get subtitles
    transcript = fetch_transcript(url)
    
    # 2. Fallback: If fetch_transcript returned an error, use Groq/Whisper
    if "Error" in transcript:
        transcript = transcribe_audio(url)
    
    # 3. Generate the summary using Gemini
    summary = generate_summary(transcript)
    
    return {"status": "success", "summary": summary}