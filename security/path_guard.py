import os
from config import load_config

_cfg = load_config()

def safe_file_path(user_path: str) -> str:
    if not user_path or "\x00" in user_path:
        raise ValueError("Некорректный путь")

    base = _cfg.storage_dir
    target = os.path.abspath(os.path.join(base, user_path))

    if target != base and not target.startswith(base + os.sep):
        raise ValueError("Path Traversal: выход за пределы хранилища")

    return target