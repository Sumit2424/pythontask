# ================================================================
# app.py
# FastAPI Backend - Main Application Entry Point
#
# Responsibilities:
#   ✔ Accept audio uploads from frontend
#   ✔ Save file temporarily
#   ✔ Convert audio → text using Speech-to-Text service
#   ✔ Extract tasks using rule-based NLP logic
#   ✔ Assign tasks to correct team member
#   ✔ Return clean JSON output
#
# This is the CONTROLLER of your backend architecture.
# ================================================================

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os

# Import service modules (these files we will create next)
from services.stt_service import speech_to_text
from nlp.pipeline import process_transcript as run_nlp_pipeline
from assingment.assingment_logic import assign_tasks


# ---------------------------------------------------------------
# Initialize FastAPI Application
# ---------------------------------------------------------------
app = FastAPI(
    title="Meeting Task Extraction Backend",
    description="Upload meeting audio, extract tasks using AI-powered NLP logic.",
    version="1.0.0"
)

# ---------------------------------------------------------------
# Enable CORS
# Allows frontend (HTML/React) to call backend API without issues.
# ---------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # Allow all origins (open during development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create temporary directory for uploaded audio files
TEMP_DIR = "backend/temp/uploaded_audio"
os.makedirs(TEMP_DIR, exist_ok=True)


# ---------------------------------------------------------------
# API: Upload Meeting Audio
#
# Steps:
#   1. Receive audio file (.mp3 / .wav)
#   2. Save to temp directory
#   3. Convert to text (Speech-to-Text)
#   4. Extract tasks from text (NLP)
#   5. Assign tasks to appropriate team member
#   6. Return JSON response
def _process_tasks(transcript: str, auto_assign: bool = True):
    """
    Run the NLP pipeline and optionally apply assignment logic.
    """
    tasks = run_nlp_pipeline(transcript)

    if auto_assign and tasks:
        return assign_tasks(tasks)

    return tasks


@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    # Save file
    file_path = f"{TEMP_DIR}/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # STT → Transcript
    transcript = speech_to_text(file_path)

    # Process transcript through hybrid pipeline
    tasks = _process_tasks(transcript, auto_assign=True)

    return {
        "transcript": transcript,
        "tasks": tasks
    }
# ---------------------------------------------------------------
# Health Check Route
# Used by developers & frontend to verify backend is running.
# ---------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "Backend Running Successfully 🚀"}
