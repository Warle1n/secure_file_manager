import os
import pytest

from security.path_guard import safe_file_path


def test_normal_path_is_allowed(tmp_path):
    base = str(tmp_path)
    result = safe_file_path(base, "file.txt")
    assert result == os.path.join(base, "file.txt")


def test_path_traversal_is_blocked(tmp_path):
    base = str(tmp_path)
    with pytest.raises((ValueError, PermissionError)):
        safe_file_path(base, "../etc/passwd")


def test_absolute_path_is_blocked(tmp_path):
    base = str(tmp_path)
    with pytest.raises((ValueError, PermissionError)):
        safe_file_path(base, "/etc/passwd")


def test_deep_traversal_is_blocked(tmp_path):
    base = str(tmp_path)
    with pytest.raises((ValueError, PermissionError)):
        safe_file_path(base, "../../../../etc/shadow")
