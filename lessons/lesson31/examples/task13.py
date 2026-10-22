import asyncio
from lab_support import config, event, launch, metric, span

async def handle_client(reader, writer):
    with span("server", "echo"):
        try:
            data = await reader.readline()
            writer.write(data)
            await writer.drain()
            event("log", "server", repr(data))
        finally:
            writer.close()
            await writer.wait_closed()

async def main():
    port = config().get("port", 0)
    server = await asyncio.start_server(handle_client, "127.0.0.1", port)
    async with server:
        actual_port = server.sockets[0].getsockname()[1]
        reader, writer = await asyncio.open_connection("127.0.0.1", actual_port)
        try:
            message = b"Hello asyncio!\n"
            writer.write(message)
            await writer.drain()
            reply = await asyncio.wait_for(reader.readline(), timeout=3)
            metric("Echo matches input", reply == message)
            event("log", "client", repr(reply))
        finally:
            writer.close()
            await writer.wait_closed()

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
