import os
import zipfile
import pytest
from core.zip_handler import create_zip, extract_zip

def test_zip_roundtrip(tmp_path):
    src = tmp_path / "a.txt"
    src.write_text("hello", encoding="utf-8")
    arc = tmp_path / "a.zip"
    create_zip(str(arc), [str(src)])

    dest = tmp_path / "out"
    extract_zip(str(arc), str(dest))
    assert (dest / "a.txt").read_text(encoding="utf-8") == "hello"

def test_zip_slip_blocked(tmp_path):
    arc = tmp_path / "evil.zip"
    with zipfile.ZipFile(arc, "w") as zf:
        zf.writestr("../../evil.txt", "pwned")
    dest = tmp_path / "out"
    with pytest.raises(Exception):
        extract_zip(str(arc), str(dest))