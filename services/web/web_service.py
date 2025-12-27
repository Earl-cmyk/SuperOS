# services/web/web_service.py
#
# Web Service (User-Space)
#
# Serves project web content in an isolated HTTP server.
# This service exposes ONLY kernel-approved directories.

from http.server import SimpleHTTPRequestHandler, HTTPServer
from pathlib import Path
import threading
import os


class WebService:
    def __init__(self, root_dir: Path, host: str = "127.0.0.1", port: int = 8000):
        self.root_dir = root_dir
        self.host = host
        self.port = port
        self._server = None
        self._thread = None

    def start(self):
        os.chdir(self.root_dir)

        self._server = HTTPServer(
            (self.host, self.port),
            SimpleHTTPRequestHandler,
        )

        self._thread = threading.Thread(
            target=self._server.serve_forever,
            daemon=True,
        )
        self._thread.start()

        return {
            "host": self.host,
            "port": self.port,
        }

    def stop(self):
        if self._server:
            self._server.shutdown()
            self._server.server_close()
            self._server = None
