#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Редактор свойства кода справочника.
"""

import wx
import wx.propgrid

from ic.log import log
from ic.utils import coderror
from ic.dlg import edit_masked_txt_dlg

_ = wx.GetTranslation

__version__ = (0, 0, 0, 1)

DEFAULT_ENCODE = 'utf-8'


class icEditCodeProperty(wx.propgrid.PyStringProperty):
    """
    Редактор свойства кода справочника.
    """

    def __init__(self, label, name=wx.propgrid.LABEL_AS_NAME, value=u''):
        wx.propgrid.PyStringProperty.__init__(self, label, name, value)        

        # Для работы контроля ввода кода, необходим объект справочника
        self.sprav = None
        
        self.property_grid = None
        
    def setSprav(self, nsi_sprav):
        """
        Установить объект справочника.
        Для работы контроля ввода кода, необходим объект справочника
        """
        self.sprav = nsi_sprav
        
    def setPropertyGrid(self, property_grid):
        """
        Установить редактор свойств.
        """
        self.property_grid = property_grid
        
    def GetEditor(self):
        """
        Set editor to have button.
        ВНИМАНИЕ! Это указание типа редактора свойства.
            В данном случае это текстовый редактор с кнопкой
        """
        return 'TextCtrlAndButton'

    def _get_mask(self, sprav, code):
        """
        Определить маску по коду.
        ВНИМАНИЕ! Параметры маски:
        =========  ==========================================================
        Character   Function
        =========  ==========================================================
            #       Allow numeric only (0-9)
            N       Allow letters and numbers (0-9)
            A       Allow uppercase letters only
            a       Allow lowercase letters only
            C       Allow any letter, upper or lower
            X       Allow string.letters, string.punctuation, string.digits
            &       Allow string.punctuation only (doesn't include all unicode symbols)
            \*       Allow any visible character
            |       explicit field boundary (takes no space in the control; allows mix
                    of adjacent mask characters to be treated as separate fields,
                    eg: '&|###' means "field 0 = '&', field 1 = '###'", but there's
                    no fixed characters in between.
        =========  ==========================================================
        @param sprav: Объект справочника.
        @param code: Код записи справочника.
        """
        # Получаем структурный код
        struct_code = self.sprav.StrCode2ListCode(code)
        # Отфильтровать последние пустые подкоды
        struct_mask = [sub_code for sub_code in struct_code if sub_code]
        # Мы можем редактировать только последный подкод
        struct_mask[-1] = 'X{%d}' % (len(struct_mask[-1]))
        struct_mask = [''.join(['\\'+s for s in list(sub_code)]) for sub_code in struct_mask[:-1]] + [struct_mask[-1]]
        mask = ''.join(struct_mask)
        return mask

    def _get_regexp(self, sprav, code):
        """
        Определить регулярное выражение контроля по коду.
        <\W+?> - Добавлено в регулярное выражение для поддержки
        знаков пунктуации в кодах.
        @param sprav: Объект справочника.
        @param code: Код записи справочника.
        """
        # Получаем структурный код
        struct_code = self.sprav.StrCode2ListCode(code)
        # Отфильтровать последние пустые подкоды
        struct_exp = [sub_code for sub_code in struct_code if sub_code]
        # Мы можем редактировать только последный подкод
        struct_exp[-1] = r'[\W+?0-9a-zA-Z]{%d}' % (len(struct_exp[-1]))
        reg_exp = r''.join(struct_exp)
        return reg_exp
        
    def _get_edit_dlg(self, attr, value, pos=wx.DefaultPosition, size=wx.DefaultSize,
                      style=wx.DEFAULT_DIALOG_STYLE, 
                      propEdt=None, *arg, **kwarg):
        """
        Диалог редактирования свойства/атрибута.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type attr: C{string}
        @param attr: Имя текущего атрибута.
        @type value: C{string}
        @param value: Текущее значение.
        @type pos: C{wx.Point}
        @param pos: Позиция окна.
        @type size: C{wx.Size}
        @param size: Размер диалогового окна.
        @type style: C{int}
        @param style: Стиль диалога.
        @param propEdt: Указатель на редактор свойств.
        @return: Возвращает отредактированное значение.
        """
        if propEdt:
            mask = self._get_mask(self.sprav, value)
            log.debug(u'Маска редактора кода справочника <%s>' % mask)
            reg_exp = self._get_regexp(self.sprav, value)
            log.debug(u'Регулярное выражение контроля редактора кода справочника <%s>' % reg_exp)
            
            value = edit_masked_txt_dlg.edit_masked_text_dlg(parent=propEdt, 
                                                             title=u'Редактирование кода записи справочника',
                                                             label=u'Введите код:',
                                                             default_txt=value,
                                                             mask=mask, reg_exp=reg_exp)
            if value:
                return str(value)
            return None
        else:
            log.warning(u'Не определен объект редактора свойств')
        return u''

    def OnEvent(self, propgrid, primaryEditor, event):
        """
        Обработчик событий редактора свойства.
        @param propgrid:
        @param primaryEditor:
        @param event:
        @return:
        """
        if event.GetEventType() == wx.wxEVT_COMMAND_BUTTON_CLICKED:
            value = self._get_edit_dlg(self.GetName(), self.GetValue(),
                                       pos=wx.GetMousePosition(),
                                       propEdt=self.property_grid)
            self.SetValueInEvent(value)
            return True
        return False

    def ValueToString(self, value, flags):
        return str(value)

    def StringToValue(self, text, argFlags):
        """
        If failed, return False or (False, None). If success, return tuple
            (True, newValue).
        """
        value = unicode(text, DEFAULT_ENCODE)
        return True, value

    def ValidateValue(self, value, validationInfo):
        """
        Функция контроля/валидации.
        """
        if isinstance(value, str) or isinstance(value, unicode):
            return True, value
        else:
            return False
