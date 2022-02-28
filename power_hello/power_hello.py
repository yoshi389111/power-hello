#!/usr/bin/env python3
# (C) 2022 SATO, Yoshiyuki
# This software is released under the MIT License.
# https://opensource.org/licenses/mit-license.php


import argparse
import io
import random
import re
import sys
from typing import Dict, List, NamedTuple, Set

# from . import glyph_data
import glyph_data

# for setup.py
NAME = "power-hello"
VERSION = "0.1.0"
LICENSE = "MIT License"
DESCRIPTION = (
    "This command creates an SVG image of a powerful keystroke."
)
URL = "https://github.com/yoshi389111/power-hello"
AUTHOR = "yoshi389111"
AUTHOR_EMAIL = "yoshi.389111@gmail.com"

# constants
_GLYPH_WIDTH = glyph_data.GLYPH_WIDTH
_GLYPH_HEIGHT = glyph_data.GLYPH_HEIGHT
_MARGIN_TOP = _GLYPH_HEIGHT // 2
_MARGIN_LEFT = _GLYPH_WIDTH
_MARGIN_RIGHT = _GLYPH_WIDTH
_MARGIN_BOTTOM = _GLYPH_HEIGHT // 2

_WAIT_TOP = 0  # [ms]
_WAIT_LAST = 1000  # [ms]
_WAIT_STRONG = 1000  # [ms]
_WAIT_CLACK = 100  # [ms]


class CharInfo(NamedTuple):
    ch: str
    col: int
    wait: int  # [ms]


def power_hello(
        out: io.TextIOBase,
        content: str,
        foreground: str,
        background: str,
        strongcolor: str):

    glyphs = read_glyph()
    messages = split_content(content, glyphs)
    chars = existing_chars(content, glyphs)
    maxLength = max([len(message) for message in messages])

    canvas_width = _MARGIN_LEFT + _GLYPH_WIDTH * maxLength + _MARGIN_RIGHT
    canvas_height = _MARGIN_TOP + _GLYPH_HEIGHT + _MARGIN_BOTTOM
    out.write(
        '<svg xmlns="http://www.w3.org/2000/svg"' +
        ' width="{}px" height="{}px"'.format(
            canvas_width * 3,
            canvas_height * 3) +
        ' viewBox="0 0 {} {}">\n'.format(
            canvas_width,
            canvas_height))

    out.write("<defs>\n")
    for i in chars:
        out.write(
            '<symbol id="glyph{}"'.format(i) +
            ' viewBox="0 0 {} {}"'.format(_GLYPH_WIDTH, _GLYPH_HEIGHT) +
            ' width="{}" height="{}">\n'.format(_GLYPH_WIDTH, _GLYPH_HEIGHT))
        out.write('<path d="{}"/>\n'.format(glyphs[i]))
        out.write('</symbol>\n')
    out.write('</defs>\n')
    out.write(
        '<rect x="0" y="0" width="{}" height="{}" fill="{}"/>\n'.format(
            canvas_width,
            canvas_height,
            background))

    for y, message in enumerate(messages):
        total_time = sum(info.wait for info in message) + \
            _WAIT_TOP + _WAIT_LAST
        trigger = (
            "500ms;line{}.end".format(len(messages) - 1) if y == 0
            else "line{}.end".format(y - 1)
        )
        base_trigger = 'line{}.begin'.format(y)
        t3 = r3((total_time - _WAIT_LAST) / total_time)

        out.write('<g opacity="0">\n')
        out.write(
            '<animate attributeName="opacity"' +
            ' id="line{}"'.format(y) +
            ' begin="{}"'.format(trigger) +
            ' values="1;1;0"' +
            ' dur="{}ms"'.format(total_time) +
            ' keyTimes="0;{};1"'.format(t3) +
            '/>\n')
        out.write(
            '<animateTransform attributeName="transform"' +
            ' begin="{}"'.format(base_trigger) +
            ' type="translate"' +
            ' values="0 0;0 0;0 -{}"'.format(_GLYPH_HEIGHT) +
            ' dur="{}ms"'.format(total_time) +
            ' keyTimes="0;{};1"'.format(t3) +
            '/>\n')

        out.write('<g>\n')

        clack_values = create_clack_values(message)
        clack_keytimes = create_clack_keytimes(message, total_time)

        out.write(
            '<animateTransform attributeName="transform"' +
            ' begin="{}"'.format(base_trigger) +
            ' type="translate"' +
            ' values="{}"'.format(clack_values) +
            ' dur="{}ms"'.format(total_time) +
            ' keyTimes="{}"'.format(clack_keytimes) +
            '/>\n')

        now_time = _WAIT_TOP
        for info in message:
            xx = info.col * _GLYPH_WIDTH + _MARGIN_LEFT
            t1 = r3(now_time / total_time)
            t2 = r3((now_time + _WAIT_STRONG) / total_time)

            out.write(
                '<use href="#glyph{}" x="{}" y="{}" fill="{}">\n'
                .format(ord(info.ch), xx, _MARGIN_TOP, foreground))
            out.write(
                '<animate attributeName="fill"' +
                ' begin="{}"'.format(base_trigger) +
                ' values="{};{};{};{};{}"'.format(
                    background,
                    background,
                    strongcolor,
                    foreground,
                    foreground) +
                ' dur="{}ms"'.format(total_time) +
                ' keyTimes="0;{};{};{};1"'.format(t1, t1, t2) +
                '/>\n')
            if ord(info.ch) <= 0x20:
                out.write(
                    '<animate attributeName="opacity"' +
                    ' begin="{}"'.format(base_trigger) +
                    ' values="0;0;1;0;0"' +
                    ' dur="{}ms"'.format(total_time) +
                    ' keyTimes="0;{};{};{};1"'.format(t1, t1, t2) +
                    '/>\n')
            else:
                out.write(
                    '<animate attributeName="stroke"' +
                    ' begin="{}"'.format(base_trigger) +
                    ' values="{};{};{};{};{}"'.format(
                        background,
                        background,
                        strongcolor,
                        foreground,
                        foreground) +
                    ' dur="{}ms"'.format(total_time) +
                    ' keyTimes="0;{};{};{};1"'.format(t1, t1, t2) +
                    '/>\n')
                out.write(
                    '<animate attributeName="stroke-width"' +
                    ' begin="{}"'.format(base_trigger) +
                    ' values="0;0;0.7;0;0"' +
                    ' dur="{}ms"'.format(total_time) +
                    ' keyTimes="0;{};{};{};1"'.format(t1, t1, t2) +
                    '/>\n')

            out.write('</use>\n')
            now_time += info.wait
        out.write('</g>\n')
        out.write("</g>\n")
    out.write("</svg>\n")


def read_glyph() -> Dict[int, str]:
    return glyph_data.create()


def split_content(
    content: str,
    glyphs: Dict[int, str]
) -> List[List[CharInfo]]:

    messages: List[List[CharInfo]] = []
    for row in content.splitlines():
        chars = list(filter(lambda ch: ord(ch) in glyphs, row + '\n'))
        column = 0
        message: List[CharInfo] = []
        for i, ch in enumerate(chars):
            if ch == '\t':
                column = ((column + 4) // 4) * 4 - 1
            wait = 500 if i == len(chars) - 1 else (
                decide_wait_time(chars[i], chars[i + 1])
            )
            char_info = CharInfo(ch, column, wait)
            column += 1
            message.append(char_info)
        messages.append(message)
    return messages


def decide_wait_time(prev: str, next: str) -> int:
    # Alphabet is a quick keystroke.
    # However, word breaks in camelCase and PascalCase are excluded.
    base_wait = 200 if prev.isalpha() and next.isalpha() and not (
        prev.islower() and next.isupper()) else 500
    return base_wait + random.randint(0, 20) * 10


def existing_chars(content: str, glyphs: Dict[int, str]) -> Set[int]:
    chars: Set[int] = {ord('\n')}
    for ch in content:
        i = ord(ch)
        if i in glyphs:
            chars.add(i)
    return chars


def create_clack_values(message: List[CharInfo]) -> str:
    values = '0 0;'
    for info in message:
        if info.ch == '\n':
            (dx, dy) = (-1.2, 1.4)
        elif info.ch == '\t':
            (dx, dy) = (1, 1)
        else:
            dx = r3((
                random.randint(-1, 1) +
                random.randint(-1, 1)) / 3.0)
            dy = r3((random.randint(0, 3) + 3) / 5.0)
        values += '0 0;{} {};0 0;'.format(dx, dy)
    return values + '0 0'


def create_clack_keytimes(message: List[CharInfo], total_time: int) -> str:
    values = '0;'
    now_time = _WAIT_TOP
    for info in message:
        t1 = r3(now_time / total_time)
        t2 = r3((now_time + _WAIT_CLACK) / total_time)
        values += '{};{};{};'.format(t1, t1, t2)
        now_time += info.wait
    return values + '1'


# Round decimals to the nearest three digits.
def r3(value: float) -> str:
    """
    >>> r3(1.2345)
    1.234
    >>> r3(6.1000)
    6.1
    >>> r3(0.0000)
    0
    """
    return re.sub("\\.?0*$", '', '{:.3f}'.format(value))


def arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "MESSAGES", nargs='*', help="messages output to a svg file"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="{} {}".format(NAME, VERSION),
    )
    parser.add_argument(
        "-c",
        "--color",
        type=str,
        help="foreground color",
        default="white",
    )
    parser.add_argument(
        "-b",
        "--background",
        type=str,
        help="background color",
        default="black",
    )
    parser.add_argument(
        "-s",
        "--strong-color",
        type=str,
        help="strong color",
        default="#ff9123",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="output file path",
        default="-",
    )
    return parser


def main() -> None:
    parser = arg_parser()
    args = parser.parse_args()
    if len(args.MESSAGES) == 0:
        contents = sys.stdin.read()
    else:
        contents = "\n".join(args.MESSAGES)
    if args.output != '-':
        out = open(args.output, 'w')
    else:
        out = sys.stdout
    power_hello(out, contents, args.color, args.background, args.strong_color)
    if args.output != '-':
        out.close()


if __name__ == "__main__":
    main()
