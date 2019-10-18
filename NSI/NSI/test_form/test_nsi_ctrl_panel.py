#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль формы <icTestNSICtrlPanelProto>.
Сгенерирован проектом DEFIS по модулю формы-прототипа wxFormBuider.
"""

import wx
from . import test_nsi_form_proto

import ic
from ic.log import log

# Для управления взаимодействия с контролами wxPython
# используется менеджер форм <form_manager.icFormManager>
from ic.engine import form_manager

__version__ = (0, 0, 0, 1)


class icTestNSICtrlPanel(test_nsi_form_proto.icTestNSICtrlPanelProto, form_manager.icFormManager):
    """
    Форма .
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        test_nsi_form_proto.icTestNSICtrlPanelProto.__init__(self, *args, **kwargs)

    def init(self):
        """
        Инициализация панели.
        """
        self.init_img()
        self.init_ctrl()

    def init_img(self):
        """
        Инициализация изображений.
        """
        pass

    def init_ctrl(self):
        """
        Инициализация контролов.
        """
        pass



def show_test_nsi_ctrl_panel(parent=None, title=u''):
    """
    @param parent: Родительское окно.
        Если не определено, то берется главное окно.
    @param title: Заголовок страницы нотебука главного окна.
    """
    try:
        main_win = ic.getMainWin()
        if parent is None:
            parent = main_win

        panel = icTestNSICtrlPanel(parent)
        panel.init()
        main_win.addPage(panel, title)
    except:
        log.fatal(u'Ошибка')

