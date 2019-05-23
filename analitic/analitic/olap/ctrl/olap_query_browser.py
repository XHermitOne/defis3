#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Браузер результатов запросов к OLAP серверу.
"""

import wx

from . import olap_query_browse_panel_proto

from ic.log import log
from ic.engine import ic_user

from ic.engine import panel_manager
from ic.components import icwidget

from STD.spreadsheet import spreadsheet_view_manager

__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_OLAPQUERYBROWSER = {'__parent__': icwidget.SPC_IC_WIDGET,
                           '__attr_hlp__': {
                                            },
                           }


class icOLAPQueryBrowserProto(olap_query_browse_panel_proto.icOLAPQueryBrowsePanelProto,
                              panel_manager.icPanelManager):
    """
    Браузер результатов запросов к OLAP серверу.
    Абстрактный класс.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        olap_query_browse_panel_proto.icOLAPQueryBrowsePanelProto.__init__(self, *args, **kwargs)

        # Менеджер управления выводом структуры SpreadSheet
        self._spreadsheet_mngr = spreadsheet_view_manager.icSpreadSheetViewManager(grid=self.spreadsheet_grid)

    def onCollapseToolClicked(self, event):
        """
        Обработчик кнопки СВЕРНУТЬ.
        """
        self.collapseSplitterPanel(splitter=self.browse_splitter, toolbar=self.ctrl_toolBar,
                                   collapse_tool=self.collapse_tool, expand_tool=self.expand_tool)
        event.Skip()

    def onExpandToolClicked(self, event):
        """
        Обработчик кнопки РАЗВЕРНУТЬ.
        """
        self.expandSplitterPanel(splitter=self.browse_splitter, toolbar=self.ctrl_toolBar,
                                 collapse_tool=self.collapse_tool, expand_tool=self.expand_tool)
        event.Skip()

    def refreshPivotTable(self, request_url=None, request=None):
        """
        Обновить сводную таблицу по запросу к OLAP серверу.
        @param request_url: URL запроса к OLAP серверу.
            Если не определен, то берется из текущего выбранного элемента
            дерева запросов.
        @param request: Структура описания запроса. Словарь.
            Если не определена, то берется из текущего выбранного элемента
            дерева запросов.
        @return: True/False.
        """
        if request is None:
            item_data = self.getSelectedItemData_tree(ctrl=self.query_treectrl)
            request = item_data.get('__request__', dict())
        if request is None:
            log.warning(u'Не определен запрос к OLAP серверу')
            return False

        olap_server = self.query_treectrl.getOLAPServer()

        if request_url is None:
            request_url = request.get('url', None)
        # log.debug(u'URL: <%s>' % request_url)
        request_url = (olap_server.getRequestURL(request) if olap_server else None) if not request_url else request_url
        if request_url:
            log.debug(u'Запрос к OLAP серверу. URL <%s>' % request_url)
        else:
            log.warning(u'Не определен запрос к OLAP серверу')
            return False

        if olap_server:
            json_response = olap_server.get_response(request_url)
            if json_response:
                if 'drilldown' in request and '|' in request['drilldown']:
                    row_dimension_url, col_dimension_url = request['drilldown'].split('|')
                    row_dimension = self._parse_dimension_names(row_dimension_url, request, olap_server=olap_server)
                    col_dimension = self._parse_dimension_names(col_dimension_url, request, olap_server=olap_server)
                    dataframe = olap_server.to_pivot_dataframe(json_response, row_dimension=row_dimension,
                                                               col_dimension=col_dimension)
                else:
                    row_dimension_url = request.get('drilldown', None)
                    row_dimension = self._parse_dimension_names(row_dimension_url, request, olap_server=olap_server)
                    dataframe = olap_server.to_pivot_dataframe(json_response, row_dimension=row_dimension)
                spreadsheet = olap_server.pivot_to_spreadsheet(json_response, dataframe=dataframe)
                self._spreadsheet_mngr.view_spreadsheet(spreadsheet)
            else:
                # Если нет ничего, то полностью очистить грид
                self._spreadsheet_mngr.reCreateGrid(self._spreadsheet_mngr.getSpreadSheetGrid(), 1, 1)
            return True
        else:
            log.warning(u'Не определен OLAP сервер в браузере запросов')
        return False

    def _parse_dimension_names(self, dimension_url, request, olap_server=None):
        """
        Список имен измерения.
        @param dimension_url: Часть элемента запроса.
            Например store_date@ymd:month
        @param request: Структура описания запроса. Словарь.
        @param olap_server: OLAP сервер.
        @return: Список имен элементов измерения.
        """
        if olap_server is None:
            olap_server = self.query_treectrl.getOLAPServer()

        dimension_names = list()
        if '@' in dimension_url:
            # Указано измерение@иерархия:уровень
            cube_name = request.get('cube', None)
            cube = olap_server.findCube(cube_name)
            dimension_name = dimension_url.split('@')[0]
            dimension = cube.findDimension(dimension_name)
            hierarchy_name = dimension_url.split('@')[1].split(':')[0]
            hierarchy = dimension.findHierarchy(hierarchy_name)
            level_names = hierarchy.getLevelNames()
            hierarchy_level_name = dimension_url.split('@')[1].split(':')[1]
            level_names = level_names[:level_names.index(hierarchy_level_name)+1] if level_names else list()
            dimension_names = tuple(['%s.%s' % (dimension_name, level_name) for level_name in level_names])
        elif ':' in dimension_url:
            # Указано измерение:уровень
            cube_name = request.get('cube', None)
            cube = olap_server.findCube(cube_name)
            dimension_name = dimension_url.split(':')[0]
            dimension = cube.findDimension(dimension_name)
            level_names = [level.getName() for level in dimension.getLevels()]
            hierarchy_level_name = dimension_url.split(':')[1]
            level_names = level_names[:level_names.index(hierarchy_level_name)+1] if level_names else list()
            dimension_names = tuple(['%s.%s' % (dimension_name, level_name) for level_name in level_names])
        else:
            # Указано измерение
            dimension_names = tuple([dimension_url])

        # log.debug(u'Список элментов измерений %s' % str(dimension_names))
        return dimension_names


def show_olap_query_browser(parent=None, title=u'Аналитические отчеты', olap_server=None):
    """
    Функция просмотра браузера результатов запросов к OLAP серверу.
    @param parent: Родительское окно.
    @param title: Заголовок страницы браузера.
    @param olap_server: Объект OLAP сервера, отображаемого в браузере.
    @return: True/False.
    """
    if olap_server is None:
        log.warning(u'Не определен объект OLAP сервера для просмотре результатов запросов')
        return False

    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    try:
        # Запускаем OLAP сервер
        olap_server.run()

        browser_panel = icOLAPQueryBrowserProto(parent=parent)
        browser_panel.query_treectrl.setOLAPServer(olap_server)

        ic_user.addMainNotebookPage(browser_panel, title)

        # Остановить OLAP сервер
        olap_server.stop()

        return True
    except:
        log.fatal(u'Ошибка просмотра браузера результатов запросов к OLAP серверу')
    return False
