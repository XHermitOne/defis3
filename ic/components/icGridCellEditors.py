#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Редакторы для грида.
"""

import wx
import wx.grid as gridlib
import time
import string


class BrFontRenderer(gridlib.PyGridCellRenderer):
    def __init__(self, table, color='black', font='ARIAL', fontsize=8):
        """
        Render data in the specified color and font and fontsize
        """
        gridlib.PyGridCellRenderer.__init__(self)
        self.table = table
        self.color = color
        self.font = wx.Font(fontsize, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, font)
        self.selectedBrush = wx.Brush('blue', wx.SOLID)
        self.normalBrush = wx.Brush(wx.WHITE, wx.SOLID)
        self.colSize = None
        self.rowSize = 50

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        # Here we draw text in a grid cell using various fonts
        # and colors.  We have to set the clipping region on
        # the grid's DC, otherwise the text will spill over
        # to the next cell
        dc.SetClippingRect(rect)

        # clear the background
        dc.SetBackgroundMode(wx.SOLID)
        
        if isSelected:
            dc.SetBrush(wx.Brush(wx.BLUE, wx.SOLID))
            dc.SetPen(wx.Pen(wx.BLUE, 1, wx.SOLID))
        else:
            dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
            dc.SetPen(wx.Pen(wx.WHITE, 1, wx.SOLID))
        dc.DrawRectangleRect(rect)

        text = self.table.GetValue(row, col)
        dc.SetBackgroundMode(wx.SOLID)

        # change the text background based on whether the grid is selected
        # or not
        if isSelected:
            dc.SetBrush(self.selectedBrush)
            dc.SetTextBackground('blue')
        else:
            dc.SetBrush(self.normalBrush)
            dc.SetTextBackground('white')

        dc.SetTextForeground(self.color)
        dc.SetFont(self.font)
        dc.DrawText(text, rect.x+1, rect.y+1)

        # Okay, now for the advanced class :)
        # Let's add three dots "..."
        # to indicate that that there is more text to be read
        # when the text is larger than the grid cell

        width, height = dc.GetTextExtent(text)
        
        if width > rect.width-2:
            width, height = dc.GetTextExtent('...')
            x = rect.x+1 + rect.width-2 - width
            dc.DrawRectangle(x, rect.y+1, width+1, height)
            dc.DrawText('...', x, rect.y+1)

        dc.DestroyClippingRegion()


class icGridCellDateEditor(wx.grid.PyGridCellEditor):
    """
    Редактор дат.
    """
    def __init__(self):
        """
        Конструктор.
        """
        self._evtHandler = None
        gridlib.PyGridCellEditor.__init__(self)

    def Create(self, parent, id, evtHandler):
        """
        Called to create the control, which must derive from wx.Control.
        """
        self._tc = wx.DatePickerCtrl(parent,
                                     dt=wx.DefaultDateTime,
                                     style=wx.DP_DEFAULT)
        self.SetControl(self._tc)
        self._evtHandler = evtHandler
        self._blockHandle = False
        self.grid = None
        if evtHandler:
            self._tc.PushEventHandler(evtHandler)
        
    def OnKeyDown(self, evt):
        cod = evt.GetKeyCode()
        if cod == wx.WXK_RETURN and self.grid:
            self.grid.DisableCellEditControl()
        elif cod == wx.WXK_ESCAPE:
            self.Reset()
            if self.grid:
                self.grid.DisableCellEditControl()
        else:
            evt.Skip()

    def SetSize(self, rect):
        """
        Called to position/size the edit control within the cell rectangle.
        If you don't fill the cell (the rect) then be sure to override
        PaintBackground and do something meaningful there.
        """
        self._tc.SetDimensions(rect.x, rect.y, rect.width+2, rect.height+2,
                               wx.SIZE_ALLOW_MINUS_ONE)

    def Show(self, show, attr=None):
        """
        Show or hide the edit control.  You can use the attr (if not None)
        to set colours or fonts for the control.
        """
        self._tc.Show(show)
        
    def BeginEdit(self, row, col, grid, *arg, **kwarg):
        """
        Fetch the value from the table and prepare the edit control
        to begin editing.  Set the focus to the edit control.
        *Must Override*
        """
        self.grid = grid
        value = grid.GetTable().GetValue(row, col)
        if value is None:
            value = ''
        value = value.replace(':', '.').replace('/', '.').replace('\\', '.')
        if value:
            year, month, day = [int(s) for s in value.split('.')]
            self.startValue = wx.DateTimeFromDMY(day, month-1, year)
        else:
            tm = time.localtime()
            self.startValue = wx.DateTimeFromDMY(tm[2], tm[1]-1, tm[0])
            
        self._tc.SetValue(self.startValue)
        self._tc.SetFocus()

    def EndEdit(self, row, col, grid, *arg, **kwarg):
        """
        Complete the editing of the current cell. Returns True if the value
        has changed.  If necessary, the control may be destroyed.
        *Must Override*
        """
        changed = False
        val = self._tc.GetValue()
        if 1:
            changed = True
            #   Преобразуем к строковому представлению
            y = str(val.GetYear())
            m = ('00'+str(val.GetMonth()+1))[-2:]
            d = ('00'+str(val.GetDay()))[-2:]
            grid.GetTable().SetValue(row, col, '%s.%s.%s' % (y, m, d))  # update the table

        self.startValue = val
        return changed

    def Reset(self):
        """
        Reset the value in the control back to its starting value.
        """
        self._tc.SetValue(self.startValue)

    def IsAcceptedKey(self, evt):
        """
        Return True to allow the given key to start editing: the base class
        version only checks that the event has no modifiers.  F2 is special
        and will always start the editor.
        """
        # or do it ourselves
        return (not (evt.ControlDown() or evt.AltDown()) and
                evt.GetKeyCode() != wx.WXK_SHIFT)

    def StartingKey(self, evt):
        """
        If the editor is enabled by pressing keys on the grid, this will be
        called to let the editor do something about that first key if desired.
        """
        key = evt.GetKeyCode()
        evt.Skip()

    def StartingClick(self):
        """
        If the editor is enabled by clicking on the cell, this method will be
        called to allow the editor to simulate the click on the control if
        needed.
        """
        pass

    def Destroy(self):
        """
        final cleanup
        """
        self.base_Destroy()

    def Clone(self):
        """
        Create a new object which is the copy of this one
        *Must Override*
        """
        return icGridCellDateEditor()


from . import icextendedcomboctrl


class icDatasetComboCellEditor(gridlib.PyGridCellEditor):
    """
    Расширенный комбинированный редактор ячейки.
    Используется в гриде редактирования свойств объекта в конфигураторе.
    """

    def __init__(self):
        gridlib.PyGridCellEditor.__init__(self)

    def Create(self, parent, id, evtHandler):
        """
        Создание контрола редактирования.
        Переопределяемый метод.
        """
        self._tc = icextendedcomboctrl.icGridDatasetComboCtrl(parent, id)
        self._tc.SetInsertionPoint(0)
        self.SetControl(self._tc)
        if evtHandler:
            self._tc.PushEventHandler(evtHandler)

    def SetSize(self, rect):
        """
        Установка размеров контрола редактирования.
        Переопределяемый метод.
        """
        self._tc.SetDimensions(rect.x, rect.y, rect.width+1, rect.height+1,
                               wx.SIZE_ALLOW_MINUS_ONE)

    def Show(self, show, attr):
        """
        Отобразить редактор.
        """
        super(icDatasetComboCellEditor, self).Show(show, attr)

    def BeginEdit(self, row, col, grid, *arg, **kwarg):
        """
        Начало редактирования.
        Переопределяемый метод.
        """
        self._tc.grid = grid
        self.startValue = grid.GetTable().GetValue(row, col)
        if self.startValue is None:
            self.startValue = u''
        # !!! Это не опечатка - так надо, чтобы включить обработчик нажатие клавиш, 
        # он мог быть отключен в EndEdit
        self._tc.GetTextCtrl().Enable(True)
        self._tc.GetTextCtrl().SetValue(self.startValue)
        self._tc.GetTextCtrl().SetInsertionPointEnd()
        self._tc.GetTextCtrl().SetFocus()

    def EndEdit(self, row, col, grid, *arg, **kwarg):
        """
        Окончание редактирования. Переопределяемый метод.
        """
        changed = False
        val = self._tc.GetTextCtrl().GetValue()
        if val != self.startValue:
            changed = True
            grid.GetTable().SetValue(row, col, val)  # update the table

        self.startValue = u''
        self._tc.GetTextCtrl().SetValue(u'')
        # Нужно для того, чтобы обработчик нажатие клавиш не заходил в обработку 
        # этого компонента
        self._tc.GetTextCtrl().Enable(False)
        return changed

    def Reset(self):
        """
        Сброс значения.
        Переопределяемый метод.
        """
        self._tc.GetTextCtrl().SetValue(self.startValue)
        self._tc.GetTextCtrl().SetInsertionPointEnd()

    def IsAcceptedKey(self, evt):
        """
        Переопределяемый метод.
        """
        # or do it ourselves
        return (not (evt.ControlDown() or evt.AltDown()) and
                evt.GetKeyCode() != wx.WXK_SHIFT)

    def StartingKey(self, evt):
        """
        Нажатие клавиши .
        Переопределяемый метод.
        """
        key = evt.GetKeyCode()
        ch = None
        if key in [wx.WXK_NUMPAD0, wx.WXK_NUMPAD1, wx.WXK_NUMPAD2, wx.WXK_NUMPAD3,
                   wx.WXK_NUMPAD4, wx.WXK_NUMPAD5, wx.WXK_NUMPAD6, wx.WXK_NUMPAD7,
                   wx.WXK_NUMPAD8, wx.WXK_NUMPAD9
                   ]:
            ch = ch = chr(ord('0') + key - wx.WXK_NUMPAD0)

        elif 0 <= key < 256 and chr(key) in string.printable:
            ch = chr(key)

        if ch is not None:
            # For this example, replace the text.  Normally we would append it.
            self._tc.GetTextCtrl().SetValue(ch)
            self._tc.GetTextCtrl().SetInsertionPointEnd()
        else:
            evt.Skip()

    def StartingClick(self):
        """
        Нажатие кнопки мыши.
        Переопределяемый метод.
        """
        pass

    def Destroy(self):
        """
        Разрушение.
        """
        super(icDatasetComboCellEditor, self).Destroy()

    def Clone(self):
        """
        Клонирование редактора.
        Переопределяемый метод.
        """
        return icExtendedComboCellEditor()


DEFAULT_NSI_DELIM = ' | '


class icGridCellNSIEditor(wx.grid.PyGridCellEditor):
    """
    Редактор выбора значения из справочника.
    """

    def __init__(self):
        """
        Конструктор.
        @param NSIPassport: Паспорт справочника.
        """
        self._evtHandler = None
        gridlib.PyGridCellEditor.__init__(self)

    def Create(self, parent, id, evtHandler):
        """
        Called to create the control, which must derive from wx.Control.
        """
        from NSI.nsi_sys import icspravtreecomboctrl

        self._tc = icspravtreecomboctrl.icSpravTreeComboCtrlPrototype(parent=parent, id=id)
        self.SetControl(self._tc)
        self._evtHandler = evtHandler
        self._blockHandle = False
        self.grid = None
        if evtHandler:
            self._tc.PushEventHandler(evtHandler)

    def OnKeyDown(self, evt):
        cod = evt.GetKeyCode()
        if cod == wx.WXK_RETURN and self.grid:
            self.grid.DisableCellEditControl()
        elif cod == wx.WXK_ESCAPE:
            self.Reset()
            if self.grid:
                self.grid.DisableCellEditControl()
        else:
            evt.Skip()

    def SetSize(self, rect):
        """
        Called to position/size the edit control within the cell rectangle.
        If you don't fill the cell (the rect) then be sure to override
        PaintBackground and do something meaningful there.
        """
        self._tc.SetDimensions(rect.x, rect.y, rect.width+2, rect.height+2,
                               wx.SIZE_ALLOW_MINUS_ONE)

    def Show(self, show, attr=None):
        """
        Show or hide the edit control.  You can use the attr (if not None)
        to set colours or fonts for the control.
        """
        self._tc.Show(show)

    def BeginEdit(self, row, col, grid, *arg, **kwarg):
        """
        Fetch the value from the table and prepare the edit control
        to begin editing.  Set the focus to the edit control.
        *Must Override*
        """
        self.grid = grid
        value = grid.GetTable().GetValue(row, col)
        if value is not None:
            value = value.split(DEFAULT_NSI_DELIM)
        cod = value[0] if value else None

        self.startValue = cod

        self._tc.setValue(self.startValue)
        self._tc.SetFocus()

    def EndEdit(self, row, col, grid, *arg, **kwarg):
        """
        Complete the editing of the current cell. Returns True if the value
        has changed.  If necessary, the control may be destroyed.
        *Must Override*
        """
        changed = False
        record = self._tc.getSelectedRecord()
        if record:
            cod = record.get('cod', '')

            #   Преобразуем к строковому представлению
            cell_txt = '%s%s%s' % (cod, DEFAULT_NSI_DELIM,
                                   record.get('name', ''))
            grid.GetTable().SetValue(row, col, cell_txt)  # update the table

            self.startValue = cod
            changed = True

        return changed

    def Reset(self):
        """
        Reset the value in the control back to its starting value.
        """
        self._tc.setValue(self.startValue)

    def IsAcceptedKey(self, evt):
        """
        Return True to allow the given key to start editing: the base class
        version only checks that the event has no modifiers.  F2 is special
        and will always start the editor.
        """
        # or do it ourselves
        return (not (evt.ControlDown() or evt.AltDown()) and
                evt.GetKeyCode() != wx.WXK_SHIFT)

    def StartingKey(self, evt):
        """
        If the editor is enabled by pressing keys on the grid, this will be
        called to let the editor do something about that first key if desired.
        """
        key = evt.GetKeyCode()
        evt.Skip()

    def StartingClick(self):
        """
        If the editor is enabled by clicking on the cell, this method will be
        called to allow the editor to simulate the click on the control if
        needed.
        """
        pass

    def Destroy(self):
        """
        final cleanup
        """
        self.base_Destroy()

    def Clone(self):
        """
        Create a new object which is the copy of this one
        *Must Override*
        """
        return icGridCellNSIEditor()


def test(par=0):
    """
    Тестируем класс icGridCellDateEditor.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'icGridCellDateEditor Test')
    win = wx.Panel(frame, -1)

    edt = icGridCellDateEditor()
    edt.Create(win, wx.NewId(), None)
    
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test(0)
