#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Расширенный контрол выбора элемента справочника в виде выпадающего дерева справочника.

---------------------------------------------
|                   | V ||<x]||...|| / || ? |
| +                 |-----------------------
| --+---<..>        | ^    ^   ^     ^    ^
|   |               | |    |   |     |    -------
|   ----<..>        | |    |   |     ---------- |
--------------------- |    |   -------------- | |
                      |    ------           | | |
Вызов контрола выбора из дерева |           | | |
Сброс значения контрола справочника в None  | | |
Вызов формы поиска/выбора ------------------- | |
Вызов формы редактирования--------------------  |
Вызов всплывающего окна с описанием справочника-
"""

import wx

from ic.log import log
from ic.components import icwidget
from ic.utils import wxfunc
from . import ext_sprav_tree_choice_panel_proto
from NSI.nsi_dlg import icspraveditdlg
from NSI.nsi_dlg import icspravchoicetreedlg

# Version
__version__ = (0, 1, 1, 1)

SPC_IC_EXTSPRAVTREECHOICE = {'sprav': None,      # Паспорт справочника-источника данных
                             'root_code': None,  # Код корневого элемента ветки справочника
                             'view_all': False,  # Показывать все элементы справочника
                             'level_enable': -1,  # Номер уровня с которого включаются элементы для выбора
                             'expand': True,      # Распахнуть

                             'get_label': None,  # Функция определения надписи элемента дерева
                             'find_item': None,  # Функция поиска элемента дерева
                             'is_choice_list': False,
                             'get_selected_code': None,  # Функция получения выбранного кода
                             'set_selected_code': None,  # Функция установки выбранного кода

                             '__parent__': icwidget.SPC_IC_WIDGET,
                             }


class icExtSpravTreeChoicePrototype(ext_sprav_tree_choice_panel_proto.icExtSpravTreeChoicePanelProto):
    """
    Расширенный контрол выбора элемента справочника в виде выпадающего дерева справочника.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        ext_sprav_tree_choice_panel_proto.icExtSpravTreeChoicePanelProto.__init__(self, *args, **kwargs)

        # Всплывающее окно помощи
        self.help_popup_win = None

    def onClearButtonClick(self, event):
        """
        Обработчик кнопки очистки значения
        """
        self.sprav_tree_choice.setValue(None)
        event.Skip()

    def onFindButtonClick(self, event):
        """
        Обработчик кнопки вызова формы поиска в справочнике.
        """
        sprav = self.sprav_tree_choice.getSprav()
        if sprav:
            icspravchoicetreedlg.choice_sprav_dlg(parent=self, nsi_sprav=sprav)
        else:
            log.warning(u'Не определен справочник в контроле выбора из дерева справочника')
        event.Skip()

    def onEditButtonClick(self, event):
        """
        Обработчик кнопки вызова формы редактирования справочника.
        """
        sprav = self.sprav_tree_choice.getSprav()
        if sprav:
            icspraveditdlg.edit_sprav_dlg(parent=self, nsi_sprav=sprav)
        else:
            log.warning(u'Не определен справочник в контроле выбора из дерева справочника')
        event.Skip()

    def onHelpButtonClick(self, event):
        """
        Обработчик вызова всплывающего окна с описанием справочника.
        """
        if self.help_popup_win is None:
            sprav = self.sprav_tree_choice.getSprav()
            if sprav:
                description = sprav.getDescription()
                self.help_popup_win = wxfunc.showInfoWindow(parent=self, ctrl=self.help_button, info_text=description)
            else:
                log.warning(u'Не определен справочник в контроле выбора из дерева справочника')
        else:
            self.help_popup_win.Close()
            self.help_popup_win = None
        event.Skip()


def test_ctrl():
    """
    Тестовая функция.
    """
    app = wx.PySimpleApp()
    frame = wx.Frame(None)
    # sprav_psp = (('Sprav', 'Regions', None, 'nsi_sprav.mtd', 'NSI'),)
    tree_combo_ctrl = icExtSpravTreeChoicePrototype(parent=frame)
    button = wx.Button(frame, pos=wx.Point(10, 100))
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    test_ctrl()
