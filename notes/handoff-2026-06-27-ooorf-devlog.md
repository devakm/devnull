# Handoff — 2026-06-27: OOORF devlog (alpha92 entry in flight)

Session handoff so another session can take over the OOORF release-tracker site work without losing context.

## Where things stand

- **Guard-rail system: done, live.** All `docs/OOO/OBR/*.html` pages are hand-canonical, each carries
  `<!-- DO-NOT-REGENERATE: hand-canonical. ... -->`. A pre-commit hook (`scripts/check_obr_markers.py`,
  installed via `scripts/install-hooks.sh`) blocks any staged OBR page that is missing the marker, or
  contains a control byte, or has a malformed `<nav>`. The OOO repo's `scripts/sync_pages.py` is a
  diff-by-default advisor that skips marked files. Contract: `docs/OOO/OBR/CONTRIBUTING.md`.
- **Devlog: alpha91 entry is live.** `docs/OOO/OBR/devlog.html` — single growing page, newest release
  first. Each release = intro + arc cards (anchor-jump `#a<rel>-<slug>`) into a dated chronological
  milestone spine. Set milestones show a character render (`images/refs/OBR-OOO-item-<Set>-Armor_F*.png`)
  plus piece icon(s) (`images/item-tracker-assets/<Set>_Cuirass.png`).
- **alpha92 entry: drafted, AT THE REVIEW GATE, not yet built.** Prose draft is committed at
  `notes/devlog-alpha92-draft.md`. alpha92 is IN PROGRESS (unreleased) — frame as "work so far," never a
  release. Six new armor sets: **Dragonborne, Draconis, DaedricPrince, Dread, ImagoStorm, DremoraElite**
  (last four are a Daedric family) + a self-verifying-QC-gates thread. 5 arcs / 12 milestones.

## Next steps (resume here)

1. **Get user sign-off on the alpha92 draft** (and the one open question below).
2. **Host the six new-set renders.** Copy the best front render for each from
   `X:/dev/OblivionRemastered_ItemClone/original/UE5_OOO_ArmorReference/` into
   `docs/OOO/OBR/images/refs/`. Picks found: `Dragonborne-...-v4-front`, `DaedricPrince-...-v7-front`,
   `Dread-...-v9-front`, `ImagoStorm-...-v3-front`, `DremoraElite-...-v3-front`. **Draconis lacks a clean
   `front` render** (only cuirass/logo shots) — resolve before build (pick a usable angle or ask user).
3. **Build the alpha92 `<section>` ABOVE the alpha91 one** in `devlog.html`, using the same templates
   (arc cards → spine, `.devlog-renders` + `.devlog-thumbs`). Map each `[THUMB: Set]` to its hosted render.
4. **Verify**: `python scripts/check_devlog_anchors.py docs/OOO/OBR/devlog.html` (anchors + control bytes
   + nav), `python -m pytest -q`, confirm every referenced image exists. Then commit; push when the user says.

## Open question

- **Draconis in-game retest.** The 06-20 ItemClone handoff has Draconis built and gate-green but with one
  in-game retest pending; no later confirmation was found. Draft hedges it. User to confirm or keep the hedge.

## Voice rules for the devlog (ENFORCE — hard-won via correction)

- Restrained journalistic (who/what/why/when). **No "team," no "we," no "I"** — release/problem/solution is
  the subject.
- **No hype, wit, or drama.** Accomplishments speak for themselves.
- **Do not count attempts** (no "v35," "fifteen tries") unless explaining a real delay/gap.
- **Avoid "ship/shipped"** unless an actual release; use built/completed/added/confirmed.
- **"today," not "this day."**
- **Translate out** raw EDIDs, FormID hex, commit hashes, internal version tags.

## Gotchas

- Imagery: set milestones use BOTH the character render AND the piece icon (a prior pass wrongly dropped
  the icons). Reference-render filenames have quirks: `GrayFox`→`GreyFox`, `ShadowMail`→`Shadowwmail`.
- The WornLeather piece icon in `images/item-tracker-assets/` is wrong (vanilla Pit Armor, not the Thief
  recolor) — a known ItemClone-side issue; in the devlog it's intentionally marked with a red ✗ +
  "to be fixed in alpha92" caption. Same wrong icon is on `new-Items.html` (not yet fixed there).
- Scripted nav edits once injected a `\x01` byte (a `\1` backreference in a non-raw Python string) that
  broke the Changelog link site-wide — that's why the control-byte + malformed-nav guards now exist.
- `docs/` is published (GitHub Pages serves from it). Keep planning docs in `notes/` (not published).
- Sources: ItemClone `docs/handoff-*.md` (+ `git log` author dates) for item sets; MapClone
  `phase9-unify-tracker.md` for dungeon validation; OOO `docs/per-release/*.md` + `manifests/` for figures.
