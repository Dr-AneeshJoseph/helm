import os
from .hull.isolator import HullIsolator
from .governor.interlocks import SafetyGovernor

class HelmCaptain:
    def __init__(self):
        self.isolator = HullIsolator()
        self.governor = SafetyGovernor()
        
        # Load Prompt
        prompt_path = os.path.join(os.path.dirname(__file__), 'wheel', 'agent_prompt.md')
        with open(prompt_path, 'r') as f:
            self.base_prompt = f.read()

    def steer(self, user_query: str, history_str: str = ""):
        """
        Constructs the safe prompt.
        """
        quarantined = self.isolator.quarantine_input(user_query)
        return f"{self.base_prompt}\n\nHISTORY:\n{history_str}\n\nTASK:\n{quarantined}"

    def validate_course(self, llm_raw_response: str):
        """
        Validates the Agent's output.
        """
        # 1. Extract
        action = self.isolator.extract_result(llm_raw_response)
        if not action:
            return {"valid": False, "error": "Format Error"}

        # 2. Govern (Safety Check)
        is_safe, msg = self.governor.check_safety(action)

        if is_safe:
            return {"valid": True, "action": action, "status": "ON_COURSE"}
        else:
            return {"valid": False, "error": msg, "rejected_action": action}
          
