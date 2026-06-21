"""Timestamp parsing and YouTube URL helpers."""

from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


def time_to_seconds(time_str: str) -> int:
    """Convert 'MM:SS' or 'HH:MM:SS' to total seconds."""
    parts = time_str.split(":")
    if len(parts) not in (2, 3):
        raise ValueError(f"Invalid time format: {time_str!r}")

    try:
        numeric_parts = [int(part) for part in parts]
    except ValueError as exc:
        raise ValueError(f"Invalid time format: {time_str!r}") from exc

    if len(numeric_parts) == 2:
        minutes, seconds = numeric_parts
        return minutes * 60 + seconds

    hours, minutes, seconds = numeric_parts
    return hours * 3600 + minutes * 60 + seconds


def build_timestamp_url(video_url: str, seconds: int) -> str:
    """Build a YouTube URL that jumps to the given timestamp in seconds."""
    parsed = urlparse(video_url)
    query_params = parse_qs(parsed.query)
    query_params["t"] = [str(seconds)]
    new_query = urlencode(query_params, doseq=True)
    return urlunparse(parsed._replace(query=new_query))
