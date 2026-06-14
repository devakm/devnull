# OOORF Devlog Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a hand-canonical `docs/OOO/OBR/devlog.html` developer-diary page whose first entry is an alpha91 "making-of" retrospective — arc cards anchor-jumping into a complete dated milestone spine drawn from the ItemClone/MapClone handoff reports.

**Architecture:** A single growing HTML page in the existing OBR site style (shared CSS + an inline `<style>` block for devlog components, like `new-Items.html`). Content is drafted to a reviewable Markdown file first (human review gate), then rendered to HTML by hand. A small Python anchor-integrity checker (pure core + unit tests) guards that every arc card resolves to a real milestone `id`. The page inherits the existing guard-rails (DO-NOT-REGENERATE marker → pre-commit guard + `sync_pages.py` skip).

**Tech Stack:** HTML5, CSS (the site's dark-theme custom properties), Python 3.12 stdlib (`re`), pytest. No build step; the page is static and hand-authored.

**Repo:** `x:\dev\devnull` (git, branch `main`). Commit directly on `main`; pushing is the user's call. All paths below are relative to the repo root unless absolute.

---

## File Structure

- **Create** `docs/OOO/OBR/devlog.html` — the page (marker, shared shell, inline CSS, intro, six arc cards, alpha91 milestone spine).
- **Create** `scripts/check_devlog_anchors.py` — pure `unresolved_anchors(html)` + thin CLI; verifies every internal `#...` arc-card link has a matching `id`/`name`, and the marker is present.
- **Create** `tests/test_check_devlog_anchors.py` — unit tests for the pure core.
- **Create** `notes/devlog-alpha91-draft.md` — the reviewable prose draft (arcs + dated spine). Review gate before markup. (In `notes/`, not published.)
- **Modify** `docs/OOO/OBR/{index,overview,new-Items,changelog,install,dependencies}.html` — insert a `Devlog` nav link.
- **Modify** `docs/OOO/OBR/index.html` (Quick links) and `docs/OOO/OBR/overview.html` (body) — link to the devlog.
- **Modify** `docs/OOO/OBR/CONTRIBUTING.md` — list `devlog.html` among the hand-canonical pages.

**CSS custom properties** used by the inline block (confirmed present in `docs/css/devnull-shared.css` via the `overview.html` gallery: `--accent-cyan`, `--border-color`, `--bg-tertiary`): also uses `--bg-primary`, `--text-secondary`. Step 1 of Task 3 verifies these exist; if any is missing, substitute the nearest defined variable rather than inventing one.

---

## Phase 1 — Content draft (review gate)

### Task 1: Draft the alpha91 devlog content to a reviewable Markdown file

**Files:**
- Create: `notes/devlog-alpha91-draft.md`

This is a research-and-writing task. Dispatch a capable model. It produces prose only — no HTML, no code.

- [ ] **Step 1: Read the source handoffs and ground-truth docs**

Read (translate, do not quote raw):
- ItemClone (`X:/dev/OblivionRemastered_ItemClone/docs/`): `handoff-2026-06-10-fur-sets-built.md`, `handoff-2026-06-12-recolor-completeness-glass-rename.md`, `handoff-2026-06-12-ingame-fixes-and-icon-glow.md`, `handoff-2026-06-13-icon-pfunknown-fur-resolved.md`, `handoff-2026-06-13-gnd-preview-ctd-bisect.md`, `handoff-2026-06-04-mithril-eboron.md`, `handoff-2026-06-04-shadowmail.md`, `handoff-2026-06-05-leather-diffuse-continuity-zones.md`, `handoff-2026-06-07-gnd-orientation-and-aureus.md`, `icon-texture-PF_DXT5.md`, and the other `handoff-2026-06-*` files for set-by-set dates.
- MapClone (`X:/dev/OblivionRemastered_MapClone/docs/`): `phase3-water-handoff-2026-06-01.md` (the fire saga), the `phase3-water-handoff-2026-05-2*.md` series (water), `phase9-unify-handoff-2026-05-1*.md` (flicker/suppression), `phase9-flickering-fix-TES4.md`, and `phase9-unify-tracker.md` (the per-dungeon ✓ dates — authoritative).
- Ground truth for figures: `X:/dev/OblivionRemastered_OOO/docs/per-release/alpha91.md` and this repo's `docs/OOO/OBR/changelog.html` (the `alpha91` section) + `overview.html` alpha91 callout.

- [ ] **Step 2: Write `notes/devlog-alpha91-draft.md` with this exact structure**

```markdown
# alpha91 devlog draft (for review)

## Intro
<one short paragraph: alpha91 = the armor wave + water/fire/flicker solved>

## Arc cards (6)
Each: **Title** | target id | 1-2 sentence teaser.
- Taming water | a91-water | <teaser>
- Fire: 15 tries to a bonfire | a91-fire | <teaser>
- Flicker & ghost suppression | a91-flicker | <teaser>
- Icons & GND meshes | a91-icons | <teaser>
- The recolor pipeline (fur is a baked color) | a91-recolor | <teaser>
- The 14-set armor wave | a91-armor | <teaser>

## Chronological spine (milestones, oldest->newest within alpha91)
For each milestone: `DATE | id (only if an arc target) | title | body`.
- Cover EVERY dungeon validation (dates from phase9-unify-tracker.md) and EVERY shipped item set (dates from ItemClone handoffs).
- Expand the six breakthrough moments inline (these carry the arc `id`s).
- Note the long debugging gaps explicitly where they occur (e.g. the ~8-day water-debug run before fire rendered 2026-06-01).
- Mark which armor-wave milestones should show a reused thumbnail (set name -> existing PNG in docs/OOO/OBR/images/item-tracker-assets/).
```

**Translation rules (mandatory):** no raw EDIDs, FormID hex, or commit hashes in the prose. Keep accessible engineering color (e.g. "fur color is a 16-byte value baked into the material, not a texture"). Figures (counts like 14 sets, +254 disabled REFRs, ~307 SyncMap rebindings, 15/17 dungeons) MUST match `alpha91.md` / `changelog.html#alpha91`; if a handoff and the release doc disagree, prefer the release doc and flag the discrepancy in a `> NOTE:` line.

- [ ] **Step 3: Self-check the draft**

Confirm: all six arcs have a target id; every arc id appears exactly once as a milestone in the spine; every alpha91 dungeon (17) and every shipped set (14) is represented; no raw IDs/hashes; figures cross-checked. Add a short `## Fact-check notes` section listing any discrepancies found.

- [ ] **Step 4: Commit the draft**

```bash
git add notes/devlog-alpha91-draft.md
git commit -m "notes: alpha91 devlog prose draft for review"
```

**REVIEW GATE:** The controller surfaces the draft to the user for review/edits before Phase 3 markup. Apply requested edits and re-commit before proceeding. (Phase 2 tooling can proceed in parallel; it does not depend on the draft.)

---

## Phase 2 — Anchor-integrity checker (TDD)

### Task 2: `check_devlog_anchors.py` + tests

**Files:**
- Create: `scripts/check_devlog_anchors.py`
- Create: `tests/test_check_devlog_anchors.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_check_devlog_anchors.py`:

```python
import importlib.util
from pathlib import Path

_MODULE_PATH = Path(__file__).resolve().parent.parent / "scripts" / "check_devlog_anchors.py"
_spec = importlib.util.spec_from_file_location("check_devlog_anchors", _MODULE_PATH)
chk = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(chk)


def test_all_anchors_resolve():
    html = '<a class="arc-card" href="#a91-water">x</a><div id="a91-water"></div>'
    assert chk.unresolved_anchors(html) == []


def test_missing_target_is_flagged():
    html = '<a class="arc-card" href="#a91-fire">x</a><div id="a91-water"></div>'
    assert chk.unresolved_anchors(html) == ["a91-fire"]


def test_external_and_plain_links_ignored():
    html = '<a href="changelog.html#alpha91">c</a><a href="https://x.test#frag">e</a>'
    # Only same-page #fragment links are checked; these have a path/host, so ignored.
    assert chk.unresolved_anchors(html) == []


def test_name_attribute_also_satisfies_target():
    html = '<a href="#top">t</a><a name="top"></a>'
    assert chk.unresolved_anchors(html) == []


def test_marker_present_detection():
    assert chk.has_marker("<!-- DO-NOT-REGENERATE: x -->") is True
    assert chk.has_marker("<html>") is False
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_check_devlog_anchors.py -v`
Expected: FAIL (module does not exist). Install pytest first if needed: `python -m pip install pytest`.

- [ ] **Step 3: Create `scripts/check_devlog_anchors.py`**

```python
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
```

- [ ] **Step 4: Run to verify the tests pass**

Run: `python -m pytest tests/test_check_devlog_anchors.py -v`
Expected: all 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/check_devlog_anchors.py tests/test_check_devlog_anchors.py
git commit -m "feat: devlog anchor-integrity + marker checker"
```

---

## Phase 3 — Build the page

### Task 3: Create `devlog.html` scaffold (marker, shell, inline CSS, empty alpha91 section)

**Files:**
- Create: `docs/OOO/OBR/devlog.html`

- [ ] **Step 1: Confirm CSS variables exist**

Run: `grep -oE '\-\-(accent-cyan|border-color|bg-tertiary|bg-primary|text-secondary)' docs/css/devnull-shared.css | sort -u`
Expected: all five names appear. If one is missing, note its nearest substitute (e.g. `--accent-blue` for `--accent-cyan`) and use that consistently in Step 2's CSS.

- [ ] **Step 2: Write the scaffold**

Create `docs/OOO/OBR/devlog.html` with EXACTLY this content (the alpha91 section body is filled in Tasks 4–5):

```html
<!DOCTYPE html>
<!-- DO-NOT-REGENERATE: hand-canonical. See docs/OOO/OBR/CONTRIBUTING.md -->
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OOORF — Devlog</title>
  <link rel="stylesheet" href="../../css/devnull-shared.css">
  <style>
    .devlog-arcs {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 14px;
      margin: 20px 0 32px;
    }
    .arc-card {
      display: block;
      padding: 14px 16px;
      background: var(--bg-tertiary);
      border: 1px solid var(--border-color);
      border-left: 3px solid var(--accent-cyan);
      border-radius: 6px;
      text-decoration: none;
      color: inherit;
      transition: transform 0.15s, border-color 0.15s;
    }
    .arc-card:hover { transform: translateY(-2px); border-color: var(--accent-cyan); }
    .arc-card h4 { margin: 0 0 6px; color: var(--accent-cyan); font-size: 1.02em; }
    .arc-card p { margin: 0; color: var(--text-secondary); font-size: 0.92em; }
    .arc-card .jump { display: inline-block; margin-top: 8px; font-size: 0.85em; color: var(--accent-cyan); }

    .devlog-timeline { border-left: 2px solid var(--border-color); margin: 24px 0; padding-left: 0; }
    .milestone {
      position: relative;
      margin: 0 0 26px;
      padding: 0 0 0 22px;
      scroll-margin-top: 16px;
    }
    .milestone::before {
      content: ""; position: absolute; left: -7px; top: 6px;
      width: 10px; height: 10px; border-radius: 50%;
      background: var(--bg-primary); border: 2px solid var(--accent-cyan);
    }
    .milestone .date { font-weight: bold; color: var(--accent-cyan); font-size: 0.9em; letter-spacing: 0.02em; }
    .milestone h3 { margin: 2px 0 8px; font-size: 1.1em; }
    .milestone.gap-note { color: var(--text-secondary); font-style: italic; }

    .devlog-thumbs { display: flex; flex-wrap: wrap; gap: 10px; margin: 12px 0; }
    .devlog-thumbs a { display: block; }
    .devlog-thumbs img { height: 110px; border: 1px solid var(--border-color); border-radius: 4px; object-fit: cover; }

    .progress-strip { display: flex; flex-wrap: wrap; gap: 8px; margin: 12px 0; }
    .progress-strip img { height: 90px; border: 1px solid var(--border-color); border-radius: 4px; }

    figure.shot { margin: 14px 0; }
    figure.shot img { max-width: 100%; border: 1px solid var(--border-color); border-radius: 6px; }
    figure.shot figcaption { color: var(--text-secondary); font-size: 0.88em; margin-top: 6px; }
  </style>
</head>

<body>
  <div class="container">
    <header>
      <h1>Oscuro's Oblivion Overhaul Remastered FULL (OOORF)</h1>
      <p class="subtitle">Release Tracker</p>
    </header>
    <nav><a href="index.html">Home</a> | <a href="overview.html">Overview</a> | <a href="new-Items.html">New Items</a> | <a href="devlog.html" class="highlight-text">Devlog</a> | <a href="changelog.html">Changelog</a> | <a href="install.html">Install</a> | <a href="dependencies.html">Dependencies</a> | <a href="https://github.com/devakm/OblivionRemastered_OOO/releases" target="_blank" rel="noopener">Downloads (GitHub Releases)</a></nav>

    <h1>Devlog — the story behind each release</h1>
    <p>Curated "making-of" notes drawn from the build logs of the item and map projects behind OOORF. For the dry file-level list, see the <a href="changelog.html">changelog</a>; for the new armor sets, the <a href="new-Items.html">New Items</a> page.</p>

    <section id="alpha91">
      <h2>alpha91 — June 2026</h2>
      <!-- INTRO (Task 4) -->
      <!-- ARC CARDS (Task 4) -->
      <!-- CHRONOLOGICAL SPINE (Task 5) -->
    </section>

    <footer>
      <p>Source: <a href="https://github.com/devakm/OblivionRemastered_OOO" target="_blank" rel="noopener">github.com/devakm/OblivionRemastered_OOO</a> · Releases: <a href="https://github.com/devakm/OblivionRemastered_OOO/releases" target="_blank" rel="noopener">GitHub Releases</a></p>
    </footer>
  </div>
</body>

</html>
```

- [ ] **Step 3: Verify marker + structure**

Run: `python scripts/check_devlog_anchors.py docs/OOO/OBR/devlog.html`
Expected: `OK: anchors resolve and marker present` (no arc links yet, so trivially OK; marker present).

- [ ] **Step 4: Commit**

```bash
git add docs/OOO/OBR/devlog.html
git commit -m "OOO/OBR: devlog.html scaffold (marker, shell, components, empty alpha91 section)"
```

### Task 4: Intro + six arc cards (from the approved draft)

**Files:**
- Modify: `docs/OOO/OBR/devlog.html` (replace the `<!-- INTRO -->` and `<!-- ARC CARDS -->` comments)

- [ ] **Step 1: Insert the intro paragraph and arc-card grid**

Use the approved `notes/devlog-alpha91-draft.md`. Replace the `<!-- INTRO (Task 4) -->` line with the intro `<p>...</p>`, and the `<!-- ARC CARDS (Task 4) -->` line with this grid, filling each card's teaser from the draft. The six `href` values MUST be exactly the ids Task 5 creates:

```html
      <div class="devlog-arcs">
        <a class="arc-card" href="#a91-water"><h4>Taming water</h4><p>TEASER</p><span class="jump">Jump to the story ↓</span></a>
        <a class="arc-card" href="#a91-fire"><h4>Fire: 15 tries to a bonfire</h4><p>TEASER</p><span class="jump">Jump to the story ↓</span></a>
        <a class="arc-card" href="#a91-flicker"><h4>Flicker &amp; ghost suppression</h4><p>TEASER</p><span class="jump">Jump to the story ↓</span></a>
        <a class="arc-card" href="#a91-icons"><h4>Icons &amp; GND meshes</h4><p>TEASER</p><span class="jump">Jump to the story ↓</span></a>
        <a class="arc-card" href="#a91-recolor"><h4>The recolor pipeline</h4><p>TEASER</p><span class="jump">Jump to the story ↓</span></a>
        <a class="arc-card" href="#a91-armor"><h4>The 14-set armor wave</h4><p>TEASER</p><span class="jump">Jump to the story ↓</span></a>
      </div>
```

Replace each `TEASER` with the 1–2 sentence teaser from the draft (escape `&`, `<`, `>` as HTML entities).

- [ ] **Step 2: Commit**

```bash
git add docs/OOO/OBR/devlog.html
git commit -m "OOO/OBR: devlog alpha91 intro + arc cards"
```

### Task 5: Chronological spine (from the approved draft)

**Files:**
- Modify: `docs/OOO/OBR/devlog.html` (replace the `<!-- CHRONOLOGICAL SPINE -->` comment)

- [ ] **Step 1: Build the milestone timeline**

Replace `<!-- CHRONOLOGICAL SPINE (Task 5) -->` with a `<div class="devlog-timeline">` containing one `.milestone` per spine entry from the draft, oldest→newest. Each milestone follows this template (omit `id` on non-arc milestones):

```html
        <div class="milestone" id="a91-water">
          <div class="date">2026-05-26</div>
          <h3>MILESTONE TITLE</h3>
          <p>MILESTONE BODY (translated prose; no raw EDIDs/hashes).</p>
        </div>
```

Rules:
- The six arc-target milestones carry `id="a91-water|fire|flicker|icons|recolor|armor"` — each id exactly once.
- Include every alpha91 dungeon validation (dates from `phase9-unify-tracker.md`) and every shipped item set (dates from the ItemClone handoffs).
- For armor-wave milestones the draft tagged with a thumbnail, add a `devlog-thumbs` block linking to the matching `new-Items.html` anchor, e.g.:
  ```html
          <div class="devlog-thumbs"><a href="new-Items.html#ArcticFur"><img src="images/item-tracker-assets/ArcticFur_Cuirass.png" alt="Arctic Fur cuirass"></a></div>
  ```
  (Use only filenames that exist in `docs/OOO/OBR/images/item-tracker-assets/` — verify with `ls` before referencing.)
- Where the draft notes a debugging gap, add a short `<p class="milestone gap-note">` line describing it (e.g. the ~8 days of water work before fire rendered).

- [ ] **Step 2: Verify anchors resolve**

Run: `python scripts/check_devlog_anchors.py docs/OOO/OBR/devlog.html`
Expected: `OK: anchors resolve and marker present`. If it lists unresolved anchors, fix the mismatched id/href until clean.

- [ ] **Step 3: Verify referenced images exist**

Run:
```bash
grep -oE 'images/item-tracker-assets/[A-Za-z0-9_]+\.png' docs/OOO/OBR/devlog.html | sort -u | while read p; do test -f "docs/OOO/OBR/$p" && echo "ok $p" || echo "MISSING $p"; done
```
Expected: every line starts with `ok`. Fix any `MISSING` (wrong filename).

- [ ] **Step 4: Commit**

```bash
git add docs/OOO/OBR/devlog.html
git commit -m "OOO/OBR: devlog alpha91 chronological milestone spine"
```

---

## Phase 4 — Integration

### Task 6: Add the `Devlog` nav link to the other six pages

**Files:**
- Modify: `docs/OOO/OBR/{index,overview,new-Items,changelog,install,dependencies}.html`

- [ ] **Step 1: Insert the nav link idempotently**

Each page's `<nav>` contains `<a href="changelog.html"...>Changelog</a>`. Insert a plain Devlog link immediately before it. Run from `x:/dev/devnull` (Git Bash):

```bash
cd x:/dev/devnull
for f in index overview new-Items changelog install dependencies; do
  p="docs/OOO/OBR/$f.html"
  python - "$p" <<'PY'
import io, sys, re
path = sys.argv[1]
t = io.open(path, encoding="utf-8").read()
if 'href="devlog.html"' in t:
    print("already has devlog nav:", path); sys.exit(0)
# Insert the Devlog link right before the Changelog nav link.
new = re.sub(r'(<a href="changelog\.html")', '<a href="devlog.html">Devlog</a> | \\1', t, count=1)
assert new != t, f"no changelog nav link found in {path}"
io.open(path, "w", encoding="utf-8", newline="").write(new)
print("added devlog nav:", path)
PY
done
```

- [ ] **Step 2: Verify all seven pages have the Devlog link exactly once**

Run: `grep -c 'href="devlog.html"' docs/OOO/OBR/{index,overview,new-Items,changelog,install,dependencies,devlog}.html`
Expected: `index`/`overview`/`new-Items`/`changelog`/`install`/`dependencies` each report `1`; `devlog.html` reports `1` (its own nav active link). If any existing page reports more than 1, revert that file and re-run for it only.

- [ ] **Step 3: Confirm only the nav line changed**

Run: `git diff --stat docs/OOO/OBR/`
Expected: six files, each `1 insertion(+), 1 deletion(-)` (the single nav line rewritten). If any file shows more, inspect and fix.

- [ ] **Step 4: Commit**

```bash
git add docs/OOO/OBR/index.html docs/OOO/OBR/overview.html docs/OOO/OBR/new-Items.html docs/OOO/OBR/changelog.html docs/OOO/OBR/install.html docs/OOO/OBR/dependencies.html
git commit -m "OOO/OBR: add Devlog to nav across pages"
```

### Task 7: Body cross-links from index + overview

**Files:**
- Modify: `docs/OOO/OBR/index.html` (Quick links list)
- Modify: `docs/OOO/OBR/overview.html` (a relevant spot, e.g. near the alpha91 callout)

- [ ] **Step 1: Add a Quick links entry in `index.html`**

Find the `<h2>Quick links</h2>` `<ul>` and add, as a new `<li>` (keep the existing list style):

```html
      <li><a href="devlog.html">Devlog</a> — the making-of story behind each release</li>
```

- [ ] **Step 2: Add a link in `overview.html`**

In the alpha91 area of `overview.html`, add a sentence linking the devlog, e.g. immediately after the "What's new in alpha91" intro paragraph:

```html
    <p>Want the story behind these changes? See the <a href="devlog.html">devlog</a>.</p>
```

- [ ] **Step 3: Verify the marker guard still passes for both**

Run: `python scripts/check_obr_markers.py < /dev/null; git add docs/OOO/OBR/index.html docs/OOO/OBR/overview.html`
Then attempt the commit in Step 4 (the pre-commit hook runs `check_obr_markers.py` on staged OBR html; both still carry the marker, so it passes).

- [ ] **Step 4: Commit**

```bash
git commit -m "OOO/OBR: link the devlog from index Quick links and overview"
```

### Task 8: Note `devlog.html` in CONTRIBUTING.md

**Files:**
- Modify: `docs/OOO/OBR/CONTRIBUTING.md`

- [ ] **Step 1: Add devlog.html to the hand-canonical list**

In the "Ownership: every page here is HAND-CANONICAL" section, update the sentence that lists the pages so it includes `devlog.html`. Change the list of filenames to read:

```markdown
`index.html`, `overview.html`, `new-Items.html`, `devlog.html`, `changelog.html`,
`install.html`, and `dependencies.html` are edited by hand. Each carries this
```

- [ ] **Step 2: Commit**

```bash
git add docs/OOO/OBR/CONTRIBUTING.md
git commit -m "docs(OBR): list devlog.html as hand-canonical"
```

---

## Phase 5 — Final verification

### Task 9: Whole-page verification

- [ ] **Step 1: Anchor + marker check**

Run: `python scripts/check_devlog_anchors.py docs/OOO/OBR/devlog.html`
Expected: `OK: anchors resolve and marker present`.

- [ ] **Step 2: Full test suite**

Run: `python -m pytest -q`
Expected: all tests pass (the new anchor tests + the existing marker-check tests).

- [ ] **Step 3: External-link attribute check on devlog.html**

Run: `grep -oE '<a href="https://[^"]+"[^>]*>' docs/OOO/OBR/devlog.html | grep -v 'rel="noopener"' || echo "all external links carry rel=noopener"`
Expected: `all external links carry rel=noopener`.

- [ ] **Step 4: Coverage sanity (every set + dungeon present)**

Run: `python scripts/check_devlog_anchors.py docs/OOO/OBR/devlog.html && grep -c 'class="milestone"' docs/OOO/OBR/devlog.html`
Expected: OK, and the milestone count is at least 17 (dungeons) + 14 (sets) minus any deliberately merged entries — i.e. a high-twenties/thirties count. If it is far lower, the spine is incomplete; revisit Task 5 against the draft.

- [ ] **Step 5: Marker guard dry-run (hook parity)**

Run: `git add -A && python scripts/check_obr_markers.py; echo "exit=$?"`
Expected: `exit=0` (every staged OBR html, including devlog.html, carries the marker).

- [ ] **Step 6: Report**

Summarize: files created/modified, milestone count, any fact-check notes carried from the draft, and confirm the pre-commit hook passed on the content commits. Pushing is the user's decision (hold unless told otherwise).

---

## Self-review (plan vs spec)

- **Spec A (page & placement):** Tasks 3 (scaffold+marker+shell+CSS), 6 (nav), 7 (cross-links), 8 (CONTRIBUTING). ✓
- **Spec B (arcs → spine layout):** Tasks 4 (intro+arcs), 5 (spine), with anchor integrity enforced by Task 2's checker. ✓
- **Spec C (arc sources):** Task 1 Step 1 enumerates the exact handoff/tracker sources. ✓
- **Spec D (imagery incremental):** Task 3 CSS defines `.devlog-thumbs`/`.progress-strip`/`figure.shot`; Task 5 uses existing thumbnails; strips/shots render cleanly while empty. ✓
- **Spec E (CSS components):** Task 3 Step 2 contains the full inline `<style>`. ✓
- **Spec F (build scope):** Phases 3–4 build text + thumbnails + nav + links; progress strips/dungeon shots deferred (slots only). ✓
- **Spec G (guard-rails inherited):** marker in Task 3; Tasks 7/9 confirm the existing hook passes; no new guard-rail work. ✓
- **Acceptance criteria 1–6:** 1→Tasks 3/9; 2→Tasks 2/5; 3→Tasks 1/5/9 Step 4; 4→Task 1 translation rules + Step 3; 5→Tasks 6/7/9 Step 3; 6→Tasks 3/5. ✓

**Type/name consistency:** the six anchor ids (`a91-water|fire|flicker|icons|recolor|armor`) are identical in Task 4 (hrefs) and Task 5 (ids); the checker function `unresolved_anchors`/`has_marker` names match between Task 2's code and tests; image path prefix `images/item-tracker-assets/` matches the restored `overview.html` gallery convention.

## Notes for the executor

- Commit on `main`; do not push unless the user says so.
- No `Co-Authored-By` / "Generated with Claude Code" trailers (repo CLAUDE.md; commit-msg hook strips as backstop).
- The pre-commit hook (`scripts/check_obr_markers.py`) runs on every commit that stages `docs/OOO/OBR/*.html`; keep the marker intact in `devlog.html` and the edited pages.
- Windows line endings: git will warn LF→CRLF; do not fight it.
- Phase 2 (checker) is independent of the Phase 1 draft and can be built first; Phase 3 markup needs the *approved* draft.
