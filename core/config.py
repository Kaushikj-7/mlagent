import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

def load_dotenv_fallback(dotenv_path: Path):
    """Fallback .env parser if python-dotenv is not installed."""
    if not dotenv_path.exists():
        return
    try:
        with open(dotenv_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                if k not in os.environ:
                    os.environ[k] = v
    except Exception as e:
        print(f"[Config] Notice: Error reading .env file ({dotenv_path}): {e}")

# Attempt to load .env
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    load_dotenv_fallback(BASE_DIR / ".env")
except Exception as e:
    print(f"[Config] Notice: Exception loading .env via python-dotenv: {e}. Using fallback parser.")
    load_dotenv_fallback(BASE_DIR / ".env")

def _safe_int_env(key: str, default: int) -> int:
    val = os.getenv(key)
    if val is None or not val.strip():
        return default
    try:
        return int(val.strip())
    except ValueError:
        print(f"[Config] Warning: Invalid integer '{val}' for {key}. Using default {default}.")
        return default

class Config:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
    MAX_ITERATIONS: int = _safe_int_env("MAX_ITERATIONS", 1)
    EXPERIMENT_TIMEOUT_SECS: int = _safe_int_env("EXPERIMENT_TIMEOUT_SECS", 60)
    
    BASE_DIR: Path = BASE_DIR
    EXPERIMENTS_DIR: Path = BASE_DIR / "experiments"
    
    # Delineated Ledgers
    LEDGER_JSON: Path = BASE_DIR / "project_ledger.json"
    ACADEMIC_LEDGER_MD: Path = BASE_DIR / "PROJECT_LEDGER.md"
    CODE_MISTAKE_LEDGER_MD: Path = BASE_DIR / "PROJECT_MISTAKE_LEDGER.md"
    LEDGER_MD: Path = ACADEMIC_LEDGER_MD  # Backward compatibility alias

    @classmethod
    def ensure_dirs(cls):
        cls.EXPERIMENTS_DIR.mkdir(parents=True, exist_ok=True)
