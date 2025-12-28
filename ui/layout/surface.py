"""
Surface Layout Primitive

Used for:
- panels
- cards
- sidebars
- content areas

No logic. No state.
"""

from ui.theme import colors, spacing


class Surface:
    def __init__(
        self,
        *,
        background=colors.SURFACE,
        padding=spacing.CONTENT_PADDING,
        radius=spacing.RADIUS_MD,
        border_color=colors.BORDER,
        border_width=spacing.BORDER_WIDTH,
    ):
        self.background = background
        self.padding = padding
        self.radius = radius
        self.border_color = border_color
        self.border_width = border_width

    def style(self) -> str:
        """Return a CSS/QSS-style string."""
        return (
            f"background-color: {self.background};"
            f"padding: {self.padding}px;"
            f"border-radius: {self.radius}px;"
            f"border: {self.border_width}px solid {self.border_color};"
        )
