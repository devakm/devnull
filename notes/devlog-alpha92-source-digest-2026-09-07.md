# Source digest — alpha92 devlog update (swept 2026-09-07)

Working note, not devlog prose. Covers everything in the three source repos since the last
devlog build (2026-07-04, pushed through `b0356c3`). Voice rules do NOT apply here — they apply
at the draft stage (`notes/devlog-alpha92-draft.md`).

Sourcing convention (from `notes/handoff-2026-06-27-ooorf-devlog.md`):
ItemClone `docs/handoff-*.md` + `git log` author dates → armor sets;
MapClone `docs/phase9-unify-tracker.md` → dungeon validation;
OOO `docs/per-release/*.md` + `manifests/` → release figures.

---

## 1. Release state

**alpha92 is still unreleased.** OOO's newest tag is `alpha91`; `docs/per-release/` stops at
`alpha91.md`. Framing stays "work so far," never a release — unchanged from the last build.

---

## 2. ItemClone — the Amelion line (the whole story since 07-04)

The devlog's current alpha92 section ends with the Steel tier and TheBear's gold hardware
(2026-07-04). Everything below is new. The through-line is **one base material, Amelion**,
carrying four shipped sets.

### 2a. The premise correction that starts the arc (2026-07-04)

Noble had been built on **Steel** — derived from the records' Ebony binding plus the BladesElite
pattern. The user ruled that premise wrong: **Noble is Amelion-based.** The entire steel-based
Noble build (config, masks, `dist/Noble*`, the flat-icon call) was discarded and rebuilt.

This is a genuine devlog beat — a wrong foundation caught and paid for, not a tweak. It also
explains why the alpha92 section's "Amelion/Noble excluded as early onboarding, unverified" note
is now stale.

### 2b. Noble — closed for MVP (2026-08-23, `0258c59` on `main`)

Roughly seven weeks of object-by-object tuning. In-game approved and **closed for the MVP
release**. Merged `--no-ff`. The user deferred one item to a later release: *improve the cuirass.*

Capabilities built along the way, each in-game verified as it landed:

| capability | what it solved |
|---|---|
| **Luminance inversion** (base/detail split, applied only to the flipping silver strokes) | the stark white edges mangling trim/filigree — replaced the `aa_trim_ramp` force-lighten that was the proven root cause |
| **Autonomous filigree component** (mesh territory + `S<20 & V>90` + CC-isolate + subtract frame/grate) | replaced a hand-seeded mask whose gate was lopsided (clipped the AO-dark side) |
| **NNRM relief as an orthogonal signal** | finds a framed panel's raised rim where diffuse chroma/brightness cannot |
| **Panel anatomy + face-first masking** | the Cuirass "goo / white hats / white feet" saga |
| **Gem masks via diffuse ALPHA** (`A>128`, not the `_M` chain) | Helmet and Boots gem passes |
| **Authored-patch pass** | hand-crafted masks consumed verbatim as specification |
| **The Helmet benchmark** (#166) | user-delivered 2048² hand-crafted mask, wired as a mask-generation quality benchmark |

**The obj4 artifact (#167) is the strongest single story here.** After the benchmark was wired,
the user reported hard-edged sawtooth cutouts and a hole-punched blob. Three stale ownership
leftovers had kept those pixels out of the plate treatment entirely, so they shipped as raw
vanilla with mask-shaped edges. Artifact pixels **43,039 → 11,384**; whole-helmet teal survivors
**5,093 → 182**; untreated vanilla pixels **62,060 → 141**. It closed a config note that had sat
since 2026-07-20.

### 2c. The Amelion template (2026-08-23, branch `amelion-template`, not merged)

51 files. A verified set replicated as a donor template rather than recomputed — this is what
makes the Ancestral trio fast.

### 2d. Ancestral trio — three sets, three days (2026-09-05 → 09-07)

- **Ancestral** — onboarded end-to-end in one session on 09-05 (six pieces, `FormIDs 00DE61-66`,
  with `pegasushelmet`/`shield` collapsing onto Helmet/Shield). Scaffolded → built → rendered →
  look-approved → in-game, same day. Then v2→v13. Merged `71605d5` (09-06); **v13 approved in
  game 09-07** (`62b858d`, `main` tip) — darker trim plus the gems' own-hue emissive.
- **WornAncestral** — `097c626` (09-07). Ancestral at half strength, grime kept, **approved at
  v1**: *"You one-shotted it."*
- **UnfinishedAncestral** — `1858171` (09-07). Worn look, emissive off, unpolished trim.
  In-game verified.

Five new recolor knobs, all **absent-by-default** so the other 24 sets stay byte-identical:
`fade_limit`, `fade_flatten`, `chroma_flatten`, region-class `off_hue_converge`, and `unpolish`
(tarnishes a region by amplifying its MID band rather than its grime field).

Worth noting for the spine: the 09-06 session ran **v2→v11 on one set in one day**, and almost
every round was a *method* correction caught by the user on a render, not a value tweak. That is
the honest shape of the work — but per the voice rules, do not count attempts unless it explains
a real delay.

### 2e. Process capabilities that became durable

Two skills and a hard vocabulary ruling came out of this stretch:
- **`user-mask-contract`** — demanded by the user after four failed mask readings in one day.
- **`porting-a-proven-method`** — "port the GUARDS, not just the unit." The user named it as the
  most repeated failure in `key-learnings.md` (#161/#167, #168, #169, #172, #176, #178).
- **Vocabulary rulings:** "ground truth" BANNED (07-27); "lane" BANNED (08-23). Both are recorded
  as data lines in `tools/conventions.json`. Devlog prose should avoid both terms.

---

## 3. MapClone — the water caves CLOSED OUT

Two arcs, both on the cells that were the outstanding validation gap.

**2026-08-23** — Gloom Way z1/z2 and Red Gill onboarded: native water Z lift at scale
`k=1.42875`, plus suppression deploys (77/77, 84/84, 33/33 actors), and 30 RootHavok instances
suppressed in Gloom Way z1/z2.

**2026-08-30 — Gloom Way z1 APPROVED (`GWCz1-T5`).** The invisible barrier was solved: vertical
`M_Li_Emissive` light cards in the `_Li` layer carrying collision (`StaticMeshActor_18/_20`). The
lesson generalizes — *search ALL SIX layers*. Water 43 casts all pass.

**2026-09-07 — Gloom Way z2 APPROVED (`GWCz2-T7`, `ca85cbe`).** Haze, depth and the visible
surface all confirmed; 11 casts all pass. It took seven iterations, five of which fixed a real
member without moving the surface. Per the session handoff, **the cause of that thrash was a
process failure, not a technical one**: a complete nine-member recipe for exactly this job already
existed in the `L_BloodClotCave02` config block. The durable rule out of it — *diff a new cell
against the nearest verified cell's block before deriving anything* (KL 124) — is the same
"port the guards, not just the unit" lesson ItemClone landed as a skill on the same day. That
parallel is worth a devlog beat.

Also from that arc: **bounds GATE a mesh, verts SHAPE it** — serialized `FBoxSphereBounds` are a
rendering no-op, the engine recomputes them at runtime (KL 124/125).

**Gloom Way Cave is completed and closed out. Red Gill Cave is the only water-bearing OOO cell
still never walked** — so the dungeon count moves 15 of 17 → **16 of 17**.

### Page updated (done 2026-09-07)

`docs/OOO/OBR/overview.html` corrected in three places: the headline to 16 of 17, Gloom Way Cave's
row to Validated, and the caveat paragraph below the table to the singular. Verified with
`check_devlog_anchors.py` (marker, control bytes, nav, anchors) + `pytest` (13 passed).

**One loose end, not blocking:** the tracker grid still shows `·` for **P1 Nav / P5 Pos / P9 Flk**
on both Gloom Way zones — only P3 Wtr and P7 Sup carry ✓. The handoff also notes z2's southern arm
(world Y > 2200) was never walked. If those three phases did pass, the grid needs backfilling per
tracker maintenance rule 4; if they were never separately run, the overview's definition of
"Validated" (all applicable phases) is broader than what the grid evidences.

**Retracted from an earlier version of this digest:** I flagged overview.html's "ghost suppression
done" as a published error, on the tracker's "P7 was NEVER SHIPPED" note. That overstates it. The
finding is scoped to one loader — the Method 7 static `ClassIndex=0` patcher — and shows only that
*that* path suppressed zero actors in the 05-16 container. Method 4 (Begone Lua) was the project's
primary suppression path, confirmed in-game from 2026-03-15, and the Gloom Way ✓ was awarded off
`0d47e3d` (03-22) / `37c4630` (04-12), both predating the 05-16 migration. Suppression was the fix
applied, not a phase awaiting a verdict.

## 4. OOO — a new program control plane (2026-08-29 → 08-31)

Not an armor or dungeon change, so it may or may not belong in the devlog, but it is substantial
and currently unrepresented: a static dashboard renderer with Views panel, a collector envelope
with input-based staleness, per-repo run ledger with orphan detection, a branch feed sorted into
actions, milestones with a contradiction gate, sessions joined to handoff documents, a Release
Tracker that **derives** the version rather than declaring it, a Plots panel for MapClone review
artifacts, and a fix so the dashboard discloses its own staleness.

**Recommendation:** leave it out of the devlog. It is internal tooling, invisible to a player,
and the devlog's audience is release-facing. Worth a line only if you want a "how the work is
tracked" aside.

---

## 5. Blocking issue for release staging (not a devlog problem, but found en route)

`ItemClone/docs/item-tracker.html` was **last modified 2026-07-02**. It does not contain Noble,
Amelion, Ancestral, WornAncestral, or UnfinishedAncestral.

OOO's `scripts/gather_live.py` derives its authoritative item-pak ship-list from that file's
"dist packages" column. As it stands, **a release staging run would silently omit all five new
sets** — they would be absent from the ship-list, and their `dist/` paks would not be staged into
`release/`. The paks themselves exist and are built (`dist/NobleItems.*`, `dist/AncestralItems.*`,
`dist/WornAncestralItems.*`, `dist/UnfinishedAncestralItems.*` + the two icon ESPs).

The tracker needs regenerating on the ItemClone side before alpha92 is staged.

---

## 6. Open questions for the user

1. **Scope.** Does the alpha92 devlog section absorb the whole Amelion line (Noble + Amelion
   template + Ancestral trio), or does Noble's 08-23 MVP closure become its own beat given it
   spans seven weeks?
2. **The stale exclusion.** The current section deliberately omits the Amelion/Noble tier as
   "early onboarding, unverified." Noble is now in-game approved and closed for MVP — confirm it
   comes in.
3. **The premise correction.** Include the Steel→Amelion Noble discard (§2a) as a milestone? It
   is a real reversal with real cost, and the voice rules permit explaining a genuine delay.
4. **Renders and icons.** No renders have been hosted for Noble, Ancestral, WornAncestral, or
   UnfinishedAncestral. Need picks from
   `X:/dev/OblivionRemastered_ItemClone/original/UE5_OOO_ArmorReference/` (and piece icons from
   `docs/item-tracker-assets/`, which will need regenerating alongside the tracker in §5).
5. **The program dashboard** (§4) — in or out? My recommendation is out.
6. **The overview.html suppression correction** (§3) — fix now as a separate commit, or fold it
   into the devlog push?

---

## 7. Suggested arc structure (for the draft stage)

Building on the existing 9 arc cards / 20 milestones, the new material looks like roughly four
more arcs:

- `a92-amelion` — the base material corrected, and the template that came out of it
- `a92-filigree` — luminance inversion, the autonomous component, orthogonal relief signal
- `a92-noble` — object-by-object tuning to MVP closure, ending on the obj4 artifact numbers
- `a92-ancestral` — three sets in three days off the template, and the absent-by-default knobs
- (MapClone material folds into the existing dungeon arc rather than a new card)

Milestone dates available: 07-04, 07-15, 07-16, 07-18, 07-19, 07-21, 07-25, 07-30, 08-01, 08-23,
09-05, 09-06, 09-07 (ItemClone); 08-23, 08-29, 08-30, 08-31, 09-05 (MapClone).
