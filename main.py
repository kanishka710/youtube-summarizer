"""FastAPI backend for YouTube video summarization."""

import logging

from fastapi import FastAPI, HTTPException

from services.cache import get_cached_summary, set_cached_summary
from services.extractor import TranscriptNotFoundError, fetch_transcript, get_video_id
from services.llm import generate_summary
from services.transcriber import transcribe_audio

logger = logging.getLogger(__name__)

app = FastAPI()


def _get_transcript(video_url: str, video_id: str) -> str:
    """Fetch transcript from captions, falling back to audio transcription."""
    try:
        return fetch_transcript(video_url, video_id=video_id)
    except TranscriptNotFoundError as exc:
        logger.info("Caption fetch failed, falling back to audio: %s", exc)
        try:
            return transcribe_audio(video_url)
        except Exception as fallback_exc:
            raise HTTPException(
                status_code=422,
                detail=(
                    "Could not extract transcript. The video may be private "
                    f"or protected by anti-bot measures. ({fallback_exc})"
                ),
            ) from fallback_exc


@app.get("/summarize")
def summarize(url: str, language: str = "English"):
    """Summarize a YouTube video by URL in the requested language."""
    try:
        video_id = get_video_id(url)
        if not video_id:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")

        cached = get_cached_summary(video_id, language)
        if cached:
            return {"status": "success", "source": "cache", "summary": cached}

        transcript = _get_transcript(url, video_id)
        summary = generate_summary(transcript, language=language)
        set_cached_summary(video_id, language, summary)

        return {"status": "success", "source": "llm", "summary": summary}
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to process video")
        raise HTTPException(
            status_code=500, detail=f"Failed to process video: {exc}"
        ) from exc
