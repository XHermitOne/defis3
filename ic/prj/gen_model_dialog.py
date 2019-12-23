#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговое окно генерации модулей модели и менеджера модели.
"""

import wx
from . import gen_model_dialog_proto

from ic.db import icmodelmodulegenerator

from ic.db import icmodel

from ic.log import log

__version__ = (0, 1, 1, 1)


class icGenModelDialog(gen_model_dialog_proto.icGenModelDialogProto,
                       icmodelmodulegenerator.icModelModuleGenerator):
    """
    Диалоговое окно генерации модулей модели и менеджера модели.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        gen_model_dialog_proto.icGenModelDialogProto.__init__(self, *args, **kwargs)

    def init(self):
        """
        Инициализация.
        """
        self.init_image()
        self.init_ctrl()

    def init_image(self):
        """
        Инициализация изображений.
        """
        pass

    def init_ctrl(self):
        """
        Инициализация контролов.
        """
        scheme_dir = icmodel.getSchemeDir()
        self.dst_dirPicker.SetPath(scheme_dir)

    def onDstDirChanged(self, event):
        """
        Обработчик смены результирующей папки.
        """
        event.Skip()

    def onModelButtonClick(self, event):
        """
        Обработчик кнопки генерации модуля модели.
        """
        event.Skip()

    def onManagerButtonClick(self, event):
        """
        Обработчик кнопки генерации модуля менеджера модели.
        """
        event.Skip()

    def onCloseButtonClick(self, event):
        """
        Обработчик кнопки закрытия окна.
        """
        self.EndModal(wx.ID_OK)
        event.Skip()


def open_gen_model_dialog(parent=None, tab_res_filename=None):
    """
    Функция вызова диалогового окна генерации модулей модели и менеджера модели.

    :param parent: Родительское окно.
        Если не определено, то берется главное окно приложения.
    :param tab_res_filename: Полное имя файла ресурса таблицы, по
        которому производится генерация.
        Если не определено, то вызывается диалог выбора файла непосредственно.
    :return: True/False.
    """
    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    try:
        dlg = icGenModelDialog(parent=parent)
        dlg.init()

        dlg.ShowModal()

        return True
    except:
        log.fatal(u'Ошибка вызова диалогового окна генерации модулей модели и менеджера модели')
    return False

