# services/arduino_sim/sketch_loader.py

class Sketch:
    """
    Represents a loaded Arduino sketch.
    Must expose setup() and loop(dt_ms).
    """

    def __init__(self, setup_fn, loop_fn):
        self.setup = setup_fn
        self.loop = loop_fn


class SketchLoader:
    """
    Loads and validates Arduino-style sketches.
    """

    def load(self, source: dict) -> Sketch:
        """
        source is expected to be a dict-like object:
        {
          "setup": callable,
          "loop": callable
        }
        """

        if "setup" not in source or "loop" not in source:
            raise ValueError("Sketch must define setup() and loop()")

        setup_fn = source["setup"]
        loop_fn = source["loop"]

        if not callable(setup_fn) or not callable(loop_fn):
            raise TypeError("setup and loop must be callable")

        return Sketch(setup_fn, loop_fn)
