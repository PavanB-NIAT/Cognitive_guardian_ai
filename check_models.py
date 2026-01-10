import google.generativeai as genai
import os
from dotenv import load_dotenv
from pathlib import Path

# 1. Force load the .env file
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GOOGLE_API_KEY")
print(f"Key loaded: {api_key[:5]}...") # Check if key exists

# 2. Configure Google AI
genai.configure(api_key=api_key)

print("\n🔍 CHECKING AVAILABLE MODELS...")
print("--------------------------------")
try:
    count = 0
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ FOUND: {m.name}")
            count += 1
    if count == 0:
        print("❌ No models found! Your API key might be new or region-locked.")
except Exception as e:
    print(f"❌ Error: {e}")
print("--------------------------------")