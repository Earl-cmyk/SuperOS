# services/runtimes/java/java_service.py
#
# Java Runtime Service (User-Space)

import subprocess
from pathlib import Path


class JavaRuntimeService:
    def __init__(self, javac: str = "javac", java: str = "java"):
        self.javac = javac
        self.java = java

    def build(self, source_dir: Path, output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)

        sources = list(source_dir.glob("**/*.java"))
        if not sources:
            raise RuntimeError("No Java source files found")

        subprocess.run(
            [self.javac, "-d", str(output_dir), *map(str, sources)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        return output_dir

    def run(self, class_dir: Path, main_class: str, args: list[str] | None = None):
        args = args or []

        process = subprocess.Popen(
            [self.java, "-cp", str(class_dir), main_class, *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        return process
