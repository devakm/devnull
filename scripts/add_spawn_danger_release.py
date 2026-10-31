#!/usr/bin/env python3
r"""Add one OOORF release to the Spawn Danger page (docs/OOO/OBR/spawn-danger.html).

    python scripts/add_spawn_danger_release.py <ooo-spawn-heatmap.html> <tag> --date YYYY-MM-DD \
        --source "<the plugins in the load order that change creatures or leveled lists>"

<ooo-spawn-heatmap.html> is the page RAX's tools/spawnlog/spawn_heatmap.py builds, from a load
order with that release installed. This writes its OOO data to spawn-danger/<tag>.js and its
vanilla data to spawn-danger/vanilla.js, and puts the release first in spawn-danger/releases.js
(the page opens the first entry). Running it again for the same tag replaces that entry.

The data files are scripts, not JSON, so the page also works opened from disk (file://), where
browsers block fetch() but still run <script src>.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "docs" / "OOO" / "OBR" / "spawn-danger"
REL_PREFIX = "window.SD_RELEASES = "


def read_data(html: str) -> dict:
    m = re.search(r"^const DATA = (\{.*\});\s*$", html, re.M)
    if not m:
        raise SystemExit("no `const DATA = {...};` line in the heatmap page")
    return json.loads(m.group(1))


def write_data(key: str, obj) -> None:
    js = ("(window.SD_DATA = window.SD_DATA || {})[" + json.dumps(key) + "] = "
          + json.dumps(obj, separators=(",", ":")) + ";\n")
    (OUT / f"{key}.js").write_text(js, encoding="utf-8", newline="\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("heatmap")
    ap.add_argument("tag")
    ap.add_argument("--date", required=True, help="date the heatmap was built")
    ap.add_argument("--source", default="", help="the plugins the load order had (shown on the page)")
    a = ap.parse_args()
    data = read_data(Path(a.heatmap).read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    write_data(a.tag, data["OOO"])
    if "Vanilla" in data:
        write_data("vanilla", data["Vanilla"])
    idx = OUT / "releases.js"
    rel = []
    if idx.exists():
        t = idx.read_text(encoding="utf-8").strip()
        rel = json.loads(t[len(REL_PREFIX):].rstrip(";"))
    rel = [r for r in rel if r["tag"] != a.tag]
    rel.insert(0, {"tag": a.tag, "date": a.date, "source": a.source})
    idx.write_text(REL_PREFIX + json.dumps(rel, indent=1) + ";\n", encoding="utf-8", newline="\n")
    print(f"{a.tag}: {data['OOO']['points']} spawn points, {len(data['OOO']['lists'])} lists; "
          f"releases: {', '.join(r['tag'] for r in rel)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
