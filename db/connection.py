from contextlib import contextmanager
from psycopg2 import pool
from psycopg2.extras import RealDictCursor

_pool: pool.SimpleConnectionPool | None = None

def init_pool(dsn: str) -> None:
    global _pool
    _pool = pool.SimpleConnectionPool(minconn=1, maxconn=5, dsn=dsn)

def close_pool() -> None:
    global _pool
    if _pool:
        _pool.closeall()
        _pool = None

@contextmanager
def get_cursor(dict_cursor: bool = False):
    if _pool is None:
        raise RuntimeError("Пул соединений не инициализирован")
    conn = _pool.getconn()
    try:
        cursor_factory = RealDictCursor if dict_cursor else None
        with conn.cursor(cursor_factory=cursor_factory) as cur:
            yield cur
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        _pool.putconn(conn)