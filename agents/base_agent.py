import re
import json
from typing import Dict, Any
from core.llm import GeminiLLM
from core.ledger import ProjectLedger

class BaseAgent:
    """Base class for all ML workflow agents with ledger integration."""

    def __init__(self, llm: GeminiLLM, ledger: ProjectLedger):
        self.llm = llm
        self.ledger = ledger

    def extract_json(self, text: str) -> Dict[str, Any]:
        """Extracts and parses JSON object from LLM response, guaranteeing dict return."""
        # Try raw parse
        try:
            parsed = json.loads(text.strip())
            if isinstance(parsed, dict):
                return parsed
        except (json.JSONDecodeError, ValueError):
            pass

        # Match markdown ```json ... ```
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group(1))
                if isinstance(parsed, dict):
                    return parsed
            except (json.JSONDecodeError, ValueError):
                pass

        # Match first { to last }
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                parsed = json.loads(text[start:end + 1])
                if isinstance(parsed, dict):
                    return parsed
            except (json.JSONDecodeError, ValueError):
                pass

        return {}

    def extract_code(self, text: str) -> str:
        """Extracts Python code from markdown code fences or returns raw text."""
        # Prioritize explicit python code fences
        match_py = re.search(r"```(?:python|py)\s*\n?(.*?)\n?```", text, re.DOTALL | re.IGNORECASE)
        if match_py:
            return match_py.group(1).strip()

        # Fall back to general code fence
        match_generic = re.search(r"```\s*\n?(.*?)\n?```", text, re.DOTALL)
        if match_generic:
            return match_generic.group(1).strip()

        return text.strip()
