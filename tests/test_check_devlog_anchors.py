import importlib.util
from pathlib import Path

_MODULE_PATH = Path(__file__).resolve().parent.parent / "scripts" / "check_devlog_anchors.py"
_spec = importlib.util.spec_from_file_location("check_devlog_anchors", _MODULE_PATH)
chk = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(chk)


def test_all_anchors_resolve():
    html = '<a class="arc-card" href="#a91-water">x</a><div id="a91-water"></div>'
    assert chk.unresolved_anchors(html) == []


def test_missing_target_is_flagged():
    html = '<a class="arc-card" href="#a91-fire">x</a><div id="a91-water"></div>'
    assert chk.unresolved_anchors(html) == ["a91-fire"]


def test_external_and_plain_links_ignored():
    html = '<a href="changelog.html#alpha91">c</a><a href="https://x.test#frag">e</a>'
    # Only same-page #fragment links are checked; these have a path/host, so ignored.
    assert chk.unresolved_anchors(html) == []


def test_name_attribute_also_satisfies_target():
    html = '<a href="#top">t</a><a name="top"></a>'
    assert chk.unresolved_anchors(html) == []


def test_marker_present_detection():
    assert chk.has_marker("<!-- DO-NOT-REGENERATE: x -->") is True
    assert chk.has_marker("<html>") is False
