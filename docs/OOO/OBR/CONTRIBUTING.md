# Contributing to the OOORF release-tracker pages

These pages (`docs/OOO/OBR/*.html`) have two potential contributors: **hand
edits in this repo** and an **auto-generator** (`scripts/sync_pages.py`) in the
companion repo `OblivionRemastered_OOO`. This file is the contract that keeps
them from clobbering each other.

## Ownership: every page here is HAND-CANONICAL

`index.html`, `overview.html`, `new-Items.html`, `devlog.html`, `changelog.html`,
`install.html`, `dependencies.html`, and `spawn-danger.html` are edited by hand. Each carries this
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

## Spawn Danger data, one file per release

`spawn-danger.html` is hand-canonical like the others. Its map data is not in the
page: each release has `spawn-danger/<tag>.json`, listed in
`spawn-danger/releases.json` (newest first; the page opens the first entry, and
`?release=<tag>` opens another). To add a release, build RAX's heatmap
(`tools/spawnlog/spawn_heatmap.py`) with that release installed, then:

    python scripts/add_spawn_danger_release.py <ooo-spawn-heatmap.html> <tag> --date YYYY-MM-DD \
        --source "<the plugins in the load order that change creatures or leveled lists>"

## If you genuinely want a page to be machine-owned again

Remove its marker, move its content into the OOO repo's Markdown sources, and
let `--apply` own it. Until then, assume hand-canonical.
