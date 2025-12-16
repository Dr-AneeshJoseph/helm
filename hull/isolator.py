import re

class HullIsolator:
    """
    Layer 2: The Hull
    Quarantines input and extracts output.
    """
    
    @staticmethod
    def quarantine_input(user_query: str) -> str:
        safe_query = user_query.replace('"""', "'")
        return f'"""\n{safe_query}\n"""'

    @staticmethod
    def extract_result(llm_response: str) -> str:
        match = re.search(r"__RESULT__\s*(.*?)\s*(__STATE__|$)", llm_response, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None
      
