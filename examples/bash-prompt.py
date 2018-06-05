#!/usr/bin/env python3
import unicodedata
import grapheme
from autopalette import af

af.init(term_colors=256)


def save_cursor():
    return f'\x1b[s'


def restore_cursor():
    return f'\x1b[u'


def move_cursor_left(n):
    return f'\x1b[{n}D'


def adjust_spaces(text):
    fixed_length = len(unicodedata.normalize('NFKD', text))
    unicode_length = grapheme.length(text)
    if unicode_length != fixed_length:
        _text = ' ' * fixed_length
        _text += save_cursor()
        _text += move_cursor_left(fixed_length)
        _text += unicodedata.normalize('NFKD', text)
        _text += restore_cursor()
        return _text
    return text


# --- default (fast), render colors once and let bash render prompt variables.
##
### export PS1="$(~/bin/bash-prompt.py)"

username = r'\u'
hostname = r'\H'
local_time = r'\A '
utc_time = r'$( date -u "+%H:%M" ) '
working_dir = r'\w'

# --- alternative (slow), render full prompt via Python every time.
##
### export PS1="\$(~/bin/bash-prompt.py)"
#
# import datetime
# import getpass
# import os
# import platform
#
# username = getpass.getuser()
# hostname = platform.node()
# local_time = datetime.datetime.now().strftime('%H:%M ')
# utc_time = datetime.datetime.utcnow().strftime('%H:%M ')
# working_dir = os.getcwd().replace(os.path.expanduser('~'), '~')

prompt = r''
prompt += adjust_spaces("🇮🇳")
prompt += local_time
prompt += adjust_spaces("🌍")
prompt += utc_time
prompt += af(username).id256
prompt += '@'
prompt += af(hostname).id256
prompt += af(':' + working_dir).dark
prompt += af('\n$ ')

print(prompt)
