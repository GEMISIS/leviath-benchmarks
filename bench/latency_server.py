#!/usr/bin/env python3
"""Tiny local latency server: GET /?ms=N sleeps N milliseconds, then answers.

The mock provider calls this once per inference to simulate real model
latency, which is what makes N agents genuinely concurrent instead of
draining one-by-one at mock speed. Threaded so hundreds of in-flight
requests can sleep simultaneously.
"""
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

PORT = 18742


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        q = parse_qs(urlparse(self.path).query)
        ms = int(q.get("ms", ["0"])[0])
        time.sleep(min(ms, 30000) / 1000.0)
        body = b'{"ok":true}'
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
