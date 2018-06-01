from typing import Union, Tuple, TypeVar

import sys
import platform

import os
from colorhash import ColorHash
from colour import Color, COLOR_NAME_TO_RGB

IntervalValue = Union[int, float]
RGB255Tuple = Tuple[int, ...]
RGBTuple = Tuple[float, ...]

hex_characters = {c for c in '#0123456789abcdef'}


def map_interval(from_start: IntervalValue,
                 from_end: IntervalValue,
                 to_start: IntervalValue,
                 to_end: IntervalValue,
                 value: IntervalValue) -> IntervalValue:
    """
    Map numbers from an interval to another.

    >>> map_interval(0, 1, 0, 255, 0.5)
    127.5

    >>> map_interval(0, 255, 0, 1, 128)  # doctest: +ELLIPSIS
    0.50...

    :param from_start: lower bound of source interval.
    :param from_end: upper bound of source interval.
    :param to_start: lower bound of target interval.
    :param to_end: upper bound of target interval.
    :param value: source value to map to target interval.
    :return: value in target interval.
    """
    return ((value - from_start) * (to_end - to_start) /
            (from_end - from_start) + to_start)


def rgb_to_RGB255(rgb: RGBTuple) -> RGB255Tuple:
    """
    Convert from Color.rgb's 0-1 range to ANSI RGB (0-255) range.

    >>> rgb_to_RGB255((1, 0.5, 0))
    (255, 128, 0)
    """
    return tuple([int(round(map_interval(0, 1, 0, 255, c))) for c in rgb])


def RGB255_to_rgb(rgb: RGB255Tuple) -> RGBTuple:
    """
    Convert from ANSI RGB (0-255) range to Color.rgb (0-1) range.

    >>> RGB255_to_rgb((0, 128, 255))  # doctest: +ELLIPSIS
    (0.0, 0.50..., 1.0)
    """
    return tuple(map_interval(0, 255, 0, 1, c) for c in rgb)


def parse_color(color: str) -> Color:
    """
    Parse a string into a Color object.

    Supports strings of format:
        - "ffffff"
        - "#ffffff"
        - "orange" - names in CSS colors list.
        - any other string is hashed to a deterministic color.

    >>> c = parse_color('red')
    >>> c.get_hue() == Color('red').get_hue()
    True

    >>> c = parse_color('#00ff00')
    >>> c.get_hue() == Color('lime').get_hue()
    True

    >>> c = parse_color('test')
    >>> c.get_hue()  # doctest: +ELLIPSIS
    0.4419...
    """
    try:
        if isinstance(color, str):
            if len(color) == 6 and not set(color) - hex_characters:
                color = '#' + color
            elif (color.startswith('#') and len(color) == 7 and
                  not set(color.lower()) - hex_characters):
                pass
            elif color in COLOR_NAME_TO_RGB:
                pass
            else:
                return Color(ColorHash(color).hex)
            return Color(color)
        else:
            raise ValueError()
    except:
        raise ValueError('Cannot parse color: {!r},'
                         'expected a hex color, a color name,'
                         'or a tuple of 0-255 RGB values.'.format(color))


def terminal_colors(stream=sys.stdout) -> int:
    """
    Get number of supported ANSI colors for a stream.
    Defaults to sys.stdout.

    https://gist.github.com/XVilka/8346728

    >>> terminal_colors(sys.stderr)
    0
    """
    colors = 0
    if stream.isatty():
        if platform.system() == 'Windows':
            # colorama supports 8 ANSI colors
            # (and dim is same as normal)
            colors = 8
        elif os.environ.get('NO_COLOR', None) is not None:
            colors = 0
        elif os.environ.get('COLORTERM', '').lower() in ['truecolor', '24bit']:
            colors = -1
        else:
            # curses is used to autodetect terminal colors on *nix.
            try:
                from curses import setupterm, tigetnum

                setupterm()
                colors = max(0, tigetnum('colors'))
            except ImportError:
                pass
            except:
                pass
    return colors


def read_config(filename: os.PathLike = '~/.autopalette'):
    filename = os.environ.get('AUTOPALETTE_CONFIG', filename)
    filename = os.path.expanduser(filename)
    config = {}
    try:
        with open(filename, 'r') as infile:
            for line in infile.readlines():
                if line.strip().startswith('#'):
                    continue
                try:
                    k, v = line.split('=')
                    config.update({k.strip().lower(): v.strip().lower()})
                except:
                    raise ValueError('Cannot parse: {!r}'.format(line))
    except FileNotFoundError:
        pass
    return config


def select_palette(hint: Union[int, str]):
    from autopalette.palette import palette_map
    if hint == 0 or os.environ.get('NO_COLOR', None) is not None:
        return palette_map['0']
    config = read_config()
    palette = config.get('palette', hint)
    palette = os.environ.get('AUTOPALETTE', palette)
    palette = str(palette).lower()
    return palette_map[palette]


def select_render_engine(hint: Union[int, str]):
    """
    Automatically select appropriate render engine,
    hint is number of colors or value of $TERM.
    """
    from autopalette.render import render_map
    if hint == 0 or os.environ.get('NO_COLOR', None) is not None:
        return render_map['0']
    config = read_config()
    renderer = os.environ.get('TERM', hint)
    if os.environ.get('COLORTERM', renderer):
        renderer = os.environ.get('COLORTERM', renderer)
    renderer = config.get('renderer', renderer)
    renderer = os.environ.get('AUTOPALETTE_RENDERER', renderer)
    renderer = str(renderer).lower()
    return render_map[renderer]
