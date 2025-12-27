# services/arduino_sim/policy.py

class ArduinoSimPolicy:
    """
    Policy enforcement for the Arduino simulation service.
    This constrains what a sketch and callers are allowed to do.
    """

    def __init__(
        self,
        allowed_pins: set[int],
        max_step_ms: int = 100,
        max_runtime_ms: int = 10_000
    ):
        self.allowed_pins = set(allowed_pins)
        self.max_step_ms = max_step_ms
        self.max_runtime_ms = max_runtime_ms

    def allow_pin(self, pin: int) -> bool:
        return pin in self.allowed_pins

    def validate_pin(self, pin: int) -> None:
        if not self.allow_pin(pin):
            raise PermissionError(f"Pin {pin} is not allowed")

    def validate_step(self, ms: int) -> None:
        if ms <= 0 or ms > self.max_step_ms:
            raise ValueError(
                f"Step time {ms}ms exceeds limit ({self.max_step_ms}ms)"
            )

    def validate_runtime(self, elapsed_ms: int) -> None:
        if elapsed_ms > self.max_runtime_ms:
            raise TimeoutError(
                f"Simulation exceeded max runtime ({self.max_runtime_ms}ms)"
            )
