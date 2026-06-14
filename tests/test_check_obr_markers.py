import importlib.util
from pathlib import Path

_MODULE_PATH = Path(__file__).resolve().parent.parent / "scripts" / "check_obr_markers.py"
_spec = importlib.util.spec_from_file_location("check_obr_markers", _MODULE_PATH)
check = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check)


def test_find_unmarked_flags_missing_marker():
    content = {
        "docs/OOO/OBR/overview.html": "<!DOCTYPE html>\n<!-- DO-NOT-REGENERATE -->\n",
        "docs/OOO/OBR/index.html": "<!DOCTYPE html>\n<html></html>",
    }
    unmarked = check.find_unmarked(list(content), content.get)
    assert unmarked == ["docs/OOO/OBR/index.html"]


def test_find_unmarked_empty_when_all_marked():
    content = {"docs/OOO/OBR/a.html": "x DO-NOT-REGENERATE y"}
    assert check.find_unmarked(list(content), content.get) == []
