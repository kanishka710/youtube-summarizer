import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_summary(transcript: str):
    model = genai.GenerativeModel('gemini-3.5-flash')
    
    prompt = f"""
    You are an expert video summarizer. Analyze the following transcript and return a JSON object with this structure:
    {{
      "title": "Title of the video",
      "brief_overview": "A 3-sentence summary.",
      "key_points": ["Point 1", "Point 2", "Point 3"],
      "timestamps": [{{"time": "00:00", "description": "Topic"}}]
    }}

    Transcript:
    ###
    {transcript}
    ###

    Return ONLY the raw JSON string. Do not include markdown code blocks, do not include introductory text, and do not include the word 'json'.
    """
    
    response = model.generate_content(prompt)
    return response.text