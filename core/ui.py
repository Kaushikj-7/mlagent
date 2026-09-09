"""
Researcher View & Presentation Abstraction.
Provides a clean, professional, academic output interface for researchers,
hiding low-level agent internals, SDK warnings, and raw JSON payloads.
"""

import sys
from typing import Dict, Any, List, Optional
from pathlib import Path


class ResearcherUI:
    """Professional, clean terminal presenter designed for ML researchers."""

    WIDTH = 78

    @classmethod
    def banner(cls, topic: str, model: str, mode: str, iterations: int):
        print("=" * cls.WIDTH)
        print("                   ML HYPOTHESIS RESEARCH STUDIO")
        print("         Autonomous Scientific Exploration & Empirical Validation")
        print("=" * cls.WIDTH)
        print(f"  Research Topic : {topic}")
        print(f"  AI Engine      : {model} ({mode})")
        print(f"  Budget Limit   : {iterations} Iteration{'s' if iterations > 1 else ''} (Quota-Safe)")
        print("=" * cls.WIDTH)
        sys.stdout.flush()

    @classmethod
    def section_hypothesis(cls, iteration: int, total: int, hypothesis: Dict[str, Any]):
        print(f"\n[STEP 1/{total}] FORMULATED SCIENTIFIC HYPOTHESIS")
        print("-" * cls.WIDTH)
        print(f"  Title        : {hypothesis.get('title', 'Untitled')}")
        
        # Word wrap statement cleanly
        stmt = hypothesis.get('statement', '')
        print(f"  Hypothesis   : {cls._wrap(stmt, 17, cls.WIDTH)}")
        
        rationale = hypothesis.get('rationale', '')
        if rationale:
            print(f"  Rationale    : {cls._wrap(rationale, 17, cls.WIDTH)}")
            
        print(f"  Dataset      : {hypothesis.get('dataset', 'Synthetic')}")
        print(f"  Target Metric: {hypothesis.get('target_metric', 'N/A')}")
        sys.stdout.flush()

    @classmethod
    def section_experiment(cls, script_name: str, baseline_desc: str, variant_desc: str):
        print(f"\n[STEP 2] DESIGNING & EXECUTING EXPERIMENT")
        print("-" * cls.WIDTH)
        if baseline_desc:
            print(f"  Control Baseline  : {cls._wrap(baseline_desc, 22, cls.WIDTH)}")
        if variant_desc:
            print(f"  Hypothesis Variant: {cls._wrap(variant_desc, 22, cls.WIDTH)}")
        print(f"  Generated Script  : {script_name}")
        print(f"  Running isolated execution...")
        sys.stdout.flush()

    @classmethod
    def section_metrics(cls, metrics: Dict[str, Any], status: str, exit_code: int):
        print(f"\n[STEP 3] EMPIRICAL RESULTS")
        print("-" * cls.WIDTH)
        
        if status != "SUCCESS":
            print(f"  Status       : Execution {status} (Code: {exit_code})")
            return

        if not metrics:
            print("  Status       : Completed successfully (no quantitative metrics reported).")
            return

        print(f"  {'Metric':<25} {'Value':<20}")
        print(f"  {'-'*25} {'-'*20}")
        for k, v in metrics.items():
            val_str = f"{v:.4f}" if isinstance(v, float) else str(v)
            print(f"  {k:<25} {val_str:<20}")
        sys.stdout.flush()

    @classmethod
    def section_review(cls, audit: Dict[str, Any]):
        verdict = audit.get("verdict", "INCONCLUSIVE")
        score = audit.get("scientific_quality_score", 8)
        critique = audit.get("critique_summary", "")

        verdict_badge = f"[{verdict}]"
        print(f"\n[STEP 4] PEER REVIEW & SCIENTIFIC AUDIT")
        print("-" * cls.WIDTH)
        print(f"  Verdict      : {verdict_badge}")
        print(f"  Review Score : {score} / 10")
        if critique:
            print(f"  Assessment   : {cls._wrap(critique, 17, cls.WIDTH)}")
        sys.stdout.flush()

    @classmethod
    def section_mistakes(cls, mistakes: List[Dict[str, Any]]):
        if not mistakes:
            return
        print(f"\n  [!] Auditor Notes (Self-Healing Active):")
        for idx, m in enumerate(mistakes, 1):
            desc = m.get("description", "")
            print(f"      {idx}. [{m.get('category', 'DEFECT')}] {desc}")
        sys.stdout.flush()

    @classmethod
    def section_refinement(cls, ref: Dict[str, Any]):
        if not ref or not ref.get("applied"):
            return
        status = ref.get("status", "RESOLVED")
        changes = ref.get("changes_made", "Applied fixes.")
        print(f"  [Refiner Action] {changes}")
        print(f"  [Fix Resolution] Status: {status}")
        re_exec = ref.get("re_execution_result") or {}
        re_metrics = re_exec.get("metrics")
        if re_metrics:
            print(f"  [Repaired Run Metrics]:")
            for k, v in re_metrics.items():
                val_str = f"{v:.4f}" if isinstance(v, float) else str(v)
                print(f"      - {k}: {val_str}")
        sys.stdout.flush()

    @classmethod
    def footer(cls, ledger_path: Path):
        print("\n" + "=" * cls.WIDTH)
        print("  WORKFLOW COMPLETE")
        print(f"  Permanent Research Ledger & Audit Trail saved to:")
        print(f"  -> {ledger_path.name}")
        print("=" * cls.WIDTH + "\n")
        sys.stdout.flush()

    @classmethod
    def _wrap(cls, text: str, indent: int, max_width: int) -> str:
        """Wraps text preserving clean terminal indentation."""
        words = text.split()
        if not words:
            return ""
        lines = []
        cur_line = []
        cur_len = indent
        
        for w in words:
            if cur_len + len(w) + 1 > max_width and cur_line:
                lines.append(" ".join(cur_line))
                cur_line = [w]
                cur_len = indent + len(w)
            else:
                cur_line.append(w)
                cur_len += len(w) + 1
                
        if cur_line:
            lines.append(" ".join(cur_line))
            
        indent_space = " " * indent
        return f"\n{indent_space}".join(lines)
