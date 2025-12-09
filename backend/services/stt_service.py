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
import mimetypes

print("WORKING DIR:", os.getcwd())

load_dotenv(r"C:\Users\Admin\Desktop\task-python\backend\.env")

print("sumit debug",os.getenv("GEMINI_API_KEY"))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not GEMINI_API_KEY:
    raise Exception("❌ ERROR: Gemini API key missing. Add GEMINI_API_KEY to backend/.env")

genai.configure(api_key= GEMINI_API_KEY)

# Create Model Instance
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------------------------------------------------------
# Function: Convert Audio → Text using Gemini
# --------------------------------------------------------------

# def speech_to_text(audio_path: str) -> str:
#     """Convert an audio file into a transcript using the Gemini API."""
#     try:
#         audio_file = genai.upload_file(path=audio_path)
#         response = genai.generate_text(
#             model="models/gemini-1.5-flash",
#             audio=audio_file,
#         )
#         transcript = response.text.strip()
#         if not transcript:
#             raise ValueError("Empty transcript returned from Gemini API")
#         return transcript
#     except Exception as exc:
#         raise RuntimeError("Failed to transcribe audio with Gemini API") from exc
def speech_to_text(audio_path: str) -> str:
    """Convert an audio file into a transcript using the Gemini API."""
    try:
        # Detect MIME type
        mime_type, _ = mimetypes.guess_type(audio_path)
        if mime_type is None:
            mime_type = "audio/mpeg"  # fallback

        # Read audio bytes
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()

        print("🔊 STT DEBUG: Sending audio to Gemini...")
        print("MIME TYPE:", mime_type)

        # Call Gemini
        response = model.generate_content(
            [
                {
                    "mime_type": mime_type,
                    "data": audio_bytes
                },
                "Please transcribe this audio to text accurately."
            ]
        )

        transcript = response.text.strip()

        if not transcript:
            raise ValueError("❌ Empty transcript returned from Gemini API")

        print("🔊 STT SUCCESS: Transcript received.")
        return transcript

    except Exception as exc:
        print("❌ STT ERROR:", exc)
        raise RuntimeError("Failed to transcribe audio with Gemini API") from exc