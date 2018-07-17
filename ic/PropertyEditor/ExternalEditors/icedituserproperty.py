#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Редактор пользовательского свойства, определяемого компонентом.
"""

import wx
import wx.propgrid

from ic.utils import coderror
from ic.log import log

_ = wx.GetTranslation

__version__ = (0, 0, 1, 1)


class icEditUserProperty(wx.propgrid.PyStringProperty):
    """
    Редактор пользовательского свойства,
        определяемого компонентом
    """

    def __init__(self, label, name=wx.propgrid.LABEL_AS_NAME, value=''):
        wx.propgrid.PyStringProperty.__init__(self, label, name, value)

        self.property_edit_manager = None

    def setPropertyEditManager(self, manager):
        self.property_edit_manager = manager

    def GetEditor(self):
        """
        Set editor to have button.
        """
        # ВНИМАНИЕ! Это указание типа редактора свойства.
        # В данном случае это текстовый редактор с кнопкой
        return 'TextCtrlAndButton'

    def _get_edit_dlg(self, attr, value, pos=wx.DefaultPosition, size=wx.DefaultSize,
                      style=0, propEdt=None, *arg, **kwarg):
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
        if propEdt is None:
            propEdt = self.property_edit_manager

        if propEdt and propEdt.getResTree():
            typRes = propEdt.getResource()['type']
            modl = propEdt.getResTree().GetTypeModule(typRes)
            try:
                edtFunc = getattr(modl, 'get_user_property_editor')
                value = edtFunc(attr, value, pos, size,
                                style, propEdt, *arg, **kwarg)
                return str(value)
            except:
                log.fatal(u'Ошибка вызова пользовательского редактора свойства <%s>' % attr)
        else:
            log.warning(u'Не определен объект редактора свойств')
        return ''

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
                                       self.property_edit_manager)
            self.SetValueInEvent(value)
            return True
        return False

    def ValueToString(self, value, flags):
        return str(value)

    def str_to_val_user_property(self, value, propEdt, *arg, **kwarg):
        """
        Стандартная функция преобразования текста в значение.
        """
        if propEdt is None:
            propEdt = self.property_edit_manager

        if propEdt and propEdt.getResTree():
            typRes = propEdt.getResource()['type']
            modl = propEdt.getResTree().GetTypeModule(typRes)
            try:
                func = getattr(modl, 'str_to_val_user_property')
                value = func(self.GetName(), value, propEdt, *arg, **kwarg)
                return value
            except:
                log.fatal(u'Ошибка преобразования типа пользовательского редактора свойства <%s>' % self.GetName())
        else:
            log.warning(u'Не определен объект редактора свойств')
        return None

    def StringToValue(self, text, argFlags):
        """
        If failed, return False or (False, None). If success, return tuple
            (True, newValue).
        """
        value = self.str_to_val_user_property(text, self.property_edit_manager)
        return True, value

    def property_editor_validate(self, value, propEdt, *arg, **kwarg):
        """
        Стандартная функция контроля.
        """
        if propEdt is None:
            propEdt = self.property_edit_manager

        if propEdt and propEdt.getResTree():
            typRes = propEdt.getResource()['type']
            modl = propEdt.getResTree().GetTypeModule(typRes)
            try:
                func = getattr(modl, 'property_editor_ctrl')
                code_err = func(self.GetName(), value, propEdt, *arg, **kwarg)
                return code_err
            except:
                log.fatal(u'Ошибка преобразования типа пользовательского редактора свойства <%s>' % self.GetName())
        else:
            log.warning(u'Не определен объект редактора свойств')
        return coderror.IC_CTRL_FAILED

    def ValidateValue(self, value, validationInfo):
        """
        Функция контроля/валидации.
        """
        code_err = self.property_editor_validate(value, self.property_edit_manager)
        if code_err == coderror.IC_CTRL_OK:
            return True, value
        else:
            return False
