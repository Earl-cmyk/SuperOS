# ui/app.py

import tkinter as tk
from ui.gui import DesktopOS


def main(ipc):
    """
    SuperOS UI entrypoint.
    Called by orchestrator with IPCBus injected.
    """

    root = tk.Tk()
    root.title("SuperOS")
    root.attributes("-fullscreen", True)

    DesktopOS(
        master=root,
        ipc=ipc,
        projects_dir="projects"
    )

    root.mainloop()
