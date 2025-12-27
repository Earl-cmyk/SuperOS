# runtimes/native/service.py


from services.ml.policy import Policy
from services.ml.runtimes.base import Runtime


class NativeRuntimeService:
    """
    Native Runtime Service

    Executes compiled native binaries under strict supervision.
    """

    RUNTIME_NAME = "native"
    RUNTIME_VERSION = "restricted"

    def __init__(self):
        self.policy = Policy()
        self.runtime = Runtime(policy=self.policy)

    def start(self):
        self.runtime.initialize()

    def stop(self):
        self.runtime.shutdown()

    def execute(self, binary_path: str, *, args=None, capabilities=None):
        """
        Execute a native binary.

        WARNING:
        This runtime is highly restricted and should be used sparingly.
        """
        self.policy.validate_execution(
            binary_path=binary_path,
            capabilities=capabilities,
            require_explicit_approval=True
        )

        return self.runtime.run(
            binary_path=binary_path,
            args=args or [],
            capabilities=capabilities or {}
        )
