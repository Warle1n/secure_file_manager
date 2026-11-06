import os
import zipfile
from safezip import safe_extract
from config import load_config

_cfg = load_config()

def create_zip(archive_path: str, files: list[str]) -> None:
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            if not os.path.isfile(f):
                raise FileNotFoundError(f)
            zf.write(f, arcname=os.path.basename(f))

def extract_zip(archive_path: str, dest_dir: str) -> None:
    """Безопасная распаковка: защита от Zip Slip и Zip-бомб."""
    os.makedirs(dest_dir, exist_ok=True)
    safe_extract(
        archive_path,
        dest_dir,
        max_total_size=_cfg.max_unzip_size,
    )

def list_zip(archive_path: str) -> list[tuple[str, int]]:
    with zipfile.ZipFile(archive_path, "r") as zf:
        return [(i.filename, i.file_size) for i in zf.infolist()]