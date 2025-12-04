# ================================================================
# stt_service.py
#
# Speech-to-Text (STT) Service Module
#
# Responsibilities:
#   ✔ Convert uploaded audio file → text transcript
#   ✔ Use Gemini API for transcription (allowed)
#   ✔ Return raw transcript back to app.py
#
# IMPORTANT:
#   - This is the ONLY part where external AI models are allowed.
#   - Task extraction is done using our own rule-based NLP logic.
# ===============================================================

import google.generativeai as genai 
import os 
from dotenv import load_dotenv 
print("WORKING DIR:", os.getcwd())

load_dotenv(r"C:\Users\Admin\Desktop\task-python\backend\.env")

print("sumit debug",os.getenv("GEMINI_API_KEY"))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not GEMINI_API_KEY:
    raise Exception("❌ ERROR: Gemini API key missing. Add GEMINI_API_KEY to backend/.env")

genai.configure(api_key= GEMINI_API_KEY)


# ---------------------------------------------------------------
# Function: Convert Audio → Text using Gemini
# --------------------------------------------------------------

def speech_to_text(audio_path: str) -> str:
    """Convert an audio file into a transcript using the Gemini API."""
    try:
        audio_file = genai.upload_file(path=audio_path)
        response = genai.generate_text(
            model="models/gemini-1.5-flash",
            audio=audio_file,
        )
        transcript = response.text.strip()
        if not transcript:
            raise ValueError("Empty transcript returned from Gemini API")
        return transcript
    except Exception as exc:
        raise RuntimeError("Failed to transcribe audio with Gemini API") from exc
