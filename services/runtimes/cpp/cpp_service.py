# services/runtimes/cpp/cpp_service.py
#
# C++ Runtime Service (User-Space)
#
# Compiles and runs C++ projects inside a controlled process sandbox.
# This service has NO authority to grant permissions or escape isolation.

import subprocess
import tempfile
import os
from pathlib import Path


class CppRuntimeService:
    def __init__(self, compiler: str = "g++"):
        self.compiler = compiler

    def build(self, source_dir: Path, output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        binary_path = output_dir / "app"

        sources = list(source_dir.glob("**/*.cpp"))
        if not sources:
            raise RuntimeError("No C++ source files found")

        compile_cmd = [
            self.compiler,
            *map(str, sources),
            "-O2",
            "-std=c++20",
            "-o",
            str(binary_path),
        ]

        subprocess.run(
            compile_cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        return binary_path

    def run(self, binary_path: Path, args: list[str] | None = None):
        args = args or []

        process = subprocess.Popen(
            [str(binary_path), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        return process
