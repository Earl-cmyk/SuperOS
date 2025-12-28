"""
Chrome Layout

OS-level visual structure:
- Top bar
- Side panels
- Status areas

Chrome never scrolls.
Chrome never owns logic.
"""

from ui.theme import colors, spacing


class Chrome:
    HEIGHT_TOPBAR = 40
    WIDTH_SIDEBAR = 260
    WIDTH_RIGHTBAR = 320

    @staticmethod
    def topbar_style() -> str:
        return (
            f"background-color: {colors.PANEL};"
            f"border-bottom: {spacing.BORDER_WIDTH}px solid {colors.DIVIDER};"
            f"padding: 0 {spacing.MD}px;"
        )

    @staticmethod
    def sidebar_style() -> str:
        return (
            f"background-color: {colors.PANEL};"
            f"border-right: {spacing.BORDER_WIDTH}px solid {colors.DIVIDER};"
            f"padding: {spacing.MD}px;"
        )

    @staticmethod
    def rightbar_style() -> str:
        return (
            f"background-color: {colors.PANEL};"
            f"border-left: {spacing.BORDER_WIDTH}px solid {colors.DIVIDER};"
            f"padding: {spacing.MD}px;"
        )

    @staticmethod
    def status_style() -> str:
        return (
            f"color: {colors.TEXT_MUTED};"
            f"font-size: 12px;"
        )
