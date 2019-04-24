#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговая форма тестирования OLAP сервера Cubes.
"""

import wx
from . import cubes_olap_srv_test_dlg

from ic.log import log

__version__ = (0, 1, 1, 1)


class icCubesOLAPSrvTestDialog(cubes_olap_srv_test_dlg.icCubesOLAPSrvTestDialogProto):
    """
    Диалоговая форма тестирования OLAP сервера Cubes.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        cubes_olap_srv_test_dlg.icCubesOLAPSrvTestDialogProto.__init__(self, *args, **kwargs)

        # Тестируемый OLAP сервер
        self._OLAP_server = None

    def setOLAPServer(self, olap_server):
        """
        Установить тестируемый OLAP сервер.
        @param olap_server: OLAP сервер
        """
        self._OLAP_server = olap_server

        if self._OLAP_server:
            # Настраиваем контрол выбора кубов
            choices = [cube.description if cube.description else cube.name for cube in self._OLAP_server.getCubes()]
            self.cube_choice.Clear()
            self.cube_choice.AppendItems(choices)

    def onCloseButtonClick(self, event):
        """
        Обработчик кнопки ЗАКРЫТЬ.
        """
        self.EndModal(wx.ID_CLOSE)
        event.Skip()


def show_cubes_olap_srv_test_dlg(parent=None, olap_srv=None):
    """
    Отобразить окно тестирования OLAP сервера Cubes.
    @param parent: Родительское окно.
        Если не определено, то берется самое главное окно.
    @param olap_srv: Тестируемый OLAP сервер.
    @return: True/False.
    """
    if olap_srv is None:
        log.warning(u'Не определен объект OLAP сервера для тестирования')
        return False

    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    try:
        # Запускаем OLAP сервер
        olap_srv.run()

        dlg = icCubesOLAPSrvTestDialog(parent=parent)
        dlg.setOLAPServer(olap_srv)

        dlg.ShowModal()
        return True
    except:
        log.fatal(u'Ошибка отображения окна тестирования OLAP сервера Cubes.')
    return False