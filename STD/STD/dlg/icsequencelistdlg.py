#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Диалоговое окно организации последовательности списка.
"""

import wx
from . import sequence_list_dlg_proto
import ic
from ic.log import log

__version__ = (0, 0, 0, 1)


class icSequenceListDlg(sequence_list_dlg_proto.icSequenceListDlgProto):
    """
    Диалоговое окно организации последовательности списка.
    """

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


def sequence_list_dlg(parent=None, sequence_data=None, label_column=0):
    """
    Вызов диалогового окна для редактирования последовательностью записей.
    @param parent: Родительское окно.
        Если не определено, то берется лавное окно программы.
    @param sequence_data: Список-последовательность записей.
    @param label_column: Имя колонки - наименования записи.
    @return: Отредактированный список-пследовательность или
        None в случае ошибки/нажата <Отмена>.
    """
    if parent is None:
        parent = ic.getMainWin()

    if not sequence_data:
        log.warning(u'Не определена последовательность')
        sequence_data = list()

    dlg = icSequenceListDlg(parent=parent)
    dlg.sequence_control.setSequenceData(sequence_data)
    dlg.sequence_control.setLabelColumn(label_column)
    dlg.sequence_control.refreshSequence()
    result = dlg.ShowModal()

    if result == wx.ID_OK:
        return dlg.sequence_control.getSequenceData()

    return None