#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для класса wx.ComboBox. Генерирует поле ввода с вожмосностью выбора из списка значений.

@type SPC_IC_COMBOBOX: C{Dictionary}
@var SPC_IC_COMBOBOX: Спецификация на ресурсное описание компонента. Описание ключей:

    - B{name = 'DefaultName'}: Имя объекта.
    - B{type = 'ComboBox'}: Тип объекта.
    - B{value = ''}: Текст в поле ввода.
    - B{position = (-1,-1)}: Расположение компонента на родительском окне.
    - B{size = (-1,-1)}: Размер картинки.
    - B{font = {}}: Шрифт текста.
    - B{foregroundColor=None}: Цвет текста.
    - B{backgroundColor=None}:Цвет фона.
    - B{style = 0}: Стиль панели инструментов. Стили:
        - C{wx.CB_SIMPLE}  - Создается combobox с окном в котором выведен весь список значений (только Windows).
        - C{wx.CB_DROPDOWN} - Создается combobox с выпадающим списком.
        - C{wx.CB_READONLY} - аналог icChoice.
        - C{wx.CB_SORT}  - Сортирут список в алфавитном порядке.
    
    - B{init = None}: Функционал формирующий список выбора.
    - B{items = []}: Список выбора.

@type ICComboBoxStyle: C{dictionary}
@var ICComboBoxStyle: Словарь специальных стилей компонента. Описание ключей ICComboBoxStyle:

    - C{wx.CB_SIMPLE}  - Создается combobox с окном в котором выведен весь список значений (только Windows).
    - C{wx.CB_DROPDOWN} - Создается combobox с выпадающим списком.
    - C{wx.CB_READONLY} - аналог icChoice.
    - C{wx.CB_SORT} - Сортирут список в алфавитном порядке.
"""

import wx
from ic.dlg.msgbox import MsgBox
from ic.log.iclog import *
import ic.utils.util as util
from ic.components.icwidget import icWidget, SPC_IC_WIDGET
import ic.PropertyEditor.icDefInf as icDefInf

LOG_TYPE = 0

ICComboBoxStyle = {'CB_SIMPLE': wx.CB_SIMPLE,
                   'CB_DROPDOWN': wx.CB_DROPDOWN,
                   'CB_READONLY': wx.CB_READONLY,
                   'CB_SORT': wx.CB_SORT}

SPC_IC_COMBOBOX = {'type': 'ComboBox',
                   'name': 'default',
                   'style': 0,

                   'value': '',
                   'font': {},
                   'position': (-1, -1),
                   'size': (-1, -1),
                   'items': [],
                   'foregroundColor': (0, 0, 0),
                   'backgroundColor': (255, 255, 255),

                   '__parent__': SPC_IC_WIDGET,
                   }

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------

#   Тип компонента. None, означает, что данный компонент убран из
#   редактора и остался только для совместимости со старыми проектами.
ic_class_type = icDefInf._icControlsType

#   Имя пользовательского класса
ic_class_name = 'icComboBox'

#   Описание стилей компонента
ic_class_styles = ICComboBoxStyle

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_COMBOBOX
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtChoice'
ic_class_pic2 = '@common.imgEdtChoice'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.custom.iccombobox.icComboBox-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (1, 0, 0, 5)

                                    
class icComboBox(icWidget, wx.ComboBox):
    """
    Интерфейс для поля ввода с возможностью выбора одного
    из значений (ComboBox) - обкладка над компонентом wx.ComboBox.
    """
    def __init__(self, parent, id, component, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор для создания icComboBox.

        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type id: C{int}
        @param id: Идентификатор окна.
        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        """
        util.icSpcDefStruct(SPC_IC_COMBOBOX, component)
        icWidget.__init__(self, parent, id, component, logType, evalSpace)
        
        self.bChanged = 0
        self.items = component['items']
        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        size = component['size']
        pos = component['position']
        style = component['style']

        # --- Обрабатываем аттрибут инициализации списка
        if not component['items']:
            self.items = []
        elif type(component['items']) in (list, tuple):
            self.items = component['items']
        elif isinstance(component['items'], dict):
            self._dictRepl = component['items']
            self.items = self._dictRepl.values()
            self.items.sort()
        else:
            ret = util.getICAttr('@'+component['items'], self.evalSpace,
                                 'getICAttr() Error in icchoice.__init__(...) <items> name=%s' % self.name)

            if type(ret) in (list, tuple):
                self.items = ret
            elif isinstance(ret, dict):
                self._dictRepl = ret
                self.items = self._dictRepl.values()
                self.items.sort()
            else:
                self.items = []

        wx.ComboBox.__init__(self, parent, id, component['value'], pos, size, self.items, style, name=self.name)

        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        self.BindICEvt()
        
    def setItems(self, items, sel=-1):
        self.Clear()
        self._itemsLst = items
        self._dictRepl = None
        #   Заполняем список новыми значениями
        for item in items:
            self.Append(item[1], item[0])
        
        self.SetSelection(sel)


def test(par=0):
    """
    Тестируем класс icComboBox.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'icComboBox Test', size=(200, 100))
    win = wx.Panel(frame, -1)
    ctrl_1 = icComboBox(win, -1, {'items': ['1', '2', '3', '4'],
                                  'size': (100, -1),
                                  'keyDown': 'print \'keyDown in ComboBox\'',
                                  'position': (20, 20),
                                  })
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
