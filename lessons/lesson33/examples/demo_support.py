"""Shared infrastructure: temporary files, PostgreSQL lifecycle and request sessions."""

import os
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import dotenv_values
from fastapi import Request
from lab_support import event
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


def runtime_file(name):
    folder = Path(
        os.environ.get(
            "LESSON33_WORKDIR",
            Path(__file__).resolve().parents[1] / ".runtime" / "manual",
        )
    )
    folder.mkdir(parents=True, exist_ok=True)
    return folder / name


def database_lifespan(base):
    @asynccontextmanager
    async def lifespan(app):
        values = dotenv_values(Path(__file__).resolve().parents[1] / ".env")
        url = values.get("DATABASE_URL", "")
        if not url or make_url(url).database != "lesson33":
            raise RuntimeError(
                "Configure lesson33/.env for the lesson33 database"
            )
        schema = "demo_" + uuid.uuid4().hex
        admin = create_async_engine(url)
        engine = None
        try:
            async with admin.begin() as connection:
                await connection.execute(text(f'CREATE SCHEMA "{schema}"'))
            engine = create_async_engine(
                url, connect_args={"server_settings": {"search_path": schema}}
            )
            async with engine.begin() as connection:
                await connection.run_sync(base.metadata.create_all)
            app.state.sessions = async_sessionmaker(
                engine, expire_on_commit=False
            )
            event("log", "lifespan", "STARTUP: real PostgreSQL tables ready")
            yield
        finally:
            try:
                if engine is not None:
                    await engine.dispose()
                async with admin.begin() as connection:
                    await connection.execute(
                        text(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE')
                    )
            finally:
                await admin.dispose()
            event(
                "log",
                "lifespan",
                "SHUTDOWN: connections closed; demo schema removed",
            )

    return lifespan


async def get_db(request: Request):
    async with request.app.state.sessions() as session:
        yield session
