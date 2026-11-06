import json
from security.validators import validate_size

def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
    validate_size(len(data.encode("utf-8")))
    return json.loads(data)

def save_json(path: str, obj, pretty: bool = True) -> None:
    text = json.dumps(
        obj,
        ensure_ascii=False,
        indent=2 if pretty else None,
    )
    validate_size(len(text.encode("utf-8")))
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)