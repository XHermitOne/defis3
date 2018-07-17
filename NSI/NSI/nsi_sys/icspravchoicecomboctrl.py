#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Контрол выбора элемента справочника в стандартном виде через окно выбора.
"""

# --- Imports ---
import wx
import wx.combo

from ic.kernel import io_prnt
from ic.utils import coderror
from ic.components import icwidget

# Version
__version__ = (0, 0, 1, 2)

DEFAULT_CODE_DELIMETER = u' '
DEFAULT_ENCODING = 'utf-8'

# Спецификация
SPC_IC_SPRAVCHOICECOMBOCTRL = {'sprav': None,       # Паспорт справочника-источника данных
                               'view_fields': None,     # Список отображаемых полей
                               'search_fields': None,   # Список полей для поиска
                               '__parent__': icwidget.SPC_IC_WIDGET,
                               }


class icSpravChoiceComboCtrlProto(wx.combo.ComboCtrl):
    """
    Класс компонента выбора справочника через стандартный
    механизм диалогового окна выбора/поиска.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        # Сделать только для чтения
        style = wx.CB_READONLY
        if 'style' in kwargs:
            style = kwargs['style'] | wx.CB_READONLY
        kwargs['style'] = style

        wx.combo.ComboCtrl.__init__(self, *args, **kwargs)

        self.makeCustomButton()

        # Объект справочника
        self._sprav = None

        self._selected_cod = None

        # Список отображаемых полей
        self._view_fieldnames = None
        # Список полей для поиска
        self._search_fieldnames = None

        # Привязать обработчики событий
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseLeftDown)

    def Enable(self, *args, **kwargs):
        """
        Почему то не зарисовывается контрол серым при включении стиля wx.CB_READONLY.
        Поэтому переопределяем.
        """
        wx.combo.ComboCtrl.Enable(self, *args, **kwargs)

        if not self.IsEnabled():
            self.SetBackgroundColour(wx.Colour(236, 234, 233))
        else:
            self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DHIGHLIGHT))

    def makeCustomButton(self):
        """
        Создание кнопки '...'.
        """
        # make a custom bitmap showing "..."
        bw, bh = 16, 16
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

    def setSprav(self, sprav):
        """
        Установить справочник.
        """
        self._sprav = sprav

    def setViewFieldnames(self, fieldnames):
        """
        Установить отображаемые поля справочника.
        """
        self._view_fieldnames = fieldnames

    def setSearchFieldnames(self, fieldnames):
        """
        Установить отображаемые поля справочника.
        """
        self._search_fieldnames = fieldnames

    def getSprav(self):
        """
        Объект справочника.
        """
        return self._sprav

    def getCode(self):
        """
        Выбранный код справочника.
        """
        return self._selected_cod

    def setCode(self, code):
        """
        Установить код справочника как выбранный.
        @param code: Код справочника.
        @return: True/False.
        """
        if code is None:
            # Да пустое значение тоже можно
            # устанавливать в контроле
            self._selected_cod = None
            self.SetValue(u'')
            return True

        if self._sprav is not None:
            name = self._sprav.Find(code)
            if name:
                self._selected_cod = code
                self.SetValue(name)
                return True
        else:
            io_prnt.outWarning(u'Не определен справочник в контроле icSpravChoiceComboCtrl')
        return False

    # !!! Эти функции должны обязательно присутствовать
    # во всех контролах для унификации установки/чтения значения контрола !!!
    getValue = getCode
    setValue = setCode

    def choiceSprav(self):
        """
        Вызов выбора из справочника.
        @return: Выбранный код.
        """
        if self._sprav is not None:
            result = self._sprav.Hlp(field='name', parentForm=self,
                                     view_fields=self._view_fieldnames,
                                     search_fields=self._search_fieldnames)
            if result[0] in (0, coderror.IC_HLP_OK):
                code = result[1]
                name = result[2]
                self._selected_cod = code
                self.SetValue(name)
                return self._selected_cod
            else:
                io_prnt.outErr(u'Ошибка выбора справочника <%s>. Результат %s' % (self._sprav.name, result))
        return None

    def onMouseLeftDown(self, event):
        """
        Обработчик клика левой кнопки на контроле.
        """
        # ВНИМАНИЕ! Здесь не надо вызывать self.choiceSprav(). Достаточно поставить
        # event.Skip() и автоматом будет вызываться self.OnButtonClick()
        event.Skip()

    def OnButtonClick(self):
        """
        Overridden from ComboCtrl, called when the combo button is clicked.
        """
        self.choiceSprav()

    def DoSetPopupControl(self, popup):
        """
        Overridden from ComboCtrl to avoid assert since there is no ComboPopup.
        """
        pass
