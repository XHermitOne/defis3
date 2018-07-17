#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import winpdb
    winpdb.main()
except ImportError:
    print(u'WinPDB not installed')
    print(u'For installition use:')
    print(u'\tsudo apt install winpdb')
