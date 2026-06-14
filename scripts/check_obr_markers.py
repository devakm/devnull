#!/usr/bin/env python3
"""Pre-commit guard for the OOORF release-tracker pages.

For every staged `docs/OOO/OBR/*.html` it verifies, against the STAGED content:
  - the DO-NOT-REGENERATE marker is present (a missing marker can mean a stale
    sync_pages.py clobber — see docs/OOO/OBR/CONTRIBUTING.md);
  - there are no stray control bytes; and
  - the <nav> contains only well-formed anchors.

The last two catch scripted-edit corruption (e.g. a regex backreference that
injected a `\\x01` byte and broke the Changelog nav link) before it reaches the
live site. The structural checks live in check_devlog_anchors.py.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

MARKER = "DO-NOT-REGENERATE"

# Reuse the pure structural checks from the sibling script (scripts/ is not a
# package, so load it by path).
_spec = importlib.util.spec_from_file_location(
    "check_devlog_anchors", Path(__file__).resolve().parent / "check_devlog_anchors.py")
_cda = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cda)
page_problems = _cda.page_problems


def find_unmarked(paths, get_content, marker: str = MARKER) -> list[str]:
    """Pure core (kept for direct use/tests): paths whose content lacks the marker."""
    return [p for p in paths if marker not in (get_content(p) or "")]


def _staged_obr_html() -> list[str]:
    r = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True, text=True, check=True,
    )
    return [
        p for p in r.stdout.splitlines()
        if p.startswith("docs/OOO/OBR/") and p.endswith(".html")
    ]


def _staged_content(path: str) -> str:
    r = subprocess.run(["git", "show", f":{path}"], capture_output=True, text=True,
                        encoding="utf-8", check=True)
    return r.stdout


def main() -> int:
    rc = 0
    for path in _staged_obr_html():
        problems = page_problems(_staged_content(path))
        if problems:
            rc = 1
            print(f"ERROR: {path}", file=sys.stderr)
            for p in problems:
                print(f"  - {p}", file=sys.stderr)
    if rc:
        print("\nThese are hand-canonical OBR pages. A missing marker can mean a regenerator",
              file=sys.stderr)
        print("clobber; control bytes or malformed nav mean a scripted edit corrupted the",
              file=sys.stderr)
        print("HTML. Fix the staged file. See docs/OOO/OBR/CONTRIBUTING.md.", file=sys.stderr)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
