"""
SuperOS UI Color System

All colors are semantic.
No widget should hardcode hex values.
"""

# Core surfaces
BACKGROUND = "#0e0f13"      # app background
SURFACE = "#151722"         # main workspace surface
PANEL = "#1b1e2e"           # side panels, chrome
OVERLAY = "#202336"         # dialogs, overlays

# Borders & dividers
BORDER = "#2a2e45"
DIVIDER = "#24283b"

# Text
TEXT_PRIMARY = "#e6e6eb"
TEXT_SECONDARY = "#b4b7c5"
TEXT_MUTED = "#8b90a7"
TEXT_DISABLED = "#5c607a"

# Accents & intent
ACCENT = "#7aa2f7"          # primary action / focus
ACCENT_SOFT = "#3d59a1"

SUCCESS = "#9ece6a"
WARNING = "#e0af68"
ERROR = "#f7768e"
INFO = "#7dcfff"

# Terminal
TERMINAL_BG = "#0b0d12"
TERMINAL_FG = "#c0caf5"
TERMINAL_CURSOR = "#7aa2f7"

# States
FOCUS_RING = "#7aa2f7"
SELECTION_BG = "#283457"
HOVER_BG = "#1f2335"

# Dark Theme
DARK = {
    'bg': '#1e1e2e',
    'fg': '#cdd6f4',
    'primary': '#89b4fa',
    'secondary': '#cba6f7',
    'accent': '#f5c2e7',
    'success': '#a6e3a1',
    'warning': '#f9e2af',
    'error': '#f38ba8',
    'panel_bg': '#181825',
    'panel_fg': '#bac2de',
    'terminal_bg': '#11111b',
    'terminal_fg': '#cdd6f4',
    'border': '#313244',
    'highlight': '#45475a',
    'toolbar_bg': '#181825',
    'toolbar_fg': '#cdd6f4',
    'status_bg': '#181825',
    'status_fg': '#a6adc8',
}

# Light Theme
LIGHT = {
    'bg': '#eff1f5',
    'fg': '#4c4f69',
    'primary': '#1e66f5',
    'secondary': '#8839ef',
    'accent': '#ea76cb',
    'success': '#40a02b',
    'warning': '#df8e1d',
    'error': '#d20f39',
    'panel_bg': '#e6e9ef',
    'panel_fg': '#4c4f69',
    'terminal_bg': '#dce0e8',
    'terminal_fg': '#4c4f69',
    'border': '#bcc0cc',
    'highlight': '#acb0be',
    'toolbar_bg': '#e6e9ef',
    'toolbar_fg': '#4c4f69',
    'status_bg': '#e6e9ef',
    'status_fg': '#6c6f85',
}

# Default theme
THEME = DARK

def set_theme(theme_name: str):
    """Set the current theme."""
    global THEME
    THEME = DARK if theme_name.lower() == 'dark' else LIGHT
