#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для класса wxBoxSizer. Генерирут объект по ресурсному описанию. Данный
объект является контейнером для других визуальных компонентов. Он позволяет выстраивать эти объекты в
определенном линейном порядке.

@type SPC_IC_BOXSIZER: C{Dictionary}
@var SPC_IC_BOXSIZER: Спецификация на ресурсное описание компонента. Описание ключей:

    - B{name = 'DefaultName'}: Имя объекта.
    - B{type = 'BoxSizer'}: Тип объекта.
    - B{layout = 'vertical'}: Ориентация контейнера ('vertical' | 'horizontal')
    - B{proportion=0}: Флаг указывает как ведут себя включенные объекты при изменении размера родительского окна. 0 - размеры
         компонентов не изменяются; 1 - размеры компонентов пропорционально изменяются.
    - B{flag=0}: Способ вытягивания и выравнивания.
        wxTOP, wxBOTTOM, wxLEFT, wxRIGHT or wxALL - определяют, где будет распологатся граница.
        wxGROW or wxEXPAND - в зависимости от ориентации (vertical | horizontal)  используется первый или второй флаг для того, чтобы компонент
        увеличивал один из размеров размер до размера родительского окна.
        wxSHAPED - Для того, чтобы все размеры компонента увеличивались пропорционально размерам родительского окна.
        wxALIGN_CENTER, wxALIGN_CENTRE, wxALIGN_LEFT, wxALIGN_TOP, wxALIGN_RIGHT,
        wxALIGN_BOTTOM, wxALIGN_CENTER_VERTICAL, wxALIGN_CENTRE_VERTICAL,
        wxALIGN_CENTER_HORIZONTAL, wxALIGN_CENTRE_HORIZONTAL - способы выравнивания.
        
    - B{border=0}: Наличие бордюры.
    - B{child=[]}: Описание добавляемых элементов в сайзер.

@type SPC_IC_SIZER_SPACE: C{dictionary}
@var SPC_IC_SIZER_SPACE: Спецификация на ресурсное описание spacer - пустой компонент, обладующий только размерами.
Описание ключей SPC_IC_SIZER_SPACE:

    - C{name='DefaultName'}: Имя.
    - C{type='SizerSpace'}: Тип.
    - C{position=(-1,-1)}: Расположение в сайзере (GridBagSizer).
    - C{size=(0,0)}: Размер.

@type ICSizerFlag: C{dictionary}
@var ICSizerFlag: Словарь специальных стилей компонента. Описание ключей ICSizerFlag:

    - C{wxTOP}:
    - C{wxBOTTOM}:
    - C{wxLEFT}:
    - C{wxRIGHT}:
    - C{wxALL}: Определяют, где будет распологатся граница.
    - C{wxGROW}: Используется для того, чтобы компонент увеличивал высоту до размера родительского окна.
    - C{wxEXPAND}: Используется для того, чтобы компонент увеличивал ширину до размера родительского окна.
    - C{wxSHAPED}: Для того, чтобы все размеры компонента увеличивались пропорционально размерам родительского окна.
    - C{wxALIGN_CENTER}:
    - C{wxALIGN_CENTRE}:
    - C{wxALIGN_LEFT}:
    - C{wxALIGN_TOP}:
    - C{wxALIGN_RIGHT}:
    - C{wxALIGN_BOTTOM}:
    - C{wxALIGN_CENTER_VERTICAL}:
    - C{wxALIGN_CENTRE_VERTICAL}:
    - C{wxALIGN_CENTER_HORIZONTAL}:
    - C{wxALIGN_CENTRE_HORIZONTAL}: Cпособы выравнивания.
"""

import wx
from ic.utils.util import icSpcDefStruct
from ic.components import icwidget
import ic.kernel.io_prnt as io_prnt
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf

from ic.log import log

from . import icspacesizer

SPC_IC_BOXSIZER = {'type': 'BoxSizer',
                   'name': 'DefaultName',
                   'child': [],

                   'layout': 'vertical',
                   'position': (0, 0),
                   'span': (1, 1),
                   'proportion': 0,
                   'flag': 0,
                   'border': 0,

                   '__lists__': {'layout': ['vertical', 'horizontal']},
                   '__attr_types__': {},
                   '__parent__': icwidget.SPC_IC_SIZER,
                   '__attr_hlp__': {'layout': u'Ориентация сайзера',
                                    }
                   }


SPC_IC_SIZER_SPACE = {'type': 'SizerSpace',
                      'name': 'DefaultName',

                      'position': (-1, -1),
                      'size': (0, 0),
                      }


ICSizerFlag = {'TOP': wx.TOP,
               'BOTTOM': wx.BOTTOM,
               'LEFT': wx.LEFT,
               'RIGHT': wx.RIGHT,
               'ALL': wx.ALL,
               'GROW': wx.GROW,
               'EXPAND': wx.EXPAND,
               'SHAPED': wx.SHAPED,
               'ALIGN_CENTER': wx.ALIGN_CENTER,
               'ALIGN_LEFT': wx.ALIGN_LEFT,
               'ALIGN_TOP': wx.ALIGN_TOP,
               'ALIGN_RIGHT': wx.ALIGN_RIGHT,
               'ALIGN_BOTTOM': wx.ALIGN_BOTTOM,
               'ALIGN_CENTER_VERTICAL': wx.ALIGN_CENTER_VERTICAL,
               'ALIGN_CENTER_HORIZONTAL': wx.ALIGN_CENTER_HORIZONTAL}

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------
#   Тип компонента
ic_class_type = icDefInf._icSizersType

#   Имя пользовательского класса
ic_class_name = 'icBoxSizer'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_BOXSIZER
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtBoxSizer'
ic_class_pic2 = '@common.imgEdtBoxSizer'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.sizers.icboxsizer.icBoxSizer-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = None

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = ['Dialog', 'Frame', 'ToolBarTool', 'Separator', 'GridCell']

#   Версия компонента
__version__ = (1, 0, 2, 2)


class icBoxSizer(icwidget.icSizer, wx.BoxSizer):
    """
    Интерфейс к классу wxBoxSizer через ресурсное описание.
    """

    def __init__(self, parent, id=-1, component={}, logType=0, evalSpace={},
                 bCounter=False, progressDlg=None, sizer=None):
        """
        Конструктор для создания объекта icBoxSizer.
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
        icSpcDefStruct(SPC_IC_BOXSIZER, component)
        icwidget.icSizer.__init__(self, parent, id, component, logType, evalSpace, sizer=sizer)
        orient = component['layout']

        # Кортеж задающий ориентацию (bHoriz, bVert)
        self.enableScr = None
        if orient == 'vertical':
            self.orient = wx.VERTICAL
        else:
            self.orient = wx.HORIZONTAL

        wx.BoxSizer.__init__(self, self.orient)

        self.objectList = []
        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)
        
        if parent:
            import ic.utils.graphicUtils as grph
            parent_bgr = parent.GetBackgroundColour()
            self.shape_clr = grph.AdjustColour2(parent_bgr, 7)
        else:
            self.shape_clr = icwidget.icSizer.DESIGN_SHAPE_COLOR

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.child:
            if '_root_obj' not in self.evalSpace or not self.evalSpace['_root_obj']:
                self.evalSpace['_root_obj'] = self
                parent = self
            else:
                parent = self.parent

            kernel = self.GetKernel()
            kernel.parse_resource(parent, self.child, self, context=self.evalSpace,
                                  bCounter=bCounter, progressDlg=progressDlg)

            # Добавляем в сайзер дочерние элементы
            for child in self.component_lst:
                # log.debug(u'Добавляем в сайзер <%s> элемент <%s>' % (self.name, child.name))
                self.Add(child, child.proportion, child.flag, child.border)
                self.regObject(child)
            try:
                if not self.parent_sizer:
                    # log.debug(u'Привязка сайзера <%s> к <%s>' % (self.name, parent.name))
                    parent.SetSizer(self)
                    if self.enableScr:
                        parent.EnableScrolling(*self.enableScr)
                        self.SetVirtualSizeHints(parent)
            except:
                io_prnt.outErr(u'Ошибка при привязке сайзера')

    def DrawShape(self, dc=None):
        """
        Рисует представление для BoxSizer.
        """
        if self.editorBackground:
            clr = self.shape_clr
            
            if self.shapeType == icwidget.icParentShapeType:
                clr = (190, 0, 0)

            self.DrawCursor(clr=clr)

            #   Рисуем разметку для компонентов
            if not dc:
                dc = wx.ClientDC(self.GetParent())
                
            x, y = self.GetPosition()
            sx, sy = self.GetSize()
            oldpen = dc.GetPen()
            pen = wx.Pen(clr, 1)
            dc.SetPen(pen)
            
            for obj in self.objectList:
                x1, y1 = obj.GetPosition()
                sx1, sy1 = obj.GetSize()

                #   Рисуем курсор
                if self.GetOrientation() == wx.VERTICAL:
                    dc.DrawLine(x, y1+sy1, x+sx, y1+sy1)
                else:
                    dc.DrawLine(x1+sx1, y, x1+sx1, y+sy)
                    
            #   Востанавливаем
            dc.SetPen(oldpen)

    def Add(self, obj, proportion=0, flag=0, border=0):
        """
        Вызов стандартной функции добавления элементов сайзера.
        ВНИМАНИЕ! Если пользоваться не стандартной функцией,
        а определенной в icSizer, то при закрытии формы возникает
        исключение <Segmentation fault>.
        Выявлена проблема только методом исключения.
        @param obj: Окно, которое будет добавлено в sizer.
            Его первоначальный размер (либо явно заданный пользователем,
            либо вычисляемый внутри себя при использовании wxDefaultSize)
            интерпретируется как минимальный, а во многих случаях и начальный размер.
        @param proportion: Хотя значение этого параметра не определено в wxSizer,
            оно используется в wxBoxSizer, чтобы указать, может ли дочерний элемент
            изменять свой размер в основной ориентации wxBoxSizer,
            где 0 означает, что оно не изменяется, а значение больше нуля равно
            интерпретируется относительно значения других детей одного и
            того же wxBoxSizer.
            Например, у вас может быть горизонтальный wxBoxSizer с тремя детьми,
            два из которых должны изменить свой размер с помощью sizer.
            Затем два растяжимых окна получат значение 1 каждый, чтобы заставить
            их расти и сжиматься одинаково с горизонтальным размером sizer.
        @param flag: OR-сочетание флагов, влияющих на поведение sizer.
            Подробнее см. Список флагов wxSizer.
        @param border: Определяет ширину границы, если параметр флага установлен
            для включения любого флага границы.
        """
        if isinstance(obj, icspacesizer.icSpaceSizer):
            size = tuple(obj.GetSize())
            return wx.BoxSizer.AddSpacer(self, size, proportion, flag, border)
        return wx.BoxSizer.Add(self, obj, proportion, flag, border)


def test(par=0):
    """
    Тестируем класс icBoxSizer
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'BoxSizer Test')
    win = wx.ScrolledWindow(frame, -1)
    sz = icBoxSizer(win, -1, {})
    btn1 = wx.Button(win, -1, 'btn1')
    btn2 = wx.Button(win, -1, 'btn2')
    btn1.type = 'Button'
    btn2.type = 'Button'
    sz.Add(btn1, 0, wx.EXPAND)
    sz.Add(btn2)
    win.SetSizer(sz)
    frame.Show(True)
    print(u'pos=%s, size=%s' % (sz.GetPosition(), sz.GetSize()))
    print(u'>> pos=%s, size=%s' % (btn1.GetPosition(), btn1.GetSize()))
    app.MainLoop()


if __name__ == '__main__':
    test()
