from typing import Sequence, Union, Tuple

import kdtree

from colour import Color

AnsiCodeType = Union[str, int, Tuple[int, int, int]]


class ColorPoint(object):
    def __init__(self, source: Color, target: Color,
                 ansi: AnsiCodeType) -> None:
        """
        Map source color to target color, stores target
        ansi color ans a single int, a sequence of RGB  as ints
        or markup string.
        """
        self.source = source
        self.target = target
        self.ansi = ansi

    def __len__(self) -> int:
        """
        >>> cp = ColorPoint(Color('black'), Color('white'), '')
        >>> len(cp) == 3
        True
        """
        return 3

    def __getitem__(self, item) -> float:
        """
        >>> cp = ColorPoint(Color('#880073'), Color('white'), '')
        >>> cp[0]  # hue
        0.8590686274509803
        >>> cp[1]  # saturation
        1.0
        >>> cp[2]  # luminance
        0.26666666666666666
        """
        return self.source.hsl[item]

    def __repr__(self) -> str:
        return 'ColorPoint({!r} => {!r})'.format(self.source, self.target)


class ColorMatch(object):
    def __init__(self) -> None:
        self.tree = kdtree.create(dimensions=3)

    def add(self, source: Color, target: Color, ansi: AnsiCodeType) -> None:
        point = ColorPoint(source, target, ansi)
        self.tree.add(point)

    def match(self, color: Color) -> ColorPoint:
        """
        >>> cm = ColorMatch()
        >>> cm.add(Color('red'), Color('white'), '')
        >>> cm.add(Color('blue'), Color('white'), '')
        >>> cm.match(Color('yellow'))
        ColorPoint(<Color red> => <Color white>)
        """
        results = self.tree.search_nn(color.hsl)
        if not results:
            raise KeyError('No match found for color: {}'.format(color))
        return results[0].data


