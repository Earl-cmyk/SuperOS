"""
SuperOS Spacing System

All layout spacing must come from here.
No magic numbers in widgets.
"""

# Base spacing unit (px)
UNIT = 8

# Common spacings
XS = UNIT // 2      # 4px
SM = UNIT           # 8px
MD = UNIT * 2       # 16px
LG = UNIT * 3       # 24px
XL = UNIT * 4       # 32px

# Padding presets
PANEL_PADDING = MD
WINDOW_PADDING = LG
CONTENT_PADDING = MD

# Gaps
ITEM_GAP = SM
SECTION_GAP = MD

# Border radius
RADIUS_SM = 4
RADIUS_MD = 6
RADIUS_LG = 10

# Borders
BORDER_WIDTH = 1
FOCUS_RING_WIDTH = 2
