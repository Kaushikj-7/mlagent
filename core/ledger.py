import os
import json
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from core.schemas import LedgerEntrySchema

class ProjectLedger:
    """
    Project Ledger: Central shared blackboard and persistent memory.
    Tracks hypotheses, generated experiment code, execution outputs,
    detected mistakes (code, data, methodology), and applied fixes.
    """

    def __init__(self, json_path: Path, md_path: Path):
        self.json_path = json_path
        self.md_path = md_path
        self.entries: List[Dict[str, Any]] = []
        self.load()

    def load(self):
        """Loads existing ledger entries if present."""
        if self.json_path.exists():
            try:
                with open(self.json_path, "r", encoding="utf-8") as f:
                    raw_entries = json.load(f)
                self.entries = []
                for item in raw_entries:
                    try:
                        validated = LedgerEntrySchema.model_validate(item)
                        self.entries.append(validated.model_dump())
                    except Exception:
                        self.entries.append(item)
            except Exception as e:
                print(f"[Ledger] Warning: Failed to load existing ledger JSON: {e}")
                self.entries = []
        else:
            self.entries = []

    def save(self):
        """Saves current ledger entries to JSON atomically and updates Markdown mirror."""
        self.json_path.parent.mkdir(parents=True, exist_ok=True)
        temp_json = self.json_path.with_suffix(".tmp")
        try:
            with open(temp_json, "w", encoding="utf-8") as f:
                json.dump(self.entries, f, indent=2, ensure_ascii=False)
            os.replace(temp_json, self.json_path)
        except Exception as e:
            if temp_json.exists():
                try:
                    temp_json.unlink()
                except OSError:
                    pass
            print(f"[Ledger] Error: Failed atomic save of ledger JSON: {e}")
            raise e
        self._sync_markdown()

    def add_entry(self, entry: Dict[str, Any]) -> int:
        """Appends a new iteration record to the ledger, enforcing schema validation."""
        if "timestamp" not in entry:
            entry["timestamp"] = datetime.datetime.now().isoformat()

        # Enforce contract schema
        try:
            validated = LedgerEntrySchema.model_validate(entry)
            entry = validated.model_dump()
        except Exception as ve:
            print(f"[Ledger] Contract Notice: Validating with fallback: {ve}")

        self.entries.append(entry)
        self.save()
        return len(self.entries)

    def update_entry(self, index: int, updates: Dict[str, Any]):
        """Updates an existing iteration record in place."""
        if 0 <= index < len(self.entries):
            self.entries[index].update(updates)
            self.entries[index]["updated_at"] = datetime.datetime.now().isoformat()
            self.save()
        else:
            print(f"[Ledger] Warning: update_entry called with out-of-bounds index {index} (total entries: {len(self.entries)})")

    def get_latest_entry(self) -> Optional[Dict[str, Any]]:
        return self.entries[-1] if self.entries else None

    def get_all_mistakes(self) -> List[Dict[str, Any]]:
        """Extracts all recorded mistakes across all iterations."""
        mistakes = []
        for entry in self.entries:
            critic = entry.get("critic_review") or {}
            ref = entry.get("refinement") or {}
            for m in (critic.get("mistakes") or []):
                mistakes.append({
                    "iteration": entry.get("iteration"),
                    "category": m.get("category", "UNKNOWN"),
                    "description": m.get("description", ""),
                    "suggested_fix": m.get("suggested_fix", ""),
                    "status": ref.get("status", "PENDING")
                })
        return mistakes

    def get_summary_of_mistakes_for_prompt(self) -> str:
        """Formats all prior mistakes into a prompt-friendly context string."""
        mistakes = self.get_all_mistakes()
        if not mistakes:
            return "No previous mistakes recorded in ledger. Proceeding from clean slate."
        
        lines = ["--- PAST MISTAKES RECORDED IN PROJECT LEDGER ---"]
        for idx, m in enumerate(mistakes, 1):
            lines.append(
                f"{idx}. [Iter {m['iteration']} | {m['category']} | Status: {m['status']}]\n"
                f"   Problem: {m['description']}\n"
                f"   Prescribed Fix: {m['suggested_fix']}"
            )
        lines.append("--- END OF PAST MISTAKES (DO NOT REPEAT THESE) ---")
        return "\n".join(lines)

    def get_past_hypotheses_for_prompt(self) -> str:
        """Formats previous hypotheses into a context string to avoid duplicates."""
        if not self.entries:
            return "No prior hypotheses tested."
        lines = ["--- PREVIOUSLY TESTED HYPOTHESES ---"]
        for entry in self.entries:
            hyp = entry.get("hypothesis") or {}
            critic = entry.get("critic_review") or {}
            lines.append(
                f"- Iteration {entry.get('iteration')}: {hyp.get('title', 'Untitled')} "
                f"[Verdict: {critic.get('verdict', 'PENDING')}]"
            )
        lines.append("--- END OF PREVIOUS HYPOTHESES ---")
        return "\n".join(lines)

    def _sync_markdown(self):
        """Renders the ledger into a readable, academic Markdown document."""
        md_lines = [
            "# Academic ML Project Ledger & Mistake Audit Trail",
            "",
            "> Persistent shared memory tracking hypotheses, empirical experiments, code mistakes, auditor critiques, and self-healing fixes.",
            "",
            f"*Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
            "",
            "## Summary Table",
            "",
            "| Iteration | Hypothesis Title | Status | Mistakes Detected | Verdict | Fix Status |",
            "|-----------|------------------|--------|-------------------|---------|------------|"
        ]

        if not self.entries:
            md_lines.append("| - | *No iterations logged yet* | - | - | - | - |")
        else:
            for e in self.entries:
                it = e.get("iteration", "?")
                title = (e.get("hypothesis") or {}).get("title", "Untitled")[:40]
                status = (e.get("execution") or {}).get("status", "N/A")
                mistakes_count = len(((e.get("critic_review") or {}).get("mistakes")) or [])
                verdict = (e.get("critic_review") or {}).get("verdict", "PENDING")
                ref_dict = e.get("refinement") or {}
                fix_status = ref_dict.get("status", "N/A")
                md_lines.append(f"| {it} | {title} | `{status}` | {mistakes_count} found | **{verdict}** | `{fix_status}` |")

        md_lines.extend(["", "---", "", "## Detailed Iteration Logs", ""])

        for e in self.entries:
            it = e.get("iteration", "?")
            hyp = e.get("hypothesis") or {}
            exp = e.get("experiment") or {}
            exec_res = e.get("execution") or {}
            critic = e.get("critic_review") or {}
            ref = e.get("refinement") or {}

            md_lines.extend([
                f"### Iteration {it}: {hyp.get('title', 'Untitled')}",
                f"- **Timestamp**: {e.get('timestamp', 'N/A')}",
                f"- **Hypothesis Statement**: {hyp.get('statement', 'N/A')}",
                f"- **Rationale**: {hyp.get('rationale', 'N/A')}",
                f"- **Target Metric**: `{hyp.get('target_metric', 'N/A')}`",
                "",
                "#### Experiment Details",
                f"- **Script**: `{exp.get('script_name', 'N/A')}`",
                f"- **Dataset**: {exp.get('dataset', 'N/A')}",
                f"- **Baseline**: {exp.get('baseline_description', 'N/A')}",
                f"- **Variant Tested**: {exp.get('variant_description', 'N/A')}",
                "",
                "#### Execution Results",
                f"- **Status**: `{exec_res.get('status', 'N/A')}` (Exit Code: `{exec_res.get('exit_code', 'N/A')}`)",
                f"- **Metrics**: `{json.dumps(exec_res.get('metrics', {}))}`",
            ])

            if exec_res.get("stderr"):
                md_lines.extend([
                    "```text",
                    "Execution Traceback / Warnings:",
                    exec_res.get("stderr")[:500],
                    "```"
                ])

            md_lines.extend([
                "",
                "#### Auditor (Critic Agent) Review",
                f"- **Scientific Verdict**: **{critic.get('verdict', 'PENDING')}**",
                f"- **Critique**: {critic.get('critique_summary', 'None')}",
                ""
            ])

            mistakes = critic.get("mistakes", [])
            if mistakes:
                md_lines.append("**Mistakes Logged in Ledger:**")
                for idx, m in enumerate(mistakes, 1):
                    md_lines.append(
                        f"{idx}. **[{m.get('category', 'BUG')}]** {m.get('description', '')}\n"
                        f"   - *Suggested Fix*: {m.get('suggested_fix', '')}"
                    )
            else:
                md_lines.append("*No critical code or methodological mistakes identified.*")

            if ref and ref.get("applied"):
                    re_exec = ref.get("re_execution_result") or {}
                    md_lines.extend([
                        "",
                        "#### Refiner / Fixer Action",
                        f"- **Agent**: `{ref.get('fix_agent', 'RefinerAgent')}`",
                        f"- **Fix Status**: `{ref.get('status', 'PENDING')}`",
                        f"- **Changes Made**: {ref.get('changes_made', 'N/A')}",
                        f"- **Re-Execution Status**: `{re_exec.get('status', 'N/A')}`",
                        f"- **Updated Metrics**: `{json.dumps(re_exec.get('metrics', {}))}`"
                    ])

            md_lines.extend(["", "---", ""])

        # Safety guard against overwriting Codebase Mistake Ledger
        if self.md_path.name.lower() in ("project_mistake_ledger.md", "mistake_ledger.md"):
            raise ValueError(f"[Ledger] Refusing to overwrite Quality Assurance Mistake Ledger at {self.md_path}")
        if self.md_path.exists():
            try:
                with open(self.md_path, "r", encoding="utf-8", errors="ignore") as existing_f:
                    header = existing_f.read(256)
                    if "# Project Mistake Ledger" in header:
                        raise ValueError(f"[Ledger] Target file {self.md_path} contains '# Project Mistake Ledger'. Aborting write.")
            except ValueError:
                raise
            except Exception:
                pass

        temp_md = self.md_path.with_suffix(".tmp")
        try:
            with open(temp_md, "w", encoding="utf-8") as f:
                f.write("\n".join(md_lines))
            os.replace(temp_md, self.md_path)
        except Exception as ex:
            if temp_md.exists():
                try:
                    temp_md.unlink()
                except OSError:
                    pass
            print(f"[Ledger] Warning: Failed to write markdown ledger: {ex}")
