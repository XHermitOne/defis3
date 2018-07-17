#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Контрол конструктора ярусов.
"""

import os
import os.path
import wx

from . import wms_shape
from . import board

from ic.bitmap import ic_bmp
from ic.log import log

__version__ = (0, 0, 1, 2)

DEFAULT_SHAPE_POS = None

# Типы фигур располагаемых в конструкторе яруса
BOX_SHAPE_TYPE = 'box'

# Словарь соответствий типов фигур их классам
SHAPE_TYPES = {BOX_SHAPE_TYPE: wms_shape.icWMSBoxShape}


class icWMSTierContructorCtrl(wx.ScrolledWindow):
    """
    Контрол конструктора ярусов.
    """

    def __init__(self, parent, ID=-1):
        """
        Конструктор.
        @param parent: Родительское wx.Window окно.
        @param ID: Идентификатор wx.ID.
        """
        wx.ScrolledWindow.__init__(self, parent, ID)

        # Фигуры для отрисовки
        self.shapes = []
        self.dragImage = None
        self.dragShape = None
        self.hiliteShape = None

        # Количество ярусов
        self.tier_count = 0
        # Доски размещения
        self.boards = list()

        # Курсор стрелка
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))

        # Фон
        self.bg_bmp = None
        self.SetBackgroundStyle(wx.BG_STYLE_ERASE)

        # Всплывающее окно для отображения доп информации
        self.popup_win = None

        # Выбранная точка в конструкторе яруса
        self._selected_point = None

        # Объект обновляемый по выбору фигуры
        self.refresh_selected_obj = None

        # Дополнительная функция проверки возможности перемещения фигуры
        self.can_move_to_func = None

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)

    def setCanMoveToFunc(self, can_move_to_func=None):
        """
        Установить дополнительную функцию проверки возможности перемещения фигуры.
        ВНИМАНИЕ! В качестве аргументтов функция принимает:
            x, y - координаты размещения фигуры
            constructor - конструктор яруса.
            shape - перемещаемая фигура.
            Возвращает:
            True - можно перемещать фигуру
            False - нельзя перемещать фигуру
        @param can_move_to_func: Дополнительная функция проверки возможности перемещения фигуры.
        """
        self.can_move_to_func = can_move_to_func

    def getBoard(self, idx=0):
        """
        Обект доски размещения.
        @param idx: Номер доски размещения
        @return: Объект доски размещения.
        """
        if idx < 0:
            idx = 0
        if idx >= len(self.boards):
            idx = len(self.boards)-1
        if self.boards:
            return self.boards[idx]
        return None

    def setBackgroundBmp(self, background_bitmap=None):
        """
        Установить картинку фона.
        @param background_bitmap: Объект картинки wx.Bitmap.
        Может задаваться прсто именем файла.
        """
        if isinstance(background_bitmap, wx.Bitmap):
            self.bg_bmp = background_bitmap
        elif type(background_bitmap) in (str, unicode):
            # Задается именем файла
            bmp = ic_bmp.createBitmap(background_bitmap)
            self.bg_bmp = bmp
        elif background_bitmap is None:
            self.bg_bmp = None
        else:
            log.warning(u'Не обрабатываемый тип входных данных <%s>' % type(background_bitmap))

    def deleteBoard(self, idx=-1):
        """
        Удалить доску.
        @param idx: Идекс доски.
        @return: True/False.
        """
        try:
            del self.boards[idx]
            return True
        except:
            log.fatal(u'Ошибка удаления доски с индексом <%s>' % idx)
        return False

    def deleteBoards(self):
        """
        Удалить все доски.
        @return: True/False.
        """
        self.boards = list()
        return True

    def appendBoard(self, new_board, *args, **kwargs):
        """
        Добавить доску размещения. Сколько досок столько и ярусов.
        @param new_board: Объект доски размещения.
        """
        if board:
            if isinstance(new_board, board.icWMSBoard):
                new_board.setConstructor(self)
                # Доска задается как объект
                self.boards.append(new_board)
            elif isinstance(new_board, list):
                # Доска задается как схема размещения
                new_board = board.icWMSBoard(new_board, constructor=self,
                                             *args, **kwargs)
                self.boards.append(new_board)
            self.tier_count = len(self.boards)
        else:
            log.warning(u'Не определен объект доски размещения')

    def findFreeCell(self):
        """
        Поиск свободной ячейки на досках расположения.
        @return: Объект board.icWMSCell или None, если
        не найдено ни одной свободной ячейки.
        """
        cell = None
        for board_obj in self.boards:
            cell = board_obj.findFreeCell()
            if cell:
                break
        return cell

    def getCell(self, x, y, board_idx=0):
        """
        Поиск ячейки на доске расположения по позиции.
        @param x: Позиция ячейки X.
        @param y: Позиция ячейки Y.
        @param board_idx: Индекс доски расположения.
        @return: Объект board.icWMSCell или None, если
        не найдено ни одной ячейки.
        """
        board_obj = self.boards[board_idx]
        cell = board_obj.find_cell(x, y)
        return cell

    def getCellByIdx(self, cell_idx, board_idx=0):
        """
        Поиск ячейки на доске расположения по позиции.
        @param cell_idx: Индекс ячейки.
        @param board_idx: Индекс доски расположения.
        @return: Объект board.icWMSCell или None, если
            не найдено ни одной ячейки.
        """
        board_obj = self.boards[board_idx]
        cell = board_obj.getCell(cell_idx)
        return cell

    def deleteShapes(self):
        """
        Удалить фигуры.
        @return: True/False
        """
        self.shapes = []

        # И ссылки во всех досках
        for board in self.boards:
            for cell in board.cells:
                if cell:
                    cell.shape = None
        return True

    def appendShape(self, shape_type=BOX_SHAPE_TYPE,
                    pos_x=-1, pos_y=-1, tag=None):
        """
        Добавление новой фигуры.
        ВНИМАНИЕ! Если координата первого размещения фигуры не
        указана (т.е. (-1, -1)), то размещение происходит
        в первую свободную ячейку.
        @param shape_type: Идентификатор типа фигуры.
        @param pos_x: Координата X первого размещения фигуры.
        @param pos_y: Координата Y первого размещения фигуры.
        @param tag: Тег прикрепляемый к фигуре.
        Тег - дополнительный параметр идентификации фигуры.
        @return: True/False.
        """
        # Фигура
        shape_class = SHAPE_TYPES.get(shape_type, None)
        if shape_class:
            shape = shape_class(tag=tag)
            if pos_x >= 0 and pos_y >= 0:
                # По координатное добавление
                shape.pos = (pos_x, pos_y)
                shape.size = (board.DEFAULT_CELL_WIDTH,
                              board.DEFAULT_CELL_HEIGHT)
                cell = self.getCell(pos_x, pos_y)
                # is_add = True
            else:
                # Добавление в свободные ячейки
                # Найти свободную ячейку и поставить в нее фигуру
                cell = self.findFreeCell()
            # Указать для фигуры ячейку размещения
            if cell:
                is_add = shape.setCell(cell)
            else:
                is_add = False
                log.warning(u'Не найдена ячейка <%s : %s> размещения для фигуры' % (pos_x, pos_y))

            if is_add:
                self.shapes.append(shape)
                self.refreshShapes()
            return True
        else:
            log.warning(u'Не определенный тип <%s> фигуры конструктора яруса' % shape_type)
        return False

    def getTierCount(self):
        """
        Количество ярусов.
        """
        return self.tier_count

    def OnLeaveWindow(self, event):
        """
        We're not doing anything here, but you might have reason to.
        for example, if you were dragging something, you might elect to
        'drop it' when the cursor left the window.
        """
        pass

    def drawBackground(self, dc, x=0, y=0):
        """
        Отрисовка фона.
        @param dc: Контекст устройства виджета.
        @param x: Координата X.
        @param y: Координата Y.
        """
        dc.DrawBitmap(self.bg_bmp, x, y)

    def DrawShapes(self, dc):
        """
        Go through our list of shapes and draw them in whatever place they are.
        """
        for shape in self.shapes:
            if shape.shown:
                # print 'draw', dc
                shape.Draw(dc)

    def FindShape(self, point):
        """
        This is actually a sophisticated 'hit test', but in this
        case we're also determining which shape, if any, was 'hit'.
        Поиск фигуры по точке.
        @param point: Точка.
        @return: Объект фигуры
        """
        for shape in self.shapes:
            if shape.HitTest(point):
                return shape
        return None

    def refreshSelected(self, selected_point=None, mouse_pressed=wx.MOUSE_BTN_LEFT):
        """
        Обновить информацию о выделенной фигуре в другом объекте.
        ВНИМАНИЕ! Объект д.б. определен в конструкторе яруса
            и у этого объекта д.б. метод refreshSelected.
        @param selected_point: Выбранная точка.
        @param mouse_pressed: Код нажатой кнопки мыши.
        """
        if self.refresh_selected_obj and hasattr(self.refresh_selected_obj, 'refreshSelected'):
            # Просто передаем управление методу другого объекта
            self.refresh_selected_obj.refreshSelected(selected_point, mouse_pressed=mouse_pressed)

    def OnEraseBackground(self, event):
        """
        Clears the background, then redraws it. If the DC is passed, then
        we only do so in the area so designated. Otherwise, it's the whole thing.
        """
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        self.drawBackground(dc)

    def refreshShapes(self):
        """
        Перерисовка всех фигур.
        """
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        for board_obj in self.boards:
            board_obj.draw(dc)
        self.DrawShapes(dc)

    def OnPaint(self, event):
        """
        Fired whenever a paint event occurs
        """
        self.refreshShapes()

    def OnLeftDown(self, event):
        """
        Left mouse button is down.
        """
        self._selected_point = event.GetPosition()
        self.refreshSelected(self._selected_point, wx.MOUSE_BTN_LEFT)

        # Did the mouse go down on one of our shapes?
        shape = self.FindShape(self._selected_point)

        # If a shape was 'hit', then set that as the shape we're going to
        # drag around. Get our start position. Dragging has not yet started.
        # That will happen once the mouse moves, OR the mouse is released.
        if shape:
            self.dragShape = shape
            self.dragStartPos = self._selected_point

        event.Skip()

    def OnRightDown(self, event):
        """
        Обработчик клика правой кнопки мыши.
        """
        self._selected_point = event.GetPosition()
        self.refreshSelected(self._selected_point, wx.MOUSE_BTN_RIGHT)

        event.Skip()

    def showShapeTagInfo(self, shape, x=-1, y=-1):
        """
        Отобразить дополнительные данные о фигуре в всплывающем окне.
        По умолчанию всплывающее окно отображается под фигурой.
        @param shape: Объект фигуры.
        @param x: Координата X вывода всплывающего окна.
        Если -1, то береться left.
        @param y: Координата Y вывода всплывающего окна.
        Если -1, то береться top.
        """
        if shape is None:
            return

        x_offset, y_offset = self.ClientToScreen((0, 0))
        if x <= 0:
            x = shape.pos[0] + x_offset
        if y <= 0:
            y = shape.pos[1] + y_offset

        txt = shape.getTagInfo()
        if self.popup_win is None:
            self.popup_win = wx.PopupWindow(self, wx.SIMPLE_BORDER)
            panel = wx.Panel(self.popup_win)
            panel.SetBackgroundColour('CADET BLUE')

            static_txt = wx.StaticText(panel, -1, txt, pos=(10, 10))

            size = static_txt.GetBestSize()
            self.popup_win.SetSize((size.width+20, size.height+20))
            panel.SetSize((size.width+20, size.height+20))

            height = shape.size.height if isinstance(shape.size, wx.Size) else shape.size[1]
            self.popup_win.Position(wx.Point(x, y), (0, height))
            self.popup_win.Show()

    def hideShapeTagInfo(self):
        """
        Скрыть дополнительные данные о фигуре в всплывающем окне.
        """
        if self.popup_win:
            self.popup_win.Show(False)
            self.popup_win = None

    def find_cell(self, x, y):
        """
        Найти ячейку по точке.
        Поиск производится по всем доскам расположения.
        @param x: Координата x проверяемой точки.
        @param y: Координата y проверяемой точки.
        @return: Объект ячейки, в которую попадает точка (x, y).
            None если ячейка не найдена.
        """
        find_cell = None
        for board_obj in self.boards:
            find_cell = board_obj.find_cell(x, y)
            if find_cell:
                break
        return find_cell

    def replaceCells(self, src_cell, dst_cell):
        """
        Поменять местами содержимое ячеек.
        @param src_cell: Ячейка - источник.
        @param dst_cell: Ячейка - получатель
        @return: True - перемещение прошло успешно / 
            False - перемещение не прошло по какой-либо ошибке.
        """
        src_shape = src_cell.getShape()
        dst_shape = dst_cell.getShape()
        try:
            new_point = (dst_shape.pos[0], dst_shape.pos[1])
            src_can_move = self.can_move_to_func(x=new_point[0], y=new_point[1],
                                                 constructor=self, shape=src_shape) if self.can_move_to_func else True
            new_point = (src_shape.pos[0], src_shape.pos[1])
            dst_can_move = self.can_move_to_func(x=new_point[0], y=new_point[1],
                                                 constructor=self, shape=dst_shape) if self.can_move_to_func else True
            can_move = src_can_move and dst_can_move
        except:
            log.fatal(u'Ошибка дополнительной функции проверки возможности перемещения фигуры.')
            can_move = True

        if dst_cell and can_move:
            # Если по этим координатам есть такая ячейка
            # то расположить там фигуру
            src_shape.setCell(dst_cell)
            return True
        return False

    def OnLeftUp(self, event):
        """
        Left mouse button up.
        """
        if not self.dragImage or not self.dragShape:
            self.dragImage = None
            self.dragShape = None
            return

        # Hide the image, end dragging, and nuke out the drag image.
        self.dragImage.Hide()
        self.dragImage.EndDrag()
        self.dragImage = None

        if self.hiliteShape:
            self.RefreshRect(self.hiliteShape.GetRect())
            self.hiliteShape = None

        # reposition and draw the shape

        # Note by jmg 11/28/03
        # Here's the original:
        #
        # self.dragShape.pos = self.dragShape.pos + event.GetPosition() - self.dragStartPos
        #
        # So if there are any problems associated with this, use that as
        # a starting place in your investigation. I've tried to simulate the
        # wx.Point __add__ method here -- it won't work for tuples as we
        # have now from the various methods
        #
        # There must be a better way to do this :-)
        #

        new_point = (self.dragShape.pos[0] + event.GetPosition()[0] - self.dragStartPos[0],
                     self.dragShape.pos[1] + event.GetPosition()[1] - self.dragStartPos[1])
        find_cell = self.find_cell(new_point[0], new_point[1])

        try:
            can_move = self.can_move_to_func(x=new_point[0], y=new_point[1],
                                             constructor=self, shape=self.dragShape) if self.can_move_to_func else True
        except:
            log.fatal(u'Ошибка дополнительной функции проверки возможности перемещения фигуры.')
            can_move = True

        dst_shape = None
        if find_cell and can_move:
            # Если по этим координатам есть такая ячейка
            # то расположить там фигуру
            dst_shape = find_cell.shape
            self.dragShape.setCell(find_cell)

        self.dragShape.shown = True
        self.RefreshRect(self.dragShape.GetRect())
        # Если происходит подмена фигуры, то  обновить и подменяемую фигуру
        if dst_shape:
            self.RefreshRect(dst_shape.GetRect())

        self.dragShape = None

        event.Skip()

    def OnMotion(self, event):
        """
        The mouse is moving
        """
        # Ignore mouse movement if we're not dragging.
        if not self.dragShape or not event.Dragging() or not event.LeftIsDown():
            return

        # if we have a shape, but haven't started dragging yet
        if self.dragShape and not self.dragImage:

            # only start the drag after having moved a couple pixels
            tolerance = 2
            pt = event.GetPosition()
            dx = abs(pt.x - self.dragStartPos.x)
            dy = abs(pt.y - self.dragStartPos.y)
            if dx <= tolerance and dy <= tolerance:
                return

            # refresh the area of the window where the shape was so it
            # will get erased.
            self.dragShape.shown = False
            self.RefreshRect(self.dragShape.GetRect(), True)
            self.Update()

            if self.dragShape.text:
                self.dragImage = wx.DragString(self.dragShape.text,
                                               wx.StockCursor(wx.CURSOR_HAND))
            else:
                self.dragImage = wx.DragImage(self.dragShape.bmp,
                                              wx.StockCursor(wx.CURSOR_HAND))

            hotspot = self.dragStartPos - self.dragShape.pos
            self.dragImage.BeginDrag(hotspot, self, self.dragShape.fullscreen)

            self.dragImage.Move(pt)
            self.dragImage.Show()

        # if we have shape and image then move it, posibly highlighting another shape.
        elif self.dragShape and self.dragImage:
            onShape = self.FindShape(event.GetPosition())
            unhiliteOld = False
            hiliteNew = False

            # figure out what to hilite and what to unhilite
            if self.hiliteShape:
                if onShape is None or self.hiliteShape is not onShape:
                    unhiliteOld = True

            if onShape and onShape is not self.hiliteShape and onShape.shown:
                hiliteNew = True

            # if needed, hide the drag image so we can update the window
            if unhiliteOld or hiliteNew:
                self.dragImage.Hide()

            if unhiliteOld:
                dc = wx.ClientDC(self)
                self.hiliteShape.Draw(dc)
                self.hiliteShape = None

            if hiliteNew:
                dc = wx.ClientDC(self)
                self.hiliteShape = onShape
                self.hiliteShape.Draw(dc, wx.INVERT)

            # now move it and show it again if needed
            self.dragImage.Move(event.GetPosition())
            if unhiliteOld or hiliteNew:
                self.dragImage.Show()

        event.Skip()


def test():
    """
    Функция тестирования.
    """
    app = wx.PySimpleApp()

    frame = wx.Frame(None)

    panel = icWMSTierContructorCtrl(frame)
    board_obj = board.icWMSBoard()
    board_obj.auto_build()
    panel.appendBoard(board_obj)

    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
