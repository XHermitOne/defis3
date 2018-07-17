#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------
# Name:        treeReestrInterface.py
# Purpose:     Интерфейс древовидного реестра.
#
# Author:      <Okoneshnikov A. V.>
#
# Created:     05.06.06
# Copyright:   (c) 2006 Infocenter
# Licence:     <your licence>
# -----------------------------------------------------------------------------
"""
# Версия
__version__ = (0, 0, 0, 1)

import STD.interfaces.reestr.reestrInterface as reestr

class icTreeReestrInterface(reestr.icBaseReestrInterface):
    """
    """
    def __init__(self, *arg, **kwarg):
        """
        """
        reestr.icBaseReestrInterface.__init__(self, *arg, **kwarg)