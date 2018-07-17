#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль запуска.
"""

import sys
import ic.engine.main
import os.path

if not sys.argv[1:]:
    path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
    main_sys = path.split('/')[-1]
    args = ['-run', '-dbg', '%s/%s/' % (path, main_sys), '-s']
    ic.engine.main.main(args)
else:
    ic.engine.main.run()
