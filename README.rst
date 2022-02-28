===========
power-hello
===========

This command creates an SVG image of a powerful keystroke.

Supported character codes are in the range of ISO 8859-1(Latin-1)

Examples
========

::

    $ power-hello "Hello world." "Welcome to my GitHub." > sample1.svg

.. image:: docs/sample1.svg

::

    $ power-hello -c black -b white -s red -o sample2.svg \
     "Open browser" "Search for the code" "Control C" "Control V"

.. image:: docs/sample2.svg

::

    $ power-hello -c '#6b493d' -b '#fffeb8' -s '#ef454a' -o sample3.svg \
     "Laziness" "Impatience" "Hubris"

.. image:: docs/sample3.svg

::

    $ cat <<'EOD' | power-hello -c 'hsl(217,68%,37%)' -b transparent -s 'rgb(0,123,187)' -o sample4.svg
    NAME = 'power-hello'
    VERSION = '0.1.0'
    LICENSE = 'MIT License'
    if (you like it) follow && star
    EOD

.. image:: docs/sample4.svg


Requirements
============

* Python 3.5 or higher

Installation
============

Install
-------

::

    $ git clone https://github.com/yoshi389111/power-hello.git
    $ cd power-hello
    $ pip3 install -e .

or

::

    $ pip3 install git+https://github.com/yoshi389111/power-hello.git

Uninstall
---------

::

    $ pip3 uninstall power-hello

Usage
=====

Usage:
------

::

    power-hello -h
    power-hello -v
    power-hello [-c COLOR] [-b COLOR] [-s COLOR] [-o OUTPUT] [MESSAGES...]

Options:
--------

::

      MESSAGES...                     messages to output to the svg image (default: stdin)
      -h,        --help               show this help message and exit
      -v,        --version            show program's version number and exit
      -c COLOR,  --color COLOR        foreground color (default: black)
      -b COLOR,  --background COLOR   background color (default: white)
      -s COLOR,  --strong-color COLOR strong color (default: '#ff9123')
      -o OUTPUT, --output OUTPUT      output file path (default: stdout)


Copyright and License
=====================

Program
-------

Copyright (C) 2022 SATO, Yoshiyuki

This software is released under the MIT License.
https://opensource.org/licenses/mit-license.php

Glyphs
------

This glyph data is based on "Hack-Regular.ttf".

https://github.com/source-foundry/Hack

Copyright (c) 2018 Source Foundry Authors

MIT License
