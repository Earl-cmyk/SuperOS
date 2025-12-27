# services/runtimes/csharp/csharp_service.py
#
# C# Runtime Service (User-Space)
#
# Builds and runs C# projects using the .NET SDK.
# This service executes only within kernel-approved sandboxes.

import subprocess
from pathlib import Path


class CSharpRuntimeService:
    def __init__(self, dotnet_cmd: str = "dotnet"):
        self.dotnet_cmd = dotnet_cmd

    def build(self, project_dir: Path, output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)

        build_cmd = [
            self.dotnet_cmd,
            "build",
            str(project_dir),
            "-c",
            "Release",
            "-o",
            str(output_dir),
        ]

        subprocess.run(
            build_cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Convention: first dll in output dir is entry
        dlls = list(output_dir.glob("*.dll"))
        if not dlls:
            raise RuntimeError("No build output produced")

        return dlls[0]

    def run(self, dll_path: Path, args: list[str] | None = None):
        args = args or []

        process = subprocess.Popen(
            [self.dotnet_cmd, str(dll_path), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        return process
