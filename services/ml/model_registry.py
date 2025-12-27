# ml/model_registry.py

class ModelRegistry:
    """
    Registry for available LLM adapters.
    Allows model lookup by name without coupling callers
    to concrete adapter implementations.
    """

    def __init__(self):
        self._models = {}

    def register(self, name: str, adapter) -> None:
        if name in self._models:
            raise ValueError(f"Model '{name}' already registered")
        self._models[name] = adapter

    def get(self, name: str):
        if name not in self._models:
            raise KeyError(f"Model '{name}' not found")
        return self._models[name]

    def list(self) -> list[str]:
        return list(self._models.keys())
