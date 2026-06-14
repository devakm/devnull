# OOORF page regeneration conflict — requirements definition

**Status:** Draft requirements for a future planning session. Not a plan itself.

**Trigger:** A regenerate-from-Markdown commit destroyed several turns' worth of hand-edits on the OOORF pages under [`docs/OOO/OBR/`](../docs/OOO/OBR/). The next session needs to (1) restore the lost work, (2) salvage anything genuinely new the regenerator contributed, and (3) prevent the two contributors from stepping on each other again.

## Background

The OOORF release-tracker site under [`docs/OOO/OBR/`](../docs/OOO/OBR/) has two contributors writing to the same HTML files:

1. **Hand edits in this repo.** Substantive content (rich item-set gallery, per-dungeon validation table, alpha91 narrative callouts, naming corrections, custom CSS, link reorganization) authored directly in the HTML files in `docs/OOO/OBR/`.
2. **Auto-regeneration from the companion repo.** A script in [`X:\dev\OblivionRemastered_OOO`](X:/dev/OblivionRemastered_OOO/) (see `scripts/sync_pages.py` plus the Markdown sources in `docs/*.md` and `docs/per-release/*.md`) converts those Markdown sources to HTML and writes the result over `docs/OOO/OBR/` in *this* repo.

Neither contributor knows about the other's existence. The Markdown converter has known formatting bugs (raw `<p>| col | col |</p>` rows where Markdown tables should have rendered; fenced code blocks splat into per-line `<p>` paragraphs; etc.) which the hand edits had cleaned up.

## The trigger event

Two adjacent commits on `main`:

| Commit  | Date                | Author          | Effect                                                                                                                                                |
| ------- | ------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `cd650fa` | 2026-06-14 02:36 -05 | Hand edit (this session) | "release alpha91 pages + new-Items page" — rich content (gallery, validation table, alpha91 callout, OOORF rename, etc.) plus 109 image files. |
| `b945ff2` | 2026-06-14 09:29 -05 | Regenerate from Markdown | "OOO/OBR: regenerate alpha91 pages — fix 'UE5-layer suppression' -> 'TES4 REFR suppression'" — overwrote five `docs/OOO/OBR/*.html` files, +17,155 / -3,010 lines. Most of `cd650fa`'s content disappeared. |

`new-Items.html` and the [`docs/OOO/OBR/images/`](../docs/OOO/OBR/images/) directory survived only because they are new files the regenerator didn't know about. They are now orphaned — nothing on the regenerated pages links to them.

## What was lost (audit against `cd650fa`)

Confirmed via `git show cd650fa:docs/OOO/OBR/overview.html` vs. the current working tree. Compiled list, not necessarily exhaustive — the next session should re-audit:

### `overview.html`
- "OOORF" name used throughout (current regen reverted to "OOORS Full" in title, h1, body, table column headings)
- OOORF-vs-OOORS-Slim disambiguation note with link to the Slim edition Nexus page
- "What's new in alpha91" callout (14 new item sets, BGlass→BlueGlass / RGlass→Drakefired renames, ~307 SyncMap rebindings, 7 dungeon paks rebuilt, GraveGroundExterior_P, +254 disabled REFRs / +17 position overrides / +92 Begone entries, +6 LairVileCrimsonScarRaiment ARMO records)
- "Previously: what was new in alpha90" history block preserved for future beta/GA rollup
- **Per-dungeon validation status table** (current state: 15 of 17 fully validated, with Gloom Way Cave and Red Gill Cave noted as ghost-suppression-only). Source of truth: `X:\dev\OblivionRemastered_MapClone\docs\phase9-unify-tracker.md`.
- **15-thumbnail item-set gallery** with `.item-gallery` grid CSS, `object-fit: cover` + `object-position: right center`, and per-card hover lift. Each cell links to the matching `#SetName` anchor in `new-Items.html`.
- Inline `<style>` block in `<head>` for the gallery
- "Custom cloned and retextured item sets" section with the categorized rundown of all 15 sets (Glass / Mithril / Elven / Leather / Fur families) and visual-source credits (SquigM, ProhagonCreations / Blackened Glass)
- Any link from `overview.html` to `new-Items.html`
- Updated "What is included in an OOORF release" framing (`alpha91 · 199 files · ~216 MiB`; the regen has alpha90/alpha91 mixed depending on which spot you read; index.html currently says 824.7 MiB which doesn't match either source)
- `Begone` repositioned as an alpha-testing utility (the regen has the old "removes specific actor/object references at runtime" description)

### `changelog.html`
- The full `alpha91` section with the curated Summary / Highlights / Added / Removed / Changed lists with file sizes pulled from `manifests/alpha91.json`. The regen's `alpha91` section (if present) should be diffed against `cd650fa`'s.

### `dependencies.html`
- Markdown-table-to-HTML-table conversion done by hand (regen leaves raw `<p>| Detail | Value |</p>` rows)
- Two-table split for UE4SS mods: required-for-normal-play (RAX) vs. alpha-testing-utilities (Begone, OOO_REFRFix) with the new Begone framing
- Nexus links on the optional-patches table with `target="_blank" rel="noopener"`

### `install.html`
- The `dependencies.md` → `dependencies.html` link fix
- Stray Markdown blockquote (`&gt;`) cleanup
- Naming updates (OOORF)

### `index.html`
- OOORF rename throughout
- New Items entry in the nav (overview now in second position)
- Item-tracker-aware Quick links entry
- Acronym disambiguation note with link to the OOORS-Slim Nexus page
- Correct alpha91 size (`215.9 MiB` per the dist archive on disk; the current regenerated index shows `824.7 MiB` which is suspicious — needs verification)
- 89-release count and alpha91 at the top of the all-releases list (some of this may have survived)

### Cross-page
- Nav order: `Home | Overview | New Items | Changelog | Install | Dependencies | Downloads` (regen reverted to `Home | Changelog | Install | Dependencies | Overview | Downloads`)
- External `https://` links uniformly carry `target="_blank" rel="noopener"` (regen drops the attributes — large-scale regression)
- cspell allowlist additions in [`.vscode/settings.json`](../.vscode/settings.json) — survived (not in the regen commit's scope)

## What the regenerator may have contributed that we should salvage

`b945ff2`'s message says "fix 'UE5-layer suppression' -> 'TES4 REFR suppression'" — that rename is a substantive correction we should keep. The next session should:

- Diff `git show cd650fa:docs/OOO/OBR/changelog.html` against the current file to find every place where the regen actually carries useful new content (terminology corrections, file-list updates, new per-release sections).
- The Markdown sources in [`X:\dev\OblivionRemastered_OOO\docs\`](X:/dev/OblivionRemastered_OOO/docs/) may have other recent edits worth grafting.

## Requirements

R1. **Restore the rich content from `cd650fa`** on top of the current `main`, preserving any substantive corrections introduced by `b945ff2` (notably the suppression-terminology rename). Approaches to consider:
   - Cherry-pick `cd650fa`'s file states onto a new commit and re-apply the deltas the regen carried.
   - Or pure manual re-write of the affected files using `cd650fa` as the template and the current regen as the new-content source.

R2. **Establish a documented source-of-truth per file.** For each file under `docs/OOO/OBR/`, the next session should record: who owns the canonical version (this repo / the OOO repo / hybrid), what content lives where, and how a new contributor (human or AI) can tell which is which without grep-archaeology.

R3. **Block accidental overwrite.** Whichever ownership model wins, the loser must be guard-railed:
   - If the regenerator owns these files: hand edits in this repo must produce a visible conflict / fail a precommit hook, not silently regenerate over them. Or: hand edits move into the Markdown sources (raw HTML inside Markdown is allowed by most converters).
   - If hand edits own these files: `sync_pages.py` in the OOO repo must skip them, or only run on a "bootstrap" subset, or run into an unmerged branch the human reviews.
   - Hybrid (likely best for this site): rich pages (`overview.html`, `new-Items.html`) are hand-canonical; mechanical pages (`changelog.html`, `index.html` release list) are regen-canonical from the Markdown + manifests in the OOO repo. The split must be encoded somewhere the regenerator reads (a manifest, an `.editorconfig`-style include/exclude file, or `<!-- DO-NOT-REGENERATE -->` markers it honors).

R4. **Fix the converter's known bugs** (whoever owns `sync_pages.py` in the OOO repo). At minimum:
   - Markdown tables (`| col | col |`) must produce real `<table>` not per-line `<p>`.
   - Fenced code blocks must produce `<pre><code>` not per-line `<p>`.
   - External links must carry `target="_blank" rel="noopener"` (this site's standard).

R5. **Re-link `new-Items.html` and its [`images/`](../docs/OOO/OBR/images/) directory.** Both exist on disk and on the live site but are now orphaned (no inbound links from the regen-state pages). At minimum `overview.html`, `index.html`, and the nav must restore the link.

R6. **Verify or correct the alpha91 file-size figure.** Current regen shows "199 files · 824.7 MiB total" in `index.html`. The dist archive at `X:\dev\OblivionRemastered_OOO\dist\alpha91.7z` is 215.9 MiB (verified at write time of `cd650fa`). One of these is wrong; figure out which and document the source for the next regenerate cycle.

R7. **Update `phase9-unify-tracker.md` ingestion**, since the validation table on `overview.html` is sourced from that file in the MapClone repo. The next session should re-pull (the headline number was 15/17 fully validated at last read; that file may have moved since).

R8. **Document the workflow** in `CLAUDE.md` or a `CONTRIBUTING.md` at the repo root so the rule is enforceable on the next session (and on the OOO-repo side).

## Open questions for the planning session

- Who runs `sync_pages.py` and on what trigger? Cron? Manual? Pre-release? The answer drives R3's design.
- Is `sync_pages.py` aware of "files modified since last run" or does it always blast? If the former, hand edits can win by being newer; if the latter, R3's guard-rails are mandatory.
- Are there *other* devnull pages outside `docs/OOO/OBR/` that are also Markdown-sourced and at risk of the same conflict? A repo-wide audit is cheap.
- Should `new-Items.html` move into the Markdown-sourced workflow (as a `docs/new-items.md` in the OOO repo), or stay hand-edited? It is rich content with custom CSS, so probably stays hand-edited — but the source data (which item sets, what images) is mechanical and could plausibly be generated.
- What is the relationship between `X:\dev\OblivionRemastered_ItemClone\docs\item-tracker.html` (the original from which `new-Items.html` was derived) and the OOORF site's copy? Will the ItemClone repo's tracker continue to evolve, and do we want to track those changes?

## Acceptance criteria for the resulting plan

1. Every bullet under "What was lost" is restored on the live site or explicitly classified as "intentionally not restored, with reason".
2. Every substantive contribution from `b945ff2` (terminology, new file-list entries, etc.) is preserved.
3. A future re-run of `sync_pages.py` against the current `main` produces zero unwanted changes to the OBR pages (whether by skipping them, by failing if it would clobber, or by producing exactly the current content because the Markdown was updated to match).
4. A note in `CLAUDE.md` (or `docs/OOO/OBR/CONTRIBUTING.md`, or `docs/OOO/OBR/README.md`) tells the next contributor — human or AI — which side owns each file and what to do if they need to change content the other side owns.
5. The Markdown converter's table and code-block bugs are either fixed or work-arounded (e.g., the rich pages don't rely on those features).

## Key files and references

- This repo (`devnull`):
  - [`docs/OOO/OBR/`](../docs/OOO/OBR/) — the affected pages
  - [`.vscode/settings.json`](../.vscode/settings.json) — cspell allowlist (preserved; not in `b945ff2`'s scope)
  - Commit `cd650fa` — the hand-edited version that was clobbered
  - Commit `b945ff2` — the regenerate commit that clobbered it
- Companion repo `X:\dev\OblivionRemastered_OOO`:
  - `docs/overview.md`, `docs/changelog.md`, `docs/dependencies.md`, `docs/installation.md` — Markdown sources
  - `docs/per-release/alpha91.md` — per-release diff doc
  - `manifests/alpha91.json` — file-level manifest with SHA-256s + sizes
  - `scripts/sync_pages.py` — the converter (likely culprit for the bugs; not yet read)
- Source of truth for the validation table: `X:\dev\OblivionRemastered_MapClone\docs\phase9-unify-tracker.md`
- Memory: [`reference_ooorf_esp_inventory.md`](../../../Users/aubre/.claude/projects/x--dev-devnull/memory/reference_ooorf_esp_inventory.md) — where to look for ESP-level ground truth when describing record changes.
