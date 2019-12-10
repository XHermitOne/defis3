#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль панели запроса сводной таблицы из OLAP куба.
"""

import wx
from . import cubes_olap_srv_request_form_proto

import ic
from ic.log import log
from ic.utils import wxfunc
from ic.dlg import dlgfunc

# Для управления взаимодействия с контролами wxPython
# используется менеджер форм <form_manager.icFormManager>
from ic.engine import form_manager

__version__ = (0, 1, 1, 1)

CUT_HELP = u'Cпецификация ячейки среза, например: date:2004,1|category:2|entity:12345'


class icCubesPivotTabRequestPanel(cubes_olap_srv_request_form_proto.icCubesPivotTabRequestPanelProto,
                                  form_manager.icFormManager):
    """
    Панель запроса сводной таблицы из OLAP куба.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        cubes_olap_srv_request_form_proto.icCubesPivotTabRequestPanelProto.__init__(self, *args, **kwargs)

        # Тестируемый OLAP сервер
        self._OLAP_server = None

        self._help_popup_win = None
        self.init()

    def setOLAPServer(self, olap_server, bRefresh=False):
        """
        Установить тестируемый OLAP сервер.
        :param olap_server: OLAP сервер
        :param bRefresh: Сделать обновление контролов?
        """
        self._OLAP_server = olap_server

        if self._OLAP_server and bRefresh:
            # Настраиваем контрол выбора кубов
            self.refreshCubeChoice()

    def refreshCubeChoice(self, i_cube=0):
        """
        Обновить список кубов.
        :param i_cube: Индекс выбранного куба.
        """
        if self._OLAP_server:
            # Настраиваем контрол выбора кубов
            choices = [cube.getLabel() for cube in self._OLAP_server.getCubes()]
            self.cube_choice.Clear()
            self.cube_choice.AppendItems(choices)
            if choices:
                self.cube_choice.setSelection(i_cube)
                self.refreshDimensionChoice(i_cube)
                self.refreshAggregateChoice(i_cube)

    def refreshDimensionChoice(self, i_cube):
        """
        Обновить список измерений в зависимости от выбранного куба.
        :param i_cube: Индекс выбранного куба.
        """
        cube = self._OLAP_server.getCubes()[i_cube] if i_cube >= 0 else None
        if cube:
            choices = [u''] + [dimension.getLabel() for dimension in cube.getDimensions()]

            self.row_dimension_choice.Clear()
            self.row_dimension_choice.AppendItems(choices[1:])
            self.row_dimension_choice.setSelection(0)

            self.col_dimension_choice.Clear()
            self.col_dimension_choice.AppendItems(choices)
            self.col_dimension_choice.setSelection(0)

            self.cut_dimension_choice.Clear()
            self.cut_dimension_choice.AppendItems(choices)
            self.cut_dimension_choice.setSelection(0)

    def refreshAggregateChoice(self, i_cube):
        """
        Обновить список агрегаций.
        :param i_cube: Индекс выбранного куба.
        """
        cube = self._OLAP_server.getCubes()[i_cube] if i_cube >= 0 else None
        if cube:
            choices = [aggregate.getLabel() for aggregate in cube.getAggregates()]

            self.aggregate_checkList.Clear()
            self.aggregate_checkList.AppendItems(choices)
            self.checkAllItems_list_ctrl(ctrl=self.aggregate_checkList)

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
        self.setColumns_list_ctrl(ctrl=self.cut_listCtrl,
                                  cols=(dict(label=u'Измерение', width=250),
                                        dict(label=u'Наименование', width=150),
                                        dict(label=u'Значение', width=300)))

    def show_help_popup_win(self, button, info_text):
        """
        Отобразить/скрыть всплывающее окно помощи.
        :param button: Кнопка вызова окна помощи.
        :param info_text: Текст помощи.
        :return:
        """
        if self._help_popup_win:
            self._help_popup_win.close()
            self._help_popup_win = None
        else:
            self._help_popup_win = wxfunc.showInfoWindow(parent=self,
                                                         ctrl=button,
                                                         info_text=info_text)

    def onHelpCutButtonClick(self, event):
        """
        Обработчик кнопки помощи для среза.
        """
        self.show_help_popup_win(self.cut_help_bpButton,
                                 info_text=CUT_HELP)
        event.Skip()

    def _parse_drilldown(self, drilldown):
        """
        Парсер представления части запроса измерений по строкам и колонкам.
        :param drilldown: Часть запроса в виде
        :return: Кортеж:
            Имя измерения строк, Имя уровня измерения строк,
            Имя измерения колонок, Имя уровня измерения колонок
        """
        row_drilldown_dimension = None
        row_drilldown_level = None
        col_drilldown_dimension = None
        col_drilldown_level = None

        if drilldown and '|' in drilldown:
            drilldown_list = drilldown.split('|')
            drilldown_row, drilldown_col = drilldown_list[0], drilldown_list[1]
            if ':' in drilldown_row:
                row_drilldown_dimension, row_drilldown_level = drilldown_row.split(':')
            else:
                row_drilldown_dimension = drilldown_row
            if ':' in drilldown_col:
                col_drilldown_dimension, col_drilldown_level = drilldown_col.split(':')
            else:
                col_drilldown_dimension = drilldown_col

        elif drilldown and '|' not in drilldown:
            drilldown_row = drilldown
            if ':' in drilldown_row:
                row_drilldown_dimension, row_drilldown_level = drilldown_row.split(':')
            else:
                row_drilldown_dimension = drilldown_row
        return row_drilldown_dimension, row_drilldown_level, col_drilldown_dimension, col_drilldown_level

    def setRequest(self, request):
        """
        Установить запрос к серверу OLAP в структурном виде.
        :param request: Словарь параметров запроса к OLAP серверу.
        :return: True/False.
        """
        try:
            return self._setRequest(request=request)
        except:
            log.fatal(u'Ошибка установки значений для редактирования запроса к OLAP серверу')
        return False

    def _setRequest(self, request):
        """
        Установить запрос к серверу OLAP в структурном виде.
        :param request: Словарь параметров запроса к OLAP серверу.
        :return: True/False.
        """
        if request is None:
            request = dict()

        cube_name = request.get('cube', None)
        cubes = self._OLAP_server.getCubes()
        cube = None
        if cube_name:
            cube_names = [cube.getName() for cube in cubes]
            try:
                i_cube = cube_names.index(cube_name)
                cube = cubes[i_cube]
                self.refreshCubeChoice(i_cube=i_cube)
            except ValueError:
                log.error(u'Куб с именем <%s> не найден среди %s' % (cube_name, str(cube_names)))

        if cube is None and cubes:
            log.warning(u'Не определен куб для установки. По умолчанию выбран первый')
            cube = cubes[0]
            self.refreshCubeChoice(i_cube=0)
        elif cube is None and not cubes:
            log.warning(u'Не определены кубы OLAP сервера')
            return False

        # Измерения строк и колонок
        drilldown = request.get('drilldown', u'')
        row_drilldown_dimension, row_drilldown_level, col_drilldown_dimension, col_drilldown_level = self._parse_drilldown(drilldown=drilldown)

        if row_drilldown_dimension:
            i_dimension = [dimension.getName() for dimension in cube.getDimensions()].index(row_drilldown_dimension)
            self.row_dimension_choice.setSelection(i_dimension)
            if row_drilldown_level:
                dimension = cube.getDimensions()[i_dimension]
                choices = [level.getLabel() for level in dimension.getLevels()]
                self.row_level_choice.SetItems([u''] + choices)
                level_names = [level.getName() for level in dimension.getLevels()]
                i_level = level_names.index(row_drilldown_level)
                self.row_level_choice.setSelection(i_level + 1)
            else:
                self.row_dimension_choice.setSelection(0)
                self.row_level_choice.SetItems([u''])
                self.row_level_choice.setSelection(0)
        else:
            self.row_dimension_choice.setSelection(0)
            self.row_level_choice.SetItems([u''])
            self.row_level_choice.setSelection(0)

        if col_drilldown_dimension:
            i_dimension = [dimension.getName() for dimension in cube.getDimensions()].index(col_drilldown_dimension)
            self.col_dimension_choice.setSelection(i_dimension + 1)
            if col_drilldown_level:
                dimension = cube.getDimensions()[i_dimension]
                choices = [level.getLabel() for level in dimension.getLevels()]
                self.col_level_choice.SetItems([u''] + choices)
                level_names = [level.getName() for level in dimension.getLevels()]
                i_level = level_names.index(col_drilldown_level)
                self.col_level_choice.setSelection(i_level + 1)
            else:
                self.col_dimension_choice.setSelection(0)
                self.col_level_choice.SetItems([u''])
                self.col_level_choice.setSelection(0)
        else:
            self.col_dimension_choice.setSelection(0)
            self.col_level_choice.SetItems([u''])
            self.col_level_choice.setSelection(0)

        # Агрегации
        aggregates = request.get('aggregates', u'')
        if aggregates.strip():
            aggregates = aggregates.strip().split('|')
            all_aggregate_names = [aggregate.getName() for aggregate in cube.getAggregates()]
            checked_list = [all_aggregate_names.index(aggregate) for aggregate in aggregates]
            self.aggregate_checkList.SetCheckedItems(checked_list)

        # Срезы
        cut = request.get('cut', u'')
        if cut.strip():
            cut = cut.strip().split('|')
            cut_list = [sub_cut.split(':') for sub_cut in cut]
            rows = tuple([(cube.findDimension(cut[0]).getLabel(), cut[0], cut[1]) for cut in cut_list])
            self.setRows_list_ctrl(ctrl=self.cut_listCtrl, rows=rows)

        return True

    def getRequest(self):
        """
        Получить запрос к серверу OLAP в структурном виде.
        :return: Словарь параметров запроса к OLAP серверу.
            Словарь заполняется в соответствии с выбранными
            параметрами контролов панели.
        """
        try:
            return self._getRequest()
        except:
            log.fatal(u'Ошибка получения отредактированного запроса к OLAP серверу')
        return dict()

    def _getRequest(self):
        """
        Получить запрос к серверу OLAP в структурном виде.
        :return: Словарь параметров запроса к OLAP серверу.
            Словарь заполняется в соответствии с выбранными
            параметрами контролов панели.
        """
        request = dict()
        i_cube = self.cube_choice.GetSelection()
        cube = self._OLAP_server.getCubes()[i_cube] if i_cube >= 0 else None
        cube_name = cube.getName() if cube else None
        if cube_name:
            request['cube'] = cube_name

        request['method'] = 'aggregate'

        # Наполнить параметрами
        # Строки и столбцы сводной таблицы
        row_param = u''
        i_dimension = self.row_dimension_choice.GetSelection()
        if i_dimension >= 0:
            dimension_name = [dimension.getName() for dimension in cube.getDimensions()][i_dimension]
            # log.debug(u'Измерение <%s>. Индекс [%d]' % (dimension_name, i_dimension))
            dimension = cube.findDimension(dimension_name)
            i_level = self.row_level_choice.GetSelection()
            if i_level > 0:
                # log.debug(u'Уровень [%d] среди %s' % (i_level, str([level.getName() for level in dimension.getLevels()])))
                level_name = [level.getName() for level in dimension.getLevels()][i_level - 1]
                row_param = u'%s:%s' % (dimension_name, level_name)
            else:
                row_param = dimension_name
        col_param = u''
        i_dimension = self.col_dimension_choice.GetSelection()
        if i_dimension > 0:
            dimension_name = [dimension.getName() for dimension in cube.getDimensions()][i_dimension - 1]
            # log.debug(u'Измерение <%s>. Индекс [%d]' % (dimension_name, i_dimension))
            dimension = cube.findDimension(dimension_name)
            i_level = self.col_level_choice.GetSelection()
            if i_level > 0:
                level_name = [level.getName() for level in dimension.getLevels()][i_level - 1]
                # log.debug(u'Уровень [%d : %s] среди %s.' % (i_level, level_name, str([level.getName() for level in dimension.getLevels()])))
                col_param = u'%s:%s' % (dimension_name, level_name)
            else:
                col_param = dimension_name

        if row_param and not col_param:
            request['drilldown'] = row_param
        elif row_param and col_param:
            request['drilldown'] = u'%s|%s' % (row_param, col_param)

        # Агрегации
        aggregate_checked = self.getCheckedItems_list_ctrl(ctrl=self.aggregate_checkList,
                                                           check_selected=True)
        aggregates = cube.getAggregates()
        request['aggregates'] = u'|'.join([aggregates[check_idx].getName() for check_idx in aggregate_checked])

        # Срезы
        rows = self.getRows_list_ctrl(ctrl=self.cut_listCtrl)
        request['cut'] = u'|'.join([u'%s:%s' % (row[1], row[2]) for row in rows])

        log.debug(u'Данные запроса: %s' % str(request))
        return request

    def getRequestURL(self, request=None):
        """
        Получить URL запроса к серверу OLAP по его структурному описанию.
        :return: Словарь параметров запроса к OLAP серверу.
            Если не определен, то берется из контролов.
        """
        if request is None:
            request = self.getRequest()

        try:
            full_request_url = self._OLAP_server.getRequestURL(request)
            return full_request_url
        except:
            log.fatal(u'Ошибка получения полного запроса URL к OLAP серверу')

        return u''

    def onRowDimensionChoice(self, event):
        """
        Обработчик смены измерения в настройках строк сводной таблицы.
        """
        i_dimension = event.GetSelection()
        i_cube = self.cube_choice.GetSelection()
        if i_dimension >= 0:
            cube = self._OLAP_server.getCubes()[i_cube]
            dimension = cube.getDimensions()[i_dimension]
            choices = [u''] + [level.getLabel() for level in dimension.getLevels()]

            self.row_level_choice.Clear()
            self.row_level_choice.AppendItems(choices)
            self.row_level_choice.setSelection(0)
        else:
            self.row_level_choice.Clear()

        event.Skip()

    def onColDimensionChoice(self, event):
        """
        Обработчик смены измерения в настройках колонок сводной таблицы.
        """
        i_dimension = event.GetSelection()
        i_cube = self.cube_choice.GetSelection()
        if i_dimension > 0:
            cube = self._OLAP_server.getCubes()[i_cube]
            dimension = cube.getDimensions()[i_dimension - 1]
            choices = [u''] + [level.getLabel() for level in dimension.getLevels()]

            self.col_level_choice.Clear()
            self.col_level_choice.AppendItems(choices)
            self.col_level_choice.setSelection(0)
        else:
            self.col_level_choice.Clear()

        event.Skip()

    def onAddCutToolClicked(self, event):
        """
        Обработчик добавления среза в список.
        """
        i_cube = self.cube_choice.GetSelection()
        i_dimension = self.cut_dimension_choice.GetSelection()

        if i_dimension <= 0:
            dlgfunc.openWarningBox(u'СРЕЗ', u'Не выбрано измерение среза')
        else:
            value = self.cut_value_textCtrl.GetValue()
            if not value.strip():
                dlgfunc.openWarningBox(u'СРЕЗ', u'Не указано значение среза')
            else:
                cube = self._OLAP_server.getCubes()[i_cube]
                dimension = cube.getDimensions()[i_dimension - 1]
                row = (dimension.getLabel(), dimension.getName(), value)
                self.appendRow_list_ctrl(ctrl=self.cut_listCtrl, row=row)

                # После добавления очищаем контролы среза
                self.cut_dimension_choice.setSelection(0)
                self.cut_value_textCtrl.SetValue(u'')

        event.Skip()

    def onDelCutToolClicked(self, event):
        """
        Обработчик удаления среза из списка.
        """
        i_del_row = self.getItemSelectedIdx(self.cut_listCtrl)
        if i_del_row < 0:
            dlgfunc.openWarningBox(u'СРЕЗ', u'Не выбран срез для удаления из списка')
        else:
            self.cut_listCtrl.DeleteItem(i_del_row)
        event.Skip()


def show_cubes_pivot_tab_request_panel(title=u''):
    """
    Отобразить панель запроса сводной таблицы к OLAP серверу.
    :param title: Заголовок страницы нотебука главного окна.
    """
    try:
        main_win = ic.getMainWin()

        panel = icCubesPivotTabRequestPanel(main_win)
        # panel.init()
        main_win.addPage(panel, title)
    except:
        log.fatal(u'Ошибка')
