#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Браузер журнала сообщений программы.

Журнал сообщений программы сохраняется в файле *.log
Формат журнала:
2016-11-18 08:22:11 INFO Сообщение
    ^         ^      ^      ^
    |         |      |      +-- Текст сообщения
    |         |      +--------- Тип сообщения
    |         +---------------- Время регистрации
    +-------------------------- Дата регистрации
Текст сообщения может быть многострочным. В основном для критических ошибок.
Все программы должны выводить сообщения в таком формате.
Тогда браузер сообщений становиться универсальным для всех программ.
"""

import datetime
import os
import os.path
import wx
import log_browser_proto

import log_file
import log

from ic.utils import ic_time

# Version
__version__ = (0, 0, 3, 6)

TIME_FMT = '%H:%M:%S'

LOG_TYPE_COLOURS = {
                    log_file.INFO_LOG_TYPE: wx.NamedColour('DARKGREEN'),
                    log_file.WARNING_LOG_TYPE: wx.NamedColour('GOLDENROD'),
                    log_file.ERROR_LOG_TYPE: wx.NamedColour('RED4'),
                    log_file.FATAL_LOG_TYPE: wx.NamedColour('RED3'),
                    log_file.DEBUG_LOG_TYPE: wx.NamedColour('BLUE4'),
                    log_file.DEBUG_SERVICE_LOG_TYPE: wx.NamedColour('CYAN4'),
                    log_file.SERVICE_LOG_TYPE: wx.NamedColour('CYAN4'),
                    }

LOG_TYPE_LABELS = {
                   log_file.INFO_LOG_TYPE: u'Информация',
                   log_file.WARNING_LOG_TYPE: u'Предупреждение',
                   log_file.ERROR_LOG_TYPE: u'Ошибка',
                   log_file.FATAL_LOG_TYPE: u'Критическая ошибка',
                   log_file.DEBUG_LOG_TYPE: u'Отладка',
                   log_file.DEBUG_SERVICE_LOG_TYPE: u'Сервисная информация',
                   log_file.SERVICE_LOG_TYPE: u'Сервисная информация',
                   }

LOG_TYPE_ICONS = {
                  log_file.INFO_LOG_TYPE: wx.ICON_INFORMATION,
                  log_file.WARNING_LOG_TYPE: wx.ICON_WARNING,
                  log_file.ERROR_LOG_TYPE: wx.ICON_ERROR,
                  log_file.FATAL_LOG_TYPE: wx.ICON_HAND,
                  log_file.DEBUG_LOG_TYPE: wx.ICON_ASTERISK,
                  log_file.DEBUG_SERVICE_LOG_TYPE: wx.ICON_EXCLAMATION,
                  log_file.SERVICE_LOG_TYPE: wx.ICON_EXCLAMATION,
                  }


class icLogBrowserPanelManager:
    """
    Менеджер работы с панелью браузера.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        @param args:
        @param kwargs:
        """
        self.filter_panel = self

        if 'filter_panel' in kwargs:
            self.filter_panel = kwargs['filter_panel']
            del kwargs['filter_panel']

        # Текущий обрабатываемый список записей
        self.records = list()

        # Список дополнительных фильтров
        self.ext_filters = ()

    def init(self):
        """
        Инициализация панели.
        """
        self.init_ctrl()

    def init_ctrl(self):
        """
        Инициализация контролов.
        """
        # Колонки списка сообщений
        self.filter_panel.msg_listCtrl.InsertColumn(0, u'Дата/Время', width=200)
        self.filter_panel.msg_listCtrl.InsertColumn(1, u'Тип', width=100)
        self.filter_panel.msg_listCtrl.InsertColumn(2, u'Сообщение', width=wx.LIST_AUTOSIZE)
        # Привязать wxSpinButton к TimeCtrl
        self.filter_panel.start_timeControl.BindSpinButton(self.filter_panel.start_spinBtn)
        self.filter_panel.stop_timeControl.BindSpinButton(self.filter_panel.stop_spinBtn)

    def get_selected_log_types(self):
        """
        Список выбранных типов сообщений.
        @return:
        """
        result = list()

        if self.filter_panel.info_checkBox.IsChecked():
            result.append(log_file.INFO_LOG_TYPE)
        if self.filter_panel.warning_checkBox.IsChecked():
            result.append(log_file.WARNING_LOG_TYPE)
        if self.filter_panel.error_checkBox.IsChecked():
            result.append(log_file.ERROR_LOG_TYPE)
        if self.filter_panel.fatal_checkBox.IsChecked():
            result.append(log_file.FATAL_LOG_TYPE)
        if self.filter_panel.debug_checkBox.IsChecked():
            result.append(log_file.DEBUG_LOG_TYPE)
        if self.filter_panel.service_checkBox.IsChecked():
            result.append(log_file.DEBUG_SERVICE_LOG_TYPE)
            result.append(log_file.SERVICE_LOG_TYPE)
        return tuple(result)

    def get_selected_start_dt(self):
        """
        Выбранное начальное время.
        @return:
        """
        result = None
        if self.filter_panel.start_checkBox.IsChecked():
            wx_date = self.filter_panel.start_datePicker.GetValue()
            wx_time = self.filter_panel.start_timeControl.GetValue()
            py_date = ic_time.wxdate2pydate(wx_date)
            # py_time = ic_time.wxdatetime2pydatetime(wx_time)
            py_time = datetime.datetime.strptime(wx_time, TIME_FMT)
            result = py_time.replace(year=py_date.year, month=py_date.month, day=py_date.day)
        return result

    def get_selected_stop_dt(self):
        """
        Выбранное конечное время.
        @return:
        """
        result = None
        if self.filter_panel.stop_checkBox.IsChecked():
            wx_date = self.filter_panel.stop_datePicker.GetValue()
            wx_time = self.filter_panel.stop_timeControl.GetValue()
            py_date = ic_time.wxdate2pydate(wx_date)
            # py_time = ic_time.wxdatetime2pydatetime(wx_time)
            py_time = datetime.datetime.strptime(wx_time, TIME_FMT)
            result = py_time.replace(year=py_date.year, month=py_date.month, day=py_date.day)
        return result

    def get_selected_filters(self):
        """
        Выбранные дополнительные фильтры.
        @return:
        """
        check_idx = [i for i in range(self.filter_panel.filter_checkList.GetCount()) if self.filter_panel.filter_checkList.IsChecked(i)]
        result = [self.ext_filters[i][1] for i in check_idx]
        return tuple(result)

    def set_filters(self, filter_logic=log_file.AND_FILTER_LOGIC, *ext_filters):
        """
        Установить дополнительные фильтры.
        @param filter_logic: Логика обработки фильтров.
        @param ext_filters: Список дополнительных фильтров:
            ((u'Наименование фильтра на русском', Функция/lambda дополнительного фильтра),...)
            Функция дополнительного фильтра принимает словарь записи и
            возвращает True/False.
        @return: True/False
        """
        self.filter_panel.logic_radioBox.SetSelection(0 if filter_logic == log_file.AND_FILTER_LOGIC else 1)
        if ext_filters:
            self.ext_filters = ext_filters
            for ext_filter in ext_filters:
                if type(ext_filter) in (list, tuple):
                    label, filter_func = ext_filter
                    self.filter_panel.filter_checkList.Append(label)
                else:
                    log.warning(u'Не корректный вид расширенного фильтра <%s>. Фильтр должен состоять из (u\'Наименование фильтра на русском\', Функция/lambda дополнительного фильтра)' % str(ext_filter))
            return True
        return False

    def set_log_filename(self, sLogFileName=None):
        """
        Установить файл журнала для просмотра.
        @param sLogFileName: Файл журнала.
        @return:
        """
        if sLogFileName is not None and os.path.exists(sLogFileName):
            self.filter_panel.log_filePicker.SetPath(sLogFileName)

    def set_datetime_filter_range(self, dtStartFilter=None, dtStopFilter=None):
        """
        Установить фильтр по диапазону времени.
        @param dtStartFilter:
        @param dtStopFilter:
        """
        self.filter_panel.start_checkBox.SetValue(dtStartFilter is not None)
        self.filter_panel.stop_checkBox.SetValue(dtStopFilter is not None)
        if dtStartFilter:
            self.filter_panel.start_datePicker.Enable(dtStartFilter is not None)
            self.filter_panel.start_timeControl.Enable(dtStartFilter is not None)
            self.filter_panel.start_spinBtn.Enable(dtStartFilter is not None)
            wx_date = ic_time.pydate2wxdate(dtStartFilter)
            wx_time_str = dtStartFilter.strftime(TIME_FMT)
            self.filter_panel.start_datePicker.SetValue(wx_date)
            self.filter_panel.start_timeControl.SetValue(wx_time_str)
        if dtStopFilter:
            self.filter_panel.stop_datePicker.Enable(dtStopFilter is not None)
            self.filter_panel.stop_timeControl.Enable(dtStopFilter is not None)
            self.filter_panel.stop_spinBtn.Enable(dtStopFilter is not None)
            wx_date = ic_time.pydate2wxdate(dtStopFilter)
            wx_time_str = dtStopFilter.strftime(TIME_FMT)
            self.filter_panel.stop_datePicker.SetValue(wx_date)
            self.filter_panel.stop_timeControl.SetValue(wx_time_str)

    def set_log_types_filter(self, *log_types):
        """
        Установить фильтр по типам сообщений
        @param log_types: Список типов сообщений.
        """
        if log_types:
            for log_type in log_types:
                if log_type == log_file.INFO_LOG_TYPE:
                    self.filter_panel.info_checkBox.SetValue(True)
                elif log_type == log_file.WARNING_LOG_TYPE:
                    self.filter_panel.warning_checkBox.SetValue(True)
                elif log_type == log_file.ERROR_LOG_TYPE:
                    self.filter_panel.error_checkBox.SetValue(True)
                elif log_type == log_file.FATAL_LOG_TYPE:
                    self.filter_panel.fatal_checkBox.SetValue(True)
                elif log_type == log_file.DEBUG_LOG_TYPE:
                    self.filter_panel.debug_checkBox.SetValue(True)
                elif log_type in (log_file.SERVICE_LOG_TYPE, log_file.DEBUG_SERVICE_LOG_TYPE):
                    self.filter_panel.service_checkBox.SetValue(True)

    def get_records(self, sLogFileName=None, tLogTypes=None,
                    dtStartFilter=None, dtStopFilter=None,
                    tFilters=None, sFilterLogic=None):
        """
        Получить список сообщений, соответствующих выставленным фильтрам.
        @param sLogFileName: Полное имя log файла.
        @param tLogTypes: Кортеж/список типов сообщений.
        @param dtStartFilter: Начальная дата/время фильтра по времени.
            Если не определено, то выбор происходит с начала файла.
        @param dtStopFilter: Конечная дата/время фильтра по времени.
            Если не определено, то выбор происходит до конца файла.
        @param tFilters: Кортеж/список дополнительных методов фильтрации.
            Методы фильтрации задаются как lambda или функции, которые принимают
            Словарь записи, а возвращают True-запись попадает в выбор/False - не попадает.
        @param sFilterLogic: Комманда способа обработки дополнительных фильтров
            AND - Чтобы запись попала в выбор необходимо положительное выполнение всех фильтров,
            OR - Чтобы запись попала в выбор достаточно положительное выполнение одного фильтра.
        @return: Список записей сообщений.
        """
        if sLogFileName is None:
            sLogFileName = self.filter_panel.log_filePicker.GetPath()
        if not sLogFileName:
            log.warning(u'Не определен файл журнала сообщений прораммы')
            return ()

        if tLogTypes is None:
            tLogTypes = self.get_selected_log_types()

        if dtStartFilter is None:
            dtStartFilter = self.get_selected_start_dt()
        if dtStopFilter is None:
            dtStopFilter = self.get_selected_stop_dt()

        if tFilters is None:
            tFilters = self.get_selected_filters()

        if sFilterLogic is None:
            sFilterLogic = log_file.OR_FILTER_LOGIC if self.filter_panel.logic_radioBox.GetSelection() == 1 else log_file.AND_FILTER_LOGIC

        records = log_file.get_records_log_file(sLogFileName, tLogTypes,
                                                dtStartFilter, dtStopFilter,
                                                tFilters, sFilterLogic)
        # print('>', len(records))
        return records

    def refresh(self):
        """
        Обновить список сообщений, соответствующих выставленным фильтрам.
        @return: True/False
        """
        self.filter_panel.msg_listCtrl.DeleteAllItems()
        self.records = self.get_records()
        for i, record in enumerate(self.records):
            item_idx = self.filter_panel.msg_listCtrl.InsertStringItem(i, record['dt'].strftime(log_file.DATETIME_LOG_FMT))
            self.filter_panel.msg_listCtrl.SetStringItem(i, 1, record.get('type', u''))
            self.filter_panel.msg_listCtrl.SetStringItem(i, 2, record.get('short', u''))

            self.filter_panel.msg_listCtrl.SetItemTextColour(i, LOG_TYPE_COLOURS.get(record['type'], wx.BLACK))

        # Переразмерить колонку текста сообщения
        self.filter_panel.msg_listCtrl.SetColumnWidth(2, wx.LIST_AUTOSIZE)

    def onRefreshButtonClick(self, event):
        """
        Обработчик кнопки обновления.
        """
        self.refresh()
        event.Skip()

    def onStartCheckBox(self, event):
        """
        Обработчик вкл/выкл стартового времени.
        """
        check = event.IsChecked()
        self.filter_panel.start_datePicker.Enable(check)
        self.filter_panel.start_timeControl.Enable(check)
        self.filter_panel.start_spinBtn.Enable(check)
        event.Skip()

    def onStopCheckBox(self, event):
        """
        Обработчик вкл/выкл конечного времени.
        """
        check = event.IsChecked()
        self.filter_panel.stop_datePicker.Enable(check)
        self.filter_panel.stop_timeControl.Enable(check)
        self.filter_panel.stop_spinBtn.Enable(check)
        event.Skip()

    def onMsgListItemActivated(self, event):
        """
        Обработчик выбора сообщения из списка.
        """
        item_idx = event.GetIndex()
        try:
            record = self.records[item_idx]
        except IndexError:
            record = None
        if record:
            full_msg = record.get('text', record.get('short', u''))
            dt_title = u'Время: ' + unicode(str(record.get('dt', '')), log_file.DEFAULT_ENCODING)
            title = LOG_TYPE_LABELS.get(record.get('type', u''), u'') + u'. ' + dt_title
            icon = LOG_TYPE_ICONS.get(record.get('type', u''), wx.ICON_HAND)
            wx.MessageBox(full_msg, title, style=wx.OK | icon)

        event.Skip()


class icLogBrowserPanel(icLogBrowserPanelManager,
                        log_browser_proto.icLogBrowserPanelProto):
    """
    Панель браузера журнала сообщений программы.
    В некоторых случаях необходимо отображать браузер в странице нотебука.
    Для этого создаем отдельно панель.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        @param args:
        @param kwargs:
        """
        icLogBrowserPanelManager.__init__(self, filter_panel=self)
        log_browser_proto.icLogBrowserPanelProto.__init__(self, *args, **kwargs)


class icLogBrowserDlg(icLogBrowserPanelManager,
                      log_browser_proto.icLogBrowserDialogProto):
    """
    Диалоговое окно браузера журнала сообщений программы.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        @param args:
        @param kwargs:
        """
        log_browser_proto.icLogBrowserDialogProto.__init__(self, *args, **kwargs)
        icLogBrowserPanelManager.__init__(self, filter_panel=self.browser_panel)

        # Здесь необходимо переопределить все обработчики событий
        self.browser_panel.refresh_bpButton.Bind(wx.EVT_BUTTON, self.onRefreshButtonClick)
        self.browser_panel.start_checkBox.Bind(wx.EVT_CHECKBOX, self.onStartCheckBox)
        self.browser_panel.stop_checkBox.Bind(wx.EVT_CHECKBOX, self.onStopCheckBox)
        self.browser_panel.msg_listCtrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onMsgListItemActivated)

    def init(self):
        """
        Инициализация панели.
        """
        self.init_ctrl()

    def onOkButtonClick(self, event):
        """
        Обработчик кнопки <Ok>.
        """
        self.EndModal(wx.ID_OK)
        event.Skip()


def get_log_browser_panel(parent=None, sLogFileName=None, tLogTypes=None,
                          dtStartFilter=None, dtStopFilter=None,
                          tFilters=None, sFilterLogic=None):
    """
    Функция получения объекта панели просмотра журнала сообщений программы.
    @param parent: Родительское окно.
        Если не указано, то берется главное окно.
    @param sLogFileName: Полное имя log файла.
    @param tLogTypes: Кортеж/список типов сообщений.
    @param dtStartFilter: Начальная дата/время фильтра по времени.
        Если не определено, то выбор происходит с начала файла.
    @param dtStopFilter: Конечная дата/время фильтра по времени.
        Если не определено, то выбор происходит до конца файла.
    @param tFilters: Кортеж/список дополнительных методов фильтрации.
        Методы фильтрации задаются как lambda или функции, которые принимают
        Словарь записи, а возвращают True-запись попадает в выбор/False - не попадает.
    @param sFilterLogic: Комманда способа обработки дополнительных фильтров
        AND - Чтобы запись попала в выбор необходимо положительное выполнение всех фильтров,
        OR - Чтобы запись попала в выбор достаточно положительное выполнение одного фильтра.
    @return: Объект панели или None в случае ошибки.
    """
    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    if sLogFileName is None:
        sLogFileName = log.get_log_filename()

    panel = icLogBrowserPanel(parent=parent)
    panel.init()
    panel.set_log_filename(sLogFileName)
    panel.set_datetime_filter_range(dtStartFilter, dtStopFilter)
    panel.set_log_types_filter(*(tLogTypes if tLogTypes else ()))
    panel.set_filters(sFilterLogic, *(tFilters if tFilters else ()))
    panel.refresh()
    return panel


def show_log_browser_dlg(parent=None, sLogFileName=None, tLogTypes=None,
                         dtStartFilter=None, dtStopFilter=None,
                         tFilters=None, sFilterLogic=None):
    """
    Вызвать диалоговое окно
    @param parent: Родительское окно.
        Если не указано, то берется главное окно.
    @param sLogFileName: Полное имя log файла.
    @param tLogTypes: Кортеж/список типов сообщений.
    @param dtStartFilter: Начальная дата/время фильтра по времени.
        Если не определено, то выбор происходит с начала файла.
    @param dtStopFilter: Конечная дата/время фильтра по времени.
        Если не определено, то выбор происходит до конца файла.
    @param tFilters: Кортеж/список дополнительных методов фильтрации.
        Методы фильтрации задаются как lambda или функции, которые принимают
        Словарь записи, а возвращают True-запись попадает в выбор/False - не попадает.
    @param sFilterLogic: Комманда способа обработки дополнительных фильтров
        AND - Чтобы запись попала в выбор необходимо положительное выполнение всех фильтров,
        OR - Чтобы запись попала в выбор достаточно положительное выполнение одного фильтра.
    @return: True/False.
    """
    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    if sLogFileName is None:
        sLogFileName = log.get_log_filename()

    dlg = icLogBrowserDlg(parent=parent)
    dlg.init()
    dlg.set_log_filename(sLogFileName)
    dlg.set_datetime_filter_range(dtStartFilter, dtStopFilter)
    dlg.set_log_types_filter(*(tLogTypes if tLogTypes else ()))
    dlg.set_filters(sFilterLogic, *(tFilters if tFilters else ()))
    dlg.refresh()
    result = dlg.ShowModal()
    return result == wx.ID_OK


def test():
    """
    Тестовая функция.
    """
    from ic import config
    from ic.log import log
    log.init(config)
    app = wx.PySimpleApp()

    frame = wx.Frame(None)
    show_log_browser_dlg(parent=frame,
                         dtStartFilter=datetime.datetime(year=2017, month=7, day=4))
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
