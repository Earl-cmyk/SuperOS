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

        # ───────── Window ─────────
        self.title("SuperOS")
        self.geometry("1400x900")
        self.minsize(1100, 700)

        try:
            icon = Path(__file__).parent / "assets" / "icon.ico"
            if icon.exists():
                self.iconbitmap(icon)
        except Exception:
            pass

        # ───────── Theme ─────────
        self._dark_mode = True
        set_theme("dark")
        self._setup_styles()

        # ───────── Layout ─────────
        self._setup_layout()

        # ───────── UI ─────────
        self._create_toolbar()
        self._create_workspace()
        self._create_assistant()
        self._create_terminal()
        self._create_statusbar()

        # ───────── Events ─────────
        self.bind("<Control-q>", lambda _: self.on_close())
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.update_status("Ready")

    # ───────────────────────── Styles ─────────────────────────

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(".", background=THEME["bg"], foreground=THEME["fg"])
        style.configure("TFrame", background=THEME["bg"])
        style.configure("Panel.TFrame", background=THEME["panel_bg"])

        style.configure(
            "TButton",
            padding=6,
            relief="flat"
        )

        style.map(
            "TButton",
            background=[("active", THEME["highlight"])],
            foreground=[("active", THEME["fg"])]
        )

        self.configure(background=THEME["bg"])

    # ───────────────────────── Layout ─────────────────────────

    def _setup_layout(self):
        self.columnconfigure(0, weight=0, minsize=260)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0, minsize=320)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)

    # ───────────────────────── Components ─────────────────────────

    def _create_toolbar(self):
        self.toolbar = Toolbar(self, self.ipc, self.on_toolbar_action)
        self.toolbar.grid(row=0, column=0, columnspan=3, sticky="ew", padx=2, pady=(2, 1))

    def _create_workspace(self):
        self.left_panel = SidePanel(self, "Explorer", THEME["panel_bg"])
        self.desktop = Desktop(self)
        self.right_panel = SidePanel(self, "AI Assistant", THEME["panel_bg"])

        self.left_panel.grid(row=1, column=0, sticky="nsew", padx=(2, 1), pady=1)
        self.desktop.grid(row=1, column=1, sticky="nsew", padx=1, pady=1)
        self.right_panel.grid(row=1, column=2, sticky="nsew", padx=(1, 2), pady=1)

    def _create_assistant(self):
        self.assistant_frame = ttk.Frame(self.right_panel, style="Panel.TFrame")
        self.assistant_frame.pack(fill="both", expand=True, padx=1, pady=1)

        self.chat_display = tk.Text(
            self.assistant_frame,
            wrap="word",
            state="disabled",
            bg=THEME["panel_bg"],
            fg=THEME["panel_fg"],
            insertbackground=THEME["panel_fg"],
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill="both", expand=True)

        input_frame = ttk.Frame(self.assistant_frame)
        input_frame.pack(fill="x", padx=5, pady=5)

        self.chat_input = ttk.Entry(input_frame)
        self.chat_input.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.chat_input.bind("<Return>", self._on_send_message)

        ttk.Button(input_frame, text="Send", command=self._on_send_message).pack(side="right")

    def _create_terminal(self):
        self.terminal = Terminal(self, self.ipc)
        self.terminal.grid(row=2, column=0, columnspan=3, sticky="ew", padx=2, pady=1)

    def _create_statusbar(self):
        self.status_bar = StatusBar(self)
        self.status_bar.grid(row=3, column=0, columnspan=3, sticky="ew")

    # ───────────────────────── Assistant ─────────────────────────

    def _on_send_message(self, event=None):
        msg = self.chat_input.get().strip()
        if not msg:
            return
        self.chat_input.delete(0, "end")
        self._append_message("You", msg)
        self._append_message("Assistant", "AI integration pending.")

    def _append_message(self, sender, message):
        self.chat_display.config(state="normal")
        self.chat_display.insert("end", f"{sender}: {message}\n\n")
        self.chat_display.see("end")
        self.chat_display.config(state="disabled")

    # ───────────────────────── Actions ─────────────────────────

    def on_toolbar_action(self, action: str):
        if action == "run":
            self.terminal.run_command("python sandbox/hello.py")
        elif action == "toggle_theme":
            self.toggle_theme()
        else:
            self.ipc.send("ui_action", {"action": action})

    def toggle_theme(self):
        self._dark_mode = not self._dark_mode
        set_theme("dark" if self._dark_mode else "light")
        self._setup_styles()

    def update_status(self, message, category="info"):
        self.status_bar.set_message(message, category)

    def on_close(self):
        try:
            self.ipc.send("app_shutdown", {})
        finally:
            self.destroy()

    def run(self):
        self.mainloop()
