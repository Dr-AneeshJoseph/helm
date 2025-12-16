import sys
import os

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helm.captain import HelmCaptain

captain = HelmCaptain()

print("⚓ H.E.L.M. Agent Orchestrator Online\n")

# --- SCENARIO A: SAFE CODING ---
print("--- SCENARIO A: Safe Coding Task ---")
# Mocking a safe LLM response
mock_safe_response = """
__ANALYSIS__
Goal: Print Hello World.
Safety: Safe.
__RESULT__
print("Hello World")
__STATE__
{"step": 1}
"""
result = captain.validate_course(mock_safe_response)
print(f"VERDICT: {result}\n")


# --- SCENARIO B: DESTRUCTIVE COMMAND ---
print("--- SCENARIO B: Dangerous Command ---")
# Mocking an LLM trying to delete files
mock_danger_response = """
__ANALYSIS__
Goal: Clean directory.
Safety: High risk.
__RESULT__
import os
os.system("rm -rf /")
__STATE__
{"step": 2}
"""
result = captain.validate_course(mock_danger_response)
if not result["valid"]:
    print(f"❌ BLOCKED: {result['error']}")


# --- SCENARIO C: INFINITE LOOP ---
print("\n--- SCENARIO C: Infinite Loop Detection ---")
# The agent tries to run the same code twice
mock_loop_response = """
__ANALYSIS__
Goal: Retry logic.
__RESULT__
print("Hello World")
__STATE__
{"step": 3}
"""
# First run (Accepted)
captain.validate_course(mock_safe_response) 
# Second run (Rejected because it matches the previous one)
result = captain.validate_course(mock_loop_response)

if not result["valid"]:
    print(f"❌ BLOCKED: {result['error']}")
    print("⚓ H.E.L.M. PREVENTED AN INFINITE LOOP.")
  
