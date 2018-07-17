#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Defis setup script
#
# USAGE:
# python setup.py install
#
# Used for installations:
#   - create ic.path in .../site-packages/ direcory

import sys


def get_site_packages():
    for el in sys.path:
        if 'site-packages' in el:
            return el.replace('\\', '/').split('site-packages')[0] + 'site-packages'


def setup(*arg, **kwarg):
    if sys.argv[1:] and sys.argv[1] == 'install':
        from os.path import dirname, abspath
        path = dirname(abspath(__file__)).replace('\\', '/')
        sp = get_site_packages()
        f = open('%s/ic.pth' % sp, 'wb+')
        f.write(path)
        f.close()
        print('ic.pth is copied to %s' % sp)


if __name__ == '__main__':
    setup()
