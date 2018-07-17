#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для класса wxStaticBoxSizer. Генерирут объект по ресурсному описанию. Класс wxStaticBoxSizer
наследуется от wxBoxSizer. Отличие состоит в том, что компонент имеет границу c подписью как wxStaticBox.

@type SPC_IC_STATIC_BOXSIZER: C{Dictionary}
@var SPC_IC_STATIC_BOXSIZER: Спецификация на ресурсное описание компонента. Описание ключей:

    - B{name = 'DefaultName'}: Имя объекта.
    - B{type = 'BoxSizer'}: Тип объекта.
    - B{label=''}: Подпись группы.
    - B{layout = 'vertical'}: Ориентация контейнера ('vertical' | 'horizontal')
    - B{proportion=0}: Флаг указывает как ведут себя включенные объекты при изменении размера родительского окна. 0 - размеры
         компонентов не изменяются; 1 - размеры компонентов пропорционально изменяются.
    - B{flag=0}: Способ вытягивания и выравнивания.
        TOP, BOTTOM, LEFT, RIGHT or ALL - определяют, где будет распологатся граница.
        GROW or EXPAND - в зависимости от ориентации (vertical | horizontal)  используется первый или второй флаг для того, чтобы компонент
        увеличивал один из размеров размер до размера родительского окна.
        SHAPED - Для того, чтобы все размеры компонента увеличивались пропорционально размерам родительского окна.
        ALIGN_CENTER, ALIGN_LEFT, ALIGN_TOP, ALIGN_RIGHT,
        ALIGN_BOTTOM, ALIGN_CENTER_VERTICAL,
        ALIGN_CENTER_HORIZONTAL, ALIGN_CENTRE_HORIZONTAL - способы выравнивания
    - B{border=0}: Наличие бордюры.
    - B{child=[]}: Описание добавляемых элементов в сайзер.
"""

import wx
from ic.utils.util import icSpcDefStruct
from ic.components import icwidget
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf
from ic.log import log

from . import icspacesizer


SPC_IC_STATIC_BOXSIZER = {'type': 'StaticBoxSizer',
                          'name': 'DefaultName',
                          'child': [],

                          'label': '',
                          'size': (-1, -1),
                          'position': (-1, -1),
                          'layout': 'vertical',
                          'proportion': 0,
                          'flag': 0,
                          'border': 0,

                          '__lists__': {'layout': ['vertical', 'horizontal']},
                          '__parent__': icwidget.SPC_IC_SIZER,

                          '__attr_hlp__': {'layout': u'Ориентация сайзера',
                                           }
                          }

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------

#   Тип компонента
ic_class_type = icDefInf._icSizersType

#   Имя пользовательского класса
ic_class_name = 'icStaticBoxSizer'

#   Описание стилей компонента
ic_class_styles = None

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_STATIC_BOXSIZER
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtStaticBoxSizer'
ic_class_pic2 = '@common.imgEdtStaticBoxSizer'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.sizersr.icstaticboxsizer.icStaticBoxSizer-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = None

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = ['Dialog', 'Frame', 'ToolBarTool', 'Separator', 'GridCell']

#   Версия компонента
__version__ = (1, 0, 1, 2)


class icStaticBoxSizer(icwidget.icSizer, wx.StaticBoxSizer):
    """
    Интерфейс к классу wx.StaticBoxSizer через ресурсное описание.
    """

    def __init__(self, parent, id=-1, component={}, logType=0,
                 evalSpace={}, bCounter=False, progressDlg=None, sizer=None):
        """
        Конструктор для создания объекта icStaticBoxSizer.
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
        @type sizer: C{icSizer}
        @param sizer: Ссылка на родительский сайзер.
        """
        icSpcDefStruct(SPC_IC_STATIC_BOXSIZER, component)
        icwidget.icSizer.__init__(self, parent, id, component,
                                  logType, evalSpace, sizer=sizer)
        
        #   Картеж задающий вид прокутки (bHoriz, bVert)
        self.enableScr = None
        orient = component['layout']
                
        if orient == 'vertical':
            self.orient = wx.VERTICAL
        else:
            self.orient = wx.HORIZONTAL
            
        statbox = wx.StaticBox(parent, -1, component['label'], size=self.size)
        statbox.Enable(False)
        wx.StaticBoxSizer.__init__(self, statbox, self.orient)
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
            if not self.evalSpace['_root_obj']:
                self.evalSpace['_root_obj'] = self
                parent = self
            else:
                parent = self.parent

            kernel = self.GetKernel()
            kernel.parse_resource(parent, self.child, self, context=self.evalSpace,
                                  bCounter=bCounter, progressDlg=progressDlg)

            # Добавляем в сайзер дочерние элементы
            for child in self.component_lst:
                # log.debug(u'Добавление объекта <%s> в сайзер <%s>. %s' % (child.name, self.name, child.flag))
                self.Add(child, child.proportion, child.flag, child.border)
                self.regObject(child)

            try:
                if not self.parent_sizer:
                    parent.SetSizer(self)
                    parent.SetAutoLayout(1)
                    if self.enableScr:
                        parent.EnableScrolling(* self.enableScr)
                        self.SetVirtualSizeHints(parent)
            except:
                log.fatal(u'Ошибка при привязке сайзера')

    def DrawShape(self, dc=None):
        """
        Рисует представление для StaticBoxSizer.
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
            return wx.StaticBoxSizer.AddSpacer(self, size, proportion, flag, border)
        return wx.StaticBoxSizer.Add(self, obj, proportion, flag, border)
