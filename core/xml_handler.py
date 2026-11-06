from defusedxml import ElementTree as DefusedET
from security.validators import validate_size
import os

def load_xml(path: str):
    validate_size(os.path.getsize(path))
    return DefusedET.parse(path).getroot()

def xml_to_dict(elem) -> dict:
    result = {"tag": elem.tag, "attrib": dict(elem.attrib), "children": []}
    if elem.text and elem.text.strip():
        result["text"] = elem.text.strip()
    for child in elem:
        result["children"].append(xml_to_dict(child))
    return result

def save_xml(path: str, root_elem) -> None:
    tree = DefusedET.ElementTree(root_elem)
    tree.write(path, encoding="utf-8", xml_declaration=True)