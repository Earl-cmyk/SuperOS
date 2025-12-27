# ui/app.py
#
# SuperOS UI Application
#
# This is the main UI entrypoint.
# The UI is an IPC client and state observer.
# It NEVER executes code directly.

from ui.window_manager import WindowManager
from ui.ipc_bridge import IPCBridge
from ui.project_explorer import ProjectExplorer
from ui.terminal import TerminalView
from ui.error_sidebar import ErrorSidebar


class SuperOSApp:
    def __init__(self):
        self.ipc = IPCBridge()
        self.window_manager = WindowManager()
        self.error_sidebar = ErrorSidebar()

        self.project_explorer = ProjectExplorer(self.ipc)
        self.terminal = TerminalView(self.ipc)

    def start(self):
        self.window_manager.register_panel("projects", self.project_explorer)
        self.window_manager.register_panel("terminal", self.terminal)
        self.window_manager.register_panel("errors", self.error_sidebar)

        self.ipc.subscribe("errors", self.error_sidebar.push)
        self.ipc.subscribe("process_output", self.terminal.write)

        self.window_manager.render()

    def shutdown(self):
        self.ipc.close()


if __name__ == "__main__":
    app = SuperOSApp()
    app.start()
