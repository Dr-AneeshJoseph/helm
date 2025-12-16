# ⚓ H.E.L.M. (Heuristic Execution Logic Manager)

> **The Safety Governor for Autonomous AI Agents.**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


---

## ⚠️ The Problem
Autonomous Agents are powerful but prone to expensive failures:
* **Infinite Loops:** An agent gets stuck repeating "Thinking..." and burns $50 in API credits.
* **Destructive Actions:** An agent decides the best way to "clean up" is `rm -rf /`.
* **State Amnesia:** The agent forgets what it did 2 steps ago.

## 🛡️ The Solution
**H.E.L.M.** is an orchestration layer that sits between your Agent Loop and the LLM. It enforces "Plan-First" logic and mechanically blocks dangerous system calls.

### The Architecture
1.  **Layer 1: The Wheel (Prompt)**
    * Forces the agent to output `__ANALYSIS__` (Plan) and `__STATE__` (Memory) before acting.
2.  **Layer 2: The Hull (Sanitizer)**
    * Quarantines user input.
3.  **Layer 3: The Governor (Validator)**
    * **Loop Detection:** Uses fuzzy matching to kill the process if the agent repeats itself >90%.
    * **Syscall Lock:** Regex blocking of `os.system`, `subprocess`, and destructive file operations.

## 🚀 Quick Start
```python
from helm.captain import HelmCaptain

captain = HelmCaptain()

# Inside your Agent Loop:
llm_response = call_llm(prompt)
verdict = captain.validate_course(llm_response)

if verdict["valid"]:
    execute_code(verdict["action"])
else:
    print(f"STOP: {verdict['error']}")

