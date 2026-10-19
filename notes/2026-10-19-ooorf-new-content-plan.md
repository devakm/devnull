# Plan — marking content that is new in OOORF (never in classic OOO)

Status: **planned, not started** (2026-10-19). Working note; `docs/` is published, this is not.

## Why

Readers cannot tell which OOORF content carries classic OOO forward and which is new. The site
needs to say so, and the credits depend on it:

- Sets that carry a classic OOO family forward are credited "New armor set created by devakm with
  inspiration from classic OOO artists."
- Content that never existed in classic OOO is credited "New armor set created by devakm."

## What is already on the site (2026-10-19)

Only what the user stated, with no diff behind it:

- The **Ancestral**, **Worn Ancestral** and **Unfinished Ancestral** armor sets: credit changed to
  "New armor set created by devakm."; a "New in OOORF" tag on their New Items cards.
- An overview section **"New in OOORF — not in classic OOO"** that names the Ancestral armor, the Royal
  weapons, the Ancient Harbinger armor and weapons, and the Ancient Gargoyles, and says the list is
  not yet complete.

## What a complete list needs: a diff against classic OOO

1. **Pick the baseline.** Classic OOO 1.36 (`Oscuro's_Oblivion_Overhaul.esp`) plus the classic
   Shivering Isles add-on (Saldron). Confirm the exact files and versions with the user, and where
   they are on disk.
2. **Inventory the baseline** with the OOO repo's own tools (`scripts/build_records.py`,
   `tes4_parser.py`) into a `work/_inv_classic/` set, matching the per-release `work/_inv_<tag>/`.
3. **Diff the baseline against the latest release** (`scripts/diff_records.py`). Match records by
   EditorID first, then by FormID, because OOORF renamed some records (the Harbinger pieces became
   "Ancient Harbinger" in alpha92).
4. **Classify each OOORF-only record.**
   - New: a record that has no classic counterpart.
   - Renamed: a classic record with a new display name only. This is NOT new content.
   - Reworked: a classic record whose role changed enough that the user calls it new (Ancient
     Harbinger is the example to settle).
   The user rules on every Renamed or Reworked case. Do not guess.
5. **Group by player-facing thing**: an armor set, a weapon line, a creature family, a quest. Do
   not group by record type.

## What the site gets from it

- **New Items:** a "New in OOORF" tag on every card whose set is new, and the plain
  "New armor set created by devakm." credit on those cards.
- **Overview:** the "New in OOORF" section becomes the full, grouped list, with links to New Items
  cards where they exist.
- **Changelog / per-release notes:** from then on, mark new-to-OOORF additions when they ship.
- **Devlog:** no change. It already tells the story of each set.

## Open questions for the user

1. The classic baseline files and versions (OOO 1.36? the SI add-on version?).
2. Ancient Harbinger: is it new records, or classic Harbinger records reworked? This decides how
   the diff counts it.
3. Ancient Gargoyles and the Royal weapons have no New Items card. Should they get one (new
   creature and weapon entries), or only the overview list?
