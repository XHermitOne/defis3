#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Контрол выбора фильтров.
"""

import copy
import os
import os.path
import uuid
import operator
import wx
import wx.combo

from ic.dlg import ic_dlg
from ic.kernel import io_prnt
from ic.utils import ic_res

from . import filter_choice_dlg
from . import filter_constructor_dlg

__version__ = (0, 0, 2, 2)

DEFAULT_LIMIT_LABEL_FMT = u'Ограничение количества объектов: %d'
ERROR_LIMIT_LABEL_FMT = u'(!) Превышено ограничение: %d'


class icFilterChoiceDlg(filter_choice_dlg.icFilterChoiceDlgProto):
    """
    Диалог выбора фильтров.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        filter_choice_dlg.icFilterChoiceDlgProto.__init__(self, *args, **kwargs)

        # Структура фильтров
        self._filters = []

        self.environment = None

    def setEnvironment(self, env=None):
        """
        Установить окружение для работы редактора.
        @param env: Окружение, словарно-списковая структура формата
        filter_builder_env.FILTER_ENVIRONMENT.
        """
        self.environment = env

    def _genUUID(self):
        """
        Генерация UUID.
        @return: UUID.
        """
        return str(uuid.uuid4())

    def addFilter(self, new_filter=None):
        """
        Добавить новый фильтр.
        @param new_filter: Структура фильтра.
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
            self.filterCheckList.Append(new_filter['description'], new_filter['id'])

    def delFilter(self, filter_name=None):
        """
        Удалить фильтр.
        @param filter_name: Имя фильтра.
        @return: True/False.
        """
        if filter_name is None:
            # Если имя не определено удалить выбранный фильтр
            i = self.filterCheckList.GetSelection()
            if i >= 0:
                do_del = ic_dlg.icAskBox(u'Удаление', u'Удалить фильтр?')
                if do_del:
                    del self._filters[i]
                    self.filterCheckList.Delete(i)
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
            self.filterCheckList.Delete(i+1)
            return True

    def getFilter(self):
        """
        Результирующий фильтр.
        ВНИМАНИЕ! У всех фильтров корневым элементом д.б. группа.
        """
        filters_list = list()
        checks = [self.filterCheckList.IsChecked(i) for i in range(self.filterCheckList.GetCount())]
        for i, check in enumerate(checks):
            self._filters[i]['check'] = check
            filters_list.append(self._filters[i])

        # ВНИМАНИЕ! У всех фильтров корневым элементом д.б. группа.
        group_dict = dict()
        group_dict['name'] = 'grp'
        group_dict['type'] = 'group'
        group_dict['logic'] = 'AND' if self.logicRadioBox.GetSelection() else 'OR'
        group_dict['description'] = u'И' if self.logicRadioBox.GetSelection() else u'ИЛИ'
        group_dict['children'] = filters_list
        return group_dict

    def clearFilters(self):
        """
        Очистить фильтры контрола.
        @return: True/False
        """
        self._filters = []
        self.filterCheckList.Clear()

    def setFilters(self, filter_data=None):
        """
        Установить фильтр контрола.
        @param filter_data: Данные фильтра.
            Если None, то просто устанавливается список фильтров
            без установки логической связки.
        @return: True/False.
        """
        if filter_data is not None:
            # Сначала очистить
            self.clearFilters()

            # Выбор условия соединения фильтров
            and_or = filter_data.get('logic', 'OR')
            if and_or == 'OR':
                self.logicRadioBox.SetSelection(0)
            else:
                self.logicRadioBox.SetSelection(1)

            self._filters = filter_data.get('children', [])
        else:
            self.filterCheckList.Clear()

        # Просто установить список фильтров
        for filter_dict in self._filters:
            name = filter_dict.get('description', filter_dict.get('uuid', self._genUUID()))
            item = self.filterCheckList.Append(name, name)
            # Сразу пометить если пункты помечены в фильтре
            self.filterCheckList.Check(item, filter_dict.get('check', False))
        return True

    def refreshFilters(self):
        """
        Обновление контрола фильтров.
        @return: True/False.
        """
        return self.setFilters()

    def sortFilters(self, is_reverse=False):
        """
        Отсортировать список фильтров по наименованию.
        @param is_reverse: Обратная сортировка?
        @return: Отсортированный список фильтров.
        """
        # ВНИМАНИЕ! Здесь используется operator.itemgetter
        # для определения порядка группировки сортировки
        # operator.itemgetter('a', 'b', 'c') аналог
        # lambda rec: (rec['a'], rec['b'], rec['c'])
        # но выполняется быстрее
        self._filters = sorted(self._filters,
                               key=operator.itemgetter('description'))
        if is_reverse:
            self._filters.reverse()

        self.refreshFilters()
        return self._filters

    def moveFilterUp(self, filter_idx=None):
        """
        Передвинуть фильтр с индексом filter_idx вверх по списку.
        @param filter_idx: Индекс фильтра. Если None,
            то берется текущий выбранный.
        @return: True/False.
        """
        if filter_idx is None:
            filter_idx = self.filterCheckList.GetSelection()
        num_filters = len(self._filters)
        if (filter_idx < 0) or (filter_idx >= num_filters):
            io_prnt.outWarning(u'Не корректный индекс <%s>' % filter_idx)
            return False
        elif filter_idx == 0:
            io_prnt.outWarning(u'Не возможно передвинуть фильтр выше')
            return False
        # Меняем фильтры местами
        selected_filter = self._filters[filter_idx]
        self._filters[filter_idx] = self._filters[filter_idx - 1]
        self._filters[filter_idx - 1] = selected_filter

        self.refreshFilters()
        # Выделить
        self.filterCheckList.SetSelection(filter_idx - 1)
        return True

    def moveFilterDown(self, filter_idx=None):
        """
        Передвинуть фильтр с индексом filter_idx вниз по списку.
        @param filter_idx: Индекс фильтра. Если None,
            то берется текущий выбранный.
        @return: True/False.
        """
        if filter_idx is None:
            filter_idx = self.filterCheckList.GetSelection()
        num_filters = len(self._filters)
        if (filter_idx < 0) or (filter_idx >= num_filters):
            io_prnt.outWarning(u'Не корректный индекс <%s>' % filter_idx)
            return False
        elif filter_idx == num_filters-1:
            io_prnt.outWarning(u'Не возможно передвинуть фильтр ниже')
            return False
        # Меняем фильтры местами
        selected_filter = self._filters[filter_idx]
        self._filters[filter_idx] = self._filters[filter_idx + 1]
        self._filters[filter_idx + 1] = selected_filter

        self.refreshFilters()
        # Выделить
        self.filterCheckList.SetSelection(filter_idx + 1)
        return True

    def setLimitLabel(self, limit=None, over_limit=None):
        """
        Вывести сообщение об ограничении количества записей.
        @param limit: Ограничение количества записей.
        @param over_limit: Количество записей при привышении ограничения.
        """
        if over_limit:
            try:
                label = ERROR_LIMIT_LABEL_FMT % int(over_limit)
                self.limit_staticText.SetLabel(label)
                self.limit_staticText.SetForegroundColour(wx.RED)
                return
            except:
                io_prnt.outLastErr(u'Ошибка в setLimitLabel')
        if limit:
            # Есть ограничение, но не превышено
            try:
                label = DEFAULT_LIMIT_LABEL_FMT % int(limit)
                self.limit_staticText.SetLabel(label)
                fg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)
                self.limit_staticText.SetForegroundColour(fg)
                return
            except:
                io_prnt.outLastErr(u'Ошибка в setLimitLabel')
        # Нет ограничений
        self.limit_staticText.SetLabel(u'')

    def onAddButtonClick(self, event):
        self.GetParent().addFilter()
        event.Skip()

    def onDelButtonClick(self, event):
        self.GetParent().delFilter()
        event.Skip()

    def onCancelButtonClick(self, event):
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onSortToolClick(self, event):
        self.GetParent().sortFilters()
        event.Skip()

    def onSortReverseToolClick(self, event):
        self.GetParent().sortFilters(is_reverse=True)
        event.Skip()

    def onMoveUpToolClick(self, event):
        self.GetParent().moveFilterUp()
        event.Skip()

    def onMoveDownToolClick(self, event):
        self.GetParent().moveFilterDown()
        event.Skip()


class icFilterChoiceCtrlProto(wx.combo.ComboCtrl):
    """
    Контрол выбора фильтров.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        # ВНИМАНИЕ! Элементы этого контрола можно только выбирать
        # Редактирование подразумевается только при вызове соответствующих функций
        kwargs['style'] = wx.CB_READONLY | wx.CB_DROPDOWN | kwargs.get('style', 0)

        wx.combo.ComboCtrl.__init__(self, *args, **kwargs)

        self._uuid = None

        self._init_button()

        # Результирующий отредактированный фильтр
        self._filter = dict()

        # Имя файла хранения фильтров.
        self._filter_filename = None

        # Окружение фильтра
        self._environment = None

        # Диалоговое окно выбора фильтров
        self._dlg = None

        # Ограничение количества строк фильтруемого объекта.
        self._limit = None
        # Количество строк при привышении лимита
        self._over_limit = None

    def setEnvironment(self, env=None):
        """
        Установить окружение для работы редактора.
        @param env: Окружение, словарно-списковая структура формата
        filter_builder_env.FILTER_ENVIRONMENT.
        """
        self._environment = env

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

    def _init_button(self):
        """
        Инициализация кнопки выбора.
        """
        # make a custom bitmap showing "..."
        bw, bh = 14, 16
        bmp = wx.EmptyBitmap(bw, bh)
        dc = wx.MemoryDC(bmp)

        # clear to a specific background colour
        bgcolor = wx.Colour(255, 255, 255)
        dc.SetBackground(wx.Brush(bgcolor))
        dc.Clear()

        # draw the label onto the bitmap
        label = '...'
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        tw, th = dc.GetTextExtent(label)
        dc.DrawText(label, (bw-tw)/2, (bw-tw)/2)
        del dc

        # now apply a mask using the bgcolor
        bmp.SetMaskColour(bgcolor)

        # and tell the ComboCtrl to use it
        self.SetButtonBitmaps(bmp, True)

    def getFilter(self):
        """
        Результирующий фильтр.
        """
        return self._filter

    def getStructFilter(self):
        """
        Получить структуру результирующего фильтра без <не отмеченных>.
        @return: Структуру фильтра или None в случае ошибки.
        """
        if self._filter:
            struct_filter = copy.deepcopy(self._filter)
            struct_filter['children'] = [fltr for fltr in struct_filter['children'] if fltr['check']]
            return struct_filter
        return None

    def getLimit(self):
        """
        Ограничение количества строк фильтруемого объекта.
        """
        if self._limit < 0:
            self._limit = 0
        return self._limit

    def validLimit(self, obj_count):
        """
        Проверка преодоления ограничения.
        Функция автоматически сигнализирует о перодолении ограничения.
        @param obj_count: Реальное количество объектов.
        @return: True - ограничение не преодолено / False -превышено ограничение.
        """
        valid = obj_count <= self._limit
        if not valid:
            self._over_limit = obj_count
            self.SetBackgroundColour(wx.RED)
        else:
            self._over_limit = None
            self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        return valid

    def doDlgChoiceFilter(self):
        """
        Вызов диалогового окна выбора фильтра.
        @return: True - нажата в итоге <OK>, False - <Отмена>.
        """
        result = False
        self._dlg = icFilterChoiceDlg(self)
        self._dlg.setEnvironment(self._environment)
        self._dlg.setFilters(self._filter)
        self._dlg.setLimitLabel(self._limit, self._over_limit)
        if self._dlg.ShowModal() == wx.ID_OK:
            self._filter = self._dlg.getFilter()
            self.saveFilter()
            str_filter = self.getStrFilter()
            self.SetValue(str_filter)
            result = True
        self._dlg.Destroy()
        self._dlg = None
        return result

    def OnButtonClick(self):
        """
        Overridden from ComboCtrl, called when the combo button is clicked.
        """
        self.doDlgChoiceFilter()
        self.SetFocus()

    def getStrFilter(self):
        """
        Фильтр в строковом представлении.
        @return: Строка фильтра.
        """
        if self._filter:
            join_str = u' %s ' % self._filter.get('description', u'ИЛИ')
            return join_str.join([u'<%s>' % fltr.get('description', fltr.get('name', '...')) for fltr in self._filter['children'] if fltr.get('check', False)])
        return u''

    def DoSetPopupControl(self, popup):
        """
        Overridden from ComboCtrl to avoid assert since there is no ComboPopup.
        """
        pass

    def getFilterFileName(self):
        """
        Имя файла хранения фильтра.
        """
        return self._filter_filename

    def setFilterFileName(self, filename):
        """
        Имя файла хранения фильтра.
        """
        io_prnt.outLog(u'icFilterChoiceCtrl [%s]. Установка файла <%s> для хранения фильтра' % (self.getUUID(), filename))
        self._filter_filename = filename

    def saveFilter(self, filter_filename=None):
        """
        Сохранить фильтр.
        @param filter_filename: Имя файла хранения фильтра.
            Если не определен, то генерируется по UUID.
        @return: True/False.
        """
        if filter_filename:
            filter_filename = os.path.normpath(filter_filename)
        else:
            filter_filename = self._filter_filename

        if filter_filename:
            if os.path.exists(filter_filename):
                # Сначала прочитать файл
                res = ic_res.LoadResource(filter_filename)
                if res:
                    # Затем расширить своими фильтрами и записать
                    res[self.getUUID()] = self._filter
                    ic_res.SaveResourcePickle(filter_filename, res)
                else:
                    io_prnt.outWarning(u'Error resource file <%s>' % filter_filename)
                    return False
            else:
                # Просто записать в файл
                res = {self.getUUID(): self._filter}
                ic_res.SaveResourcePickle(filter_filename, res)
        else:
            io_prnt.outWarning(u'Not define save filter file')
            return False
        return True

    def loadFilter(self, filter_filename=None):
        """
        Загрузить фильтр.
        @param filters_filename: Имя файла хранения фильтра.
            Если не определен, то генерируется по UUID.
        """
        if filter_filename:
            filter_filename = os.path.normpath(filter_filename)
        else:
            filter_filename = self._filter_filename

        if filter_filename and os.path.exists(filter_filename):
            res = ic_res.LoadResource(filter_filename)
            if res:
                filter_data = res.get(self.getUUID(), None)
                if filter_data:
                    self.setFilter(filter_data)
                else:
                    io_prnt.outWarning(u'Not fond filters for combo box <%s> in file <%s>!' % (self.getUUID(),
                                                                                               filter_filename))
        else:
            io_prnt.outWarning(u'Filters file <%s> not exists!' % filter_filename)

    def setFilter(self, filter_data):
        """
        Установить фильтр контрола.
        @param filter_data: Данные фильтра.
        @return: True/False.
        """
        self._filter = filter_data

    def getFilterFilename(self):
        return self._filter_filename

    def addFilter(self, *args, **kwargs):
        """
        Добавить новый фильтр.
        ВНИМАНИЕ! Эта функция присутствует в компоненте для ограничения
        прав на добавление/удаление фильтров.
        """
        if self._dlg:
            return self._dlg.addFilter(*args, **kwargs)
        return False

    def delFilter(self, *args, **kwargs):
        """
        Удалить фильтр.
        ВНИМАНИЕ! Эта функция присутствует в компоненте для ограничения
        прав на добавление/удаление фильтров.
        """
        if self._dlg:
            return self._dlg.delFilter(*args, **kwargs)
        return False

    def sortFilters(self, *args, **kwargs):
        """
        Отсортировать список фильтров по наименованию.
        """
        if self._dlg:
            return self._dlg.sortFilters(*args, **kwargs)
        return False

    def moveFilterUp(self, *args, **kwargs):
        """
        Передвинуть фильтр с индексом filter_idx вверх по списку.
        """
        if self._dlg:
            return self._dlg.moveFilterUp(*args, **kwargs)
        return False

    def moveFilterDown(self, *args, **kwargs):
        """
        Передвинуть фильтр с индексом filter_idx вниз по списку.
        """
        if self._dlg:
            return self._dlg.moveFilterDown(*args, **kwargs)
        return False


def test():
    """
    Тестирование компонента.
    """
    app = wx.PySimpleApp()

    frame = wx.Frame(None)

    boxsizer = wx.BoxSizer(wx.VERTICAL)
    combo = icFilterChoiceCtrlProto(frame)
    boxsizer.Add(combo, 0, wx.EXPAND, 5)
    button1 = wx.Button(frame, label=u'Test')
    boxsizer.Add(button1)
    frame.SetSizer(boxsizer)

    frame.Show()

    app.MainLoop()


if __name__ == '__main__':
    test()
