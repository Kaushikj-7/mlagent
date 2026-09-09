"""
High-level Workflow Abstraction for ML Hypothesis Generation & Validation.
Exposes an intuitive, academic API while managing agents, execution sandbox,
Pydantic contracts, and the Project Ledger behind the scenes.
"""

import os
import sys
import warnings
from pathlib import Path
from typing import Dict, Any, Optional

from core.config import Config
from core.ledger import ProjectLedger
from core.llm import GeminiLLM
from core.ui import ResearcherUI
from core.schemas import LedgerEntrySchema
from execution.runner import ExperimentRunner
from agents.hypothesis_agent import HypothesisAgent
from agents.experiment_agent import ExperimentAgent
from agents.critic_agent import CriticAgent
from agents.refiner_agent import RefinerAgent


class WorkflowResult:
    """Structured result returned to the researcher upon workflow completion."""

    def __init__(self, topic: str, entries: list, ledger_path: Path):
        self.topic = topic
        self.entries = entries
        self.ledger_path = ledger_path
        self.latest_entry = entries[-1] if entries else None

    @property
    def verdict(self) -> str:
        if not self.latest_entry:
            return "N/A"
        return (self.latest_entry.get("critic_review") or {}).get("verdict", "UNKNOWN")

    @property
    def metrics(self) -> Dict[str, Any]:
        if not self.latest_entry:
            return {}
        return (self.latest_entry.get("execution") or {}).get("metrics", {})

    @property
    def hypothesis_title(self) -> str:
        if not self.latest_entry:
            return "N/A"
        return (self.latest_entry.get("hypothesis") or {}).get("title", "N/A")

    def __repr__(self) -> str:
        return f"<WorkflowResult topic='{self.topic}' verdict='{self.verdict}' entries={len(self.entries)}>"


class MLHypothesisWorkflow:
    """
    Primary High-Level Abstraction for Academic Researchers.
    
    Usage:
        workflow = MLHypothesisWorkflow(topic="Regularization in Neural Nets")
        result = workflow.run(iterations=1)
    """

    def __init__(
        self,
        topic: str = "Tabular Feature Representations and Neural Ensembling",
        mock: bool = False,
        verbose: bool = False
    ):
        self.topic = topic
        self.mock = mock
        self.verbose = verbose

        # Silence SDK warnings and internal noise unless verbose
        if not self.verbose:
            warnings.filterwarnings("ignore")
            os.environ["PYTHONWARNINGS"] = "ignore"

        Config.ensure_dirs()
        self.ledger = ProjectLedger(Config.LEDGER_JSON, Config.LEDGER_MD)
        self.llm = GeminiLLM(mock=self.mock)
        self.runner = ExperimentRunner(timeout_secs=Config.EXPERIMENT_TIMEOUT_SECS)

        self.hyp_agent = HypothesisAgent(self.llm, self.ledger)
        self.exp_agent = ExperimentAgent(self.llm, self.ledger)
        self.critic_agent = CriticAgent(self.llm, self.ledger)
        self.refiner_agent = RefinerAgent(self.llm, self.ledger)

    def run(self, iterations: int = 1, demo_mistake_fix: bool = False) -> WorkflowResult:
        """Runs the hypothesis generation, testing, and auditing cycle."""
        iterations_to_run = min(iterations, Config.MAX_ITERATIONS if not self.mock else iterations)
        mode_str = "OFFLINE MOCK" if self.mock else "LIVE GEMINI"

        ResearcherUI.banner(
            topic=self.topic,
            model=Config.GEMINI_MODEL,
            mode=mode_str,
            iterations=iterations_to_run
        )

        for i in range(1, iterations_to_run + 1):
            # Step 1: Hypothesis Generation
            hypothesis = self.hyp_agent.propose_hypothesis(self.topic)
            ResearcherUI.section_hypothesis(i, iterations_to_run, hypothesis)

            # Step 2: Experiment Synthesis
            script_path = self.exp_agent.generate_experiment(hypothesis, iteration=i)
            baseline_desc = hypothesis.get("baseline_description", "")
            variant_desc = hypothesis.get("variant_description", "")
            ResearcherUI.section_experiment(script_path.name, baseline_desc, variant_desc)

            # Optional demo bug injection
            if demo_mistake_fix and i == 1:
                with open(script_path, "r", encoding="utf-8") as f:
                    content = f.read()
                with open(script_path, "w", encoding="utf-8") as f:
                    f.write("# Injected demonstration bug\nundefined_test_variable_xyz\n" + content)

            # Step 3: Execution
            exec_result = self.runner.run_script(script_path)
            ResearcherUI.section_metrics(
                exec_result.get("metrics", {}),
                exec_result.get("status", "UNKNOWN"),
                exec_result.get("exit_code", 0)
            )

            # Step 4: Critic Audit
            with open(script_path, "r", encoding="utf-8") as f:
                script_code = f.read()

            audit_result = self.critic_agent.audit(hypothesis, script_code, exec_result)
            ResearcherUI.section_review(audit_result)

            mistakes = audit_result.get("mistakes", [])
            if mistakes:
                ResearcherUI.section_mistakes(mistakes)

            # Step 5: Commit to Project Ledger
            ledger_entry = {
                "iteration": i,
                "hypothesis": hypothesis,
                "experiment": {
                    "script_name": script_path.name,
                    "dataset": hypothesis.get("dataset", ""),
                    "baseline_description": baseline_desc,
                    "variant_description": variant_desc
                },
                "execution": exec_result,
                "critic_review": audit_result,
                "refinement": None
            }
            entry_idx = self.ledger.add_entry(ledger_entry) - 1

            # Step 6: Self-Healing Refinement if necessary
            if mistakes or exec_result.get("status") != "SUCCESS":
                ref_record = self.refiner_agent.fix_and_reexecute(
                    script_path=script_path,
                    hypothesis=hypothesis,
                    mistakes=mistakes,
                    stderr=exec_result.get("stderr", ""),
                    runner=self.runner,
                    ledger_entry_index=entry_idx
                )
                ResearcherUI.section_refinement(ref_record)

        ResearcherUI.footer(Config.LEDGER_MD)
        return WorkflowResult(self.topic, self.ledger.entries, Config.LEDGER_MD)
