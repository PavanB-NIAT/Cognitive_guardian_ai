import re

class SafetyModule:
    def check_input(self, text: str):
        """Basic keyword filtering for child safety."""
        unsafe_keywords = ["kill", "hurt", "bomb", "suicide", "cheat"]
        for word in unsafe_keywords:
            if word in text.lower():
                return False, "I cannot discuss that topic. Let's focus on learning something positive!"
        return True, ""