# Project Mistake Ledger

> **Notice**: This ledger is automatically referenced and maintained by monitoring subagents and the primary orchestrator agent. It tracks architectural mistakes, syntax errors, contract violations, and logic flaws across the codebase.

---

## 1. Ledger Schema & Conventions

### 1.1 Status Lifecycle
- `[OPEN]`: Newly identified issue logged by the monitor agent. Awaiting main agent review.
- `[IN_PROGRESS]`: Currently being investigated or refactored by the main agent.
- `[RESOLVED]`: Fixed by the main agent and verified through syntax checks / tests.
- `[WONT_FIX]` / `[FALSE_POSITIVE]`: Reviewed and deemed acceptable or false positive with documented justification.

### 1.2 Categories & ID Prefix
| Category | Prefix | Description |
| :--- | :--- | :--- |
| **Architecture** | `ERR-ARCH-###` | Layer violations, circular dependencies, tight coupling, leaky abstractions, antipatterns. |
| **Syntax / Parse** | `ERR-SYNT-###` | Syntax errors, unclosed brackets, invalid grammar, unparsed ASTs. |
| **Typing / Contract** | `ERR-TYPE-###` | Type mismatches, invalid signatures, missing contract enforcement. |
| **Logic / Runtime** | `ERR-LOGI-###` | Unhandled exceptions, off-by-one errors, state mutation bugs, race conditions. |
| **Performance / Security** | `ERR-PSEC-###` | Memory leaks, N+1 queries, insecure input handling, resource leaks. |

### 1.3 Severity Levels
- **P0 - Critical**: Breaks build/runtime, syntax failure, catastrophic architectural flaw.
- **P1 - High**: Major contract breakdown, circular dependency cycle, data corruption risk.
- **P2 - Medium**: Code smell, non-optimal layering, unhandled edge cases, missing validation.
- **P3 - Low**: Style discrepancy, minor redundancy, missing type annotation.

---

## 2. Active Mistake Registry (Open & In Progress)

| ID | Category | Sev | Location | Summary | Status | Detected By |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ERR-ARCH-001` | Architecture | P1 | `core/config.py:L40-L42`, `core/ledger.py:L198-L202` | Ledger file ambiguity and destructive markdown overwrite vulnerability | [RESOLVED] | codebase_monitor |
| `ERR-LOGI-001` | Logic / Runtime | P1 | `core/ledger.py:L31-L36, L198-L202` | Non-atomic ledger writes risk JSON data corruption on interruption | [RESOLVED] | codebase_monitor |
| `ERR-LOGI-002` | Logic / Runtime | P1 | `core/llm.py:L70-L81, L83-L90` | Unhandled response safety block exceptions crashing pipeline | [RESOLVED] | codebase_monitor |
| `ERR-LOGI-003` | Logic / Runtime | P1 | `core/llm.py:L116-L125`, `experiments/exp_iter_1.py:L4, L12` | Runtime PermissionError on `fetch_california_housing` in experiment execution | [RESOLVED] | codebase_monitor |
| `ERR-LOGI-004` | Logic / Runtime | P2 | `core/config.py:L35-L36` | Unhandled ValueError on invalid environment variable casting at module import | [RESOLVED] | codebase_monitor |
| `ERR-ARCH-002` | Architecture | P2 | `core/llm.py:L83-L90` | Absence of rate limit backoff/retry causing silent synthetic mock contamination | [RESOLVED] | codebase_monitor |
| `ERR-ARCH-003` | Architecture | P2 | `scripts/audit_codebase.py:L1-L85`, `AGENTS.md:L24-L31` | Audit script capabilities diverge from documented specifications in AGENTS.md | [RESOLVED] | codebase_monitor |
| `ERR-LOGI-005` | Logic / Runtime | P2 | `core/ledger.py:L46-L51` | Silent failure on out-of-bounds index in `ProjectLedger.update_entry` | [RESOLVED] | codebase_monitor |
| `ERR-ARCH-004` | Architecture | P2 | `execution/runner.py:L18-L23` | OS-specific hardcoded virtualenv path breaks cross-platform and container runs | [RESOLVED] | codebase_monitor |
| `ERR-TYPE-001` | Typing / Contract | P2 | `core/ledger.py:L16`, `agents/critic_agent.py:L42` | Untyped data contracts and ad-hoc dict lookups across agent pipeline | [RESOLVED] | codebase_monitor |
| `ERR-LOGI-006` | Logic / Runtime | P3 | `core/llm.py:L66-L69` | Overly restrictive model name prefix overrides valid custom / vertex models | [RESOLVED] | codebase_monitor |
| `ERR-LOGI-007` | Logic / Runtime | P3 | `core/config.py:L22-L23` | Silent exception suppression in `load_dotenv_fallback` masks I/O issues | [RESOLVED] | codebase_monitor |
| `ERR-LOGI-008` | Logic / Runtime | P1 | `core/ledger.py:L223-L224` | Unsafe dictionary access on optional `re_execution_result` crashes during markdown synchronization | [RESOLVED] | codebase_monitor |
| `ERR-ARCH-005` | Architecture | P1 | `main.py:L64, L77, L118` | Static loop index resets to 1 across invocations, causing destructive overwriting of historical experiment scripts | [RESOLVED] | codebase_monitor |
| `ERR-LOGI-009` | Logic / Runtime | P2 | `agents/base_agent.py:L43-L46` | Non-specific code fence regex extracts non-Python markdown snippets into experiment scripts | [RESOLVED] | codebase_monitor |
| `ERR-TYPE-002` | Typing / Contract | P2 | `agents/base_agent.py:L14-L39`, `execution/runner.py:L106-L117` | Missing dict type validation in `extract_json` and `_parse_metrics` returns non-dict types that break callers | [RESOLVED] | codebase_monitor |
| `ERR-TYPE-003` | Typing / Contract | P3 | `core/schemas.py:L55-L60` | `RefinementSchema` contract omits explicit `applied` field required by markdown renderer | [RESOLVED] | codebase_monitor |
| `ERR-LOGI-010` | Logic / Runtime | P3 | `agents/hypothesis_agent.py:L44` | Prompt schema example suggests `california_housing`, reintroducing the permission error addressed in ERR-LOGI-003 | [RESOLVED] | codebase_monitor |

---

## 3. Detailed Issue Breakdown

### [ERR-ARCH-001] Ledger File Ambiguity & Destructive Overwrite Vulnerability
- **Category**: Architecture
- **Severity**: P1
- **File / Lines**: `core/config.py:L40-L42`, `core/ledger.py:L198-L202`
- **Detected On**: 2026-09-09
- **Root Cause & Description**:
  The repository maintains two distinct ledger concepts: `PROJECT_MISTAKE_LEDGER.md` (QA engineering defects) and `PROJECT_LEDGER.md` (ML hypothesis experiments). `core/config.py` did not differentiate between them, and `ProjectLedger._sync_markdown()` overwrote its destination file with `"w"`, risking accidental destruction of the QA mistake ledger.
- **Proposed Remediation**:
  Explicitly delineate `ACADEMIC_LEDGER_MD` and `CODE_MISTAKE_LEDGER_MD` in `core/config.py`. In `core/ledger.py`, add a safety assertion in `_sync_markdown()` blocking overwrite if target is `PROJECT_MISTAKE_LEDGER.md` or contains `# Project Mistake Ledger`.
- **Resolution Notes**:
  Resolved by main agent on 2026-09-09. `core/config.py` now specifies both `ACADEMIC_LEDGER_MD` and `CODE_MISTAKE_LEDGER_MD`. `core/ledger.py:_sync_markdown` now verifies destination path name and header, raising `ValueError` if an overwrite is attempted. Verified via unit assertion.

### [ERR-LOGI-001] Non-Atomic Ledger Writes Risk Data Loss on Interruption
- **Category**: Logic / Runtime
- **Severity**: P1
- **File / Lines**: `core/ledger.py:L31-L36`, `core/ledger.py:L198-L202`
- **Detected On**: 2026-09-09
- **Root Cause & Description**:
  Direct `open(..., "w")` serialization left `project_ledger.json` vulnerable to 0-byte corruption if execution was interrupted mid-write.
- **Proposed Remediation**:
  Serialize data to `.tmp` file first, then atomically replace destination file using `os.replace`.
- **Resolution Notes**:
  Resolved by main agent on 2026-09-09. Implemented atomic write with temporary `.tmp` file and `os.replace` in both `save()` and `_sync_markdown()`.

### [ERR-LOGI-002] Unhandled Response Safety Block Exceptions Crashing Pipeline
- **Category**: Logic / Runtime
- **Severity**: P1
- **File / Lines**: `core/llm.py:L70-L81`, `core/llm.py:L83-L90`
- **Detected On**: 2026-09-09
- **Root Cause & Description**:
  Accessing `response.text` unconditionally caused `ValueError` when candidates were blocked by safety filters. Uncaught exceptions crashed the orchestrator.
- **Proposed Remediation**:
  Inspect candidate presence and finish reasons before accessing `response.text`, and handle `ValueError` gracefully with fallback.
- **Resolution Notes**:
  Resolved by main agent on 2026-09-09. In `core/llm.py`, inspect `finish_reason` for `SAFETY`, `BLOCKED`, or `RECITATION`, and safely catch `(ValueError, AttributeError)` when reading `response.text`.

### [ERR-LOGI-003] Runtime PermissionError on `fetch_california_housing` in Experiment Subprocess
- **Category**: Logic / Runtime
- **Severity**: P1
- **File / Lines**: `core/llm.py:L116-L125`, `experiments/exp_iter_1.py:L4, L12`
- **Detected On**: 2026-09-09
- **Root Cause & Description**:
  `fetch_california_housing()` attempted to download/cache dataset in restricted system paths, throwing `PermissionError: [Errno 13]`.
- **Proposed Remediation**:
  Switch synthetic generation to self-contained datasets such as `make_regression` or `load_diabetes`.
- **Resolution Notes**:
  Resolved by main agent on 2026-09-09. Updated `core/llm.py` mock generator and `experiments/exp_iter_1.py` to use `make_regression(n_samples=1000, n_features=10)`.

### [ERR-LOGI-004] Unhandled ValueError on Invalid Environment Variable Casting at Module Import
- **Category**: Logic / Runtime
- **Severity**: P2
- **File / Lines**: `core/config.py:L35-L36`
- **Detected On**: 2026-09-09
- **Root Cause & Description**:
  Import-time `int(os.getenv(...))` failed with `ValueError` if environment variable was empty string or invalid number.
- **Proposed Remediation**:
  Use a helper function `_safe_int_env` with default fallback.
- **Resolution Notes**:
  Resolved by main agent on 2026-09-09. Implemented `_safe_int_env(key, default)` in `core/config.py`.

### [ERR-ARCH-002] Absence of Rate Limit Backoff/Retry Causing Silent Synthetic Mock Contamination
- **Category**: Architecture
- **Severity**: P2
- **File / Lines**: `core/llm.py:L83-L90`
- **Detected On**: 2026-09-09
- **Root Cause & Description**:
  Immediate fallback to mock on 429 quota exhaustion without retry backoff contaminated research runs.
- **Proposed Remediation**:
  Implement retry loop with exponential backoff before falling back.
- **Resolution Notes**:
  Resolved by main agent on 2026-09-09. Added 3-attempt exponential backoff (`2 ** attempt` seconds delay) in `core/llm.py:generate`.

### [ERR-ARCH-003] Audit Script Capabilities Diverge From Documented Specifications
- **Category**: Architecture
- **Severity**: P2
- **File / Lines**: `scripts/audit_codebase.py:L1-L85`, `AGENTS.md:L24-L31`
- **Detected On**: 2026-09-09
- **Root Cause & Description**:
  `scripts/audit_codebase.py` did not check circular imports or broken symbols, diverging from `AGENTS.md`.
- **Proposed Remediation**:
  Upgrade `scripts/audit_codebase.py` to build import graphs, detect circular dependency cycles, and verify ledger integrity.
- **Resolution Notes**:
  Resolved by main agent on 2026-09-09. Re-architected `scripts/audit_codebase.py` with DFS cycle detection across module trees and ledger section validation.

### [ERR-LOGI-005] Silent Failure on Out-of-Bounds Index in `ProjectLedger.update_entry`
- **Category**: Logic / Runtime
- **Severity**: P2
- **File / Lines**: `core/ledger.py:L46-L51`
- **Detected On**: 2026-09-09
- **Root Cause & Description**:
  Out-of-bounds indices in `update_entry()` were silently ignored.
- **Proposed Remediation**:
  Log a warning or raise IndexError.
- **Resolution Notes**:
  Resolved by main agent on 2026-09-09. Added warning log alerting caller when an out-of-bounds index is supplied.

### [ERR-ARCH-004] OS-Specific Hardcoded Virtualenv Path Breaks Cross-Platform Runs
- **Category**: Architecture
- **Severity**: P2
- **File / Lines**: `execution/runner.py:L18-L23`
- **Detected On**: 2026-09-09
- **Root Cause & Description**:
  Hardcoded Windows-only `.venv/Scripts/python.exe` failed on POSIX systems.
- **Proposed Remediation**:
  Check POSIX `.venv/bin/python`, Windows `.venv/Scripts/python.exe`, and `sys.executable`.
- **Resolution Notes**:
  Resolved by main agent on 2026-09-09. `execution/runner.py` now checks candidate paths for both Windows and POSIX virtual environments.

### [ERR-TYPE-001] Untyped Data Contracts and Ad-Hoc Dict Lookups Across Agent Pipeline
- **Category**: Typing / Contract
- **Severity**: P2
- **File / Lines**: `core/ledger.py:L16`, `agents/critic_agent.py:L42`
- **Detected On**: 2026-09-09
- **Root Cause & Description**:
  Untyped dictionaries created fragile data handoffs across the pipeline.
- **Proposed Remediation**:
  Define typed Pydantic models in `core/schemas.py`.
- **Resolution Notes**:
  Resolved by main agent on 2026-09-09. Created `core/schemas.py` with Pydantic models for all agent contracts, including robust fallback if pydantic is not installed in the active environment.

### [ERR-LOGI-006] Overly Restrictive Model Name Prefix Overrides Valid Custom Models
- **Category**: Logic / Runtime
- **Severity**: P3
- **File / Lines**: `core/llm.py:L66-L69`
- **Detected On**: 2026-09-09
- **Root Cause & Description**:
  Model names not starting strictly with `gemini-` (e.g. `models/`, `tunedModels/`) were forcibly overridden.
- **Proposed Remediation**:
  Allow valid resource prefixes before falling back.
- **Resolution Notes**:
  Resolved by main agent on 2026-09-09. Updated model validation to allow `models/`, `tunedModels/`, and `projects/` namespaces.

### [ERR-LOGI-007] Silent Exception Suppression in `load_dotenv_fallback` Masks I/O Issues
- **Category**: Logic / Runtime
- **Severity**: P3
- **File / Lines**: `core/config.py:L22-L23`
- **Detected On**: 2026-09-09
- **Root Cause & Description**:
  Bare `except Exception: pass` hid `.env` parsing errors.
- **Proposed Remediation**:
  Log a warning with the exception details.
- **Resolution Notes**:
  Resolved by main agent on 2026-09-09. Added notice logger with exception details in `core/config.py:load_dotenv_fallback`.

### [ERR-LOGI-008] Unsafe Dictionary Access on Optional `re_execution_result`
- **Category**: Logic / Runtime
- **Severity**: P1
- **File / Lines**: `core/ledger.py:L223-L224`
- **Detected On**: 2026-09-09
- **Root Cause & Description**:
  In `_sync_markdown()`, `ref.get('re_execution_result', {}).get(...)` failed when `re_execution_result` was explicitly set to `None` in the schema dict, causing `AttributeError: 'NoneType' object has no attribute 'get'` and breaking the sync process.
- **Proposed Remediation**:
  Use `(ref.get('re_execution_result') or {}).get(...)` to defensively guard against `None`.
- **Resolution Notes**:
  Resolved by main agent on 2026-09-09. Updated `core/ledger.py` lines 217-226 with safe dict fallback `ref.get("re_execution_result") or {}`. Verified with end-to-end execution.

### [ERR-ARCH-005] Static Loop Index Resets to 1 Across Invocations
- **Category**: Architecture
- **Severity**: P1
- **File / Lines**: `main.py:L64, L77, L118`
- **Detected On**: 2026-09-09
- **Root Cause & Description**:
  `main.py` restarted iteration indexing from 1 on every invocation, causing `exp_iter_1.py` to be overwritten and creating duplicate iteration 1 rows in the ledger.
- **Proposed Remediation**:
  Derive `start_iteration = len(ledger.entries) + 1` in `main.py`.
- **Resolution Notes**:
  Resolved by main agent on 2026-09-09. Updated `main.py` to calculate `start_iteration = len(ledger.entries) + 1` and loop through `range(start_iteration, start_iteration + iterations_to_run)`. Verified across multiple sequential CLI runs without file collisions.

### [ERR-LOGI-009] Non-Specific Code Fence Regex Extracts Non-Python Markdown
- **Category**: Logic / Runtime
- **Severity**: P2
- **File / Lines**: `agents/base_agent.py:L43-L46`
- **Detected On**: 2026-09-09
- **Root Cause & Description**:
  The regex `r"```(?:python)?\s*(.*?)\s*```"` matched any code fence, potentially extracting non-Python blocks (e.g. bash or json) into executable `.py` files.
- **Proposed Remediation**:
  Prioritize explicit ````python` or ````py` fences with case insensitivity before falling back to generic fences.
- **Resolution Notes**:
  Resolved by main agent on 2026-09-09. Updated `extract_code()` in `agents/base_agent.py` to search for explicit python fences first.

### [ERR-TYPE-002] Missing Dict Type Validation in `extract_json` and `_parse_metrics`
- **Category**: Typing / Contract
- **Severity**: P2
- **File / Lines**: `agents/base_agent.py:L14-L39`, `execution/runner.py:L106-L117`
- **Detected On**: 2026-09-09
- **Root Cause & Description**:
  Functions declaring `-> Dict[str, Any]` returned non-dict types if `json.loads` parsed booleans, arrays, or scalars, crashing downstream dict operations.
- **Proposed Remediation**:
  Validate `isinstance(parsed, dict)` before returning; default to `{}` otherwise.
- **Resolution Notes**:
  Resolved by main agent on 2026-09-09. Wrapped all parsed returns in `agents/base_agent.py` and `execution/runner.py` with `isinstance(parsed, dict)` checks.

### [ERR-TYPE-003] `RefinementSchema` Contract Omits Explicit `applied` Field
- **Category**: Typing / Contract
- **Severity**: P3
- **File / Lines**: `core/schemas.py:L55-L60`
- **Detected On**: 2026-09-09
- **Root Cause & Description**:
  `RefinementSchema` lacked an explicit `applied` field, causing `core/ledger.py:L216` (`if ref and ref.get("applied"):`) to evaluate false when strictly validated.
- **Proposed Remediation**:
  Add `applied: bool = True` to `RefinementSchema`.
- **Resolution Notes**:
  Resolved by main agent on 2026-09-09. Added `applied: bool = True` in `core/schemas.py`. Verified in test run.

### [ERR-LOGI-010] Prompt Schema Example Suggests Forbidden Dataset `california_housing`
- **Category**: Logic / Runtime
- **Severity**: P3
- **File / Lines**: `agents/hypothesis_agent.py:L44`
- **Detected On**: 2026-09-09
- **Root Cause & Description**:
  The JSON template example listed `california_housing`, contradicting the system prompt and risking permission errors during execution.
- **Proposed Remediation**:
  Update the prompt example to safe datasets: `synthetic_regression, load_diabetes, breast_cancer`.
- **Resolution Notes**:
  Resolved by main agent on 2026-09-09. Updated prompt template in `agents/hypothesis_agent.py`.

---

## 4. Resolution & Verification Archive

| ID | Resolved Date | Fixed By | Verification Method | Summary of Fix |
| :--- | :--- | :--- | :--- | :--- |
| `ERR-ARCH-001` | 2026-09-09 | Main Agent | Unit test assertion | Delineated ledger constants in `core/config.py`; added overwrite guard in `core/ledger.py`. |
| `ERR-LOGI-001` | 2026-09-09 | Main Agent | Atomic write test | Implemented tempfile serialization + `os.replace` in `core/ledger.py`. |
| `ERR-LOGI-002` | 2026-09-09 | Main Agent | Code inspection & AST | Added safety block finish reason checks and `ValueError` fallback in `core/llm.py`. |
| `ERR-LOGI-003` | 2026-09-09 | Main Agent | Subprocess runner execution | Switched to `make_regression` to eliminate dataset cache permission errors. |
| `ERR-LOGI-004` | 2026-09-09 | Main Agent | Unit execution | Replaced unsafe `int()` casts with `_safe_int_env` fallback parser in `core/config.py`. |
| `ERR-ARCH-002` | 2026-09-09 | Main Agent | AST audit | Added 3-attempt exponential backoff retry loop for 429/ResourceExhausted in `core/llm.py`. |
| `ERR-ARCH-003` | 2026-09-09 | Main Agent | `scripts/audit_codebase.py` execution | Added DFS circular dependency detection and ledger integrity validation in audit script. |
| `ERR-LOGI-005` | 2026-09-09 | Main Agent | Python execution | Added boundary warning in `ProjectLedger.update_entry`. |
| `ERR-ARCH-004` | 2026-09-09 | Main Agent | Path verification test | Added cross-platform Windows/POSIX virtualenv interpreter detection in `execution/runner.py`. |
| `ERR-TYPE-001` | 2026-09-09 | Main Agent | Pydantic schema validation | Created `core/schemas.py` with typed models for all agent contracts. |
| `ERR-LOGI-006` | 2026-09-09 | Main Agent | Unit test | Permitted `models/`, `tunedModels/`, and `projects/` prefixes in `core/llm.py`. |
| `ERR-LOGI-007` | 2026-09-09 | Main Agent | Exception trace test | Added warning notice on `.env` read failure in `core/config.py`. |
| `ERR-LOGI-008` | 2026-09-09 | Main Agent | Subprocess pipeline execution | Protected optional `re_execution_result` with None-safe dict access in `core/ledger.py`. |
| `ERR-ARCH-005` | 2026-09-09 | Main Agent | Multi-run CLI execution test | Calculated `start_iteration` dynamically from existing ledger count in `main.py`. |
| `ERR-LOGI-009` | 2026-09-09 | Main Agent | Regex unit test | Prioritized explicit python/py code fences in `agents/base_agent.py`. |
| `ERR-TYPE-002` | 2026-09-09 | Main Agent | Type verification test | Added `isinstance(parsed, dict)` enforcement in `agents/base_agent.py` and `execution/runner.py`. |
| `ERR-TYPE-003` | 2026-09-09 | Main Agent | Markdown rendering check | Added explicit `applied: bool = True` to `RefinementSchema` in `core/schemas.py`. |
| `ERR-LOGI-010` | 2026-09-09 | Main Agent | Prompt template audit | Replaced `california_housing` with `synthetic_regression` in `agents/hypothesis_agent.py`. |

---

## 5. Workflow Protocols for Agents

### For Monitor Subagents:
1. Scan the repository (AST parse, architecture validation, static checks).
2. For any defect found, allocate the next numerical ID for that category.
3. Append a structured entry to Section 3 and add an item to the Active Mistake Registry in Section 2.
4. Notify the main agent with a concise summary of detected issues.

### For Main Agent:
1. Inspect the Active Mistake Registry in Section 2.
2. Prioritize items by Severity (P0 -> P1 -> P2 -> P3).
3. Implement the remediation in code.
4. Run verification tests and syntax validation (`python -m py_compile`, pytest, or AST parse).
5. Update the issue status to `[RESOLVED]`, fill in Resolution Notes, and append to the Archive in Section 4.
