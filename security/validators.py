from config import load_config

_cfg = load_config()

ALLOWED_EXTENSIONS = {
    ".txt", ".json", ".xml", ".zip",
    ".log", ".csv", ".dat",
}

def validate_filename(name: str) -> None:
    if not name or len(name) > 255:
        raise ValueError("Некорректное имя файла")
    if any(c in name for c in ("/", "\\", "\x00")):
        raise ValueError("Имя файла содержит запрещённые символы")

def validate_extension(name: str) -> None:
    _, ext = _split_ext(name)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Расширение {ext} не разрешено")

def validate_size(size: int) -> None:
    if size > _cfg.max_file_size:
        raise ValueError(
            f"Размер файла превышает лимит {_cfg.max_file_size} байт"
        )

def _split_ext(name: str) -> tuple[str, str]:
    idx = name.rfind(".")
    if idx == -1:
        return name, ""
    return name[:idx], name[idx:]