import sys
import os
import json
import subprocess
from pathlib import Path
from typing import Dict, Any
from core.config import Config

class ExperimentRunner:
    """
    Subprocess runner for executing generated ML experiments safely.
    Captures outputs, exceptions, execution time, and parsed metrics.
    """

    def __init__(self, timeout_secs: int = None):
        self.timeout_secs = timeout_secs or Config.EXPERIMENT_TIMEOUT_SECS
        # Identify Python interpreter: check Windows (.venv/Scripts/python.exe) and POSIX (.venv/bin/python)
        candidates = [
            Config.BASE_DIR / ".venv" / "Scripts" / "python.exe",
            Config.BASE_DIR / ".venv" / "bin" / "python",
            Path(sys.executable)
        ]
        self.python_executable = str(sys.executable)
        for cand in candidates:
            if cand.exists():
                self.python_executable = str(cand)
                break

    def run_script(self, script_path: Path) -> Dict[str, Any]:
        """
        Executes the experiment script located at script_path.
        Returns execution record dictionary.
        """
        if not script_path.exists():
            return {
                "status": "FAILED",
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Error: Experiment script does not exist: {script_path}",
                "metrics": {}
            }

        cmd = [self.python_executable, str(script_path)]
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        cache_dir = Config.BASE_DIR / ".cache" / "scikit_learn_data"
        cache_dir.mkdir(parents=True, exist_ok=True)
        env["SCIKIT_LEARN_DATA"] = str(cache_dir)

        try:
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout_secs,
                cwd=str(Config.BASE_DIR),
                env=env
            )

            stdout = process.stdout
            stderr = process.stderr
            exit_code = process.returncode
            status = "SUCCESS" if exit_code == 0 else "FAILED"
            metrics = self._parse_metrics(stdout)

            res = {
                "status": status,
                "exit_code": exit_code,
                "stdout": stdout,
                "stderr": stderr,
                "metrics": metrics
            }
            try:
                from core.schemas import ExecutionResultSchema
                return ExecutionResultSchema.model_validate(res).model_dump()
            except Exception:
                return res

        except subprocess.TimeoutExpired as e:
            res = {
                "status": "TIMEOUT",
                "exit_code": -2,
                "stdout": e.stdout or "",
                "stderr": f"Experiment timed out after {self.timeout_secs} seconds.",
                "metrics": {}
            }
            try:
                from core.schemas import ExecutionResultSchema
                return ExecutionResultSchema.model_validate(res).model_dump()
            except Exception:
                return res
        except Exception as e:
            res = {
                "status": "FAILED",
                "exit_code": -3,
                "stdout": "",
                "stderr": f"Unexpected execution failure: {str(e)}",
                "metrics": {}
            }
            try:
                from core.schemas import ExecutionResultSchema
                return ExecutionResultSchema.model_validate(res).model_dump()
            except Exception:
                return res

    def _parse_metrics(self, stdout: str) -> Dict[str, Any]:
        """Extracts JSON metrics tagged with EXPERIMENT_METRICS_JSON:."""
        metrics = {}
        marker = "EXPERIMENT_METRICS_JSON:"
        for line in stdout.splitlines():
            if marker in line:
                raw_json = line.split(marker, 1)[1].strip()
                try:
                    parsed = json.loads(raw_json)
                    if isinstance(parsed, dict):
                        metrics = parsed
                except (json.JSONDecodeError, ValueError):
                    pass
        return metrics
