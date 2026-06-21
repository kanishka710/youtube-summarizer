"""Shared configuration and environment setup for the summarizer services."""

import os

import redis
from dotenv import load_dotenv

load_dotenv()

CACHE_TTL_SECONDS = 30 * 24 * 60 * 60
GEMINI_MODEL = "gemini-3.5-flash"
WHISPER_MODEL = "whisper-large-v3"
API_BASE_URL = "http://127.0.0.1:8000"

_redis_client = None


def get_redis_client():
    """Return a lazily initialized Upstash Redis client."""
    global _redis_client
    if _redis_client is None:
        port = os.getenv("UPSTASH_REDIS_PORT")
        _redis_client = redis.Redis(
            host=os.getenv("UPSTASH_REDIS_HOST"),
            port=int(port) if port else 6379,
            password=os.getenv("UPSTASH_REDIS_PASSWORD"),
            ssl=True,
            ssl_cert_reqs=None,
            decode_responses=True,
        )
    return _redis_client


def get_google_api_key() -> str | None:
    return os.getenv("GOOGLE_API_KEY")


def get_groq_api_key() -> str | None:
    return os.getenv("GROQ_API_KEY")
