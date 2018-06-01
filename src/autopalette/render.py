from typing import Union, ClassVar

import sty
from colour import Color

from autopalette.colormatch import ColorPoint, AnsiCodeType
from autopalette.palette import Ansi256Palette, Ansi16Palette, Ansi8Palette
from autopalette.utils import rgb_to_RGB255

OptionalColor = Union['Color', None]
OptionalPalette = ClassVar['BasePalette']
OptionalRenderer = ClassVar['Renderer']


class BaseRenderer(object):
    def __init__(self,
                 palette: OptionalPalette = None,
                 fallback: OptionalPalette = None) -> None:
        self.palette = palette if palette else Ansi256Palette()
        self.fallback = fallback if fallback else Ansi256Palette()

    def render(self, text, fg: Color, bg: OptionalColor = None):
        raise NotImplementedError()

    def is_bright(self, color: Color):
        if color.get_saturation() == 0 \
                and color.get_luminance() == 1:
            return True
        if color.get_luminance() > 0.7:
            return True
        if color.get_saturation() >= 0.3 \
                and color.get_luminance() >= 0.3:
            return True
        return False


class Ansi256Renderer(BaseRenderer):
    def render(self, text, fg: Color, bg: OptionalColor = None, ansi_reset=False):
        if ansi_reset:
            return text
        fg = self.palette.match(fg, ansi=True)
        if fg.ansi == '' or fg.ansi is None:
            fg = self.fallback.match(fg.target, ansi=True)
        if bg:
            bg = self.palette.match(bg, ansi=True)
            if bg.ansi == '' or bg.ansi is None:
                bg = self.fallback.match(bg.target, ansi=True)
        return self._render(text, fg=fg, bg=bg)

    def _render(self, text, fg: ColorPoint, bg: ColorPoint = None):
        out = ''
        out += sty.fg(fg.ansi)
        if bg:
            out += sty.bg(bg.ansi)
        out += text
        out += sty.rs.all
        return out

    def is_bright(self, color: Color):
        ansi = self.palette.match(color).ansi
        if ansi < 16:
            if ansi in (0, 1, 2, 3, 4, 5, 6, 8):
                return False
            return True
        return super().is_bright(color)

    def bg(self, color: Color) -> str:
        return sty.bg(self.palette.match(color, ansi=True).ansi)

    def fg(self, color: Color) -> str:
        return sty.fg(self.palette.match(color, ansi=True).ansi)

    @property
    def rs(self):
        return sty.rs

    @property
    def ef(self):
        return sty.ef


class AnsiNoColorRenderer(Ansi256Renderer):
    def render(self, text, fg: Color, bg: OptionalColor = None, ansi_reset=False):
        return text


class Ansi16Renderer(Ansi256Renderer):

    def __init__(self,
                 palette: OptionalPalette = None,
                 fallback: OptionalPalette = None) -> None:
        super().__init__(palette=Ansi16Palette,
                         fallback=fallback)

    def render(self, text, fg: Color, bg: OptionalColor = None, ansi_reset=False):
        # todo: downsample 256 to 16 colors
        return super().render(text, fg=fg, bg=bg, ansi_reset=False)


class Ansi8Renderer(Ansi256Renderer):

    def __init__(self,
                 palette: OptionalPalette = None,
                 fallback: OptionalPalette = None) -> None:
        super().__init__(palette=Ansi8Palette,
                         fallback=fallback)

    def render(self, text, fg: Color, bg: OptionalColor = None, ansi_reset=False):
        # todo: downsample 256 to 8 colors
        return super().render(text, fg=fg, bg=bg, ansi_reset=False)


class AnsiTruecolorRenderer(BaseRenderer):
    def match(self, color: Color) -> ColorPoint:
        ansi = rgb_to_RGB255(color.rgb)
        return ColorPoint(color, color, ansi=ansi)

    def render(self, text, fg: Color, bg: OptionalColor = None, ansi_reset=False):
        if ansi_reset:
            return text
        fg = self.palette.match(fg)
        if bg:
            bg = self.palette.match(bg)
        return self._render(text, fg=fg, bg=bg)

    def _render(self, text, fg: ColorPoint, bg: ColorPoint = None):
        rgb = rgb_to_RGB255(fg.target.rgb)
        out = ''
        out += sty.fg(*rgb)
        if bg:
            bgrgb = rgb_to_RGB255(bg.target.rgb)
            out += sty.bg(*bgrgb)
        out += text
        out += sty.rs.all
        return out

    def bg(self, color: Color) -> str:
        bg = self.palette.match(color)
        rgb = rgb_to_RGB255(bg.target.rgb)
        return sty.fg(*rgb)

    def fg(self, color: Color) -> str:
        fg = self.palette.match(color)
        rgb = rgb_to_RGB255(fg.target.rgb)
        return sty.fg(*rgb)

    @property
    def rs(self):
        return sty.rs

    @property
    def ef(self):
        return sty.ef


render_map = {
    '-1':             AnsiTruecolorRenderer,
    '0':              AnsiNoColorRenderer,
    '8':              Ansi8Renderer,
    '16':             Ansi16Renderer,
    '88':             Ansi256Renderer,
    '256':            Ansi256Renderer,
    'ansi':           Ansi256Renderer,
    'rgb':            AnsiTruecolorRenderer,
    'truecolor':      AnsiTruecolorRenderer,
    '24bit':          AnsiTruecolorRenderer,
    'vt100':          AnsiNoColorRenderer,
    'vt200':          AnsiNoColorRenderer,
    'vt220':          AnsiNoColorRenderer,
    'rxvt':           Ansi16Renderer,
    'rxvt-88color':   Ansi256Renderer,
    'xterm':          Ansi16Renderer,
    'xterm-color':    Ansi16Renderer,
    'xterm-256color': Ansi256Renderer,

}
