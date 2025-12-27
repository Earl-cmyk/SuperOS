# services/runtimes/rust/rust_service.py
#
# Rust Runtime Service (User-Space)

import subprocess
from pathlib import Path


class RustRuntimeService:
    def __init__(self, cargo_cmd: str = "cargo"):
        self.cargo_cmd = cargo_cmd

    def build(self, project_dir: Path) -> Path:
        subprocess.run(
            [self.cargo_cmd, "build", "--release"],
            cwd=project_dir,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        target_dir = project_dir / "target" / "release"
        binaries = [p for p in target_dir.iterdir() if p.is_file() and p.stat().st_mode & 0o111]

        if not binaries:
            raise RuntimeError("No Rust binaries produced")

        return binaries[0]

    def run(self, binary_path: Path, args: list[str] | None = None):
        args = args or []

        process = subprocess.Popen(
            [str(binary_path), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        return process
