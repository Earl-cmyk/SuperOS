"""
SuperOS Main GUI

Modern, responsive IDE-style UI for SuperOS.
Toolbar • Explorer • Desktop • Assistant • Terminal • Status Bar
"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path

from ui.theme.colors import THEME, set_theme
from ui.widgets.panel import SidePanel
from ui.widgets.desktop import Desktop
from ui.widgets.terminal import Terminal
from ui.widgets.toolbar import Toolbar
from ui.widgets.statusbar import StatusBar


class SuperOSGUI(tk.Tk):
    def __init__(self, ipc):
        super().__init__()
        self.ipc = ipc

        # ───────────────────────── Window ─────────────────────────
        self.title("SuperOS")
        self.geometry("1400x900")
        self.minsize(1100, 700)

        try:
            icon = Path(__file__).parent / "assets" / "icon.ico"
            if icon.exists():
                self.iconbitmap(icon)
        except Exception:
            pass

        # ───────────────────────── Theme ─────────────────────────
        self._dark_mode = True
        set_theme("dark")
        self._setup_styles()

        # ───────────────────────── Layout ─────────────────────────
        self._setup_layout()

        # ───────────────────────── UI ─────────────────────────
        self._create_toolbar()
        self._create_workspace()
        self._create_terminal()
        self._create_statusbar()

        # ───────────────────────── Events ─────────────────────────
        self.bind("<Control-q>", lambda _: self.on_close())
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.update_status("Ready")

    # ───────────────────────── Styles ─────────────────────────

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        self.configure(bg=THEME["bg"])

        style.configure(
            "TFrame",
            background=THEME["bg"]
        )
        style.configure(
            "TLabel",
            background=THEME["bg"],
            foreground=THEME["fg"]
        )
        style.configure(
            "TButton",
            padding=(8, 4),
            background=THEME["panel_bg"],
            foreground=THEME["fg"]
        )
        style.map(
            "TButton",
            background=[("active", THEME["highlight"])]
        )

        style.configure(
            "Primary.TButton",
            background=THEME["primary"],
            foreground=THEME["bg"]
        )

    # ───────────────────────── Grid ─────────────────────────

    def _setup_layout(self):
        """
        Rows:
        0 ─ Toolbar
        1 ─ Main workspace
        2 ─ Terminal
        3 ─ Status bar
        """

        self.columnconfigure(0, weight=0, minsize=260)   # Explorer
        self.columnconfigure(1, weight=1)                # Desktop
        self.columnconfigure(2, weight=0, minsize=320)   # Assistant

        self.rowconfigure(0, weight=0)  # Toolbar
        self.rowconfigure(1, weight=1)  # Workspace
        self.rowconfigure(2, weight=0)  # Terminal
        self.rowconfigure(3, weight=0)  # Status bar

    # ───────────────────────── Components ─────────────────────────

    def _create_toolbar(self):
        self.toolbar = Toolbar(self, self.ipc)
        self.toolbar.grid(
            row=0, column=0, columnspan=3,
            sticky="ew", padx=2, pady=(2, 1)
        )

    def _create_workspace(self):
        self.left_panel = SidePanel(
            parent=self,
            title="Explorer",
            bg=THEME["panel_bg"]
        )
        self.desktop = Desktop(self)
        self.right_panel = SidePanel(
            parent=self,
            title="AI Assistant",
            bg=THEME["panel_bg"]
        )

        self.left_panel.grid(
            row=1, column=0,
            sticky="nsew", padx=(2, 1), pady=1
        )
        self.desktop.grid(
            row=1, column=1,
            sticky="nsew", padx=1, pady=1
        )
        self.right_panel.grid(
            row=1, column=2,
            sticky="nsew", padx=(1, 2), pady=1
        )

    def _create_terminal(self):
        self.terminal = Terminal(self, self.ipc)
        self.terminal.grid(
            row=2, column=0, columnspan=3,
            sticky="ew", padx=2, pady=(1, 1)
        )

    def _create_statusbar(self):
        self.status_bar = StatusBar(self)
        self.status_bar.grid(
            row=3, column=0, columnspan=3,
            sticky="ew"
        )

    # ───────────────────────── Actions ─────────────────────────

    def toggle_theme(self):
        self._dark_mode = not self._dark_mode
        set_theme("dark" if self._dark_mode else "light")
        self._setup_styles()
        self.status_bar.update_theme_indicator(self._dark_mode)

    def on_toolbar_action(self, action: str):
        if action == "new_file":
            self.desktop.create_new_file()
        elif action == "save":
            self.desktop.save_current_file()
        elif action == "run":
            self.terminal.run_command("python main.py")
        elif action == "toggle_theme":
            self.toggle_theme()
        else:
            self.ipc.send("ui_action", {"action": action})

    def update_status(self, message: str, category: str = "info"):
        if hasattr(self, "status_bar"):
            self.status_bar.set_message(message, category)

    def on_close(self):
        try:
            self.ipc.send("app_shutdown", {})
        finally:
            self.destroy()

    def run(self):
        self.mainloop()
