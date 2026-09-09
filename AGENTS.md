# Agent Collaboration & Mistake Ledger Guidelines

This project implements an **Agentic Quality Assurance & Mistake Ledger Protocol**.

## Core Roles & Responsibilities

### 1. Codebase Monitor Subagent (`codebase_monitor`)
- **Duty**: Scans codebase for architectural anti-patterns, circular dependencies, syntax errors, contract violations, and type mismatches.
- **Action**: When mistakes or potential defects are found:
  1. Assign an ID conforming to `PROJECT_MISTAKE_LEDGER.md` convention (`ERR-ARCH-###`, `ERR-SYNT-###`, etc.).
  2. Append the detailed entry into `PROJECT_MISTAKE_LEDGER.md` under Section 3.
  3. Register the item in the active table in Section 2 with status `[OPEN]`.
  4. Communicate the summary back to the main agent.

### 2. Primary / Main Agent
- **Duty**: Primary builder, orchestrator, and refactoring engineer.
- **Action**:
  1. Periodically check `PROJECT_MISTAKE_LEDGER.md` for `[OPEN]` items.
  2. Prioritize items by severity (`P0` -> `P1` -> `P2` -> `P3`).
  3. Formulate a fix plan and execute the code refactoring.
  4. Validate the fix with test executions or syntax verifications.
  5. Update the issue status to `[RESOLVED]` in Section 2, record resolution notes in Section 3, and add a log row in Section 4 (Resolution Archive).

## Automated Audit Scripts
- An automated audit utility is located at `scripts/audit_codebase.py`.
- Run `python scripts/audit_codebase.py` to quickly scan all `.py` files in the repository for:
  - Python AST syntax errors
  - Circular import chains
  - Incomplete/stub functions lacking implementation
  - Undefined/broken symbol imports
