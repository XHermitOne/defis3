#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс описания сложной шапки.

Модуль содержит описания класса сложной шапки для гридов, которая может
состоять из нескольких рядов ячеек (в том числе и объедененных). Шапка
сделана на основе контейнера wx.GridBagSizer.

:type ICHeadCellStyle: C{Dictionary}
:var ICHeadCellStyle: Описание стилей компонента (значения атрибута <style>):

    - B{wx.ALIGN_LEFT}: Выравнивает текст по левому краю.
    - B{wx.ALIGN_RIGHT}: Выравнивае текст по правому краю.
    - B{wx.ALIGN_CENTRE}: Выравнивает текст по центру.
    - B{wx.ST_NO_AUTORESIZE}: Отключает автоматический подбор размер компонента.

:type SPC_IC_HEADER: C{Dictionary}
:var SPC_IC_HEADER: Спецификация на описание сложной шапки. Описание ключей:

    - B{name='Head'}: Имя объекта.
    - B{type='Head'}: Тип объекта.
    - B{position=(-1,-1)}: Позиция на окне если используется как самостоятельный компонент.
    - B{size=(-1,-1)}: Размер компонента.
    - B{object_link=None}: Имя грида, к которому присоединяется шапка.
    - B{backgroundColor=None}: Цвет подложки.
    - B{foregroundColor=None}: Цвет текста.
    - B{font={}}: Шрифт (см. описание icFont).
    - B{child=[]}: Список описаний ячеек шапки.
"""

import wx

from ic.components import icwidget
from ic.utils import util

try:
    from . import icheadcell
except ImportError:
    import icheadcell

from ic.log import log
from ic.PropertyEditor import icDefInf

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

SPC_IC_HEADER = {'type': 'Header',
                 'name': 'default',
                 'child': [],

                 'position': (-1, -1),
                 'size': (-1, -1),
                 'backgroundColor': None,
                 'foregroundColor': None,
                 'font': {},
                 'alignment': ('left', 'middle'),

                 '__styles__': ic_class_styles,
                 '__parent__': icwidget.SPC_IC_WIDGET,
                 }

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------

#   Тип компонента. None, означает, что данный компонент убран из
#   редактора и остался только для совместимости со старыми проектами.
ic_class_type = icDefInf._icComboType

#   Имя пользовательского класса
ic_class_name = 'icHeader'

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_HEADER

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtHeader'
ic_class_pic2 = '@common.imgEdtHeader'

#   Путь до файла документации
ic_class_doc = 'ic/doc/_build/html/ic.components.custom.icheadergrid.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['HeadCell']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None   # ['Dialog', 'Frame', 'ToolBar', 'ToolBarTool', 'DatasetNavigator', 'GridCell']

#   Версия компонента
__version__ = (1, 1, 2, 1)


def sortCell(cell):
    """
    Функция сортировки ячеек.
    """
    return str(cell.span) + str(cell.position)


class icHeader(icwidget.icBase, wx.ScrolledWindow):
    """
    Класс описания сложной шапки.
    """

    def __init__(self, parent, id=-1, component={}, logType=0, evalSpace={},
                 bCounter=False, progressDlg=None):
        """
        Конструктор для создания объекта icBoxSizer.

        :type parent: C{wxWindow}
        :param parent: Указатель на родительское окно.
        :type id: C{int}
        :param id: Идентификатор окна.
        :type component: C{dictionary}
        :param component: Словарь описания компонента.
        :type logType: C{int}
        :param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        :param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        :type evalSpace: C{dictionary}
        """
        util.icSpcDefStruct(SPC_IC_HEADER, component)
        icwidget.icBase.__init__(self, parent, id, component, logType, evalSpace)
        pos = component['position']
        size = component['size']
        
        wx.ScrolledWindow.__init__(self, parent, id, pos, size, style=0)
        self.sz = wx.GridBagSizer(0, 0)
        
        self.SetClientSize(size)
        self.sz.SetEmptyCellSize((10, 1))
        self.SetSizer(self.sz)
            
        #   Обработчики событий
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_MOTION, self.onMove)
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.onLeftUp)

        #   Цвета текста и фона
        self.bgr = bgr = component['backgroundColor']
        self.fgr = fgr = component['foregroundColor']
        self.font = component['font']

        if bgr:
            self.SetBackgroundColour(bgr)

        if fgr:
            self.SetForegroundColour(bgr)
        #
        self.oldPosition = (0, 0)
        self.mv_pos = (0, 0)
        self.scroll_pos = (0, 0)

        #   Список параметров ячейки
        self.parAddList = []
        self.grid = None
        
        #   Выбранный объект
        self.selObj = None

        #   Максимальный номер строки и колонки
        self.maxRow = 0
        self.maxCol = 0
        
        #   Создаем дочерние компоненты
        self.childCreator(bCounter=bCounter, progressDlg=progressDlg)

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if 'child' in self.resource:
            kernel = self.GetKernel()
            kernel.parse_resource(self, self.resource['child'], None, context=self.evalSpace,
                                  bCounter=bCounter, progressDlg=progressDlg)

            for el in self.component_lst:
                self.addCell(el)

    def connectGrid(self, grid, bAuto=False, bHideOldHead=False):
        """
        Присоединяет грид к шапке.

        :type grid: C{icGrid}
        :param grid: Указатель на грид.
        :type bAuto: C{bool}
        :param bAuto: Признак автоматического создания стандартной шапки грида.
        :type bHideOldHead: C{bool}
        :param bHideOldHead: Признак скрытия старой шапки.
        """
        if not grid:
            return False
        
        self.grid = grid

        if bAuto:
            self.parAddList = []

            #   Устанавливаем новые размеры шапки
            w, h = self.GetClientSize()
                
            for col in range(grid.GetNumberCols()):
                label = grid.GetColLabelValue(col)
                size = (grid.GetColSize(col), h)
                cell = icheadcell.icHeadCell(self, -1,
                                             {'label': label, 'size': size,
                                              'position': (0, col),
                                              'span': (1, 1),
                                              'backgroundColor': self.bgr,
                                              'foregroundColor': self.fgr,
                                              'font': self.font,
                                              'isSort': 1})
                self.addCell(cell)

        #   По необходимости старую шапку скрываем
        if bHideOldHead:
            grid.SetColLabelSize(0)
                
        return True
    
    def setViewStart(self, x, y):
        """
        Подстраивает шапку под грид при наличии горизонтальной и вертикальной прокрутки.

        :type x: C{int}
        :param x: X координата, с которой начинается видимая область грида.
        :type y: C{int}
        :param y: Y координата, с которой начинается видимая область грида.
        """
        oldx, oldy = self.scroll_pos

        dx = oldx - x
        dy = oldy - y
        
        self.scroll_pos = (x, y)
        self.ScrollWindow(dx, dy)

    def addCell(self, cell):
        """
        Функция добавляет ячейку заголовока.

        :type cell: C{string}
        :param cell: Компонент ячейки.
        """

        if cell.position == (-1, -1):
            pos = (0, len(self.parAddList))
        else:
            pos = cell.position
            
        try:
            self.sz.Add(cell, pos, cell.span, cell.add_style)
        except:
            log.fatal(u'Ошибка добавления ячейки в сайзер')
            
        self.parAddList.append(cell)
        # self.parAddList.sort(sortCell)
        self.parAddList = sorted(self.parAddList, key=sortCell)
        self.sz.Layout()

    def getMaxRow(self):
        """
        Определяе максимальный номер строки.
        """
        for obj in self.parAddList:
            row, col = obj.position
                
            if row > self.maxRow:
                self.maxRow = row

        return self.maxRow
    
    def getMaxCol(self):
        """
        Определяе максимальный номер колонки.
        """
        for obj in self.parAddList:
            row, col = obj.position

            if col > self.maxCol:
                self.maxCol = col
                
        return self.maxCol

    def findCell(self, row, col):
        """
        Возвращает по заданным координатам объект, который в ней находится.

        :type row: C{int}
        :param row: Номер ряда.
        :type col: C{int}
        :param col: Номер колонки.
        """
        for obj in self.parAddList:
            _row, _col = obj.position
            s_row, s_col = obj.span
            
            if (_row <= row <= _row + s_row - 1) and (_col <= col <= _col + s_col - 1):
                return obj
            
        return None

    def drawAll(self):
        """
        Перерисовывает все объекты помещенные в шапке.
        """
        dc = wx.ClientDC(self)
        
        for obj in self.parAddList:
            obj.draw(dc)

    def reconstruct(self):
        """
        Переконструирует шапку.
        """
        for obj in self.parAddList:
            obj_idx = self.parAddList.index(obj)
            if 0 <= obj_idx < self.sz.GetItemCount():
                self.sz.Remove(obj_idx)
            else:
                log.warning(u'Ошибка удаления ячейки шапки из сайзера. Индекс <%s>' % str(obj_idx))
        
        for indx, obj in enumerate(self.parAddList):

            if obj.size[0] == -1:
                obj.SetSize((10, obj.size[1]))
            else:
                obj.SetSize(obj.size)

            if obj.position == (-1, -1):
                pos = (0, indx)
            else:
                pos = obj.position

            try:
                self.sz.Add(obj, pos, obj.span, obj.add_style)
            except:
                log.warning(u'wxGridBagSize ячейка (%s : %s) занята' % (pos[0], pos[1]))

        self.sz.Layout()
        self.Refresh()

        if self.grid:
            vx, vy = self.grid.GetViewStart()
            dx, dy = self.grid.GetScrollPixelsPerUnit()
            self.ScrollWindow(-vx * dx, 0)
            self.scroll_pos = (vx * dx, 0)

    def onPaint(self, event):
        """
        Обрабатывает сообщение <EVT_PAINT>.
        """
        dc = wx.BufferedPaintDC(self)

        width, height = self.GetClientSize()
        if not width or not height:
            return

        clr = self.GetBackgroundColour()
        backBrush = wx.Brush(clr, wx.BRUSHSTYLE_SOLID)

        if wx.Platform == '__WXMAC__' and clr == self.defBackClr:
            # if colour is still the default then use the striped background on Mac
            # 1 == kThemeBrushDialogBackgroundActive
            #                     V
            backBrush.SetMacTheme(1)

        dc.SetBackground(backBrush)
        dc.SetTextForeground(self.GetForegroundColour())
        dc.Clear()
        dc.SetFont(self.GetFont())
        
    def drawDiv(self, dc, clr=(100, 100, 100)):
        """
        Рисует разделитель.

        :type dc: C{wx.DC}
        :param dc: Контекст устройства.
        :type clr: C{wx.Colour}
        :param clr: Цвет разделителя.
        """
        width, height = self.GetClientSize()
        pen = wx.Pen(clr)
        dc.SetPen(pen)
        x_p, y_p = self.mv_pos
        dc.DrawLine(x_p, 0, x_p, height)

    def eraseDiv(self, dc):
        """
        Чистит изображение разделителя.
        """
        clr = self.GetBackgroundColour()
        self.drawDiv(dc, clr)
        x, y = self.mv_pos
        
        for obj in self.parAddList:
            rect = obj.GetRect()
            
            if rect.x <= x and rect.x + rect.width >= x+1:
                dc_obj = wx.ClientDC(obj)
                obj.draw(dc_obj)
            
    def onLeftDown(self, event):
        """
        Обработка нажатия левой кнопки мыши <wx.EVT_LEFT_DOWN>.
        """
        x, y = self.oldPosition = event.GetPosition()
        
        for obj in self.parAddList:
            rect = obj.GetRect()

            #   Захватываем объект
            if rect.x + rect.width in [x, x+1]:
                self.selObj = obj
                return
            
    def onLeftUp(self, event):
        """
        Обработка отпускания левой кнопки мыши <wx.EVT_LEFT_UP>.
        """
        cursor = wx.StockCursor(wx.CURSOR_DEFAULT)
        self.SetCursor(cursor)
        dc = wx.ClientDC(self)
        self.eraseDiv(dc)

        # Если объект был захвачен, то изменяем его размеры и освобождаем
        # объект от захвата
        if self.selObj:
            x, y = event.GetPosition()
            sx, sy = self.selObj.GetSize()
            _x, _y = self.selObj.GetPosition()

            if x > _x:
                self.selObj.size = wx.Size(x - _x, sy)
                self.selObj.SetSize(self.selObj.size)
                self.reconstruct()
                
            self.selObj = None
            
    def DoGetBestSize(self):
        """
        """
        return self.GetSize()
        
    def onMove(self, event):
        """
        Обработка сообщения <wx.EVT_MOTION>.
        """
        x, y = event.GetPosition()
        width, height = self.GetClientSize()
        bEdge = False

        for obj in self.parAddList:
            rect = obj.GetRect()
            
            if rect.x + rect.width in [x, x+1]:
                cursor = wx.StockCursor(wx.CURSOR_SIZEWE)
                self.SetCursor(cursor)
                bEdge = True
                break
            
        if not bEdge and not event.Dragging():
            cursor = wx.StockCursor(wx.CURSOR_DEFAULT)
            self.SetCursor(cursor)

        if event.Dragging() and self.selObj:
            # Двигаем курсор
            dc = wx.ClientDC(self)
            self.eraseDiv(dc)
            self.mv_pos = (x, y)
            self.drawDiv(dc)
            
        event.Skip()


def test(par=0):
    """
    Тестируем класс icHeadCell.
    """
    from ic.components.ictestapp import TestApp
    import wx.grid
    app = TestApp(par)
    
    frame = wx.Frame(None, -1, 'icCell Test', size=(600, 350))
    panel = wx.Panel(frame, -1)
    panel.SetBackgroundColour((100, 180, 200))
    
    hx = 480
    bsz = wx.GridBagSizer(1, 1)

    panel.SetSizer(bsz)
   
    header = icHeader(panel, 0, {'position': (10, 10), 'size': (hx, 120),
                                 # 'backgroundColor': (200, 0, 0),
                                 'foregroundColor': (255, 0, 0)})

    sz_cell = (70, 20)

    cell = icheadcell.icHeadCell(header, 1,
                                 {'label': 'row- 1:0', 'size': (-1, -1),
                                  'position': (1, 0), 'span': (1, 2),
                                  # 'backgroundColor': (120, 170, 220),
                                  'backgroundType': 1})
    header.addCell(cell)
    cell = icheadcell.icHeadCell(header, 2,
                                 {'label': 'row- 2:0', 'size': sz_cell,
                                  'position': (2, 0), 'isSort': False,
                                  # 'backgroundColor': (120, 170, 220),
                                  'backgroundType': 1})
    header.addCell(cell)
    cell = icheadcell.icHeadCell(header, 3,
                                 {'label': 'row- 2:1', 'size': sz_cell,
                                  'position': (2, 1), 'isSort': False,
                                  # 'backgroundColor': (120, 170, 220),
                                  'backgroundType': 1})
    header.addCell(cell)
    cell = icheadcell.icHeadCell(header, 4,
                                 {'label': 'row- 2:2', 'size': sz_cell,
                                  'position': (2, 2), 'isSort': False,
                                  # 'backgroundColor': (120, 170, 220),
                                  'backgroundType': 1})
    header.addCell(cell)
    cell = icheadcell.icHeadCell(header, 5,
                                 {'label': 'row- 2:3', 'size': sz_cell,
                                  'position': (2, 3), 'isSort': False,
                                  # 'backgroundColor': (120, 170, 220),
                                  'backgroundType': 1})
    header.addCell(cell)
    cell = icheadcell.icHeadCell(header, -1,
                                 {'label': 'row- 2:4', 'size': sz_cell,
                                  'position': (2, 4),
                                  # 'backgroundColor': (120, 170, 220),
                                  'backgroundType': 1})
    header.addCell(cell)
    cell = icheadcell.icHeadCell(header, -1,
                                 {'label': 'row- 1:5', 'size': (-1, -1),
                                  'position': (1, 5),
                                  # 'backgroundColor': (120, 170, 220),
                                  'backgroundType': 1})
    header.addCell(cell)
    cell = icheadcell.icHeadCell(header, -1,
                                 {'label': 'row- 2:5', 'size': (70, 20),
                                  'position': (2, 5),
                                  # 'backgroundColor': (120, 170, 220),
                                  'backgroundType': 1})
    header.addCell(cell)
    cell = icheadcell.icHeadCell(header, -1,
                                 {'label': 'row- 1:2', 'size': (-1, 20),
                                  'position': (1, 2), 'span': (1, 3),
                                  # 'backgroundColor': (120, 170, 220),
                                  'backgroundType': 1})
    header.addCell(cell)
    cell = icheadcell.icHeadCell(header, -1,
                                 {'label': 'row- 0:0', 'size': (-1, 20),
                                  'position': (0, 0),
                                  'span': (1, 6),
                                  # 'backgroundColor': (120, 170, 220),
                                  'backgroundType': 1,
                                  'borderTopColor': (100, 100, 100)})
    header.addCell(cell)
    cell = icheadcell.icHeadCell(header, -1,
                                 {'label': 'row- 0:6\ntest', 'size': (70, 120),
                                  'position': (0, 6), 'span': (3, 1),
                                  'isSort': False,
                                  # 'backgroundColor': (120, 170, 220),
                                  'backgroundType': 3,
                                  'borderStep': 2})
    header.addCell(cell)
    bsz.Add(header, (0, 0), (1, 1), 0, wx.EXPAND)

    grid = wx.grid.Grid(panel)
    grid.CreateGrid(3, 7)
    bsz.Add(grid, (1, 0), (1, 1), 0, wx.EXPAND)

    header.connectGrid(grid)

    log.info(u'header.GetSize() = %s\t%s' % (header.GetSize(), header.size))
    frame.Show(True)

    app.MainLoop()


if __name__ == '__main__':
    test(0)
