import json
from pathlib import Path
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from execution.runner import ExperimentRunner

class RefinerAgent(BaseAgent):
    """
    Refiner & Self-Healing Fixer Agent.
    Reads mistakes recorded in the Project Ledger, diagnoses the root cause,
    generates a corrected/repaired version of the experiment code,
    re-executes the experiment, and logs the fix resolution back into the ledger.
    """

    SYSTEM_PROMPT = """You are an Autonomous Code Debugger and Machine Learning Refiner.
Your mission is to fix mistakes, bugs, or methodological flaws recorded in the Project Ledger.

You are given:
1. The broken or flawed experiment script.
2. The exact mistakes and diagnosis logged by the Critic Agent.
3. The execution traceback / stderr.

Your task:
- Correct the code so that it runs successfully and cleanly.
- Maintain the original scientific hypothesis and dataset.
- STRICT CONSTRAINT: Do NOT import torch, tensorflow, or jax (they are not installed). Use only scikit-learn, numpy, pandas, scipy.
- Ensure all imports and metrics calculation are valid.
- Output ONLY the complete, fixed Python code inside a ```python ... ``` block.
"""

    def fix_and_reexecute(
        self,
        script_path: Path,
        hypothesis: Dict[str, Any],
        mistakes: List[Dict[str, Any]],
        stderr: str,
        runner: ExperimentRunner,
        ledger_entry_index: int
    ) -> Dict[str, Any]:
        """Repairs the experiment script, re-runs it, and updates the ledger."""
        try:
            with open(script_path, "r", encoding="utf-8") as f:
                original_code = f.read()
        except Exception:
            original_code = ""

        mistakes_summary = "\n".join([
            f"- [{m.get('category', 'BUG')}] {m.get('description')}. Suggested Fix: {m.get('suggested_fix')}"
            for m in mistakes
        ])

        user_prompt = f"""Target Hypothesis: {hypothesis.get('statement')}

Mistakes Logged in Project Ledger:
{mistakes_summary}

Execution Traceback / Error:
{stderr[:1500]}

Original Code:
```python
{original_code}
```

Provide the complete fixed Python code that resolves all these mistakes.
"""

        response_text = self.llm.generate(user_prompt, system_instruction=self.SYSTEM_PROMPT)
        fixed_code = self.extract_code(response_text)

        # Write back fixed code
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(fixed_code)

        print(f"[RefinerAgent] Code repaired. Re-executing {script_path.name}...")
        re_result = runner.run_script(script_path)

        resolved_status = "RESOLVED" if re_result.get("status") == "SUCCESS" else "UNRESOLVED"

        refinement_record = {
            "applied": True,
            "fix_agent": "RefinerAgent",
            "changes_made": f"Addressed mistakes: {[m.get('category') for m in mistakes]}",
            "re_execution_result": re_result,
            "status": resolved_status
        }

        try:
            from core.schemas import RefinementSchema
            refinement_record = RefinementSchema.model_validate(refinement_record).model_dump()
        except Exception:
            pass

        # Update ledger with the fix
        self.ledger.update_entry(ledger_entry_index, {"refinement": refinement_record})
        print(f"[RefinerAgent] Ledger updated with fix status: {resolved_status}")

        return refinement_record
