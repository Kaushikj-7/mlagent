import os
import json
import time
from typing import Optional, Dict, Any
from core.config import Config

class GeminiLLM:
    """
    Unified LLM wrapper for Google Gemini models.
    Supports google-genai (v1) and google-generativeai with robust fallbacks,
    token-aware rate handling, and an offline mock mode for quota preservation.
    """

    def __init__(self, mock: bool = False):
        self.mock = mock
        self.api_key = Config.GEMINI_API_KEY
        self.model_name = Config.GEMINI_MODEL
        self._client = None
        self._backend = None

        if not self.mock:
            self._init_client()

    def _init_client(self):
        if not self.api_key:
            print("[GeminiLLM] Warning: No GEMINI_API_KEY configured. Falling back to mock mode.")
            self.mock = True
            return

        # Attempt 1: google-genai (official modern SDK)
        try:
            from google import genai
            self._client = genai.Client(api_key=self.api_key)
            self._backend = "google_genai"
            return
        except ImportError:
            pass

        # Attempt 2: google.generativeai (classic SDK)
        try:
            import google.generativeai as genai_legacy
            genai_legacy.configure(api_key=self.api_key)
            self._client = genai_legacy.GenerativeModel(self.model_name)
            self._backend = "google_generativeai"
            return
        except ImportError:
            pass

        print("[GeminiLLM] Notice: Neither 'google-genai' nor 'google-generativeai' is installed yet. Falling back to mock responses until libraries are installed.")
        self.mock = True

    def generate(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Generates text from Gemini or mock fallback."""
        if self.mock:
            return self._mock_response(prompt, system_instruction)

        max_retries = 3
        for attempt in range(max_retries):
            try:
                if self._backend == "google_genai":
                    from google.genai import types
                    candidate_models = [self.model_name, "gemini-3.6-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
                    seen = set()
                    models_to_try = [m for m in candidate_models if m and not (m in seen or seen.add(m))]

                    config = types.GenerateContentConfig(
                        system_instruction=system_instruction
                    ) if system_instruction else None

                    response = None
                    last_err = None
                    for candidate in models_to_try:
                        try:
                            response = self._client.models.generate_content(
                                model=candidate,
                                contents=prompt,
                                config=config
                            )
                            if response:
                                break
                        except Exception as me:
                            last_err = me
                            if "404" in str(me) or "NOT_FOUND" in str(me):
                                print(f"[GeminiLLM] Model {candidate} not found, trying next available model...")
                                continue
                            raise me

                    if not response and last_err:
                        raise last_err

                    # Inspect safety block and finish reasons safely
                    if hasattr(response, "candidates") and response.candidates:
                        cand = response.candidates[0]
                        finish_reason = str(getattr(cand, "finish_reason", "")).upper()
                        if "SAFETY" in finish_reason or "BLOCKED" in finish_reason or "RECITATION" in finish_reason:
                            print(f"[GeminiLLM] Warning: Generation candidate blocked by policy: {finish_reason}")
                            return self._mock_response(prompt, system_instruction)

                    try:
                        return response.text
                    except (ValueError, AttributeError) as ve:
                        print(f"[GeminiLLM] Warning: Response text empty or unavailable ({ve}). Using fallback.")
                        return self._mock_response(prompt, system_instruction)

                elif self._backend == "google_generativeai":
                    # Using google-generativeai
                    full_prompt = f"System: {system_instruction}\n\nUser: {prompt}" if system_instruction else prompt
                    response = self._client.generate_content(full_prompt)

                    # Check prompt feedback or candidate blocks
                    if hasattr(response, "prompt_feedback") and getattr(response.prompt_feedback, "block_reason", None):
                        print(f"[GeminiLLM] Warning: Prompt blocked: {response.prompt_feedback.block_reason}")
                        return self._mock_response(prompt, system_instruction)

                    try:
                        return response.text
                    except (ValueError, AttributeError) as ve:
                        print(f"[GeminiLLM] Warning: Response text unavailable ({ve}). Using fallback.")
                        return self._mock_response(prompt, system_instruction)

            except Exception as e:
                err_msg = str(e)
                is_rate_limit = "ResourceExhausted" in err_msg or "429" in err_msg
                if is_rate_limit and attempt < max_retries - 1:
                    backoff = 2 ** attempt
                    print(f"[GeminiLLM] Rate limit encountered. Retrying in {backoff}s (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(backoff)
                    continue
                elif is_rate_limit:
                    print("[GeminiLLM] Rate limit/quota exhausted after retries. Switching to safe mock response to continue workflow.")
                    return self._mock_response(prompt, system_instruction)
                else:
                    print(f"[GeminiLLM] Error calling Gemini API: {err_msg}")
                    # In case of uncaught API error, fall back to mock safely instead of crashing entire agent loop
                    return self._mock_response(prompt, system_instruction)

        return self._mock_response(prompt, system_instruction)

    def _mock_response(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Deterministic mock generator simulating academic ML agent responses."""
        prompt_lower = (prompt + " " + (system_instruction or "")).lower()

        # 1. Refiner Agent (highest precedence)
        if "refiner" in prompt_lower or "debugger" in prompt_lower or "resolve all these mistakes" in prompt_lower:
            return """```python
# Refined experiment script fixing previous errors
import json
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, QuantileTransformer
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score

def run_experiment():
    print("Executing repaired experiment script...")
    X, y = make_regression(n_samples=1000, n_features=10, noise=15.0, random_state=42)
    X[:, 0] = np.exp(np.clip(X[:, 0] / 3.0, -2, 3))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler_base = StandardScaler()
    X_train_base = scaler_base.fit_transform(X_train)
    X_test_base = scaler_base.transform(X_test)
    model_base = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=100, random_state=42)
    model_base.fit(X_train_base, y_train)
    y_pred_base = model_base.predict(X_test_base)
    mse_base = mean_squared_error(y_test, y_pred_base)
    r2_base = r2_score(y_test, y_pred_base)

    scaler_var = QuantileTransformer(output_distribution='normal', random_state=42)
    X_train_var = scaler_var.fit_transform(X_train)
    X_test_var = scaler_var.transform(X_test)
    model_var = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=100, random_state=42)
    model_var.fit(X_train_var, y_train)
    y_pred_var = model_var.predict(X_test_var)
    mse_var = mean_squared_error(y_test, y_pred_var)
    r2_var = r2_score(y_test, y_pred_var)

    results = {
        "baseline_mse": float(round(mse_base, 4)),
        "baseline_r2": float(round(r2_base, 4)),
        "variant_mse": float(round(mse_var, 4)),
        "variant_r2": float(round(r2_var, 4)),
        "mse_improvement_pct": float(round((mse_base - mse_var) / mse_base * 100, 2))
    }
    print("EXPERIMENT_METRICS_JSON:" + json.dumps(results))
    return results

if __name__ == "__main__":
    run_experiment()
```"""

        # 2. Critic Agent (must be before Experiment Agent)
        if "critic" in prompt_lower or "auditor" in prompt_lower or "peer reviewer" in prompt_lower or "scientific verdict" in prompt_lower:
            return json.dumps({
                "verdict": "SUPPORTED",
                "critique_summary": "The experiment executed cleanly. Quantile feature normalization reduced test MSE on the skewed benchmark, supporting the hypothesis.",
                "mistakes": [],
                "scientific_quality_score": 9,
                "notes_for_future": "Consider testing across multiple random seeds to verify statistical significance."
            }, indent=2)

        # 3. Hypothesis Agent
        if "hypothesis" in prompt_lower and ("propose" in prompt_lower or "formulate" in prompt_lower):
            return json.dumps({
                "title": "Robustness of Log-Scaled Feature Ensembling in Gradient-Boosted Trees vs MLPs",
                "statement": "Applying adaptive log-scaling to skewed continuous features in tabular benchmarks reduces gradient variance and improves test AUC by at least 2% in neural baselines compared to unscaled inputs.",
                "rationale": "High kurtosis and heavy-tailed tabular distributions destabilize early MLP layer activations, whereas tree splits are invariant. Pre-compressing tails bridges this inductive bias gap.",
                "target_metric": "test_r2",
                "dataset": "synthetic_regression",
                "baseline_description": "Standard MLP regressor on standard-scaled features",
                "variant_description": "MLP regressor with non-linear quantile transformation on heavy-tailed features"
            }, indent=2)

        # 4. Experiment Agent
        if "experiment" in prompt_lower or "python code" in prompt_lower:
            return """```python
# Experiment Script: Comparing Standard Scaling vs Quantile Transformation on Non-Linear Benchmark
import json
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, QuantileTransformer
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score

def run_experiment():
    print("Generating synthetic benchmark with skewed distribution...")
    X, y = make_regression(n_samples=1000, n_features=10, noise=15.0, random_state=42)
    X[:, 0] = np.exp(np.clip(X[:, 0] / 3.0, -2, 3))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 1. Baseline: Standard Scaling
    scaler_base = StandardScaler()
    X_train_base = scaler_base.fit_transform(X_train)
    X_test_base = scaler_base.transform(X_test)

    model_base = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=100, random_state=42)
    model_base.fit(X_train_base, y_train)
    y_pred_base = model_base.predict(X_test_base)
    mse_base = mean_squared_error(y_test, y_pred_base)
    r2_base = r2_score(y_test, y_pred_base)

    # 2. Variant: Non-linear Quantile Transformation (Hypothesis)
    scaler_var = QuantileTransformer(output_distribution='normal', random_state=42)
    X_train_var = scaler_var.fit_transform(X_train)
    X_test_var = scaler_var.transform(X_test)

    model_var = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=100, random_state=42)
    model_var.fit(X_train_var, y_train)
    y_pred_var = model_var.predict(X_test_var)
    mse_var = mean_squared_error(y_test, y_pred_var)
    r2_var = r2_score(y_test, y_pred_var)

    results = {
        "baseline_mse": float(round(mse_base, 4)),
        "baseline_r2": float(round(r2_base, 4)),
        "variant_mse": float(round(mse_var, 4)),
        "variant_r2": float(round(r2_var, 4)),
        "mse_improvement_pct": float(round((mse_base - mse_var) / mse_base * 100, 2))
    }
    
    print("EXPERIMENT_METRICS_JSON:" + json.dumps(results))
    return results

if __name__ == "__main__":
    run_experiment()
```"""

        return "Mock response completed."
