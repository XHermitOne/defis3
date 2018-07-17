#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс пользовательского компонента ПРОСТОЙ ПРОСМОТРЩИК OGL ДИАГРАММ.

@type ic_user_name: C{string}
@var ic_user_name: Имя пользовательского класса.
@type ic_can_contain: C{list | int}
@var ic_can_contain: Разрешающее правило - список типов компонентов, которые
    могут содержаться в данном компоненте. -1 - означает, что любой компонент
    может содержатся в данном компоненте. Вместе с переменной ic_can_not_contain
    задает полное правило по которому определяется возможность добавления других
    компонентов в данный комопнент.
@type ic_can_not_contain: C{list}
@var ic_can_not_contain: Запрещающее правило - список типов компонентов,
    которые не могут содержаться в данном компоненте. Запрещающее правило
    начинает работать если разрешающее правило разрешает добавлять любой
    компонент (ic_can_contain = -1).

Перья:
@var BLACK_DASHED_PEN: Черный пунктир
@var BLACK_PEN: Черный
@var CYAN_PEN: Голубой
@var GREY_PEN: Серый
@var LIGHT_GREY_PEN: Светло-серый
@var MEDIUM_GREY_PEN: Средне-серый
@var RED_PEN: Красный
@var TRANSPARENT_PEN: Прозрачный
@var WHITE_PEN: Белый

Заливки:
@var BLACK_BRUSH: Черная
@var BLUE_BRUSH: Синяя
@var CYAN_BRUSH: Голубая
@var GREY_BRUSH: Серая
@var LIGHT_GREY_BRUSH: Светло-серая
@var MEDIUM_GREY_BRUSH: Средне-серая
@var RED_BRUSH: Красная
@var TRANSPARENT_BRUSH: Прозрачная
@var WHITE_BRUSH: Белая

Стрелки:
@var ARROW_HOLLOW_CIRCLE: Пустой круг
@var ARROW_FILLED_CIRCLE: Заполненный круг
@var ARROW_ARROW: Простая стрелка
@var ARROW_SINGLE_OBLIQUE: Одинарная косая
@var ARROW_DOUBLE_OBLIQUE: Двойная косая
"""

import wx
import ic.components.icwidget as icwidget
import ic.utils.util as util
from ic.utils import coderror
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf

import wx.lib.ogl as parentModule

from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportListUserEdt as pspListEdt

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icSimpleOGLViewer'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = {'type': 'SimpleOGLViewer',
                'name': 'default',
                'description': None,
                'child': [],
                'activate': True,
                'init_expr': None,
                '_uuid': None,

                'is_draggable': True,
                'on_shape_dbl_click': None,    # Обработчик двойного клика на фигуре

                '__styles__': ic_class_styles,
                '__events__': {},
                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_TEXTFIELD: ['description'],
                                   icDefInf.EDT_CHECK_BOX: ['is_draggable'],
                                   },
                '__parent__': icwidget.SPC_IC_WIDGET,
                '__attr_hlp__': {'on_shape_dbl_click': u'Обработчик двойного клика на фигуре',
                                 },
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = common.imgEdtDiagram
ic_class_pic2 = common.imgEdtDiagram

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = None

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 4)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    return pspEdt.str_to_val_user_property(text, propEdt)


# --- Константы ---

# Размеры фигуры по умолчанию
DEFAULT_OGL_SHAPE_WIDTH = 150
DEFAULT_OGL_SHAPE_HEIGHT = 70

# Спейсер авторазмещения
DEFAULT_AUTOLAYOUT_SPACER_X = 50
DEFAULT_AUTOLAYOUT_SPACER_Y = 50

# Перья
BLACK_DASHED_PEN = wx.BLACK_DASHED_PEN
BLACK_PEN = wx.BLACK_PEN
CYAN_PEN = wx.CYAN_PEN
GREY_PEN = wx.GREY_PEN
LIGHT_GREY_PEN = wx.LIGHT_GREY_PEN
MEDIUM_GREY_PEN = wx.MEDIUM_GREY_PEN
RED_PEN = wx.RED_PEN
TRANSPARENT_PEN = wx.TRANSPARENT_PEN
WHITE_PEN = wx.WHITE_PEN
IC_PEN_LIST = [BLACK_DASHED_PEN, BLACK_PEN, CYAN_PEN, GREY_PEN, LIGHT_GREY_PEN,
               MEDIUM_GREY_PEN, RED_PEN, TRANSPARENT_PEN, WHITE_PEN]
IC_PEN_STR_LIST = ['BLACK_DASHED_PEN', 'BLACK_PEN', 'CYAN_PEN', 'GREY_PEN', 'LIGHT_GREY_PEN',
                   'MEDIUM_GREY_PEN', 'RED_PEN', 'TRANSPARENT_PEN', 'WHITE_PEN']

# Заливки
BLACK_BRUSH = wx.BLACK_BRUSH
BLUE_BRUSH = wx.BLUE_BRUSH
CYAN_BRUSH = wx.CYAN_BRUSH
GREY_BRUSH = wx.GREY_BRUSH
LIGHT_GREY_BRUSH = wx.LIGHT_GREY_BRUSH
MEDIUM_GREY_BRUSH = wx.MEDIUM_GREY_BRUSH
RED_BRUSH = wx.RED_BRUSH
TRANSPARENT_BRUSH = wx.TRANSPARENT_BRUSH
WHITE_BRUSH = wx.WHITE_BRUSH
IC_BRUSH_LIST = [BLACK_BRUSH, BLUE_BRUSH, CYAN_BRUSH, GREY_BRUSH, LIGHT_GREY_BRUSH,
                 MEDIUM_GREY_BRUSH, RED_BRUSH, TRANSPARENT_BRUSH, WHITE_BRUSH]
IC_BRUSH_STR_LIST = ['BLACK_BRUSH', 'BLUE_BRUSH', 'CYAN_BRUSH', 'GREY_BRUSH', 'LIGHT_GREY_BRUSH',
                     'MEDIUM_GREY_BRUSH', 'RED_BRUSH', 'TRANSPARENT_BRUSH', 'WHITE_BRUSH']


# Стрелки
ARROW_HOLLOW_CIRCLE = parentModule.ARROW_HOLLOW_CIRCLE
ARROW_FILLED_CIRCLE = parentModule.ARROW_FILLED_CIRCLE
ARROW_ARROW = parentModule.ARROW_ARROW
ARROW_SINGLE_OBLIQUE = parentModule.ARROW_SINGLE_OBLIQUE
ARROW_DOUBLE_OBLIQUE = parentModule.ARROW_DOUBLE_OBLIQUE
IC_ARROW_LIST = [ARROW_HOLLOW_CIRCLE, ARROW_FILLED_CIRCLE, ARROW_ARROW,
                 ARROW_SINGLE_OBLIQUE, ARROW_DOUBLE_OBLIQUE]
IC_ARROW_STR_LIST = ['ARROW_HOLLOW_CIRCLE', 'ARROW_FILLED_CIRCLE', 'ARROW_ARROW',
                     'ARROW_SINGLE_OBLIQUE', 'ARROW_DOUBLE_OBLIQUE']


class icDividedShape(parentModule.DividedShape):
    """
    Фигура с разделенными регионами.
    """

    def __init__(self, id, width, height, canvas=None):
        """
        Конструктор.
        """
        parentModule.DividedShape.__init__(self, width, height)

        self.id = id
        self.titleFont = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.textFont = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.text2Font = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL)
        self.SetRegionSizes()
        self.ReformatRegions(canvas)

    def ReformatRegions(self, canvas=None):
        """
        Переформатирование регионов.
        """
        rnum = 0

        if canvas is None:
            canvas = self.GetCanvas()

        dc = wx.ClientDC(canvas)  # used for measuring

        for region in self.GetRegions():
            text = region.GetText()
            self.FormatText(dc, text, rnum)
            rnum += 1

    def OnSizingEndDragLeft(self, pt, x, y, keys, attch):
        """
        """
        parentModule.DividedShape.OnSizingEndDragLeft(self, pt, x, y, keys, attch)
        self.SetRegionSizes()
        self.ReformatRegions()
        self.GetCanvas().Refresh()


class icShapeEvtHandler(parentModule.ShapeEvtHandler):
    """
    """

    def __init__(self, *args, **kwargs):
        parentModule.ShapeEvtHandler.__init__(self)

    def OnLeftClick(self, x, y, keys=0, attachment=0):
        """
        """
        shape = self.GetShape()
        canvas = shape.GetCanvas()
        dc = wx.ClientDC(canvas)
        canvas.PrepareDC(dc)

        if shape.Selected():
            shape.Select(False, dc)
            canvas.Refresh(False)
            canvas.selected_shape = None
        else:
            redraw = False
            shapeList = canvas.GetDiagram().GetShapeList()
            toUnselect = []

            for s in shapeList:
                if s.Selected():
                    # If we unselect it now then some of the objects in
                    # shapeList will become invalid (the control points are
                    # shapes too!) and bad things will happen...
                    toUnselect.append(s)

            shape.Select(True, dc)
            canvas.selected_shape = shape

            if toUnselect:
                for s in toUnselect:
                    s.Select(False, dc)

                canvas.Refresh(False)

    def OnLeftDoubleClick(self, x, y, keys=0, attachment=0):
        """
        """
        shape = self.GetShape()
        canvas = shape.GetCanvas()
        on_shape_dbl_click = canvas.getOnShapeDblClick()
        if on_shape_dbl_click:
            canvas.context['selected_shape'] = shape
            canvas.eval_event('on_shape_dbl_click', None, False)
        return parentModule.ShapeEvtHandler.OnLeftDoubleClick(self, x, y, keys, attachment)

    def OnEndDragLeft(self, x, y, keys=0, attachment=0):
        """
        """
        shape = self.GetShape()
        parentModule.ShapeEvtHandler.OnEndDragLeft(self, x, y, keys, attachment)

        if not shape.Selected():
            self.OnLeftClick(x, y, keys, attachment)

    def OnSizingEndDragLeft(self, pt, x, y, keys, attch):
        """
        """
        parentModule.ShapeEvtHandler.OnSizingEndDragLeft(self, pt, x, y, keys, attch)

    def OnMovePost(self, dc, x, y, oldX, oldY, display):
        """
        """
        shape = self.GetShape()
        parentModule.ShapeEvtHandler.OnMovePost(self, dc, x, y, oldX, oldY, display)

    def OnRightClick(self, *dontcare):
        """
        """
        pass


class icSimpleOGLViewer(icwidget.icWidget, parentModule.ShapeCanvas):
    """
    Простой обозреватель OGL диаграмм.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.

        - B{type='defaultType'}:
        - B{name='default'}:
    """
    component_spc = ic_class_spc

    is_ogl_initialized = False

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор базового класса пользовательских компонентов.

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
        @type bCounter: C{bool}
        @param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        @type progressDlg: C{wx.ProgressDialog}
        @param progressDlg: Указатель на идикатор создания формы.
        """
        # Сначала инициализировать OGL если надо
        if not self.is_ogl_initialized:
            parentModule.OGLInitialize()
            self.is_ogl_initialized = True

        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        parentModule.ShapeCanvas.__init__(self, parent, id, style=wx.NO_BORDER)
        maxWidth = 1500
        maxHeight = 1500
        self.SetScrollbars(20, 20, maxWidth/20, maxHeight/20)
        # --- Свойства компонента ---
        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if x.find('__') != 0]

        for key in lst_keys:
            setattr(self, key, component[key])

        if component.get('backgroundColor', None):
            self.SetBackgroundColour(component['backgroundColor'])

        # Инициализация внутренних объектов компонента и установка значений по умолчанию.
        self._init_ogl_default()
        self._default_par = {}

        # Текущая выделенная фигура
        self.selected_shape = None

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        return prs.icResourceParser(self, self.resource['child'], None, evalSpace=self.evalSpace,
                                    bCounter=bCounter, progressDlg=progressDlg)

    def _init_ogl_default(self):
        """
        Инициализация внутренних объектов компонента и установка значений по умолчанию.
        """
        # Диаграмма
        self.diagram = parentModule.Diagram()
        self.SetDiagram(self.diagram)
        self.diagram.SetCanvas(self)

        # Список фигур диаграммы
        self.shapes = dict()
        # Список линий/связей
        self.lines = dict()

        # Данные диаграммы
        self.diagram_res = None

    def createShape(self, **attrs):
        """
        Создать объект фигуры.
        """
        shape = None
        if 'type' in attrs and 'name' in attrs:
            type = attrs['type']
            name = attrs['name']
            # Размеры
            if 'size' in attrs:
                width, height = tuple(attrs['size'])
            else:
                width, height = (DEFAULT_OGL_SHAPE_WIDTH, DEFAULT_OGL_SHAPE_HEIGHT)

            if type in ('icDividedShape',):
                shape = icDividedShape(id=name, width=width, height=height, canvas=self)
                shape.cod = attrs.get('cod', None)

        return shape

    def _isPointInArea(self, x, y, X_, Y_, Width_, Height_):
        """
        Находится указанная точка в области?
        """
        return x >= X_ and x <= (X_ + Width_) and y >= Y_ and y <= (Y_ + Height_)

    def _getShapeIntersectionArea(self, X_, Y_, Width_, Height_):
        """
        Найти фигуру пересекающую указанную область.
        """
        for shape in self.shapes.values():
            x = shape.GetX()
            y = shape.GetY()
            width = shape.GetWidth()
            height = shape.GetHeight()
            if self._isPointInArea(x, y, X_, Y_, Width_, Height_) or \
               self._isPointInArea(x+width, y, X_, Y_, Width_, Height_) or \
               self._isPointInArea(x, y+height, X_, Y_, Width_, Height_) or \
               self._isPointInArea(x+width, y+height, X_, Y_, Width_, Height_):
                return shape
        return None

    def genAutoLayoutPosXY(self, ShapeAttrs_):
        """
        Генерация следующего месторасположения фигуры.
        @return: Возвращает кортеж координат фигуры на канве.
        """
        try:
            x = DEFAULT_AUTOLAYOUT_SPACER_X + 50
            y = DEFAULT_AUTOLAYOUT_SPACER_Y
            if 'size' in ShapeAttrs_:
                width, height = tuple(ShapeAttrs_['size'])
            else:
                width, height = (DEFAULT_OGL_SHAPE_WIDTH, DEFAULT_OGL_SHAPE_HEIGHT)

            # Генерация Y
            to_lines = [line for line in self.diagram_res['lines'] if line['to'] == ShapeAttrs_['name']]
            for line in to_lines:
                from_shape = self.findShape(line['from'])
                if from_shape:
                    max_y = from_shape.GetY() + from_shape.GetHeight() + DEFAULT_AUTOLAYOUT_SPACER_Y
                    if max_y > y:
                        y = max_y
            from_lines = [line for line in self.diagram_res['lines'] if line['from'] == ShapeAttrs_['name']]
            for line in from_lines:
                to_shape = self.findShape(line['to'])
                if to_shape:
                    max_y = to_shape.GetY() + to_shape.GetHeight() + DEFAULT_AUTOLAYOUT_SPACER_Y
                    if max_y > y:
                        y = max_y

            # Генерация X
            intersection_shape = self._getShapeIntersectionArea(x, y, width, height)
            while intersection_shape is not None:
                x = intersection_shape.GetX() + intersection_shape.GetWidth() + DEFAULT_AUTOLAYOUT_SPACER_X
                intersection_shape = self._getShapeIntersectionArea(x, y, width, height)

            return x, y
        except:
            return DEFAULT_AUTOLAYOUT_SPACER_X + 50, DEFAULT_AUTOLAYOUT_SPACER_Y

    def set_default_par(self, dct):
        """
        Устанавливает позиции по умолчанию.
        """
        self._default_par = dct

    def get_default_par(self):
        """
        Возвращает позиции по умолчанию.
        """
        return self._default_par

    def setShapeProperties(self, Shape_, **attrs):
        """
        Установить свойства у объекта фигуры.
        """
        if Shape_:
            # Можно передвигать фигуры?
            is_draggable = self.isDraggable()
            Shape_.SetDraggable(is_draggable, is_draggable)
            Shape_.SetCanvas(self)

            # Установить координаты, если они определены
            if self._default_par.get(Shape_.id, None):
                x, y, width, height = self._default_par[Shape_.id]
                Shape_.SetWidth(width)
                Shape_.SetHeight(height)
                Shape_.SetX(x)
                Shape_.SetY(y)
            else:
                if 'pos' in attrs:
                    x, y = tuple(attrs['pos'])
                else:
                    x, y = self.genAutoLayoutPosXY(attrs)
                Shape_.SetX(x)
                Shape_.SetY(y)

                # Установить размер, если они определены
                if 'size' in attrs:
                    width, height = tuple(attrs['size'])
                else:
                    width, height = (150, 100)
                Shape_.SetWidth(width)
                Shape_.SetHeight(height)

            # Перо
            if 'pen' in attrs:
                pen = attrs['pen']
                if type(pen) in (str, unicode):
                    # Перо задано строковым значением
                    pen = eval(pen, globals(), locals())
                Shape_.SetPen(pen)

            # Заливка
            if 'brush' in attrs:
                brush = attrs['brush']
                if type(brush) in (str, unicode):
                    # Заливка задана строковым значением
                    brush = eval(brush, globals(), locals())
                Shape_.SetBrush(brush)

            is_divided_shape = isinstance(Shape_, parentModule.DividedShape)
            # Заголовок
            if 'title' in attrs:
                title = attrs['title']
                if title:
                    if is_divided_shape:
                        region_title = parentModule.ShapeRegion()
                        region_title.SetName('title')
                        region_title.SetText(title)
                        region_title.SetProportions(0.0, 0.3)   # Треть оставить под заголовок
                        region_title.SetFormatMode(parentModule.FORMAT_CENTRE_HORIZ)
                        region_title.SetFont(Shape_.titleFont)
                        Shape_.AddRegion(region_title)
                    else:
                        for line_txt in title.split('\n'):
                            Shape_.AddText(line_txt)
            # Текст
            if 'text' in attrs:
                text = attrs['text']
                if text:
                    if is_divided_shape:
                        region_text = parentModule.ShapeRegion()
                        region_text.SetName('text')
                        region_text.SetText(text)
                        if attrs.get('text2', None):
                            region_text.SetProportions(0.0, 0.4)    # Оставшееся оставить под текст
                        else:
                            region_text.SetProportions(0.0, 0.7)
                        region_text.SetFormatMode(parentModule.FORMAT_NONE)
                        region_text.SetFont(Shape_.textFont)
                        Shape_.AddRegion(region_text)
                    else:
                        for line_txt in text.split('\n'):
                            Shape_.AddText(line_txt)
            # Описание
            if 'text2' in attrs:
                text2 = attrs['text2']
                if text2:
                    if is_divided_shape:
                        region_descr = parentModule.ShapeRegion()
                        region_descr.SetName('text2')
                        region_descr.SetText(text2)
                        region_descr.SetProportions(0.0, 0.3)   # Оставшееся оставить под текст
                        region_descr.SetFormatMode(parentModule.FORMAT_NONE)
                        font = region_descr.GetFont()
                        region_descr.SetFont(Shape_.text2Font)
                        Shape_.AddRegion(region_descr)

            if is_divided_shape:
                Shape_.SetRegionSizes()
                Shape_.ReformatRegions(self)

        return Shape_

    def addShape(self, **attrs):
        """
        Добавить на канву новую фигуру.
        """
        shape = self.createShape(**attrs)
        if shape:
            # Если фигура определена, то установить ее свойства
            self.setShapeProperties(shape, **attrs)

            # Установить фигуру на диаграмме
            self.diagram.AddShape(shape)
            shape.Show(True)

            evt_handler = icShapeEvtHandler()
            evt_handler.SetShape(shape)
            evt_handler.SetPreviousHandler(shape.GetEventHandler())
            shape.SetEventHandler(evt_handler)

            # Зарегистрировать фигуру в списке фигур диаграммы
            shape_name = None
            if 'name' in attrs:
                shape_name = str(attrs['name'])
            self.shapes[shape_name] = shape
        return shape

    def createLine(self, **attrs):
        """
        Создать новую линию.
        """
        line = parentModule.LineShape()
        return line

    def findShape(self, ShapeName_):
        """
        Найти объект фигуры по его уникальному имени.
        """
        return self.shapes.get(ShapeName_, None)

    def setLineProperties(self, Line_, **attrs):
        """
        Установить свойства линии.
        """
        if Line_:
            # Сначала определить фигуры, которые связывает линия
            # если фигур нет, то не нужна и линия
            fromShape = None
            if 'from' in attrs:
                from_shape_name = attrs['from']
                fromShape = self.findShape(from_shape_name)

            toShape = None
            if 'to' in attrs:
                to_shape_name = attrs['to']
                toShape = self.findShape(to_shape_name)

            if fromShape and toShape:
                Line_.SetCanvas(self)

                # Перо
                if 'pen' in attrs:
                    pen = attrs['pen']
                    if type(pen) in (str, unicode):
                        # Перо задано строковым значением
                        pen = eval(pen, globals(), locals())
                    Line_.SetPen(pen)

                # Заливка
                if 'brush' in attrs:
                    brush = attrs['brush']
                    if type(brush) in (str, unicode):
                        # Заливка задана строковым значением
                        brush = eval(brush, globals(), locals())
                    Line_.SetBrush(brush)

                # Стрелка
                if 'arrow' in attrs:
                    arrow = attrs['arrow']
                    if type(arrow) in (str, unicode):
                        # Стрелка задана строковым значением
                        arrow = eval(arrow, globals(), locals())
                    Line_.AddArrow(arrow)

                Line_.MakeLineControlPoints(2)

                fromShape.AddLine(Line_, toShape)

        return Line_

    def addLine(self, **attrs):
        """
        Добавить на канву новую линию.
        """
        line = self.createLine(**attrs)
        if line:
            # Если линия определена, то установить ее свойства
            self.setLineProperties(line, **attrs)

            # Установить линию на диаграмме
            self.diagram.AddShape(line)
            line.Show(True)

            # Зарегистрировать фигуру в списке фигур диаграммы
            line_name = None
            if 'name' in attrs:
                line_name = str(attrs['name'])
            self.lines[line_name] = line
        return line

    def setDiagram(self, Diagram_):
        """
        Установить диаграмму.
        """
        # Сначала удалить все объекты предыдущей диаграммы
        self.diagram.DeleteAllShapes()
        self.shapes = dict()
        self.lines = dict()

        # Данные диаграммы
        self.diagram_res = Diagram_

        if self.diagram_res:
            return self.addDiagram(self.diagram_res)
        return None

    def _genLineName(self, Line_):
        """
        Генерация имени линии по ее данным.
        @param Line_: Данные, описывающие линию.
        """
        if 'name' in Line_:
            return Line_['name']
        elif ('name' not in Line_) and \
             ('from' in Line_ and 'to' in Line_):
            return Line_['from'] + '->' + Line_['to']
        from ic.utils import ic_uuid
        return ic_uuid.get_uuid()

    def addDiagram(self, Diagram_, ReCreate_=False):
        """
        Добавить диаграмму.
        @param Diagram_: Словарно-списковая структура диаграммы.
        @param ReCreate_: Пересоздать элементы, если они уже есть?
        """
        shapes = list()
        if 'shapes' in Diagram_:
            shapes = Diagram_['shapes']

        lines = list()
        if 'lines' in Diagram_:
            lines = Diagram_['lines']

        # Добавить фигуры
        for shape in shapes:
            if shape['name'] not in self.shapes or ReCreate_:
                self.addShape(**shape)

        # Добавить линии
        for line in lines:
            if 'name' not in line:
                line['name'] = self._genLineName(line)
            if line['name'] not in self.lines or ReCreate_:
                self.addLine(**line)

    def _obj2str_analog(self, Obj_, ObjList_, ObjStrList_):
        """
        Преобразование объектов в текстовое представление.
        """
        if Obj_ in ObjList_:
            i = ObjList_.index(Obj_)
            return ObjStrList_[i]
        # Если все таки нельзя преобразовать объект то вернуть его
        return Obj_

    def _getLineRes(self, Line_):
        """
        Получить словарь ресурса линии из объекта.
        Линия диаграммы - словарь формата:
            {
                'type': Тип линии/имя класса,
                'from': Идентификатор фигуры от которой направлена линия,
                'to': Идентификатор фигуры к которой направлена линия,
                'pen': Перо (см. Перья),
                'brush': Заливка (см. Заливки),
                'arrow': Стрелка  (см. Стрелки),
            }
        """
        type = Line_.GetClassName()
        pen = self._obj2str_analog(Line_.GetPen(), IC_PEN_LIST, IC_PEN_STR_LIST)
        brush = self._obj2str_analog(Line_.GetBrush(), IC_BRUSH_LIST, IC_BRUSH_STR_LIST)
        arrow = self._obj2str_analog(Line_.GetArrows()[0]._GetType(), IC_ARROW_LIST, IC_ARROW_STR_LIST)
        from_shape = Line_.GetFrom()
        to_shape = Line_.GetTo()
        line_res = {'type': type,
                    'from': from_shape.id,
                    'to': to_shape.id,
                    'pen': pen,
                    'brush': brush,
                    'arrow': arrow}
        return line_res

    def _getDividedShapeRes(self, Shape_):
        """
        Получить ресурс фигуры из объекта фигуры.
        Фигура диаграммы - словарь формата:
            {
                'type': Тип фигуры,
                'name': Наименование/Идентификатор фигуры,
                'pos': Позиция (x, y) на диаграмме,
                'size': Размер (width, height),
                'pen': Перо,
                'brush': Заливка,
                'title': Заголовок,
                'text': Текст описания,
            }
        """
        type = Shape_.GetClassName()
        name = Shape_.id
        x = Shape_.GetX()
        y = Shape_.GetY()
        width = Shape_.GetWidth()
        height = Shape_.GetHeight()
        pen = self._obj2str_analog(Shape_.GetPen(), IC_PEN_LIST, IC_PEN_STR_LIST)
        brush = self._obj2str_analog(Shape_.GetBrush(), IC_BRUSH_LIST, IC_BRUSH_STR_LIST)

        title_id = Shape_.FindRegion('title')[1]
        title = ''
        if title_id >= 0:
            region = Shape_._regions[title_id]
            title = region.GetText()

        text_id = Shape_.FindRegion('text')[1]
        text = ''
        if text_id >= 0:
            region = Shape_._regions[text_id]
            text = region.GetText()

        shape_res = {'type': type,
                     'name': name,
                     'pos': (x, y),
                     'size': (width, height),
                     'pen': pen,
                     'brush': brush,
                     'title': title,
                     'text': text}
        return shape_res

    def getDiagram(self):
        """
        Получить диаграмму из объектов OGL.
        Диаграмма - словарь формата:
            {'shapes': [Список фигур диаграммы],
             'liines': [Список линий диаграммы]}
        """
        diagram_res = {'shapes': [], 'lines': []}
        diagram = self.GetDiagram()

        shapes = diagram.GetShapeList()
        for shape in shapes:
            if issubclass(shape.__class__, parentModule.LineShape):
                # Заполнение линий
                shape_res = self._getLineRes(shape)
                diagram_res['lines'].append(shape_res)
            elif issubclass(shape.__class__, icDividedShape):
                # Заполнение фигур
                shape_res = self._getDividedShapeRes(shape)
                diagram_res['shapes'].append(shape_res)

        return diagram_res

    def getSelectedShape(self):
        """
        Текущая выделенная фигура.
        """
        return self.selected_shape

    #   Обработчики событий
    def getOnShapeDblClick(self):
        """
        Обработчик двойного клика на фигуре.
        """
        return self.getICAttr('on_shape_dbl_click')

    #   Свойства
    def isDraggable(self):
        """
        Можно перемещать фигуры по полю?
        """
        return self.getICAttr('is_draggable')


def test():
    """
    Функция тестирования.
    """
    diagram = {
        'shapes': [{'type': 'icDividedShape', 'name': 'test4', 'title': u'Заголовок по русски', 'text': u'Текст4', },
                   {'type': 'icDividedShape', 'name': 'test2', 'title': u'Заголовок по русски 2', 'text': u'Текст 2', 'text2': u'Текст 2.2', 'pen': 'CYAN_PEN', 'brush': 'LIGHT_GREY_BRUSH'},
                   {'type': 'icDividedShape', 'name': 'test3', 'title': u'Заголовок по русски 3', 'text': u'Текст 3 просто охренеть какой длинный текст по русски вот!', 'pen': 'GREY_PEN', 'brush':'CYAN_BRUSH'},
                   {'type': 'icDividedShape', 'name': 'test1', 'title': u'Заголовок по русски', 'text': u'Текст', 'pen': 'RED_PEN', 'brush': 'BLUE_BRUSH'}, ],
        'lines': [{'name': 'line1', 'from': 'test1', 'to': 'test2', 'pen': 'BLACK_DASHED_PEN', 'brush': 'MEDIUM_GREY_BRUSH', 'arrow': 'ARROW_ARROW'},
                  {'name': 'line2', 'from': 'test1', 'to': 'test3', 'pen': 'BLACK_PEN', 'brush': 'BLACK_BRUSH', 'arrow': 'ARROW_HOLLOW_CIRCLE'},
                  {'name': 'line3', 'from': 'test4', 'to': 'test1', 'pen': 'BLACK_PEN', 'brush': 'BLACK_BRUSH', 'arrow': 'ARROW_HOLLOW_CIRCLE'}, ],
                }

    app = wx.PySimpleApp()
    form = wx.Frame(None, size=wx.Size(800, 500))
    sizer = wx.BoxSizer(wx.VERTICAL)
    btn = wx.Button(form, -1, label='TEST')
    sizer.Add(btn)
    ogl_view = icSimpleOGLViewer(form, -1)
    sizer.Add(ogl_view, 1, wx.EXPAND | wx.GROW)
    ogl_view.setDiagram(diagram)
    ogl_view.shapes['test1'].SetY(250)
    ogl_view.diagram.ShowAll(True)

    def on_test_button(event):
        """
        """
        print(u'Debug: %s' % ogl_view.getDiagram())
        event.Skip()

    btn.Bind(wx.EVT_BUTTON, on_test_button)

    form.SetSizer(sizer)
    form.SetAutoLayout(True)
    sizer.FitInside(form)

    form.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()

