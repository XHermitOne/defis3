#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль запуска.
"""

import sys
import os.path

import ic.engine.main

__version__ = (0, 1, 1, 1)


if not sys.argv[1:]:
    path = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    main_sys = path.split(os.path.sep)[-1]
    args = ['-run', '-dbg', os.path.join(path, main_sys), '-s']
    ic.engine.main.main(args)
else:
    ic.engine.main.run()
