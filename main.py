from config import load_config
from db.connection import init_pool, close_pool
from cli.menu import run_main_menu


def main():
    cfg = load_config()
    init_pool(cfg.database_dsn)
    try:
        run_main_menu(cfg)
    finally:
        close_pool()


if __name__ == "__main__":
    main()