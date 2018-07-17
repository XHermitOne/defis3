#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для компонента wx.CheckListBox.

@type SPC_IC_CHECK_LIST_BOX: C{dictionary}
@var SPC_IC_CHECK_LIST_BOX: Спецификация на ресурсное описание CheckListBox.
Описание ключей SPC_IC_CHECK_LIST_BOX:

    - B{type='CheckListBox'}: Тип компонента.
    - B{name='default'}: Имя компонента.
    - B{field_name=None}: Имя поля базы данных, которое отображает компонент (не реализовано).
    - B{style=0}: Стиль окна.
    - B{position=(-1, -1)}: Расположение на родительском окне.
    - B{size=(-1,-1)}: Размеры компонента.
    - B{items=None}: Элемены выбора списка. Если словарь, то в качестве ключей используются
        элементы списка, в качестве значений значение флажка True | False. Если атрибут
        является списком, то его элементы являются элементами списка выбора, а значения
        все флагов установлены в False.
    - B{foregroundColor=None}: Цвет текста.
    - B{backgroundColor=None}: Цвет фона.
    - B{keyDown=None}: Выражение, выполняемое после нажатия любой кнопки в компоненте.
    - B{select=0}: Выражение, выполняемое после выбора значения.
    - B{source=None}: Описание или ссылка на источник данных.
"""

import wx
# from ic.dlg.msgbox import MsgBox
# from ic.log.iclog import MsgLastError, LogLastError
# from ic.utils.util import icSpcDefStruct
from ic.components.icfont import *
import ic.utils.util as util
from ic.components.icwidget import icWidget, SPC_IC_WIDGET
from ic.components import icwindow
import ic.PropertyEditor.icDefInf as icDefInf

SPC_IC_CHECK_LIST_BOX = {'type': 'CheckListBox',
                         'name': 'default',

                         'style': 0,
                         'position': (-1, -1),
                         'size': (-1, -1),
                         'items': None,     # Выравнивание
                         'foregroundColor': (0, 0, 0),
                         'backgroundColor': None,

                         '__attr_types__': {icDefInf.EDT_PY_SCRIPT: ['items'],
                                            },
                         '__parent__': SPC_IC_WIDGET,
                         }
                
# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------

#   Тип компонента. None, означает, что данный компонент убран из
#   редактора и остался только для совместимости со старыми проектами.
ic_class_type = icDefInf._icControlsType

#   Имя пользовательского класса
ic_class_name = 'icCheckListBox'

#   Описание стилей компонента
ic_class_styles = icwindow.ic_class_styles

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_CHECK_LIST_BOX
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtListCheckBox'
ic_class_pic2 = '@common.imgEdtListCheckBox'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.custom.icchecklistbox.icCheckListBox-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (1, 0, 0, 5)


class icCheckListBox(icWidget, wx.CheckListBox):
    """
    Класс представляет список выбора, элементы которого отмечаются флажками.
    """

    def __init__(self, parent, id, component, logType=0, evalSpace=None,
                bCounter=False, progressDlg=None, *arg, **kwarg):
        """
        Конструктор для создания icList

        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно
        @type id: C{int}
        @param id: Идентификатор окна
        @type component: C{dictionary}
        @param component: Словарь описания компонента
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений
        @type evalSpace: C{dictionary}
        """

        util.icSpcDefStruct(SPC_IC_CHECK_LIST_BOX, component)
        icWidget.__init__(self, parent, id, component, logType, evalSpace, bPrepareProp=True)

        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        size = component['size']
        pos = component['position']
        style = component['style']

        # --- Обрабатываем аттрибут инициализации списка --------------------
        self._dictRepl = dict()
        
        if not component['items']:
            self.items = list()
        elif type(component['items']) in (list, tuple):
            self.items = component['items']
        elif isinstance(component['items'], dict):
            self._dictRepl = component['items']
            self.items = self._dictRepl.keys()
        else:
            ret = util.getICAttr('@'+component['items'],
                                 self.evalSpace,
                                 'getICAttr() Error in icchoice.__init__(...) <items> name=%s' % self.name)

            if type(ret) in (list, tuple):
                self.items = ret
            elif isinstance(ret, dict):
                self._dictRepl = ret
                self.items = self._dictRepl.keys()
            else:
                self.items = list()

        wx.CheckListBox.__init__(self, parent, id, pos, size, self.items, style, name=self.name)

        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        self._choice_items = None
        if self._dictRepl:
            self.SetChoiceDict(self._dictRepl)
        self.BindICEvt()

    def SetChoiceItems(self, items):
        """
        Устанавливаем список выбора.
        """
        self._choice_items = items
        #   Чистим список выбора
        self.Clear()
        #   Добовляем элементы и устанавливаем нужные флаги
        for i, item in enumerate(items):
            self.Append(item[1])
            if len(item) > 2:
                self.Check(i, item[2])
        
    def GetRowId(self, indx):
        try:
            return self._choice_items[indx][0]
        except:
            pass
    
    def SetChoiceDict(self, dict):
        """
        Устанавливает новый список с признаками выбора.
        @type dict: C{dictionary}
        @param dict: Словарь, определяющий список с признаками выбора.
        """
        self._dictRepl = dict
        #   Чистим список выбора
        self.Clear()
        #   Добовляем элементы и устанавливаем нужные флаги
        indx = 0
        for key in dict:
            self.Append(key)
            self.Check(indx, dict[key])
            indx += 1
            
    def GetChoiceDict(self, bId=False):
        """
        Возврвщает словарь выбора, где в качестве ключей элементы выбора, в качестве
        значений бинарные признаки выбора.
        """
        dict_keys = list()
        for x in range(self.GetCount()):
            if bId:
                dict_keys.append(self.GetRowId(x) or self.GetString(x))
            else:
                dict_keys.append(self.GetString(x))

        for indx, key in enumerate(dict_keys):
            if self.IsChecked(indx):
                self._dictRepl[key] = True
            else:
                self._dictRepl[key] = False
                
        return self._dictRepl

    def GetChoiceList(self):
        """
        Возврвщает список выбора, элементами которого являются бинарные признаки выбора.
        """
        list_values = list()

        for indx in range(self.GetCount()):
            if self.IsChecked(indx):
                list_values.append(True)
            else:
                list_values.append(False)
                
        return list_values
        
    def SetChoiceList(self, lst):
        """
        Устанавливает список выбора, элементами которого являются бинарные признаки выбора.
        """
        try:
            for indx in range(self.GetCount()):
                if indx < len(lst):
                    self.Check(indx, lst[indx])
        except:
            LogLastError(u'Error in SetChoiceList(lst=%s)' % lst)
            return False
            
        return True
        
            
def test(par=0):
    """
    Тестируем класс icCheckListBox.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'icCheckListBox Test')
    
    win2 = icCheckListBox(frame, -1, {'position': (5, 35), 'items': ['one', 'two', 'three']})

    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()


if __name__ == '__main__':
    test()
