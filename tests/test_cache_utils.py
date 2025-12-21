import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cache_utils import ids_need_refresh


def test_ids_need_refresh_first_load():
    assert ids_need_refresh({}, "file1.out", "node") is True


def test_ids_need_refresh_when_file_changes():
    state = {"ids": ["a"], "last_file": "old.out", "last_item_type": "node"}
    assert ids_need_refresh(state, "new.out", "node") is True


def test_ids_need_refresh_when_element_type_changes():
    state = {"ids": ["a"], "last_file": "file.out", "last_item_type": "node"}
    assert ids_need_refresh(state, "file.out", "link") is True


def test_ids_need_refresh_when_cache_valid():
    state = {"ids": ["a"], "last_file": "file.out", "last_item_type": "node"}
    assert ids_need_refresh(state, "file.out", "node") is False
