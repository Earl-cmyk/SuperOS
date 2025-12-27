# ml/adapters/base.py

class ModelAdapter:
    """
    Base interface for all LLM adapters.
    Adapters must be stateless and side-effect free.
    """

    def generate(self, prompt: str) -> str:
        """
        Generate text from a prompt.
        Must return raw model output as string.
        """
        raise NotImplementedError("generate() not implemented")
