# OOORF Devlog — design / spec

**Status:** Approved design (2026-06-14). Drives the implementation plan. Companion to the
release-tracker site under `x:\dev\devnull\docs\OOO\OBR\`.

## Concept

A new **developer-diary page** on the OOORF release-tracker site that turns the dense, internal
**handoff reports** from the sibling projects (`OblivionRemastered_ItemClone`,
`OblivionRemastered_MapClone`) into a readable "making-of" narrative — the story *behind* each
release, complementing the dry file-level `changelog.html`. Kickstarted with a retrospective on
**alpha91**.

The handoffs are raw material only (full of EDIDs, commit hashes, iteration tags like `BCCz3-T3-v15`,
tool internals). The devlog is a **curated, hand-authored** (AI-drafted, human-reviewed) translation
for a curious modder/player audience — no raw EDIDs or commit hashes in the prose.

## Decisions (locked with the user)

1. **Structure:** a single growing page, `devlog.html`, newest release first, one `<section>` per
   release. alpha91 is the first (and currently only) entry. Split into per-release pages later only
   if it grows unwieldy (YAGNI).
2. **Tone:** enthusiast "making-of" — accessible storytelling that keeps the genuinely interesting
   engineering color, translated (no raw IDs/hashes).
3. **alpha91 entry shape:** **arc cards → chronological spine.** Themed breakthrough arc cards sit on
   top as an overview/teaser layer; each card anchor-jumps (`#a91-...`) into a single dated
   **chronological spine** that holds the complete milestone list. Coverage is comprehensive: every
   dungeon validation and every item set ship is a milestone; the dramatic functionality
   breakthroughs (water, fire, flickering, ghost suppression, icons, GND meshes, recolor) are
   expanded inline; the **date gaps in the spine are left visible** as the long debugging stretches.
4. **Imagery:** reuse the already-hosted item thumbnails now; design layout slots that fill in later
   (v1→v25 progress strips, dungeon screenshots after retests, cropped classic OOO reference shots).
   Not blocking on images that don't exist yet.
5. **Ownership:** hand-canonical, marked `DO-NOT-REGENERATE`; protected by the existing pre-commit
   guard and skipped by `sync_pages.py`.

## A. Page & placement

- **File:** `docs/OOO/OBR/devlog.html`.
- **Marker:** `<!-- DO-NOT-REGENERATE: hand-canonical. See docs/OOO/OBR/CONTRIBUTING.md -->` immediately
  after `<!DOCTYPE html>` (same as the other six pages).
- **Shell/CSS:** the shared shell markup used by the other hand pages — `<link rel="stylesheet"
  href="../../css/devnull-shared.css">` — plus an inline `<style>` block in `<head>` for
  devlog-specific components (mirrors how `new-Items.html` carries its gallery CSS).
- **Nav:** add a **Devlog** entry to the shared nav on every OBR page. New order:
  `Home | Overview | New Items | Devlog | Changelog | Install | Dependencies | Downloads`.
  This is a cross-page edit to the `<nav>` line in all seven pages
  (`index, overview, new-Items, devlog, changelog, install, dependencies`).
- **Cross-links:** `index.html` (Quick links) and `overview.html` link to `devlog.html`. The alpha91
  entry links out to `changelog.html#alpha91`, `new-Items.html`, and the GitHub release page
  (external links carry `target="_blank" rel="noopener"`, the site standard).

## B. alpha91 entry layout (three bands)

Inside `<section id="alpha91">`:

1. **Intro** — one short paragraph framing alpha91 (the release where the 14-set armor wave landed and
   water / fire / flicker / ghost-suppression got solved in the bundled dungeons).
2. **Arc cards** — a responsive card grid (`.devlog-arcs` > `.arc-card`). Each card: a title, a 1–2
   sentence teaser, and an anchor link into the spine. The six arcs:
   - **Taming water** → `#a91-water`
   - **Fire: 15 tries to a bonfire** → `#a91-fire`
   - **Flicker & ghost suppression** → `#a91-flicker`
   - **Icons & GND meshes** → `#a91-icons`
   - **The recolor pipeline (fur is a baked color)** → `#a91-recolor`
   - **The 14-set armor wave** → `#a91-armor`
3. **Chronological spine** — `.devlog-timeline`, a list of dated `.milestone` entries from mid-May to
   mid-June. Each milestone: a date, a title, a short narrative body, and an `id="a91-..."` anchor
   where it is the target of an arc card. Every dungeon validation (from the validation tracker's ✓
   dates) and every item-set ship (from the ItemClone handoff dates) appears; the breakthrough
   milestones carry the expanded arc narrative. Visible date gaps = debugging stretches (called out
   in prose where notable, e.g. the ~8-day water-debugging run before fire rendered on 06-01).

## C. Content arcs and their sources

The drafting agent pulls from these (translating, not quoting raw):

| Arc | Primary sources |
| --- | --- |
| Water | MapClone `docs/phase3-water-handoff-*.md` (05-22 → 06-01); Blood Clot Cave z1/z2/z3 verified 05-26 / 05-27 / 06-01; Deep Cover, Drowned Hopes (XCLW water injection, donor cells) |
| Fire | MapClone `docs/phase3-water-handoff-2026-06-01.md` (BCCz3-T3-v15: 15 iterations, 5 structural bugs, cross-package Niagara clone) |
| Flicker & ghost suppression | MapClone `docs/phase9-unify-handoff-*.md`, `phase9-flickering-fix-TES4.md`; TES4-REFR suppression baked into paks; Begone migration |
| Icons & GND meshes | ItemClone `docs/handoff-2026-06-12-ingame-fixes-and-icon-glow.md`, `handoff-2026-06-13-icon-pfunknown-fur-resolved.md`, `handoff-2026-06-13-gnd-preview-ctd-bisect.md`, `icon-texture-PF_DXT5.md` |
| Recolor pipeline | ItemClone `docs/handoff-2026-06-10-fur-sets-built.md` (MIC vector-param discovery), `handoff-2026-06-05-*` (leather/tonal), `material-change-v1-pristine-overlay.md` |
| Armor wave | ItemClone June set-build handoffs (mithril, eboron, shadowmail, aureus, fur, leather, elven variants); `handoff-2026-06-12-recolor-completeness-glass-rename.md` (BGlass→BlueGlass, RGlass→Drakefired) |
| Spine dates | MapClone `docs/phase9-unify-tracker.md` per-dungeon ✓ dates + ItemClone handoff dates, interleaved |

Cross-checks for factual grounding: the alpha91 per-release doc `X:\dev\OblivionRemastered_OOO\docs\per-release\alpha91.md` and the restored `changelog.html#alpha91` / `overview.html` alpha91 callout (must stay consistent — e.g. +254 disabled REFRs, ~307 SyncMap rebindings, 14 new sets).

## D. Imagery (incremental)

- **Now:** reuse the 94 already-hosted PNGs under `docs/OOO/OBR/images/item-tracker-assets/` to
  illustrate the armor-wave milestones inline (small thumbnails linking to the matching `new-Items.html`
  anchor, like the overview gallery does).
- **Layout slots (empty-friendly):** the CSS includes a `.progress-strip` component (a horizontal row
  of small images for v1→v25 iteration sequences) and a `.shot` figure component for dungeon
  screenshots. Entries render cleanly with these absent; they fill in later without markup rework.
- **Future image home:** `docs/OOO/OBR/images/devlog/` for progress strips, dungeon shots, and the
  cropped classic OOO reference renders (cropping the blank white half is a separate later asset task).

## E. CSS components (inline `<style>` in `<head>`)

- `.devlog-arcs` — responsive grid of arc cards (reuse the `auto-fit, minmax(...)` pattern from
  `new-Items.html`'s `.item-gallery`).
- `.arc-card` — bordered card with hover lift; title + teaser + jump link.
- `.devlog-timeline` / `.milestone` — left-ruled dated entries; a `.milestone .date` style; generous
  vertical rhythm so date gaps read as pauses.
- `.progress-strip` — horizontal thumbnail row (future).
- `.shot` — `<figure>` for a screenshot + caption (future).
- Anchor offset (`scroll-margin-top`) on `.milestone` targets so jump-links don't hide titles under
  any sticky header.

## F. Build scope (this iteration)

In scope:
- `devlog.html` with the marker, shell, inline CSS, intro, six arc cards, and the full alpha91
  chronological spine (all text), with item thumbnails reused inline.
- Nav "Devlog" entry added to all seven pages; cross-links from `index.html` and `overview.html`.
- `CONTRIBUTING.md` note listing `devlog.html` as hand-canonical.

Deferred to the user:
- v1→v25 progress strips, dungeon screenshots, cropped reference renders (the slots exist; the user
  supplies the images later).

## G. Guard-rails (inherited)

`devlog.html` is `docs/OOO/OBR/*.html`, so the pre-commit marker guard (`scripts/check_obr_markers.py`)
blocks committing it without the marker, and `sync_pages.py` neither generates nor `--apply`-writes it.
No new guard-rail work needed.

## Acceptance criteria

1. `devlog.html` exists, is marked, validates as a sibling of the other hand pages (shared shell, nav,
   footer), and commits cleanly through the pre-commit guard.
2. The alpha91 entry has the three bands; all six arc cards anchor-jump to a matching `id` in the spine
   (no dangling anchors).
3. The spine lists every alpha91 dungeon validation and every shipped item set as a dated milestone,
   with the breakthrough arcs expanded and the debugging gaps visible.
4. Prose is translated to the making-of tone — no raw EDIDs, FormIDs, or commit hashes; figures match
   `alpha91.md` / `changelog.html#alpha91`.
5. Nav "Devlog" entry present on all seven pages; `index.html` + `overview.html` link to it; external
   links carry `target="_blank" rel="noopener"`.
6. Imagery: armor-wave milestones show reused thumbnails; the `.progress-strip` / `.shot` slots exist
   in CSS and render cleanly while empty.

## Key references

- This repo: `docs/OOO/OBR/{overview,new-Items,changelog,index}.html` (shell/CSS/nav patterns),
  `docs/OOO/OBR/CONTRIBUTING.md`, `docs/OOO/OBR/images/item-tracker-assets/`.
- ItemClone: `docs/handoff-2026-06-*.md`, `docs/item-tracker.html`, `docs/icon-texture-PF_DXT5.md`.
- MapClone: `docs/phase3-water-handoff-*.md`, `docs/phase9-unify-handoff-*.md`,
  `docs/phase9-unify-tracker.md`, `docs/phase9-flickering-fix-TES4.md`.
- OOO: `docs/per-release/alpha91.md`.
- Prior guard-rail design/plan: `notes/OOORF-page-regen-resolution-design.md`,
  `notes/2026-06-14-ooorf-regen-guardrails-plan.md`.
