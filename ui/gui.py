# ui/gui.py
"""
SuperOS GUI Shell

Responsibilities:
- Window composition ONLY
- Widget placement
- User input → intent (future IPC)

NO business logic
NO execution
"""

import os
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

# ---- FUTURE IMPORTS (INTENTIONAL, UNUSED FOR NOW) ----
# from ui.ipc_bridge import IPCBridge
# from ui.event_loop import UIEventLoop
# from ai.agent_client import AIAgentClient
# from orchestrator.client import OrchestratorClient
# -----------------------------------------------------


class SuperOSGUI(tk.Tk):
    def __init__(self, projects_dir="projects", ipc=None):
        super().__init__()

        self.ipc = ipc
        self.projects_dir = projects_dir

        self.title("SuperOS")
        self.geometry("1280x800")
        self.minsize(1024, 640)

        self._configure_styles()
        self._configure_grid()
        self._build_left_output_panel()
        self._build_center_workspace()
        self._build_right_ai_panel()
        self._build_terminal_panel()

    # --------------------------------------------------
    # Styles (LIGHT, NOT A THEME ENGINE)
    # --------------------------------------------------

    def _configure_styles(self):
        style = ttk.Style()
        style.configure("TLabel", font=("Segoe UI", 9))
        style.configure("Header.TLabel", font=("Segoe UI", 9, "bold"))

    # --------------------------------------------------
    # Layout Grid
    # --------------------------------------------------

    def _configure_grid(self):
        # 3 columns: output | workspace | ai
        self.columnconfigure(0, minsize=180, weight=0)
        self.columnconfigure(1, minsize=480, weight=1)
        self.columnconfigure(2, minsize=190, weight=0)

        # 2 rows: main | terminal
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, minsize=130, weight=0)

    # --------------------------------------------------
    # Left: Output Panel
    # --------------------------------------------------

    def _build_left_output_panel(self):
        frame = ttk.LabelFrame(self, text="Output", padding=6)
        frame.grid(row=0, column=0, sticky="nsew", padx=(6, 3), pady=6)

        self.output_view = ScrolledText(
            frame,
            state="disabled",
            wrap="word",
            font=("Consolas", 9),
            background="#f7f7f7"
        )
        self.output_view.pack(fill="both", expand=True)

    # --------------------------------------------------
    # Center: Workspace (Projects)
    # --------------------------------------------------

    def _build_center_workspace(self):
        frame = ttk.LabelFrame(self, text="Workspace", padding=6)
        frame.grid(row=0, column=1, sticky="nsew", padx=3, pady=6)

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        self.workspace = ttk.Treeview(frame)
        self.workspace.grid(row=0, column=0, sticky="nsew")

        self._load_projects()

    def _load_projects(self):
        self.workspace.delete(*self.workspace.get_children())

        root = self.workspace.insert("", "end", text=self.projects_dir, open=True)

        if not os.path.isdir(self.projects_dir):
            self.workspace.insert(root, "end", text="[projects dir missing]")
            return

        for item in sorted(os.listdir(self.projects_dir)):
            self.workspace.insert(root, "end", text=item)

    # --------------------------------------------------
    # Right: AI Agent Panel
    # --------------------------------------------------

    def _build_right_ai_panel(self):
        frame = ttk.LabelFrame(self, text="AI Agent", padding=6)
        frame.grid(row=0, column=2, sticky="nsew", padx=(3, 6), pady=6)

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        # Chat input (search-box style)
        self.ai_input = ttk.Entry(frame)
        self.ai_input.grid(row=0, column=0, sticky="ew", pady=(0, 6))

        # Chat history
        self.ai_chat = ScrolledText(
            frame,
            state="disabled",
            wrap="word",
            font=("Segoe UI", 9)
        )
        self.ai_chat.grid(row=1, column=0, sticky="nsew")

    # --------------------------------------------------
    # Bottom: Terminal Panel
    # --------------------------------------------------

    def _build_terminal_panel(self):
        frame = ttk.LabelFrame(self, text="Terminal", padding=6)
        frame.grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="nsew",
            padx=6,
            pady=(0, 6),
        )

        frame.columnconfigure(0, weight=1)

        self.terminal_input = ttk.Entry(
            frame,
            font=("Consolas", 10)
        )
        self.terminal_input.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        btns = ttk.Frame(frame)
        btns.grid(row=0, column=1, sticky="e")

        ttk.Button(btns, text="Run", command=self._on_run).pack(side="left", padx=2)
        ttk.Button(btns, text="Stop", command=self._on_stop).pack(side="left", padx=2)
        ttk.Button(btns, text="Run Last", command=self._on_run_last).pack(side="left", padx=2)

    # --------------------------------------------------
    # Button Handlers (INTENTS ONLY)
    # --------------------------------------------------

    def _on_run(self):
        cmd = self.terminal_input.get()
        self._append_output(f"> {cmd}\n")
        # FUTURE: ipc.publish("process.spawn", ...)

    def _on_stop(self):
        self._append_output("[STOP]\n")

    def _on_run_last(self):
        self._append_output("[RUN LAST]\n")

    # --------------------------------------------------
    # Utilities
    # --------------------------------------------------

    def _append_output(self, text: str):
        self.output_view.configure(state="normal")
        self.output_view.insert("end", text)
        self.output_view.configure(state="disabled")
        self.output_view.see("end")


# ------------------------------------------------------
# Standalone Run (for testing only)
# ------------------------------------------------------

def main():
    app = SuperOSGUI(projects_dir="projects")
    app.mainloop()


if __name__ == "__main__":
    main()
