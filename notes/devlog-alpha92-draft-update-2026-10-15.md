# alpha92 devlog draft — UPDATE

**BUILT 2026-10-18 after alpha92 was released.** All 16 milestones below went into
`docs/OOO/OBR/devlog.html`, plus five written at build time: Light of Dawn on 10-07, 10-13 and
10-15 (the weapon shipped in alpha92, so the "optional" block below was promoted and revised),
the SyncMap three-way review on 10-17, and DarkMalachite / Vella's armor / icons on 10-18.
Open decisions resolved by the defaults: all arc cards kept, intro rewritten as released, the
cross-repo parallel kept, the ghost fire named on overview.html as a known issue (not in the
devlog). The intro and cards were re-linted after the build (2 deliberate survivors, as noted).

Extends the existing alpha92 section. Everything here is **new material after 2026-07-04**, the
date the current section ends. Sources digested in `notes/devlog-alpha92-source-digest-2026-09-07.md`,
plus a second sweep on 2026-10-15 (see "What changed since the 09-07 draft" below).

**Supersedes `notes/devlog-alpha92-draft-update-2026-09-07.md`.** That draft never passed its review
gate. This version carries all of it forward and adds the material through 2026-10-15.

alpha92 is not released. Nothing below describes it as released.

**Language pass (2026-09-07, extended 2026-10-15):** rewritten under ASD-STE100, STE-flavored mode.
Structural rules enforced: sentences at or under 25 words, no semicolons, no phrasal verbs, no
nominalizations, no marketing adjectives, simple tenses, one term per action. Metaphors removed
throughout. Departures are recorded at the end.

---

## What changed since the 09-07 draft

- **Red Gill Cave was confirmed in game today, 2026-10-15, in all five phases.** Every dungeon in
  the release is now validated. The intro, the `a92-water` card, and the 09-07 water milestone are
  revised, and one new milestone is added.
- **Ancestral's 09-07 approval closed the Amelion family.** The 09-07 Ancestral milestone now says so.
- **The "southern arm never walked" open item is removed.** MapClone retracted that claim on 09-07
  as unsupported (`2b49445`).
- **One open defect is now on record.** MapClone logged a ghost fire in Gloom Way's second zone as an
  open immersion defect that must be fixed before release. See the fact-check notes.
- **Light of Dawn, the first weapon set, started 10-05.** It is on an unmerged branch and its latest
  rounds are not confirmed in game. It is drafted below as an optional block, **out by default**.
- **Not included:** ItemClone's QC gate for the inventory CSV (09-12) and MapClone's map-render
  design (09-12 to 10-06). Both are internal tooling with no player-visible effect.

---

## Intro — REVISION

The current intro says the map work settled at alpha91 and alpha92 is armor only. That is no longer
true. Suggested replacement:

> alpha92 is in progress. The armor work extends the recolor pipeline across a family of sets that
> share one base material, Amelion. Amelion is a bright silver tier with indigo trim and fine silver
> pattern work, and that pattern work needed methods the earlier recolors did not have. The map work
> returns after alpha91. Two water caves had never had a full cleanup session. Both are now closed,
> and every dungeon in the release is validated. Twice in this period a fix came faster from copying
> a verified neighbor than from deriving a new one. The armor pipeline and the map pipeline reached
> that conclusion separately on the same day.

---

## Arc cards (5 new)

- **The Amelion correction** | `a92-amelion` | Noble was first built on Steel, on the evidence of the
  item records and of an earlier set that cloned Steel successfully. The premise was wrong. Noble is
  an Amelion set, and the whole steel build was discarded and started again. The rebuild produced a
  donor template that two later sets reused.
- **Fine pattern work** | `a92-filigree` | Ordinary recolors returned the silver pattern work on
  Amelion armor with hard white edges. Three methods fixed it: treat a pixel's brightness separately
  from its color, derive the pattern's extent from the mesh instead of drawing it by hand, and read
  a panel's raised rim from the relief map when color and brightness cannot find it.
- **Noble, object by object** | `a92-noble` | Seven weeks of tuning one set one object at a time, each
  change confirmed in game before the next began. It ended on a hand-painted benchmark that exposed
  three separate ownership declarations. Each one held pixels out of the treatment entirely.
- **The Ancestral sets** | `a92-ancestral` | Three sets built from the Amelion template in three
  days — the pristine Ancestral set, a Worn Ancestral variant, and an Unfinished Ancestral with its
  trim tarnished. Every new surface control was added switched off, so the other two dozen sets
  rebuild byte-for-byte identical.
- **The last water caves** | `a92-water` | Gloom Way Cave and Red Gill Cave were the two dungeons that
  had never had a full cleanup session. Both are now validated. An invisible wall in Gloom Way's first
  zone was removed, and its second zone's water surface now reaches across the whole cave. Red Gill
  needed one suppression entry removed to get its light back.

---

## Chronological spine — new entries (2026-07-04 -> 2026-10-15)

- `2026-07-04 | a92-amelion | Noble's base material corrected, and the first build discarded | Noble was first built on Steel. The premise came from the item records, which show an ebony binding, and from an earlier set that cloned Steel successfully. It was wrong. Noble is an Amelion set: bright silver plate, indigo trim, and fine silver pattern work. No adjustment to a steel body reaches that. The whole steel build was discarded, including its configuration, its masks, its packaged output, and the flat icons requested for it. Work restarted on the Amelion body the same day and built the material layer, the glow pipeline, and the first masks against it. The discard is why the set took until late August instead of mid-July.`

- `2026-07-13 | a92-filigree | Hard white edges traced to a forced lightening | The silver pattern work on the Amelion cuirass kept returning with hard white edges, and no mask correction removed them. The cause was in the recolor. One step lightened the anti-aliased boundary of the trim, which forced those boundary pixels toward white whatever sat under them. The replacement separates a pixel's brightness from its color and inverts only the brightness. It applies to the silver strokes alone, and composites over a build that is otherwise already right. The pattern keeps its shape, and its edges keep the tone under them. The forced lightening was removed from the pipeline rather than tuned.`

- `2026-07-15 | a92-filigree | The chest plate's central pattern, derived instead of drawn | A hand-drawn mask covered the cuirass's central pattern, and its brightness threshold was lopsided. It clipped the shaded right side of the panel, where ambient occlusion darkens the plate. The pattern then read as present on one side and absent on the other. The drawn mask was not adjusted. The pattern's extent is now derived instead. The derivation takes the panel's own mesh territory, thresholds it for the bright low-saturation strokes, isolates the connected components, and subtracts the enclosing frame. The drawn seed was retired. The result was confirmed in game. The tone that came with it improved the whole set in one pass, not just the piece it targeted.`

- `2026-07-16 | a92-noble | Per-object tuning, and a tool to review it | With the pattern solved, the set moved to tuning one object at a time, starting with the neckguard lining. Each change was rendered, reviewed, and confirmed in game before the next began. A durable review page was built alongside it, so a proposed change could be seen against the current state instead of described. The working pattern is a recolor authored for one named object and applied only there. It became the standard approach for the rest of the set.`

- `2026-07-18 | a92-noble | The rondel, and two standards that came out of it | The rondel's pattern needed two masks working together, one for the pattern's core and one for its shadow. A single mask could not hold both the stroke and its depth. That recipe was written down. So was a second standard, which governs how a frame's edge fades into the panel it encloses. Both were generalized past the pieces that produced them, and the working branch was merged.`

- `2026-07-21 | a92-noble | Gems read from the transparency channel | The gems on the helmet and boots would not take a recolor through the usual route. Their masks are not in the metallic chain that carries every other surface property. They sit in the diffuse texture's transparency channel, which the master material routes as a per-gem reveal. Reading them there instead of deriving them let the gem passes run as an ordinary post-step. The order of those passes was then fixed, so it does not move between sets.`

- `2026-08-01 | a92-noble | Masks that reach the pass, and that record what they are | Two related faults closed. First, a hand-painted mask was wired to a surface class that never consumed it. The mask was correct, committed, and inert, and no part of the build reported that it went unused. Confirming that a mask reaches the pass that reads it became a required step. Second, masks now record their own provenance. Whether a mask is hand-painted or pipeline-derived is written into the artifact when it is made, instead of inferred later from where the file sits. Both faults produced work that looked done and was not.`

- `2026-08-23 | a92-noble | The helmet benchmark, and three ownership declarations | A hand-painted helmet mask arrived as a quality benchmark for mask generation. It is a specification to consume as delivered, not a guide to approximate. Wiring it exposed a defect underneath: hard sawtooth cutouts and a punched-out blob on one helmet panel. None of it was residue the treatment had failed to lift. Three separate declarations of ownership held those pixels out of the plate treatment altogether, so they rendered as untouched vanilla with mask-shaped edges. They were a stale mask left in place after it measured as harmless, and a protective passthrough that preserved a belief about the panel's color. A third mask was carved against both. Measurement dissolved the belief in seconds. After the fix the visible artifact dropped to roughly a quarter of its extent. Untreated pixels on the helmet fell from tens of thousands to about a hundred and forty. The fix also closed a defect noted in the set's own configuration a month earlier. Noble was confirmed in game and closed for the release, with one cuirass improvement deferred. [THUMB: Noble]`

- `2026-08-23 | a92-amelion | Amelion kept as a donor template | The finished Amelion set was replicated as a donor template of fifty-one files, ready to repoint at a new set. The alternative was to record how the set had been built and derive the next one from that record. A confirmed result is cheaper to copy than a written method is to re-derive. The three sets that follow are the trial of that claim.`

- `2026-08-23 | a92-water | The last two water caves onboarded | Gloom Way Cave and Red Gill Cave were the only dungeons that had never had a full cleanup session. Both are water caves, and in both the water sat at the wrong height. The game data places a water level that the rendered cave does not match. The surface was lifted to its true position and the geometry under it was brought into agreement. Ghost-object suppression was deployed for all three zones in the same pass.`

- `2026-08-30 | a92-water | The invisible wall in Gloom Way's first zone | An invisible barrier blocked the tunnel that connects Gloom Way's first zone to the rest of the cave. The obstruction was not ordinary geometry. Two vertical emissive light cards, the flat panels that paint a glow onto a cave wall, carried collision and stood across the passage. They sat in a layer that had not been searched. That is the general lesson: a cell is assembled from six layers, and an obstruction can be in any of them. The cards were suppressed and the surface was measured against forty-three depth probes. The zone was then confirmed in game.`

- `2026-09-05 | a92-ancestral | Ancestral, onboarded in a day | The Amelion template took the Ancestral set from nothing to in game in one session. It was scaffolded, repointed, measured against the template's recipes, built, rendered, approved on its look, and deployed. The set is six pieces, with the winged helmet and shield folding onto the standard helmet and shield slots. The in-game round then found two defects in the grime, which set up the following day. [THUMB: Ancestral]`

- `2026-09-06 | a92-ancestral | Separating grime from wear | Fixing Ancestral's grime meant separating three effects that had been treated as one. The stains and the scratches sit at different spatial frequencies and are now handled apart. The mottling across the plate proved to be a color-saturation artifact rather than a brightness one. The rondel's base plate, long assumed to be gold, was measured and had never been gold. Five new surface controls came out of the work. Every one stays switched off unless a set asks for it, so the other two dozen sets rebuild byte-for-byte identical.`

- `2026-09-07 | a92-water | Gloom Way's second zone, and the recipe that already existed | The second zone's water had to reach across the whole cave. Getting it there took a week and seven rebuilds, and five of those corrected a real component without moving the visible surface at all. The cause was not technical. A complete recipe for this exact job, nine components working together, already existed in the configuration of a cave confirmed in game back in May. The week went to deriving a new recipe instead of comparing against that one. The rule written down afterwards is to diff a new cell against the nearest confirmed cell before deriving anything. A second finding came with it. The stored bounds of a water mesh decide only whether it is drawn, never what shape it takes, because the engine recomputes them on load. The shape lives in the vertices. The zone was confirmed in game against eleven depth probes. Gloom Way Cave is closed. That left Red Gill Cave as the one dungeon without a full cleanup session.`

- `2026-09-07 | a92-ancestral | Two more sets, and the rule about copying | Two variants were built from Ancestral and confirmed in game the same day. The worn set is Ancestral at half strength with its grime kept, and it was approved on its first look. The unfinished set removes the glow and tarnishes the trim, which needed a new control. Tarnish is produced by amplifying a region's mid-tones rather than by adding more grime over them. It tapers off in the darks, so no black ring forms at the edge. The session also named a failure that recurs across the whole project: copying a proven method without the guards that made it work. The rule written down is to port the guards, not just the unit. The map work reached the same conclusion from the opposite direction on the same day. Ancestral's own final revision, a darker trim and a glow in the gems' own hue, was also confirmed in game that day. That closed the Amelion family for the release. [THUMB: WornAncestral] [THUMB: UnfinishedAncestral]`

- `2026-10-15 | a92-water | Red Gill Cave, and the last dungeon | Red Gill Cave was built in August but did not have a cleanup session until now. Its water surface rises 57 units over the vanilla level. It needed none of the extra water components that Gloom Way's second zone needed, because the vanilla water area already encloses the cave. A build gate failed on the first attempt. It read the water's tile grid from the wrong position in the file. The gate was fixed, and the earlier caves' results stay valid because the misread did not change their outcome. In game, the water was right, but the cave had no ambient light. One suppression entry removed the prefab that holds the cave's sky light. A bulk migration in May added that entry with no recorded reason, and every other water cave keeps its sky light. That one entry was removed and nothing else changed. The zone was then confirmed in game in all five phases, against twenty-three depth probes. The measured surface was within one unit of its target. Every dungeon in the release is now validated.`

---

## OPTIONAL — Light of Dawn (out by default)

Include only if the Light of Dawn set goes into alpha92. As of 2026-10-15 it is on an unmerged
branch. Rounds 15 to 22 are built but not confirmed in game, and three defects are open. The
recommendation is to hold it for the next release section. The prose below is ready if that changes.

Arc card:

- **The first weapon** | `a92-weapon` | Light of Dawn is the first weapon set. Its blade carries a
  flame etching that glows, through four restoration stages from tainted to restored. Armor methods
  did not carry over directly. A weapon scopes its glow by a material slot and by the mesh's vertex
  color, not by the diffuse transparency channel that the armor gems use.

Milestones:

- `2026-10-07 | a92-weapon | A weapon, and a mask drawn by hand | Light of Dawn opened the weapon work. Its most-restored stage was recolored from a pink copper to a darker red copper and confirmed in game. The flame etching on the blade was harder. Several derived masks failed to separate the etching from the blade around it. The etching mask was then drawn by hand and used as delivered, and the derivation was removed. A set of white specks that remained came from the preview renderer, not from the mask.`

- `2026-10-13 | a92-weapon | How a weapon scopes its glow | All four stages now run on one shader with a real glow ramp, and that build was confirmed in game. Black spots that moved with the view angle were traced to a parallax depth setting on the blade's layer map. Setting it to zero removed them. The fire enchant is scoped by the mesh's vertex color. The vertex mask therefore had to be cut at the blade's start, not only the texture mask. Work continues on the balance between glow strength and the layer map's dark streaks.`

---

## Language-pass notes

- **Mode: STE-flavored, not Strict.** The skill excludes creative prose from Strict and names
  explanatory prose as the STE-flavored case. Structural rules are enforced in full. Lexical rules
  are applied as a direction only, since the approved-word dictionary is not redistributed.
- **One term per action.** In-game verification is always "confirmed in game". The earlier draft
  rotated "verified", "validated", and "confirmed" for the same action. Dungeon testing is always a
  "cleanup session", following the term used in the arc-card edit.
- **Metaphors removed.** "Grew teeth", "made of light", "outlived it", "resisted every recolor",
  "arrived independently", "the test of it", "lifted the whole set", and "claims of ownership" are
  all gone. "Ownership declaration" is kept because it is the pipeline's own term for the artifact
  that carves a mask's scope, not a figure of speech.
- **Semicolons removed.** All six are now separate sentences (Rule 8.1 bans the mark outright).
- **Passive voice kept in places, deliberately.** The devlog's standing voice rule forbids "we", "I",
  and "team" and makes the release or the problem the subject. That rule and STE's active-voice
  preference conflict. STE permits passive in descriptive text when the actor is irrelevant to the
  reader, which is exactly the case here, so constructions like "was discarded" and "was confirmed in
  game" stay. Where an inanimate subject could act, it now does.
- **Linter result.** `scripts/ste-lint.py` from the skill repo, run over the published prose only
  (intro, arc cards, milestone bodies): **13 hard violations before, 2 after**, 2.0 per 100 words.
  Both survivors are deliberate. First, "Gloom Way is now completed and validated" keeps "validated"
  because that is the published status word on the overview page and the term used in the arc-card
  edit, and a dungeon passing its phases is a different action from an armor change confirmed in
  game. Second, "The mask was correct, committed, and inert" uses "correct" as an adjective, not as
  the verb in the fix/repair/correct group. The linter does no part-of-speech tagging and says so in
  its own source.
- **Paragraph length is the one structural rule not met.** STE caps a paragraph at six sentences.
  Four milestone bodies run to eight or eleven. Splitting them would break the devlog's one-body-per
  -milestone format, and cutting them would drop facts. Flagged rather than forced.
- **No facts changed.** Every figure, date, hedge, and qualifier is carried over. Nothing was added
  to make a sentence read better.
- **New prose (2026-10-15).** The Red Gill milestone, the revised intro and water card, and the
  optional Light of Dawn block were written to the same rules. "Validated" is kept for the dungeon
  status, as before. "Confirmed in game" is kept for every in-game check.

---

## Fact-check notes

- **Dates are commit author dates.** Where a handoff filename's date differs from the commit date, the commit date is used. Ancestral's own final approval, a darker trim plus the gems' own-hue glow, landed 09-07 on the main branch after the 09-07 handoff was written. It is folded into the 09-06 and 09-07 entries rather than given its own milestone.
- **Set status.** Noble was confirmed in game and closed for the release on 08-23. Ancestral was confirmed in game, with its latest revision approved 09-07. Worn Ancestral and Unfinished Ancestral were both confirmed in game on 09-07. All four are built and their packages are current.
- **In-progress framing.** alpha92 is not released. Nothing is described as shipped. Items are "built", "confirmed in game", or "closed for the release".
- **Attempt counts.** Two appear, and both explain a real delay, which the voice rules permit. They are the Noble discard on 07-04, which explains a six-week slip, and the seven rebuilds on Gloom Way's second zone on 09-07, whose point is that the delay was avoidable. The 09-06 Ancestral session ran eleven revisions in one day. That is deliberately not stated, because it explains nothing.
- **Open items carried, not resolved.** One improvement to the Noble cuirass is deferred to a later release. The 09-07 draft also listed a southern arm of Gloom Way's second zone as never walked. MapClone retracted that claim the same day as unsupported, so it is removed.
- **Red Gill figures.** From MapClone `phase3-water-model-testing.md` (RGCz1-T1-v3, RGCz1-T2-v1) and the tracker row. Water surface 114.30 to 171.45 (+57 units). The tile-grid check read the pair at the wrong byte offset. The tracker states that the earlier passes for both Blood Clot Cave zones and Gloom Way's second zone stay valid. In game, 23 depth probes, surface error 0.3 units, rendered in the milestone as "within one unit". All five phases confirmed.
- **Open immersion defect (new).** MapClone's tracker now lists the Gloom Way second-zone ghost fire under "Open immersion defects". The tracker says these do not block a zone approval but must be fixed before release. Large flames show on a burnt rubble pile that classic Oblivion has without fire. They deal no damage. It is not in the devlog prose. See decision 5.
- **Gloom Way grid gap.** The tracker still shows nav, positions, and flicker as unmarked for both Gloom Way zones. Only water and suppression carry a check mark. "Validated" for Gloom Way rests on the in-game approvals. This is unchanged from the 09-07 note.
- **Not included.** The program dashboard built in the OOO repository at the end of August is internal tooling with no player-visible effect, and is left out. The same applies to ItemClone's inventory-CSV QC gate (09-12) and MapClone's map-render design and plan (09-12 to 10-06). The Amelion template branch is not merged. It is described as created, which is accurate.
- **Vocabulary.** "Ground truth" and "lane" are both under standing bans and do not appear. Object numbers, item ids, texture and component names, commit hashes, and version tags are translated out of the prose. Set names are written as two words, so "Worn Ancestral" rather than the packaged spelling.
- **Before the build.** `docs/OOO/OBR/overview.html` has an uncommitted 09-07 edit that reads "16 of 17". It must read 17 of 17, with Red Gill Cave's row set to Validated and the caveat paragraph rewritten, before the devlog goes live. Otherwise the two pages disagree. No renders are hosted yet for Noble, Ancestral, Worn Ancestral, or Unfinished Ancestral. The four `[THUMB: ...]` markers all need picks from the reference render folder. The piece icons need regenerating on the ItemClone side first, since that icon asset set is stale as of 2026-07-02.

---

## Open decisions for review

1. **Arc count.** This adds 5 arc cards to the existing 9, and 16 milestones to the existing 20, for a 14-card and 36-milestone alpha92 section. With Light of Dawn it is 15 and 38. If that is too heavy, the merge candidates are `a92-amelion` folding into `a92-noble`, and the 07-16, 07-18, and 07-21 milestones collapsing into one.
2. **The intro rewrite** above drops the claim that alpha92 is armor only, and now states that every dungeon is validated. Confirm the wording.
3. **The cross-repo parallel**, meaning copy the confirmed neighbor and port the guards, appears in the intro and both 09-07 milestones. It is the most interesting result in the period, but it is a process observation rather than a player-visible change. Keep or cut.
4. **Light of Dawn.** Out by default (unmerged, unconfirmed rounds, open defects). Confirm, or include the optional block.
5. **The ghost fire.** The tracker says it must be fixed before release. Either fix it before alpha92 and say nothing, or name it in the devlog as a known open defect. The draft currently says nothing.
6. **overview.html.** Update it to 17 of 17 in the same commit as the devlog, or as a separate commit first.
