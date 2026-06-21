import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to Upstash Redis
# Use the credentials from your Upstash console
redis_client = redis.Redis(
    host=os.getenv("UPSTASH_REDIS_HOST"),
    port=int(os.getenv("UPSTASH_REDIS_PORT")),
    password=os.getenv("UPSTASH_REDIS_PASSWORD"),
    ssl=True,      
    ssl_cert_reqs=None,
    decode_responses=True
)

def get_cached_summary(video_id: str, language: str):
    key = f"summary:v={video_id}:lang={language}"
    cached_data = redis_client.get(key)
    return json.loads(cached_data) if cached_data else None

def set_cached_summary(video_id: str, language: str, summary: dict):
    key = f"summary:v={video_id}:lang={language}"
    # Save as JSON string with 30 days (2592000 seconds) expiration
    redis_client.setex(key, 2592000, json.dumps(summary))