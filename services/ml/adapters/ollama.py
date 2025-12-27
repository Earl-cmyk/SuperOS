# ml/adapters/ollama.py

import subprocess
from .base import ModelAdapter


class OllamaAdapter(ModelAdapter):
    """
    Adapter for local Ollama models.
    Runs ollama as a subprocess (user-space only).
    """

    def __init__(self, model: str = "llama3.2"):
        self.model = model

    def generate(self, prompt: str) -> str:
        proc = subprocess.run(
            ["ollama", "run", self.model],
            input=prompt,
            text=True,
            capture_output=True
        )

        if proc.returncode != 0:
            raise RuntimeError(
                f"Ollama failed: {proc.stderr.strip()}"
            )

        return proc.stdout.strip()
