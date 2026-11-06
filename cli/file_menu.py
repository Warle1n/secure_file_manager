import os
import json as jsonlib

from core.file_ops import (
    read_file_text, write_file_text, append_file_text,
    delete_file, copy_file, move_file, file_size,
)
from core.json_handler import load_json, save_json
from core.xml_handler import load_xml, xml_to_dict, save_xml
from core.zip_handler import create_zip, extract_zip, list_zip
from security.path_guard import safe_file_path
from security.validators import validate_filename, validate_extension
from audit.logger import log_operation
from db.queries import (
    create_file_record, find_file_by_location,
    delete_file_record, update_file_record,
)
from xml.etree.ElementTree import Element


def _register_file(user_id: int, path: str, op_type: str) -> int:
    """Создаёт или обновляет запись о файле и возвращает file_id."""
    existing = find_file_by_location(path, user_id)
    if existing:
        update_file_record(existing["id"], file_size(path))
        fid = existing["id"]
    else:
        fid = create_file_record(
            filename=os.path.basename(path),
            size=file_size(path),
            location=path,
            owner_id=user_id,
        )
    log_operation(user_id, fid, op_type)
    return fid


def file_menu_loop(user):
    while True:
        print("\n--- Файлы ---")
        print("1. Прочитать файл")
        print("2. Записать в файл")
        print("3. Удалить файл")
        print("4. Копировать файл")
        print("5. Переместить файл")
        print("6. Дописать в файл")
        print("0. Назад")
        choice = input("Выбор: ").strip()

        if choice == "0":
            return

        try:
            if choice == "1":
                path = safe_file_path(input("Путь: ").strip())
                print(read_file_text(path))
                _register_file(user["id"], path, "read")

            elif choice == "2":
                name = input("Имя файла: ").strip()
                validate_filename(name)
                validate_extension(name)
                path = safe_file_path(name)
                text = input("Текст: ")
                write_file_text(path, text)
                _register_file(user["id"], path, "create")
                print("Записано.")

            elif choice == "3":
                path = safe_file_path(input("Путь: ").strip())
                existing = find_file_by_location(path, user["id"])
                delete_file(path)
                if existing:
                    log_operation(user["id"], existing["id"], "delete")
                    delete_file_record(existing["id"])
                print("Удалено.")

            elif choice == "4":
                src = safe_file_path(input("Откуда: ").strip())
                dst = safe_file_path(input("Куда: ").strip())
                copy_file(src, dst)
                _register_file(user["id"], dst, "create")
                print("Скопировано.")

            elif choice == "5":
                src = safe_file_path(input("Откуда: ").strip())
                dst = safe_file_path(input("Куда: ").strip())
                move_file(src, dst)
                existing = find_file_by_location(src, user["id"])
                if existing:
                    update_file_record(existing["id"], file_size(dst))
                    log_operation(user["id"], existing["id"], "modify")
                else:
                    _register_file(user["id"], dst, "modify")
                print("Перемещено.")

            elif choice == "6":
                path = safe_file_path(input("Путь: ").strip())
                text = input("Текст: ")
                append_file_text(path, text)
                _register_file(user["id"], path, "modify")
                print("Дописано.")

            else:
                print("Неверный выбор.")
        except Exception as e:
            print(f"Ошибка: {e}")


def json_submenu(user):
    try:
        print("1. Прочитать JSON")
        print("2. Записать JSON")
        action = input("Выбор: ").strip()

        if action == "1":
            path = safe_file_path(input("Путь к JSON: ").strip())
            data = load_json(path)
            print(data)
            _register_file(user["id"], path, "read")

        elif action == "2":
            name = input("Имя файла: ").strip()
            validate_filename(name)
            if not name.lower().endswith(".json"):
                raise ValueError("Файл должен иметь расширение .json")
            path = safe_file_path(name)
            raw = input("JSON-строка: ")
            obj = jsonlib.loads(raw)
            save_json(path, obj)
            _register_file(user["id"], path, "create")
            print("JSON сохранён.")
    except Exception as e:
        print(f"Ошибка: {e}")


def xml_submenu(user):
    try:
        print("1. Прочитать XML")
        print("2. Показать как dict")
        print("3. Записать XML")
        action = input("Выбор: ").strip()

        if action == "1":
            path = safe_file_path(input("Путь к XML: ").strip())
            root = load_xml(path)
            print(f"Корневой тег: {root.tag}, дочерних элементов: {len(list(root))}")
            _register_file(user["id"], path, "read")

        elif action == "2":
            path = safe_file_path(input("Путь к XML: ").strip())
            root = load_xml(path)
            print(xml_to_dict(root))
            _register_file(user["id"], path, "read")

        elif action == "3":
            name = input("Имя файла (.xml): ").strip()
            validate_filename(name)
            if not name.lower().endswith(".xml"):
                raise ValueError("Файл должен иметь расширение .xml")
            root_tag = input("Корневой тег: ").strip()
            if not root_tag:
                raise ValueError("Корневой тег не задан")
            root = Element(root_tag)
            while True:
                key = input("Дочерний тег (пусто — закончить): ").strip()
                if not key:
                    break
                val = input(f"Значение для <{key}>: ")
                child = Element(key)
                child.text = val
                root.append(child)
            path = safe_file_path(name)
            save_xml(path, root)
            _register_file(user["id"], path, "create")
            print("XML сохранён.")
    except Exception as e:
        print(f"Ошибка: {e}")


def zip_submenu(user):
    try:
        print("1. Создать архив")
        print("2. Распаковать архив")
        print("3. Список содержимого")
        action = input("Выбор: ").strip()

        if action == "1":
            arc_name = input("Имя архива (.zip): ").strip()
            validate_filename(arc_name)
            if not arc_name.lower().endswith(".zip"):
                raise ValueError("Архив должен иметь расширение .zip")
            arc_path = safe_file_path(arc_name)
            files = input("Файлы через запятую: ").split(",")
            files = [safe_file_path(f.strip()) for f in files if f.strip()]
            create_zip(arc_path, files)
            _register_file(user["id"], arc_path, "create")
            print("Архив создан.")

        elif action == "2":
            arc_path = safe_file_path(input("Путь к архиву: ").strip())
            dest = safe_file_path(input("Куда распаковать: ").strip())
            extract_zip(arc_path, dest)
            _register_file(user["id"], arc_path, "read")
            print("Распаковано.")

        elif action == "3":
            arc_path = safe_file_path(input("Путь к архиву: ").strip())
            for name, size in list_zip(arc_path):
                print(f"  {name}  ({size} байт)")
            _register_file(user["id"], arc_path, "read")
    except Exception as e:
        print(f"Ошибка: {e}")