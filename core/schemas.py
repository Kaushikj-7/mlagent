"""
Data contract definitions and Pydantic schemas for the research agent pipeline.
Ensures strict validation across agent handoffs and persistent ledger storage.
"""

from typing import List, Dict, Any, Optional

try:
    from pydantic import BaseModel, Field, ConfigDict

    class BaseContract(BaseModel):
        """Base model permitting extra fields for agent flexibility."""
        model_config = ConfigDict(extra="allow")

except ImportError:
    # Graceful fallback when running in an environment without pydantic
    def Field(default=None, default_factory=None, **kwargs):
        if default_factory is not None:
            return default_factory()
        return default

    class BaseContract:
        """Lightweight fallback contract when pydantic is not installed."""
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

        @classmethod
        def model_validate(cls, obj: Any):
            if isinstance(obj, dict):
                return cls(**obj)
            return obj

        def model_dump(self) -> Dict[str, Any]:
            return getattr(self, "__dict__", {})


class HypothesisSchema(BaseContract):
    title: str
    statement: str
    rationale: str
    target_metric: str = "test_r2"
    dataset: str = "synthetic_regression"
    baseline_description: str = ""
    variant_description: str = ""


class ExperimentSchema(BaseContract):
    script_name: str
    dataset: str = ""
    baseline_description: str = ""
    variant_description: str = ""


class ExecutionResultSchema(BaseContract):
    status: str
    exit_code: int
    stdout: str = ""
    stderr: str = ""
    metrics: Dict[str, Any] = Field(default_factory=dict)


class MistakeItem(BaseContract):
    category: str = "BUG"
    description: str
    suggested_fix: str = ""
    status: str = "PENDING"


class AuditReviewSchema(BaseContract):
    verdict: str  # e.g., 'SUPPORTED', 'REFUTED', 'INCONCLUSIVE', 'CODE_ERROR'
    critique_summary: str
    mistakes: List[MistakeItem] = Field(default_factory=list)
    scientific_quality_score: int = Field(default=8, ge=1, le=10)
    notes_for_future: str = ""


class RefinementSchema(BaseContract):
    applied: bool = True
    fix_agent: str = "RefinerAgent"
    status: str = "PENDING"  # 'RESOLVED', 'UNRESOLVED', 'PENDING'
    changes_made: str = ""
    re_execution_result: Optional[ExecutionResultSchema] = None


class LedgerEntrySchema(BaseContract):
    iteration: int
    timestamp: str
    updated_at: Optional[str] = None
    hypothesis: HypothesisSchema
    experiment: ExperimentSchema
    execution: ExecutionResultSchema
    critic_review: AuditReviewSchema
    refinement: Optional[RefinementSchema] = None
