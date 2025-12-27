# services/runtimes/python/python_service.py
#
# Python Runtime Service (User-Space)

import subprocess
from pathlib import Path


class PythonRuntimeService:
    def __init__(self, python_cmd: str = "python3"):
        self.python_cmd = python_cmd

    def run(self, entry_file: Path, args: list[str] | None = None):
        if not entry_file.exists():
            raise RuntimeError("Entry Python file does not exist")

        args = args or []

        process = subprocess.Popen(
            [self.python_cmd, str(entry_file), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        return process
