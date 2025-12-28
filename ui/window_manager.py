# ui/window_manager.py
#
# SuperOS Window Manager
#
# Owns the display surface.
# Responsible ONLY for layout + rendering.
# No IPC, no execution, no side effects.

import time
from typing import Dict


class WindowManager:
    def __init__(self, fps: int = 60):
        self.panels: Dict[str, object] = {}
        self.running = False
        self.frame_delay = 1.0 / fps

        # Placeholder for future:
        # - framebuffer
        # - compositor
        # - renderer backend (TUI / Web / Native)

    # -------------------------
    # Panel management
    # -------------------------

    def register_panel(self, name: str, panel: object) -> None:
        """
        Register a UI panel.
        Panel must expose:
          - render()
        """
        if not hasattr(panel, "render"):
            raise ValueError(f"Panel '{name}' has no render() method")

        self.panels[name] = panel

    def unregister_panel(self, name: str) -> None:
        self.panels.pop(name, None)

    # -------------------------
    # Lifecycle
    # -------------------------

    def start(self) -> None:
        """
        Start the window manager.
        BLOCKS for lifetime of UI.
        """
        self.running = True
        self._main_loop()

    def stop(self) -> None:
        self.running = False

    # -------------------------
    # Rendering
    # -------------------------

    def _main_loop(self) -> None:
        """
        Main render loop.
        Owns the display.
        """
        self._init_display()

        while self.running:
            start = time.time()

            self._clear()
            self._render_panels()
            self._present()

            elapsed = time.time() - start
            sleep_time = max(0, self.frame_delay - elapsed)
            time.sleep(sleep_time)

        self._shutdown_display()

    def render_frame(self) -> None:
        """
        Single-frame render (used if WM is driven externally).
        """
        self._clear()
        self._render_panels()
        self._present()

    # -------------------------
    # Internal helpers
    # -------------------------

    def _init_display(self) -> None:
        """
        Initialize display surface.
        """
        print("[UI] Display initialized")

    def _shutdown_display(self) -> None:
        """
        Clean up display surface.
        """
        print("[UI] Display shutdown")

    def _clear(self) -> None:
        """
        Clear screen / framebuffer.
        """
        print("\033[2J\033[H", end="")  # ANSI clear (safe default)

    def _render_panels(self) -> None:
        """
        Render all registered panels.
        Layout policy lives here.
        """
        for name, panel in self.panels.items():
            try:
                panel.render()
            except Exception as e:
                print(f"[UI][ERROR] Panel '{name}': {e}")

    def _present(self) -> None:
        """
        Flush frame to display.
        """
        pass  # No-op for now (TTY auto-flush)
