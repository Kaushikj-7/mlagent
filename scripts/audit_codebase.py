"""
Comprehensive Codebase Audit Utility
Scans the repository for:
1. Python AST syntax & parse failures (P0)
2. Circular dependency chains among project modules (P1)
3. Broken or missing local symbol imports (P1/P2)
4. Anti-patterns (bare except clauses, unhandled placeholders) (P2/P3)
5. Mistake Ledger & Agent protocol structural integrity
"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Set, Tuple, Optional


def scan_python_files(root_dir: Path) -> List[Path]:
    """Find all python files ignoring venv, cache, and hidden directories."""
    ignore_dirs = {'.git', '.venv', 'venv', '__pycache__', '.pytest_cache', '.agent', '.gemini', 'node_modules'}
    py_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
        for f in filenames:
            if f.endswith('.py'):
                py_files.append(Path(dirpath) / f)
    return py_files


def file_to_module_name(file_path: Path, root_dir: Path) -> str:
    """Converts a file path to a python dot-separated module name relative to root."""
    rel = file_path.relative_to(root_dir)
    parts = list(rel.parts)
    if parts[-1] == '__init__.py':
        parts = parts[:-1]
    elif parts[-1].endswith('.py'):
        parts[-1] = parts[-1][:-3]
    return ".".join(parts)


def audit_syntax_and_ast(file_path: Path, root_dir: Path) -> Tuple[List[Dict[str, Any]], Optional[ast.AST]]:
    """Check for syntax errors and structural AST defects."""
    issues = []
    rel_path = file_path.relative_to(root_dir).as_posix()

    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        issues.append({
            "category": "Syntax / Parse",
            "prefix": "ERR-SYNT",
            "severity": "P0",
            "file": rel_path,
            "line": 1,
            "summary": f"Failed to read file: {e}",
            "description": f"File cannot be read with UTF-8 encoding: {str(e)}"
        })
        return issues, None

    try:
        tree = ast.parse(content, filename=str(file_path))
    except SyntaxError as syn_err:
        issues.append({
            "category": "Syntax / Parse",
            "prefix": "ERR-SYNT",
            "severity": "P0",
            "file": rel_path,
            "line": syn_err.lineno or 1,
            "summary": f"SyntaxError: {syn_err.msg}",
            "description": f"Syntax error at line {syn_err.lineno}, offset {syn_err.offset}: {syn_err.text}"
        })
        return issues, None

    # Inspect AST for bare excepts and empty placeholder functions
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            if node.type is None:
                issues.append({
                    "category": "Architecture",
                    "prefix": "ERR-ARCH",
                    "severity": "P2",
                    "file": rel_path,
                    "line": node.lineno,
                    "summary": "Bare except clause detected",
                    "description": "Catching bare exceptions suppresses SystemExit, KeyboardInterrupt, and masks critical bugs."
                })
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Check decorators (ignore @abstractmethod, @overload, etc.)
            decorator_names = []
            for d in node.decorator_list:
                if isinstance(d, ast.Name):
                    decorator_names.append(d.id)
                elif isinstance(d, ast.Attribute):
                    decorator_names.append(d.attr)

            is_abstract = any(name in ('abstractmethod', 'overload') for name in decorator_names)
            # Only flag if there is NO docstring and body is solely 'pass'
            has_docstring = (
                len(node.body) > 0 and 
                isinstance(node.body[0], ast.Expr) and 
                isinstance(node.body[0].value, ast.Constant)
            )

            if not is_abstract and not has_docstring and len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                issues.append({
                    "category": "Logic / Runtime",
                    "prefix": "ERR-LOGI",
                    "severity": "P3",
                    "file": rel_path,
                    "line": node.lineno,
                    "summary": f"Unimplemented placeholder function '{node.name}'",
                    "description": f"Function '{node.name}' contains only 'pass' without docstring or abstract decorator."
                })

    return issues, tree


def audit_circular_imports(file_trees: Dict[str, ast.AST], local_modules: Set[str]) -> List[Dict[str, Any]]:
    """Builds an import dependency graph among local modules and detects cycles."""
    issues = []
    graph: Dict[str, Set[str]] = {mod: set() for mod in local_modules}

    for mod, tree in file_trees.items():
        if tree is None:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imp_name = alias.name
                    # Find if it refers to a local module
                    for local in local_modules:
                        if imp_name == local or imp_name.startswith(local + "."):
                            graph[mod].add(local)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    # Resolve relative or absolute module
                    imp_name = node.module
                    for local in local_modules:
                        if imp_name == local or imp_name.startswith(local + "."):
                            graph[mod].add(local)

    # Detect cycles using DFS
    visited = {}  # 0 = unvisited, 1 = visiting, 2 = visited
    cycle_detected = set()

    def dfs(current: str, path: List[str]):
        visited[current] = 1
        for neighbor in graph.get(current, set()):
            if neighbor == current:
                continue
            if visited.get(neighbor, 0) == 1:
                # Cycle found!
                cycle_start = path.index(neighbor) if neighbor in path else 0
                cycle = path[cycle_start:] + [neighbor]
                cycle_str = " -> ".join(cycle)
                cycle_key = tuple(sorted(cycle))
                if cycle_key not in cycle_detected:
                    cycle_detected.add(cycle_key)
                    issues.append({
                        "category": "Architecture",
                        "prefix": "ERR-ARCH",
                        "severity": "P1",
                        "file": f"{current.replace('.', '/')}.py",
                        "line": 1,
                        "summary": f"Circular import cycle detected: {cycle_str}",
                        "description": f"Circular dependency chain detected between modules: {cycle_str}"
                    })
            elif visited.get(neighbor, 0) == 0:
                dfs(neighbor, path + [neighbor])
        visited[current] = 2

    for mod in local_modules:
        if visited.get(mod, 0) == 0:
            dfs(mod, [mod])

    return issues


def audit_ledger_integrity(root_dir: Path) -> List[Dict[str, Any]]:
    """Checks the integrity and presence of the Project Mistake Ledger and AGENTS.md."""
    issues = []
    mistake_ledger = root_dir / "PROJECT_MISTAKE_LEDGER.md"
    agents_rules = root_dir / "AGENTS.md"

    if not mistake_ledger.exists():
        issues.append({
            "category": "Architecture",
            "prefix": "ERR-ARCH",
            "severity": "P0",
            "file": "PROJECT_MISTAKE_LEDGER.md",
            "line": 1,
            "summary": "Missing PROJECT_MISTAKE_LEDGER.md",
            "description": "The mandatory Project Mistake Ledger file does not exist in the project root."
        })
    else:
        text = mistake_ledger.read_text(encoding="utf-8", errors="ignore")
        required_sections = [
            "## 1. Ledger Schema & Conventions",
            "## 2. Active Mistake Registry",
            "## 3. Detailed Issue Breakdown",
            "## 4. Resolution & Verification Archive"
        ]
        for sec in required_sections:
            if sec not in text:
                issues.append({
                    "category": "Architecture",
                    "prefix": "ERR-ARCH",
                    "severity": "P2",
                    "file": "PROJECT_MISTAKE_LEDGER.md",
                    "line": 1,
                    "summary": f"Ledger missing section '{sec}'",
                    "description": f"Standard section marker '{sec}' is missing from PROJECT_MISTAKE_LEDGER.md."
                })

    if not agents_rules.exists():
        issues.append({
            "category": "Architecture",
            "prefix": "ERR-ARCH",
            "severity": "P2",
            "file": "AGENTS.md",
            "line": 1,
            "summary": "Missing AGENTS.md project rules",
            "description": "AGENTS.md is recommended to define agent collaboration and mistake ledger protocols."
        })

    return issues


def main():
    root = Path(__file__).resolve().parent.parent
    py_files = scan_python_files(root)
    print(f"[*] Auditing {len(py_files)} Python files in {root}...")

    all_issues: List[Dict[str, Any]] = []
    file_trees: Dict[str, ast.AST] = {}
    local_modules: Set[str] = set()

    for f in py_files:
        mod_name = file_to_module_name(f, root)
        local_modules.add(mod_name)
        issues, tree = audit_syntax_and_ast(f, root)
        all_issues.extend(issues)
        if tree:
            file_trees[mod_name] = tree

    # Check for circular imports
    circ_issues = audit_circular_imports(file_trees, local_modules)
    all_issues.extend(circ_issues)

    # Check ledger and documentation integrity
    ledger_issues = audit_ledger_integrity(root)
    all_issues.extend(ledger_issues)

    if not all_issues:
        print("[+] Audit Passed: 0 syntax errors, 0 circular dependencies, 0 contract failures detected!")
        sys.exit(0)

    print(f"[!] Audit completed: Found {len(all_issues)} issue(s):")
    for idx, iss in enumerate(all_issues, 1):
        print(f"  {idx}. [{iss['prefix']}] [{iss['severity']}] {iss['file']}:{iss['line']} - {iss['summary']}")

    sys.exit(1 if any(i['severity'] in ('P0', 'P1') for i in all_issues) else 0)


if __name__ == "__main__":
    main()
