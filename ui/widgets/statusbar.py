"""
Status Bar Widget

Displays status messages, theme toggle, and other status indicators.
"""
import tkinter as tk
from tkinter import ttk
from ui.theme.colors import THEME

class StatusBar(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, style='StatusBar.TFrame', **kwargs)
        self.parent = parent
        
        # Configure grid
        self.columnconfigure(0, weight=1)  # Status message
        self.columnconfigure(1, weight=0)  # Spacer
        self.columnconfigure(2, weight=0)  # Theme indicator
        
        # Status message
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(
            self,
            textvariable=self.status_var,
            style='StatusBar.TLabel',
            anchor='w',
            padding=(8, 4)
        )
        self.status_label.grid(row=0, column=0, sticky='ew')
        
        # Theme indicator
        self.theme_btn = ttk.Button(
            self,
            text="☀️",
            command=self.toggle_theme,
            style='StatusBar.TButton',
            width=4
        )
        self.theme_btn.grid(row=0, column=2, sticky='e', padx=4, pady=2)
        
        # Apply theme
        self._update_theme()
    
    def set_message(self, message: str, category: str = 'info'):
        """Update the status message with optional category styling"""
        self.status_var.set(message)
        
        # Update styling based on category
        style = ttk.Style()
        if category == 'error':
            style.configure('StatusBar.TLabel', 
                          foreground=THEME['error'],
                          background=THEME['status_bg'])
        elif category == 'warning':
            style.configure('StatusBar.TLabel',
                          foreground=THEME['warning'],
                          background=THEME['status_bg'])
        elif category == 'success':
            style.configure('StatusBar.TLabel',
                          foreground=THEME['success'],
                          background=THEME['status_bg'])
        else:  # info
            style.configure('StatusBar.TLabel',
                          foreground=THEME['status_fg'],
                          background=THEME['status_bg'])
    
    def update_theme_indicator(self, dark_mode: bool):
        """Update the theme indicator icon"""
        self.theme_btn.config(text="🌙" if dark_mode else "☀️")
        self._update_theme()
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        if hasattr(self.parent, 'toggle_theme'):
            self.parent.toggle_theme()
    
    def _update_theme(self):
        """Update styling based on current theme"""
        style = ttk.Style()
        
        # Configure status bar frame
        style.configure('StatusBar.TFrame',
                      background=THEME['status_bg'],
                      borderwidth=1,
                      relief='sunken')
        
        # Configure status label
        style.configure('StatusBar.TLabel',
                      background=THEME['status_bg'],
                      foreground=THEME['status_fg'],
                      font=('Segoe UI', 9))
        
        # Configure theme button
        style.configure('StatusBar.TButton',
                      background=THEME['status_bg'],
                      borderwidth=0,
                      relief='flat')
        
        style.map('StatusBar.TButton',
                 background=[('active', THEME['highlight']),
                           ('!disabled', THEME['status_bg'])],
                 foreground=[('!disabled', THEME['status_fg'])])
