#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для класса wx.BagGridSizer. Генерируется объект по ресурсному описанию.
Данный объект является контейнером для других визуальных компонентов.
Он выстраивает эти объекты в
виде таблицы и разрешает изменять размеры определенных колонках и рядах при изменении размеров
родительского окна.

@type SPC_IC_GRID_BAGSIZER: C{Dictionary}
@var SPC_IC_GRID_BAGSIZER: Спецификация на ресурсное описание компонента. Описание ключей:
    - B{name = 'DefaultName'}: Имя объекта.
    - B{type = 'BagGridSizer'}: Тип объекта.
    - B{flexCols = []}: Указываются номера колонок, размеры которых могут изменяться.
    - B{flexRows = []}: Указываются номера рядов, размеры которых могут изменяться.
    - B{vgap = 0}: Отступы между рядами.
    - B{hgap = 0}: Отступы между колонками.
    - B{minCellWidth = 10}: Минимальная ширина ячейки.
    - B{minCellHeight = 10}: Минимальная высота ячейки.
    - B{child=[]}: Описание добавляемых элементов в сайзер.
"""

import wx
from ic.utils.util import icSpcDefStruct
from ic.components.icwidget import icSizer, icParentShapeType, icSelectedShapeType, SPC_IC_SIZER
from ic.log.iclog import MsgLastError, LogLastError
import ic.PropertyEditor.icDefInf as icDefInf
from ic.kernel import io_prnt
import ic.imglib.common as common


SPC_IC_GRID_BAGSIZER = {'type': 'GridBagSizer',
                        'name': 'DefaultName',
                        'child': [],

                        'flexRows': [],
                        'flexCols': [],
                        'vgap': 0,
                        'hgap': 0,

                        'minCellWidth': 10,
                        'minCellHeight': 10,

                        '__attr_types__': {icDefInf.EDT_NUMBER: ['minCellWidth',
                                                                 'minCellHeight', 'hgap', 'vgap'],
                                           icDefInf.EDT_TEXTLIST: ['flexRows', 'flexCols'],
                                           },
                        '__parent__': SPC_IC_SIZER,
                        }

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------

#   Тип компонента
ic_class_type = icDefInf._icSizersType

#   Имя пользовательского класса
ic_class_name = 'icGridBagSizer'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_GRID_BAGSIZER
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtFlexGridSizer'
ic_class_pic2 = '@common.imgEdtFlexGridSizer'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.sizers.icgridbagsizer.icGridBagSizer-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = None

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = ['Dialog', 'Frame', 'ToolBarTool', 'Separator', 'GridCell']

#   Версия компонента
__version__ = (1, 0, 0, 4)


class icGridBagSizer(icSizer, wx.GridBagSizer):
    """
    Интерфейс к классу wx.BagGridSizer через ресурсное описание.
    """

    def __init__(self, parent, id=-1, component={}, logType=0, evalSpace={},
                 bCounter=False, progressDlg=None, sizer=None):
        """
        Конструктор для создания объекта icGridBagSizer.
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
        @type sizer: C{icSizer}
        @param sizer: Ссылка на родительский сайзер.
        """
        icSpcDefStruct(SPC_IC_GRID_BAGSIZER, component)
        #   Кортеж задающий вид прокутки (bHoriz, bVert)
        self.enableScr = None
        icSizer.__init__(self, parent, id, component, logType, evalSpace, sizer=sizer)
        self.vgap = component['vgap']
        self.hgap = component['hgap']
        wx.GridBagSizer.__init__(self, component['vgap'], component['hgap'])

        self.minCellWidth = w = component['minCellWidth']
        self.minCellHeight = h = component['minCellHeight']

        self.SetEmptyCellSize((w, h))

        #   Максимальный номер строки и колонки
        self.maxRow = 0
        self.maxCol = 0

        #   Размеры колонок и рядов
        self.sizeCols = []
        self.sizeRows = []
        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

        #   Устанавливаем колонки и ряды, которые подстраивают
        #   свои размеры под размеры родительского окна
        #   ВНИМАНИЕ! Эту операцию необходимо выполнять после
        #   добавления объектов в сайзер
        for col in component['flexCols']:
            try:
                self.AddGrowableCol(col)
            except:
                io_prnt.outLastErr('flexCols col=<%s>' % col)

        for row in component['flexRows']:
            self.AddGrowableRow(row)

        if parent:
            import ic.utils.graphicUtils as grph
            parent_bgr = parent.GetBackgroundColour()
            self.shape_clr = grph.AdjustColour2(parent_bgr, 7)
        else:
            self.shape_clr = icSizer.DESIGN_SHAPE_COLOR
            
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.child:
            if not self.evalSpace['_root_obj']:
                self.evalSpace['_root_obj'] = self
                parent = self.evalSpace['_main_parent'] or self
            else:
                parent = self.parent

            kernel = self.GetKernel()
            kernel.parse_resource(parent, self.child, self, context=self.evalSpace,
                                  bCounter=bCounter, progressDlg=progressDlg)
            try:
                if not self.parent_sizer:
                    parent.SetSizer(self)
                    parent.SetAutoLayout(1)
                    if self.enableScr:
                        parent.EnableScrolling(* self.enableScr)
                        self.SetVirtualSizeHints(parent)
            except:
                io_prnt.outErr(u'Ошибка при привязке сайзера')

            self.win_parent = parent
            # Добавляем в сайзер дочерние элементы
            for wxw in self.component_lst:
                self.Add(wxw, wxw.position, wxw.span, wxw.flag, wxw.border)
        
    def Add(self, obj, pos, span=(1, 1), flag = 0, border = 0):
        """
        Функция добавления в сайзер. Она переопределена для того, чтобы контролировать
        комопненты, которые добавляются, т. к. стандартные сайзеры этого делать не позволяют.
        """
        row, col = pos

        if row == -1:
            row = len(self.objectList)
            
        if col == -1:
            col = 0

        pos = (row, col)
        
        if obj.type == 'SizerSpace':
            bret = wx.GridBagSizer.Add(self, obj.size, pos, span, flag, border)
        else:
            bret = wx.GridBagSizer.Add(self, obj, pos, span, flag, border)

        if bret:
            obj.contaningSizer = self
            obj.span = span
            obj.position = pos
            obj.flag = flag
            obj.border = border
            obj.pt_dw = 0
            obj.pt_dh = 0
            
            self.objectList.append(obj)
        else:
            io_prnt.outLastErr('Error Add obj: <%s>' % obj)

        return bret

    def GetMaxRow(self):
        """
        Определяе максимальный номер строки.
        """
        self.maxRow = len(self.GetRowHeights())-1
        return self.maxRow
    
    def GetMaxCol(self):
        """
        Определяе максимальный номер колонки.
        """
        self.maxCol = len(self.GetColWidths())-1
        return self.maxCol

    def Reconstruct(self):
        """
        Переконструирует сайзер.
        """
        _list = self.objectList
        self.objectList = []
        
        for indx, obj in enumerate(_list):
            if not issubclass(obj.__class__, wx.Sizer):
                obj.size = obj.GetSize()
                self.Detach(obj)

        for indx, obj in enumerate(_list):
            if not issubclass(obj.__class__, wx.Sizer):
                if obj.size[0] == -1:
                    obj.SetSize((50, obj.size[1]))
                    
                obj.SetSize(obj.size)

                if obj.position == (-1, -1):
                    pos = (0, indx)
                else:
                    pos = obj.position

                try:
                    self.Add(obj, pos, obj.span, obj.flag, obj.border)
                    
                    if obj.span[0] == 1 and obj.span[1] == 1:
                        self.SetItemMinSize(obj, obj.size)
                    elif obj.flag != wx.EXPAND:
                        self.SetItemMinSize(obj, obj.size)
                except:
                    LogLastError('Reconstruct Error')
            else:
                self.objectList.append(obj)
                
        self.Layout()

    def FindCell(self, row, col):
        """
        Возвращает по заданным координатам объект, который в ней находится.
        @type row: C{int}
        @param row: Номер ряда.
        @type col: C{int}
        @param col: Номер колонки.
        """
        for obj in self.objectList:
            _row, _col = obj.position
            s_row, s_col = obj.span

            if (_row <= row <= (_row+s_row - 1)) and (_col <= col <= (_col+s_col - 1)):
                return obj
            
        return None

    def DrawShape(self, dc=None):
        """
        Рисует представление GridBagSizer.
        """
        if self.editorBackground:
            clr = self.shape_clr
            if self.shapeType == icParentShapeType:
                clr = (190, 0, 0)

            self.DrawCursor(clr=clr)
            #   Рисуем разметку для компонентов
            if not dc:
                dc = wx.ClientDC(self.GetParent())
                
            oldpen = dc.GetPen()
            pen = wx.Pen(clr, 1)
            dc.SetPen(pen)
            H = 0
            W = 0
            border = 0
            Px, Py = self.GetPosition()
            xx, yy = self.GetSize()
            rowsLst = self.GetRowHeights()
            colsLst = self.GetColWidths()
            maxrow = self.GetMaxRow()
            maxcol = self.GetMaxCol()
            self.sizeCols = []
            self.sizeRows = []
            
            #   Разметка рядов
            for row in range(maxrow+1):
                if row < len(rowsLst):
                    h = rowsLst[row]
                else:
                    h = self.minCellHeight
                    
                H += h+self.vgap
                self.sizeRows.append(H)
                dc.DrawLine(Px+1, Py+H-self.vgap/2, Px+xx-1, Py+H-self.vgap/2)
                
            #   Разметка колонк
            for col in range(maxcol+1):
                if col < len(colsLst):
                    w = colsLst[col]
                else:
                    w = self.minCellWidth
                            
                W += w + self.hgap
                self.sizeCols.append(W)
                dc.DrawLine(Px+W-self.hgap/2, Py+1, Px+W-self.hgap/2, Py+yy-1)

            #   Востанавливаем
            dc.SetPen(oldpen)
            
    def GetCellInPoint(self, pt):
        """
        Вычисляет координаты ячеки по позиции на окне, к которму привязан
        GridBagSizer.
        @type pt: C{wx.Point}
        @param pt: позиции в окне.
        @rtype: C{tuple}
        @return: Возвращает координату ячеки.
        """
        x, y = pt
        col, row = (0, 0)
        Px, Py = self.GetPosition()
        
        #   Определяем колонку
        if self.sizeCols:
            if x >= self.sizeCols[-1]+Px:
                col = len(self.sizeCols) + (x - (self.sizeCols[-1]+Px))/self.minCellWidth
            elif x < self.sizeCols[0]+Px:
                col = 0
            else:
                w1 = Px
                for indx, w2 in enumerate(self.sizeCols):
            
                    if w1 <= x < w2+Px:
                        col = indx
                        break
                        
                    w1 = w2+Px
        else:
            col = (x-Px)/self.minCellWidth

        #   Определяем ряд
        if self.sizeRows:
            if y > self.sizeRows[-1]+Py:
                row = len(self.sizeRows) + (y - (self.sizeRows[-1]+Py))/self.minCellHeight
            elif y < self.sizeRows[0]+Py:
                row = 0
            else:
                h1 = Py
                for indx, h2 in enumerate(self.sizeRows):
                                
                    if h1 <= y < h2+Py:
                        row = indx
                        break
                        
                    h1 = h2+Py
        else:
            row = (y-Py)/self.minCellHeight
            
        return row, col
        
    def GetCellRBPoint(self, row, col):
        """
        Возвращает координаты верхнего левого угла заданой ячейки.
        """
        if col < 0 or row < 0:
            return None

        dx, dy = self.GetPosition()
        try:
            for i in range(row):
                dy += wx.GridBagSizer.GetCellSize(self, i, col)
            for i in range(col):
                dx += wx.GridBagSizer.GetCellSize(self, row, i)
        except:
            io_prnt.outLastErr('icGridBagSizer.GetCellRBPoint')
                
        return wx.Point(dx, dy)


def test(par=0):
    """
    Тестируем класс icGridBagSizer.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'icGridBagSizer Test')
    win = wx.ScrolledWindow(frame, -1)
    win.SetBackgroundColour(wx.Colour(226, 226, 241))
    res = {'flag': wx.GROW | wx.EXPAND, 'flexCols': [2]}
    sz = icGridBagSizer(win, -1, res)

    print(u'>>> issubclass(sz.__class__, wx.Sizer): %s' % issubclass(sz.__class__, wx.Sizer))
    btn1 = wx.Button(win, -1, 'btn1')
    btn2 = wx.Button(win, -1, 'btn2')
    btn1.type = 'Button'
    btn2.type = 'Button'
    lbl1 = wx.StaticText(win, -1, 'lbl1')
    lbl2 = wx.StaticText(win, -1, 'lbl2')
    lbl1.type = 'StaticText'
    lbl2.type = 'StaticText'
    cmb1 = wx.ComboBox(win, -1)
    cmb2 = wx.ComboBox(win, -1)
    cmb1.type = 'ComboBox'
    cmb2.type = 'ComboBox'

    sz.Add(btn1, (1, 1), flag=wx.EXPAND)
    sz.Add(btn2, (1, 2), flag=wx.EXPAND)
    sz.Add(lbl1, (2, 1), flag=wx.EXPAND)
    sz.Add(cmb1, (2, 2), flag=wx.EXPAND)
    sz.Add(lbl2, (3, 1), flag=wx.EXPAND)
    sz.Add(cmb2, (3, 2), flag=wx.EXPAND)

    # ВНИМАНИЕ! Для распахивания объектов в колонке необходимо
    # указать эту возможность
    # sz.AddGrowableCol(2)

    win.SetSizer(sz)
    frame.Show(True)
    sz.editorBackground = True
    sz.DrawShape()
    print(sz.GetIndex(btn1))
    print(u'pos=%s, size=%s' % (sz.GetPosition(), sz.GetSize()))
    app.MainLoop()


if __name__ == '__main__':
    test(0)
