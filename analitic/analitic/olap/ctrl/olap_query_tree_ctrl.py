#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Контрол управления деревом запросов к OLAP кубам OLAP сервера.
"""

import wx
import wx.gizmos

from ic.engine import treectrl_manager
from ic.engine import stored_ctrl_manager
from ic.components import icwidget

__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_OLAPQUERYTREECTRL = {'__parent__': icwidget.SPC_IC_WIDGET,
                            '__attr_hlp__': {
                                             },
                            }


class icOLAPQueryTreeCtrlProto(wx.TreeCtrl,
                               treectrl_manager.icTreeCtrlManager,
                               stored_ctrl_manager.icStoredCtrlManager):
    """
    Контрол управления деревом запросов к OLAP кубам OLAP сервера.
    Абстрактный класс.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        wx.TreeCtrl.__init__(self, *args, **kwargs)

