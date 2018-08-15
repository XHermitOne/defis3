#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль класса - менеджера абстрактного контрола панели WX.
"""

# Подключение библиотек
import wx
import wx.adv
import wx.gizmos
import wx.dataview

from ic.log import log
from ic.utils import ic_time
from ic.utils import ic_str
from ic.utils import key_combins
from ic.utils import wxfunc
from ic import config

from . import listctrl_manager
from . import treectrl_manager
from . import toolbar_manager
from . import validate_manger


__version__ = (0, 1, 1, 1)


class icPanelManager(listctrl_manager.icListCtrlManager,
                     treectrl_manager.icTreeCtrlManager,
                     toolbar_manager.icToolBarManager,
                     validate_manger.icValidateManager):
    """
    Менеджер WX панели.
    В самом общем случае в этот класс перенесены функции работы
    с панелью из менеджера форм.
    Перенос сделан с целью рефакторинга.
    Также этот класс могут наследовать классы специализированных
    менеджеров, которые работают с панелями для управления
    записями/объектами.
    """
    # ВНИМАНИЕ! Метод get_ctrl_value определен в validate_manger.icValidateManager

    def set_ctrl_value(self, ctrl, value):
        """
        Установить значение контрола не зависимо от типа.
        @param ctrl: Объект контрола.
        @param value: Значение контрола.
        @return: True/False.
        """
        result = False
        if hasattr(ctrl, 'setValue'):
            # Обработка пользовательских контролов
            # Обычно все пользовательские контролы имеют
            # метод установки данных <setValue>
            ctrl.setVaue(value)
            result = True
        elif issubclass(ctrl.__class__, wx.CheckBox):
            ctrl.SetValue(value)
            result = True
        elif issubclass(ctrl.__class__, wx.StaticText):
            value = value if isinstance(value, str) else ic_str.toUnicode(value, config.DEFAULT_ENCODING)
            ctrl.SetLabel(value)
            result = True
        elif issubclass(ctrl.__class__, wx.TextCtrl):
            value = value if isinstance(value, str) else ic_str.toUnicode(value, config.DEFAULT_ENCODING)
            ctrl.SetValue(value)
            result = True
        elif issubclass(ctrl.__class__, wx.adv.DatePickerCtrl):
            wx_dt = ic_time.pydatetime2wxdatetime(value)
            ctrl.SetValue(wx_dt)
            result = True
        elif issubclass(ctrl.__class__, wx.DirPickerCtrl):
            ctrl.SetPath(value)
            result = True
        elif issubclass(ctrl.__class__, wx.SpinCtrl):
            ctrl.SetValue(int(value))
            result = True
        elif issubclass(ctrl.__class__, wx.dataview.DataViewListCtrl):
            self._set_wxDataViewListCtrl_data(ctrl, value)
            result = True
        else:
            log.warning(u'icFormManager. Тип контрола <%s> не поддерживается для заполнения' % ctrl.__class__.__name__)
        return result

    def get_panel_data(self, panel, data_dict=None, *ctrl_names):
        """
        Получить выставленные значения в контролах объекта панели.
        @param data_dict: Словарь для заполнения.
            Если не определен то создается новый словарь.
        @param ctrl_names: Взять только контролы с именами...
            Если имена контролов не определены,
            то обрабатываются контролы,
            указанные в соответствиях (accord).
        """
        result = dict() if data_dict is None else data_dict
        if not ctrl_names:
            ctrl_names = self.__accord.values()

        for ctrlname in dir(panel):
            if ctrl_names and ctrlname not in ctrl_names:
                # Если нельзя автоматически добавлять новые
                # данные и этих данных нет в заполняемом словаре,
                # то пропустить обработку
                continue

            ctrl = getattr(panel, ctrlname)
            if issubclass(ctrl.__class__, wx.Window) and ctrl.IsEnabled():
                if issubclass(ctrl.__class__, wx.Panel):
                    data = self.get_panel_data(ctrl, data_dict, *ctrl_names)
                    result.update(data)
                else:
                    value = self.get_ctrl_value(ctrl)
                    result[ctrlname] = value
        return result

    def set_panel_data(self, panel, data_dict=None, *ctrl_names):
        """
        Установить значения в контролах.
        @param panel: Объект панели.
        @param data_dict: Словарь для заполнения.
        @param ctrl_names: Взять только контролы с именами...
            Если имена контролов не определены,
            то обрабатываются контролы,
            указанные в соответствиях (accord).
        """
        if data_dict is None:
            log.warning(u'Не определен словарь заполнения для контролов окна')
            return

        for name, value in data_dict.items():
            for ctrlname in dir(panel):
                if ctrl_names and ctrlname not in ctrl_names:
                    # Если нельзя автоматически добавлять новые
                    # данные и этих данных нет в заполняемом словаре,
                    # то пропустить обработку
                    continue

                if ctrlname == name:
                    ctrl = getattr(panel, ctrlname)
                    self.set_ctrl_value(ctrl, value)
                    break

    def _getCtrlData(self):
        """
        Получить данные контролов для сохранения.
        Не все данные могут сохраняться.
        @return: Словарь с данными для записи.
        """
        ctrl_data = dict()
        # Сначала сохранить размеры и положение самого окна
        ctrl_data['self'] = dict(pos=tuple(self.GetPosition()),
                                 size=tuple(self.GetSize()))

        for ctrlname in dir(self):
            ctrl = getattr(self, ctrlname)
            if issubclass(ctrl.__class__, wx.Window) and ctrl.IsEnabled():
                if issubclass(ctrl.__class__, wx.SplitterWindow):
                    ctrl_data[ctrlname] = dict(sash_pos=ctrl.GetSashPosition())
                else:
                    log.warning(u'icDialogManager. Тип контрола <%s> не поддерживается' % ctrl.__class__.__name__)

        return ctrl_data

    def _setCtrlData(self, ctrl_data):
        """
        Установить данные контролов после загрузки.
        @param ctrl_data: Данные контролов.
        @return: True/False.
        """
        # Сначала установить размеры и позиции
        # самого диалогового окна
        dlg_data = ctrl_data.get('self', dict())
        size = dlg_data.get('size', (-1, -1))
        self.SetSize(*size)
        pos = dlg_data.get('pos', (-1, -1))
        self.SetPosition(*pos)

        # Перебор других контролов
        for ctrlname, ctrl_value in [item for item in ctrl_data.items() if item[0] != 'self']:
            ctrl = getattr(self, ctrlname)
            if issubclass(ctrl.__class__, wx.Window) and ctrl.IsEnabled():
                if issubclass(ctrl.__class__, wx.SplitterWindow):
                    ctrl.SetSashPosition(ctrl_value.get('sash_pos', -1))
                else:
                    log.warning(u'icDialogManager. Тип контрола <%s> не поддерживается' % ctrl.__class__.__name__)
        return True

    def set_accord(self, **accord):
        """
        Установить словарь соответствий значений
        контролов и имен прикладного кода.
        @param accord: Cловарь соответствий значений
        контролов и имен прикладного кода.
            Формат:
            {'Имя используемое в прикладном коде': 'Имя контрола', ...}
        """
        self.__accord = accord

    def add_accord(self, **accord):
        """
        Добавить словарь соответствий значений
        контролов и имен прикладного кода.
        @param accord: Cловарь соответствий значений
        контролов и имен прикладного кода.
            Формат:
            {'Имя используемое в прикладном коде': 'Имя контрола', ...}
        """
        if accord:
            self.__accord.update(accord)

    def get_accord(self):
        """
        Получить словарь соответствий значений
        контролов и имен прикладного кода.
        @return: Cловарь соответствий значений
        контролов и имен прикладного кода.
            Формат:
            {'Имя используемое в прикладном коде': 'Имя контрола', ...}
        """
        return self.__accord

    def get_accord_ctrl_data(self):
        """
        Получить согласованные данные.
        @return: Словарь значений из контролов
            в формате соответствий.
            Формат:
            {'Имя используемое в прикладном коде': 'Значение контрола', ...}
        """
        ctrl_data = self.get_ctrl_data(*self.__accord.values())
        result_data = dict([(name, ctrl_data[self.__accord[name]]) for name in self.__accord.keys()])
        return result_data

    def set_accord_ctrl_data(self, **data):
        """
        Установить согласованные данные.
        @param data: Словарь значений в формате соответствий.
            Контролы заполняются в согласно соответствиям.
            Формат:
            {'Имя используемое в прикладном коде': 'Значение контрола', ...}
        """
        ctrl_data = dict([(self.__accord[name], data[name]) for name in data.keys()])
        self.set_ctrl_data(ctrl_data, *ctrl_data.keys())

    def find_panel_accord(self, panel):
        """
        Найти на панели контролы ввода на панели и определить
        их как словарь соответствий.
        @param panel: Объект панели.
        @return: Словарь соответствий контролов ввода.
        """
        panel_ctrl_names = dir(panel)
        accord = dict()
        for ctrl_name in panel_ctrl_names:
            ctrl = getattr(panel, ctrl_name)
            if issubclass(ctrl.__class__, wx.TextCtrl):
                accord[ctrl_name] = ctrl_name
            elif issubclass(ctrl.__class__, wx.SpinCtrl):
                accord[ctrl_name] = ctrl_name
            elif issubclass(ctrl.__class__, wx.CheckBox):
                accord[ctrl_name] = ctrl_name
            elif issubclass(ctrl.__class__, wx.adv.DatePickerCtrl):
                accord[ctrl_name] = ctrl_name
            elif issubclass(ctrl.__class__, wx.DirPickerCtrl):
                accord[ctrl_name] = ctrl_name
            elif issubclass(ctrl.__class__, wx.dataview.DataViewListCtrl):
                accord[ctrl_name] = ctrl_name

        return accord

    def setAcceleratorTable_win(self, win=None, **key_combine_connections):
        """
        Установить акселераторную таблицу для окна.
        @param win: Объект окна для которого устанавливается акселераторная
            таблица. Если не определен, то берется self.
        @param key_combine_connections: Словарь связей комбинаций клавиш
            с контролами обработки/управления.
            Формат:
                {
                    'комбинация клавиш': идентификатор инструмента/пункта меню,
                    ...
                }
            Например:
                {
                    'CTRL_F1': self.tool1.GetId(), ...
                }
            Пример комбинаций клавиш см. ic/utils/key_combins.py
        @return: True/False
        """
        if win is None:
            win = self

        used_key_combins = [(key_combine_name,
                             key_combins.get_key_combine(key_combine_name)) for key_combine_name in key_combine_connections.keys()]
        used_key_connections = [(combine_key['mode'],
                                 combine_key['key'],
                                 key_combine_connections[name]) for name, combine_key in used_key_combins]
        win._accelerator_table = wx.AcceleratorTable(used_key_connections)
        win.SetAcceleratorTable(win._accelerator_table)

    def getAcceleratorTable_win(self, win=None):
        """
        Получить акселераторную таблицу окна.
        @param win: Объект окна для которого устанавливается акселераторная
            таблица. Если не определен, то берется self.
        @return: Объект акселераторной таблицы если он есть или None если его нет.
        """
        if win is None:
            win = self

        if hasattr(win, '_accelerator_table'):
            return win._accelerator_table
        else:
            log.warning(u'В объекте <%s> не обнаружена акселераторная таблица' % win.__class__.__name__)
        return None

    def setNotebookPage_image(self, notebook_ctrl, n_page=-1, img=None):
        """
        Установить картинку-иконку на странице wx.Notebook.
        @param notebook_ctrl: Объект wx.Notebook.
        @param n_page: Индекс страницы. Если < 0, то берется текущая выбранная.
        @param img: Объект образа. Если None, то картинка убирается.
        @return: True - картинка установлена. False - не устанолена по какой либо причине.
        """
        if notebook_ctrl is None:
            # Если объект не определен, то функция бессмыслена
            log.warning(u'Не определен объект wx.Notebook для установки иконки страницы')
            return False
        elif not issubclass(notebook_ctrl.__class__, wx.Notebook):
            log.warning(u'Объект не класса wx.Notebook в функции установки иконки страницы')
            return False

        if n_page < 0:
            n_page = notebook_ctrl.GetSelection()
        if n_page == wx.NOT_FOUND:
            log.warning(u'Не определена страница для установки иконки')
            return False

        try:
            if img is None:
                # Убрать иконку
                notebook_ctrl.SetPageImage(n_page, wx.NOT_FOUND)
            else:
                # ВНИМАНИЕ! В wx.Notebook не определен метод HasImageList
                # Для проверки наличия проверяем что возвращает GetImageList
                notebook_img_list = notebook_ctrl.GetImageList()
                if notebook_img_list:
                    img_idx = notebook_img_list.Add(img)
                else:
                    img_size = img.GetSize()
                    notebook_img_list = wx.ImageList(*img_size)
                    img_idx = notebook_img_list.Add(img)
                    notebook_ctrl.AssignImageList(notebook_img_list)
                notebook_ctrl.SetPageImage(n_page, img_idx)
            return True
        except:
            log.fatal(u'Ошибка установки иконки страницы объекта wx.Notebook')
        return False

    def clear_panel_data(self, panel):
        """
        Очистить значения в контролах.
        @param panel: Объект панели.
        """
        try:
            return self._clear_panel_data(panel)
        except:
            log.fatal(u'Ошибка очистки значения в контролах панели')

    def _clear_panel_data(self, panel):
        """
        Очистить значения в контролах.
        @param panel: Объект панели.
        """
        if not issubclass(panel.__class__, wx.Panel):
            return

        children = panel.GetChildren()

        for ctrl in children:
            if issubclass(ctrl.__class__, wx.Window) and ctrl.IsEnabled():
                if issubclass(ctrl.__class__, wx.Panel) and not wxfunc.is_same_wx_object(ctrl, panel):
                    self._clear_panel_data(ctrl)
                else:
                    try:
                        self.clear_ctrl_value(ctrl)
                    except:
                        log.fatal(u'Ошибка очистки значения контрола <%s>' % ctrl.__class__.__name__)

    def clear_ctrl_value(self, ctrl):
        """
        Очистить значение контрола не зависимо от типа.
        @param ctrl: Объект контрола.
        @return: True/False.
        """
        result = False
        if hasattr(ctrl, 'setValue'):
            # Обработка пользовательских контролов
            # Обычно все пользовательские контролы имеют
            # метод установки данных <setValue>
            ctrl.setValue(None)
            result = True
        elif issubclass(ctrl.__class__, wx.CheckBox):
            ctrl.SetValue(False)
            result = True
        elif issubclass(ctrl.__class__, wx.TextCtrl):
            ctrl.SetValue('')
            result = True
        elif issubclass(ctrl.__class__, wx.adv.DatePickerCtrl):
            if ctrl.GetExtraStyle() & wx.adv.DP_ALLOWNONE:
                ctrl.SetValue(None)
            else:
                wx_date = ic_time.pydate2wxdate(ic_time.Today())
                ctrl.SetValue(wx_date)
            result = True
        elif issubclass(ctrl.__class__, wx.DirPickerCtrl):
            ctrl.SetPath('')
            result = True
        elif issubclass(ctrl.__class__, wx.SpinCtrl):
            ctrl.SetValue(0)
            result = True
        elif issubclass(ctrl.__class__, wx.dataview.DataViewListCtrl):
            self._set_wxDataViewListCtrl_data(ctrl, ())
            result = True
        elif issubclass(ctrl.__class__, wx.ListCtrl):
            ctrl.DeleteAllItems()
            result = True
        else:
            log.warning(u'icFormManager. Тип контрола <%s> не поддерживается для очистки значения' % ctrl.__class__.__name__)
        return result

    def collapseSplitterPanel(self, splitter, toolbar=None, collapse_tool=None, expand_tool=None):
        """
        Cвертывание панели сплиттера.
        @param splitter: Объект сплиттера wx.SplitterWindow.
        @param toolbar: Панель инструментов.
            Для включения и выключения инструментов.
        @param collapse_tool: Инструмент панели инструментов свертывания панели сплиттера.
            Для включения и выключения инструментов.
        @param expand_tool: Инструмент панели инструментов развертывания панели сплиттера.
            Для включения и выключения инструментов.
        @return: True/False.
        """
        if not isinstance(splitter, wx.SplitterWindow):
            log.warning(u'Объект <%s> не является сплиттером' % str(splitter))
            return False

        setattr(self, '_last_sash_position_%s' % splitter.GetId(),
                splitter.GetSashPosition())
        # ВНИМАНИЕ! Указывать позицию сплитера как 0 нельзя
        # иначе схлопывание панели будет не полным
        #                        v
        splitter.SetSashPosition(1)

        if toolbar:
            if collapse_tool:
                toolbar.EnableTool(collapse_tool.GetId(), False)
            if expand_tool:
                toolbar.EnableTool(expand_tool.GetId(), True)
        return True

    def expandSplitterPanel(self, splitter, toolbar=None, collapse_tool=None, expand_tool=None):
        """
        Развертывание панели сплиттера.
        @param splitter: Объект сплиттера wx.SplitterWindow.
        @param toolbar: Панель инструментов.
            Для включения и выключения инструментов.
        @param collapse_tool: Инструмент панели инструментов свертывания панели сплиттера.
            Для включения и выключения инструментов.
        @param expand_tool: Инструмент панели инструментов развертывания панели сплиттера.
            Для включения и выключения инструментов.
        @return: True/False.
        """
        if not isinstance(splitter, wx.SplitterWindow):
            log.warning(u'Объект <%s> не является сплиттером' % str(splitter))
            return False

        last_sash_position_name = '_last_sash_position_%s' % splitter.GetId()
        if not hasattr(self, last_sash_position_name):
            log.warning(u'Не определеана предыдущее положение панели сплиттера')
            return False

        last_sash_position = getattr(self, last_sash_position_name)
        splitter.SetSashPosition(last_sash_position)
        if toolbar:
            if collapse_tool:
                toolbar.EnableTool(collapse_tool.GetId(), True)
            if expand_tool:
                toolbar.EnableTool(expand_tool.GetId(), False)
        return True

    def get_ctrl_data(self, data_dict=None, *ctrl_names):
        """
        Получить выставленные значения в контролах.
        @param data_dict: Словарь для заполнения.
            Если не определен то создается новый словарь.
        @param ctrl_names: Взять только контролы с именами...
            Если имена контролов не определены,
            то обрабатываются контролы,
            указанные в соответствиях (accord).
        """
        return self.get_panel_data(self, data_dict, *ctrl_names)

    def set_ctrl_data(self, data_dict=None, *ctrl_names):
        """
        Установить значения в контролах.
        @param data_dict: Словарь для заполнения.
        @param ctrl_names: Взять только контролы с именами...
            Если имена контролов не определены,
            то обрабатываются контролы,
            указанные в соответствиях (accord).
        """
        return self.set_panel_data(self, data_dict, *ctrl_names)

