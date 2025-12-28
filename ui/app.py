# ui/app.py
#
# SuperOS UI Application
#
# This is the main UI entrypoint.
# The UI is an IPC client and state observer.
# It NEVER executes code directly.

import time

from ui.window_manager import WindowManager
from ui.ipc_bridge import IPCBridge
from ui.project_explorer import ProjectExplorer
from ui.terminal import TerminalView
from ui.error_sidebar import ErrorSidebar
# ui/app.py
#
# SuperOS GUI Shell
# Tkinter owns rendering & input.
# This is a USER-SPACE PROCESS.

from ui.ipc_bridge import IPCBridge
from ui.gui import SuperOSGUI

class SuperOSApp:
    def __init__(self):
        self.ipc = IPCBridge()
        self.window_manager = WindowManager()
        self.error_sidebar = ErrorSidebar()

        self.project_explorer = ProjectExplorer(self.ipc)
        self.terminal = TerminalView(self.ipc)

        self._running = False

    def start(self):
        self.window_manager.register_panel("projects", self.project_explorer)
        self.window_manager.register_panel("terminal", self.terminal)
        self.window_manager.register_panel("errors", self.error_sidebar)

        self.ipc.subscribe("errors", self.error_sidebar.push)
        self.ipc.subscribe("process_output", self.terminal.write)

        self._running = True

        # 🔴 THIS MUST BLOCK
        self.run_loop()

    def run_loop(self):
        """
        UI main loop.
        Owns the display and blocks for the lifetime of the UI.
        """
        while self._running:
            self.window_manager.render_frame()
            time.sleep(0.016)  # ~60 FPS or event-driven

    def shutdown(self):
        self._running = False
        self.ipc.close()

def main():
    # app = SuperOSApp()
    # try:
    #     app.start()
    # except KeyboardInterrupt:
    #     app.shutdown()
    ipc = IPCBridge()
    gui = SuperOSGUI(ipc)
    gui.run()

if __name__ == "__main__":
    main()
