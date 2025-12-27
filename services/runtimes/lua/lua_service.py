# runtimes/lua/service.py

from services.ml.policy import Policy
from services.ml.runtimes.base import Runtime


class LuaRuntimeService:
    """
    Lua Runtime Service

    Lightweight, embedded scripting environment.
    """

    RUNTIME_NAME = "lua"
    RUNTIME_VERSION = "5.4"

    def __init__(self):
        self.policy = Policy()
        self.runtime = Runtime(policy=self.policy)

    def start(self):
        self.runtime.initialize()

    def stop(self):
        self.runtime.shutdown()

    def execute(self, script_path: str, *, context=None, capabilities=None):
        """
        Execute a Lua script.

        Args:
            script_path: Path to .lua file
            context: Injected execution context
            capabilities: Allowed operations
        """
        self.policy.validate_execution(
            script_path=script_path,
            capabilities=capabilities
        )

        return self.runtime.run(
            script_path=script_path,
            context=context or {},
            capabilities=capabilities or {}
        )
