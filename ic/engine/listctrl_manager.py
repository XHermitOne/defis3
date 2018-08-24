#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль класса - менеджера абстрактного спискового контрола WX.
"""

# Подключение библиотек
import sys
import wx
import wx.adv
import wx.gizmos
import wx.dataview

from ic.log import log
from ic.utils import ic_str
from ic.utils import wxfunc
from ic import config


__version__ = (0, 1, 1, 1)


class icListCtrlManager(object):
    """
    Менеджер WX спискового контрола.
    В самом общем случае в этот класс перенесены функции работы
    со списковыми контролами из менеджера форм.
    Перенос сделан с целью рефакторинга.
    Также этот класс могут наследовать классы специализированных
    менеджеров, которые работают со списками записей/объектов.
    """

    def _get_wxDataViewListCtrl_data(self, ctrl):
        """
        Получить данные из контрола wxDataViewListCtrl.
        @param ctrl: Объект контрола.
        @return: Список словарей - строк контрола.
        """
        recordset = list()
        store = ctrl.GetStore()
        # Определить имена колонок контрола
        self_col_names = [name for name in dir(self) if
                          issubclass(getattr(self, name).__class__, wx.dataview.DataViewColumn)]
        # По именом определить объекты колонок определенные в диалоговой форме
        self_cols = [getattr(self, name) for name in self_col_names]

        for i_row in range(store.GetCount()):
            record = dict()
            for i_col in range(ctrl.GetColumnCount()):
                # Колонка контрола
                col = ctrl.GetColumn(i_col)
                # Если можно определить имя колонки, то берем имя
                # иначе берем в качестве имени индекс
                col_name = self_col_names[wxfunc.get_index_wx_object_in_list(col, self_cols)] if wxfunc.is_wx_object_in_list(col, self_cols) else i_col
                # Добавить значение колонки в запись
                record[col_name] = ctrl.GetValue(i_row, i_col)
            recordset.append(record)

        return recordset

    def _set_wxDataViewListCtrl_data(self, ctrl, records):
        """
        Установить данные в контрол wxDataViewListCtrl.
        @param ctrl: Объект контрола.
        @param records: Список словарей - записей.
            Имя колонки в записи может задаваться как именем,
            так и индексом.
        @return: True/False.
        """
        # Сначала очистить контрол от записей
        ctrl.DeleteAllItems()

        # Определить имена колонок контрола
        self_col_names = [name for name in dir(self) if
                          issubclass(getattr(self, name).__class__, wx.dataview.DataViewColumn)]
        # По именом определить объекты колонок определенные в диалоговой форме
        self_cols = [getattr(self, name) for name in self_col_names]

        for record in records:
            wx_rec = [u''] * ctrl.GetColumnCount()
            for colname, value in record.items():
                if isinstance(colname, str):
                    # Колонка задается именем
                    if colname in self_col_names:
                        i_colname = self_col_names.index(colname)
                        idx = wxfunc.get_index_wx_object_in_list(self_cols[i_colname],
                                                                 ctrl.GetColumns())
                        wx_rec[idx] = ic_str.toUnicode(value)
                    else:
                        log.warning(u'Не найдено имя колонки <%s> при заполнении wxDataViewListCtrl контрола данными' % colname)
                elif isinstance(colname, int):
                    # Колонка задается индексом
                    wx_rec[colname] = ic_str.toUnicode(value)
                else:
                    log.warning(u'Не поддерживаемый тип имени колонки <%s> при заполнении wxDataViewListCtrl контрола данными' % colname)
            ctrl.AppendItem(wx_rec)

        return True

    def refresh_DataViewListCtrl(self, ctrl, data_list=None, columns=None):
        """
        Обновить список строк контрола типа wx.dataview.DataViewListCtrl
        @param ctrl: Объект контрола.
        @param data_list: Данные списка.
        @param columns: Список/кортеж колонок в случае если строки списка
            задаются словарями.
        """
        if data_list is None:
            data_list = list()

        if columns is not None:
            data_list = [[rec[col] for col in columns] for rec in data_list]

        # Удаляем все строки
        ctrl.DeleteAllItems()
        for row in data_list:
            ctrl.AppendItem(row)

    def refresh_ListCtrl(self, ctrl, data_list=None, columns=None):
        """
        Обновить список строк контрола типа wx.ListCtrl
        @param ctrl: Объект контрола.
        @param data_list: Данные списка.
        @param columns: Список/кортеж колонок в случае если строки списка
            задаются словарями.
        """
        if data_list is None:
            data_list = list()

        if columns is not None:
            data_list = [[rec[col] for col in columns] for rec in data_list]

        self.setRows_list_ctrl(ctrl, data_list)

    def refresh_list_ctrl(self, ctrl=None, data_list=None, columns=None):
        """
        Обновить список строк контрола.
        @param ctrl: Объект контрола.
        @param data_list: Данные списка.
        @param columns: Список/кортеж колонок в случае если строки списка
            задаются словарями.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для обновления')
            return

        if isinstance(ctrl, wx.dataview.DataViewListCtrl):
            self.refresh_DataViewListCtrl(ctrl, data_list, columns)
        else:
            log.warning(u'Обновление списка контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)

    def moveUpRow_DataViewListCtrl(self, ctrl, data_list=None, idx=wx.NOT_FOUND,
                                   columns=None, n_col=None, do_refresh=False):
        """
        Переместить строку выше в контроле типа wx.dataview.DataViewListCtrl
        @param ctrl: Объект контрола.
        @param data_list: Данные списка.
        @param idx: Индекс перемещаемой строки.
        @param columns: Список/кортеж колонок в случае если строки списка
            задаются словарями.
        @param n_col: Наименование/индекс колонки номера строки.
            Если не определено, то нет такой колонки.
        @param do_refresh: Произвести полное обновление контрола?
        @return: True - было сделано перемещение, False - перемещения не было.
        """
        if idx != wx.NOT_FOUND and idx > 0:
            # Поменять номер строки если необходимо
            if n_col is not None:
                value = data_list[idx][n_col]
                data_list[idx][n_col] = data_list[idx - 1][n_col]
                data_list[idx - 1][n_col] = value
            # Поменять значения строк
            value = data_list[idx - 1]
            data_list[idx - 1] = data_list[idx]
            data_list[idx] = value

            if do_refresh:
                # Обновляем полностью контрол
                self.refresh_DataViewListCtrl(ctrl, data_list, columns=columns)
            else:
                # Обновляем конкретные строки
                for i_col, value in enumerate(data_list[idx-1]):
                    ctrl.SetTextValue(value if isinstance(value, str) else str(value), idx-1, i_col)
                for i_col, value in enumerate(data_list[idx]):
                    ctrl.SetTextValue(value if isinstance(value, str) else str(value), idx, i_col)
            ctrl.SelectRow(idx - 1)
            return True
        else:
            log.warning(u'Не выбрана перемещаемая строка списка')
        return False

    def moveUpRow_ListCtrl(self, ctrl, data_list=None, idx=wx.NOT_FOUND,
                           columns=None, n_col=None, do_refresh=False):
        """
        Переместить строку выше в контроле типа wx.ListCtrl
        @param ctrl: Объект контрола.
        @param data_list: Данные списка.
        @param idx: Индекс перемещаемой строки.
        @param columns: Список/кортеж колонок в случае если строки списка
            задаются словарями.
        @param n_col: Наименование/индекс колонки номера строки.
            Если не определено, то нет такой колонки.
        @param do_refresh: Произвести полное обновление контрола?
        @return: True - было сделано перемещение, False - перемещения не было.
        """
        if idx != wx.NOT_FOUND and idx > 0:
            # Поменять номер строки если необходимо
            if n_col is not None:
                value = data_list[idx][n_col]
                data_list[idx][n_col] = data_list[idx - 1][n_col]
                data_list[idx - 1][n_col] = value
            # Поменять значения строк
            value = data_list[idx - 1]
            data_list[idx - 1] = data_list[idx]
            data_list[idx] = value

            if do_refresh:
                # Обновляем полностью контрол
                self.refresh_ListCtrl(ctrl, data_list, columns=columns)
            else:
                # Обновляем конкретные строки
                for i_col, value in enumerate(data_list[idx-1]):
                    ctrl.SetStringItem(idx-1, i_col, value if isinstance(value, str) else str(value))
                for i_col, value in enumerate(data_list[idx]):
                    ctrl.SetStringItem(idx, i_col, value if isinstance(value, str) else str(value))
            ctrl.Select(idx - 1)
            return True
        else:
            log.warning(u'Не выбрана перемещаемая строка списка')
        return False

    def moveUpRow_list_ctrl(self, ctrl, data_list=None, idx=wx.NOT_FOUND,
                            columns=None, n_col=None, do_refresh=False):
        """
        Переместить строку выше в контроле.
        @param ctrl: Объект контрола.
        @param data_list: Данные списка.
        @param idx: Индекс перемещаемой строки.
        @param columns: Список/кортеж колонок в случае если строки списка
            задаются словарями.
        @param n_col: Наименование/индекс колонки номера строки.
            Если не определено, то нет такой колонки.
        @param do_refresh: Произвести полное обновление контрола?
        @return: True - было сделано перемещение, False - перемещения не было.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для обновления')
            return False

        if isinstance(ctrl, wx.dataview.DataViewListCtrl):
            return self.moveUpRow_DataViewListCtrl(ctrl=ctrl, data_list=data_list,
                                                   idx=idx, columns=columns, n_col=n_col,
                                                   do_refresh=do_refresh)
        elif isinstance(ctrl, wx.ListCtrl):
            return self.moveUpRow_ListCtrl(ctrl=ctrl, data_list=data_list,
                                           idx=idx, columns=columns, n_col=n_col,
                                           do_refresh=do_refresh)
        else:
            log.warning(u'Перемещение строки списка контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)
        return False

    def moveDownRow_DataViewListCtrl(self, ctrl, data_list=None, idx=wx.NOT_FOUND,
                                     columns=None, n_col=None, do_refresh=False):
        """
        Переместить строку ниже в контроле типа wx.dataview.DataViewListCtrl
        @param ctrl: Объект контрола.
        @param data_list: Данные списка.
        @param idx: Индекс перемещаемой строки.
        @param columns: Список/кортеж колонок в случае если строки списка
            задаются словарями.
        @param n_col: Наименование/индекс колонки номера строки.
            Если не определено, то нет такой колонки.
        @param do_refresh: Произвести полное обновление контрола?
        @return: True - было сделано перемещение, False - перемещения не было.
        """
        if idx != wx.NOT_FOUND and idx < (len(data_list) - 1):
            # Поменять номер строки если необходимо
            if n_col is not None:
                value = data_list[idx][n_col]
                data_list[idx][n_col] = data_list[idx + 1][n_col]
                data_list[idx + 1][n_col] = value
            # Поменять значения строк
            value = data_list[idx + 1]
            data_list[idx + 1] = data_list[idx]
            data_list[idx] = value

            if do_refresh:
                # Обновляем полностью контрол
                self.refresh_DataViewListCtrl(ctrl, data_list, columns=columns)
            else:
                # Обновляем конкретные строки
                for i_col, value in enumerate(data_list[idx]):
                    ctrl.SetTextValue(value if isinstance(value, str) else str(value), idx, i_col)
                for i_col, value in enumerate(data_list[idx+1]):
                    ctrl.SetTextValue(value if isinstance(value, str) else str(value), idx+1, i_col)
            ctrl.SelectRow(idx + 1)
            return True
        else:
            log.warning(u'Не выбрана строка списка для перемещения')
        return False

    def moveDownRow_ListCtrl(self, ctrl, data_list=None, idx=wx.NOT_FOUND,
                             columns=None, n_col=None, do_refresh=False):
        """
        Переместить строку ниже в контроле типа wx.ListCtrl
        @param ctrl: Объект контрола.
        @param data_list: Данные списка.
        @param idx: Индекс перемещаемой строки.
        @param columns: Список/кортеж колонок в случае если строки списка
            задаются словарями.
        @param n_col: Наименование/индекс колонки номера строки.
            Если не определено, то нет такой колонки.
        @param do_refresh: Произвести полное обновление контрола?
        @return: True - было сделано перемещение, False - перемещения не было.
        """
        if idx != wx.NOT_FOUND and idx < (len(data_list) - 1):
            # Поменять номер строки если необходимо
            if n_col is not None:
                value = data_list[idx][n_col]
                data_list[idx][n_col] = data_list[idx + 1][n_col]
                data_list[idx + 1][n_col] = value
            # Поменять значения строк
            value = data_list[idx + 1]
            data_list[idx + 1] = data_list[idx]
            data_list[idx] = value

            if do_refresh:
                # Обновляем полностью контрол
                self.refresh_ListCtrl(ctrl, data_list, columns=columns)
            else:
                # Обновляем конкретные строки
                for i_col, value in enumerate(data_list[idx]):
                    ctrl.SetStringItem(idx, i_col, value if isinstance(value, str) else str(value))
                for i_col, value in enumerate(data_list[idx+1]):
                    ctrl.SetStringItem(idx+1, i_col, value if isinstance(value, str) else str(value))
            ctrl.Select(idx + 1)
            return True
        else:
            log.warning(u'Не выбрана строка списка для перемещения')
        return False

    def moveDownRow_list_ctrl(self, ctrl, data_list=None, idx=wx.NOT_FOUND,
                              columns=None, n_col=None, do_refresh=False):
        """
        Переместить строку ниже в контроле.
        @param ctrl: Объект контрола.
        @param data_list: Данные списка.
        @param idx: Индекс перемещаемой строки.
        @param columns: Список/кортеж колонок в случае если строки списка
            задаются словарями.
        @param n_col: Наименование/индекс колонки номера строки.
            Если не определено, то нет такой колонки.
        @param do_refresh: Произвести полное обновление контрола?
        @return: True - было сделано перемещение, False - перемещения не было.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для обновления')
            return False

        if isinstance(ctrl, wx.dataview.DataViewListCtrl):
            return self.moveDownRow_DataViewListCtrl(ctrl=ctrl, data_list=data_list,
                                                     idx=idx, columns=columns, n_col=n_col,
                                                     do_refresh=do_refresh)
        elif isinstance(ctrl, wx.ListCtrl):
            return self.moveDownRow_ListCtrl(ctrl=ctrl, data_list=data_list,
                                             idx=idx, columns=columns, n_col=n_col,
                                             do_refresh=do_refresh)
        else:
            log.warning(u'Перемещение строки списка контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)
        return False

    def appendColumn_ListCtrl(self, ctrl, label=u'', width=-1, align='LEFT'):
        """
        Добавить колонку в wx.ListCtrl.
        ВНИМАНИЕ! На старых ОС (...-16.04) wx.LIST_AUTOSIZE_USEHEADER не работает!!!
            Поэтому для автоширины используем везде wx.LIST_AUTOSIZE.
        @param ctrl: Объект контрола wx.ListCtrl.
        @param label: Надпись колонки.
        @param width: Ширина колонки.
        @param align: Выравнивание: LEFT/RIGHT.
        @return: True - все прошло нормально / False - какая-то ошибка.
        """
        try:
            i = ctrl.GetColumnCount()
            if width <= 0:
                width = wx.LIST_AUTOSIZE

            col_align = str(align).strip().upper()
            if col_align == 'RIGHT':
                col_format = wx.LIST_FORMAT_RIGHT
            elif col_align == 'CENTRE':
                col_format = wx.LIST_FORMAT_CENTRE
            elif col_align == 'CENTER':
                col_format = wx.LIST_FORMAT_CENTER
            else:
                col_format = wx.LIST_FORMAT_LEFT
            ctrl.InsertColumn(i, label, width=width, format=col_format)
            return True
        except:
            log.fatal(u'Ошибка добавления колонки в контрол wx.ListCtrl')
        return False

    def appendColumn_list_ctrl(self, ctrl=None, label=u'', width=-1, align='LEFT'):
        """
        Добавить колонку в контрол списка.
        @param ctrl: Объект контрола.
        @param label: Надпись колонки.
        @param width: Ширина колонки.
        @param align: Выравнивание: LEFT/RIGHT.
        @return: True - все прошло нормально / False - какая-то ошибка.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для добавления колонки')
            return False

        if isinstance(ctrl, wx.ListCtrl):
            return self.appendColumn_ListCtrl(ctrl=ctrl, label=label, width=width)
        else:
            log.warning(u'Добавление колонки списка контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)
        return False

    def setColumns_list_ctrl(self, ctrl=None, cols=()):
        """
        Установить колонки в контрол списка.
        @param ctrl: Объект контрола.
        @param cols: Список описаний колонок.
            колонка может описываться как списком
            ('Заголовок колонки', Ширина колонки, Выравнивание)
            так и словарем:
            {'label': Заголовок колонки,
            'width': Ширина колонки,
            'align': Выравнивание}
            ВНИМАНИЕ! На старых ОС (...-16.04) wx.LIST_AUTOSIZE_USEHEADER не работает!!!
                Поэтому для автоширины используем везде wx.LIST_AUTOSIZE.
        @return: True - все прошло нормально / False - какая-то ошибка.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для добавления колонки')
            return False

        if isinstance(ctrl, wx.ListCtrl):
            result = True
            ctrl.ClearAll()
            for col in cols:
                if isinstance(col, dict):
                    result = result and self.appendColumn_ListCtrl(ctrl=ctrl, **col)
                elif isinstance(col, list) or isinstance(col, tuple):
                    result = result and self.appendColumn_ListCtrl(ctrl, *col)
            return result

        elif isinstance(ctrl, wx.gizmos.TreeListCtrl):
            col_count = ctrl.GetColumnCount()
            if col_count:
                for i_col in range(col_count-1, -1, -1):
                    ctrl.RemoveColumn(i_col)
            for i_col, col in enumerate(cols):
                if isinstance(col, dict):
                    ctrl.AddColumn(col.get('label', u''))
                    ctrl.SetColumnWidth(i_col, col.get('width', wx.COL_WIDTH_AUTOSIZE))
                elif isinstance(col, list) or isinstance(col, tuple):
                    ctrl.AddColumn(col[0])
                    ctrl.SetColumnWidth(i_col, col[1])
                else:
                    log.warning(u'Не поддерживаемый тип данных колонки')
            # Назначить первую колонку главной
            ctrl.SetMainColumn(0)
            return True
        else:
            log.warning(u'Добавление колонок списка контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)
        return False

    def setColumnsAutoSize_list_ctrl(self, ctrl=None):
        """
        Установить авторазмер колонок контрола списка.
        ВНИМАНИЕ! На старых ОС (...-16.04) wx.LIST_AUTOSIZE_USEHEADER не работает!!!
            Поэтому для автоширины используем везде wx.LIST_AUTOSIZE.
        @param ctrl: Объект контрола.
        @return: True - все прошло нормально / False - какая-то ошибка.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для установки авторазмеров списка')
            return False

        if isinstance(ctrl, wx.ListCtrl):
            # Обновить размер колонок
            for i in range(ctrl.GetColumnCount()):
                ctrl.SetColumnWidth(i, wx.LIST_AUTOSIZE)
            return True
        else:
            log.warning(u'Установление авторазмера колонок списка контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)
        return False

    def appendRow_ListCtrl(self, ctrl, row=(),
                           evenBackgroundColour=None, oddBackgroundColour=None):
        """
        Добавить строку в контрол wx.ListCtrl.
        @param ctrl: Объект контрола wx.ListCtrl.
        @param row: Список строки по полям.
        @param evenBackgroundColour: Цвет фона четных строк.
        @param oddBackgroundColour: Цвет фона нечетных строк.
        @return: True - все прошло нормально / False - какая-то ошибка.
        """
        if type(row) not in (list, tuple):
            log.warning(u'Не корректный тип списка строки <%s> объекта wx.ListCtrl' % type(row))
            return False

        try:
            row_idx = -1
            # Ограничить список количеством колонок
            row = row[:ctrl.GetColumnCount()]
            for i, value in enumerate(row):
                if value is None:
                    value = u''
                elif type(value) in (int, float):
                    value = str(value)
                # elif isinstance(value, str):
                #    value = unicode(value, config.DEFAULT_ENCODING)
                elif isinstance(value, str):
                    pass
                else:
                    value = str(value)

                if i == 0:
                    row_idx = ctrl.InsertStringItem(sys.maxsize, value)
                else:
                    ctrl.SetStringItem(row_idx, i, value)

            if row_idx != -1:
                if evenBackgroundColour and not (row_idx % 2):
                    # Добавляемая строка четная?
                    ctrl.SetItemBackgroundColour(row_idx, evenBackgroundColour)
                elif oddBackgroundColour and (row_idx % 2):
                    # Добавляемая строка не четная?
                    ctrl.SetItemBackgroundColour(row_idx, oddBackgroundColour)
            return True
        except:
            log.fatal(u'Ошибка добавления строки %s в контрол wx.ListCtrl' % str(row))
        return False

    def appendRow_list_ctrl(self, ctrl=None, row=(),
                            evenBackgroundColour=None, oddBackgroundColour=None):
        """
        Добавить строку в контрол списка.
        @param ctrl: Объект контрола.
        @param row: Список строки по полям.
        @param evenBackgroundColour: Цвет фона четных строк.
        @param oddBackgroundColour: Цвет фона нечетных строк.
        @return: True - все прошло нормально / False - какая-то ошибка.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для добавления строки')
            return False

        if isinstance(ctrl, wx.ListCtrl):
            return self.appendRow_ListCtrl(ctrl=ctrl, row=row,
                                           evenBackgroundColour=evenBackgroundColour,
                                           oddBackgroundColour=oddBackgroundColour)
        elif isinstance(ctrl, wx.dataview.DataViewListCtrl):
            ctrl.AppendItem(row)
            return True
        else:
            log.warning(u'Добавление колонок списка контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)
        return False

    def setRow_list_ctrl(self, ctrl=None, row_idx=-1, row=(),
                         evenBackgroundColour=None, oddBackgroundColour=None,
                         doSavePos=False):
        """
        Установить строку контрола списка.
        @param ctrl: Объект контрола.
        @param row_idx: Индекс строки. Если -1, то строка не устанавливается.
        @param row: Cтрока.
            Строка представляет собой список/кортеж:
            (Значение 1, Значение 2, ..., Значение N),
        @param evenBackgroundColour: Цвет фона четных строк.
        @param oddBackgroundColour: Цвет фона нечетных строк.
        @param doSavePos: Сохранять позицию курсора?
        @return: True - все прошло нормально / False - какая-то ошибка.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для установки строки')
            return False
        if row_idx == -1:
            log.warning(u'Не указан индекс устанавливаемой строки')
            return False
        if not isinstance(row, list) and not isinstance(row, tuple):
            log.warning(u'Не корректный тип данных строки <%s>' % row.__class__.__name__)
            return False

        if isinstance(ctrl, wx.ListCtrl):
            row_count = ctrl.GetItemCount()
            if 0 > row_idx > row_count:
                log.warning(u'Не корректный индекс <%d> контрола <%s>' % (row_idx, ctrl.__class__.__name__))
                return False
            cursor_pos = None
            if doSavePos:
                cursor_pos = ctrl.GetFirstSelected()

            for i, item in enumerate(row):
                item_str = ic_str.toUnicode(item, config.DEFAULT_ENCODING)
                ctrl.SetStringItem(row_idx, i, item_str)
                if evenBackgroundColour and not (row_idx % 2):
                    # Четная строка?
                    ctrl.SetItemBackgroundColour(row_idx, evenBackgroundColour)
                elif oddBackgroundColour and (row_idx % 2):
                    # Не четная строка?
                    ctrl.SetItemBackgroundColour(row_idx, oddBackgroundColour)
            if cursor_pos not in (None, -1) and cursor_pos < row_count:
                ctrl.Select(cursor_pos)
            return True
        else:
            log.warning(u'Установка строки контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)
        return False

    def setRows_list_ctrl(self, ctrl=None, rows=(),
                          evenBackgroundColour=None, oddBackgroundColour=None,
                          doSavePos=False):
        """
        Установить строки в контрол списка.
        @param ctrl: Объект контрола.
        @param rows: Список строк.
            Строка представляет собой список:
            [
            (Значение 1, Значение 2, ..., Значение N), ...
            ]
        @param evenBackgroundColour: Цвет фона четных строк.
        @param oddBackgroundColour: Цвет фона нечетных строк.
        @param doSavePos: Сохранять позицию курсора?
        @return: True - все прошло нормально / False - какая-то ошибка.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для добавления строк')
            return False

        if isinstance(ctrl, wx.ListCtrl):
            result = True
            cursor_pos = None
            if doSavePos:
                cursor_pos = ctrl.GetFirstSelected()
            ctrl.DeleteAllItems()
            for row in rows:
                if isinstance(row, list) or isinstance(row, tuple):
                    result = result and self.appendRow_ListCtrl(ctrl=ctrl, row=row,
                                                                evenBackgroundColour=evenBackgroundColour,
                                                                oddBackgroundColour=oddBackgroundColour)
            if cursor_pos not in (None, -1):
                try:
                    len_rows = len(rows)
                    if cursor_pos < len_rows:
                        ctrl.Select(cursor_pos)
                        # Использую для прокрутки скролинга до выбранного элемента
                        ctrl.Focus(cursor_pos)
                    elif len_rows:
                        ctrl.Select(len_rows - 1)
                        # Использую для прокрутки скролинга до выбранного элемента
                        ctrl.Focus(len_rows - 1)
                except:
                    log.fatal(u'Ошибка восставления выбора элемента списка')
            return result
        elif isinstance(ctrl, wx.dataview.DataViewListCtrl):
            result = True
            cursor_pos = None
            if doSavePos:
                cursor_pos = ctrl.GetSelection()
            ctrl.DeleteAllItems()
            for row in rows:
                if isinstance(row, list) or isinstance(row, tuple):
                    try:
                        ctrl.AppendItem(row)
                        result = result and True
                    except:
                        log.fatal(u'Ошибка доавления строки %s в контрол <%s>' % (str(row), ctrl.__class__.__name__))
                        result = False
            if cursor_pos not in (None, -1):
                try:
                    len_rows = len(rows)
                    if cursor_pos < len_rows:
                        ctrl.SelectRow(cursor_pos)
                    elif len_rows:
                        ctrl.SelectRow(len_rows - 1)
                except:
                    log.fatal(u'Ошибка восставления выбора элемента списка')
            return result
        else:
            log.warning(u'Добавление колонок контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)
        return False

    def setRowColour_list_ctrl_requirement(self, ctrl=None, rows=(),
                                           fg_colour=None, bg_colour=None, requirement=None):
        """
        Установить цвет строки в контроле списка по определенному условию.
        @param ctrl: Объект контрола.
        @param rows: Список строк.
        @param fg_colour: Цвет текста, если условие выполненно.
        @param bg_colour: Цвет фона, если условие выполненно.
        @param requirement: lambda выражение, формата:
            lambda i, row: ...
            Которое возвращает True/False.
            Если True, то установка цвета будет сделана.
            False - строка не расцвечивается.
        @return: True/False.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для установления цвета строки')
            return False
        if requirement is None:
            log.warning(u'Не определено условие установки цвета')
            return False
        if fg_colour is None and bg_colour is None:
            log.warning(u'Не определены цвета')
            return False

        for i, row in enumerate(rows):
            colorize = requirement(i, row)
            if fg_colour and colorize:
                self.setRowForegroundColour_list_ctrl(ctrl, i, fg_colour)
            if bg_colour and colorize:
                self.setRowBackgroundColour_list_ctrl(ctrl, i, bg_colour)
        return True

    def setRowForegroundColour_list_ctrl(self, ctrl=None, i_row=0, colour=None):
        """
        Установить цвет текста строки в контроле списка.
        @param ctrl: Объект контрола.
        @param i_row: Индекс строки.
        @param colour: Цвет текста строки.
        @return: True - все прошло нормально / False - какая-то ошибка.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для установления цвета строки')
            return False
        if colour is None:
            colour = wx.SYS_COLOUR_CAPTIONTEXT

        if isinstance(ctrl, wx.ListCtrl):
            try:
                ctrl.SetItemTextColour(i_row, colour)
            except:
                log.warning(u'Не корректный индекс строки <%s>' % i_row)
                return False
            return True
        else:
            log.warning(u'Установление цвета строки контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)
        return False

    def setRowBackgroundColour_list_ctrl(self, ctrl=None, i_row=0, colour=None):
        """
        Установить цвет фона строки в контроле списка.
        @param ctrl: Объект контрола.
        @param i_row: Индекс строки.
        @param colour: Цвет фона строки.
        @return: True - все прошло нормально / False - какая-то ошибка.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для установления цвета строки')
            return False
        if colour is None:
            colour = wx.SYS_COLOUR_INACTIVECAPTION

        if isinstance(ctrl, wx.ListCtrl):
            try:
                ctrl.SetItemBackgroundColour(i_row, colour)
            except:
                log.warning(u'Не корректный индекс строки <%s>' % i_row)
                return False
            return True
        else:
            log.warning(u'Установление цвета строки контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)
        return False

    def getItemSelectedIdx(self, obj):
        """
        Получить индекс выбранного элемента контрола.
        Т.к. индекс выбранного элемента может возвращать объекты разных
        типов (контролы и события) то:
        Эта функция нужна чтобы не заботиться о названии функции
        для каждого контрола/события.
        @param obj: Объект контрола или события.
        @return: Индекс выбранного элемента или -1 если ничего не выбрано.
        """
        if isinstance(obj, wx.ListEvent):
            return obj.Index
        elif isinstance(obj, wx.ListCtrl):
            return obj.GetFirstSelected()
        elif isinstance(obj, wx.dataview.DataViewListCtrl):
            return obj.GetSelectedRow()

        log.warning(u'Объект типа <%s> не поддерживается как определитель выбранного элемента контрола' % obj.__class__.__name__)
        return -1

    def selectItem_list_ctrl(self, ctrl=None, item_idx=-1,
                             is_focus=True, deselect_prev=False):
        """
        Выбрать элемент контрола списка по индексу.
        @param ctrl: Объект контрола.
        @param is_focus: Автоматически переместить фокус на элемент?
        @param deselect_prev: Произвести отмену выбора предыдущего выбранного элемента?
        @return: True - выбор прошел успешно.
        """
        if ctrl is None:
            log.warning(u'Не указан контрол списка для выбора элемента')
            return False

        if isinstance(ctrl, wx.ListCtrl):
            if (0 > item_idx) or (item_idx >= ctrl.GetItemCount()):
                log.warning(u'Не корректный индекс <%d> контрола списка <%s>' % (item_idx, ctrl.__class__.__name__))
                return False
            if deselect_prev:
                ctrl.Select(self.getItemSelectedIdx(ctrl), 0)
            ctrl.Select(item_idx)
            if is_focus:
                ctrl.Focus(item_idx)
            return True
        elif isinstance(ctrl, wx.dataview.DataViewListCtrl):
            try:
                ctrl.SelectRow(item_idx)
            except:
                log.fatal(u'Ошибка индекса <%d> контрола списка <%s>' % (item_idx, ctrl.__class__.__name__))
                return False
            return True
        else:
            log.warning(u'Объект типа <%s> не поддерживается для выбора элемента контрола' % ctrl.__class__.__name__)
        return False

    def getItemCount(self, obj):
        """
        Получить количество элементов контрола.
        Т.к.  количество элементов контрола может возвращать объекты разных
        типов, то:
        Эта функция нужна чтобы не заботиться о названии функции
        для каждого контрола.
        @param obj: Объект контрола списка элементов.
        @return: Количество элементов контрола списка.
        """
        if isinstance(obj, wx.ListCtrl):
            return obj.GetItemCount()
        elif isinstance(obj, wx.dataview.DataViewListCtrl):
            log.warning(u'ВНИМАНИЕ! В этой версии wxPython не реализована функция получения количества элементов для контрола <%s>' % obj.__class__.__name__)
            return 0

        log.warning(u'Объект типа <%s> не поддерживается как определитель количества элементов контрола' % obj.__class__.__name__)
        return 0

    def getLastItemIdx(self, obj):
        """
        Индекс последнего элемента списка.
        @param obj: Объект контрола списка элементов.
        @return: Индекс последнего элемента контрола списка или -1 если
            в списке нет элементов.
        """
        item_count = self.getItemCount(obj)
        return item_count - 1

    def checkAllItems_list_ctrl(self, ctrl, check=True):
        """
        Установить галки всех элементов контрола списка.
        @param check: Вкл./выкл.
        @return: True/False.
        """
        return self.checkItems_list_ctrl(ctrl, check=check)

    def checkItems_list_ctrl(self, ctrl, check=True, n_begin=-1, n_end=-1):
        """
        Установить галки элементов контрола списка.
        @param ctrl: Объект контрола.
        @param check: Вкл./выкл.
        @param n_begin: Номер первого обрабатываемого элемента.
            Если не определен, то берется самый первый элемент.
        @param n_end: Номер последнего обрабатываемого элемента.
        @return: True/False.
        """
        if isinstance(ctrl, wx.ListCtrl):
            if n_begin < 0:
                n_begin = 0
            if n_end < 0:
                n_end = ctrl.GetItemCount() - 1
            for i in range(n_begin, n_end + 1):
                ctrl.CheckItem(i, check=check)
            return True

        log.warning(u'Объект типа <%s> не поддерживается вкл./выкл. элментов контрола' % ctrl.__class__.__name__)
        return False

    def getCheckedItems_list_ctrl(self, ctrl):
        """
        Получить список индексов помеченных/отмеченных элементов контрола списка.
        @param ctrl: Объект контрола списка элементов.
        @return: Список индексов помеченных элементов контрола списка.
            Либо None в случае ошибки.
        """
        if isinstance(ctrl, wx.ListCtrl):
            return [i for i in range(ctrl.GetItemCount()) if ctrl.IsChecked(i)]

        log.warning(u'Объект типа <%s> не поддерживается вкл./выкл. элментов контрола' % ctrl.__class__.__name__)
        return None


