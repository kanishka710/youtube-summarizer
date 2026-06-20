import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_summary(transcript: str, target_language: str = "English"):
    model = genai.GenerativeModel('gemini-3.5-flash')
    
    prompt = f"""
    You are an expert video summarizer. Analyze the following transcript and return a JSON object.
    
    IMPORTANT: You must write the entire output in {target_language}.
    
    Structure:
    {{
      "title": "Title of the video in {target_language}",
      "brief_overview": "A 3-sentence summary in {target_language}.",
      "key_points": ["Point 1 in {target_language}", "Point 2 in {target_language}"],
      "timestamps": [{{"time": "00:00", "description": "Topic description in {target_language}"}}]
    }}

    Transcript:
    ###
    {transcript}
    ###

    Return ONLY the raw JSON string. Do not include markdown code blocks, do not include introductory text, and do not include the word 'json'.
    """
    
    response = model.generate_content(prompt)
    return response.text