#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Диалоговая форма выбора принтера установленного в системе.
"""

import sys
import wx
from . import printer_dlg_proto
from ic.bitmap import ic_bmp
from ic.utils import printerfunc


class icChoicePrinterDlg(printer_dlg_proto.icChoicePrinterDlgProto):
    """
    Диалоговая форма выбора принтера установленного в системе.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        printer_dlg_proto.icChoicePrinterDlgProto.__init__(self, *args, **kwargs)

        self.selected_printer_info = None
        self.init()

    def init(self):
        """
        Инициализация диалогового окна.
        """
        self.init_images()
        self.init_printers()

    def init_images(self):
        """
        Инициализация образов.
        """
        # Поддержка картинок в <ListCtrl>
        self.image_list = wx.ImageList(16, 16)
        bmp = ic_bmp.createLibraryBitmap('printer-monochrome.png')
        self.printer_idx = self.image_list.Add(bmp)
        bmp = ic_bmp.createLibraryBitmap('printer--arrow.png')
        self.default_printer_idx = self.image_list.Add(bmp)
        bmp = ic_bmp.createLibraryBitmap('printer-network.png')
        self.network_printer_idx = self.image_list.Add(bmp)
        self.printer_listCtrl.SetImageList(self.image_list, wx.IMAGE_LIST_SMALL)

    def init_printers(self):
        """
        Инициализация списка принтеров.
        ВНИМАНИЕ! Для корректного отображения иконок в
            элементах списка ListCtrl необходимо
            в стиле контрола указать wx.LC_LIST.
        """
        self.printers_info = printerfunc.getPrintersInfo()

        self.printer_listCtrl.DeleteAllItems()
        default_idx = -1
        for i, info in enumerate(self.printers_info):
            is_default = info[0]
            printer_name = info[1]
            is_network = info[2]

            if is_default:
                default_idx = i

            if is_default:
                img_idx = self.default_printer_idx
            elif is_network:
                img_idx = self.network_printer_idx
            else:
                img_idx = self.printer_idx
            self.printer_listCtrl.InsertImageStringItem(sys.maxint, printer_name, img_idx)

        # Выделить принтер по умолчанию
        if default_idx >= 0:
            self.printer_listCtrl.Select(default_idx)

    def onOkButtonClick(self, event):
        """
        Обработчик кнопки <OK>
        """
        idx = self.printer_listCtrl.GetFirstSelected()
        if idx == -1:
            # Если не выбран ни один принтер
            # считаем что выбран принтер по умолчанию
            find_default = [info for info in self.printers_info if info[0]]
            self.selected_printer_info = find_default[0] if find_default else None
        else:
            self.selected_printer_info = self.printers_info[idx]
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onCancelButtonClick(self, event):
        """
        Обработчик кнопки <Отмена>
        """
        self.selected_printer_info = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def getSelectedPrinterInfo(self):
        """
        Информация о выбранном принтере в виде словаря формата:
            {
                'name': 'Имя принтера',
                'default': True - Принтер является принтером по умолчанию.
                           False - Обычный принтер
                'network': True - Принтер является сетевым принтером.
                           False - Локальный принтер
            }
        """
        if self.selected_printer_info:
            return dict(name=self.selected_printer_info[1],
                        default=self.selected_printer_info[0],
                        network=self.selected_printer_info[2])
        return None


def choice_printer_dlg(parent=None):
    """
    Выбрать установленный в системе принтер с помощью диалогового окна.
    @param parent: Родительское окно.
    @return: Информация о выбранном принтере в виде словаря формата:
            {
                'name': 'Имя принтера',
                'default': True - Принтер является принтером по умолчанию.
                           False - Обычный принтер
                'network': True - Принтер является сетевым принтером.
                           False - Локальный принтер
            }
        Либо None если нажата <Отмена>.
    """
    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    dlg = icChoicePrinterDlg(parent=parent)
    result = dlg.ShowModal()

    ret = None
    if result == wx.ID_OK:
        ret = dlg.getSelectedPrinterInfo()

    dlg.Destroy()
    return ret


def test():
    """
    Функция тестирования.
    """
    app = wx.PySimpleApp()

    dlg = icChoicePrinterDlg(None)
    dlg.ShowModal()
    dlg.Destroy()
    dlg = None
    app.MainLoop()


if __name__ == '__main__':
    test()
