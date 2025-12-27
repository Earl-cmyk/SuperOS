# services/runtimes/unreal/unreal_service.py
#
# Unreal Engine Runtime Service (User-Space)
#
# Builds and runs Unreal Engine projects via Unreal Automation Tool (UAT).
# This service assumes Unreal Engine is installed on the host.
# It has NO authority to escape kernel-enforced sandboxing.

import subprocess
from pathlib import Path


class UnrealRuntimeService:
    def __init__(self, unreal_root: Path):
        self.unreal_root = unreal_root
        self.uat = unreal_root / "Engine" / "Build" / "BatchFiles" / "RunUAT.sh"

        if not self.uat.exists():
            raise RuntimeError("Unreal Automation Tool (UAT) not found")

    def build(self, project_file: Path, output_dir: Path, platform: str = "Linux"):
        output_dir.mkdir(parents=True, exist_ok=True)

        cmd = [
            str(self.uat),
            "BuildCookRun",
            f"-project={project_file}",
            "-noP4",
            "-build",
            "-cook",
            "-stage",
            "-pak",
            "-archive",
            f"-archivedirectory={output_dir}",
            f"-platform={platform}",
        ]

        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        return output_dir

    def run(self, executable: Path, args: list[str] | None = None):
        if not executable.exists():
            raise RuntimeError("Unreal executable not found")

        args = args or []

        process = subprocess.Popen(
            [str(executable), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        return process
