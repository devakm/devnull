# OOORF Regen Guard-Rails Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make it structurally impossible for the OOO Markdown regenerator to silently clobber the hand-curated `docs/OOO/OBR/` pages again, and fix the converter bugs that motivated the hand edits.

**Architecture:** Two repos. In `OblivionRemastered_OOO`, `scripts/sync_pages.py` is reworked from an always-writing tool into a **diff-by-default advisor** that, with `--apply`, refuses to overwrite any file carrying a `DO-NOT-REGENERATE` marker; its Markdown converter gains tables, fenced code blocks, and `target="_blank"` external links. In `devnull`, every OBR page gets the marker, a tracked `pre-commit` guard rejects any OBR page committed without it, and a `CONTRIBUTING.md` documents the contract.

**Tech Stack:** Python 3.12 (stdlib only: `re`, `html`, `difflib`, `subprocess`, `pathlib`), pytest for tests, POSIX `sh` git hook (Git Bash on Windows), HTML.

**Repos & absolute paths:**
- devnull: `x:\dev\devnull`
- OOO: `x:\dev\OblivionRemastered_OOO`

**The marker string (used identically in both repos):**
```
<!-- DO-NOT-REGENERATE: hand-canonical. See docs/OOO/OBR/CONTRIBUTING.md -->
```
The substring that both `sync_pages.py` and the pre-commit guard test for is `DO-NOT-REGENERATE`.

---

## File Structure

**OblivionRemastered_OOO:**
- Modify: `scripts/sync_pages.py` — converter fixes + diff/apply rework + marker skip
- Create: `tests/test_sync_pages.py` — unit tests for converter + skip logic
- Create: `tests/__init__.py` — empty (makes `tests` importable if needed)

**devnull:**
- Modify: `docs/OOO/OBR/{index,overview,new-Items,changelog,install,dependencies}.html` — insert marker
- Create: `scripts/check_obr_markers.py` — pure-logic marker check + git glue
- Create: `tests/test_check_obr_markers.py` — unit test for the pure logic
- Create: `scripts/hooks/pre-commit` — tracked hook template
- Create: `scripts/install-hooks.sh` — installs the template into `.git/hooks`
- Create: `docs/OOO/OBR/CONTRIBUTING.md` — the ownership contract (published; keep terse)

---

## Part 1 — OOO repo: rework `sync_pages.py`

All commands in Part 1 run from `x:\dev\OblivionRemastered_OOO`.

### Task 1: Test scaffold + ensure pytest

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/test_sync_pages.py`

- [ ] **Step 1: Ensure pytest is available**

Run: `python -m pytest --version`
Expected: prints a version. If it errors with "No module named pytest", run `python -m pip install pytest` and retry.

- [ ] **Step 2: Create empty package marker**

Create `tests/__init__.py` with no content (empty file).

- [ ] **Step 3: Create the test file importing the module under test**

`sync_pages.py` lives in `scripts/`, which is not a package. Import it by path. Create `tests/test_sync_pages.py`:

```python
import importlib.util
from pathlib import Path

_MODULE_PATH = Path(__file__).resolve().parent.parent / "scripts" / "sync_pages.py"
_spec = importlib.util.spec_from_file_location("sync_pages", _MODULE_PATH)
sync_pages = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sync_pages)


def test_module_imports():
    assert hasattr(sync_pages, "md_to_simple_html")
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest tests/test_sync_pages.py -v`
Expected: `test_module_imports PASSED`

- [ ] **Step 5: Commit**

```bash
git add tests/__init__.py tests/test_sync_pages.py
git commit -m "test: scaffold sync_pages tests"
```

### Task 2: Converter — fenced code blocks, tables, external links (TDD)

**Files:**
- Modify: `scripts/sync_pages.py:98-145` (the `md_to_simple_html` function)
- Modify: `tests/test_sync_pages.py`

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_sync_pages.py`:

```python
def test_fenced_code_block_becomes_pre_code():
    md = "```bash\ngit diff a..b\necho hi\n```"
    out = sync_pages.md_to_simple_html(md)
    assert "<pre><code>" in out
    assert "git diff a..b\necho hi" in out
    assert "</code></pre>" in out
    assert "<p>```bash</p>" not in out


def test_pipe_table_becomes_html_table():
    md = "| Name | Size |\n| --- | --- |\n| alpha91 | 215.9 MiB |"
    out = sync_pages.md_to_simple_html(md)
    assert "<table>" in out
    assert "<th>Name</th>" in out
    assert "<td>alpha91</td>" in out
    assert "<p>| Name | Size |</p>" not in out


def test_external_links_get_target_blank():
    md = "See [the repo](https://github.com/devakm/OblivionRemastered_OOO)."
    out = sync_pages.md_to_simple_html(md)
    assert 'target="_blank"' in out
    assert 'rel="noopener"' in out


def test_internal_links_stay_plain():
    md = "See [install](install.html)."
    out = sync_pages.md_to_simple_html(md)
    assert '<a href="install.html">install</a>' in out
    assert 'target="_blank"' not in out
```

- [ ] **Step 2: Run to verify they fail**

Run: `python -m pytest tests/test_sync_pages.py -v`
Expected: the 4 new tests FAIL (current converter emits `<p>` for fences/tables and plain links).

- [ ] **Step 3: Replace `md_to_simple_html` with the index-based rewrite**

Replace the entire function (lines ~98-145) with:

```python
def md_to_simple_html(md: str) -> str:
    """Markdown -> HTML for our per-release docs and handwritten docs/*.md.
    Supports headings, lists, paragraphs, code spans, links, bold, italic,
    fenced code blocks, and pipe tables. External (http/https) links get
    target=_blank rel=noopener. NOT a general-purpose Markdown renderer."""
    lines = md.splitlines()
    out: list[str] = []
    in_ul = False
    i = 0
    n = len(lines)

    def flush_ul():
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    def render_inline(s: str) -> str:
        s = html.escape(s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)

        def link_sub(m: "re.Match[str]") -> str:
            text, url = m.group(1), m.group(2)
            if url.startswith(("http://", "https://")):
                return f'<a href="{url}" target="_blank" rel="noopener">{text}</a>'
            return f'<a href="{url}">{text}</a>'

        return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_sub, s)

    def is_table_sep(s: str) -> bool:
        return bool(re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$", s))

    def split_row(s: str) -> list[str]:
        s = s.strip()
        if s.startswith("|"):
            s = s[1:]
        if s.endswith("|"):
            s = s[:-1]
        return [c.strip() for c in s.split("|")]

    while i < n:
        line = lines[i]

        if re.match(r"^```(\w*)\s*$", line):
            flush_ul()
            code_lines: list[str] = []
            i += 1
            while i < n and not re.match(r"^```\s*$", lines[i]):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip the closing fence
            out.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
            continue

        if line.lstrip().startswith("|") and i + 1 < n and is_table_sep(lines[i + 1]):
            flush_ul()
            headers = split_row(line)
            i += 2  # consume header + separator
            rows: list[list[str]] = []
            while i < n and lines[i].lstrip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            thead = "".join(f"<th>{render_inline(h)}</th>" for h in headers)
            tbody = "".join(
                "<tr>" + "".join(f"<td>{render_inline(c)}</td>" for c in row) + "</tr>"
                for row in rows
            )
            out.append(f"<table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table>")
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush_ul()
            out.append(f"<h{len(m.group(1))}>{render_inline(m.group(2))}</h{len(m.group(1))}>")
            i += 1
            continue

        if line.startswith("- "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{render_inline(line[2:])}</li>")
            i += 1
            continue

        if line.strip() == "":
            flush_ul()
            out.append("")
            i += 1
            continue

        flush_ul()
        out.append(f"<p>{render_inline(line)}</p>")
        i += 1

    flush_ul()
    return "\n".join(out)
```

- [ ] **Step 4: Run to verify all converter tests pass**

Run: `python -m pytest tests/test_sync_pages.py -v`
Expected: all tests PASS (the 4 new + the import test).

- [ ] **Step 5: Commit**

```bash
git add scripts/sync_pages.py tests/test_sync_pages.py
git commit -m "fix(sync_pages): render tables, code fences, external-link attrs (R4)"
```

### Task 3: `page_shell` naming + nav order (TDD)

**Files:**
- Modify: `scripts/sync_pages.py:148-160` (the `nav_links` list and `<h1>` inside `page_shell`)
- Modify: `tests/test_sync_pages.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_sync_pages.py`:

```python
def test_nav_has_overview_and_new_items_in_order():
    shell = sync_pages.page_shell("T", "<p>body</p>", active_nav="Home")
    # New Items must be present and appear after Overview, before Changelog.
    assert ">New Items</a>" in shell
    i_over = shell.index(">Overview</a>")
    i_new = shell.index(">New Items</a>")
    i_chg = shell.index(">Changelog</a>")
    assert i_over < i_new < i_chg


def test_branding_mentions_ooorf():
    shell = sync_pages.page_shell("T", "<p>body</p>")
    assert "OOORF" in shell
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_sync_pages.py::test_nav_has_overview_and_new_items_in_order tests/test_sync_pages.py::test_branding_mentions_ooorf -v`
Expected: FAIL (current nav lacks New Items/Overview ordering; h1 has no "OOORF").

- [ ] **Step 3: Edit `page_shell`**

Replace the `nav_links` list (currently lines ~149-155) with:

```python
    nav_links = [
        ("index.html", "Home"),
        ("overview.html", "Overview"),
        ("new-Items.html", "New Items"),
        ("changelog.html", "Changelog"),
        ("install.html", "Install"),
        ("dependencies.html", "Dependencies"),
    ]
```

And change the `<h1>` line (currently `<h1>Oscuro's Oblivion Overhaul Remastered FULL</h1>`) to:

```python
      <h1>Oscuro's Oblivion Overhaul Remastered FULL (OOORF)</h1>
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest tests/test_sync_pages.py -v`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/sync_pages.py tests/test_sync_pages.py
git commit -m "fix(sync_pages): OOORF branding + Overview/New Items nav order"
```

### Task 4: Diff-by-default + `--apply` with marker skip (TDD)

**Files:**
- Modify: `scripts/sync_pages.py` — add module constant + helper, rewrite `main`
- Modify: `tests/test_sync_pages.py`

- [ ] **Step 1: Write the failing test for the skip helper**

Append to `tests/test_sync_pages.py`:

```python
def test_should_skip_true_when_marker_present(tmp_path):
    f = tmp_path / "overview.html"
    f.write_text("<!DOCTYPE html>\n<!-- DO-NOT-REGENERATE: x -->\n<html></html>", encoding="utf-8")
    assert sync_pages.should_skip(f) is True


def test_should_skip_false_when_marker_absent(tmp_path):
    f = tmp_path / "overview.html"
    f.write_text("<!DOCTYPE html>\n<html></html>", encoding="utf-8")
    assert sync_pages.should_skip(f) is False


def test_should_skip_false_when_file_missing(tmp_path):
    assert sync_pages.should_skip(tmp_path / "nope.html") is False
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_sync_pages.py -k should_skip -v`
Expected: FAIL with `AttributeError: module 'sync_pages' has no attribute 'should_skip'`.

- [ ] **Step 3: Add the constant + helper**

Add near the top of `sync_pages.py`, just after the `CSS_HREF` definition (~line 49):

```python
REGEN_MARKER = "DO-NOT-REGENERATE"


def should_skip(dest: Path) -> bool:
    """True if the destination is hand-canonical and must not be overwritten."""
    if not dest.exists():
        return False
    return REGEN_MARKER in dest.read_text(encoding="utf-8", errors="replace")
```

- [ ] **Step 4: Run to verify the helper tests pass**

Run: `python -m pytest tests/test_sync_pages.py -k should_skip -v`
Expected: PASS.

- [ ] **Step 5: Rewrite `main` for diff-default + `--apply`**

Replace the body of `main()` (lines ~258-292) with:

```python
def main() -> int:
    import difflib

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true",
                    help="write pages (skips any file containing the DO-NOT-REGENERATE "
                         "marker); default is diff-only, writes nothing")
    ap.add_argument("--max-changelog", type=int, default=0,
                    help="cap the changelog to N most-recent releases (0 = all)")
    args = ap.parse_args()

    all_tags = list_main_line_tags()
    if not all_tags:
        raise SystemExit("no main-line tags found in repo. Run backfill_history.py first.")
    latest = all_tags[-1]
    print(f"[sync_pages] {len(all_tags)} tags, latest = {latest}", file=sys.stderr)

    pages = {
        "index.html": render_index(latest, all_tags),
        "changelog.html": render_changelog(all_tags, args.max_changelog),
        "install.html": render_doc_page("installation", "Install", "Install"),
        "dependencies.html": render_doc_page("dependencies", "Dependencies", "Dependencies"),
        "overview.html": render_doc_page("overview", "Overview", "Overview"),
    }

    if not args.apply:
        any_diff = False
        for name, content in pages.items():
            dest = PAGES_DEST / name
            current = dest.read_text(encoding="utf-8", errors="replace") if dest.exists() else ""
            diff = "".join(difflib.unified_diff(
                current.splitlines(keepends=True),
                content.splitlines(keepends=True),
                fromfile=f"a/{name}", tofile=f"b/{name}",
            ))
            if diff:
                any_diff = True
                marked = " [DO-NOT-REGENERATE — would be skipped by --apply]" if should_skip(dest) else ""
                print(f"\n===== {name}{marked} =====")
                print(diff)
        if not any_diff:
            print("[sync_pages] no differences against the live pages.", file=sys.stderr)
        print("[sync_pages] diff-only (default). Re-run with --apply to write UNMARKED files.",
              file=sys.stderr)
        return 0

    PAGES_DEST.mkdir(parents=True, exist_ok=True)
    for name, content in pages.items():
        dest = PAGES_DEST / name
        if should_skip(dest):
            print(f"[sync_pages] SKIP {dest} (DO-NOT-REGENERATE marker present)", file=sys.stderr)
            continue
        dest.write_text(content, encoding="utf-8")
        print(f"[sync_pages] wrote {dest} ({len(content)} bytes)", file=sys.stderr)

    print(f"[sync_pages] done. Review under {PAGES_DEST}, then commit + push the devnull repo.",
          file=sys.stderr)
    return 0
```

Also update the module docstring usage block (lines ~23-26): replace the `--dry-run` line with:
```
    python scripts/sync_pages.py                   # DIFF only (writes nothing) — DEFAULT
    python scripts/sync_pages.py --apply           # write pages, skipping DO-NOT-REGENERATE files
    python scripts/sync_pages.py --apply --max-changelog 20
```

- [ ] **Step 6: Run the full suite + a real diff smoke test**

Run: `python -m pytest tests/test_sync_pages.py -v`
Expected: all PASS.

Run: `python scripts/sync_pages.py`
Expected: prints unified diffs (the live OBR pages are hand-canonical, so each marked page shows `[DO-NOT-REGENERATE — would be skipped by --apply]`), writes nothing, exits 0. (Requires the marker already present — if Part 2 Task 6 hasn't run yet, the marked annotation simply won't appear; the diff still prints.)

- [ ] **Step 7: Verify `--apply` skips marked files (manual, non-destructive)**

Run: `python scripts/sync_pages.py --apply` only AFTER Part 2 Task 6 has added markers to the live pages.
Expected: every line is `SKIP ... (DO-NOT-REGENERATE marker present)`; `git -C x:/dev/devnull status` shows no changes to `docs/OOO/OBR/`.

- [ ] **Step 8: Commit**

```bash
git add scripts/sync_pages.py tests/test_sync_pages.py
git commit -m "feat(sync_pages): diff-by-default advisor; --apply skips DO-NOT-REGENERATE (R3)"
```

---

## Part 2 — devnull repo: markers, guard, contract

All commands in Part 2 run from `x:\dev\devnull`.

### Task 5: Marker-check core + test (TDD)

**Files:**
- Create: `scripts/check_obr_markers.py`
- Create: `tests/test_check_obr_markers.py`
- Create: `tests/__init__.py` (empty)

- [ ] **Step 1: Write the failing test for the pure logic**

Create `tests/test_check_obr_markers.py`:

```python
import importlib.util
from pathlib import Path

_MODULE_PATH = Path(__file__).resolve().parent.parent / "scripts" / "check_obr_markers.py"
_spec = importlib.util.spec_from_file_location("check_obr_markers", _MODULE_PATH)
check = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check)


def test_find_unmarked_flags_missing_marker():
    content = {
        "docs/OOO/OBR/overview.html": "<!DOCTYPE html>\n<!-- DO-NOT-REGENERATE -->\n",
        "docs/OOO/OBR/index.html": "<!DOCTYPE html>\n<html></html>",
    }
    unmarked = check.find_unmarked(list(content), content.get)
    assert unmarked == ["docs/OOO/OBR/index.html"]


def test_find_unmarked_empty_when_all_marked():
    content = {"docs/OOO/OBR/a.html": "x DO-NOT-REGENERATE y"}
    assert check.find_unmarked(list(content), content.get) == []
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_check_obr_markers.py -v`
Expected: FAIL (`check_obr_markers.py` does not exist yet).

- [ ] **Step 3: Create the script**

Create `scripts/check_obr_markers.py`:

```python
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
    r = subprocess.run(["git", "show", f":{path}"], capture_output=True, text=True, check=True)
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
```

- [ ] **Step 4: Create empty `tests/__init__.py`**

Create `tests/__init__.py` with no content.

- [ ] **Step 5: Run to verify it passes**

Run: `python -m pytest tests/test_check_obr_markers.py -v`
Expected: both tests PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/check_obr_markers.py tests/test_check_obr_markers.py tests/__init__.py
git commit -m "feat: OBR marker-check core for pre-commit guard"
```

### Task 6: Insert the DO-NOT-REGENERATE marker into all six OBR pages

**Files:**
- Modify: `docs/OOO/OBR/index.html`, `overview.html`, `new-Items.html`, `changelog.html`, `install.html`, `dependencies.html`

- [ ] **Step 1: Insert the marker after the doctype in each file**

Run this idempotent inserter (Git Bash):

```bash
cd x:/dev/devnull
MARKER='<!-- DO-NOT-REGENERATE: hand-canonical. See docs/OOO/OBR/CONTRIBUTING.md -->'
for f in index overview new-Items changelog install dependencies; do
  p="docs/OOO/OBR/$f.html"
  if grep -q "DO-NOT-REGENERATE" "$p"; then
    echo "already marked: $p"
  else
    python - "$p" "$MARKER" <<'PY'
import sys, io
path, marker = sys.argv[1], sys.argv[2]
text = io.open(path, encoding="utf-8").read()
nl = "\r\n" if "\r\n" in text else "\n"
idx = text.lower().find("<!doctype html>")
assert idx != -1, f"no doctype in {path}"
end = text.index("\n", idx) + 1
text = text[:end] + marker + nl + text[end:]
io.open(path, "w", encoding="utf-8", newline="").write(text)
print("marked:", path)
PY
  fi
done
```

- [ ] **Step 2: Verify all six are marked**

Run: `grep -c "DO-NOT-REGENERATE" docs/OOO/OBR/*.html`
Expected: each of the six files reports `1`.

- [ ] **Step 3: Sanity-check the pages still render (open one)**

Run: `python -c "import pathlib; print(pathlib.Path('docs/OOO/OBR/overview.html').read_text(encoding='utf-8')[:200])"`
Expected: the doctype, then the marker comment, then the `<html>` opening — no corruption.

- [ ] **Step 4: Commit**

```bash
git add docs/OOO/OBR/index.html docs/OOO/OBR/overview.html docs/OOO/OBR/new-Items.html docs/OOO/OBR/changelog.html docs/OOO/OBR/install.html docs/OOO/OBR/dependencies.html
git commit -m "OOO/OBR: mark all pages DO-NOT-REGENERATE (hand-canonical)"
```

### Task 7: Tracked pre-commit hook + installer

**Files:**
- Create: `scripts/hooks/pre-commit`
- Create: `scripts/install-hooks.sh`

- [ ] **Step 1: Create the tracked hook template**

Create `scripts/hooks/pre-commit`:

```sh
#!/bin/sh
# devnull pre-commit guard. Installed into .git/hooks by scripts/install-hooks.sh.
# Rejects any staged docs/OOO/OBR/*.html that lost its DO-NOT-REGENERATE marker.
exec python scripts/check_obr_markers.py
```

- [ ] **Step 2: Create the installer**

Create `scripts/install-hooks.sh`:

```sh
#!/bin/sh
# Install devnull's tracked git hooks into .git/hooks.
# Re-run after cloning. Safe to run repeatedly.
set -e
repo_root=$(git rev-parse --show-toplevel)
src="$repo_root/scripts/hooks"
dst="$repo_root/.git/hooks"
for hook in "$src"/*; do
  name=$(basename "$hook")
  if [ -e "$dst/$name" ] && ! cmp -s "$hook" "$dst/$name"; then
    echo "WARNING: $dst/$name exists and differs; backing up to $dst/$name.bak"
    cp "$dst/$name" "$dst/$name.bak"
  fi
  cp "$hook" "$dst/$name"
  chmod +x "$dst/$name"
  echo "installed: $dst/$name"
done
```

- [ ] **Step 3: Install the hook**

Run: `sh scripts/install-hooks.sh`
Expected: `installed: .../.git/hooks/pre-commit`. (There is no existing `pre-commit`, so no backup is made; the existing `commit-msg`/`post-commit`/`pre-push` are untouched.)

- [ ] **Step 4: Prove the guard fails on a missing marker**

```bash
cp docs/OOO/OBR/install.html /tmp/install.bak
python - <<'PY'
import io
p="docs/OOO/OBR/install.html"
t=io.open(p,encoding="utf-8").read().replace("DO-NOT-REGENERATE","REGEN-OK")
io.open(p,"w",encoding="utf-8",newline="").write(t)
PY
git add docs/OOO/OBR/install.html
git commit -m "should be blocked" ; echo "exit=$?"
```
Expected: commit is **blocked**, stderr names `docs/OOO/OBR/install.html`, `exit` is non-zero.

- [ ] **Step 5: Restore the file and confirm a clean commit passes**

```bash
cp /tmp/install.bak docs/OOO/OBR/install.html
git add docs/OOO/OBR/install.html
git status   # should show no staged change to install.html (identical to HEAD)
```
Expected: marker restored; nothing to commit for that file.

- [ ] **Step 6: Commit the hook machinery**

```bash
git add scripts/hooks/pre-commit scripts/install-hooks.sh
git commit -m "build: tracked pre-commit guard + installer for OBR marker check"
```

### Task 8: CONTRIBUTING.md (the ownership contract)

**Files:**
- Create: `docs/OOO/OBR/CONTRIBUTING.md`

- [ ] **Step 1: Write the contract**

Create `docs/OOO/OBR/CONTRIBUTING.md`:

```markdown
# Contributing to the OOORF release-tracker pages

These pages (`docs/OOO/OBR/*.html`) have two potential contributors: **hand
edits in this repo** and an **auto-generator** (`scripts/sync_pages.py`) in the
companion repo `OblivionRemastered_OOO`. This file is the contract that keeps
them from clobbering each other.

## Ownership: every page here is HAND-CANONICAL

`index.html`, `overview.html`, `new-Items.html`, `changelog.html`,
`install.html`, and `dependencies.html` are edited by hand. Each carries this
marker right after its doctype:

    <!-- DO-NOT-REGENERATE: hand-canonical. See docs/OOO/OBR/CONTRIBUTING.md -->

**Do not regenerate these files over the marker.** The marker is enforced two ways:

- This repo's `pre-commit` hook (install once with `sh scripts/install-hooks.sh`)
  blocks any commit that stages one of these pages without the marker.
- The companion repo's `sync_pages.py` skips any file containing the marker when
  run with `--apply`.

## The regenerator is an ADVISOR, not a writer

In `OblivionRemastered_OOO`:

    python scripts/sync_pages.py            # DEFAULT: prints a diff, writes nothing
    python scripts/sync_pages.py --apply    # writes ONLY unmarked files; skips marked ones

When a new release lands, run the default (diff) form, read what changed
upstream (e.g. a new release row for `index.html`'s all-releases list, or a new
per-release changelog section), and **hand-merge** the parts you want into these
pages. The marker stays.

## If you genuinely want a page to be machine-owned again

Remove its marker, move its content into the OOO repo's Markdown sources, and
let `--apply` own it. Until then, assume hand-canonical.
```

- [ ] **Step 2: Verify it commits cleanly through the new hook**

The hook only checks `*.html`, so a `.md` commit is unaffected.

Run: `git add docs/OOO/OBR/CONTRIBUTING.md && git commit -m "docs(OBR): contributor contract for hand-canonical pages (R2, R8)"`
Expected: commit succeeds.

---

## Part 3 — Final verification & push

- [ ] **Step 1: OOO repo — full suite green**

Run (from `x:\dev\OblivionRemastered_OOO`): `python -m pytest -v`
Expected: all tests PASS.

- [ ] **Step 2: OOO repo — advisor is non-destructive against the live pages**

Run: `python scripts/sync_pages.py --apply`
Expected: every OBR page logs `SKIP ... (DO-NOT-REGENERATE marker present)`.
Then run: `git -C x:/dev/devnull status --short docs/OOO/OBR/`
Expected: **no** modified OBR files.

- [ ] **Step 3: devnull repo — full suite green + hook live**

Run (from `x:\dev\devnull`): `python -m pytest -v`
Expected: all tests PASS. Confirm `.git/hooks/pre-commit` exists and is executable.

- [ ] **Step 4: Push both repos**

```bash
git -C x:/dev/devnull push origin main
git -C x:/dev/OblivionRemastered_OOO push origin main   # confirm branch/remote first
```
Expected: both push cleanly. (Confirm the OOO repo's current branch and remote before pushing; do not force.)

---

## Spec coverage check (plan vs requirements R1–R8)

- **R1** (restore rich content) — DONE in the prior session (commit `5a884ee`); not re-done here.
- **R2** (documented source-of-truth per file) — Task 8 CONTRIBUTING.md.
- **R3** (block accidental overwrite) — Tasks 4 (sync_pages skip), 6 (markers), 7 (pre-commit hook).
- **R4** (converter bugs: tables, code fences, links) — Task 2.
- **R5** (re-link new-Items + images) — DONE in `5a884ee` (restored `cd650fa` links); marker added in Task 6.
- **R6** (size figure) — DONE in `5a884ee` (215.9 MiB verified from the 226 MB `.7z`).
- **R7** (phase9-unify-tracker re-ingestion) — OUT OF SCOPE here; restored 15/17 table retained. Follow-up only if the MapClone number changed. Flagged in the design doc.
- **R8** (document the workflow) — Task 8 CONTRIBUTING.md; nav/branding fixes in Task 3 keep advisory diffs low-noise.

## Notes for the executor

- The two repos are independent; Part 1 and Part 2 can be done in either order, but run Part 3 Step 2 only after **both** Task 4 (skip logic) and Task 6 (markers) exist.
- Windows line endings: the marker inserter preserves the file's existing newline style; do not "fix" CRLF/LF — git already warns and normalizes.
- No `Co-Authored-By` / "Generated with Claude" trailers in any commit (both repos' CLAUDE.md forbid it; a `commit-msg` hook strips them as backstop).
```
