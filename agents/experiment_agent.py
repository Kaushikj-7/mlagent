from pathlib import Path
from typing import Dict, Any
from agents.base_agent import BaseAgent
from core.config import Config

class ExperimentAgent(BaseAgent):
    """
    Experiment Designer & Code Generator Agent.
    Synthesizes a self-contained, reproducible Python ML experiment script.
    Crucially consults the Project Ledger to prevent recurring code errors,
    data leakage, or import mistakes.
    """

    SYSTEM_PROMPT = """You are an Expert Machine Learning Research Engineer.
Your task is to write a clean, self-contained, robust Python script to empirically test a scientific ML hypothesis.

Requirements for the script:
1. STRICT ENVIRONMENT CONSTRAINT: Do NOT import torch, torchvision, tensorflow, or jax. They are NOT installed.
   You MUST use `scikit-learn` (`sklearn`), `numpy`, `pandas`, `scipy`.
   For neural networks, use `sklearn.neural_network.MLPRegressor` or `sklearn.neural_network.MLPClassifier`.
2. Dataset: Use self-contained built-in datasets from `sklearn.datasets`:
   - For regression: `make_regression(n_samples=1000, n_features=10, noise=10.0, random_state=42)` or `load_diabetes()`
   - For classification: `make_classification(n_samples=1000, n_features=10, random_state=42)` or `load_breast_cancer()`
   - Do NOT use `fetch_california_housing` or any fetch_* dataset that requires external file caching or network downloads.
3. Sound Methodology:
   - Split data into train and test sets (`train_test_split`).
   - Fit scalers/preprocessors ONLY on train data, transform test data (prevent data leakage!).
   - Train Baseline Model.
   - Train Experimental Variant Model.
   - Evaluate both on the test set using the specified metric.
4. Output Format:
   - The script must print: `EXPERIMENT_METRICS_JSON:<json_string>` containing numeric values of baseline vs variant metrics.
5. Return ONLY executable Python code inside a single ```python ... ``` block. No conversational preamble.
"""

    def generate_experiment(self, hypothesis: Dict[str, Any], iteration: int) -> Path:
        past_mistakes = self.ledger.get_summary_of_mistakes_for_prompt()

        user_prompt = f"""Hypothesis to test:
Title: {hypothesis.get('title')}
Statement: {hypothesis.get('statement')}
Rationale: {hypothesis.get('rationale')}
Target Metric: {hypothesis.get('target_metric')}
Suggested Dataset: {hypothesis.get('dataset')}
Baseline: {hypothesis.get('baseline_description')}
Variant: {hypothesis.get('variant_description')}

{past_mistakes}

Write the complete Python experiment script to validate or refute this hypothesis.
Remember to print the final metrics in this exact format at the end:
print("EXPERIMENT_METRICS_JSON:" + json.dumps(results))
"""

        raw_response = self.llm.generate(user_prompt, system_instruction=self.SYSTEM_PROMPT)
        code = self.extract_code(raw_response)

        # Ensure directory exists and write script
        Config.ensure_dirs()
        script_path = Config.EXPERIMENTS_DIR / f"exp_iter_{iteration}.py"
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)

        return script_path
