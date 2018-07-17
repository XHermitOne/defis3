#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль контрола выбора записи по полю из таблицы или запроса.
"""

# Подключение библиотек
import wx
# import wx.combo

from ic.log import log
from ic.components import icwidget
# from ic.utils import coderror
from ic.utils import ic_str

__version__ = (0, 0, 2, 1)

# Спецификация
SPC_IC_TABLECHOICECTRL = {'table': None,  # Паспорт таблицы/запроса источника данных
                          'code_field': '',     # Поле, которое является кодом записи
                          'label_field': '',    # Поле, которое отображается в контроле
                          'get_label': None,    # Код определения записи контрола, в случае сложного оформления записи
                          'get_filter': None,   # Код дополнительной фильтрации данных таблицы/запроса
                          'can_empty': True,    # Возможно выбирать пустое значение?

                          'on_change': None,  # Обработчик изменения выбранного кода

                          '__parent__': icwidget.SPC_IC_WIDGET,
                          }


class icTableChoiceCtrlProto(wx.ComboBox):
    """
    Класс компонента выбора записи по полю из таблицы или запроса.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        # Сделать только для чтения
        style = wx.CB_READONLY
        if 'style' in kwargs:
            style = kwargs['style'] | wx.CB_READONLY
        kwargs['style'] = style

        wx.ComboBox.__init__(self, *args, **kwargs)

        # Объект источника данных
        self._src_data = None

        # Табличные данные
        self._table_data = None

        # Выбранный код. Определяется по кодовому полю
        self._selected_code = None

        # Привязка обработчика событий производиться в потомке
        # self.Bind(wx.EVT_COMBOBOX, self.onComboBox)

    def getCode(self):
        """
        Выбранный код. Определяется по подовому полю.
        """
        return self._selected_code

    def setCode(self, code):
        """
        Выбранный код. Определяется по подовому полю.
        """
        if code is None:
            # Да пустое значение тоже можно
            # устанавливать в контроле
            self._selected_code = None
            self.SetValue(u'')
            return True

        if self._src_data is not None:
            record = self._src_data.find_record(normal_data=self.getTableData(),
                                                field_name=self.getCodeField(),
                                                value=code)
            if record:
                self._selected_code = code
                label = record.get(self.getLabelField(), u'')
                self.SetValue(label)
                return True
        else:
            log.warning(u'Не определен табличный источник данных в контроле icTableChoiceCtrl <%s>' % self.name)
        return False

    # !!! Эти функции должны обязательно присутствовать
    # во всех контролах для унификации установки/чтения значения контрола !!!
    getValue = getCode
    setValue = setCode

    def setTableSrcData(self, tab_src_data):
        """
        Установить табличный источник данных.
        @param tab_src_data: Объект табличного источника данных.
        @return: True/False.
        """
        self._src_data = tab_src_data
        tab_data = self.refreshTableData(self._src_data)
        self.set_choices(tab_data, is_empty=self.getCanEmpty())
        return tab_data is not None

    def refreshTableData(self, tab_src_data=None):
        """
        Обновить табличные данные.
        @param tab_src_data: Объект табличного источника данных.
        @return: Обновленные табличные данные.
        """
        if tab_src_data is None:
            tab_src_data = self._src_data
        if tab_src_data is not None:
            self._table_data = tab_src_data.get_normalized()
            self._table_data = self.setFilter(self._table_data)
            return self._table_data
        else:
            log.warning(u'Не определен табличный объект источника данных в компоненте <%s>' % self.name)
        return None

    def setFilter(self, table_data=None):
        """
        Дополнительно отфильтровать записи табличных даных.
        @param table_data: Табличные данные.
        @return: Отфильтрованные табличные данные.
        """
        try:
            table_data = self._setFilter(table_data)
        except:
            log.fatal(u'Ошибка фильтрации данных')
        return table_data

    def _setFilter(self, table_data=None):
        """
        Дополнительно отфильтровать записи табличных даных.
        @param table_data: Табличные данные.
        @return: Отфильтрованные табличные данные.
        """
        if table_data is None:
            table_data = self.getTableData()

        if table_data and self.isFilterFunc():
            # Преобразовать в список словарей
            recordset = self._src_data.get_recordset_dict(table_data)
            # Отфильтровать
            recordset = self.getFilterFunc(RECORDSET=recordset,
                                           RECORDS=recordset)
            # И преобразовать в обратную форму
            table_data = self._src_data.set_recordset_dict(table_data,
                                                           recordset=recordset)
        return table_data

    def getFilterFunc(self, *arg, **kwarg):
        """
        Получить функцию дополнительной фильтрации элементов списка.
        """
        log.warning(u'Не переопределенный метод getFilterFunc')
        return list()

    def getTableData(self):
        """
        Получить табличные данные.
        """
        return self._table_data

    def getLabelField(self):
        """
        Поле надписи элемента списка.
        """
        log.warning(u'Не переопределенный метод getLabelField')
        return u''

    def getCodeField(self):
        """
        Поле кода элемента списка.
        """
        log.warning(u'Не переопределенный метод getCodeField')
        return u''

    def isLabelFunc(self):
        """
        Определена функция получения надписи элемента списка?
        @return: True/False.
        """
        return False

    def isFilterFunc(self):
        """
        Определена функция дополнительной фильтрации табличных данных?
        @return: True/False.
        """
        return False

    def getLabelFunc(self, *arg, **kwarg):
        """
        Получить функцию определения надписи элемента списка.
        """
        log.warning(u'Не переопределенный метод getLabelFunc')
        return None

    def get_label(self, record, table_data=None):
        """
        Функция полчения надписи элемента
        @param record: Текущая обрабатываемая запись.
        @param table_data: Табличные данные.
        @return: Текст элемента выбора.
        """
        if table_data is None:
            table_data = self.getTableData()

        label = u''
        label_field_name = self.getLabelField()
        if label_field_name:
            # Определено имя поля надписи в явном виде
            field_names = [field[0] for field in table_data.get('__fields__', [])]
            field_idx = field_names.index(label_field_name)
            label = ic_str.toUnicode(record[field_idx])
        else:
            # Если не определено имя поля,
            # то должна быть определена функция определения надписи элемента
            is_label_func = self.isLabelFunc()
            if is_label_func:
                rec_dict = self._src_data.get_record_dict(normal_data=table_data,
                                                          record=record)
                label = self.getLabelFunc(RECORD=rec_dict)
                if label is None:
                    label = u''
                else:
                    label = ic_str.toUnicode(label)
            else:
                log.warning(u'Не определен метод получения надписи элемента списка выбора в компоненте <%s>' % self.name)
        return label

    def set_choices(self, table_data=None, is_empty=True):
        """
        Установка списка выбора.
        @param table_data: Табличные данные.
        @param is_empty: Присутствует в списке пустая строка?
        @return: True/False.
        """
        if table_data is None:
            table_data = self.getTableData()

        if table_data is not None:
            # Сначала удалим все элементы
            self.Clear()

            # Затем заполним
            try:
                if is_empty:
                    self.Append(u'')

                for record in table_data.get('__data__', []):
                    label = self.get_label(record, table_data)
                    self.Append(label)

                self.SetSelection(0)
                return True
            except:
                log.fatal(u'Ошибка заполнения списка выбора данными')
        else:
            log.warning(u'Не определены табличные данные в компоненте <%s>' % self.name)
        return False

    def get_selected_record(self, table_data=None, selected_idx=-1):
        """
        Получить выбранную запись по индексу выбранного элемента.
        @param table_data: Табличные данные.
        @param selected_idx: Индекс выбранного элемента.
        @return: Словарь выбранной записи или None в случае ошибки.
        """
        if selected_idx < 0:
            # Ничего не выбранно
            return None

        if table_data is None:
            table_data = self.getTableData()

        if table_data is not None:
            records = table_data.get('__data__', [])
            len_records = len(records)
            if 0 <= selected_idx < len_records:
                try:
                    field_names = [field[0] for field in table_data.get('__fields__', [])]
                    record = dict([(field_names[i], val) for i, val in enumerate(records[selected_idx])])
                    return record
                except:
                    log.fatal(u'Ошибка получения выбранной записи')
            else:
                log.warning(u'Не корректный индекс <%d>. Количество записей <%d>' % (selected_idx, len_records))
        else:
            log.warning(u'Не определены табличные данные в компоненте <%s>' % self.name)
        return None

    def onComboBox(self, event):
        """
        Обработчик выбора элемента.
        """
        selected_idx = self.GetSelection() - int(self.getCanEmpty())
        selected_rec = self.get_selected_record(selected_idx=selected_idx)
        if selected_rec is not None:
            self._selected_code = selected_rec.get(self.getCodeField(), None)
        else:
            self._selected_code = None
        if event:
            event.Skip()

    def getCanEmpty(self):
        """
        Возможно выбирать пустое значение?
        """
        log.warning(u'Не переопределенный метод getCanEmpty')
        return True
