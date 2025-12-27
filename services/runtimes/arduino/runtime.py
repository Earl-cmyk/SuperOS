# services/arduino_sim/runtime.py

import time


class ArduinoSimRuntime:
    """
    Runtime wrapper for an Arduino simulation backend.
    Responsible for executing setup/loop and tracking time.
    """

    def __init__(self, simulator, policy):
        """
        simulator: an instance of ArduinoSimulator (or compatible)
        policy: ArduinoSimPolicy
        """
        self.simulator = simulator
        self.policy = policy
        self._start_time = None
        self._running = False

    def load_sketch(self, sketch) -> None:
        """
        Load a compiled / prepared sketch into the simulator.
        """
        self.simulator.load(sketch)

    def start(self) -> None:
        """
        Start the simulation (calls setup()).
        """
        self._start_time = time.time()
        self._running = True
        self.simulator.setup()

    def step(self, ms: int) -> None:
        """
        Advance the simulation by a time step (calls loop()).
        """
        if not self._running:
            raise RuntimeError("Simulation not running")

        self.policy.validate_step(ms)

        elapsed_ms = int((time.time() - self._start_time) * 1000)
        self.policy.validate_runtime(elapsed_ms)

        self.simulator.loop(ms)

    def stop(self) -> None:
        """
        Stop the simulation.
        """
        self._running = False
        self.simulator.reset()

    def read_pin(self, pin: int):
        self.policy.validate_pin(pin)
        return self.simulator.read_pin(pin)

    def write_pin(self, pin: int, value):
        self.policy.validate_pin(pin)
        self.simulator.write_pin(pin, value)
