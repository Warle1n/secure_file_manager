import os
import shutil
from security.validators import validate_size

DEFAULT_ENCODING = "utf-8"

def read_file_text(path: str) -> str:
    with open(path, "r", encoding=DEFAULT_ENCODING) as f:
        return f.read()

def write_file_text(path: str, text: str) -> None:
    data = text.encode(DEFAULT_ENCODING)
    validate_size(len(data))
    with open(path, "w", encoding=DEFAULT_ENCODING) as f:
        f.write(text)

def read_file_binary(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()

def write_file_binary(path: str, data: bytes) -> None:
    validate_size(len(data))
    with open(path, "wb") as f:
        f.write(data)

def delete_file(path: str) -> None:
    if os.path.isdir(path):
        raise ValueError("Это каталог, а не файл")
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    os.remove(path)

def copy_file(src: str, dst: str) -> None:
    shutil.copy2(src, dst)

def move_file(src: str, dst: str) -> None:
    shutil.move(src, dst)

def file_size(path: str) -> int:
    return os.path.getsize(path)

def append_file_text(path: str, text: str) -> None:
    data = text.encode(DEFAULT_ENCODING)
    validate_size(len(data))
    with open(path, "a", encoding=DEFAULT_ENCODING) as f: 
        f.write(text)