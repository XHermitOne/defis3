#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль формы <icPackScanDocPanelProto>. 
Сгенерирован проектом DEFIS по модулю формы-прототипа wxFormBuider.
"""

import wx
import pack_scan_doc_panel_proto

import ic
from ic.log import log

# Для управления взаимодействия с контролами wxPython
# используется менеджер форм <form_manager.icFormManager>
from ic.engine import form_manager


class icPackScanDocPanel(pack_scan_doc_panel_proto.icPackScanDocPanelProto, form_manager.icFormManager):
    """
    Форма .
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        pack_scan_doc_panel_proto.icPackScanDocPanelProto.__init__(self, *args, **kwargs)

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
        
    def onArchiveToolClicked(self, event):

        event.Skip()

    def onEditToolClicked(self, event):

        event.Skip()

    def onGroupToolClicked(self, event):

        event.Skip()

    def onImportToolClicked(self, event):

        event.Skip()

    def onNPagesToolClicked(self, event):

        event.Skip()

    def onQuickToolClicked(self, event):

        event.Skip()

    def onScanToolClicked(self, event):

        event.Skip()

    def onToggleCheckBox(self, event):

        event.Skip()

    def onViewToolClicked(self, event):

        event.Skip()


def show_pack_scan_doc_panel(title=u''):
    """
    @param title: Заголовок страницы нотебука главного окна.
    """
    try:
        main_win = ic.getMainWin()
        
        panel = icPackScanDocPanel(main_win)
        panel.init()
        main_win.AddPage(panel, title)
    except:
        log.fatal(u'Ошибка')    

