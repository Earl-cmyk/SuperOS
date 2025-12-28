# ui/widgets/panel.py

import tkinter as tk


class SidePanel(tk.Frame):
    def __init__(self, parent, title: str, bg: str):
        super().__init__(parent, bg=bg, width=200)

        self.pack_propagate(False)

        header = tk.Label(
            self,
            text=title,
            fg="#8be9fd",
            bg=bg,
            font=("Segoe UI", 11, "bold"),
            pady=10,
        )
        header.pack(fill="x")

        self.text = tk.Text(
            self,
            bg=bg,
            fg="#cdd6f4",
            relief="flat",
            wrap="word",
            state="disabled",
            font=("Segoe UI", 10),
        )
        self.text.pack(fill="both", expand=True, padx=8, pady=4)

    def log(self, message: str):
        self.text.config(state="normal")
        self.text.insert("end", message + "\n")
        self.text.see("end")
        self.text.config(state="disabled")
