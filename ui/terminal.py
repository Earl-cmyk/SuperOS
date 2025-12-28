# ui/widgets/terminal.py

import tkinter as tk
from tkinter import ttk
import os

class Terminal(tk.Frame):
    def __init__(self, parent, ipc):
        super().__init__(parent, bg=THEME["terminal_bg"], height=200)
        self.pack_propagate(False)
        self.ipc = ipc
        self.history = []
        self.history_index = -1
        self.current_dir = os.getcwd()
        
        self._setup_ui()
        self._bind_events()
        
    def _setup_ui(self):
        # Header
        header = tk.Frame(self, bg=THEME["terminal_header_bg"], height=28)
        header.pack(fill="x", pady=(0, 1))
        
        tk.Label(
            header,
            text="Terminal",
            fg=THEME["terminal_fg"],
            bg=THEME["terminal_header_bg"],
            font=("Segoe UI", 9, "bold"),
            padx=10
        ).pack(side="left")
        
        # Output area with scrollbar
        output_frame = tk.Frame(self, bg=THEME["terminal_bg"])
        output_frame.pack(fill="both", expand=True, padx=1, pady=(0, 1))
        
        scrollbar = ttk.Scrollbar(output_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.output = tk.Text(
            output_frame,
            bg=THEME["terminal_bg"],
            fg=THEME["terminal_fg"],
            insertbackground=THEME["terminal_cursor"],
            selectbackground=THEME["terminal_selection"],
            selectforeground=THEME["terminal_fg"],
            relief="flat",
            font=("Consolas", 10),
            yscrollcommand=scrollbar.set,
            padx=8,
            pady=8
        )
        self.output.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.output.yview)
        
        # Command line
        self.cmd_frame = tk.Frame(self, bg=THEME["terminal_bg"], height=24)
        self.cmd_frame.pack(fill="x", side="bottom", pady=(1, 0))
        
        self.prompt = tk.Label(
            self.cmd_frame,
            text=f"{os.path.basename(self.current_dir)} $ ",
            fg=THEME["terminal_prompt"],
            bg=THEME["terminal_bg"],
            font=("Consolas", 10, "bold")
        )
        self.prompt.pack(side="left", padx=(8, 0))
        
        self.cmd_entry = tk.Entry(
            self.cmd_frame,
            bg=THEME["terminal_bg"],
            fg=THEME["terminal_fg"],
            insertbackground=THEME["terminal_fg"],
            relief="flat",
            font=("Consolas", 10)
        )
        self.cmd_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.cmd_entry.focus_set()
        
    def _bind_events(self):
        self.cmd_entry.bind("<Return>", self._on_command)
        self.cmd_entry.bind("<Up>", self._history_up)
        self.cmd_entry.bind("<Down>", self._history_down)
        
    def _on_command(self, event):
        cmd = self.cmd_entry.get().strip()
        if cmd:
            self.history.append(cmd)
            self.history_index = len(self.history)
            self.write(f"{self.prompt['text']}{cmd}", "command")
            
            # Process command
            self.ipc.send("terminal_input", {"data": cmd})
            
            # Clear input
            self.cmd_entry.delete(0, "end")
            
    def _history_up(self, event):
        if self.history and self.history_index > 0:
            self.history_index -= 1
            self.cmd_entry.delete(0, "end")
            self.cmd_entry.insert(0, self.history[self.history_index])
            
    def _history_down(self, event):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.cmd_entry.delete(0, "end")
            self.cmd_entry.insert(0, self.history[self.history_index])
        elif self.history_index == len(self.history) - 1:
            self.history_index = len(self.history)
            self.cmd_entry.delete(0, "end")
            
    def write(self, text: str, text_type: str = "output"):
        """Write text to the terminal with optional styling"""
        self.output.config(state="normal")
        
        if text_type == "command":
            self.output.tag_configure("command", foreground=THEME["terminal_command"])
            self.output.insert("end", text + "\n", "command")
        elif text_type == "error":
            self.output.tag_configure("error", foreground=THEME["terminal_error"])
            self.output.insert("end", text + "\n", "error")
        else:
            self.output.insert("end", text + "\n")
            
        self.output.see("end")
        self.output.config(state="disabled")
        
    def update_prompt(self, new_dir=None):
        """Update the current working directory in the prompt"""
        if new_dir:
            self.current_dir = new_dir
        dir_name = os.path.basename(self.current_dir)
        self.prompt.config(text=f"{dir_name} $ ")