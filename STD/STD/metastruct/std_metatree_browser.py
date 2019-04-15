#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Контрол управления мета-деревьями и мета-итемами.
"""

import wx

from . import std_metatree_browser_proto

from ic.log import log
from ic.engine import ic_user
from ic.engine import form_manager

__version__ = (0, 1, 1, 1)


class icStdMetaTreeBrowser(std_metatree_browser_proto.icStdMetaTreeBrowserPanelProto,
                           form_manager.icFormManager):
    """
    Контрол управления мета-деревьями и мета-итемами.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        std_metatree_browser_proto.icStdMetaTreeBrowserPanelProto.__init__(self, *args, **kwargs)


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
            parent = ic_user.getMainWin()

        browser_panel = icStdMetaTreeBrowser(parent=parent)

        result = ic_user.addMainNotebookPage(browser_panel, title)
        return result is not None
    except:
        log.fatal(u'Ошибка вызова стандартного браузера в главном органайзере.')
    return False
