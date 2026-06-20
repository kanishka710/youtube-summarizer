from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def get_video_id(youtube_url: str):
    """Extracts the video ID from a standard YouTube URL."""
    parsed_url = urlparse(youtube_url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query)['v'][0]
    return None

def fetch_transcript(video_url: str):
    video_id = get_video_id(video_url)
    if not video_id:
        return "Error: Invalid YouTube URL"
    
    try:
        # Initialize the API object
        yt = YouTubeTranscriptApi()
        
        # Use .fetch() instead of .get_transcript()
        transcript_list = yt.fetch(video_id)
        
        # Join the text segments
        full_text = " ".join([item.text for item in transcript_list])
        return full_text
    except Exception as e:
        return f"Error: Could not retrieve transcript. {str(e)}"