# YouTube Video Summarizer

Summarize YouTube videos from a URL. The app extracts captions when available, falls back to audio transcription via Groq Whisper when needed, and generates a structured summary with Gemini. Results are cached in Upstash Redis.
<img width="1726" height="802" alt="image" src="https://github.com/user-attachments/assets/83a4a760-af2e-485e-9426-1ecb98730c00" />

## Architecture

This app runs as **two separate processes**:

1. **FastAPI backend** (`main.py`) — handles transcript extraction, summarization, and caching
2. **Streamlit frontend** (`app.py`) — UI that calls the backend at `http://127.0.0.1:8000` by default

Both must be running for the UI to work.

## Prerequisites

- Python 3.11 or newer
- [FFmpeg](https://ffmpeg.org/download.html) on your PATH (required for audio extraction fallback)
- API keys for:
  - [Google Gemini](https://aistudio.google.com/apikey)
  - [Groq](https://console.groq.com/)
  - [Upstash Redis](https://upstash.com/)

## Setup

1. Clone the repository and enter the project directory.

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   For development tools (Black):

   ```bash
   pip install black
   ```

4. Create a `.env` file in the project root with your credentials:

   ```env
   GOOGLE_API_KEY=your_google_api_key
   GROQ_API_KEY=your_groq_api_key
   UPSTASH_REDIS_HOST=your_upstash_host
   UPSTASH_REDIS_PORT=6379
   UPSTASH_REDIS_PASSWORD=your_upstash_password
   ```

## Running

Start the backend and frontend in **two separate terminals**.

**Terminal 1 — API:**

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 — UI:**

```bash
streamlit run app.py
```

Open the URL shown by Streamlit (typically `http://localhost:8501`), paste a YouTube URL, choose a language, and click **Generate Summary**.

## Optional: YouTube cookies

For videos that require authentication, place a `cookies.txt` file in the project root. It is used by yt-dlp during audio transcription fallback. This file is gitignored and must be exported from your browser separately.

## Project layout

```
youtube-summarizer/
├── main.py              # FastAPI backend
├── app.py               # Streamlit frontend
├── requirements.txt     # Runtime dependencies
├── pyproject.toml       # Project metadata and Black config
└── services/
    ├── config.py        # Environment and constants
    ├── cache.py         # Redis summary cache
    ├── extractor.py     # YouTube caption extraction
    ├── transcriber.py   # Audio download + Groq Whisper
    ├── llm.py           # Gemini summarization
    └── utils.py         # Timestamp helpers
```
