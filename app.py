import streamlit as st
import requests

st.title("YouTube Summarizer")

url = st.text_input("Paste your YouTube URL:")
language = st.selectbox("Select Summary Language", ["English", "Spanish", "Hindi", "French", "German"])

if st.button("Summarize"):
    if url:
        with st.spinner("Analyzing video..."):
            # Call your FastAPI backend
            try:
                response = requests.get(f"http://127.0.0.1:8000/summarize?url={url}&language={language}")
                print("Status Code:", response.status_code)
                print("Raw Response:", response.text)
                data = response.json()
                
                if data["status"] == "success":
                    summary = data["summary"]
                    # Display the JSON output nicely
                    st.success("Summary Generated!")
                    st.json(summary) # Streamlit renders JSON objects beautifully
                else:
                    st.error("Error generating summary.")
            except Exception as e:
                st.error(f"Connection error: {e}")
    else:
        st.warning("Please enter a URL first.")