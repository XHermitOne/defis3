#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Вызов диалогового окна создания ресурса метаданных.
"""

import copy
import wx

from . import new_metadata_resource_dlg_proto

from ic.log import log
from ic.engine import form_manager

from ic.PropertyEditor import select_component_menu


__version__ = (0, 1, 1, 1)

NONE_COMPONENT_NAME = u'Компонент не определен'


class icNewMetadataResourceDlg(new_metadata_resource_dlg_proto.icNewMetadataResourceDialogProto,
                               form_manager.icFormManager):
    """
    Диалоговое окно создания ресурса метаданных.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        new_metadata_resource_dlg_proto.icNewMetadataResourceDialogProto.__init__(self, *args, **kwargs)

        # Кортеж описания выбранног компонента. См icResTree.ObjectsInfo
        self.component_info = None

    def onCancelButtonClick(self, event):
        """
        Обработчик нажатия кнопки <Отмена>.
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        Обработчик нажатия кнопки <OK>.
        """
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onComponentButtonClick(self, event):
        """
        Обработчик кнопки выбора компонента.
        """
        self.component_info = select_component_menu.popup_component_menu(parent=self,
                                                                         button=self.component_button)
        if self.component_info:
            bitmap = self.component_info[1]
            component_name = self.component_info[3].get('type', NONE_COMPONENT_NAME)
            self.component_bitmap.SetBitmap(bitmap)
            self.component_textCtrl.SetValue(component_name)

        event.Skip()


def new_metadata_resource_dlg(parent=None, default_resource_name=None):
    """
    Вызвать диалоговое окно для выбора параметров
    для создания нового ресурса метаданных.
    @param parent: Родительское окно.
    @param default_resource_name: Имя ресурса по умолчанию.
    @return: Кортеж: (имя ресурса, ресурс выбранного компонента)
    """
    try:
        dlg = icNewMetadataResourceDlg(parent=parent)

        if default_resource_name:
            dlg.name_textCtrl.SetValue(default_resource_name)

        dlg.ShowModal()

        result = (dlg.name_textCtrl.GetValue(),
                  copy.deepcopy(dlg.component_info[3]) if dlg.component_info is not None else None)
        dlg.Destroy()
        return result
    except:
        log.fatal(u'Ошибка вызова диалогового окна создания ресурса метаданных')
    return None


def test(parent=None):
    """
    Тестовая функция.
    """
    frame = wx.Dialog(parent)
    button = wx.Button(parent=frame)
    # button2 = wx.Button(parent=frame)

    def on_test(event):
        select_component_menu.popup_component_menu(parent=frame,
                                                   button=button)
        event.Skip()

    button.Bind(wx.EVT_BUTTON, on_test, button)
    frame.ShowModal()
