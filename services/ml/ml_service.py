# ml/ml_service.py

from adapters.ollama import OllamaAdapter
from model_registry import ModelRegistry
from context_provider import ContextProvider
from action_planner import ActionPlanner
from policy import Policy
from runtimes.local import LocalRuntime


class MLService:
    """
    Main orchestration layer for ML interactions.
    This is the single entry point exposed to the rest of the system.
    """

    def __init__(self):
        # Security / authority
        self.policy = Policy({"read", "explain"})

        # Prompt + planning
        self.context_provider = ContextProvider()
        self.action_planner = ActionPlanner()

        # Model registry
        self.model_registry = ModelRegistry()
        self.model_registry.register(
            "local-default",
            OllamaAdapter("llama3.2")
        )

        # Runtime
        self.runtime = LocalRuntime()

    def handle(self, user_input: str, system_state: dict) -> dict:
        allowed_actions = list(self.policy.capabilities)

        prompt = self.context_provider.build(
            user_input=user_input,
            system_state=system_state,
            allowed_actions=allowed_actions
        )

        model = self.model_registry.get("local-default")
        raw_output = self.runtime.run(model, prompt)

        return self.action_planner.plan(raw_output)
