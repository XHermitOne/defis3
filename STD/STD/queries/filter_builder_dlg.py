#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Редактор критериев выбора коллекций.
"""

import wx
import wx.lib.scrolledpanel

from ic.imglib import common as imglib
from ic.log import log

from .filter_builder_ctrl import *

# Version
__version__ = (0, 1, 1, 1)


def doFilterBuilder(parent, environment, default=None):
    """
    Запустить редактор критериев выборки/фильтров.
    :param parent: Родительское окно редактора.
    :param environment: Структура окружения редактора.
    :param default: Структура по умолчанию.
    :return: Возвращает результат редактирования.
    """
    try:
        dlg = icFilterBuilderDialog(parent, -1, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        dlg.setEnvironment(environment)
        dlg.setEditResult(default)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            # Нажата кнопка OK в редакторе
            return dlg.getEditResult()
        else:
            # Нажата кнопка "Отмена"
            return None
    except:
        log.fatal(u'Ошибка запуска редактора критериев выбора.')
        return None


class icFilterBuilderDialog(wx.Dialog):
    """
    Диалоговое окно редактора критериев выборки коллекций.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        # Установить заголовок
        kwargs['title'] = u'Редактор критериев выборки ver. '+'.'.join([str(num) for num in list(__version__)])
        wx.Dialog.__init__(self, *args, **kwargs)
        # Установить иконку
        img_filter = imglib.imgFilter
        if img_filter:
            icon = wx.IconFromBitmap(imglib.imgFilter)
            self.SetIcon(icon)

        # Окружение редактора
        self.environment = None
        # Результат редактирования
        self.result = []
        
        # Список контролов редактирования
        self.edit_controls = []
        
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.main_sizer)

        self.builder_panel = wx.lib.scrolledpanel.ScrolledPanel(self, -1,
                                                                size=wx.Size(700, 400))
        self.builder_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.builder_panel.SetSizer(self.builder_panel_sizer)

        self.builder_panel.SetAutoLayout(1)  # Это ...
        self.builder_panel.SetupScrolling()  # ... и это нужно для того чтобы
        # прокрутка в панели автоматически включались при добавлении
        # новых контролов на нее
        
        self.builder_panel_row_sizers = []
        self.main_sizer.Add(self.builder_panel, 1, wx.EXPAND, 5)

        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.cancel_button = wx.Button(self, wx.ID_CANCEL, u'Отмена')
        self.ok_button = wx.Button(self, wx.ID_OK, 'OK')
        self.button_sizer.Add(self.cancel_button, 0, wx.EXPAND | wx.ALIGN_RIGHT)
        self.button_sizer.Add(self.ok_button, 0, wx.EXPAND | wx.ALIGN_RIGHT,5)
        self.main_sizer.Add(self.button_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.GetSizer().Fit(self)
        self.GetSizer().SetSizeHints(self)
        self.GetSizer().Layout()
        
    def setEnvironment(self, env=None):
        """
        Установить окружение для работы редактора.
        :param env: Окружение, словарно-списковая структура формата
        filter_builder_env.FILTER_ENVIRONMENT.
        """
        self.environment = env
        self.removeAll()
        self.addFilterEdit()
        self.addRequisiteChoice()

    def getEditResult(self):
        """
        Получить результат редактирования.
        """
        return self.result

    def setEditResult(self, result):
        """
        Инициализация редактора по отредактированному значению.
        """
        self.result = result
        if self.result:
            # Создание всех внутренних контролов
            self._createEditControls(self.result, self.environment)
        
    def _createEditControls(self, result, environment):
        """
        Создание всех внутренних контролов редактирования.
        """
        # Сначала удалить все контролы
        self.removeAll()
        
        logics = self._logicTranslate.keys()
        requisite = None  # Структура описания реквизита
        func = None       # Структура описания функции
        # Перебор по строкам редактирования
        for i_row, row in enumerate(result):
            if row:
                self.addFilterEdit()
                # Перебор по элементам строки редактирования
                for i, element in enumerate(row):
                    if i == 0:
                        # Поле выбора реквизита
                        self.addRequisiteChoice()
                        requisite = element
                        # Установить значение
                        if hasattr(self.edit_controls[i_row][i], 'SetValue'):
                            self.edit_controls[i_row][i].SetValue(element['description'])
                    elif i == 1:
                        # Поле выбора функции
                        self.addFuncChoice(i_row)
                        func = element
                        # Установить значение
                        if hasattr(self.edit_controls[i_row][i], 'SetValue'):
                            self.edit_controls[i_row][i].SetValue(element['description'])
                    elif i > 1 and element not in logics:
                        # Поля аргументов функции
                        arg = func['args'][i-2]
                        self._addArgEdit(i_row, arg)
                    elif i > 1 and element in logics:
                        # Логическая связь строк
                        self._addLogicChoice(i_row)
                        if hasattr(self.edit_controls[i_row][i], 'SetValue'):
                            self.edit_controls[i_row][i].SetValue(self.logicTranslate[element])
        
    def removeAll(self):
        """
        Удалить все строки редактирования.
        """
        for i in range(self.getFilterEditCount()):
            self.delFilterEdit()        
        self.edit_controls = []
        
    def _getRequisiteChoiceFromEnv(self):
        """
        Получить список выбора реквизитов из окружения.
        """
        if self.environment:
            return [requisite['description'] for requisite in self.environment['requisites']]
        return []
    
    def _getRequisites(self):
        """
        Реквизиты из окружения.
        """
        if self.environment:
            return self.environment['requisites']
        return []
    
    def _setRequisiteFilterCtrl(self, control, description):
        """
        Установить у контрола редактирования структуру управления по русскому описанию.
        """
        # Найти стурктуру управления в окружении
        for requisite in self.environment['requisites']:
            if requisite['description'] == description:
                control.filter_ctrl = requisite
                return requisite
        return None
        
    def onDelEditRow(self, event):
        """
        Удалить строку редактирования.
        """
        control = event.GetEventObject()
        idx = self._getControlRowIndex(control)
        result = self.delFilterEdit(idx)
        if result:
            # Если удалили строку, то удалить и строку результата
            if idx < len(self.result):
                del self.result[idx]

        # ВНИМАНИЕ!!! Здесь event.Skip() не нужен,
        # т.к. была удалена кнопка по которой вызывался это обработчик!
        # event.Skip()
        
    def addRequisiteChoice(self):
        """
        Добавить в редактор контрол выбора реквизита.
        """
        del_row_button = wx.Button(self.builder_panel, -1, label='-', size=wx.Size(24, 24))
        del_row_button.Bind(wx.EVT_BUTTON, self.onDelEditRow)
        self.builder_panel_row_sizers[-1].Add(del_row_button, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        self.edit_controls[-1].append(del_row_button)
        
        new_choice = icCustomChoice(self.builder_panel, -1, size=wx.Size(200, -1))
        new_choice.setData(self._getRequisites())
        new_choice.Bind(wx.EVT_TEXT, self.OnRequisiteChoice)
        self.builder_panel_row_sizers[-1].Add(new_choice, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        # Запомнить новый контрол в списке контролов редактирования
        self.edit_controls[-1].append(new_choice)
        # Надо после добавления контрола обязательно запустить
        # перераспределение контролов
        self.GetSizer().Layout()
        
    def delRequisiteChoice(self):
        """
        Удалить из редактора последний контрол выбора реквизита.
        """
        pass

    def _getControlRowIndex(self, control):
        """
        Получить индекс строки контрола редактирования.
        """
        for i, row_control in enumerate(self.edit_controls):
            # Не забыть проверить в дочерних объектах
            if control in row_control or \
               bool([control for control in row_control if control in control.GetChildren()]):
                return i
        return -1

    def _getEditControlByChild(self, control):
        """
        Получить контрол редактирования по дочернему контролу.
        """
        for i, row_control in enumerate(self.edit_controls):
            # Не забыть проверить в дочерних объектах
            find_parent = [control for control in row_control if control in control.GetChildren()]
            if control in row_control:
                return row_control[row_control.index(control)]
            elif bool(find_parent):
                find_control = find_parent[0]
                return find_control
        return None
    
    def _addRequisiteResult(self, requisite_idx):
        """
        Добавить в результат выбранный реквизит.
        :param requisite_idx: Индекс выбранного реквизита.
        """
        self.result.append([])
        control = self.edit_controls[-1][1]
        self.result[-1].append(self.environment['requisites'][requisite_idx])
        
    def OnRequisiteChoice(self, event):
        """
        Обработчик изменения реквизита.
        """
        control = event.GetEventObject()
        description = event.GetString()
        
        # Установить результат выбора
        edit_ctrl = self._getEditControlByChild(control)
        self._addRequisiteResult(edit_ctrl.choice_idx)
        
        # Добавить функцию в редактор
        idx = self._getControlRowIndex(control)
        self.addFuncChoice(idx)
        
        event.Skip()
    
    def _getFuncChoiceFromRequisite(self, requisite):
        """
        Получить список выбора функций из реквизита.
        """
        result = []
        for func in requisite['funcs']:
            if isinstance(func, str):
                # Это ссылка на стандартные функции
                # Стандартные функции находятся в окружении
                result.append(self.environment['funcs'][func]['description'])
            elif isinstance(func, dict):
                # Это описание нестандартной функции
                result.append(func['description'])
        return result
        
    def _getFuncChoiceFromEnv(self, idx):
        """
        Получить список выбора функций из окружения.
        :param idx: Индекс строки редактирования.
        """
        result = []
        requisite = self.result[idx][0]
        if requisite['funcs']:
            for func in requisite['funcs']:
                if isinstance(func, dict):
                    result.append(func['description'])
                elif isinstance(func, str):
                    if self.environment:
                        func = self.environment['funcs'][func]
                        result.append(func['description'])
                else:
                    log.warning(u'Ошибка. Не корректный тип функции: <%s<' % func)
        return result
    
    def _getFunctions(self, idx):
        """
        Получить список выбора функций из окружения для указанной строки редактирования.
        :param idx: Индекс строки редактирования.
        """
        result = []
        requisite = self.result[idx][0]
        if requisite['funcs']:
            for func in requisite['funcs']:
                if isinstance(func, dict):
                    result.append(func)
                elif isinstance(func, str):
                    if self.environment:
                        func = self.environment['funcs'][func]
                        result.append(func)
                else:
                    log.warning(u'Ошибка. Не корректный тип функции: <%s>' % func)
        return result
    
    def delFuncChoice(self, idx):
        """
        Удалить из редактора контрол выбора функции.
        :param idx: Индекс строки редактирования.
        """
        # Убрать контролы из сайзеров
        for control in self.edit_controls[idx][2:]:
            self.builder_panel_row_sizers[idx].Remove(control)
            # Да и ваще удалить контрол
            control.Destroy()
        # Убрать контролы из списка редактирумых контролов
        self.edit_controls[idx] = self.edit_controls[idx][:2]
        # Очистить результат в последнюю очередь
        self.result[idx] = self.result[idx][:1]
        
    def addFuncChoice(self, idx):
        """
        Добавить в редактор контрол выбора функции.
        :param idx: Индекс строки редактирования.
        """
        # Перед добавлением удалить все ненужное
        self.delFuncChoice(idx)
        
        new_choice = icCustomChoice(self.builder_panel, -1, size=wx.Size(200, -1))
        new_choice.setData(self._getFunctions(idx))
        new_choice.Bind(wx.EVT_TEXT, self.onFuncChoice)
        self.builder_panel_row_sizers[idx].Add(new_choice, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        # Запомнить новый контрол в списке контролов редактирования
        self.edit_controls[idx].append(new_choice)
        # Надо после добавления контрола обязательно запустить
        # перераспределение контролов
        self.GetSizer().Layout()
    
    def _addFuncResult(self, function_idx, idx=-1):
        """
        Добавить в результат выбранную функцию.
        """
        control = self.edit_controls[idx][2]
        self.result[idx].append(control.data[function_idx])
        
    def onFuncChoice(self, event):
        """
        Обработчик изменения функции.
        """
        control = event.GetEventObject()
        description = event.GetString()
        
        # Установить результат выбора
        edit_ctrl = self._getEditControlByChild(control)
        idx = self._getControlRowIndex(control)
        self._addFuncResult(edit_ctrl.choice_idx, idx)
        
        # Добавить аргументы функции в редактор
        self.addArgsEdit(idx)
        
        event.Skip()
        
    def _getArgsFromEnv(self, idx):
        """
        Получить список аргументов из окружения для указанной строки редактирования.
        """
        func = self.result[idx][1]
        return func['args']
        
    def _addArgEdit(self, idx, arg):
        """
        Добавить в редактор контрол редактирования аргумента функции.
        :param idx: Индекс строки редактирования.
        :param arg: Структура описания аргумента. Формат filter_builder_env.FILTER_ARG.
        """
        # Добавить подпись
        new_arg_label = wx.StaticText(self.builder_panel, -1, label=arg['description'] + u':')
        self.builder_panel_row_sizers[idx].Add(new_arg_label, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        self.edit_controls[idx].append(new_arg_label)
        
        # Добавить редактор
        if 'ext_edit' in arg and arg['ext_edit']:
            # Для аргумента определен расширенный редактор
            new_arg_edit = icArgExtededEdit(self.builder_panel, -1)
            if 'default' in arg:
                new_arg_edit.default = arg['default']
        else:
            # Обычный текстовый редактор
            new_arg_edit = wx.TextCtrl(self.builder_panel, -1)
            if 'default' in arg:
                new_arg_edit.SetValue(str(arg['default']))
        # Привязать обработчик изменения редактируемого текста
        new_arg_edit.Bind(wx.EVT_TEXT, self.onArgChange)
        self.builder_panel_row_sizers[idx].Add(new_arg_edit, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        self.edit_controls[idx].append(new_arg_edit)
        
    def addArgsEdit(self, idx):
        """
        Добавить в редактор контролы редактирования аргументов функции.
        :param idx: Индекс строки редактирования.
        """
        args = self._getArgsFromEnv(idx)
        for arg in args:
            # Добавить контролы редактирования аргумента функции
            self._addArgEdit(idx, arg)

        # Добавить выпадающий список логической связки строк
        self._addLogicChoice(idx)
        
        # Надо после добавления контрола обязательно запустить
        # перераспределение контролов
        self.GetSizer().Layout()
        
    # Словарь преобразований логических связок надписей
    _logicTranslate = {'': '', u'И': 'AND', u'ИЛИ': 'OR', u'НЕ': 'NOT'}
    
    def _addLogicChoice(self, idx):
        """
        Добавить выпадающий список логической связки строк - AND/OR/NOT.
        :param idx: Индекс строки редактирования.
        """
        new_logic_choice = wx.Choice(self.builder_panel, -1,
                                     choices=self._logicTranslate.keys())
        new_logic_choice.Bind(wx.EVT_CHOICE, self.onLogicChoice)
        self.builder_panel_row_sizers[idx].Add(new_logic_choice, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.edit_controls[idx].append(new_logic_choice)

    def _addLogicResult(self, logic, idx):
        """
        Добавить в результат логическую связку.
        :param logic: AND/OR/NOT.
        :param idx: Индекс строки редактирования.
        """
        if self.result[idx][-1] not in self._logicTranslate.values():
            self.result[idx].append(logic)
        else:
            self.result[idx][-1] = logic
        
    def onArgChange(self, event):
        """
        Обработчик изменения значения аргумента функции.
        """
        # Сначала проверить что-либо введено?
        arg_str = event.GetString()
        if arg_str:
            # По контролу редактирования определить строку редактирования
            control = event.GetEventObject()
            idx = self._getControlRowIndex(control)
            # Вычислить индекс аргумента по индексу контрола редактирвоания
            arg_idx = int((self.edit_controls[idx].index(control)-3)/2)
            # Изменить результат аргумента
            self._addArgResult(arg_str, arg_idx, idx)
                        
        event.Skip()
        
    def _getArgResult(self, arg_idx, idx):
        """
        Получить аргумент из результат по индексу.
        :param arg_idx: Индекс аргумента.
        :param idx: Индекс строки редактирования.
        """
        cur_arg_idx = 2 + arg_idx
        if cur_arg_idx < len(self.result[idx]):
            arg_str = self.result[idx][cur_arg_idx]
            if arg_str not in self._logicTranslate.keys():
                return arg_str
                
        # Аргумент с таким индексом не добавлен в строку
        return None        
        
    def _addArgResult(self, str_arg, arg_idx, idx):
        """
        Добавить в результат значение аргумента функции.
        :param str_arg: Строка аргумента.
        :param arg_idx: Индекс аргумента.
        :param idx: Индекс строки редактирования.
        """
        cur_arg_idx = 2 + arg_idx
        # Сначала выяснить добавлен ли аргумент в результат уже
        arg_str_result = self._getArgResult(arg_idx, idx)
        if arg_str_result is None:
            # Аргумент уже присутствует
            # надо просто поменять его значение
            self.result[idx][cur_arg_idx] = str_arg
        else:
            # Аргумента с таким индексом нет
            # нодо его добавить
            self.result[idx].insert(cur_arg_idx, str_arg)
        
    def onLogicChoice(self, event):
        """
        Обработчик выбор логического оператора.
        """
        select_str = event.GetString()
        if select_str:
            logic = self._logicTranslate[select_str]

            # Сохранить логическую связь в результате
            control = event.GetEventObject()
            idx = self._getControlRowIndex(control)
            self._addLogicResult(logic, idx)
                        
            # Если строка последняя то...
            if idx >= len(self.result)-1:
                # ...Добавить нужные контролы
                self.addFilterEdit()
                self.addRequisiteChoice()
        event.Skip()
        
    def addFilterEdit(self):
        """
        Добавить новую строку редактирования.
        """
        self.builder_panel_row_sizers.append(wx.BoxSizer(wx.HORIZONTAL))
        self.builder_panel_sizer.Add(self.builder_panel_row_sizers[-1], 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.edit_controls.append([])

    def delFilterEdit(self, idx=-1):
        """
        Удалить строку фильтрации.
        :param idx: Индекс удаляемой строки редактирования.
        :return: True-строка удалена,False-строка не удалена.
        """
        # Если удаляемая строка не последняя
        # Последнюю строку удалить нельзя
        if idx < len(self.edit_controls)-1:
            
            # Очистить сайзер
            self.builder_panel_row_sizers[idx].Clear()
            
            # Убрать контролы
            for control in self.edit_controls[idx]:
                # Да и ваще удалить контрол
                control.Destroy()
            
            # Убрать контролы из списка редактирумых контролов
            del self.edit_controls[idx]
            # И удалить сайзер
            del_sizer = self.builder_panel_row_sizers[idx]
            del self.builder_panel_row_sizers[idx]
            self.builder_panel_sizer.Detach(del_sizer)
            
            # Надо после удаления контрола обязательно запустить
            # перереразмещение контролов
            self.GetSizer().Layout()
            return True
        return False
        
    def getFilterEditCount(self):
        """
        Количество строк фильтрации.
        """
        return len(self.builder_panel_row_sizers)


def test():
    """
    Функция тестирования.
    """
    app = wx.PySimpleApp()

    # Формирование окружения
    import copy
    from . import filter_builder_env
    from ic.log import log
    import ic.config

    log.init(ic.config)

    env = copy.deepcopy(filter_builder_env.FILTER_ENVIRONMENT)
    # env = filter_builder_env.FILTER_ENVIRONMENT
    func1 = {'function': filter_builder_env.str_equal,
             'description': u'Строковое сравнение',
             'args': []
             }
    env['funcs']['str_equal'] = func1
    
    arg = copy.deepcopy(filter_builder_env.FILTER_ARG)
    arg['description'] = u'Первый'
    env['funcs']['str_equal']['args'].append(arg)
    arg = copy.deepcopy(filter_builder_env.FILTER_ARG)
    arg['description'] = u'Второй'
    env['funcs']['str_equal']['args'].append(arg)
    
    requisite1 = copy.deepcopy(filter_builder_env.FILTER_REQUISITE)
    requisite1['name'] = 'Name'
    requisite1['description'] = u'Наименование'
    func_names = env['funcs'].keys()
    func_names.sort()
    requisite1['funcs'] = func_names
    requisite1['funcs'].append({'function': None, 'description': u'Просто для отладки'})
    env['requisites'].append(requisite1)
    
    requisite2 = copy.deepcopy(filter_builder_env.FILTER_REQUISITE)
    requisite2['name'] = 'Cost'
    requisite2['description'] = u'Цена'
    env['requisites'].append(requisite2)
        
    default = []
    default.append([])
    default[-1].append(requisite1)
    default[-1].append(func1)
    default[-1].append('test')
    default[-1].append(u'Тест')    
    
    result = doFilterBuilder(None, env, default)
    app.MainLoop()
    print('TEST RESULT>>>', result)


if __name__ == '__main__':
    test()
