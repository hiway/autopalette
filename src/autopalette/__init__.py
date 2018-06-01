from .palette import (
    AutoPalette,
    Gray4Palette,
    GameBoyGreenPalette,
    GameBoyChocolatePalette,
    Oil6Palette,
    ColorsCCPalette,
    DutronPalette,
)
from .theme import (
    Theme,
    ThemeColor,
    BasicTheme,
    FourColorTheme,
)
from .render import (
    AnsiTruecolorRenderer,
    Ansi256Renderer,
    Ansi16Renderer,
    Ansi8Renderer,
    AnsiNoColorRenderer,
)
from .autoformat import AutoFormat

af = AutoFormat()
ap = af

__all__ = [
    'af',
    'ap',
    'AnsiTruecolorRenderer',
    'Ansi256Renderer',
    'Ansi16Renderer',
    'Ansi8Renderer',
    'AnsiNoColorRenderer',
    'AutoFormat',
    'AutoPalette',
    'Theme',
    'ThemeColor',
    'BasicTheme',
    'FourColorTheme',
    'Gray4Palette',
    'GameBoyGreenPalette',
    'GameBoyChocolatePalette',
    'Oil6Palette',
]
