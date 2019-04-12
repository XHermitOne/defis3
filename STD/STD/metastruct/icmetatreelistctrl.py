#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Контрол управления мета-деревьями.
"""

import wx
import wx.dataview

from ic.components import icwidget
from ic.log import log

__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_METATREELISTCTRL = {'metatree': None,    # Паспорт объекта описания мета-дерева
                           '__parent__': icwidget.SPC_IC_WIDGET,
                           '__attr_hlp__': {'metatree': u'Паспорт объекта описания мета-дерева',
                                            },
                           }


class icMetaTreeListCtrlProto(wx.dataview.TreeListCtrl):
    """
    Контрол управления мета-деревьями.
    Абстрактный класс.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        wx.dataview.TreeListCtrl.__init__(self, *args, **kwargs)

        # Объект
        self._metatree = None

    def setMetaTree(self, metatree=None):
        """
        Установить объект описания мета-дерева.
        @param metatree: Объект описания мета-дерева.
        """
        self._metatree = metatree