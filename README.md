# Academic ML Hypothesis Agentic Workflow

An autonomous multi-agent system designed for academic machine learning research. It formulates novel ML hypotheses, generates reproducible empirical experiment scripts, executes them in safe subprocesses, records all results and errors in a persistent **Project Ledger**, and autonomously fixes code or methodological mistakes.

---

## Key Features

1. **Academic ML Hypothesis Generation**:
   - `HypothesisAgent` synthesizes falsifiable, mathematically motivated hypotheses on standard benchmark datasets.
   - Constrained to standard CPU-friendly datasets (`sklearn.datasets`) for fast, zero-GPU execution.
2. **Experiment Synthesis & Sandboxed Execution**:
   - `ExperimentAgent` designs standalone Python scripts testing baseline vs. experimental variants.
   - `ExperimentRunner` executes the code in isolated subprocesses with timeout and metric extraction.
3. **Shared Persistent Project Ledger (`project_ledger.json` & `PROJECT_LEDGER.md`)**:
   - Every hypothesis, script, execution traceback, critic audit, and mistake is permanently tracked.
   - Synchronized automatically into human-readable Markdown format (`PROJECT_LEDGER.md`).
4. **Mistake Detection & Self-Healing Fix Loop**:
   - `CriticAgent` detects code bugs, syntax errors, data leakage, and ungrounded metrics, committing them to the ledger.
   - `RefinerAgent` reads the mistakes from the ledger, patches the experiment script, re-runs it, and updates the ledger with the resolution.
5. **Budget & Rate Limit Preservation**:
   - Defaults strictly to **1 iteration** to safeguard API quota.
   - Includes `--mock` mode for local offline dry-runs with zero API token consumption.

---

## Architecture

```
User Prompt / ML Topic
         │
         ▼
 ┌─────────────────┐       Reads Prior History
 │ HypothesisAgent │ ◄───────────────────────────┐
 └────────┬────────┘                             │
          │ Proposes Hypothesis                  │
          ▼                                      │
 ┌─────────────────┐       Reads Past Mistakes   │
 │ ExperimentAgent │ ◄───────────────────────────┤
 └────────┬────────┘                             │
          │ Generates Code (exp_iter_1.py)       │
          ▼                                      │
 ┌─────────────────┐                             │
 │ Subprocess Exec │                             │
 └────────┬────────┘                             │
          │ Logs stdout, stderr, metrics         │
          ▼                                      │
 ┌─────────────────┐       Audits & Commits      │
 │   CriticAgent   │ ──────────────────────────► ┼──► Project Ledger
 └────────┬────────┘                             │    (project_ledger.json
          │ Mistakes Detected?                   │     & PROJECT_LEDGER.md)
          ▼                                      │
 ┌─────────────────┐       Reads Mistake & Fixes │
 │  RefinerAgent   │ ◄───────────────────────────┘
 └────────┬────────┘
          │ Patches Code & Re-runs
          ▼
   Updated Ledger
```

---

## Quickstart

### 1. Environment Setup
The project uses `uv` and Python 3.12:
```powershell
uv venv
uv pip install -r requirements.txt
```

### 2. Configuration (`.env`)
Configure your Gemini API key in `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
MAX_ITERATIONS=1
EXPERIMENT_TIMEOUT_SECS=60
```

### 3. Run Offline Mock Test (0 API Tokens)
```powershell
.venv\Scripts\python.exe main.py --mock --iterations 1
```

### 4. Run Self-Healing Mistake Demo (Simulated Error -> Ledger Log -> Auto-Fix)
```powershell
.venv\Scripts\python.exe main.py --mock --demo-mistake-fix
```

### 5. Run Live Gemini API Cycle (1 Iteration)
```powershell
.venv\Scripts\python.exe main.py --iterations 1 --topic "Feature Quantization in Tabular Neural Networks"
```

### 6. Inspecting the Project Ledger
View the generated audit logs and mistake resolutions at:
- `PROJECT_LEDGER.md` (Rich Markdown report)
- `project_ledger.json` (Structured machine-readable audit trail)
