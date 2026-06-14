#!/usr/bin/env python3
"""Verify devlog.html internal anchors resolve and the page is marked.

`unresolved_anchors(html)` returns the list of same-page `#fragment` link
targets that have no matching `id="..."` or `name="..."` in the document.
Used to guard that every arc card jumps to a real milestone. Same-page links
only: an href containing a path or host (e.g. `changelog.html#alpha91` or
`https://.../#x`) is out of scope and ignored.
"""
from __future__ import annotations

import re
import sys

MARKER = "DO-NOT-REGENERATE"


def has_marker(html: str) -> bool:
    return MARKER in html


def unresolved_anchors(html: str) -> list[str]:
    # Same-page fragment links: href="#frag" with nothing before the '#'.
    frags = re.findall(r'href="#([^"]+)"', html)
    ids = set(re.findall(r'\bid="([^"]+)"', html))
    names = set(re.findall(r'\bname="([^"]+)"', html))
    targets = ids | names
    seen: list[str] = []
    for f in frags:
        if f not in targets and f not in seen:
            seen.append(f)
    return seen


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: check_devlog_anchors.py <file.html> [...]", file=sys.stderr)
        return 2
    rc = 0
    for path in argv:
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        if not has_marker(html):
            print(f"ERROR: {path} missing DO-NOT-REGENERATE marker", file=sys.stderr)
            rc = 1
        missing = unresolved_anchors(html)
        if missing:
            print(f"ERROR: {path} has unresolved anchors: {', '.join(missing)}", file=sys.stderr)
            rc = 1
    if rc == 0:
        print("OK: anchors resolve and marker present")
    return rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
