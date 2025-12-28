"""
SuperOS Animation Timing

Animations communicate state changes.
Never decorative.
"""

# Durations (ms)
INSTANT = 0
FAST = 120
NORMAL = 180
SLOW = 260

# Easing (semantic names)
EASE_OUT = "ease-out"
EASE_IN = "ease-in"
EASE_IN_OUT = "ease-in-out"
LINEAR = "linear"

# Common animation presets
PANEL_TOGGLE = {
    "duration": NORMAL,
    "easing": EASE_OUT,
}

FOCUS_CHANGE = {
    "duration": FAST,
    "easing": EASE_OUT,
}

WINDOW_MOVE = {
    "duration": NORMAL,
    "easing": EASE_IN_OUT,
}

PROCESS_STATE_CHANGE = {
    "duration": FAST,
    "easing": LINEAR,
}
