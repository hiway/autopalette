import sty
from colour import Color

from autopalette.colormatch import AnsiCodeType
from autopalette.palette import Ansi256Palette
from autopalette.render import OptionalPalette, OptionalRenderer, Ansi256Renderer


class ThemeColor(object):
    """
    Stores edits applied in definition of Palette.

    >>> base = ThemeColor('white').set_luminance(.8)
    >>> base._edits
    [('set_luminance', [0.8])]
    >>> base._color
    'white'
    """

    def __init__(self, color: str = None, ansi: AnsiCodeType = None):
        self._color = color
        self._edits = []
        self._ansi = ansi
        self.ansi_reset = False

    def apply(self, color: Color):
        for method, args in self._edits:
            if method == 'reset':
                self.ansi_reset = True
                # todo
                continue
            getattr(color, method)(*args)
        return self

    def reset(self):
        self._edits.append(('reset', [True]))
        return self

    def set_hue(self, value):
        self._edits.append(('set_hue', [value]))
        return self

    def set_saturation(self, value):
        self._edits.append(('set_saturation', [value]))
        return self

    def set_luminance(self, value):
        self._edits.append(('set_luminance', [value]))
        return self

    def __call__(self, *args, **kwargs):
        """Exists to prevent linter warnings."""
        raise NotImplementedError()


class ThemeStyle(object):
    """
    Style holds foreground and background colors
    for a single style in a palette.

    style = Style(fg=Color(), bg=Color())

    style("text")
    """

    def __init__(self, fg, bg, renderer, ansi_reset):
        self.fg = fg
        self.bg = bg
        self._renderer = renderer
        self._ansi_reset = ansi_reset

    def __repr__(self):
        return 'Style(fg={}, bg={})'.format(self.fg, self.bg)

    def __call__(self, text):
        return self._renderer.render(text, fg=self.fg, bg=self.bg, ansi_reset=self._ansi_reset)

    @property
    def renderer(self):
        return self._renderer


class Theme(object):
    def __init__(self, palette: OptionalPalette = None, renderer: OptionalRenderer = None):
        self.palette = palette() if palette else Ansi256Palette()
        renderer = renderer(palette=palette) if renderer else Ansi256Renderer(palette=palette)
        renderer.palette = self.palette
        self.renderer = renderer
        for name, attr in self.__class__.__dict__.items():
            if not isinstance(attr, ThemeColor):
                continue
            if name.startswith('_'):
                if hasattr(self, name[1:]):
                    continue
                else:
                    raise ValueError('Background set without foreground: {}'.format(name))
            match = self.palette.match(Color(attr._color))
            fg = Color(match.target.hex_l)
            attr.apply(fg)
            bg = None
            if hasattr(self, '_' + name):
                bgattr = getattr(self, '_' + name)
                bgmatch = self.palette.match(Color(bgattr._color))
                bg = Color(bgmatch.target.hex_l)
                bgattr.apply(bg)
            setattr(self, name,
                    ThemeStyle(fg, bg=bg,
                               renderer=self.renderer,
                               ansi_reset=attr.ansi_reset))


class BasicTheme(Theme):
    base = ThemeColor('white').reset()
    light = ThemeColor('silver')
    dark = ThemeColor('purple').set_luminance(.2)

    h1 = ThemeColor('black')
    _h1 = ThemeColor('yellow')

    h2 = ThemeColor('white')
    _h2 = ThemeColor('blue')

    h3 = ThemeColor('black')
    _h3 = ThemeColor('green').set_luminance(.8)

    h4 = ThemeColor('white').set_luminance(1)
    _h4 = ThemeColor('purple').set_luminance(.2)

    error = ThemeColor('white')
    _error = ThemeColor('red')

    warning = ThemeColor('red')

    info = ThemeColor('lightblue').set_luminance(.5).set_saturation(.7)
    ok = ThemeColor('green')


class FourColorTheme(Theme):
    base = ThemeColor('black').set_luminance(.7)
    light = ThemeColor('black').set_luminance(.9)
    dark = ThemeColor('black').set_luminance(.4)

    h1 = ThemeColor('white')
    _h1 = ThemeColor('silver').set_luminance(.5)

    h2 = ThemeColor('white')
    _h2 = ThemeColor('gray')

    h3 = ThemeColor('white')
    _h3 = ThemeColor('black')

    h4 = ThemeColor('white')
    _h4 = ThemeColor('gray')

    error = ThemeColor('white').set_luminance(.5)
    _error = ThemeColor('black').set_luminance(.5).set_saturation(.5)

    warning = ThemeColor('gray')
    _warning = ThemeColor('black').set_luminance(.5).set_saturation(.5)

    info = ThemeColor('gray').set_luminance(.5).set_saturation(.7)
    ok = ThemeColor('white').set_luminance(.5).set_saturation(.7)
