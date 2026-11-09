import os
import sqlite3


def demo(work):
    with sqlite3.connect(":memory:") as db:
        value = db.execute("SELECT 1").fetchone()[0]
    assert value == 1
    return {"database": "SQLite local probe", "query": "SELECT 1", "value": value}


if __name__ == "__main__":
    import psycopg
    with psycopg.connect(os.environ["DATABASE_URL"], connect_timeout=5) as db:
        print(db.execute("SELECT 1").fetchone()[0])
