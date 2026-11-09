import sqlite3


def demo(work):
    with sqlite3.connect(work / "init.sqlite3") as database:
        database.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY)")
        for _ in range(2):
            database.execute("INSERT OR IGNORE INTO users VALUES (?)", ("admin",))
        count = database.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    assert count == 1
    return {"local_initializations": 2, "admin_count": count}
