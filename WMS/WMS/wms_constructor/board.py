#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Управление доской расположения ящиков/боксов.
"""

import copy
import wx

DEFAULT_CELL_WIDTH = 48
DEFAULT_CELL_HEIGHT = 48

DEFAULT_BOARD_WIDTH = 480
DEFAULT_BOARD_HEIGHT = 480

DEFAULT_BOARD_BG_COLOUR = (128, 128, 128)

DEFAULT_CELL_BG_COLOUR = (255, 255, 255)
DEFAULT_CELL_BORDER_COLOUR = (64, 64, 64)


def init_colour(colour, default=None):
    """
    Инициализация цвета по входным параметрам.
    @param colour: Цвет в каком то виде.
    @param default: Значение по умолчанию в случае
        не определенном значении цвета.
    @return: Объект wx.Colour.
    """
    wx_colour = None

    if default is None:
        default = wx.WHITE

    if colour is None:
        wx_colour = wx.Colour(*default)
    elif type(colour) in (list, tuple):
        wx_colour = wx.Colour(*colour)
    else:
        # Цвет задается явно
        wx_colour = colour
    return wx_colour


class icWMSCell(object):
    """
    Ячейка размещения.
    """

    def __init__(self, left=-1, top=-1,
                 width=DEFAULT_CELL_WIDTH,
                 height=DEFAULT_CELL_HEIGHT,
                 bg_colour=None, border_colour=None,
                 idx=-1, board=None):
        """
        Конструктор.
        @param left: Координата x левой границы ячейки на доске размещения.
        @param top: Координата y верхней границы ячейки на доске размещения.
        @param width: Ширина ячейки в точках.
        @param height: Высота ячейки в точках.
        @param idx: Номер ячейки на доске размещения.
        @param board: Объект доски.
        """
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.background_colour = init_colour(bg_colour, DEFAULT_CELL_BG_COLOUR)
        self.border_colour = init_colour(border_colour, DEFAULT_CELL_BORDER_COLOUR)

        # Индекс ячейки на доске
        # -1 считается не определенным индексом
        self.index = idx

        # Фигура, привязанная к ячейке
        self.shape = None

        # Доска на которой располагается ячейка
        self.board = board

    def setIndex(self, idx):
        if idx < 0:
            idx = -1
        self.index = idx

    def getIndex(self):
        return self.index

    def getPoint(self):
        return self.left, self.top

    def getSize(self):
        return self.width, self.height

    def getWXPosition(self):
        return wx.Point(self.left, self.top)

    def getWXSize(self):
        return wx.Size(self.width, self.height)

    def point_in(self, x, y):
        """
        Проверка на попадание точки (x, y) в ячейку.
        @param x: Координата x проверяемой точки.
        @param y: Координата y проверяемой точки.
        @return: True - Точка попадает в ячейку. False - не попадает в ячейку.
        """
        # Параметры ячейки корректно проинициализированы?
        is_init = (self.left >= 0) and (self.top >= 0) and (self.width > 0) and (self.height > 0)
        return is_init and \
            ((x >= self.left) and (x < self.left+self.width)) and \
            ((y >= self.top) and (y < self.top+self.height))

    def draw(self, dc):
        """
        Отрисовка ячейки.
        @param dc: Контекст устройства для отрисовки.
        """
        if self.background_colour and self.border_colour:
            dc.SetPen(wx.Pen(self.border_colour, 0))
            dc.SetBrush(wx.Brush(self.background_colour, wx.SOLID))
            dc.DrawRectangle(self.left, self.top,
                             self.width, self.height)
            # Надпись номера ячейки
            dc.SetFont(wx.Font(pointSize=24, family=wx.FONTFAMILY_DEFAULT,
                       style=wx.FONTSTYLE_NORMAL,
                       weight=wx.FONTWEIGHT_LIGHT,
                       underline=False))
            dc.SetTextForeground(wx.LIGHT_GREY)
            txt = str(self.index+1)
            w, h = dc.GetTextExtent(txt)
            x = self.left + (self.width-w)/2
            y = self.top + (self.height-h)/2
            dc.DrawText(txt, x, y)

    def getNext(self):
        """
        Получить следующуя ячейку на доске.
        @return: Объект следующей ячейки или None, если ячейка последняя.
        """
        return self.board.getCell(self.index + 1) if self.board else None

    def getPrev(self):
        """
        Получить предыдущую ячейку на доске.
        @return: Объект предыдущей ячейки или None, если ячейка первая.
        """
        return self.board.getCell(self.index - 1) if self.board else None

    def getShape(self):
        """
        Фигура ячейки.
        """
        return self.shape


class icWMSBoard(object):
    """
    Доска расположения ячеек.
    """

    def __init__(self, cells=None, left=0, top=0,
                 width=DEFAULT_BOARD_WIDTH,
                 height=DEFAULT_BOARD_HEIGHT,
                 bg_colour=None, constructor=None):
        """
        Конструктор.
        @param cells: Список описаний ячеек.
            Формат:
            [{'left': 10, 'top': 10, 'width': 48, 'height': 48}, ...]
        @param left: Координата x левой границы доски размещения.
        @param top: Координата y верхней границы доски размещения.
        @param width: Ширина доски размещения в точках.
        @param height: Высота доски размещения в точках.
        @param bg_colour: Цвет фона доски.
        @param constructor: Объект конструктора, в котором расположена доска.
        """
        self.left = left
        self.top = top
        self.width = width
        self.height = height

        self.background_colour = init_colour(bg_colour, DEFAULT_BOARD_BG_COLOUR)

        if cells is None:
            cells = []
        self.cells = self.build(cells)

        self.constructor = constructor

    def setConstructor(self, constructor):
        """
        Объект конструктора, в котором расположена доска.
        """
        self.constructor = constructor

    def getConstructorOffset(self):
        """
        Определеить смещение доски размещения в конструкторе.
        @return: x смещение, y смещение.
        """
        if self.constructor:
            offset = self.constructor.ClientToScreen((0, 0))
            return offset
        # Если конструктор не определен считаем что смещение нулевое
        return 0, 0

    def build(self, cells):
        """
        Создание и инициализация объектов ячеек.
        @param cells: Список описаний ячеек.
            Формат:
            [{'left': 10, 'top': 10, 'width': 48, 'height': 48}, ...]
        @return: Список объектов ячеек.
        """
        assert isinstance(cells, list)

        result = list()
        for cell in cells:
            if 'board' not in cell:
                # Добавить в ячейку указатель на объект доски размещения
                cell['board'] = self
            new_cell = icWMSCell(**cell)
            result.append(new_cell)
        return result

    def deleteCells(self):
        """
        Удалить все ячейки.
        @return: True/False.
        """
        self.cells = list()
        return True

    def auto_build(self, cell_width=DEFAULT_CELL_WIDTH,
                   cell_height=DEFAULT_CELL_HEIGHT):
        """
        Автоматическое создание и инициализация объектов ячеек.
        Размещение ячеек производиться автоматом последовательно
        слева-направо сверху-вниз.
        @param cell_width: Ширина ячейки в точках.
        @param cell_height: Высота ячейки в точках.
        @return: Список объектов ячеек.
        """
        cells = list()
        w_cells_count = int(self.width/cell_width)
        h_cells_count = int(self.height/cell_height)
        for h in range(h_cells_count):
            top = self.top + h * cell_height
            for w in range(w_cells_count):
                left = self.left + w * cell_width
                cells.append(dict(left=left, top=top,
                                  width=cell_width,
                                  height=cell_height))
        self.cells = self.build(cells)
        return self.cells

    def draw(self, dc):
        """
        Отрисовка доски размещения.
        @param dc: Контекст устройства для отрисовки.
        """
        # Заполнить подложку фоном
        if self.background_colour:
            # dc.SetPen(wx.Pen(self.background_colour, 0))
            dc.SetBrush(wx.Brush(self.background_colour, wx.SOLID))
            dc.DrawRectangle(self.left, self.top,
                             self.width, self.height)

        # Отрисовка ячеек
        for cell in self.cells:
            if cell:
                cell.draw(dc)

    def find_cell(self, x, y):
        """
        Найти ячейку по точке.
        @param x: Координата x проверяемой точки.
        @param y: Координата y проверяемой точки.
        @return: Объект ячейки, в которую попадает точка (x, y).
            None если ячейка не найдена.
        """
        find_cell = None
        for cell in self.cells:
            if cell.point_in(x, y):
                find_cell = cell
                break
        return find_cell

    def findFreeCell(self):
        """
        Поиск свободной ячейки на доске расположения.
        @return: Объект board.icWMSCell или None, если
        не найдено ни одной свободной ячейки.
        """
        find_cell = None
        for cell in self.cells:
            if cell.shape is None:
                find_cell = cell
                break
        return find_cell

    def getShapeTags(self):
        """
        Получить список прикрепленных тегов к фигурам в ячейках.
        @return: Список тегов.
        """
        tags = list()
        for cell in self.cells:
            if cell and cell.shape:
                tag = copy.deepcopy(cell.shape.tag)
                pos_x, pos_y = cell.shape.pos
                tag['pos'] = (pos_x, pos_y)
                # Позицию необходимо пересчитать в зависимости от смещения
                tag['relative_pos'] = (pos_x - self.left, pos_y - self.top)
                tag['size'] = cell.shape.size
                tags.append(tag)
            else:
                tags.append(None)
        return tags

    def getCell(self, cell_idx):
        """
        Получить объект ячейки по индексу.
        @param cell_idx: Индекс ячейки.
        @return: Объект ячейки или None, если индекс ячейки не корректный.
        """
        if cell_idx < 0:
            return None
        elif cell_idx >= len(self.cells):
            return None
        return self.cells[cell_idx]


def test():
    """
    Функция тестирования.
    """
    app = wx.PySimpleApp()

    frame = wx.Frame(None)
    panel = wx.Panel(frame)

    board = icWMSBoard()
    board.auto_build()

    def on_paint(event):
        dc = wx.PaintDC(event.GetEventObject())
        dc.Clear()
        board.draw(dc)

    panel.Bind(wx.EVT_PAINT, on_paint)

    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
