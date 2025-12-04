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
from backend.services.stt_service import speech_to_text
from backend.nlp.nlp_rules import extract_tasks
from backend.assingment.assingment_logic import assign_tasks


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
# ---------------------------------------------------------------
@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    """
    Upload meeting audio and extract tasks.
    """

    # Step A: Save file temporarily
    file_path = f"{TEMP_DIR}/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Step B: Convert Audio → Text using Gemini / Whisper
    transcript = speech_to_text(file_path)

    # Step C: Task Extraction using NLP rules
    extracted_tasks = extract_tasks(transcript)

    # Step D: Assign tasks to team members
    final_output = assign_tasks(extracted_tasks)

    # Step E: Return final data
    return {
        "transcript": transcript,
        "tasks": final_output
    }


# ---------------------------------------------------------------
# Health Check Route
# Used by developers & frontend to verify backend is running.
# ---------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "Backend Running Successfully 🚀"}
