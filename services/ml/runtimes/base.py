# ml/runtimes/base.py

class Runtime:
    """
    Base runtime interface.
    A runtime executes a model adapter with a prompt.
    """

    def run(self, adapter, prompt: str) -> str:
        raise NotImplementedError("run() not implemented")
