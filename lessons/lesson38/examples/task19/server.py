from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ThreadingHTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler).serve_forever()
