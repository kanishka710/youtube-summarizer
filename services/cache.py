"""Redis-backed summary cache using Upstash."""

import json
from typing import Any

from services.config import CACHE_TTL_SECONDS, get_redis_client


def _build_cache_key(video_id: str, language: str) -> str:
    return f"summary:v={video_id}:lang={language}"


def get_cached_summary(video_id: str, language: str) -> dict[str, Any] | None:
    """Return a cached summary dict, or None on cache miss."""
    key = _build_cache_key(video_id, language)
    cached_data = get_redis_client().get(key)
    return json.loads(cached_data) if cached_data else None


def set_cached_summary(video_id: str, language: str, summary: dict[str, Any]) -> None:
    """Store a summary dict in cache with the configured TTL."""
    key = _build_cache_key(video_id, language)
    get_redis_client().setex(key, CACHE_TTL_SECONDS, json.dumps(summary))
