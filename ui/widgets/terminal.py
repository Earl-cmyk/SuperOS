# ui/widgets/terminal.py
import tkinter as tk
from tkinter import ttk
import subprocess
import threading
from ui.theme.colors import THEME

class Terminal(ttk.Frame):
    def __init__(self, parent, ipc):
        super().__init__(parent, style='Terminal.TFrame')
        self.ipc = ipc
        self._setup_style()
        self._create_widgets()
        
    def _setup_style(self):
        style = ttk.Style()
        style.configure('Terminal.TFrame', background=THEME['terminal_bg'])
        style.configure('Terminal.TLabel', 
                       background=THEME['terminal_header_bg'],
                       foreground=THEME['terminal_fg'],
                       font=('Segoe UI', 10, 'bold'),
                       padding=(10, 5, 5, 5))
        style.configure('Terminal.Text', 
                       background=THEME['terminal_bg'],
                       foreground=THEME['terminal_fg'],
                       insertbackground=THEME['terminal_fg'],
                       font=('Consolas', 10))
    
    def _create_widgets(self):
        # Header
        header = ttk.Label(
            self,
            text="Terminal",
            style='Terminal.TLabel'
        )
        header.pack(fill='x')
        
        # Text area
        self.text = tk.Text(
            self,
            wrap='word',
            bd=0,
            highlightthickness=0,
            font=('Consolas', 10),
            bg=THEME['terminal_bg'],
            fg=THEME['terminal_fg'],
            insertbackground=THEME['terminal_fg'],
            padx=8,
            pady=8
        )
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.text.yview)
        self.text.configure(yscrollcommand=scrollbar.set)
        
        # Pack everything
        self.text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
    def run_command(self, command: str):
        """Run a command in a non-blocking way"""
        def worker():
            try:
                process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                # Read output in real-time
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        self.text.after(0, self._append_output, output)
                
                # Get any remaining output
                stdout, _ = process.communicate()
                if stdout:
                    self.text.after(0, self._append_output, stdout)
                
                # Show command completion status
                if process.returncode == 0:
                    self.text.after(0, self._append_output, f"\n[Process completed with code {process.returncode}]\n")
                else:
                    self.text.after(0, self._append_output, f"\n[Process failed with code {process.returncode}]\n")
                    
            except Exception as e:
                self.text.after(0, self._append_output, f"\nError: {str(e)}\n")
        
        # Start the command in a separate thread
        threading.Thread(target=worker, daemon=True).start()
    
    def _append_output(self, text):
        self.text.config(state='normal')
        self.text.insert('end', text)
        self.text.see('end')
        self.text.config(state='disabled')
    
    def write(self, text: str):
        """Thread-safe write to terminal"""
        self.text.after(0, self._append_output, text)