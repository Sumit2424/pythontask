import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv("backend/.env")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("\n🔍 Listing Available Gemini Models...\n")

models = genai.list_models()

for m in models:
    print("MODEL:", m.name)
    print("  Supported methods:", m.supported_generation_methods)
    print("  -----------------------------")
