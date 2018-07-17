#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Редактор критериев выбора коллекций.
"""

# Version
__version__ = (0, 0, 0, 1)

# Imports
import wx
import wx.lib.scrolledpanel

from ic.kernel import io_prnt
from ic.imglib import common as imglib

from .filter_builder_ctrl import *


def doFilterBuilder(Parent_, Environment_, Default_=None):
    """
    Запустить редактор критериев выборки/фильтров.
    @param Parent_: Родительское окно редактора.
    @param Environment_: Структура окружения редактора.
    @param Default_: Структура по умолчанию.
    @return: Возвращает результат редактирования.    
    """
    try:
        dlg = icFilterBuilderDialog(Parent_, -1, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        dlg.setEnvironment(Environment_)
        dlg.setEditResult(Default_)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            # Нажата кнопка OK в редакторе
            return dlg.getEditResult()
        else:
            # Нажата кнопка "Отмена"
            return None
    except:
        io_prnt.outLastErr(u'Ошибка запуска редактора критериев выбора.')
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
        
    def setEnvironment(self, Env_=None):
        """
        Установить окружение для работы редактора.
        @param Env_: Окружение, словарно-списковая структура формата
        filter_builder_env.FILTER_ENVIRONMENT.
        """
        self.environment = Env_
        self.removeAll()
        self.addFilterEdit()
        self.addRequisiteChoice()

    def getEditResult(self):
        """
        Получить результат редактирования.
        """
        return self.result

    def setEditResult(self, Result_):
        """
        Инициализация редактора по отредактированному значению.
        """
        self.result = Result_
        if self.result:
            # Создание всех внутренних контролов
            self._createEditControls(self.result, self.environment)
        
    def _createEditControls(self, Result_, Environment_):
        """
        Создание всех внутренних контролов редактирования.
        """
        # Сначала удалить все контролы
        self.removeAll()
        
        logics = self._logicTranslate.keys()
        requisite = None  # Структура описания реквизита
        func = None       # Структура описания функции
        # Перебор по строкам редактирования
        for i_row, row in enumerate(Result_):
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
    
    def _setRequisiteFilterCtrl(self, Control_, Description_):
        """
        Установить у контрола редактирования структуру управления по русскому описанию.
        """
        # Найти стурктуру управления в окружении
        for requisite in self.environment['requisites']:
            if requisite['description'] == Description_:
                Control_.filter_ctrl = requisite
                return requisite
        return None
        
    def OnDelEditRow(self, event):
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
        del_row_button.Bind(wx.EVT_BUTTON, self.OnDelEditRow)
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

    def _getControlRowIndex(self, Control_):
        """
        Получить индекс строки контрола редактирования.
        """
        for i, row_control in enumerate(self.edit_controls):
            # Не забыть проверить в дочерних объектах
            if Control_ in row_control or \
               bool([control for control in row_control if Control_ in control.GetChildren()]):
                return i
        return -1

    def _getEditControlByChild(self, Control_):
        """
        Получить контрол редактирования по дочернему контролу.
        """
        for i, row_control in enumerate(self.edit_controls):
            # Не забыть проверить в дочерних объектах
            find_parent = [control for control in row_control if Control_ in control.GetChildren()]
            if Control_ in row_control:
                return row_control[row_control.index(Control_)]
            elif bool(find_parent):
                find_control = find_parent[0]
                return find_control
        return None
    
    def _addRequisiteResult(self, RequisiteIdx_):
        """
        Добавить в результат выбранный реквизит.
        @param RequisiteIdx_: Индекс выбранного реквизита.
        """
        self.result.append([])
        control = self.edit_controls[-1][1]
        self.result[-1].append(self.environment['requisites'][RequisiteIdx_])                
        
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
    
    def _getFuncChoiceFromRequisite(self, Requisite_):
        """
        Получить список выбора функций из реквизита.
        """
        result = []
        for func in Requisite_['funcs']:
            if isinstance(func, str):
                # Это ссылка на стандартные функции
                # Стандартные функции находятся в окружении
                result.append(self.environment['funcs'][func]['description'])
            elif isinstance(func, dict):
                # Это описание нестандартной функции
                result.append(func['description'])
        return result
        
    def _getFuncChoiceFromEnv(self, Idx_):
        """
        Получить список выбора функций из окружения.
        @param Idx_: Индекс строки редактирования.
        """
        result = []
        requisite = self.result[Idx_][0]
        if requisite['funcs']:
            for func in requisite['funcs']:
                if isinstance(func, dict):
                    result.append(func['description'])
                elif isinstance(func, str):
                    if self.environment:
                        func = self.environment['funcs'][func]
                        result.append(func['description'])
                else:
                    io_prnt.outWarning(u'Ошибка. Не корректный тип функции: <%s<' % func)
        return result
    
    def _getFunctions(self, Idx_):
        """
        Получить список выбора функций из окружения для указанной строки редактирования.
        @param Idx_: Индекс строки редактирования.
        """
        result = []
        requisite = self.result[Idx_][0]
        if requisite['funcs']:
            for func in requisite['funcs']:
                if isinstance(func, dict):
                    result.append(func)
                elif isinstance(func, str):
                    if self.environment:
                        func = self.environment['funcs'][func]
                        result.append(func)
                else:
                    io_prnt.outWarning(u'Ошибка. Не корректный тип функции: <%s>' % func)
        return result
    
    def delFuncChoice(self, Idx_):
        """
        Удалить из редактора контрол выбора функции.
        @param Idx_: Индекс строки редактирования.
        """
        # Убрать контролы из сайзеров
        for control in self.edit_controls[Idx_][2:]:
            self.builder_panel_row_sizers[Idx_].Remove(control)
            # Да и ваще удалить контрол
            control.Destroy()
        # Убрать контролы из списка редактирумых контролов
        self.edit_controls[Idx_] = self.edit_controls[Idx_][:2]
        # Очистить результат в последнюю очередь
        self.result[Idx_] = self.result[Idx_][:1]
        
    def addFuncChoice(self, Idx_):
        """
        Добавить в редактор контрол выбора функции.
        @param Idx_: Индекс строки редактирования.
        """
        # Перед добавлением удалить все ненужное
        self.delFuncChoice(Idx_)
        
        new_choice = icCustomChoice(self.builder_panel, -1, size=wx.Size(200, -1))
        new_choice.setData(self._getFunctions(Idx_))
        new_choice.Bind(wx.EVT_TEXT, self.OnFuncChoice)
        self.builder_panel_row_sizers[Idx_].Add(new_choice, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        # Запомнить новый контрол в списке контролов редактирования
        self.edit_controls[Idx_].append(new_choice)
        # Надо после добавления контрола обязательно запустить
        # перераспределение контролов
        self.GetSizer().Layout()
    
    def _addFuncResult(self, FuncIdx_, Idx_=-1):
        """
        Добавить в результат выбранную функцию.
        @param RequisiteIdx_: Индекс выбранного реквизита.
        """
        control = self.edit_controls[Idx_][2]
        self.result[Idx_].append(control.data[FuncIdx_])
        
    def OnFuncChoice(self, event):
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
        
    def _getArgsFromEnv(self, Idx_):
        """
        Получить список аргументов из окружения для указанной строки редактирования.
        """
        func = self.result[Idx_][1]
        return func['args']
        
    def _addArgEdit(self, Idx_, Arg_):
        """
        Добавить в редактор контрол редактирования аргумента функции.
        @param Idx_: Индекс строки редактирования.
        @param Arg_: Структура описания аргумента. Формат filter_builder_env.FILTER_ARG.
        """
        # Добавить подпись
        new_arg_label = wx.StaticText(self.builder_panel, -1, label=Arg_['description']+u':')
        self.builder_panel_row_sizers[Idx_].Add(new_arg_label, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        self.edit_controls[Idx_].append(new_arg_label)
        
        # Добавить редактор
        if 'ext_edit' in Arg_ and Arg_['ext_edit']:
            # Для аргумента определен расширенный редактор
            new_arg_edit = icArgExtededEdit(self.builder_panel, -1)
            if 'default' in Arg_:
                new_arg_edit.default = Arg_['default']
        else:
            # Обычный текстовый редактор
            new_arg_edit = wx.TextCtrl(self.builder_panel, -1)
            if 'default' in Arg_:
                new_arg_edit.SetValue(str(Arg_['default']))
        # Привязать обработчик изменения редактируемого текста
        new_arg_edit.Bind(wx.EVT_TEXT, self.OnArgChange)
        self.builder_panel_row_sizers[Idx_].Add(new_arg_edit, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        self.edit_controls[Idx_].append(new_arg_edit)
        
    def addArgsEdit(self, Idx_):
        """
        Добавить в редактор контролы редактирования аргументов функции.
        @param Idx_: Индекс строки редактирования.
        """
        args = self._getArgsFromEnv(Idx_)
        for arg in args:
            # Добавить контролы редактирования аргумента функции
            self._addArgEdit(Idx_, arg)

        # Добавить выпадающий список логической связки строк
        self._addLogicChoice(Idx_)
        
        # Надо после добавления контрола обязательно запустить
        # перераспределение контролов
        self.GetSizer().Layout()
        
    # Словарь преобразований логических связок надписей
    _logicTranslate = {'': '', u'И': 'AND', u'ИЛИ': 'OR', u'НЕ': 'NOT'}
    
    def _addLogicChoice(self, Idx_):
        """
        Добавить выпадающий список логической связки строк - AND/OR/NOT.
        @param Idx_: Индекс строки редактирования.
        """
        new_logic_choice = wx.Choice(self.builder_panel, -1,
                                     choices=self._logicTranslate.keys())
        new_logic_choice.Bind(wx.EVT_CHOICE, self.OnLogicChoice)
        self.builder_panel_row_sizers[Idx_].Add(new_logic_choice, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.edit_controls[Idx_].append(new_logic_choice)

    def _addLogicResult(self, Logic_, Idx_):
        """
        Добавить в результат логическую связку.
        @param Logic_: AND/OR/NOT.
        @param Idx_: Индекс строки редактирования.
        """
        if self.result[Idx_][-1] not in self._logicTranslate.values():
            self.result[Idx_].append(Logic_)
        else:
            self.result[Idx_][-1] = Logic_
        
    def OnArgChange(self, event):
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
        
    def _getArgResult(self, ArgIdx_, Idx_):
        """
        Получить аргумент из результат по индексу.
        @param ArgIdx_: Индекс аргумента.
        @param Idx_: Индекс строки редактирования.
        """
        arg_idx = 2+ArgIdx_
        if arg_idx < len(self.result[Idx_]):
            arg_str = self.result[Idx_][arg_idx]
            if arg_str not in self._logicTranslate.keys():
                return arg_str
                
        # Аргумент с таким индексом не добавлен в строку
        return None        
        
    def _addArgResult(self, StrArg_, ArgIdx_, Idx_):
        """
        Добавить в результат значение аргумента функции.
        @param StrArg_: Строка аргумента.
        @param ArgIdx_: Индекс аргумента.
        @param Idx_: Индекс строки редактирования.
        """
        arg_idx = 2+ArgIdx_
        # Сначала выяснить добавлен ли аргумент в результат уже
        arg_str_result = self._getArgResult(ArgIdx_, Idx_)
        if arg_str_result is None:
            # Аргумент уже присутствует
            # надо просто поменять его значение
            self.result[Idx_][arg_idx] = StrArg_
        else:
            # Аргумента с таким индексом нет
            # нодо его добавить
            self.result[Idx_].insert(arg_idx, StrArg_)
        
    def OnLogicChoice(self, event):
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

    def delFilterEdit(self, Idx_=-1):
        """
        Удалить строку фильтрации.
        @param Idx_: Индекс удаляемой строки редактирования.
        @return: True-строка удалена,False-строка не удалена.
        """
        # Если удаляемая строка не последняя
        # Последнюю строку удалить нельзя
        if Idx_ < len(self.edit_controls)-1:
            
            # Очистить сайзер
            self.builder_panel_row_sizers[Idx_].Clear()
            
            # Убрать контролы
            for control in self.edit_controls[Idx_]:
                # Да и ваще удалить контрол
                control.Destroy()
            
            # Убрать контролы из списка редактирумых контролов
            del self.edit_controls[Idx_]
            # И удалить сайзер
            del_sizer = self.builder_panel_row_sizers[Idx_]
            del self.builder_panel_row_sizers[Idx_]
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

    # env = copy.deepcopy(filter_builder_env.FILTER_ENVIRONMENT)
    env = filter_builder_env.FILTER_ENVIRONMENT
    func1 = {'func': filter_builder_env.str_equal,
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
    requisite1['funcs'].append({'func': None, 'description': u'Просто для отладки'})
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
