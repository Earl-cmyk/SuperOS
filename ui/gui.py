import tkinter as tk
from tkinter import font
import os
import subprocess
import threading
import webbrowser
import time


# ================= ROOT =================
root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(bg="#0b0f1a")
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))


# ================= DESKTOP OS =================
class DesktopOS(tk.Frame):
    def __init__(self, master, ipc):
        super().__init__(master, bg="#0b0f1a")
        self.ipc = ipc
        self.pack(fill="both", expand=True)

        self.current_path = os.path.abspath("projects")

        # ---------- MAIN LAYOUT ----------
        self.desktop = tk.Frame(self, bg="#0b0f1a")
        self.desktop.pack(side="left", fill="both", expand=True)

        self.panel = tk.Frame(self, bg="#020617", width=420)
        self.panel.pack(side="right", fill="y")
        self.panel.pack_propagate(False)

        self.build_desktop()
        self.build_panel(self.current_path)

        # ---------- TERMINAL ----------
        self.terminal_height = 45
        self.drag_start_y = 0

        self.build_terminal()
        self.start_shell()

        self.master.bind_all("<Button-1>", self.force_terminal_focus)
        self.terminal.bind("<Return>", self.send_command)

        self.ipc.on("ml_response", self.ai_agent.on_response)
        self.ipc.on("ml_error", self.ai_agent.on_error)

        self.ai_agent = DesktopOS(ipc=self.ipc)

    # ================= ICON HELPERS =================
    def get_icon(self, path):
        if os.path.isdir(path):
            return "📁"
        if path.endswith(".py"):
            return "🐍"
        return "📄"

    # ================= DESKTOP =================
    def build_desktop(self):
        for w in self.desktop.winfo_children():
            w.destroy()

        col = row = 0
        for item in os.listdir("projects"):
            path = os.path.join("projects", item)
            self.create_icon(self.desktop, item, path, col, row)

            col += 1
            if col >= 8:
                col = 0
                row += 1

    # ================= PANEL =================
    def build_panel(self, path):
        for w in self.panel.winfo_children():
            w.destroy()

        header = tk.Label(
            self.panel,
            text=f"📂 {os.path.basename(path)}",
            bg="#020617",
            fg="#e5e7eb",
            font=("Segoe UI", 11, "bold"),
            pady=10
        )
        header.pack(fill="x")

        grid = tk.Frame(self.panel, bg="#020617")
        grid.pack(fill="both", expand=True)

        col = row = 0
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            self.create_icon(grid, item, item_path, col, row, panel=True)

            col += 1
            if col >= 3:
                col = 0
                row += 1

    # ================= ICON CREATION =================
    def create_icon(self, parent, name, path, col, row, panel=False):
        frame = tk.Frame(
            parent,
            width=90,
            height=90,
            bg="#050814",
            highlightthickness=1,
            highlightbackground="#1e293b"
        )
        frame.grid(row=row, column=col, padx=10, pady=10)
        frame.pack_propagate(False)

        icon = tk.Label(
            frame,
            text=self.get_icon(path),
            font=("Segoe UI Emoji", 14),
            bg="#050814",
            fg="#e5e7eb"
        )
        icon.pack(expand=True)

        label = tk.Label(
            frame,
            text=name,
            wraplength=80,
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg="#050814"
        )
        label.pack()

        def action(event=None):
            if os.path.isdir(path):
                self.build_panel(path)
            elif path.endswith(".py"):
                self.launch_script(path)

        for w in (frame, icon, label):
            w.bind("<Double-Button-1>", action)

    # ================= TERMINAL =================
    def build_terminal(self):
        self.terminal_frame = tk.Frame(self, bg="#000")
        self.terminal_frame.place(
            x=0,
            y=root.winfo_screenheight() - self.terminal_height,
            relwidth=1,
            height=self.terminal_height
        )

        self.handle = tk.Frame(
            self.terminal_frame,
            height=8,
            bg="#111",
            cursor="sb_v_double_arrow"
        )
        self.handle.pack(fill="x")
        self.handle.bind("<Button-1>", self.start_drag)
        self.handle.bind("<B1-Motion>", self.drag_terminal)

        self.term_font = font.Font(family="Consolas", size=11)

        self.terminal = tk.Text(
            self.terminal_frame,
            bg="#000",
            fg="#00ff66",
            insertbackground="#00ff66",
            font=self.term_font,
            relief="flat",
            wrap="word"
        )
        self.terminal.pack(fill="both", expand=True)

        self.terminal.insert("end", "SuperOS Terminal\n\n")
        self.terminal.focus_set()

    def start_shell(self):
        self.shell = subprocess.Popen(
            ["cmd"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        threading.Thread(target=self.read_output, daemon=True).start()

    def read_output(self):
        for line in self.shell.stdout:
            self.terminal.insert("end", line)
            self.terminal.see("end")

    def send_command(self, event):
        cmd = self.terminal.get("insert linestart", "insert").strip()
        self.terminal.insert("end", "\n")

        # 🔥 AI COMMAND
        if cmd.lower().startswith("ai-agent"):
            prompt = cmd[len("ai-agent"):].strip()
            if prompt:
                self.ai_agent.submit_prompt(prompt)
            else:
                self.terminal.insert("end", "[AI] Please provide a prompt\n")
            return "break"

        # NORMAL TERMINAL COMMAND
        self.shell.stdin.write(cmd + "\n")
        self.shell.stdin.flush()
        return "break"

    def launch_script(self, script):
        try:
            with open(script, "r", encoding="utf-8") as f:
                content = f.read().lower()
        except Exception:
            content = ""

        if "flask" in content:
            self.launch_flask_app(script)
        else:
            # NORMAL PYTHON SCRIPT → RUN IN TERMINAL
            self.shell.stdin.write(f"python \"{script}\"\n")
            self.shell.stdin.flush()

    def launch_flask_app(self, script):
        # Kill previous Flask app if running
        if hasattr(self, "flask_process") and self.flask_process:
            self.flask_process.terminate()

        # 🔥 THIS IS THE SCRIPT ACTUALLY RUNNING
        self.flask_process = subprocess.Popen(
            ["python", script],
            cwd=os.path.dirname(script),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        # OPTIONAL: pipe Flask logs into SuperOS terminal
        threading.Thread(
            target=self.pipe_flask_output,
            daemon=True
        ).start()

        # Open browser AFTER Flask starts
        def open_browser():
            time.sleep(1.5)
            webbrowser.open_new("http://127.0.0.1:5000")

        threading.Thread(target=open_browser, daemon=True).start()

    # ================= DRAG =================
    def start_drag(self, event):
        self.drag_start_y = event.y_root

    def drag_terminal(self, event):
        delta = self.drag_start_y - event.y_root
        self.drag_start_y = event.y_root
        self.terminal_height = max(120, min(600, self.terminal_height + delta))

        self.terminal_frame.place(
            x=0,
            y=root.winfo_screenheight() - self.terminal_height,
            relwidth=1,
            height=self.terminal_height
        )

    def force_terminal_focus(self, event=None):
        self.terminal.focus_set()
        self.terminal.mark_set("insert", "end")

    def pipe_flask_output(self):
        for line in self.flask_process.stdout:
            self.terminal.insert("end", "[FLASK] " + line)
            self.terminal.see("end")

    def render(self):
        self.terminal.insert("end", "\n=== ML Panel ===\n")
        for item in self._history[-20:]:
            role = item["role"].upper()
            content = item["content"]
            self.terminal.insert("end", f"[{role}] {content}\n")
        self.terminal.insert("end", "================\n")
        self.terminal.see("end")


# ================= RUN =================
DesktopOS(root, ipc)

root.mainloop()
