import pytest
from core.xml_handler import load_xml

def test_xxe_blocked(tmp_path):
    payload = """<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<foo>&xxe;</foo>"""
    p = tmp_path / "evil.xml"
    p.write_text(payload, encoding="utf-8")
    with pytest.raises(Exception):
        load_xml(str(p))