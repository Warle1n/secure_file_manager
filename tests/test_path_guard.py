import pytest
from security.path_guard import safe_file_path

def test_normal_path():
    p = safe_file_path("note.txt")
    assert p.endswith("note.txt")

def test_traversal_blocked():
    with pytest.raises(ValueError):
        safe_file_path("../../etc/passwd")

def test_absolute_blocked():
    with pytest.raises(ValueError):
        safe_file_path("/etc/passwd")

def test_null_byte_blocked():
    with pytest.raises(ValueError):
        safe_file_path("a\x00b")