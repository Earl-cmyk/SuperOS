# ui/gui.py

import tkinter as tk
from ui.widgets.panel import SidePanel
from ui.widgets.desktop import Desktop
from ui.widgets.terminal import Terminal


class SuperOSGUI(tk.Tk):
    def __init__(self, ipc):
        super().__init__()

        self.ipc = ipc
        self.title("SuperOS")
        self.geometry("1200x800")
        self.configure(bg="#0f1115")
        self.minsize(900, 600)

        # Grid layout
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        # Panels
        self.ai_panel = SidePanel(self, "AI", "#151821")
        self.error_panel = SidePanel(self, "Errors", "#151821")
        self.desktop = Desktop(self)
        self.terminal = Terminal(self, ipc)

        self.ai_panel.grid(row=0, column=0, rowspan=2, sticky="ns")
        self.desktop.grid(row=0, column=1, sticky="nsew")
        self.terminal.grid(row=1, column=1, sticky="ew")
        self.error_panel.grid(row=0, column=2, rowspan=2, sticky="ns")

    def run(self):
        self.mainloop()
