from pathlib import Path


def demo(work):
    root = Path(__file__).parent
    stages = {name: sum(line.startswith("FROM ") for line in (root / name).read_text().splitlines())
              for name in ("Dockerfile.single", "Dockerfile")}
    assert list(stages.values()) == [1, 2]
    return {"build_stages": stages, "size_measurement": "sh compare.sh on a Docker host"}


from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from os import getenv
from threading import Thread
from urllib.request import urlopen


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = getenv("HOSTNAME", "local").encode()
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def probe(work):
    with ThreadingHTTPServer(("127.0.0.1", 0), Handler) as server:
        thread = Thread(target=server.serve_forever)
        thread.start()
        try:
            with urlopen(f"http://127.0.0.1:{server.server_port}", timeout=3) as response:
                assert response.status == 200
                return {"http": response.status, "body": response.read().decode()}
        finally:
            server.shutdown()
            thread.join()


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
