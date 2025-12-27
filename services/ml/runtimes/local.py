# ml/runtimes/local.py

from .base import Runtime


class LocalRuntime(Runtime):
    """
    Local runtime executes the model adapter in the same process.
    """

    def run(self, adapter, prompt: str) -> str:
        return adapter.generate(prompt)
