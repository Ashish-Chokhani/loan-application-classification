#!/usr/bin/env python3
"""
run_pipeline.py — Execute HMDA 2023 notebooks in sequence
==========================================================
Extracts code cells from each .ipynb and executes them in-process.

Usage:
    python run_pipeline.py --all
    python run_pipeline.py --notebook 3 --skip-download
    python run_pipeline.py --notebook 1
"""

import argparse
import json
import os
import sys
import time

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTEBOOK_DIR = os.path.join(PROJECT_DIR, "notebooks")
sys.path.insert(0, PROJECT_DIR)

NOTEBOOKS = [
    "1_data_ingestion.ipynb",
    "2_eda_comprehensive.ipynb",
    "3_feature_engineering.ipynb",
    "4_model_training.ipynb",
    "5_evaluation_and_analysis.ipynb",
    "6_visualization_export.ipynb",
]


def extract_code_cells(notebook_path):
    """Extract source code from code cells in a notebook."""
    with open(notebook_path, "r") as f:
        nb = json.load(f)
    code_blocks = []
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            source = "".join(cell.get("source", []))
            if source.strip():
                code_blocks.append(source)
    return code_blocks


def run_notebook(notebook_name):
    """Execute all code cells from a notebook in the current process."""
    path = os.path.join(NOTEBOOK_DIR, notebook_name)
    if not os.path.exists(path):
        print(f"  ERROR: {path} not found")
        return False

    print(f"\n{'='*60}")
    print(f"  Running: {notebook_name}")
    print(f"{'='*60}")

    code_cells = extract_code_cells(path)
    print(f"  Found {len(code_cells)} code cells")

    # Change to notebook directory for relative paths
    original_dir = os.getcwd()
    os.chdir(NOTEBOOK_DIR)

    global_ns = {"__name__": "__main__"}
    success = True

    for i, code in enumerate(code_cells, 1):
        try:
            exec(code, global_ns)
            print(f"  Cell {i}/{len(code_cells)} — OK")
        except Exception as e:
            print(f"  Cell {i}/{len(code_cells)} — FAILED: {e}")
            success = False
            break

    os.chdir(original_dir)
    return success


def main():
    parser = argparse.ArgumentParser(description="Run HMDA pipeline notebooks")
    parser.add_argument("--all", action="store_true", help="Run all notebooks")
    parser.add_argument("--notebook", type=int, help="Run specific notebook (1-6)")
    parser.add_argument("--skip-download", action="store_true", help="Skip data download")
    args = parser.parse_args()

    if args.notebook:
        idx = args.notebook - 1
        if 0 <= idx < len(NOTEBOOKS):
            success = run_notebook(NOTEBOOKS[idx])
            sys.exit(0 if success else 1)
        else:
            print(f"Invalid notebook number. Choose 1-{len(NOTEBOOKS)}")
            sys.exit(1)
    elif args.all:
        start_total = time.time()
        results = {}
        for nb in NOTEBOOKS:
            start = time.time()
            ok = run_notebook(nb)
            elapsed = time.time() - start
            results[nb] = {"success": ok, "time": elapsed}
            if not ok:
                print(f"\n  Pipeline stopped at {nb}")
                break

        print(f"\n{'='*60}")
        print("  PIPELINE SUMMARY")
        print(f"{'='*60}")
        for nb, r in results.items():
            status = "PASS" if r["success"] else "FAIL"
            print(f"  {nb:<45} {status}  ({r['time']:.1f}s)")
        print(f"  Total time: {time.time() - start_total:.1f}s")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
