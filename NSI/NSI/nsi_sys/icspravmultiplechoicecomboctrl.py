#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Контрол выбора нескольких элементов справочника в стандартном виде через окно выбора.

ВНИМАНИЕ! В компонент можно только добавлять коды из справочника.
Удалять нельзя. Компонент используется в формах задания критериев поиска или
формах фильтров и т.п.
"""

# --- Imports ---
import wx
import wx.combo

from ic.kernel import io_prnt
from ic.utils import coderror
from ic.components import icwidget

# Version
__version__ = (0, 0, 0, 2)

# DEFAULT_CODE_DELIMETER = u' '
DEFAULT_ENCODING = 'utf-8'

# Разделитель по умолчанию наименований в контроле
DEFAULT_LABEL_DELIMETER = u'; '

# Спецификация
SPC_IC_SPRAVMULTIPLECHOICECOMBOCTRL = {'sprav': None,           # Паспорт справочника-источника данных
                                       'view_fields': None,     # Список отображаемых полей
                                       'search_fields': None,   # Список полей для поиска
                                       '__parent__': icwidget.SPC_IC_WIDGET,
                                       }


class icSpravMultipleChoiceComboCtrlProto(wx.combo.ComboCtrl):
    """
    Класс компонента множественного выбора справочника через стандартный
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

        # Выбранные коды
        self._selected_codes = None

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

    def getCodes(self):
        """
        Выбранные коды справочника.
        """
        if self._selected_codes is None:
            return list()
        return self._selected_codes

    def setCodes(self, codes):
        """
        Установить коды справочника как выбранные.
        @param codes: Коды справочника. Список строк.
            ВНИМАНИЕ! Коды могут задаваться строкой.
            Тогда считаем что это список из 1 кода.
        @return: True/False.
        """
        if codes is None:
            # Да пустое значение тоже можно
            # устанавливать в контроле
            self._selected_codes = None
            self.SetValue(u'')
            return True

        if isinstance(codes, str) or isinstance(codes, unicode):
            codes = [codes]

        self._selected_codes = list()
        if self._sprav is not None and codes:
            names = list()
            for code in codes:
                name = self._sprav.Find(code)
                if name:
                    self._selected_codes.append(code)
                    names.append(name)

            label = DEFAULT_LABEL_DELIMETER.join(names)
            self.SetValue(label)
            return True
        else:
            io_prnt.outWarning(u'Не определен справочник в контроле icSpravMultipleChoiceComboCtrl')
        return False

    getValue = getCodes
    setValue = setCodes

    def choiceSprav(self):
        """
        Вызов выбора из справочника.
        @return: Выбранный код.
        """
        if self._selected_codes is None:
            self._selected_codes = list()

        if self._sprav is not None:
            result = self._sprav.Hlp(field='name', parentForm=self,
                                     view_fields=self._view_fieldnames,
                                     search_fields=self._search_fieldnames)
            if result[0] in (0, coderror.IC_HLP_OK):
                code = result[1]
                name = result[2]
                if code not in self._selected_codes:
                    self._selected_codes.append(code)

                    label = self.GetValue() + DEFAULT_LABEL_DELIMETER + name if self.GetValue() else name
                    self.SetValue(label)
                    return code
                else:
                    io_prnt.outWarning(u'Код [%s] уже присутствует в выбранных' % code)
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
