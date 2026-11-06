from db.queries import get_or_create_user
from cli.file_menu import (
    file_menu_loop, json_submenu, xml_submenu, zip_submenu,
)
from core.disk_info import show_disks
from audit.logger import print_audit_log


def run_main_menu(cfg):
    print("=== Secure File Manager (CLI) ===")
    print(f"Хранилище: {cfg.storage_dir}")

    username = input("Введите имя пользователя: ").strip()
    if not username:
        print("Имя не задано, выход.")
        return

    user_id = get_or_create_user(username)
    user = {"id": user_id, "username": username}

    while True:
        print(f"\nПользователь: {user['username']}")
        print("1. Список дисков")
        print("2. Работа с файлами")
        print("3. JSON")
        print("4. XML")
        print("5. ZIP-архивы")
        print("6. Журнал операций")
        print("7. Список файлов в БД")
        print("0. Выход")
        choice = input("Выбор: ").strip()

        if choice == "0":
            print("До свидания.")
            return
        elif choice == "1":
            show_disks()
        elif choice == "2":
            file_menu_loop(user)
        elif choice == "3":
            json_submenu(user)
        elif choice == "4":
            xml_submenu(user)
        elif choice == "5":
            zip_submenu(user)
        elif choice == "6":
            print_audit_log(user["id"])
        elif choice == "7":
            from db.queries import list_user_files
            rows = list_user_files(user["id"])
            print("\n--- Файлы в БД ---")
            if not rows:
                print("Записей нет.")
            for r in rows:
                print(
                    f"[{r['id']}] {r['filename']}  "
                    f"{r['size']} байт  {r['location']}"
                )
        else:
            print("Неверный выбор.")