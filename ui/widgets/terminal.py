# ui/widgets/terminal.py

import tkinter as tk


class Terminal(tk.Frame):
    def __init__(self, parent, ipc):
        super().__init__(parent, bg="#0b0d12", height=220)
        self.pack_propagate(False)

        self.ipc = ipc

        header = tk.Label(
            self,
            text="Terminal",
            fg="#50fa7b",
            bg="#0b0d12",
            font=("Segoe UI", 10, "bold"),
            pady=6,
        )
        header.pack(fill="x")

        self.output = tk.Text(
            self,
            bg="#0b0d12",
            fg="#f8f8f2",
            insertbackground="white",
            relief="flat",
            font=("Consolas", 10),
        )
        self.output.pack(fill="both", expand=True, padx=8, pady=4)

    def write(self, text: str):
        self.output.insert("end", text + "\n")
        self.output.see("end")
