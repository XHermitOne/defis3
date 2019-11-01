#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Контрол выбора элемента справочника в виде выбора кодов по уровням.
"""

import wx

from ic.components import icwidget
from ic.log import log

# Version
__version__ = (0, 1, 1, 3)

DEFAULT_CODE_DELIMETER = u' '
DEFAULT_ENCODING = 'utf-8'

# Спецификация
SPC_IC_SPRAVLEVELCHOICECTRL = {'sprav': None,  # Паспорт справочника-источника данных
                               'label': None,  # Заголовок области выбора справочника
                                               # если не определена, то берется как descrption из справочника
                               'auto_select': True,    # Производить авто заполнение

                               'on_select_code': None,  # Код, который выполняется
                                                        # при заполнении кода

                               '__parent__': icwidget.SPC_IC_WIDGET,

                               '__attr_hlp__': {'sprav': u'Паспорт справочника-источника данных',
                                                'label': u'Заголовок области выбора справочника, если не определена, то берется как descrption из справочника',
                                                'auto_select': u'Производить авто заполнение',
                                                'on_select_code': u'Блок кода, который выполняется при заполнении кода справочника',
                                                },
                               }


class icSpravLevelChoiceCtrlProto(wx.StaticBox):
    """
    Класс компонента выбора элемента справочника в виде выбора кодов по уровням.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        wx.StaticBox.__init__(self, *args, **kwargs)

        self.box_sizer = wx.BoxSizer(wx.VERTICAL)
        self.scrolled_win = wx.ScrolledWindow(self,  wx.ID_ANY,
                                              wx.DefaultPosition, wx.DefaultSize,
                                              wx.HSCROLL | wx.VSCROLL)
        self.scrolled_win.SetScrollRate(5, 5)

        self.sizer = wx.FlexGridSizer(0, 2, 0, 0)
        self.sizer.AddGrowableCol(1)
        self.sizer.SetFlexibleDirection(wx.BOTH)
        self.sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_ALL)

        self.scrolled_win.SetSizer(self.sizer)
        self.scrolled_win.Layout()
        self.sizer.Fit(self.scrolled_win)

        self.box_sizer.Add(self.scrolled_win, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.box_sizer)
        self.Layout()

        # Объект справочника
        self._sprav = None
        # Текущий выбранный код в списковом представлении
        self._selected_code = []

        # Зарегистрированные контролы вобора кодов по уровням
        self._choice_ctrl_list = []

    def getSelectedCode(self):
        return tuple(self._selected_code)

    def setSprav(self, sprav):
        """
        Устанвить справочник.
        """
        self._sprav = sprav

        if self._sprav:
            # Заголовок
            label = self.GetLabel()
            if not label:
                # Если заголовок не определен, то взять из справочника
                if hasattr(self._sprav, 'description'):
                    label = self._sprav.description
                    self.SetLabel(label)
            # Контролы уровней
            self._selected_code = [None] * self._sprav.getLevelCount()
            self._choice_ctrl_list = []
            for i, level in enumerate(self._sprav.getLevels()):
                description = level.description if level.description else u''
                label = wx.StaticText(self.scrolled_win, wx.ID_ANY, description,
                                      wx.DefaultPosition, wx.DefaultSize, 0)

                level_choices = list()
                if not i:
                    for rec in self._sprav.getStorage().getLevelTable():
                        rec_dict = self._sprav.getStorage().getSpravFieldDict(rec, level_idx=i)
                        if self._sprav.isActive(rec_dict['cod']):
                            level_choice = (rec_dict['cod'], rec_dict['name'])
                            level_choices.append(level_choice)

                choice_id = wx.NewId()
                choice = wx.Choice(self.scrolled_win, choice_id,
                                   wx.DefaultPosition, wx.DefaultSize)
                for code, name in level_choices:
                    item = choice.Append(name)
                    choice.SetClientData(item, code)

                # Запомнить индекс уровня
                choice.level_index = i
                choice.Bind(wx.EVT_CHOICE, self.onLevelCodeChange, id=choice_id)
                # Зарегистрировать контрол
                self._choice_ctrl_list.append(choice)

                self.sizer.Add(label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
                self.sizer.Add(choice, 1, wx.ALL | wx.EXPAND, 5)
            self.scrolled_win.Layout()
            self.sizer.Fit(self.scrolled_win)

    def getSprav(self):
        """
        Объект справочника.
        """
        return self._sprav

    def getCode(self):
        """
        Выбранный код справочника.
        """
        return ''.join([subcode for subcode in self.getSelectedCode() if subcode])

    def findItemIdxByCode(self, level_index, code):
        """
        Найти индекс элемента списка по коду.
        @param level_index: Индекс уровня, соответствующий списку выбора.
        @param code: Код справочника.
        @return: Индекс элемента списка или -1 если не найдено.
        """
        choice_ctrl = self._choice_ctrl_list[level_index]
        for item in range(choice_ctrl.GetCount()):
            find_code = choice_ctrl.GetClientData(item)
            if find_code == code:
                return item
        return -1

    def setCode(self, code=None):
        """
        Установить код справочника как выбранный.
        @param code: Код справочника.
        @return: True/False.
        """
        if code is None:
            # Если код не определен, то скорее всего мы
            # хотим очистить контрол
            return self.clearSelect()

        if self._sprav is not None:
            # ВНИМАНИЕ! self._selected_code заполняется
            # в функции selectLevelChoice. Поэтому
            # здесь инициализировать его не надо.
            selected_code = self._sprav.StrCode2ListCode(code)
            for i, subcode in enumerate(selected_code):
                item = self.findItemIdxByCode(i, subcode)
                if item >= 0:
                    self.selectLevelChoice(i, item, auto_select=False)
            return True
        return False

    getValue = getCode
    setValue = setCode

    def getChoiceSelectedCode(self, choice_ctrl, item=-1):
        """
        Получить выбранный код из контрола wx.Choice.
        @param choice_ctrl: Объект контрола.
        @param item: Индекс пункта, есл не определен, то
            имеется в виду выбранный пункт.
        @return: Строковый выбранный код.
        """
        if item < 0:
            item = choice_ctrl.GetSelection()
        try:
            return choice_ctrl.GetClientData(item)
        except:
            log.fatal(u'Не данных узла <%d>' % item)
        return None

    def clearLevelChoice(self, min_index=0, max_index=-1):
        """
        Очистить списки выбора.
        @param min_index: Индекс первого уровня.
            Если не определен, то берется самый первый уровень.
        @param max_index: Индекс последнего уровня.
            Если не определен, то берется самый последний уровень.
        @return: True/False.
        """
        if max_index < 0:
            max_index = len(self._selected_code)-1

        for i in range(min_index, max_index+1):
            # Очистить коды этих уровней
            self._selected_code[i] = None
            if self._choice_ctrl_list[i]:
                # Очистить списки контролов выбора
                self._choice_ctrl_list[i].Clear()
        return True

    def clearSelect(self):
        """
        Очистить выбор контролов.
        """
        for choice_ctrl in self._choice_ctrl_list:
            choice_ctrl.SetSelection(wx.NOT_FOUND)
        return True

    def initLevelChoice(self, level_index, auto_select=True):
        """
        Инициализировать список выбора.
        @param level_index: Индекс уровня, соответствующий списку выбора
        @param auto_select: Автоматический выбор первого элемента списка.
        @return: True/False.
        """
        if self._sprav.isEmpty():
            # Если справочник пустой, то не можем
            # инициализировать по индексу уровня
            log.warning(u'Пустой справочник. Не возможно инициализировать список выбора')
            return False

        if level_index < 0:
            level_index = 0
        elif level_index >= len(self._selected_code):
            level_index = len(self._selected_code)-1

        # Получить контрол выбора кода уровня
        choice_ctrl = self._choice_ctrl_list[level_index]
        if choice_ctrl:
            code_list = self._selected_code[:level_index]
            if not code_list:
                log.warning(u'Не найдены подкоды <%s : %d>' % (str(self._selected_code), level_index))
                return False

            str_code = ''.join(code_list)

            level_choices = list()
            for rec in self._sprav.getStorage().getLevelTable(str_code):
                rec_dict = self._sprav.getStorage().getSpravFieldDict(rec, level_idx=level_index)
                if self._sprav and self._sprav.isActive(rec_dict['cod']):
                    # log.debug(u'Словарь записи %s' % str(rec_dict))
                    level_choice = (rec_dict['cod'][len(str_code):], rec_dict['name'])
                    level_choices.append(level_choice)

            for code, name in level_choices:
                item = choice_ctrl.Append(name)
                choice_ctrl.SetClientData(item, code)
            if auto_select:
                self.selectLevelChoice(level_index, auto_select=auto_select)
        return True

    def selectLevelChoice(self, level_index, item=0, auto_select=True):
        """
        Выбрать код уровня.
        @param level_index: Индекс уровня.
        @param item: Индекс выбирамого пункта.
        @param auto_select: Автоматический выбор первого элемента списка
            в последующих контролах.
        @return: True/False.
        """
        if level_index >= len(self._selected_code):
            return False
        choice_ctrl = self._choice_ctrl_list[level_index]
        choice_ctrl.SetSelection(item)
        # Заполнить код уровня
        item_code = self.getChoiceSelectedCode(choice_ctrl, item)
        # print 'DBG. Item code:', item, item_code
        self._selected_code[level_index] = item_code
        # print 'DBG. Selected code', self._selected_code

        # Заполнили код и надо выполнить код
        self.onSelectCode()

        i = choice_ctrl.level_index+1
        # Очистить нижестоящие уровни
        self.clearLevelChoice(i)
        # После заполнения кода надо определить список следующего уровня
        if i < len(self._selected_code):
            self.initLevelChoice(i, auto_select=auto_select)

    def getAutoSelect(self):
        """
        Производить ато-заполнение?
        @return: True/False.
        """
        return True

    def onLevelCodeChange(self, event):
        """
        Обработчик смены кода уровня.
        """
        choice_ctrl = event.GetEventObject()
        self.selectLevelChoice(choice_ctrl.level_index,
                               choice_ctrl.GetSelection(),
                               auto_select=self.getAutoSelect())
        event.Skip()

    def onSelectCode(self):
        """
        Код который выполняется когда выбирается код.
        Метод должен переопределяться в дочерних классах.
        """
        pass


def test():
    """
    Функция тестирования.
    """
    app = wx.PySimpleApp()

    frm = wx.Frame(None, -1)

    ctrl = icSpravLevelChoiceCtrlProto(frm, -1)
    ctrl.SetLabel(u'Тест')

    frm.Show()

    app.MainLoop()


if __name__ == '__main__':
    test()
