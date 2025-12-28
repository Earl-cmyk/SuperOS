# ui/theme/colors.py

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
    'border': '#313244',
    'highlight': '#45475a',
    'toolbar_bg': '#181825',
    'toolbar_fg': '#cdd6f4',
    'status_bg': '#181825',
    'status_fg': '#a6adc8',
    
    # Terminal colors
    'terminal_bg': '#0b0d12',
    'terminal_fg': '#f8f8f2',
    'terminal_header_bg': '#1a1e26',
    'terminal_prompt': '#50fa7b',
    'terminal_cursor': '#f8f8f2',
    'terminal_selection': '#44475a',
    'terminal_command': '#8be9fd',
    'terminal_error': '#ff5555',
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
    'border': '#bcc0cc',
    'highlight': '#acb0be',
    'toolbar_bg': '#e6e9ef',
    'toolbar_fg': '#4c4f69',
    'status_bg': '#e6e9ef',
    'status_fg': '#6c6f85',
    
    # Terminal colors
    'terminal_bg': '#f8f8f2',
    'terminal_fg': '#282a36',
    'terminal_header_bg': '#e6e6e6',
    'terminal_prompt': '#50fa7b',
    'terminal_cursor': '#282a36',
    'terminal_selection': '#b4d8fd',
    'terminal_command': '#6272a4',
    'terminal_error': '#ff5555',
}

# Default theme
THEME = DARK

def set_theme(theme_name: str):
    """Set the current theme.
    
    Args:
        theme_name: Either 'dark' or 'light' (case-insensitive)
    """
    global THEME
    theme_name = theme_name.lower()
    if theme_name == 'dark':
        THEME = DARK
    elif theme_name == 'light':
        THEME = LIGHT
    else:
        raise ValueError(f"Unknown theme: {theme_name}. Use 'dark' or 'light'")