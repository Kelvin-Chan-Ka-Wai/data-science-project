"""Fail if any committed notebook is unexecuted or contains an error.

Used by CI after `nbconvert --execute`; also useful locally:

    python scripts/check_notebooks.py

Exit code 0 = every notebook has been executed and has no error output.
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check(path):
    with open(path, encoding="utf-8") as fh:
        nb = json.load(fh)
    cells = [c for c in nb.get("cells", []) if c.get("cell_type") == "code"]
    unrun = [i for i, c in enumerate(cells) if not c.get("execution_count")]
    errors = [(i, o.get("ename"), str(o.get("evalue"))[:120])
              for i, c in enumerate(cells) for o in c.get("outputs", [])
              if o.get("output_type") == "error"]
    results = sum(1 for c in cells for o in c.get("outputs", [])
                  if o.get("output_type") in ("display_data", "execute_result", "stream"))
    return {"path": path, "cells": len(cells), "unrun": unrun,
            "errors": errors, "results": results}


def main():
    paths = sorted(glob.glob(os.path.join(ROOT, "notebooks", "*.ipynb")))
    if not paths:
        print("no notebooks found")
        return 1
    bad = 0
    for path in paths:
        info = check(path)
        name = os.path.basename(path)
        status = "OK"
        if info["errors"]:
            status = "ERRORS"
        elif info["unrun"]:
            status = "NOT EXECUTED"
        if status != "OK":
            bad += 1
        print("%-40s cells=%-3d results=%-4d %s" % (name, info["cells"], info["results"], status))
        for i, ename, evalue in info["errors"]:
            print("    cell %d: %s: %s" % (i, ename, evalue))
        if info["unrun"]:
            print("    unexecuted cells: %s" % info["unrun"])
    print()
    print("%d/%d notebook(s) OK" % (len(paths) - bad, len(paths)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
