"""
Main entry point for the Academic ML Hypothesis Research Studio.
Leverages high-level workflow abstractions to provide a clean,
professional interface tailored specifically for academic researchers.
"""

import sys
import argparse
import warnings

# Ensure real-time unbuffered terminal output on Windows
try:
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
except Exception:
    pass

from core.workflow import MLHypothesisWorkflow


def main():
    parser = argparse.ArgumentParser(
        description="ML Hypothesis Research Studio: Autonomous Academic Scientific Exploration"
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="Tabular Feature Representations and Neural Ensembling",
        help="Academic ML research domain or hypothesis topic"
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=1,
        help="Number of hypothesis cycles to run (Default: 1 to preserve API quota)"
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Run in offline mock mode without consuming API tokens"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Display low-level agent communication, stack traces, and internal debug logs"
    )
    parser.add_argument(
        "--demo-mistake-fix",
        action="store_true",
        help="Inject a demonstration code mistake to showcase automatic audit & self-healing"
    )
    args = parser.parse_args()

    # Suppress internal SDK noise and warnings unless explicitly running verbose
    if not args.verbose:
        warnings.filterwarnings("ignore")

    workflow = MLHypothesisWorkflow(
        topic=args.topic,
        mock=args.mock,
        verbose=args.verbose
    )
    
    workflow.run(
        iterations=args.iterations,
        demo_mistake_fix=args.demo_mistake_fix
    )


if __name__ == "__main__":
    main()
