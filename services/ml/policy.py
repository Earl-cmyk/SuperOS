# ml/policy.py

class Policy:
    """
    Defines what actions the ML system is allowed to propose.
    This enforces authority boundaries between the model and the OS.
    """

    def __init__(self, capabilities: set[str]):
        self.capabilities = set(capabilities)

    def allow(self, action: str) -> bool:
        return action in self.capabilities

    def filter_actions(self, actions: list[str]) -> list[str]:
        return [a for a in actions if self.allow(a)]
