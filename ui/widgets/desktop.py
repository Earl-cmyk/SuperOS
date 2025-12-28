# ui/widgets/desktop.py

import tkinter as tk


class Desktop(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#0f1115")

        title = tk.Label(
            self,
            text="Workspace",
            fg="#f8f8f2",
            bg="#0f1115",
            font=("Segoe UI", 14, "bold"),
        )
        title.pack(anchor="w", padx=16, pady=(16, 8))

        placeholder = tk.Label(
            self,
            text="GUI applications will render here",
            fg="#6272a4",
            bg="#0f1115",
            font=("Segoe UI", 11),
        )
        placeholder.pack(anchor="center", expand=True)
