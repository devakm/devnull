#!/usr/bin/env python3
"""Pre-commit guard for the OOORF release-tracker pages.

Every staged file matching docs/OOO/OBR/*.html must carry the
DO-NOT-REGENERATE marker. These pages are hand-canonical; a stale run of the
OOO repo's sync_pages.py would strip the marker, so a missing marker means you
are about to commit a regenerator clobber. See docs/OOO/OBR/CONTRIBUTING.md.
"""
from __future__ import annotations

import subprocess
import sys

MARKER = "DO-NOT-REGENERATE"


def find_unmarked(paths, get_content, marker: str = MARKER) -> list[str]:
    """Pure core: return the subset of paths whose content lacks the marker."""
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
    unmarked = find_unmarked(_staged_obr_html(), _staged_content)
    if unmarked:
        print("ERROR: hand-canonical OBR pages are missing the DO-NOT-REGENERATE marker:",
              file=sys.stderr)
        for p in unmarked:
            print(f"  {p}", file=sys.stderr)
        print("\nThese pages must not be regenerated. If a stale sync_pages.py stripped the",
              file=sys.stderr)
        print("marker, you are about to commit a clobber. See docs/OOO/OBR/CONTRIBUTING.md.",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
