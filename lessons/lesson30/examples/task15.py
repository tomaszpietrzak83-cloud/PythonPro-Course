import queue
import threading
import time
import urllib.request
from html.parser import HTMLParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urljoin, urlsplit

from lab_support import launch, metric, span

# Local site: fixed data and real HTTP requests, no Internet needed.
PAGES = {
    "/": '<a href="/a">A</a><a href="/b">B</a>',
    "/a": '<a href="/b">B</a><a href="/c">C</a>',
    "/b": '<a href="/c">C</a><a href="/">Start</a>',
    "/c": '<a href="/">Start</a>',
}


class DemoPageHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        time.sleep(0.35)  # Explicit delay in the demonstration server.
        self.send_response(200)
        self.end_headers()
        self.wfile.write(PAGES.get(self.path, "").encode())

    def log_message(self, *args):
        pass


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.extend(v for k, v in attrs if k == "href")


def main(config):
    server = ThreadingHTTPServer(("127.0.0.1", 0), DemoPageHandler)
    t = threading.Thread(target=server.serve_forever)
    t.start()
    base_url = f"http://127.0.0.1:{server.server_port}/"
    tasks, visited = queue.Queue(), set()
    lock = threading.Lock()

    def enqueue_url(url):
        # @step deduplicate
        with lock:
            if (
                urlsplit(url).netloc == urlsplit(base_url).netloc
                and url not in visited
                and len(visited) < 50
            ):
                visited.add(url)
                tasks.put(url)

    def crawl_worker(number):
        while True:
            url = tasks.get()
            try:
                if url is None:
                    return
                with span(f"Crawler {number}", urlsplit(url).path):
                    # @step fetch
                    with urllib.request.urlopen(url, timeout=5) as response:
                        parser = LinkParser()
                        parser.feed(response.read().decode())
                    for link in parser.links:
                        enqueue_url(urljoin(url, link))
            finally:
                tasks.task_done()

    try:
        enqueue_url(base_url)
        threads = [
            threading.Thread(target=crawl_worker, args=(i,)) for i in (1, 2, 3)
        ]
        for worker_thread in threads:
            worker_thread.start()
        # @step drain
        tasks.join()
        for _ in threads:
            tasks.put(None)
        for worker_thread in threads:
            worker_thread.join()
        metric("Unique pages", len(visited))
    finally:
        server.shutdown()
        t.join()
        server.server_close()


if __name__ == "__main__":
    launch(main)
