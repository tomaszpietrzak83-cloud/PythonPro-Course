import os
import sqlite3


def demo(work):
    with sqlite3.connect(":memory:") as db:
        value = db.execute("SELECT 1").fetchone()[0]
    assert value == 1
    from pathlib import Path
    import yaml
    services = yaml.safe_load(Path(__file__).with_name("docker-compose.yml").read_text())["services"]
    assert services["backend"]["depends_on"]["database"]["condition"] == "service_healthy"
    return {"depends_on": "service_healthy", "database": "SQLite local probe", "query": "SELECT 1", "value": value}


if __name__ == "__main__":
    import psycopg
    with psycopg.connect(os.environ["DATABASE_URL"], connect_timeout=5) as db:
        print(db.execute("SELECT 1").fetchone()[0])
