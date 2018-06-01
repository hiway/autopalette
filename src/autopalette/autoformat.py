import sys

import os
import sty

from autopalette import BasicTheme
from autopalette.colormatch import ColorPoint
from autopalette.colortrans import rgb2short
from autopalette.utils import (
    terminal_colors,
    select_render_engine,
    parse_color,
    select_palette,
)


class ColoredString(str):
    def __new__(cls, body, theme, key=''):
        return super().__new__(cls, body)

    def __init__(self, body, theme, key=''):
        super().__init__()
        self.theme = theme
        self.key = key
        self.render = self.theme.renderer.render
        self._render = self.theme.renderer._render

    @property
    def _raw(self):
        return super().__repr__()

    @property
    def _body(self):
        return super().__str__()

    def copy(self, body):
        return ColoredString(body, theme=self.theme)

    @property
    def id(self):
        if self.key:
            color = parse_color(self.key)
        else:
            color = parse_color(self._body)
        text = self.render(self._body, fg=color)
        return self.copy(text)

    @property
    def id256(self):
        if terminal_colors() == 0:
            return self.copy(self._body)
        if self.key:
            color = parse_color(self.key)
        else:
            color = parse_color(self._body)
        ansi = int(rgb2short(color.hex_l)[0])
        match = ColorPoint(source=color, target=color, ansi=ansi)
        text = self._render(self._body, fg=match)
        return self.copy(text)

    @property
    def p(self):
        text = self.theme.base(self._body)
        return self.copy(text)

    @property
    def light(self):
        text = self.theme.light(self._body)
        return self.copy(text)

    @property
    def dark(self):
        text = self.theme.dark(self._body)
        return self.copy(text)

    @property
    def h1(self):
        text = self.theme.h1(self._body)
        return self.copy(text)

    @property
    def h2(self):
        text = self.theme.h2(self._body)
        return self.copy(text)

    @property
    def h3(self):
        text = self.theme.h3(self._body)
        return self.copy(text)

    @property
    def h4(self):
        text = self.theme.h4(self._body)
        return self.copy(text)

    @property
    def li(self):
        text = self.theme.light('- ' + self._body)
        return self.copy(text)

    @property
    def err(self):
        text = self.theme.error(self._body)
        return self.copy(text)

    @property
    def warn(self):
        text = self.theme.warning(self._body)
        return self.copy(text)

    @property
    def info(self):
        text = self.theme.info(self._body)
        return self.copy(text)

    @property
    def ok(self):
        text = self.theme.ok(self._body)
        return self.copy(text)

    @property
    def b(self):
        if terminal_colors() == 0:
            return self.copy(self._body)
        text = self._body
        text = sty.ef.bold + text + sty.rs.all
        return self.copy(text)

    @property
    def i(self):
        if terminal_colors() == 0:
            return self.copy(self._body)
        text = self._body
        text = sty.ef.italic + text + sty.rs.all
        return self.copy(text)

    @property
    def u(self):
        if terminal_colors() == 0:
            return self.copy(self._body)
        text = self._body
        text = sty.ef.underl + text + sty.rs.all
        return self.copy(text)

    @property
    def r(self):
        if terminal_colors() == 0:
            return self.copy(self._body)
        text = self._body
        text = sty.ef.inverse + text + sty.rs.all
        return self.copy(text)

    @property
    def m(self):
        if terminal_colors() == 0:
            return self.copy(self._body)
        text = self._body
        text = sty.ef.dim + text + sty.rs.all
        return self.copy(text)

    @property
    def raw(self):
        return repr(self)


class AutoFormat(object):
    def __init__(self, term_colors=0,
                 renderer=None, palette=None,
                 theme=None):
        self.init(term_colors=term_colors,
                  renderer=renderer,
                  palette=palette,
                  theme=theme)

    def init(self,
             term_colors=0,
             renderer=None,
             palette=None,
             theme=None,
             fix_all=False,
             fix_text=False):
        self.term_colors = term_colors or terminal_colors(sys.stdout)
        self.renderer = renderer or select_render_engine(self.term_colors)
        self.palette = palette or select_palette(self.term_colors)
        self.theme = theme(palette=self.palette,
                           renderer=self.renderer) if theme else BasicTheme(
                palette=self.palette,
                renderer=self.renderer)
        self._need_text_fix = self.need_text_fix()
        self._need_emoji_fix = self.need_emoji_fix()
        if fix_all and self._need_emoji_fix:
            fix_text = True
            try:
                from emoji2text import emoji2text
                self.fix_emoji = emoji2text
            except ImportError:
                raise ImportError('Please install python package: emoji2text')
        if fix_text and self._need_text_fix:
            try:
                from ftfy import fix_text
                self.fix_text = fix_text
            except ImportError:
                raise ImportError('Please install python package: ftfy')

    def need_text_fix(self):
        if 0 <= self.term_colors <= 16:
            return True
        return False

    def need_emoji_fix(self):
        if 0 <= self.term_colors <= 16:
            return True
        return False

    def fix_text(self, text):
        return text

    def fix_emoji(self, text, sep):
        return text

    def __call__(self, content, *, key=''):
        if self._need_text_fix:
            content = self.fix_text(content)
        if self._need_emoji_fix:
            content = self.fix_emoji(content, ':')
        return ColoredString(content, theme=self.theme, key=key)
