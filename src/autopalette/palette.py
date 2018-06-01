from typing import List

from colour import Color

from autopalette.colormatch import ColorPoint, ColorMatch, AnsiCodeType
from autopalette.utils import parse_color, map_interval
from colortrans import rgb2short, short2rgb


class BasePalette(object):
    def match(self, color: Color) -> ColorPoint:
        raise NotImplementedError()


class Ansi256Palette(BasePalette):
    def match(self, color: Color, ansi=False) -> ColorPoint:
        ansi = int(rgb2short(color.hex_l)[0])
        target = Color('#' + short2rgb(str(ansi)))
        return ColorPoint(color, target, ansi=ansi)


class AutoPalette(BasePalette):
    def __init__(self, colors: List[dict] = None):
        self.tree = ColorMatch()
        if not colors:
            colors = getattr(self, 'colors', {})
        if isinstance(colors, dict):
            self.colors = self.colors_from_dict(colors)
        else:
            raise ValueError('Expected a dict for colors with the format => '
                             'source-color: (target-color, target-ansi-code). '
                             'Got: {}'.format(colors))
        for color, data in self.colors.items():
            self.add_color(source=data['source'],
                           target=data['target'],
                           ansi=data['ansi'])

    def colors_from_dict(self, colors: dict) -> dict:
        new_colors = {}
        for clr_name, payload in colors.items():
            if not 'source' in payload:
                color = parse_color(clr_name)
                color_hex = color.hex_l
                target = parse_color(payload[0])
                ansi = payload[1]
                new_colors.update({color_hex: {'source': color,
                                               'target': target,
                                               'ansi':   ansi}})
            else:
                color_hex = payload['source'].hex_l
                new_colors.update({color_hex: {'source': payload['source'],
                                               'target': payload['target'].hex_l,
                                               'ansi':   payload['ansi']}})
        return new_colors

    def add_color(self, source: Color, target: Color, ansi: AnsiCodeType):
        self.tree.add(source, target, ansi)

    def match(self, color: Color, ansi=False) -> ColorPoint:
        match = self.tree.match(color)
        return match


class Ansi8Palette(AutoPalette):
    colors = {
        'black':   ('#000000', 0),
        'red':     ('#ff0000', 1),
        'lime':    ('#00ff00', 2),
        'yellow':  ('#ffff00', 3),
        'blue':    ('#0000ff', 4),
        'magenta': ('#ff00ff', 5),
        'cyan':    ('#00ffff', 6),
        'white':   ('#ffffff', 7),
    }
    #   ^^ source   ^^ target  ^^ ansi-code


class Ansi16Palette(AutoPalette):
    colors = {
        'black':       ('black', 0),
        'darkred':     ('darkred', 1),
        'green':       ('darkgreen', 2),
        'orange':      ('orange', 3),
        'darkblue':    ('darkblue', 4),
        'darkmagenta': ('darkmagenta', 5),
        'darkcyan':    ('darkcyan', 6),
        'silver':      ('silver', 7),
        'gray':        ('gray', 8),
        'red':         ('red', 9),
        'lime':        ('green', 10),
        'yellow':      ('yellow', 11),
        'blue':        ('blue', 12),
        'magenta':     ('magenta', 13),
        'cyan':        ('cyan', 14),
        'white':       ('white', 15),
    }
    #   ^^ source       ^^ target ^^ ansi-code


class Gray4Palette(AutoPalette):
    """
    A 4-bit grayscale palette, desaturates and maps all colors
    to one of four target shades.
    """
    colors = {
        'black':  ('#000000', 0),
        'silver': ('#676767', 8),
        'blue':   ('#b6b6b6', 7),
        'yellow': ('#b6b6b6', 0),
        'white':  ('#fafafa', 15),
    }

    #   ^^ source   ^^ target  ^^ ansi-code

    def match(self, color: Color, ansi=False) -> ColorPoint:
        if not ansi:
            return super().match(color)
        color.set_saturation(0.3)
        return super(Gray4Palette, self).match(color)


class Oil6Palette(AutoPalette):
    """
    Source: https://lospec.com/palette-list/oil-6
    """
    colors = {
        'white':     ('#fbf5ef', 91),
        'silver':    ('#f2d3ab', 11),
        'lightgray': ('#c69fa5', 139),
        'gray':      ('#8b6d9c', 5),
        'darkgray':  ('#494d7e', 98),
        'black':     ('#272744', 0),
    }

    #   ^^ source       ^^ target ^^ ansi-code

    def match(self, color: Color, ansi=False) -> ColorPoint:
        lum = map_interval(0, 1, .3, .9, color.get_luminance())
        color.set_luminance(lum)
        sat = map_interval(0, 1, .2, .9, color.get_saturation())
        color.set_saturation(sat)
        return super().match(color)


class GameBoyChocolatePalette(AutoPalette):
    """
    Source: https://lospec.com/palette-list/gb-chocolate
    """
    colors = {
        'white':  ('#ffe4c2', 15),
        'silver': ('#dca456', 3),
        'gray':   ('#a9604c', 1),
        'black':  ('#422936', 0),
    }

    #   ^^ source       ^^ target ^^ ansi-code

    def match(self, color: Color, ansi=False) -> ColorPoint:
        lum = map_interval(0, 1, .2, .9, color.get_luminance())
        color.set_luminance(lum)
        return super().match(color)


class GameBoyGreenPalette(AutoPalette):
    """
    Source: https://www.designpieces.com/palette/ \
                game-boy-original-color-palette-hex-and-rgb/
    """
    colors = {
        'white':  ('green', 10),  # help auto conversion with a brighter color.
        'yellow': ('#9bbc0f', 15),
        'green':  ('#8bac0f', 10),
        'gray':   ('#306230', 2),
        'black':  ('#0f380f', 0),
    }

    #   ^^ source       ^^ target ^^ ansi-code

    def match(self, color: Color, ansi=False) -> ColorPoint:
        lum = map_interval(0, 1, .3, .85, color.get_luminance())
        color.set_luminance(lum)
        return super().match(color)


class ColorsCCPalette(AutoPalette):
    """
    Source: https://clrs.cc/
    Also see: https://clrs.cc/a11y/
    """
    colors = {
        'navy':    ('#001f3f', 4),
        'blue':    ('#0074D9', 12),
        'aqua':    ('#7FDBFF', 14),
        'teal':    ('#39CCCC', 6),
        'olive':   ('#3D9970', 3),
        'green':   ('#2ECC40', 2),
        'lime':    ('#01FF70', 10),
        'yellow':  ('#FFDC00', 11),
        'orange':  ('#FF851B', 3),
        'red':     ('#FF4136', 9),
        'maroon':  ('#85144b', 1),
        'fuchsia': ('#F012BE', 13),
        'purple':  ('#B10DC9', 5),
        'black':   ('#111111', 0),
        'gray':    ('#AAAAAA', 8),
        'silver':  ('#DDDDDD', 7),
        'white':   ('#FFFFFF', 15),
    }
    #   ^^ source       ^^ target ^^ ansi-code


class BasicPalette(AutoPalette):
    colors = {
        'black':     ('#000000', 0),
        'silver':    ('#eaebbc', 7),
        'gray':      ('#286c80', 8),
        'purple':    ('#8339a0', 5),
        'blue':      ('#0059c8', 4),
        'lightblue': ('#2f9ffa', 12),
        'magenta':   ('#ea75f9', 13),
        'red':       ('#ed452f', 9),
        'orange':    ('#ec835b', 3),
        'yellow':    ('#f3e945', 11),
        'lime':      ('#9df381', 10),
        'green':     ('#47AA49', 2),
        'white':     ('#ffffff', 15),
    }

    #   ^^ source   ^^ target  ^^ ansi-code

    def match(self, color: Color, ansi=False) -> ColorPoint:
        lum = map_interval(0, 1, .2, 1, color.get_luminance())
        color.set_luminance(lum)
        return super().match(color)


class DutronPalette(AutoPalette):
    colors = {
        'black':     ('#000000', 0),
        'silver':    ('#94945d', 7),
        'gray':      ('#595d82', 8),
        'purple':    ('#415ac4', 4),
        'blue':      ('#7e8ff8', 4),
        'lightblue': ('#8384fb', 12),
        'magenta':   ('#a2adf4', 12),
        'red':       ('#585539', 3),
        'orange':    ('#a7a24f', 3),
        'yellow':    ('#f2e745', 11),
        'lime':      ('#e4dd88', 11),
        'green':     ('#82844B', 3),
        'white':     ('#ffffff', 15),
    }
    #   ^^ source   ^^ target  ^^ ansi-code


palette_map = {
    '-1':               BasicPalette,
    '0':                Ansi8Palette,
    '8':                Ansi8Palette,
    '16':               Ansi16Palette,
    '88':               Ansi256Palette,
    '256':              Ansi256Palette,
    'ansi':             Ansi256Palette,
    'rgb':              Ansi256Palette,
    'truecolor':        Ansi256Palette,
    'vt100':            Ansi8Palette,
    'vt200':            Ansi8Palette,
    'vt220':            Ansi8Palette,
    'rxvt':             Ansi8Palette,
    'rxvt-88color':     Ansi256Palette,
    'xterm':            Ansi8Palette,
    'xterm-color':      Ansi16Palette,
    'xterm-256color':   Ansi256Palette,
    'dutron':           DutronPalette,
    'gameboychocolate': GameBoyChocolatePalette,
    'gameboygreen':     GameBoyGreenPalette,
    'gray4':            Gray4Palette,
    'oil6':             Oil6Palette,
    'basic':            BasicPalette,
}
