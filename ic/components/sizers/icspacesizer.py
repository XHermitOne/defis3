#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Компонент, обладающий только размерами. Используется в сайзерах.

@type SPC_IC_SIZER_SPACE: C{dictionary}
@var SPC_IC_SIZER_SPACE: Спецификация на ресурсное описание spacer - пустой компонент, обладующий только размерами.
Описание ключей SPC_IC_SIZER_SPACE:
    - C{name='DefaultName'}: Имя.
    - C{type='SizerSpace'}: Тип.
    - C{position=(-1,-1)}: Расположение в сайзере (GridBagSizer).
    - C{size=(0,0)}: Размер.
"""

import wx
from ic.utils.util import icSpcDefStruct
from ic.components import icwidget
from ic.imglib import common
import ic.PropertyEditor.icDefInf as icDefInf

SPC_IC_SIZER_SPACE = {'type': 'SizerSpace',
                      'name': 'DefaultName',

                      'position': (-1, -1),
                      'size': (0, 0),

                      '__parent__': icwidget.SPC_IC_BASE,
                      }

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------

#   Тип компонента
ic_class_type = icDefInf._icSizersType

#   Имя пользовательского класса
ic_class_name = 'icSpaceSizer'

#   Описание стилей компонента
ic_class_styles = None

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_SIZER_SPACE
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtSizerSpacer'
ic_class_pic2 = '@common.imgEdtSizerSpacer'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.sizers.icspacesizer.icSpaceSizer-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (1, 0, 1, 2)


class icSpaceSizer(icwidget.icBase):
    """
    Компонент обладающий только размером. Используется только в сайзерах.
    """
    component_spc = ic_class_spc
    
    def __init__(self, parent, id=-1, component={}, logType=0, evalSpace={},
                 bCounter=False, progressDlg=None):
        """
        Конструктор для создания объекта icSpaceSizer.

        @type parent: C{wxWindow}
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
        icSpcDefStruct(SPC_IC_SIZER_SPACE, component)
        icwidget.icBase.__init__(self, parent, id, component, logType, evalSpace)

        #   Указатель на сайзер, куда добавляется компонент
        self.contaningSizer = None
        
    def GetParent(self):
        """
        Возвращает указатель на родителя.
        """
        return self.parent

    def GetName(self):
        """
        Возвращает имя компонента.
        """
        return self.name
    
    def SetName(self, name):
        """
        Устанавливает имя компонента.
        """
        self.name = name
        
    def GetSize(self):
        """
        Возвращает размер компонента.
        """
        return self.size

    def SetSize(self, size):
        """
        Устанавливает новые размеры.
        """
        self.size = size
        
    def GetPosition(self):
        """
        Возвращает позицию компонента.
        """
        #   Позиция вычисляется по разному в зависимости от типа сайзера,
        #   где расологается компонент
        if self.contaningSizer and self.contaningSizer.type == 'GridBagSizer':
            row, col = self.position
            sx, sy = self.GetSize()
            
            pt = self.contaningSizer.GetCellRBPoint(row, col)
            if pt:
                x, y = pt
                return wx.Point(x-sx, y-sy)
            else:
                return wx.Point(0, 0)
                
        elif self.contaningSizer:
            try:
                if self.contaningSizer.type == 'StaticBoxSizer':
                    x, y = (5, 13)
                else:
                    x, y = (0, 0)

                for obj in self.contaningSizer.objectList:

                    if obj != self:
                        dx, dy = obj.GetSize()
                        
                        if self.contaningSizer.orient == wx.VERTICAL:
                            y = y+dy
                        else:
                            x = x+dx
                    else:
                        return wx.Point(x, y)
            except:
                pass
        
        return self.position

    def SetPosition(self, pos):
        """
        Устанавливает новую позицию.
        """
        self.position = pos
        
    def GetRect(self):
        """
        Возвращает координаты и размеры компонента.
        """
        x, y = self.GetPosition()
        sx, sy = self.GetSize()
        return wx.Rect(x, y, sx, sy)
