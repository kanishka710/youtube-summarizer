"""Streamlit frontend for the YouTube video summarizer."""

import json

import requests
import streamlit as st

from services.config import API_BASE_URL
from services.utils import build_timestamp_url, time_to_seconds


def _normalize_summary(summary):
    """Parse summary if it is a legacy cached JSON string."""
    if isinstance(summary, str):
        # TODO: Remove after old cache entries expire.
        return json.loads(summary)
    return summary


def _render_summary(summary: dict, video_url: str) -> None:
    """Render a structured summary in the Streamlit UI."""
    st.success("Summary Ready!")
    st.subheader(summary.get("title", "No Title"))
    st.info(summary.get("brief_overview", ""))

    with st.expander("Key Takeaways", expanded=True):
        for point in summary.get("key_points", []):
            st.write(f"• {point}")

    with st.expander("Timeline/Timestamps"):
        for item in summary.get("timestamps", []):
            time_label = item["time"]
            description = item["description"]
            try:
                seconds = time_to_seconds(time_label)
                jump_url = build_timestamp_url(video_url, seconds)
                st.markdown(f"[{time_label} - {description}]({jump_url})")
            except ValueError:
                st.write(f"{time_label} - {description}")


st.set_page_config(page_title="AI Video Summarizer", layout="wide")

st.title("YouTube Video Summarizer")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    url = st.text_input("YouTube URL:")
with col2:
    language = st.selectbox(
        "Language", ["English", "Spanish", "Hindi", "French", "German"]
    )

if st.button("Generate Summary"):
    if not url:
        st.warning("Please enter a URL.")
    else:
        with st.spinner("Processing... this might take a moment if the video is long."):
            try:
                response = requests.get(
                    f"{API_BASE_URL}/summarize",
                    params={"url": url, "language": language},
                )
                data = response.json()

                if data["status"] == "success":
                    summary = _normalize_summary(data["summary"])
                    _render_summary(summary, url)
                else:
                    st.error(f"Error: {data.get('message', 'Unknown error')}")
            except Exception as exc:
                st.error(f"Could not connect to backend: {exc}")
