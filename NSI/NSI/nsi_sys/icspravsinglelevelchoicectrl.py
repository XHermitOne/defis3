#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Контрол выбора кода элемента справочника одного уровня.
"""

import wx

from ic.components import icwidget
from ic.log import log

# Version
__version__ = (0, 1, 1, 1)

DEFAULT_CODE_DELIMETER = u' '
DEFAULT_ENCODING = 'utf-8'

# Спецификация
SPC_IC_SPRAVSINGLELEVELCHOICECTRL = {'sprav': None,  # Паспорт справочника-источника данных
                                     'label': None,  # Заголовок области выбора справочника
                                                     # если не определена, то берется как descrption из справочника
                                     'n_level': 0,   # Номер уровня справочника для выбора

                                     'on_select_code': None,  # Код, который выполняется
                                                              # при заполнении кода

                                     '__parent__': icwidget.SPC_IC_WIDGET,

                                     '__attr_hlp__': {'sprav': u'Паспорт справочника-источника данных',
                                                      'label': u'Заголовок области выбора справочника, если не определена, то берется как descrption из справочника',
                                                      'n_level': u'Номер уровня справочника для выбора',
                                                      'on_select_code': u'Код, который выполняется при заполнении кода',
                                                      },
                                     }


class icSpravSingleLevelChoiceCtrlProto(wx.StaticBox):
    """
    Класс компонента выбора кода элемента справочника одного уровня.
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

        # Родительский код справочника в списковом представлении
        self._parent_code = [None]
        # Текущий выбранный код в списковом представлении
        self._selected_code = None

        # Контрол вобора кодов уровня
        self._choice = None

    def getSelectedCode(self):
        return tuple(self._selected_code)

    def setSprav(self, sprav):
        """
        Установить справочник.
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
            # Контрол уровня
            self._selected_code = None    # * self._sprav.getLevelCount()
            # self._choice_ctrl_list = []
            sprav_levels = self._sprav.getLevels()
            n_level = self.getNLevel()
            if 0 <= n_level < self._sprav.getLevelCount():
                level = sprav_levels[n_level]
                description = level.description if level.description else u''
                label = wx.StaticText(self.scrolled_win, wx.ID_ANY, description,
                                      wx.DefaultPosition, wx.DefaultSize, 0)
                level_choices = [(rec[0], rec[1]) for rec in self._sprav.getStorage().getLevelTable()]
                choice_id = wx.NewId()
                self._choice = wx.Choice(self.scrolled_win, choice_id,
                                         wx.DefaultPosition, wx.DefaultSize)
                for code, name in level_choices:
                    item = self._choice.Append(name)
                    self._choice.SetClientData(item, code)

                # Запомнить индекс уровня
                self._choice.Bind(wx.EVT_CHOICE, self.onLevelCodeChange, id=choice_id)

                self.sizer.Add(label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
                self.sizer.Add(self._choice, 1, wx.ALL | wx.EXPAND, 5)
            else:
                log.warning(u'Не корректно задан индекс <%s> редактируемого уровня справочника <%s>' % (n_level, self._sprav.getName()))

            self.scrolled_win.Layout()
            self.sizer.Fit(self.scrolled_win)

    def getSprav(self):
        """
        Объект справочника.
        """
        return self._sprav

    def setParentCode(self, parent_code=None):
        """
        Установить родительский код уровня.
        @param parent_code: Родительский код уровня.
            Пожет задаваться в строковом и списковом варианте.
        @return: True/False.
        """
        if isinstance(parent_code, list):
            self._parent_code = parent_code
        elif isinstance(parent_code, tuple):
            self._parent_code = list(parent_code)
        elif parent_code is None:
            self._parent_code = [None]
        elif isinstance(parent_code, str):
            self._parent_code = self._sprav.StrCode2ListCode(parent_code) if self._sprav else [None]
        else:
            log.warning(u'Не поддерживаемый тип <%s> родительского кода контрола <%s>' % (parent_code.__class__.__name__, self.name))
            return False
        return True

    def getCode(self):
        """
        Выбранный код справочника.
        """
        return ''.join([subcode for subcode in self.getSelectedCode() if subcode])

    def findItemIdxByCode(self, code):
        """
        Найти индекс элемента списка по коду.
        @param code: Код справочника.
        @return: Индекс элемента списка или -1 если не найдено.
        """
        choice_ctrl = self._choice
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
            # for idx, subcode in enumerate(selected_code):
            item = self.findItemIdxByCode(selected_code)
            if item >= 0:
                self.selectLevelChoice(item)
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
            # if self._choice_ctrl_list[idx]:
            # Очистить списки контролов выбора
            self._choice.Clear()
        return True

    def clearSelect(self):
        """
        Очистить выбор контролов.
        """
        self._choice.setSelection(wx.NOT_FOUND)
        return True

    def initLevelChoice(self):
        """
        Инициализировать список выбора.
        @return: True/False.
        """
        if self._sprav.isEmpty():
            # Если справочник пустой, то не можем
            # инициализировать по индексу уровня
            log.warning(u'Пустой справочник. Не возможно инициализировать список выбора')
            return False

        # Получить контрол выбора кода уровня
        choice_ctrl = self._choice
        if choice_ctrl:
            str_code = ''.join(self._selected_code)
            level_choices = [(rec[0][len(str_code):], rec[1]) for rec in self._sprav.getStorage().getLevelTable(str_code)]
            for code, name in level_choices:
                item = choice_ctrl.Append(name)
                choice_ctrl.SetClientData(item, code)
            # if auto_select:
            #     self.selectLevelChoice()
        return True

    def selectLevelChoice(self, item=0):
        """
        Выбрать код уровня.
        @param item: Индекс выбирамого пункта.
        @return: True/False.
        """
        choice_ctrl = self._choice
        choice_ctrl.setSelection(item)
        # Заполнить код уровня
        item_code = self.getChoiceSelectedCode(choice_ctrl, item)
        # print 'DBG. Item code:', item, item_code
        self._selected_code = item_code
        # print 'DBG. Selected code', self._selected_code

        # Заполнили код и надо выполнить код
        self.onSelectCode()

        i = choice_ctrl.level_index+1
        # Очистить нижестоящие уровни
        self.clearLevelChoice(i)
        # После заполнения кода надо определить список следующего уровня
        if i < len(self._selected_code):
            self.initLevelChoice()

    def getNLevel(self):
        """
        Индекс редактируемого уровня справочника.
        Уровни справочника индекисруются от 0.
        @return: Индекс редактируемого уровня справочника.
        """
        return 0

    def onLevelCodeChange(self, event):
        """
        Обработчик смены кода уровня.
        """
        choice_ctrl = event.GetEventObject()
        self.selectLevelChoice(choice_ctrl.GetSelection())
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

    ctrl = icSpravSingleLevelChoiceCtrlProto(frm, -1)
    ctrl.SetLabel(u'Тест')

    frm.Show()

    app.MainLoop()


if __name__ == '__main__':
    test()
