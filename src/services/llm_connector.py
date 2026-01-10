import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

# --- FIX: Force load the .env file from the project root ---
# This finds the file even if VS Code doesn't inject it automatically
root_dir = Path(__file__).resolve().parent.parent.parent
env_file_path = root_dir / ".env"

print(f"Loading API Key from: {env_file_path}") # Debug print
load_dotenv(dotenv_path=env_file_path)
# -----------------------------------------------------------

class GeminiConnector:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("❌ GOOGLE_API_KEY not found! Please check your .env file.")
        
        # ... rest of your code ...
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_stream(self, system_instruction, user_message, history=[]):
        """
        Streams response from Gemini with full context.
        """
        # Convert streamlit history to Gemini format if needed
        # For simplicity, we construct a raw prompt chain here or use chat session
        chat = self.model.start_chat(history=[])
        
        # Inject the "Guardian" system instruction essentially as the first message context
        full_prompt = f"""
        [SYSTEM INSTRUCTION - DO NOT IGNORE]
        {system_instruction}
        
        [USER MESSAGE]
        {user_message}
        """
        
        response = chat.send_message(full_prompt, stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text