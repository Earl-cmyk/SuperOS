"""
Modern Toolbar Component

A customizable toolbar with icons, tooltips, and theming support.
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, Optional, Tuple

from ui.theme.colors import THEME

class Toolbar(ttk.Frame):
    """
    A modern toolbar with support for buttons, dropdowns, and separators.
    """
    
    def __init__(self, parent, ipc, **kwargs):
        """
        Initialize the toolbar.
        
        Args:
            parent: Parent widget
            ipc: IPC bridge for communication
            **kwargs: Additional frame arguments
        """
        super().__init__(parent, style='Toolbar.TFrame', **kwargs)
        self.ipc = ipc
        self.buttons: Dict[str, ttk.Button] = {}
        self._setup_style()
        self._create_toolbar()
    
    def _setup_style(self):
        """Configure toolbar styles"""
        style = ttk.Style()
        
        # Toolbar frame
        style.configure('Toolbar.TFrame',
                      background=THEME['toolbar_bg'],
                      borderwidth=1,
                      relief='flat')
        
        # Toolbar buttons
        style.configure('Toolbar.TButton',
                      background=THEME['toolbar_bg'],
                      foreground=THEME['toolbar_fg'],
                      borderwidth=0,
                      relief='flat',
                      padding=4)
        
        style.map('Toolbar.TButton',
                 background=[('active', THEME['highlight']),
                           ('!disabled', THEME['toolbar_bg'])],
                 foreground=[('!disabled', THEME['toolbar_fg'])])
        
        # Toolbar separators
        style.configure('Toolbar.TSeparator',
                      background=THEME['border'])
    
    def _create_toolbar(self):
        """Create toolbar contents"""
        # File operations
        self.add_button('new_file', '📄', 'New File (Ctrl+N)', 'new_file')
        self.add_button('open', '📂', 'Open File (Ctrl+O)', 'open_file')
        self.add_button('save', '💾', 'Save (Ctrl+S)', 'save')
        self.add_separator()
        
        # Edit operations
        self.add_button('undo', '↩️', 'Undo (Ctrl+Z)', 'undo')
        self.add_button('redo', '↪️', 'Redo (Ctrl+Shift+Z)', 'redo')
        self.add_separator()
        
        # Build and run
        self.add_button('build', '🔨', 'Build Project (Ctrl+B)', 'build')
        self.add_button('run', '▶️', 'Run (F5)', 'run')
        self.add_button('debug', '🐞', 'Debug (F6)', 'debug')
        self.add_separator()
        
        # Version control
        self.add_button('git', '🐙', 'Git Operations', 'git')
        
        # Spacer to push settings to the right
        spacer = ttk.Frame(self, style='Toolbar.TFrame')
        spacer.pack(side='left', expand=True, fill='x')
        
        # Settings and theme
        self.add_button('settings', '⚙️', 'Settings', 'settings')
        self.add_button('theme', '🌙', 'Toggle Theme', 'toggle_theme')
    
    def add_button(self, name: str, icon: str, tooltip: str, action: str):
        """
        Add a button to the toolbar.
        
        Args:
            name: Unique identifier for the button
            icon: Emoji or text icon to display
            tooltip: Tooltip text to show on hover
            action: Action to trigger when clicked
        """
        btn = ttk.Button(
            self,
            text=icon,
            style='Toolbar.TButton',
            command=lambda: self._on_button_click(action)
        )
        btn.pack(side='left', padx=1, pady=2)
        
        # Store button reference
        self.buttons[name] = btn
        
        # Add tooltip
        self._create_tooltip(btn, tooltip)
        
        return btn
    
    def add_separator(self):
        """Add a vertical separator to the toolbar"""
        sep = ttk.Separator(self, orient='vertical', style='Toolbar.TSeparator')
        sep.pack(side='left', fill='y', padx=4, pady=4)
    
    def _on_button_click(self, action: str):
        """Handle button clicks"""
        # Special handling for theme toggle
        if action == 'toggle_theme':
            if hasattr(self.master, 'toggle_theme'):
                self.master.toggle_theme()
                return
        
        # Forward other actions
        if hasattr(self.master, 'on_toolbar_action'):
            self.master.on_toolbar_action(action)
        else:
            self.ipc.send('toolbar_action', {'action': action})
    
    def _create_tooltip(self, widget, text: str):
        """Create a tooltip for a widget"""
        # TODO: Implement tooltip functionality
        pass
    
    def set_button_state(self, name: str, state: str):
        """
        Enable or disable a toolbar button.
        
        Args:
            name: Button name
            state: 'normal' or 'disabled'
        """
        if name in self.buttons:
            self.buttons[name].state(['!disabled' if state == 'normal' else 'disabled'])
    
    def update_theme(self):
        """Update toolbar appearance when theme changes"""
        self._setup_style()
        for btn in self.buttons.values():
            btn.update()
