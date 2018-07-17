#!/usr/bin/env python
# -*- coding: utf-8 -*-
### TEMPLATE_MODULE:

import wx
import ic.interfaces.ictemplate as ictemplate
import ic.utils.util as util
import copy
import ic.components.user.icsimplegrid as parentModule
from ic.utils import graphicUtils
import wx.lib.mixins.gridlabelrenderer as glr
from ic.components import icfont
from ic.components.renders import xpgridrenders as xpr
from ic.kernel import io_prnt
import  wx.grid as  gridlib
from ic.imglib import newstyle_img

### Standart component interface
ictemplate.inherit_component_interface(globals(), parentModule, ic_class_name = 'CXPSpravTable')
ic_class_pic = '@ic.imglib.newstyle_img.xpgrid'
ic_class_pic2 = '@ic.imglib.newstyle_img.xpgrid'
#   Component version
__version__ = (1,0,0,1)

ic_class_spc = {'name':'default',
                'type':'XPSpravTable',
                '__parent__':parentModule.ic_class_spc}

# Имя объекта справочника в контексте
#CONTEXT_SPRAV_NAME = 'OBJ'
parentClass = getattr(parentModule, parentModule.ic_class_name)
class CXPSpravTable(parentClass):
    """ User component class.
    @type component_spc: C{dictionary}
    @cvar component_spc: Specification.
        - B{type='defaultType'}:
        - B{name='default'}:
    """
    component_spc = ic_class_spc

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace = None, bCounter=False, progressDlg=None):
        """ Interface constructor."""
        # Append for specification
        component = util.icSpcDefStruct(ic_class_spc, component)
        parentClass.__init__(self, parent, id, component, logType, evalSpace,
                                                bCounter, progressDlg)
        header = ({'label':u'Код'}, {'label':u'Наименование'})
        table = HugeTable(header=header)
        self.SetTable(table, True)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        for key in [x for x in component.keys() if not x.startswith('__')]:
            setattr(self, key, component[key])

        self.SetCornerLabelRenderer(xpr.XPCornerLabelRenderer())
        self._colAttrs = []
        for col in xrange(self.GetNumberCols()):
            self.SetColLabelRenderer(col, xpr.XPColLabelRenderer())
            attr = xpr.XPColAttr()
            self.SetColAttr(col, attr)
            self._colAttrs.append(attr)
            if col < len(self.wcols):
                self.SetColSize(col, self.wcols[col])

#        self._row_render = rowr = xpr.XPRowLabelRenderer()
#        for row in xrange(self.GetNumberRows()):
#            self.SetRowLabelRenderer(row, rowr)
        self.SetRowLabelSize(0)

        self._cell_height = 18
        self.SetColLabelSize(self._cell_height)
        font = icfont.icFont({})
        self.SetLabelFont(font)
        self.SetDefaultCellBackgroundColour(xpr.DEFAULT_EMPTY_BGR_CLR)
        self.SetLabelTextColour(xpr.TEXT_LAB_CLR)
        self.SetGridLineColour(xpr.GRID_LINE_CLR)
        self.SetLabelBackgroundColour(xpr.BOT_LAB_CLR)
        self.SetRowMinimalAcceptableHeight(0)
        #self.SetDefaultRenderer(xpr.DefaultCellRenderer())
        self.state = 0
        self.state_dct = {}
        # Список имен кода
        self.cod_name_lst = []
        self.cur_cod = None
        self.sprav = None

    def select_cod(self, cod=None, sel_cod=None):
        """ Выбор кода."""
        sprav = self.get_sprav()
        name = ''
        if cod == None:
            cod = self.get_sel_cod()
            name = self.get_sel_name()

        cur = self.get_cur_cod()
        if cod != '...':
            #Получить таблицу
            level = sprav.getLevelByCod(cod)
            if level.isNext():
                level_tab=sprav.getStorage().getLevelTable(cod)
                self.SetDataset([('...', '')] + level_tab, cod)
                if name:
                    self.cod_name_lst.append(name)
                else:
                    self.cod_name_lst.append(cod)
        else:
            #Получить родительскую таблицу
            level = sprav.getLevelByCod(cur)
            if cur:
                prnt_cod = cur[:-level.getCodLen()]
                prnt_level_tab = sprav.getStorage().getLevelTable(prnt_cod)
                self.SetDataset([('...', '')] + prnt_level_tab, prnt_cod)
            else:
                prnt_level_tab = [('', sprav.description, '', '', '')]
                self.SetDataset(prnt_level_tab, '')

            if self.cod_name_lst:
                self.cod_name_lst = self.cod_name_lst[:-1]

        if sel_cod:
            wx.CallAfter(self.sel_cell_cod, sel_cod)

    def sel_cell_cod(self, sel_cod, col=1):
        """ Выбор нужной ячейки грида."""
        for r in xrange(self.GetTable().GetNumberRows()):
            rc = self.GetTable().GetValue(r, 0)
            if rc == sel_cod:
                self.SetGridCursor(r, col)
                self.MakeCellVisible(r, col)
                break

    def ShowRow(self, row, flag=True):
        """ Показать скрытую строку."""
        if flag:
            self.SetRowSize(row, self._cell_height)
        else:
            self.SetRowSize(row, 0)

    def HideRow(self, row):
        """ Скрыть строку."""
        self.SetRowSize(row, 0)

    def set_sprav(self, sprav):
        self.sprav = sprav

    def get_sprav(self):
        """ Возвращает объкт справочника."""
        return self.sprav
#        return self.GetContext().get(CONTEXT_SPRAV_NAME, None)

    def get_sel_cod(self, row=None):
        """ Возвращает выбранный код."""
        if row == None:
            row = self.GetGridCursorRow()
        return self.GetTable().GetValue(row, 0)

    def get_sel_name(self, row=None):
        """ Возвращает выбранный код."""
        if row == None:
            row = self.GetGridCursorRow()
        return self.GetTable().GetValue(row, 1)

    def get_cur_cod(self):
        """ Возвращает текущий код."""
        return self.cur_cod

    def GetRowState(self, row):
        """ Возвращает состояние строки."""
        if row in self.state_dct:
            return (0, self.state_dct[row])
        elif self.get_sprav():
            sprav = self.get_sprav()
            cod = self.GetTable().GetValue(row, 0)
            level=sprav.getLevelByCod(cod)
            if level.isNext() and cod != '...':
                self.state_dct[row] = 0
            else:
                self.state_dct[row] = 1

            return (0, self.state_dct[row])

        return (0, self.state)

    def HideRows(self, rows):
        """ Скрыть строки."""
        self.BeginBatch()
        for row in rows:
            self.HideRow(row)
        self.EndBatch()

    def ShowRows(self, rows):
        """ Скрыть строки."""
        self.BeginBatch()
        for row in rows:
            self.ShowRow(row)
        self.EndBatch()

    def GetDefaultRowLabelRanderer(self):
        if self._row_render:
            return self._row_render
        else:
            return self._defRowRenderer

    def GetRowLabelRenderer(self, row):
        """ Возвращает текущий рендерер на строку."""
        try:
            return self._rowRenderers[row]
        except KeyError:
            return self._defRowRenderer

    def GetColLabelRenderer(self, col):
        """ Возвращает текущий рендерер на колонку."""
        try:
            return self._colRenderers[col]
        except KeyError:
            return self._defColRenderer

    def GetColAttr(self, col):
        """ Возвращает объект атрибутов колонки."""
        return self._colAttrs[col]

    def SetColRenderer(self, col, render):
        """ Устанавливаем рендер для колонки."""
        try:
            attr = self.GetColAttr(col)
            attr.SetRenderer(render)
        except IndexError:
            pass

    def GetDataset(self):
        return self.GetTable().dataset

    def SetDataset(self, dataset, cod=None, goBegin = True):
        """ Определяет данные для грида."""
        self.oldSize = self.GetTable().GetNumberRows()
        self.GetTable().dataset = dataset
        self.RefreshGrid()
        self.cur_cod = cod
        self.state_dct = {}
        if goBegin:
            wx.CallAfter(self.SetGridCursor, 0,0)

    def RefreshGrid(self):
        """ Перечитывает данные и перерисовывает грид."""
#        self.Refresh()
        self.UpdateDataView()

    def UpdateDataView(self):
        """ Обновляет вид грида после изменения размеров таблицы данных."""
        #   Если размер грида не совпадает с размерами данных, то подстраиваем размер грида
        try:
            cur = self.GetTable().GetNumberRows()
            oldSize, dataSize = self.oldSize, cur
            num = oldSize - dataSize
            if oldSize > dataSize:
                self.SendDelMess(cur, num)
            elif oldSize < dataSize:
                num = dataSize - oldSize
                self.SendAddMess(num)

            self.ForceRefresh()
        except:
            io_prnt.outErr(u'Exception in UpdateDataView')

    def SendAddMess(self, num):
        """ Функция посылает сообщение на добавление строк в грид."""
        if num <= 0:
            return False
        try:
            msg = wx.grid.GridTableMessage(self.GetTable(), wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED, num)
            self.ProcessTableMessage(msg)
        except:
            return False

        self.oldSize = self.GetTable().GetNumberRows()
        return True

    def SendDelMess(self, cur, num):
        """ Функция посылает сообщение на добавление строк в грид."""
        if num <= 0 or cur < 0:
            return False
        try:
            msg = wx.grid.GridTableMessage(self.GetTable(), wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED, cur, num)
            self.ProcessTableMessage(msg)
        except Exception:
            io_prnt.outLog(u'Exception, wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED')
            return False

        self.oldSize = self.GetTable().GetNumberRows()
        return True

    def setColLabels(self, cols):
        pass

class HugeTable(gridlib.PyGridTableBase):

    def __init__(self, header=None, log=None):
        gridlib.PyGridTableBase.__init__(self)
        self.log = log
        self.header = header
        self.defattr=gridlib.GridCellAttr()
        self.defattr.SetReadOnly()
        self.defattr.SetBackgroundColour(wx.WHITE)

        self.cod_attr=gridlib.GridCellAttr()
        self.cod_attr.SetReadOnly()
        self.cod_attr.SetBackgroundColour(wx.WHITE)

        self.dataset = None
#        from ic.imglib import newstyle_img
        img_rndr = xpr.stateImageRenderer(newstyle_img.folder)
        self.cod_attr.SetRenderer(img_rndr)
#        self.even=gridlib.GridCellAttr()
#        self.even.SetBackgroundColour("sea green")

    def GetAttr(self, row, col, kind):
        if col == 0:
            attr = self.cod_attr
        else:
            attr = self.defattr
        attr.IncRef()
        return attr

    def GetColLabelValue(self, col):
        """ """
        if self.header and col < len(self.header):
            return self.header[col].get('label','[None]')
        return ''

    def GetNumberRows(self):
        if self.dataset:
            return len(self.dataset)
        return 0

    def GetNumberCols(self):
        if self.header:
            return len(self.header)
        return 0

    def IsEmptyCell(self, row, col):
        return False

    def GetValue(self, row, col):
        if self.dataset:
            return self.dataset[row][col]

        return str( (row, col) )

    def SetValue(self, row, col, value):
        pass

def test(par=0):
    """ Тестируем класс icGrid"""
    from ic.components import ictestapp
    #import ic.components.icGridCellEditors as icEdt

    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'icGrid Test')
    win = wx.Panel(frame, -1)
    grid = CXPGrid(win, -1, {'size':(400, 300), 'col_count':10, 'row_count':10})
    rn = grid.GetRowLabelRenderer(0)
#    rn.SetVisibleNumRow(False)
#    rn.SetCursorFlag()
    grid.SetRowMinimalAcceptableHeight(0)
    grid.HideRow(5)
    cr = grid.GetColLabelRenderer(0)
    cr.SetSortFlag()
    cr.sortDirection = 0

    cr1 = grid.GetColLabelRenderer(1)
    cr1.SetSortFlag()
    cr1.sortDirection = 1

    cr2 = grid.GetColLabelRenderer(2)
    cr2.SetSortFlag()
    cr2.sortDirection = -1

    from ic.imglib import newstyle_img
    rr = xpr.cellImageRenderer(newstyle_img.item_closed, newstyle_img.item_opened)
    grid.SetColRenderer(0, rr)
    frame.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    test()