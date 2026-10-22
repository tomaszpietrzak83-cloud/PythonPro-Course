"""Real local HTTP observation and isolated PostgreSQL schemas for demonstrations."""
import asyncio
import json
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from aiohttp import ClientSession, ClientTimeout, web
from dotenv import dotenv_values
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from lab_support import event, metric, span

SESSION = web.AppKey('session_factory', async_sessionmaker)


@asynccontextmanager
async def database(base):
    values = dotenv_values(Path(__file__).resolve().parents[1] / '.env')
    url = values.get('DATABASE_URL')
    if not url or not url.rsplit('/', 1)[-1] == 'lesson32':
        raise RuntimeError('Configure lesson32/.env with the lesson32 database first')
    schema = 'demo_' + uuid.uuid4().hex
    admin = create_async_engine(url)
    engine = None
    try:
        async with admin.begin() as connection:
            await connection.execute(text(f'CREATE SCHEMA "{schema}"'))
        engine = create_async_engine(url, connect_args={'server_settings': {'search_path': schema}})
        async with engine.begin() as connection:
            await connection.run_sync(base.metadata.create_all)
        event('log', 'database', 'Fresh isolated schema; real PostgreSQL')
        yield async_sessionmaker(engine, expire_on_commit=False)
    finally:
        if engine is not None:
            await engine.dispose()
        async with admin.begin() as connection:
            await connection.execute(text(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE'))
        await admin.dispose()
        event('log', 'database', 'Demo schema removed; connections closed')


@asynccontextmanager
async def server(app):
    runner = web.AppRunner(app)
    await runner.setup()
    try:
        site = web.TCPSite(runner, '127.0.0.1', 0)
        await site.start()
        host, port = runner.addresses[0]
        event('log', 'server', f'Listening on {host}:{port}')
        yield f'http://127.0.0.1:{port}'
    finally:
        await runner.cleanup()
        event('log', 'server', 'Server stopped')


async def request(client, method, url, data=None, expected=200):
    with span(method + ' ' + url.split('/')[-1], 'HTTP request'):
        event('log', 'client', f'{method} {url}; JSON={data}',
              http_method=method, http_url=url, request_body=data)
        async with client.request(method, url, json=data) as response:
            body = await response.text()
            event('log', 'response', f'{response.status}: {body}',
                  http_method=method, http_url=url, http_status=response.status,
                  response_body=body, content_type=response.content_type)
            if response.status != expected:
                raise AssertionError(f'Expected {expected}, received {response.status}: {body}')
            metric('HTTP status', response.status)
            return json.loads(body) if response.content_type == 'application/json' else body


async def demo(app, cases):
    async with server(app) as url:
        async with ClientSession(timeout=ClientTimeout(total=15)) as client:
            for method, path, data, expected in cases:
                await request(client, method, url + path, data, expected)


async def object_json(request):
    try:
        data = await request.json()
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise web.HTTPBadRequest(text='Invalid JSON')
    if not isinstance(data, dict):
        raise web.HTTPBadRequest(text='Expected a JSON object')
    return data


def product_fields(data, partial=False):
    if set(data) - {'name', 'price'} or not data:
        raise web.HTTPBadRequest(text='Use name and price fields')
    if not partial and not {'name', 'price'} <= data.keys():
        raise web.HTTPBadRequest(text='name and price are required')
    if 'name' in data and (not isinstance(data['name'], str) or not data['name'].strip() or len(data['name']) > 100):
        raise web.HTTPBadRequest(text='name must contain 1..100 characters')
    if 'price' in data and (type(data['price']) is not int or not 0 <= data['price'] <= 2147483647):
        raise web.HTTPBadRequest(text='price must be integer cents, 0..2147483647')
    return data


def positive_id(value):
    try:
        number = int(value)
    except ValueError:
        raise web.HTTPBadRequest(text='ID must be an integer')
    if number < 1:
        raise web.HTTPBadRequest(text='ID must be positive')
    return number
