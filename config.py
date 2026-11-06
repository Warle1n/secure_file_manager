import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    database_dsn: str
    storage_dir: str
    max_file_size: int
    max_unzip_size: int

def load_config() -> Config:
    dsn = os.getenv("DATABASE_DSN")
    if not dsn:
        raise RuntimeError("DATABASE_DSN не задан в .env")

    storage_dir = os.path.abspath(os.getenv("STORAGE_DIR", "./storage"))
    os.makedirs(storage_dir, exist_ok=True)

    return Config(
        database_dsn=dsn,
        storage_dir=storage_dir,
        max_file_size=int(os.getenv("MAX_FILE_SIZE", "10485760")),
        max_unzip_size=int(os.getenv("MAX_UNZIP_SIZE", "104857600")),
    )