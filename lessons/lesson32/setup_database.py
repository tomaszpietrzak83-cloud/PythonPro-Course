"""Create only the lesson32 database and save local, ignored credentials."""
from pathlib import Path

import psycopg2
from dotenv import dotenv_values
from sqlalchemy import URL

ROOT = Path(__file__).resolve().parent


def main():
    source = ROOT.parent / 'lesson28' / '.env'
    values = dotenv_values(source)
    connection = psycopg2.connect(
        host=values['POSTGRES_HOST'], port=values['POSTGRES_PORT'],
        user=values['POSTGRES_USER'], password=values['POSTGRES_PASSWORD'],
        dbname='postgres', connect_timeout=5,
    )
    connection.autocommit = True
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1 FROM pg_database WHERE datname = %s', ('lesson32',))
            if cursor.fetchone() is None:
                cursor.execute('CREATE DATABASE lesson32')
    finally:
        connection.close()
    target = ROOT / '.env'
    if not target.exists():
        url = URL.create('postgresql+asyncpg', username=values['POSTGRES_USER'],
                         password=values['POSTGRES_PASSWORD'],
                         host=values['POSTGRES_HOST'], port=int(values['POSTGRES_PORT']),
                         database='lesson32').render_as_string(hide_password=False)
        # python-dotenv single quoted values preserve literal dollar signs.
        escaped = url.replace('\\', '\\\\').replace("'", "\\'")
        target.write_text("DATABASE_URL='" + escaped + "'\n", encoding='utf-8')
    print('lesson32 database ready; local configuration saved without displaying credentials.')


if __name__ == '__main__':
    main()
