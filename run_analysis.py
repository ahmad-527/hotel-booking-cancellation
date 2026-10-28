"""Verify the fixed input and run the notebook in a fresh Python kernel."""
import argparse
import json
import os
import sys
import time
from pathlib import Path

import nbformat
from jupyter_client import KernelManager
from nbclient import NotebookClient

from scripts.data import check_inputs

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python", default=sys.executable, help="Compatible Python interpreter for the analysis kernel")
    args = parser.parse_args()
    check_inputs()
    for name in ["OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"]:
        os.environ.setdefault(name, "1")
    os.environ.setdefault("HOTEL_MAX_WORKERS", "2")
    notebook = nbformat.read(ROOT / "hotel_cancellation_analysis.ipynb", as_version=4)
    manager = KernelManager(kernel_name="python3")
    manager.kernel_spec.argv = [args.python, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
    client = NotebookClient(notebook, km=manager, timeout=3600,
                            resources={"metadata": {"path": str(ROOT)}})
    client.on_cell_start = lambda cell, cell_index: print(f"Executing cell {cell_index + 1}/{len(notebook.cells)}", flush=True) if cell.cell_type == "code" else None
    (ROOT / "reports").mkdir(exist_ok=True)
    checkpoint = ROOT / "reports/hotel_cancellation_analysis.checkpoint.ipynb"
    client.on_cell_executed = lambda **kwargs: nbformat.write(notebook, checkpoint)
    started = time.monotonic()
    try:
        client.execute()
    finally:
        if manager.has_kernel:
            manager.shutdown_kernel(now=True)
        manager.cleanup_resources()
    output = ROOT / "reports/hotel_cancellation_analysis.executed.ipynb"
    output.parent.mkdir(exist_ok=True)
    nbformat.write(notebook, output)
    print(json.dumps({"elapsed_seconds": round(time.monotonic() - started, 2),
                      "executed_code_cells": sum(cell.cell_type == "code" and cell.execution_count is not None for cell in notebook.cells)}), flush=True)


if __name__ == "__main__":
    main()
