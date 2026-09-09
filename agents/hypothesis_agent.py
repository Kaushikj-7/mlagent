import json
from typing import Dict, Any
from agents.base_agent import BaseAgent

class HypothesisAgent(BaseAgent):
    """
    Hypothesis Generator Agent.
    Formulates novel, mathematically grounded, testable ML hypotheses.
    Reads prior hypotheses and historical mistakes from the Project Ledger
    to prevent redundancy and conceptual pitfalls.
    """

    SYSTEM_PROMPT = """You are an Academic Machine Learning Research Scientist.
Your objective is to propose concrete, testable empirical hypotheses in machine learning.
Focus on areas such as:
- Feature transformations and representations (e.g. power transforms, log-scaling, quantile normalization)
- Loss function variations and regularization (e.g. L1 vs L2, label smoothing, Huber loss)
- Model architecture variations (e.g. residual connections vs feed-forward, layer normalization)
- Optimization dynamics (e.g. learning rate warmups, decay schedules, gradient clipping)

Rules:
1. The experiment MUST be executable on standard CPU-friendly datasets from sklearn (e.g., make_regression, make_classification, load_diabetes, load_breast_cancer, load_wine). Do NOT use fetch_california_housing or external downloads.
2. The hypothesis MUST be quantifiable with a target metric (e.g., accuracy, MSE, R2 score, AUC).
3. Always provide a control baseline and an experimental variant.
4. Output MUST be valid JSON only.
"""

    def propose_hypothesis(self, domain_topic: str = "Tabular Feature Engineering and Neural Representations") -> Dict[str, Any]:
        past_hypotheses = self.ledger.get_past_hypotheses_for_prompt()
        past_mistakes = self.ledger.get_summary_of_mistakes_for_prompt()

        user_prompt = f"""Domain / Research Topic: {domain_topic}

{past_hypotheses}

{past_mistakes}

Please formulate a new, testable ML hypothesis. Output MUST be a JSON object with this exact schema:
{{
  "title": "<Concise research paper style title>",
  "statement": "<Formal, falsifiable scientific hypothesis>",
  "rationale": "<Theoretical or empirical reason why this should hold>",
  "target_metric": "<e.g. test_mse, test_accuracy, test_r2>",
  "dataset": "<e.g. synthetic_regression, load_diabetes, breast_cancer>",
  "baseline_description": "<Description of baseline model/pipeline>",
  "variant_description": "<Description of experimental variant testing the hypothesis>"
}}
"""
        response_text = self.llm.generate(user_prompt, system_instruction=self.SYSTEM_PROMPT)
        parsed = self.extract_json(response_text)

        if not parsed or "statement" not in parsed:
            parsed = {
                "title": f"Empirical Evaluation of Regularization in {domain_topic}",
                "statement": "L2 regularization reduces overfitting gap by >5% compared to unregularized baselines on noisy tabular datasets.",
                "rationale": "Shrinking weight magnitudes limits model sensitivity to feature noise.",
                "target_metric": "test_r2",
                "dataset": "synthetic_regression",
                "baseline_description": "Unregularized Linear baseline",
                "variant_description": "L2-regularized baseline"
            }

        try:
            from core.schemas import HypothesisSchema
            return HypothesisSchema.model_validate(parsed).model_dump()
        except Exception:
            return parsed
