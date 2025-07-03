import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Read key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ API key not found in .env")
    exit()

# Set Gemini key
genai.configure(api_key=api_key)

try:
    models = genai.list_models()
    print("✅ Gemini API is ENABLED! Available models:")
    for m in models:
        print("-", m.name, m.supported_generation_methods)
except Exception as e:
    print("❌ Gemini API NOT working:")
    print(e)
