"""Gemini-based transcript summarization."""

import json
import re
from typing import Any

import google.generativeai as genai

from services.config import GEMINI_MODEL, get_google_api_key

genai.configure(api_key=get_google_api_key())


def _parse_summary_response(raw_text: str) -> dict[str, Any]:
    """Parse LLM output into a summary dict, stripping markdown fences if present."""
    text = raw_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"LLM returned invalid JSON: {exc}") from exc


def generate_summary(transcript: str, language: str = "English") -> dict[str, Any]:
    """Generate a structured video summary from a transcript in the given language."""
    model = genai.GenerativeModel(GEMINI_MODEL)

    prompt = f"""
    You are an expert video summarizer. Analyze the following transcript and return a JSON object.

    IMPORTANT: You must write the entire output in {language}.

    Structure:
    {{
      "title": "Title of the video in {language}",
      "brief_overview": "A 3-sentence summary in {language}.",
      "key_points": ["Point 1 in {language}", "Point 2 in {language}"],
      "timestamps": [{{"time": "00:00", "description": "Topic description in {language}"}}]
    }}

    Transcript:
    ###
    {transcript}
    ###

    Return ONLY the raw JSON string. Do not include markdown code blocks, do not include introductory text, and do not include the word 'json'.
    """

    response = model.generate_content(prompt)
    return _parse_summary_response(response.text)
