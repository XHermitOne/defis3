#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль диалога просмотра результата SQL запроса.
"""

import traceback
import wx
import wx.propgrid
from. import view_sql_query_dlg_proto

import ic
from ic.log import log
from ic.utils import txtgen
from ic.utils import ic_str

# Для управления взаимодействия с контролами wxPython
# используется менеджер форм <form_manager.icFormManager>
from ic.engine import form_manager


__version__ = (0, 0, 1, 3)

UNIX_CR = '\n'
WIN_CR = '\r\n'

ERROR_FIELD = (u'Error', )
ERROR_COL_WIDTH = 700


class icViewSQLQueryDialog(view_sql_query_dlg_proto.icViewSQLQueryDialogProto,
                           form_manager.icFormManager):
    """
    Форма диалога просмотра результата SQL запроса.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        view_sql_query_dlg_proto.icViewSQLQueryDialogProto.__init__(self, *args, **kwargs)

        # Шаблон SQL запроса
        self.sql_query = u''

        # Переменные SQL запроса
        self.variables = dict()

        # БД
        self.db = None

    def setDB(self, db):
        """
        Установить БД.
        @param db: Объект БД.
        """
        self.db = db
        if self.db is None:
            log.warning(u'Не установлен объект БД в окне просмотра результатов SQL запроса')
            log.warning(u'SQL запросы не будут выполняться')

    def setSQLQuery(self, sql_txt):
        """
        Установить SQL запрос для просмотра.
        @param sql_txt: Текст SQL запроса.
        @return: True/False.
        """
        if not sql_txt:
            log.warning(u'Не определен текст SQL запроса')
            return False

        # Необходимо заменить перевод кареток
        sql_txt = sql_txt.replace('\\n', UNIX_CR)

        # Запоминаем шаблон запроса
        self.sql_query = sql_txt

        # Парсим шаблона и выбираем имена переменных
        if txtgen.is_genered(self.sql_query):
            log.debug(u'SQL запрос генерируемый')
            var_names = txtgen.get_raplace_names(self.sql_query)
            self.variables = dict([(name, u'') for name in var_names])
            self.setVariables(self.variables)
        return True

    def setVariables(self, variables):
        """
        Установить переменные SQl запроса для редактирования.
        @param variables: Словарь переменных.
        @return: True/False.
        """
        if variables is None:
            variables = self.variables

        if not isinstance(variables, dict):
            log.warning(u'Ошибка типа словаря переменных SQl запроса.')
            return False

        var_names = variables.keys()
        var_names.sort()

        self.var_propertyGrid.Clear()
        for var_name in var_names:
            wx_property = wx.propgrid.StringProperty(var_name, value=u'')
            self.var_propertyGrid.Append(wx_property)

    def getSQLText(self, sql_query=None, variables=None):
        """
        Получить текст SQL запроса в зависимости от значения переменных.
        @param sql_query: Шаблон SQL запроса.
        @param variables: Словарь переменных.
        @return: Текст SQL запроса.
        """
        if sql_query is None:
            sql_query = self.sql_query
        if variables is None:
            variables = self.variables

        return txtgen.gen(sql_query, variables)

    def getVariables(self):
        """
        Получить словарь отредактированных переменных.
        @return: Словарь отредактированных переменных.
        """
        variables = dict()
        for property_name in self.variables.keys():
            value = self.var_propertyGrid.GetPropertyValueAsString(property_name)
            variables[property_name] = value
        return variables

    def refreshSQLText(self, sql_query=None, variables=None):
        """
        Обновить текст SQL запроса в зависимости от значения переменных.
        @param sql_query: Шаблон SQL запроса.
        @param variables: Словарь переменных.
        @return: True/False
        """
        if sql_query is None:
            sql_query = self.sql_query
        if variables is None:
            variables = self.variables

        sql_text = self.getSQLText(sql_query, variables)
        if sql_text:
            self.sql_textCtrl.SetValue(sql_text)
            return True
        else:
            log.warning(u'Ошибка определения текста SQL запроса')
        return False

    def refreshDataList(self, sql_query=None, variables=None):
        """
        Обновление списка записей - результатов запроса.
        @param sql_query: Шаблон SQL запроса.
        @param variables: Словарь переменных.
        @return: True/False
        """
        if sql_query is None:
            sql_query = self.sql_query
        if variables is None:
            variables = self.variables

        sql_text = self.getSQLText(sql_query, variables)
        if sql_text:
            # Есть заполненное sql выражение
            query_tab = self.getSQLDataset(sql_text)
            if query_tab:
                # Колонки
                fields = query_tab.get('__fields__', ())
                if fields == ERROR_FIELD:
                    cols = [dict(label=field_name, width=ERROR_COL_WIDTH) for field_name in fields]
                else:
                    cols = [dict(label=field_name, width=-1) for field_name in fields]
                # Строки
                rows = query_tab.get('__data__', ())

                self.setColumns_list_ctrl(self.records_listCtrl, cols=cols)
                self.setRows_list_ctrl(self.records_listCtrl, rows=rows)
                if rows:
                    # Автообразмерить колонки
                    self.setColumnsAutoSize_list_ctrl(self.records_listCtrl)
                return True
        return False

    def getSQLDataset(self, sql_text):
        """
        Получить набор записей по заполненному SQL выражению.
        @param sql_text: SQL выражение.
        @return: Заполненная таблица запроса.
            Формат:
            ТАБЛИЦА ЗАПРОСА ПРЕДСТАВЛЯЕТСЯ В ВИДЕ СЛОВАРЯ
            {'__fields__': имена полей таблицы, '__data__': данные таблицы}
        """
        if self.db is None:
            error_txt = u'Не установлен объект БД в окне просмотра результатов SQL запроса'
        else:
            try:
                query_table = self.db.executeSQL(sql_text)

                query_table['__fields__'] = [field[0] for field in query_table['__fields__']]
                query_table['__data__'] = list(query_table['__data__'])
                for i, rec in enumerate(query_table['__data__']):
                    query_table['__data__'][i] = [ic_str.toUnicode(value, self.db.getEncoding()) for value in rec]
                return query_table
            except:
                error_txt = traceback.format_exc()
                log.fatal(u'Ошибка получения набора записей по SQL выражению <%s>' % sql_text)
        error_list = error_txt.split(UNIX_CR)
        return {'__fields__': ERROR_FIELD, '__data__': [(line, ) for line in error_list]}

    def init(self):
        """
        Инициализация диалогового окна
        """
        self.init_ctrl()

    def init_ctrl(self):
        """
        Инициализация контролов диалогового окна.
        """
        self.ctrl_toolBar.EnableTool(self.expand_tool.GetId(), False)
        self.refreshSQLText()

    def onCollapseToolClicked(self, event):
        """
        Обработчик свертывания панели запроса.
        """
        self.collapseSplitterPanel(self.panel_splitter,
                                   self.ctrl_toolBar,
                                   collapse_tool=self.collapse_tool,
                                   expand_tool=self.expand_tool)
        event.Skip()

    def onExpandToolClicked(self, event):
        """
        Обработчик свертывания панели запроса.
        """
        self.expandSplitterPanel(self.panel_splitter,
                                 self.ctrl_toolBar,
                                 collapse_tool=self.collapse_tool,
                                 expand_tool=self.expand_tool)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        Обработчик кнопки <OK>.
        """
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onRefreshToolClicked(self, event):
        """
        Обработчик обновление данных SQL запроса.
        """
        self.variables = self.getVariables()
        self.refreshSQLText(variables=self.variables)
        self.refreshDataList(variables=self.variables)
        event.Skip()


def view_sql_query_dlg(parent=None, db=None, sql_txt=None):
    """
    Запуск диалогового окна просмотра результата SQL запроса.
    @param parent: Родительское окно.
    @param db: Объект БД.
    @param sql_txt: Текст SQL запроса.
    """
    if parent is None:
        parent = ic.getMainWin()

    dlg = icViewSQLQueryDialog(parent)
    # Т.к. инициализация некоторых контролов зависит
    # от содержимого sql запроса
    # то сначала инициализируем sql запрос в диалоговом окне ...
    dlg.setDB(db)
    dlg.setSQLQuery(sql_txt)
    # ... а затем инициализируем все остальное
    dlg.init()
    dlg.ShowModal()

    return True


def test():
    """
    Функция тестирования.
    @return:
    """
    app = wx.PySimpleApp()

    view_sql_query_dlg()

    app.MainLoop()


if __name__ == '__main__':
    test()
