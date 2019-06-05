#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговая форма редактирования запроса сводной таблицы к OLAP серверу Cubes.
"""

import wx

from . import edit_cubes_olap_srv_request_dlg_proto

from ic.log import log


__version__ = (0, 1, 1, 1)


class icEditCubesPivotTabRequestDialog(edit_cubes_olap_srv_request_dlg_proto.icEditCubesPivotTabRequestDlgProto):
    """
    Диалоговая форма редактирования запроса сводной таблицы к OLAP серверу Cubes.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        edit_cubes_olap_srv_request_dlg_proto.icEditCubesPivotTabRequestDlgProto.__init__(self, *args, **kwargs)

        # OLAP сервер
        self._OLAP_server = None

        # Отредактированная структура запроса
        self._request = None

    def setOLAPServer(self, olap_server):
        """
        Установить тестируемый OLAP сервер.
        @param olap_server: OLAP сервер
        """
        self._OLAP_server = olap_server

        if self._OLAP_server:
            self.request_panel.setOLAPServer(self._OLAP_server)

    def getRequest(self):
        """
        Отредактированная структура запроса.
        """
        return self._request

    def setRequest(self, request=None):
        """
        Отредактированная структура запроса. Установить.
        @param request: Отредактированная структура запроса в виде словаря.
        """
        self._request = request

        if self._request:
            self.request_panel.setRequest(self._request)

    def onCancelButtonClick(self, event):
        """
        Обработчик кнопки ОТМЕНА.
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        Обработчик кнопки OK.
        """
        self._request = self.request_panel.getRequest()
        # Отдельно сохраняем url для дальнейшего использования в браузере
        self._request['url'] = self.request_panel.getRequestURL(self._request)
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onRefreshButtonClick(self, event):
        """
        Обработчик кнопки обновления адреса.
        """
        url = self.request_panel.getRequestURL()
        self.request_panel.request_textCtrl.SetValue(url)
        event.Skip()


def edit_cubes_pivot_tab_request_dlg(parent=None, olap_srv=None,
                                     olap_srv_request=None):
    """
    Редактирование запроса сводной таблицы к OLAP серверу Cubes.
    @param parent: Родительское окно.
        Если не определено, то берется самое главное окно.
    @param olap_srv: Объект OLAP сервера.
    @param olap_srv_request: Структура запроса к OLAP серверу Cubes.
    @return: Отредактированная структура запроса к OLAP серверу Cubes
        или None, если нажата <Отмена>.
    """
    if olap_srv is None:
        log.warning(u'Не определен объект OLAP сервера для редактирования запроса')
        return None

    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    try:
        dlg = icEditCubesPivotTabRequestDialog(parent=parent)
        dlg.setOLAPServer(olap_srv)
        log.debug(u'Редактируемый запрос %s' % str(olap_srv_request))
        dlg.setRequest(olap_srv_request)

        result = None
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.getRequest()
        dlg.Destroy()
        return result
    except:
        log.fatal(u'Ошибка редактирования запроса сводной таблицы к OLAP серверу Cubes')
    return None
