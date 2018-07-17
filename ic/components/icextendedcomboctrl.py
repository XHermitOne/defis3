#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Всевозможные расширенные комбинированные редакторы.
"""

# --- Подключение библиотек ---
import wx
import wx.combo

__version__ = (0, 0, 0, 2)

# --- Описание классов ---


class icExtendedComboCtrlPrototype(wx.combo.ComboCtrl):
    """
    Прототип расширеннного комбинированнного редактора.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        wx.combo.ComboCtrl.__init__(self, *args, **kwargs)
        bmp = self._drawButton()
        # and tell the ComboCtrl to use it
        self.SetButtonBitmaps(bmp, True)
        
    def _drawButton(self):
        """
        Отрисовка кнопки выбора.
        """
        # make a custom bitmap showing "..."
        bw, bh = 14, 16
        bmp = wx.EmptyBitmap(bw, bh)
        dc = wx.MemoryDC(bmp)

        # clear to a specific background colour
        bgcolor = wx.Colour(255, 254, 255)
        dc.SetBackground(wx.Brush(bgcolor))
        dc.Clear()

        # draw the label onto the bitmap
        label = '...'
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        tw, th = dc.GetTextExtent(label)
        dc.DrawText(label, (bw-tw)/2, (bw-tw)/2)
        del dc

        # now apply a mask using the bgcolor
        bmp.SetMaskColour(bgcolor)
        return bmp
        
    def extendedChoice(self):
        """
        Выполнение расширенной функции выбора.
        """
        return None
        
    def OnButtonClick(self):
        """
        Переопределяемый обработчик события нажатия на кнопку выбора.
        """
        result = str(self.extendedChoice())
        self.SetValue(result)

    def DoSetPopupControl(self, popup):
        """
        Переопределяемый метод выпадения списка выбора в комбобоксе.
        """
        pass


class icExtendedComboCtrl(icExtendedComboCtrlPrototype):
    """
    Расширеннный комбинированнный редактор.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        icExtendedComboCtrlPrototype.__init__(self, *args, **kwargs)


class icGridDatasetComboCtrl(icExtendedComboCtrlPrototype):
    """
    Расширеннный комбинированнный редактор.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        icExtendedComboCtrlPrototype.__init__(self, *args, **kwargs)
        # Указатель на icgriddataset
        self.grid = None

    def OnButtonClick(self):
        """
        Переопределяемый обработчик события нажатия на кнопку выбора.
        """
        if self.grid:
            return self.grid.OnExtend()

    def GetButton(self):
        return wx.combo.ComboCtrl.GetButton(self)
