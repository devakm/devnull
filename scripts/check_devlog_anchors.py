#!/usr/bin/env python3
"""Structural checks for the OOORF release-tracker HTML pages.

Pure helpers (no I/O), reused by the pre-commit guard:

- `has_marker(html)`        — the DO-NOT-REGENERATE marker is present.
- `unresolved_anchors(html)`— same-page `#fragment` links with no matching
  `id`/`name` (used to verify devlog arc cards jump to real milestones).
  Same-page links only: an href with a path or host (e.g.
  `changelog.html#alpha91`, `https://.../#x`) is ignored.
- `control_chars(html)`     — stray control bytes (anything < 0x20 except
  tab/newline/cr). Catches corruption like the `\\x01` a buggy regex
  backreference once injected into the nav.
- `malformed_nav(html)`     — text left in the `<nav>` after removing
  well-formed `<a ...>...</a>` links and separators, i.e. a broken anchor
  such as a dropped opening tag leaving `>Changelog`.

Run directly to check the devlog (anchors + the structural checks):
    python scripts/check_devlog_anchors.py docs/OOO/OBR/devlog.html
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


def control_chars(html: str) -> list[tuple[int, int]]:
    """(offset, codepoint) for each disallowed control character."""
    return [(i, ord(c)) for i, c in enumerate(html)
            if ord(c) < 32 and c not in "\t\n\r"]


def malformed_nav(html: str) -> list[str]:
    """Residue text in the first <nav> after removing well-formed anchors and
    separators. Non-empty means a broken nav anchor. Returns a one-item list
    with the offending residue (truncated), or [] when the nav is clean."""
    m = re.search(r"<nav\b[^>]*>(.*?)</nav>", html, re.S)
    if not m:
        return []
    residue = re.sub(r"<a\b[^>]*>.*?</a>", "", m.group(1), flags=re.S)
    residue = residue.replace("|", "").strip()
    return [residue[:80]] if residue else []


def page_problems(html: str, *, check_anchors: bool = False) -> list[str]:
    """All structural problems for one page, as human-readable strings."""
    problems: list[str] = []
    if not has_marker(html):
        problems.append("missing DO-NOT-REGENERATE marker")
    for offset, cp in control_chars(html):
        problems.append(f"control character U+{cp:04X} at offset {offset}")
    for residue in malformed_nav(html):
        problems.append(f"malformed nav (text outside anchors): {residue!r}")
    if check_anchors:
        for a in unresolved_anchors(html):
            problems.append(f"unresolved anchor #{a}")
    return problems


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: check_devlog_anchors.py <file.html> [...]", file=sys.stderr)
        return 2
    rc = 0
    for path in argv:
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        problems = page_problems(html, check_anchors=True)
        if problems:
            rc = 1
            print(f"ERROR: {path}", file=sys.stderr)
            for p in problems:
                print(f"  - {p}", file=sys.stderr)
    if rc == 0:
        print("OK: marker present, no control bytes, nav well-formed, anchors resolve")
    return rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
