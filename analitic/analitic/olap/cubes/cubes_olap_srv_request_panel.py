#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль формы <icCubesOLAPSrvRequestPanelProto>. 
Сгенерирован проектом DEFIS по модулю формы-прототипа wxFormBuider.
"""

import wx
from . import cubes_olap_srv_request_form_proto

import ic
from ic.log import log
from ic.utils import wxfunc

# Для управления взаимодействия с контролами wxPython
# используется менеджер форм <form_manager.icFormManager>
from ic.engine import form_manager

__version__ = (0, 1, 1, 1)

OLAP_METHODS = ('aggregate', 'members', 'facts', 'fact', 'cell', 'report')

CUT_PARAMETER_HELP = u'cut - спецификация ячейки, например: cut=date:2004,1|category:2|entity:12345'
DRILLDOWN_PARAMETER_HELP = u'''drilldown - измерение, который нужно "сверлить". Например drilldown=date даст строки для каждого значения
следующий уровень даты измерения. Вы можете явно указать уровень для детализации в форме: dimension:level,
таких как: drilldown=date:month. Чтобы указать иерархию используйте dimension@hierarchy как в
drilldown=date@ywd для неявного уровня или drilldown=date@ywd:week явно указать уровень.'''
AGGREGATES_PARAMETER_HELP = u'''aggregates – список агрегатов для расчета, разделяется с помошью |,
например: aggergates=amount_sum|discount_avg|count'''
MEASURES_PARAMETER_HELP = u'''measures – список мер, для которых будут рассчитаны их соответствующие агрегаты (см. ниже).
Разделяется с помощью |, например: aggergates=proce|discount'''
PAGE_PARAMETER_HELP = u'page - номер страницы для нумерации страниц'
PAGESIZE_PARAMETER_HELP = u'pagesize - размер страницы для разбивки на страницы'
ORDER_PARAMETER_HELP = u'order - список атрибутов для заказа'
SPLIT_PARAMETER_HELP = u'''split – разделенная ячейка, тот же синтаксис, что и у вырезки, определяет виртуальное двоичное (флаговое) измерение, которое указывает, является ли ячейка
принадлежит разделенному разрезу (true) или нет (false). Атрибут измерения называется __within_split__.
Обратитесь к бэкэнду, который вы используете для получения дополнительной информации, поддерживается ли эта функция или нет.'''

OLAP_SERVER_URL_FMT = 'cube/%s/%s'


class icCubesOLAPSrvRequestPanel(cubes_olap_srv_request_form_proto.icCubesOLAPSrvRequestPanelProto, form_manager.icFormManager):
    """
    Форма .
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        cubes_olap_srv_request_form_proto.icCubesOLAPSrvRequestPanelProto.__init__(self, *args, **kwargs)

        # Тестируемый OLAP сервер
        self._OLAP_server = None

        self._help_popup_win = None
        self.init()

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
            if choices:
                self.cube_choice.SetSelection(0)
                self.method_choice.SetSelection(0)
                self.refreshDimensionChoice(0)

    def refreshDimensionChoice(self, i_cube):
        """
        Обновить список измерений в зависимости от выбранного куба.
        """
        cube = self._OLAP_server.getCubes()[i_cube] if i_cube >= 0 else None
        if cube:
            choices = [u''] + [dimension.getLabel() for dimension in cube.getDimensions()]

            self.dimension_choice.Clear()
            self.dimension_choice.AppendItems(choices)
            if choices:
                self.dimension_choice.SetSelection(0)

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
        self.method_choice.AppendItems(OLAP_METHODS)

        # Выключить все параметры
        self.cut_textCtrl.Enable(False)
        self.drilldown_textCtrl.Enable(False)
        self.aggregates_textCtrl.Enable(False)
        self.measures_textCtrl.Enable(False)
        self.page_textCtrl.Enable(False)
        self.pagesize_textCtrl.Enable(False)
        self.order_textCtrl.Enable(False)
        self.split_textCtrl.Enable(False)

    # def onCubeChoice(self, event):
    #     """
    #     Обработчик выбора куба.
    #     """
    #     i_cube = event.GetSelection()
    #     self.refreshDimensionChoice(i_cube)
    #
    #     event.Skip()

    def onAggregatesCheckBox(self, event):
        """
        Обработчик включения параметра aggregate.
        """
        enable = event.IsChecked()
        self.aggregates_textCtrl.Enable(enable)
        event.Skip()

    def show_help_popup_win(self, button, info_text):
        """
        Отобразить/скрыть всплывающее окно помощи.
        @param button: Кнопка вызова окна помощи.
        @param info_text: Текст помощи.
        @return:
        """
        if self._help_popup_win:
            self._help_popup_win.close()
            self._help_popup_win = None
        else:
            self._help_popup_win = wxfunc.showInfoWindow(parent=self,
                                                         ctrl=button,
                                                         info_text=info_text)

    def onAggregatesHelpButtonClick(self, event):
        """
        Подсказка по параметру.
        """
        self.show_help_popup_win(self.aggregates_hlp_bpButton,
                                 info_text=AGGREGATES_PARAMETER_HELP)
        event.Skip()

    def onCutCheckBox(self, event):
        """
        Обработчик включения параметра cut.
        """
        enable = event.IsChecked()
        self.cut_textCtrl.Enable(enable)
        event.Skip()

    def onCutHelpButtonClick(self, event):
        """
        Подсказка по параметру.
        """
        self.show_help_popup_win(self.cut_hlp_bpButton,
                                 info_text=CUT_PARAMETER_HELP)
        event.Skip()

    def onDrilldownCheckBox(self, event):
        """
        Обработчик включения параметра drilldown.
        """
        enable = event.IsChecked()
        self.drilldown_textCtrl.Enable(enable)
        event.Skip()

    def onDrilldownHelpButtonClick(self, event):
        """
        Подсказка по параметру.
        """
        self.show_help_popup_win(self.drilldown_hlp_bpButton,
                                 info_text=DRILLDOWN_PARAMETER_HELP)
        event.Skip()

    def onMeasuresCheckBox(self, event):
        """
        Обработчик включения параметра measures.
        """
        enable = event.IsChecked()
        self.measures_textCtrl.Enable(enable)
        event.Skip()

    def onMeasuresHelpButtonClick(self, event):
        """
        Подсказка по параметру.
        """
        self.show_help_popup_win(self.measures_hlp_bpButton,
                                 info_text=MEASURES_PARAMETER_HELP)
        event.Skip()

    def onOrderCheckBox(self, event):
        """
        Обработчик включения параметра order.
        """
        enable = event.IsChecked()
        self.order_textCtrl.Enable(enable)
        event.Skip()

    def onOrderHelpButtonClick(self, event):
        """
        Подсказка по параметру.
        """
        self.show_help_popup_win(self.order_hlp_bpButton,
                                 info_text=ORDER_PARAMETER_HELP)
        event.Skip()

    def onPageCheckBox(self, event):
        """
        Обработчик включения параметра page.
        """
        enable = event.IsChecked()
        self.page_textCtrl.Enable(enable)
        event.Skip()

    def onPageHelpButtonClick(self, event):
        """
        Подсказка по параметру.
        """
        self.show_help_popup_win(self.page_hlp_bpButton,
                                 info_text=PAGE_PARAMETER_HELP)
        event.Skip()

    def onPagesizeCheckBox(self, event):
        """
        Обработчик включения параметра pagesize.
        """
        enable = event.IsChecked()
        self.pagesize_textCtrl.Enable(enable)
        event.Skip()

    def onPagesizeHelpButtonClick(self, event):
        """
        Подсказка по параметру.
        """
        self.show_help_popup_win(self.pagesize_hlp_bpButton,
                                 info_text=PAGESIZE_PARAMETER_HELP)
        event.Skip()

    def onSplitCheckBox(self, event):
        """
        Обработчик включения параметра split.
        """
        enable = event.IsChecked()
        self.split_textCtrl.Enable(enable)
        event.Skip()

    def onSplitHelpButtonClick(self, event):
        """
        Подсказка по параметру.
        """
        self.show_help_popup_win(self.split_hlp_bpButton,
                                 info_text=SPLIT_PARAMETER_HELP)
        event.Skip()

    def getRequestURL(self):
        """
        Получить URL запроса к серверу OLAP.
        """
        i_cube = self.cube_choice.GetSelection()
        cube = self._OLAP_server.getCubes()[i_cube] if i_cube >= 0 else None
        cube_name = cube.getName() if cube else None
        i_func = self.method_choice.GetSelection()
        method_name = OLAP_METHODS[i_func] if i_func >= 0 else None
        i_dimension = self.dimension_choice.GetSelection() - 1
        # log.debug(u'Выбранное измерение %d' % i_dimension)
        dimension = (cube.getDimensions()[i_dimension] if cube else None) if i_dimension >= 0 else None

        request_url = u''
        if cube_name and method_name:
            request_url = OLAP_SERVER_URL_FMT % (cube_name, method_name)
        if dimension:
            request_url += '/%s' % dimension.getName()

        # Наполнить параметрами
        params = list()
        if self.cut_checkBox.GetValue():
            param = self.cut_textCtrl.GetValue().strip()
            if param:
                params.append('cut=' + param)
        if self.drilldown_checkBox.GetValue():
            param = self.drilldown_textCtrl.GetValue().strip()
            if param:
                params.append('drilldown=' + param)
        if self.aggregates_checkBox.GetValue():
            param = self.aggregates_textCtrl.GetValue().strip()
            if param:
                params.append('aggregates=' + param)
        if self.measures_checkBox.GetValue():
            param = self.measures_textCtrl.GetValue().strip()
            if param:
                params.append('measures=' + param)
        if self.page_checkBox.GetValue():
            param = self.page_textCtrl.GetValue().strip()
            if param:
                params.append('page=' + param)
        if self.pagesize_checkBox.GetValue():
            param = self.pagesize_textCtrl.GetValue().strip()
            if param:
                params.append('pagesize=' + param)
        if self.order_checkBox.GetValue():
            param = self.order_textCtrl.GetValue().strip()
            if param:
                params.append('order=' + param)
        if self.split_checkBox.GetValue():
            param = self.split_textCtrl.GetValue().strip()
            if param:
                params.append('split=' + param)
        if params:
            params_url = '&'.join(params)
            request_url += '?%s' % params_url

        try:
            full_request_url = self._OLAP_server.get_request_url(request_url)
            self.request_textCtrl.SetValue(full_request_url)
        except:
            log.fatal(u'Ошибка получения полного запроса URL к OLAP серверу')

        return request_url


def show_cubes_olap_srv_request_panel(title=u''):
    """
    @param title: Заголовок страницы нотебука главного окна.
    """
    try:
        main_win = ic.getMainWin()
        
        panel = icCubesOLAPSrvRequestPanel(main_win)
        # panel.init()
        main_win.AddPage(panel, title)
    except:
        log.fatal(u'Ошибка')    

