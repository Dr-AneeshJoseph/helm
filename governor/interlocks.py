import re
from Levenshtein import ratio

class SafetyGovernor:
    """
    Layer 3: The Governor
    Prevents Infinite Loops and Destructive Commands.
    """
    
    def __init__(self):
        self.history = []
        # Commands that effectively brick a system or delete data
        self.DANGEROUS_PATTERNS = [
            r"rm\s+-rf", r"shutil\.rmtree", r"os\.remove", 
            r"os\.system", r"subprocess\.call", r"format\s+[a-z]:"
        ]

    def check_safety(self, agent_response: str):
        """
        Returns (is_safe: bool, error: str)
        """
        if not agent_response:
            return False, "EMPTY RESPONSE"

        # 1. DANGER CHECK (Regex)
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, agent_response):
                return False, f"SAFETY LOCK: Dangerous command '{pattern}' detected."

        # 2. LOOP DETECTION (Fuzzy Matching)
        # Check if the current response is >90% similar to the last response
        if self.history:
            last_response = self.history[-1]
            similarity = ratio(agent_response, last_response)
            if similarity > 0.9:
                return False, "LOOP DETECTED: Agent is repeating itself. Terminating."

        # Update History (Keep last 3 turns)
        self.history.append(agent_response)
        if len(self.history) > 3:
            self.history.pop(0)

        return True, "SAFE"
      
