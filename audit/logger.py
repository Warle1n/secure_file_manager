from db.queries import insert_operation, get_user_operations


def log_operation(user_id: int, file_id: int | None, op_type: str) -> None:
    if op_type not in ("create", "modify", "delete", "read"):
        raise ValueError("Недопустимый тип операции")
    insert_operation(user_id, file_id, op_type)


def print_audit_log(user_id: int) -> None:
    rows = get_user_operations(user_id)
    print("\n--- Журнал операций ---")
    if not rows:
        print("Операций нет.")
        return
    for r in rows:
        fname = r["filename"] or "—"
        print(
            f"{r['timestamp']:%Y-%m-%d %H:%M:%S}  "
            f"{r['operation_type']:<8}  файл: {fname}"
        )