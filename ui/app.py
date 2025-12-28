# # ui/app.py
# #
# # SuperOS UI Application
# #
# # This is the main UI entrypoint.
# # The UI is an IPC client and state observer.
# # It NEVER executes code directly.

# import time

# from ui.window_manager import WindowManager
# from ui.ipc_bridge import IPCBridge
# from ui.project_explorer import ProjectExplorer
# from ui.terminal import TerminalView
# from ui.error_sidebar import ErrorSidebar
# # ui/app.py
# #
# # SuperOS GUI Shell
# # Tkinter owns rendering & input.
# # This is a USER-SPACE PROCESS.

# from ui.ipc_bridge import IPCBridge
# from ui.gui import SuperOSGUI

# class SuperOSApp:
#     def __init__(self):
#         self.ipc = IPCBridge()
#         self.window_manager = WindowManager()
#         self.error_sidebar = ErrorSidebar()

#         self.project_explorer = ProjectExplorer(self.ipc)
#         self.terminal = TerminalView(self.ipc)

#         self._running = False

#     def start(self):
#         self.window_manager.register_panel("projects", self.project_explorer)
#         self.window_manager.register_panel("terminal", self.terminal)
#         self.window_manager.register_panel("errors", self.error_sidebar)

#         self.ipc.subscribe("errors", self.error_sidebar.push)
#         self.ipc.subscribe("process_output", self.terminal.write)

#         self._running = True

#         # 🔴 THIS MUST BLOCK
#         self.run_loop()

#     def run_loop(self):
#         """
#         UI main loop.
#         Owns the display and blocks for the lifetime of the UI.
#         """
#         while self._running:
#             self.window_manager.render_frame()
#             time.sleep(0.016)  # ~60 FPS or event-driven

#     def shutdown(self):
#         self._running = False
#         self.ipc.close()

# def main():
#     # app = SuperOSApp()
#     # try:
#     #     app.start()
#     # except KeyboardInterrupt:
#     #     app.shutdown()
#     ipc = IPCBridge()
#     gui = SuperOSGUI(ipc)
#     gui.run()

# if __name__ == "__main__":
#     main()

# ui/app.py
#
# SuperOS UI Application
#
# This is the USER-SPACE GUI shell.
# It observes system state via IPC and renders it.
#
# Rules:
# - UI NEVER executes kernel or service logic
# - UI is a pure observer + input forwarder
# - Rendering BLOCKS for the lifetime of the process

"""
SuperOS UI Application

This is the main entry point for the SuperOS GUI.
It initializes the IPC bridge and starts the GUI.
"""
import os
import sys
import logging
import signal
from pathlib import Path

# Add the project root to the Python path
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('superos_ui.log')
    ]
)
logger = logging.getLogger(__name__)

# Import after path setup
from ui.ipc_bridge import IPCBridge
from ui.gui import SuperOSGUI


class SuperOSApp:
    """
    SuperOS GUI Application Wrapper.

    Manages the lifecycle of the GUI and IPC communication.
    """

    def __init__(self):
        """Initialize the application with IPC and GUI components."""
        self.running = False
        self.ipc = None
        self.gui = None
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self._initialize()

    def _initialize(self):
        """Initialize IPC and GUI components."""
        try:
            logger.info("Initializing SuperOS UI...")
            self.ipc = IPCBridge()
            self.gui = SuperOSGUI(
                projects_dir="projects",
                ipc=self.ipc
            )
            logger.info("SuperOS UI initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize SuperOS UI: {e}")
            self._cleanup()
            raise

    def start(self):
        """
        Start the GUI application.
        This call blocks until the application is closed.
        """
        if not self.gui:
            logger.error("GUI not initialized")
            return

        self.running = True
        logger.info("Starting SuperOS UI...")
        
        try:
            self.gui.mainloop()
        except Exception as e:
            logger.error(f"Error in GUI main loop: {e}")
        finally:
            self.shutdown()

    def shutdown(self):
        """Clean up resources and shut down the application."""
        if not self.running:
            return
            
        logger.info("Shutting down SuperOS UI...")
        self.running = False
        
        try:
            if hasattr(self.gui, 'on_close'):
                self.gui.on_close()
        except Exception as e:
            logger.error(f"Error during GUI shutdown: {e}")
        
        self._cleanup()
        logger.info("SuperOS UI shutdown complete")
    
    def _cleanup(self):
        """Clean up resources."""
        try:
            if self.ipc:
                self.ipc.close()
        except Exception as e:
            logger.error(f"Error during IPC cleanup: {e}")
        
        # Ensure all tkinter windows are destroyed
        try:
            import tkinter as tk
            for widget in tk._default_root.winfo_children() if tk._default_root else []:
                try:
                    widget.destroy()
                except:
                    pass
        except:
            pass
    
    def _signal_handler(self, signum, frame):
        """Handle termination signals."""
        logger.info(f"Received signal {signum}, shutting down...")
        self.shutdown()
        sys.exit(0)


def main():
    """Main entry point for the application."""
    try:
        app = SuperOSApp()
        app.start()
    except Exception as e:
        logger.critical(f"Fatal error in SuperOS UI: {e}", exc_info=True)
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user")
        sys.exit(0)


if __name__ == "__main__":
    main()
