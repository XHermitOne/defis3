#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль формы <icGroupManipulationDlgProto>. 
Сгенерирован проектом DEFIS по модулю формы-прототипа wxFormBuider.
"""

import wx
import group_manipulation_dlg_proto

import ic
from ic.log import log

# Для управления взаимодействия с контролами wxPython
# используется менеджер форм <form_manager.icFormManager>
from ic.engine import form_manager


class icGroupManipulationDlg(group_manipulation_dlg_proto.icGroupManipulationDlgProto, 
                             form_manager.icFormManager):
    """
    Форма пареметров групповой обработки в режиме пакетного сканирования.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        group_manipulation_dlg_proto.icGroupManipulationDlgProto.__init__(self, *args, **kwargs)

        # Отредактированное значение параметров групповой обработки
        self._value = dict(n_begin=None, n_end=None,
                           on_off=None, 
                           n_pages=None, is_duplex=None)
        
    def init(self, n_min=1, n_max=100):
        """
        Инициализация панели.
        @param n_min: Диапазон возможных номеров. Минимальное значение.
        @param n_max: Диапазон возможных номеров. Максимальное значение.
        """
        self.init_img()
        self.init_ctrl(n_min, n_max)
        
    def init_img(self):
        """
        Инициализация изображений.
        """
        pass
        
    def init_ctrl(self, n_min=1, n_max=100):
        """
        Инициализация контролов.
        @param n_min: Диапазон возможных номеров. Минимальное значение.
        @param n_max: Диапазон возможных номеров. Максимальное значение.
        """
        self.begin_spinCtrl.SetRange(n_min, n_max)
        self.begin_spinCtrl.SetValue(n_min)
        
        self.end_spinCtrl.SetRange(n_min, n_max)
        self.end_spinCtrl.SetValue(n_max)
        
    def onBeginSpinCtrl(self, event):
        """
        Обработчик изменения значения первого номера диапазона группы.
        """
        value = self.begin_spinCtrl.GetValue()
        if value > self.end_spinCtrl.GetValue():
            self.end_spinCtrl.SetValue(value)
        event.Skip()

    def onCancelButtonClick(self, event):
        """
        Обработчик кнопки <Отмена>.
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onEndSpinCtrl(self, event):
        """
        Обработчик изменения значения последнего номера диапазона группы.
        """
        value = self.end_spinCtrl.GetValue()
        if value < self.begin_spinCtrl.GetValue():
            self.begin_spinCtrl.SetValue(value)
        event.Skip()

    def onExtOptionsCheckBox(self, event):
        """
        Вкл./Выкл. дополнительных параметров групповой обработки.
        """
        check = event.IsChecked()
        
        self.pages_staticText.Enable(check)
        self.pages_spinCtrl.Enable(check)
        self.duplex_checkBox.Enable(check)
            
        event.Skip()

    def onOkButtonClick(self, event):
        """
        Обработчик кнопки <OK>.
        """
        self.readValue()
        self.EndModal(wx.ID_OK)
        event.Skip()

    def readValue(self):
        """
        Запомнить отредактированные параметры групповой обработки.
        """
        self._value['n_begin'] = self.begin_spinCtrl.GetValue()
        self._value['n_end'] = self.end_spinCtrl.GetValue()
        self._value['on_off'] = self.on_off_checkBox.IsChecked()
        
        self._value['n_pages'] = self.pages_spinCtrl.GetValue() if self.pages_spinCtrl.IsEnabled() else None
        self._value['is_duplex'] = self.duplex_checkBox.IsChecked() if self.duplex_checkBox.IsEnabled() else None
        
    def getValue(self):
        """
        Отредактированные параметры групповой обработки.
        """
        return self._value


def show_group_manipulation_dlg(parent=None, n_min=1, n_max=100, position=None):
    """
    Открыть форму пареметров групповой обработки в режиме пакетного сканирования.
    @param parent: Родительское окно.
    @param n_min: Диапазон возможных номеров. Минимальное значение.
    @param n_max: Диапазон возможных номеров. Максимальное значение.
    @param position: Позиция вывода диалогового окна.
    @return: True/False.
    """
    if parent is None:
        parent = ic.getMainWin()

    dlg = icGroupManipulationDlg(parent)
    if position:
        dlg.SetPosition(position)
    dlg.init(n_min, n_max)
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        return dlg.getValue()
    return None
