import streamlit as st
import requests
import json
from services.utils import time_to_seconds

st.set_page_config(page_title="AI Video Summarizer", layout="wide")

st.title("Youtube Video Summarizer")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    url = st.text_input("YouTube URL:")
with col2:
    language = st.selectbox("Language", ["English", "Spanish", "Hindi", "French", "German"])

if st.button("Generate Summary"):
    if not url:
        st.warning("Please enter a URL.")
    else:
        with st.spinner("Processing... this might take a moment if the video is long."):
            try:
                # Call your FastAPI backend
                response = requests.get(f"http://127.0.0.1:8000/summarize?url={url}&language={language}")
                data = response.json()
                
                if data["status"] == "success":
                    summary = data["summary"]
                    # If summary is a string (due to LLM response), parse it
                    if isinstance(summary, str):
                        summary = json.loads(summary)
                    
                    # Display UI
                    st.success("Summary Ready!")
                    st.subheader(summary.get("title", "No Title"))
                    st.info(summary.get("brief_overview", ""))
                    
                    with st.expander("Key Takeaways", expanded=True):
                        for point in summary.get("key_points", []):
                            st.write(f"• {point}")
                    
                    with st.expander("Timeline/Timestamps"):
                        for item in summary.get("timestamps", []):
                            seconds = time_to_seconds(item['time'])
                            # Construct the YouTube URL with the time offset
                            jump_url = f"{url}&t={seconds}s"
                            
                            # Display as a clickable button or markdown link
                            st.markdown(f"[{item['time']} - {item['description']}]({jump_url})")
                            
                else:
                    st.error(f"Error: {data.get('message', 'Unknown error')}")
            except Exception as e:
                st.error(f"Could not connect to backend: {e}")