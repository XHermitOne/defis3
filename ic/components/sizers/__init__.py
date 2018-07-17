#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Пакет сайзеры.
"""

#
__version__ = (1, 0, 0, 3)


def icGetModulDict(dct):
    """
    Инициализация модулей сайзеров.
    """
    from . import icboxsizer
    from . import icspacesizer
    from . import icgridbagsizer
    from . import icstaticboxsizer

    dct[icboxsizer.ic_class_spc['type']] = icboxsizer
    dct[icspacesizer.ic_class_spc['type']] = icspacesizer
    dct[icgridbagsizer.ic_class_spc['type']] = icgridbagsizer
    dct[icstaticboxsizer.ic_class_spc['type']] = icstaticboxsizer

    return dct
