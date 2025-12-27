# services/runtimes/r/r_service.py
#
# R Runtime Service (User-Space)

import subprocess
from pathlib import Path


class RRuntimeService:
    def __init__(self, rscript_cmd: str = "Rscript"):
        self.rscript_cmd = rscript_cmd

    def run(self, script_file: Path, args: list[str] | None = None):
        if not script_file.exists():
            raise RuntimeError("R script does not exist")

        args = args or []

        process = subprocess.Popen(
            [self.rscript_cmd, str(script_file), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        return process
