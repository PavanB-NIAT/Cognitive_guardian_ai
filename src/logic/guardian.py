# logic/guardian_brain.py
import streamlit as st
import google.generativeai as genai

class GuardianBrain:
    def __init__(self):
        # 1. Fail-safe Authentication
        try:
            api_key = st.secrets["GOOGLE_API_KEY"]
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception:
            self.model = None

    def generate_response(self, user_input, history, age, role, style):
        if not self.model:
            return "⚠️ System Error: API Key missing. Please check .streamlit/secrets.toml"

        # 2. The "Two-Step" Persona Engine
        system_prompt = self._construct_persona(age, role, style)
        
        try:
            # 3. Stateless Execution (Faster for Demos)
            full_prompt = f"{system_prompt}\n\n[USER SAYS]: {user_input}"
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"⚠️ Cognitive Connection Error: {str(e)}"

    def _construct_persona(self, age, role, style):
        """
        Dynamically adjusts the AI's teaching strategy.
        """
        # TONE & METAPHOR SELECTION
        if "Child" in role or age < 12:
            tone = "Use emojis 🌟. Be super friendly. Use analogies like Lego, Minecraft, or Pizza."
        elif "Developer" in role:
            tone = "Be strictly technical. Use code blocks. No small talk."
        else:
            tone = "Professional, clear, and Socratic (like a mentor)."

        # THE TWO-STEP INSTRUCTION
        return f"""
        You are 'Cognitive Guardian'.
        USER PROFILE: Age {age} | Role: {role} | Style: {style}
        
        YOUR STRICT BEHAVIOR PROTOCOL:
        
        STEP 1: THE SCAFFOLD (If the user asks a new question)
        - Do NOT give the direct answer immediately.
        - Explain the concept simply using your tone ({tone}).
        - Ask ONE short, fun guiding question to make them think.
        
        STEP 2: THE REVEAL (If the user tries to answer or asks again)
        - If the user answers your question (even wrongly), PRAISE them.
        - Then give the CLEAR, FINAL answer.
        - Don't trap them in a loop. Guide -> Then Solve.
        """
