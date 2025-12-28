"""
Split Layout Primitive

Used for:
- main workspace splits
- editor / terminal
- left-right panels
"""

from ui.theme import colors, spacing


class Split:
    def __init__(
        self,
        *,
        orientation: str = "horizontal",  # horizontal | vertical
        divider_color=colors.DIVIDER,
        divider_width=spacing.BORDER_WIDTH,
        gap=0,
    ):
        assert orientation in ("horizontal", "vertical")
        self.orientation = orientation
        self.divider_color = divider_color
        self.divider_width = divider_width
        self.gap = gap

    def container_style(self) -> str:
        direction = "row" if self.orientation == "horizontal" else "column"
        return (
            f"display: flex;"
            f"flex-direction: {direction};"
            f"gap: {self.gap}px;"
        )

    def divider_style(self) -> str:
        if self.orientation == "horizontal":
            return (
                f"width: {self.divider_width}px;"
                f"background-color: {self.divider_color};"
            )
        return (
            f"height: {self.divider_width}px;"
            f"background-color: {self.divider_color};"
        )
