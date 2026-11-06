import os
import pytest


@pytest.mark.skipif(
    not os.getenv("TEST_DATABASE_DSN"),
    reason="TEST_DATABASE_DSN не задан",
)
def test_sql_injection_safe():
    from db.connection import init_pool, close_pool
    from db.queries import get_or_create_user

    init_pool(os.environ["TEST_DATABASE_DSN"])
    try:
        evil = "admin' OR '1'='1"
        uid = get_or_create_user(evil)
        uid2 = get_or_create_user(evil)
        assert uid == uid2  # одна и та же запись, а не чужая
    finally:
        close_pool()