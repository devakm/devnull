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


def test_control_chars_flags_stray_byte():
    # The exact corruption class that broke the nav: a SOH (U+0001) byte.
    assert chk.control_chars("ok\x01ok") == [(2, 1)]


def test_control_chars_allows_tab_newline_cr():
    assert chk.control_chars("a\tb\nc\r\n") == []


def test_malformed_nav_flags_dropped_opening_tag():
    # `>Changelog</a>` has no opening <a — exactly the live bug.
    nav = '<nav><a href="a.html">A</a> | >Changelog</a> | <a href="c.html">C</a></nav>'
    assert chk.malformed_nav(nav) != []


def test_wellformed_nav_passes():
    nav = ('<nav><a href="a.html">Home</a> | <a href="b.html" class="x">B</a> | '
           '<a href="https://e.test" target="_blank" rel="noopener">Downloads (x)</a></nav>')
    assert chk.malformed_nav(nav) == []


def test_no_nav_is_not_an_error():
    assert chk.malformed_nav("<html><body>no nav here</body></html>") == []


def test_page_problems_aggregates():
    bad = '<nav><a href="a.html">A</a> | \x01>B</a></nav>'  # no marker, ctrl byte, bad nav
    problems = chk.page_problems(bad)
    assert any("marker" in p for p in problems)
    assert any("control character" in p for p in problems)
    assert any("malformed nav" in p for p in problems)
