"""YouTube transcript extraction via youtube-transcript-api."""

from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi


class TranscriptNotFoundError(Exception):
    """Raised when a video's transcript cannot be retrieved."""


def get_video_id(video_url: str) -> str | None:
    """Extract the video ID from a standard YouTube URL."""
    parsed_url = urlparse(video_url)
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]
    if parsed_url.hostname in ("www.youtube.com", "youtube.com"):
        if parsed_url.path == "/watch":
            query_params = parse_qs(parsed_url.query)
            video_ids = query_params.get("v")
            if video_ids:
                return video_ids[0]
    return None


def fetch_transcript(video_url: str, video_id: str | None = None) -> str:
    """
    Fetch the full transcript text for a YouTube video.

    Raises:
        ValueError: If the URL is invalid or the video ID cannot be determined.
        TranscriptNotFoundError: If captions are unavailable or fetch fails.
    """
    resolved_video_id = video_id or get_video_id(video_url)
    if not resolved_video_id:
        raise ValueError("Invalid YouTube URL")

    try:
        yt = YouTubeTranscriptApi()
        transcript_list = yt.fetch(resolved_video_id)
        return " ".join(item.text for item in transcript_list)
    except Exception as exc:
        raise TranscriptNotFoundError(f"Could not retrieve transcript: {exc}") from exc
