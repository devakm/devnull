# OOORF page regeneration conflict — design / spec

**Status:** Approved design (2026-06-14). Companion to
[`OOORF-page-regen-resolution-requirements.md`](OOORF-page-regen-resolution-requirements.md),
which defines the requirements (R1–R8). This document is the agreed solution and
drives the implementation plan.

**Repos in scope:**
- `X:\dev\devnull` (this repo — the GitHub Pages site, served from `docs/`)
- `X:\dev\OblivionRemastered_OOO` (companion repo — owns `scripts/sync_pages.py` and the Markdown sources)

## Problem (one paragraph)

Rich, hand-authored content under `docs/OOO/OBR/` (galleries, validation tables,
two-table dependency splits, OOORF naming, curated changelog) was overwritten by
`scripts/sync_pages.py` from the OOO repo, which mechanically converts Markdown to
HTML and **always blasts all five pages** with no change-detection, a converter that
can't render tables or code fences, wrong naming/nav, and no knowledge of
`new-Items.html`. The hand work from commit `cd650fa` was clobbered by regen commit
`b945ff2` (refined by `755a46e`). A backup branch `backup/regen-alpha91-20260614`
preserves the regen state.

## Decisions (locked with the user)

1. **Changelog:** the curated `cd650fa` version (3,499 lines) is canonical. The regen's
   17,951-line version is discarded except for the terminology correction it carried.
2. **Ownership model:** hybrid, resolved to **all OBR pages hand-canonical**. No page is
   auto-written by `sync_pages.py`.
3. **`sync_pages.py` role flips** from *writer* to *advisor*: by default it emits a
   reviewable diff of what upstream changed; it never silently overwrites a hand page.
4. **Both repos** are changed this session.

## Part A — Content restore (devnull repo)

Restore each file's `cd650fa` state, then re-apply the corrections the regen legitimately
introduced (so neither side's good work is lost).

| File | Source | Corrections to graft |
|---|---|---|
| `overview.html` | `cd650fa` | bump `alpha90`→`alpha91` in the "compare two releases" `<pre><code>` block (the uncommitted working-tree edit); terminology rename (below) |
| `dependencies.html` | `cd650fa` | — |
| `install.html` | `cd650fa` | — |
| `index.html` | `cd650fa` | — (carries the correct `215.9 MiB` figure, OOORF naming, New-Items nav, acronym note) |
| `changelog.html` | `cd650fa` | terminology rename (below) |
| `new-Items.html` | keep current (intact) | re-linked automatically once `overview`/`index`/nav are restored from `cd650fa` |
| `.vscode/settings.json` | keep working-tree edit | the `oneline` cspell addition |

**Terminology rename** (source of truth = OOO repo `docs/per-release/alpha91.md`, already
corrected in commits `72a85da` / `ce68ed7`):
- `UE5-layer suppression` → `TES4 REFR suppression`
- `Ghost suppression (Begone)` → `UE5-layer ghost suppression (Begone)`

**Size figure (R6) — resolved:** `alpha91.7z` on disk is 226,395,498 bytes = **215.9 MiB**
(the download). The regen's "824.7 MiB" is the manifest sum (uncompressed install
footprint). The hand figure `215.9 MiB` is user-facing-correct; restoring `cd650fa` fixes it.

This satisfies R1, R5, R6.

## Part B — Ownership model

**All five generated pages + `new-Items.html` are hand-canonical.** `sync_pages.py` writes
none of them. The auto-growing all-releases list on `index.html` is maintained by
hand-merging from the advisor diff (a single new `<li>` row per release).

## Part C — Guard-rails (defense-in-depth; satisfies R3)

1. **Markers in HTML.** Every hand-canonical page carries, right after `<!DOCTYPE html>`:
   `<!-- DO-NOT-REGENERATE: hand-canonical. See docs/OOO/OBR/CONTRIBUTING.md -->`
2. **`sync_pages.py` rework** (OOO repo):
   - **Default mode = diff/advisory.** Prints a unified diff of each generated page vs the
     destination file; **writes nothing**.
   - `--apply` writes **only** destination files that do *not* contain the
     `DO-NOT-REGENERATE` marker. Under the current model that is zero existing OBR files,
     so `--apply` is a safe no-op for them and only ever creates genuinely new pages.
   - Refuses to overwrite a marked file even with `--apply`; logs each skip loudly.
   - **Converter bug fixes (R4):** real `<table>` from `| col | col |`; `<pre><code>` from
     fenced code blocks; `target="_blank" rel="noopener"` on external (`https://`) links.
   - Naming/nav fixes in `page_shell` so advisory diffs are low-noise: OOORF naming, nav
     order `Home | Overview | New Items | Changelog | Install | Dependencies | Downloads`,
     New-Items link.
3. **Precommit check** (devnull repo): a `pre-commit` hook fails the commit if any file under
   `docs/OOO/OBR/*.html` is staged without its `DO-NOT-REGENERATE` marker. Catches a clobber
   even if someone runs a stale `sync_pages.py` and tries to commit the result.

## Part D — Workflow doc + cross-repo

- **`docs/OOO/OBR/CONTRIBUTING.md`** (devnull): documents the split, the marker contract, and
  the `sync_pages.py` diff-then-hand-merge review gate (R2, R8). This file lives under `docs/`
  and is published — keep it terse and contributor-facing.
- Apply the `sync_pages.py` rework + the converter fixes in the OOO repo this session.

## Out of scope / not restored (explicit, per R-doc acceptance criterion 1)

- The regen's 17,951-line changelog body is intentionally discarded (buggy formatting, no
  added curated value over `cd650fa`). Only its terminology correction is kept.
- `phase9-unify-tracker.md` re-ingestion (R7): the restored `cd650fa` validation table
  (15/17) is retained as-is; a fresh pull from the MapClone repo is deferred unless the
  number has changed. Flag for a follow-up if the user wants it re-verified.

## Acceptance criteria (from the requirements doc)

1. Every "What was lost" bullet is restored, or listed above as intentionally-not-restored.
2. Every substantive `b945ff2`/`755a46e` contribution (terminology) is preserved.
3. A future `sync_pages.py` run produces **zero** unwanted writes to OBR pages (default mode
   writes nothing; `--apply` skips marked files).
4. `CONTRIBUTING.md` tells the next contributor which side owns each file and what to do.
5. The converter's table/code-fence/link bugs are fixed.

## Key references

- Backup branch: `backup/regen-alpha91-20260614` (= old `main`, the regen state)
- Good commit: `cd650fa`; regen commits: `b945ff2`, `755a46e`
- Converter: `X:\dev\OblivionRemastered_OOO\scripts\sync_pages.py`
- Terminology source of truth: `X:\dev\OblivionRemastered_OOO\docs\per-release\alpha91.md`
