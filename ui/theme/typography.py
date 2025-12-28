"""
SuperOS Typography System

Font choices are intentional:
- UI: readable, neutral
- Terminal: monospaced, precise
"""

# Font families
UI_FONT = "Inter, Segoe UI, sans-serif"
MONO_FONT = "JetBrains Mono, Fira Code, monospace"

# Font sizes (px)
FONT_XS = 11
FONT_SM = 12
FONT_BASE = 13
FONT_MD = 14
FONT_LG = 16
FONT_XL = 18

# Weights
WEIGHT_REGULAR = 400
WEIGHT_MEDIUM = 500
WEIGHT_SEMIBOLD = 600

# Line heights
LINE_TIGHT = 1.2
LINE_NORMAL = 1.4
LINE_RELAXED = 1.6

# Usage hints (not enforced, but documented)
# Titles      -> FONT_LG / SEMIBOLD
# Body        -> FONT_BASE / REGULAR
# Labels      -> FONT_SM / MEDIUM
# Terminal    -> FONT_SM / MONO_FONT
