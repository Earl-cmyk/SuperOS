# services/arduino_sim/service.py

from .runtime import ArduinoSimRuntime
from .policy import ArduinoSimPolicy
from .sketch_loader import SketchLoader


class ArduinoSimService:
    """
    User-space Arduino simulation service.
    Exposes a safe, policy-enforced API to the OS.
    """

    def __init__(self, simulator_backend):
        self.policy = ArduinoSimPolicy(
            allowed_pins={0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13}
        )

        self.runtime = ArduinoSimRuntime(
            simulator=simulator_backend,
            policy=self.policy
        )

        self.loader = SketchLoader()
        self._loaded = False

    # ---- Public service API (IPC targets) ----

    def load_sketch(self, sketch_source: dict) -> None:
        sketch = self.loader.load(sketch_source)
        self.runtime.load_sketch(sketch)
        self._loaded = True

    def start(self) -> None:
        if not self._loaded:
            raise RuntimeError("No sketch loaded")
        self.runtime.start()

    def step(self, ms: int) -> None:
        self.runtime.step(ms)

    def stop(self) -> None:
        self.runtime.stop()
        self._loaded = False

    def read_pin(self, pin: int):
        return self.runtime.read_pin(pin)

    def write_pin(self, pin: int, value):
        self.runtime.write_pin(pin, value)
