import json
from typing import Dict, Any
from agents.base_agent import BaseAgent

class CriticAgent(BaseAgent):
    """
    Critic & Auditor Agent.
    Evaluates experiment execution, detects code bugs, methodological flaws
    (e.g., data leakage, biased metric calculation), determines scientific verdicts,
    and logs granular mistake records directly into the Project Ledger.
    """

    SYSTEM_PROMPT = """You are a Rigorous Academic Peer Reviewer and ML Code Auditor.
Your job is to audit an ML experiment execution for both code integrity and scientific validity.

You must examine:
1. Code execution status (did it crash, throw an exception, or time out?)
2. Methodological soundness:
   - Data leakage: Did scalers or encoders fit on test data?
   - Evaluation bias: Are baseline and variant evaluated on the exact same test split with the same metric?
   - Target metric calculation: Did it compute the right metric?
3. Scientific conclusions:
   - Do the numbers statistically or directionally support the hypothesis?
   - Or is the hypothesis refuted / inconclusive?

You must output a JSON object with:
{
  "verdict": "SUPPORTED" | "REFUTED" | "INCONCLUSIVE" | "CODE_ERROR" | "METHODOLOGY_FLAW",
  "critique_summary": "<concise academic evaluation of the findings>",
  "mistakes": [
    {
      "category": "CODE_BUG" | "DATA_LEAKAGE" | "METRIC_FLAW" | "HYPOTHESIS_FLAW",
      "description": "<clear description of what went wrong>",
      "suggested_fix": "<concrete steps to fix the code or methodology>"
    }
  ],
  "scientific_quality_score": <int between 1 and 10>
}
Output JSON ONLY.
"""

    def audit(self, hypothesis: Dict[str, Any], script_code: str, exec_result: Dict[str, Any]) -> Dict[str, Any]:
        """Audits the experiment and returns structured critique."""
        status = exec_result.get("status", "UNKNOWN")
        exit_code = exec_result.get("exit_code", 0)
        stdout = exec_result.get("stdout", "")
        stderr = exec_result.get("stderr", "")
        metrics = exec_result.get("metrics", {})

        user_prompt = f"""Hypothesis Statement: {hypothesis.get('statement')}
Target Metric: {hypothesis.get('target_metric')}

Experiment Code:
```python
{script_code[:2500]}
```

Execution Result:
Status: {status} (Exit Code: {exit_code})
Stdout:
{stdout[:1500]}

Stderr / Traceback:
{stderr[:1500]}

Extracted Metrics:
{json.dumps(metrics, indent=2)}

Perform your audit and return the JSON evaluation.
"""

        response_text = self.llm.generate(user_prompt, system_instruction=self.SYSTEM_PROMPT)
        audit_result = self.extract_json(response_text)

        # Fallback & safety net if code crashed but LLM hallucinated success
        if exit_code != 0:
            if not audit_result or audit_result.get("verdict") == "SUPPORTED":
                audit_result = {
                    "verdict": "CODE_ERROR",
                    "critique_summary": f"Experiment script failed during execution with exit code {exit_code}.",
                    "mistakes": [
                        {
                            "category": "CODE_BUG",
                            "description": f"Runtime exception encountered: {stderr[-300:] if stderr else 'Script failed to run'}",
                            "suggested_fix": "Fix traceback error, verify imports, and ensure proper variable names."
                        }
                    ],
                    "scientific_quality_score": 2
                }
            elif not audit_result.get("mistakes"):
                audit_result.setdefault("mistakes", []).append({
                    "category": "CODE_BUG",
                    "description": f"Subprocess exited with non-zero code {exit_code}: {stderr[-200:] if stderr else 'Execution error'}",
                    "suggested_fix": "Debug error traceback and fix code execution."
                })

        fallback_result = {
            "verdict": "INCONCLUSIVE",
            "critique_summary": "Unable to definitively parse audit. Defaulting to inconclusive.",
            "mistakes": [],
            "scientific_quality_score": 5
        }
        final_dict = audit_result or fallback_result
        try:
            from core.schemas import AuditReviewSchema
            return AuditReviewSchema.model_validate(final_dict).model_dump()
        except Exception:
            return final_dict
