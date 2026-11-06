from db.connection import get_cursor


# ---------- Users ----------

def get_or_create_user(username: str) -> int:
    with get_cursor() as cur:
        cur.execute("SELECT id FROM Users WHERE username = %s", (username,))
        row = cur.fetchone()
        if row:
            return row[0]
        cur.execute(
            "INSERT INTO Users (username) VALUES (%s) RETURNING id",
            (username,),
        )
        return cur.fetchone()[0]


# ---------- Files ----------

def create_file_record(filename: str, size: int, location: str, owner_id: int) -> int:
    with get_cursor() as cur:
        cur.execute(
            "INSERT INTO Files (filename, size, location, owner_id) "
            "VALUES (%s, %s, %s, %s) RETURNING id",
            (filename, size, location, owner_id),
        )
        return cur.fetchone()[0]


def get_file_record(file_id: int):
    with get_cursor(dict_cursor=True) as cur:
        cur.execute(
            "SELECT id, filename, size, location, owner_id FROM Files WHERE id = %s",
            (file_id,),
        )
        return cur.fetchone()


def find_file_by_location(location: str, owner_id: int):
    with get_cursor(dict_cursor=True) as cur:
        cur.execute(
            "SELECT id, filename, size, location, owner_id "
            "FROM Files WHERE location = %s AND owner_id = %s",
            (location, owner_id),
        )
        return cur.fetchone()


def list_user_files(owner_id: int):
    with get_cursor(dict_cursor=True) as cur:
        cur.execute(
            "SELECT id, filename, size, location, created_at "
            "FROM Files WHERE owner_id = %s ORDER BY created_at DESC",
            (owner_id,),
        )
        return cur.fetchall()


def update_file_record(file_id: int, size: int) -> None:
    with get_cursor() as cur:
        cur.execute(
            "UPDATE Files SET size = %s WHERE id = %s",
            (size, file_id),
        )


def delete_file_record(file_id: int) -> None:
    with get_cursor() as cur:
        cur.execute("DELETE FROM Files WHERE id = %s", (file_id,))


# ---------- Operations ----------

def insert_operation(user_id: int, file_id: int | None, op_type: str) -> None:
    with get_cursor() as cur:
        cur.execute(
            "INSERT INTO Operations (user_id, file_id, operation_type) "
            "VALUES (%s, %s, %s)",
            (user_id, file_id, op_type),
        )


def get_user_operations(user_id: int, limit: int = 50):
    with get_cursor(dict_cursor=True) as cur:
        cur.execute(
            "SELECT o.id, o.timestamp, o.operation_type, f.filename "
            "FROM Operations o "
            "LEFT JOIN Files f ON f.id = o.file_id "
            "WHERE o.user_id = %s "
            "ORDER BY o.timestamp DESC LIMIT %s",
            (user_id, limit),
        )
        return cur.fetchall()