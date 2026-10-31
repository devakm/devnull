#!/usr/bin/env python3
r"""Add one OOORF release to the Spawn Danger page (docs/OOO/OBR/spawn-danger.html).

    python scripts/add_spawn_danger_release.py <ooo-spawn-heatmap.html> <tag> --date YYYY-MM-DD \
        --source "<the plugins in the load order that change creatures or leveled lists>"

<ooo-spawn-heatmap.html> is the page RAX's tools/spawnlog/spawn_heatmap.py builds, from a load
order with that release installed. This writes its OOO data to spawn-danger/<tag>.json and its
vanilla data to spawn-danger/vanilla.json, and puts the release first in spawn-danger/releases.json
(the page opens the first entry). Running it again for the same tag replaces that entry.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "docs" / "OOO" / "OBR" / "spawn-danger"


def read_data(html: str) -> dict:
    m = re.search(r"^const DATA = (\{.*\});\s*$", html, re.M)
    if not m:
        raise SystemExit("no `const DATA = {...};` line in the heatmap page")
    return json.loads(m.group(1))


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, separators=(",", ":")), encoding="utf-8", newline="\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("heatmap")
    ap.add_argument("tag")
    ap.add_argument("--date", required=True, help="date the heatmap was built")
    ap.add_argument("--source", default="", help="the plugins the load order had (shown on the page)")
    a = ap.parse_args()
    data = read_data(Path(a.heatmap).read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    write_json(OUT / f"{a.tag}.json", data["OOO"])
    if "Vanilla" in data:
        write_json(OUT / "vanilla.json", data["Vanilla"])
    idx = OUT / "releases.json"
    rel = json.loads(idx.read_text(encoding="utf-8")) if idx.exists() else []
    rel = [r for r in rel if r["tag"] != a.tag]
    rel.insert(0, {"tag": a.tag, "date": a.date, "file": f"{a.tag}.json", "source": a.source})
    idx.write_text(json.dumps(rel, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"{a.tag}: {data['OOO']['points']} spawn points, {len(data['OOO']['lists'])} lists; "
          f"releases: {', '.join(r['tag'] for r in rel)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
