#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Контрол комбобокса выбора фильтров.
"""

import os
import os.path
import wx
import uuid

from ic.components import icwidget
from ic.kernel import io_prnt
from ic.utils import ic_res
from ic.dlg import ic_dlg

from . import filter_constructor_dlg


DEFAULT_ALL_LABEL = '<Все>'

# Имя типа
FILTER_COMBOBOX_TYPE = 'FilterComboBox'

# Спецификация
SPC_IC_FILTER_COMBOBOX = {'name': 'default',
                          'type': FILTER_COMBOBOX_TYPE,
                          'description': '',
                          '_uuid': None,

                          'filename': None,  # Имя файла сохранения фильтров,
                                             # если не определен, то генерируется по _uuid
                          'dirname': None,   # Имя папки сохранения фильтров,
                                             # если не определен, то берется local_dir текущего пользователя

                          '__parent__': icwidget.SPC_IC_WIDGET,
                          }


class icFilterComboBoxProto(wx.ComboBox):
    """
    Контрол комбобокса выбора фильтров.
    """

    def __init__(self, parent, env=None, *args, **kwargs):
        """
        Конструктор.
        """
        kwargs['parent'] = parent
        # ВНИМАНИЕ! Элементы этого контрола можно только выбирать
        # Редактирование подразумевается только при вызове соответствующих функций
        kwargs['style'] = wx.CB_READONLY | wx.CB_DROPDOWN | kwargs.get('style', 0)
        wx.ComboBox.__init__(self, *args, **kwargs)
        self.Append(DEFAULT_ALL_LABEL, 'all')
        self.Select(0)

        # Имя файла хранения фильтров.
        self._filter_filename = None

        # Структура фильтров
        self._filters = []

        self._uuid = None

        self.environment = None
        if env:
            # Устанивить окружение работы конструктора фильтров
            self.setEnvironment(env)

    def setEnvironment(self, env=None):
        """
        Установить окружение для работы редактора.
        @param env: Окружение, словарно-списковая структура формата
        filter_builder_env.FILTER_ENVIRONMENT.
        """
        self.environment = env

    def getUUID(self):
        if not self._uuid:
            self._uuid = self._genUUID()
        return self._uuid

    def _genUUID(self):
        """
        Генерация UUID.
        @return: UUID.
        """
        return str(uuid.uuid4())

    def clearFilters(self):
        """
        Очистить фильтры контрола.
        @return: True/False
        """
        self._filters = []
        self.Clear()
        self.Append(DEFAULT_ALL_LABEL, 'all')

    def setFilters(self, filters):
        """
        Установить фильтры контрола.
        @param filters:
        @return: True/False.
        """
        # Сначала очистить комбобокс
        self.clearFilters()
        for filter_dict in filters:
            name = filter_dict.get('description', filter_dict.get('uuid', self._genUUID()))
            self.Append(name, name)
        return True

    def saveFilters(self, filters_filename=None):
        """
        Сохранить фильтры.
        @param filters_filename: Имя файла хранения фильтров.
            Если не определен, то генерируется по UUID.
        """
        if os.path.exists(filters_filename):
            # Сначала прочитать файл
            res = ic_res.LoadResource(filters_filename)
            if res:
                # Затем расширить своими фильтрами и записать
                res[self.getUUID()] = self._filters
                ic_res.SaveResourcePickle(filters_filename, res)
            else:
                io_prnt.outWarning(u'Error resource file <%s>' % filters_filename)
        else:
            # Просто записать в файл
            res = {self.getUUID(): self._filters}
            ic_res.SaveResourcePickle(filters_filename, res)

    def loadFilters(self, filters_filename=None):
        """
        Загрузить фильтры.
        @param filters_filename: Имя файла хранения фильтров.
            Если не определен, то генерируется по UUID.
        """
        filters_filename = os.path.normpath(filters_filename)
        if os.path.exists(filters_filename):
            res = ic_res.LoadResource(filters_filename)
            if res:
                filters = res.get(self.getUUID(), None)
                if filters:
                    self.setFilters(filters)
                else:
                    io_prnt.outWarning(u'Not fond filters for combo box <%s> in file <%s>!' % (self.getUUID(), filters_filename))
        else:
            io_prnt.outWarning(u'Filters file <%s> not exists!' % filters_filename)

    def getFilterFilename(self):
        return self._filter_filename

    def selectFilter(self, filter_name):
        """
        Сделать активным фильтр в комбобокс.
        @param filter_name: Имя фильтра.
        @return: Структура выбранного фильтра, или None если фильтр не найден.
        """
        find_filter = [(i, filter_dict) for i, filter_dict in enumerate(self._filters) if filter_dict['id'] == filter_name]
        if find_filter:
            self.Select(find_filter[0][0]+1)
            return find_filter[0][1]

        return None

    def getSelectedFilter(self):
        """
        Выбранный фильтр.
        @return: Возвращает структуру выбранного фильтра или
            None, если фильтрация отключена.
        """
        i = self.GetSelection()-1
        if i < 0:
            io_prnt.outLog(u'Фильтрация отключена')
            return None
        try:
            return self._filters[i]
        except IndexError:
            io_prnt.outWarning(u'Нет фильтра с таким индексом <%d>' % i)
            return None

    def offFilter(self):
        """
        Выключить фильтрацию.
        """
        self.Select(0)

    def addFilter(self, new_filter=None, auto_select=True):
        """
        Дбавить фильтр.
        @param new_filter: Структура фильтра.
        @param auto_select: Автовыбор нового фильтра?
        @return: True/False.
        """
        if new_filter is None:
            # Необходимо сначала сконструировать фильтр
            new_filter = filter_constructor_dlg.icFilterConstructorDlg(self, None, self.environment)

            if new_filter:
                filter_id = self._genUUID()
                filter_description = ic_dlg.icTextEntryDlg(self, u'Фильтр',
                                                           u'Введите наименование фильтра')
                new_filter['id'] = filter_id
                new_filter['description'] = filter_description
            else:
                io_prnt.outWarning(u'Не определен фильтр для добавления')
                return False

        if new_filter:
            self._filters.append(new_filter)
            i = len(self._filters)
            self.Append(new_filter['description'], new_filter['id'])
            if auto_select:
                self.Select(i)

    def delFilter(self, filter_name=None):
        """
        Удалить фильтр.
        @param filter_name: Имя фильтра.
        @return: True/False.
        """
        if filter_name is None:
            # Если имя не определено удалить выбранный фильтр
            i = self.GetSelection()
            if i > 0:
                do_del = ic_dlg.icAskBox(u'Удаление', u'Удалить фильтр?')
                if do_del:
                    del self._filters[i-1]
                    self.Delete(i)
                    return True
                return False
        else:
            filters_id = [filter_dict['id'] for filter_dict in self._filters]
            try:
                i = filters_id.index(filter_name)
            except IndexError:
                io_prnt.outWarning(u'Не найден фильтр <%s> среди <%s>' % (filter_name, filters_id))
                return False
            del self._filters[i]
            self.Delete(i+1)
            self.Select(0)
            return True


def test():
    """
    Функция тестирования.
    """
    import copy

    app = wx.PySimpleApp()

    from . import filter_builder_env

    frame = wx.Frame(None)

    env = filter_builder_env.FILTER_ENVIRONMENT
    env['requisites'] = []

    requisite1 = copy.deepcopy(filter_builder_env.FILTER_REQUISITE)
    requisite1['name'] = 'Name'
    requisite1['description'] = u'Название'
    requisite1['type'] = filter_builder_env.REQUISITE_TYPE_STR
    requisite1['funcs'] = list(filter_builder_env.DEFAULT_STRING_FUNCS)
    env['requisites'].append(requisite1)

    requisite2 = copy.deepcopy(filter_builder_env.FILTER_REQUISITE)
    requisite2['name'] = 'Cost'
    requisite2['description'] = u'Цена'
    requisite1['type'] = filter_builder_env.REQUISITE_TYPE_FLOAT
    requisite2['funcs'] = list(filter_builder_env.DEFAULT_NUMBER_FUNCS)
    env['requisites'].append(requisite2)

    boxsizer = wx.BoxSizer(wx.VERTICAL)
    combo = icFilterComboBoxProto(frame, env)
    boxsizer.Add(combo)
    button1 = wx.Button(frame, label=u'Load')
    boxsizer.Add(button1)
    button2 = wx.Button(frame, label=u'Save')
    boxsizer.Add(button2)
    button3 = wx.Button(frame, label=u'Add')
    boxsizer.Add(button3)
    button4 = wx.Button(frame, label=u'Del')
    boxsizer.Add(button4)
    frame.SetSizer(boxsizer)

    def on_del(event):
        print('on del')
        combo.delFilter()
        event.Skip()

    def on_add(event):
        print('on add')
        combo.addFilter()
        event.Skip()

    def on_save(event):
        print('on save')
        combo.saveFilters()
        event.Skip()

    def on_load(event):
        print('on load')
        combo.loadFilters()
        event.Skip()

    frame.Bind(wx.EVT_BUTTON, on_add, button3)
    frame.Bind(wx.EVT_BUTTON, on_del, button4)
    frame.Bind(wx.EVT_BUTTON, on_load, button1)
    frame.Bind(wx.EVT_BUTTON, on_save, button2)

    frame.Show()

    app.MainLoop()

if __name__ == '__main__':
    test()
