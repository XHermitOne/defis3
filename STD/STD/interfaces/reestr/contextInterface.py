#!/usr/bin/env python
#  -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# Name:        contextInterface.py
# Purpose:     Интерфейс задает контекст реестра.
#
# Author:      <Okoneshnikov A. V.>
#
# Created:     05.06.06
# Copyright:   (c) 2006 Infocenter
# Licence:     <your licence>
# -----------------------------------------------------------------------------

"""
Интерфейс задает контекст реестра.
Автор(ы): Оконешников А.В.
"""

# Версия
__version__ = (0, 0, 0, 1)

import ic.kernel.icContext as context

class icReestrContextInterface(context.Context):
    """
    Интерфейс контекста реестра.
    """
    def __init__(self, *arg, **kwarg):
        """
        Конструктор.
        """
        context.Context.__init__(self, *arg, **kwarg)