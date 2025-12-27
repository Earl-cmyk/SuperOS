# services/runtimes/js/js_service.py
#
# JavaScript Runtime Service (User-Space)

import subprocess
from pathlib import Path


class JsRuntimeService:
    def __init__(self, node_cmd: str = "node"):
        self.node_cmd = node_cmd

    def run(self, entry_file: Path, args: list[str] | None = None):
        if not entry_file.exists():
            raise RuntimeError("Entry JS file does not exist")

        args = args or []

        process = subprocess.Popen(
            [self.node_cmd, str(entry_file), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        return process
