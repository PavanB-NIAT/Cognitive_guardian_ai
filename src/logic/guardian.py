from src.services.llm_connector import GeminiConnector
from src.logic.profiles import UserProfile
from src.logic.safety import SafetyModule

class CognitiveGuardian:
    def __init__(self):
        self.llm = GeminiConnector()
        self.safety = SafetyModule()

    def process_interaction(self, user_input, profile: UserProfile, chat_history):
        # 1. Safety Check
        is_safe, warning = self.safety.check_input(user_input)
        if not is_safe:
            yield warning
            return

        # 2. Construct Socratic System Prompt
        system_prompt = profile.get_system_persona()
        
        # 3. Add pedagogical constraints
        system_prompt += "\n\nCRITICAL RULE: Do not explain the concept yet. Ask the user to try to define it first based on their own knowledge."

        # 4. Stream response from LLM
        response_stream = self.llm.generate_stream(
            system_instruction=system_prompt,
            user_message=user_input,
            history=chat_history
        )
        
        for chunk in response_stream:
            yield chunk