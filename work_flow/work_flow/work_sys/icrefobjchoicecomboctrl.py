#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Контрол выбора бизнес объекта/документа для организации связи
в стандартном виде через окно выбора.
"""

# --- Imports ---
import wx
import wx.combo

from ic.kernel import io_prnt
from ic.components import icwidget

# Version
__version__ = (0, 0, 0, 2)

DEFAULT_CODE_DELIMETER = u' '
DEFAULT_ENCODING = 'utf-8'

# Спецификация
SPC_IC_REFOBJCHOICECOMBOCTRL = {'obj_psp': None,  # Паспорт объекта-источника данных
                                '__parent__': icwidget.SPC_IC_WIDGET,
                                }


class icRefObjChoiceComboCtrlProto(wx.combo.ComboCtrl):
    """
    Класс компонента выбора бизнес объекта/документа
    через стандартный механизм диалогового
    окна выбора/поиска.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        wx.combo.ComboCtrl.__init__(self, *args, **kwargs)

        self.makeCustomButton()

        # Объект
        self._ref_obj = None

        self._selected_uuid = None

    def makeCustomButton(self):
        """
        Создание кнопки '...'.
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

        # and tell the ComboCtrl to use it
        self.SetButtonBitmaps(bmp, True)

    def setRefObj(self, ref_obj):
        """
        Устанвить бизнес объект/документ.
        """
        self._ref_obj = ref_obj

    def getRefObj(self):
        """
        Объект бизнес объекта/документа.
        """
        return self._ref_obj

    def getUUID(self):
        """
        Выбранный UUID.
        """
        return self._selected_uuid

    def setUUID(self, uuid):
        """
        Установить UUID бизнес объекта/документа как выбранный.
        @param uuid: UUID бизнес объекта/документа.
        @return: True/False.
        """
        if uuid is None:
            # Да пустое значение тоже можно
            # устанавливать в контроле
            self._selected_uuid = None
            self.SetValue(u'')
            return True

        if self._ref_obj is not None:
            self._ref_obj.load_obj(uuid)
            txt = self._ref_obj.getRequisiteValue('n_obj')
            if txt:
                self._selected_uuid = uuid
                self.SetValue(txt)
                return True
        else:
            io_prnt.outWarning(u'Не определен бизнес объект/документ в контроле icRefObjChoiceComboCtrl')
        return False

    getValue = getUUID
    setValue = setUUID

    def OnButtonClick(self):
        """
        Overridden from ComboCtrl, called when the combo button is clicked.
        """
        if self._ref_obj is not None:
            result = self._ref_obj.Choice(parent=self)
            if result:
                self._selected_uuid = result
                self._ref_obj.load_obj(self._selected_uuid)
                txt = self._ref_obj.getRequisiteValue('n_obj')
                self.SetValue(txt)
            else:
                io_prnt.outErr(u'Ошибка выбора бизнес объекта/документа <%s>. Результат %s' % (self._ref_obj.name, result))

    def DoSetPopupControl(self, popup):
        """
        Overridden from ComboCtrl to avoid assert since there is no ComboPopup.
        """
        pass
