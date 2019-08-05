#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Контрол управления мета-деревьями и мета-итемами.
"""

import wx

from . import std_metatree_browser_proto

from ic.log import log
from ic.engine import glob_functions
from ic.engine import form_manager
from ic.components import icwidget

__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_STDMETATREEBROWSER = {'name': 'default',
                             '__parent__': icwidget.SPC_IC_WIDGET,
                             }


class icStdMetaTreeBrowserProto(std_metatree_browser_proto.icStdMetaTreeBrowserPanelProto,
                                form_manager.icFormManager):
    """
    Контрол управления мета-деревьями и мета-итемами.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        std_metatree_browser_proto.icStdMetaTreeBrowserPanelProto.__init__(self, *args, **kwargs)

    def setMetaTree(self, metatree=None):
        """
        Установить метадерево.
        @param metatree: Объект метадерева.
        """
        return self.metatree_list_ctrl.setMetaTree(metatree)


def browse_metatree_std_panel(parent=None, title=u''):
    """
    Функция вызова стандартного браузера в главном органайзере.
    @param parent: Родительское окно.
        Если не определено, то берется главное окно.
    @param title: Заголовок.
    @return: True/False.
    """
    try:
        if parent is None:
            parent = glob_functions.getMainWin()

        browser_panel = icStdMetaTreeBrowserProto(parent=parent)

        result = glob_functions.addMainNotebookPage(browser_panel, title)
        return result is not None
    except:
        log.fatal(u'Ошибка вызова стандартного браузера в главном органайзере.')
    return False
