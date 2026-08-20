import sqlite3
from functools import wraps
from pathlib import Path
from typing import Any


def sql_row_counter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        cursor, outcome_or_type = func(*args, **kwargs)

        if outcome_or_type == "executemany":
            print(
                f"[LOG] Mass operation (executemany) modified rows: {cursor.rowcount}"
            )
            return None
        elif outcome_or_type == "execute_modify":
            print(f"[LOG] Operation (execute) modified rows: {cursor.rowcount}")
            return None
        elif (
            isinstance(outcome_or_type, tuple)
            and outcome_or_type[0] == "create_table"
        ):
            _, table_name, columns_count = outcome_or_type

            print(
                f"[LOG] Table '{table_name}' created with "
                f"{columns_count} columns."
            )
            return None
        else:
            print(f"[LOG] SELECT query returned rows: {len(outcome_or_type)}")
            return outcome_or_type

    return wrapper


@sql_row_counter
def sql_query_executioner(
    query: str,
    params: tuple[Any, ...]
    | list[Any]
    | list[tuple[Any, ...]]
    | list[list[Any]]
    | dict[str, Any]
    | list[dict[str, Any]],
    db_path: str | Path | None = None,
) -> list[Any]:
    if db_path is None:
        raise ValueError("db_path must be provided")

    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()

        query_clean = query.strip()
        if query_clean.startswith("--sql"):
            query_clean = query_clean[5:].strip()

        if (
            isinstance(params, list)
            and len(params) > 0
            and isinstance(params[0], (list, tuple, dict))
        ):
            cursor.executemany(query_clean, params)
            connection.commit()
            return cursor, "executemany"

        else:
            cursor.execute(query_clean, params)

            if query_clean.strip().upper().startswith("SELECT"):
                data = cursor.fetchall()
                return cursor, data

            elif query_clean.strip().upper().startswith("CREATE TABLE"):
                connection.commit()

                parts = query_clean.split()

                if parts[2].upper() == "IF":
                    table_name = parts[5]
                else:
                    table_name = parts[2]

                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()

                return cursor, ("create_table", table_name, len(columns))

            else:
                connection.commit()
                return cursor, "execute_modify"
