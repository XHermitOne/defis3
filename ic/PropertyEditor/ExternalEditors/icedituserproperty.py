#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Редактор пользовательского свойства, определяемого компонентом.
"""

import wx
import wx.propgrid

from ic.utils import coderror
from ic.log import log

_ = wx.GetTranslation

__version__ = (0, 1, 1, 1)


class icEditUserPropertyEditor(wx.propgrid.PGTextCtrlAndButtonEditor):
    """
    Редактор пользовательского свойства,
        определяемого компонентом.
    """
    property_edit_manager = None

    @classmethod
    def setPropertyEditManager(self, manager):
        self.property_edit_manager = manager

    @classmethod
    def GetEditor(self):
        """
        Set editor to have button.
        ВНИМАНИЕ! Это указание типа редактора свойства.
        В данном случае это текстовый редактор с кнопкой
        """
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
                # log.debug(u'Значение: %s, Атрибут %s' % (str(value), attr))
                return str(value)
            except:
                log.fatal(u'Ошибка вызова пользовательского редактора свойства <%s>' % attr)
        else:
            log.warning(u'Не определен объект редактора свойств')
        return ''

    # def OnEvent(self, propgrid, primaryEditor, event):
    #    """
    #    Обработчик событий редактора свойства.
    #    @param propgrid:
    #    @param primaryEditor:
    #    @param event:
    #    @return:
    #    """
    #    if event.GetEventType() == wx.wxEVT_COMMAND_BUTTON_CLICKED:
    #        value = self._get_edit_dlg(self.GetName(), self.GetValue(),
    #                                   self.property_edit_manager)
    #        self.SetValueInEvent(value)
    #        return True
    #    return False

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

    # --- Переопределеяемые методы родительского редактора ----
    def CreateControls(self, propgrid, property, pos, sz):
        """
        Create the actual wxPython controls here for editing the
            property value.

            You must use propgrid.GetPanel() as parent for created controls.

            Return value is either single editor control or tuple of two
            editor controls, of which first is the primary one and second
            is usually a button.
        """
        try:
            x, y = pos
            w, h = sz

            # Make room for button
            bw = propgrid.GetRowHeight()
            w -= bw

            s = property.GetDisplayedString();

            self.tc = wx.TextCtrl(propgrid.GetPanel(), wx.propgrid.PG_SUBID1, s,
                                  (x, y), (w, h),
                                  wx.TE_PROCESS_ENTER)
            btn = wx.Button(propgrid.GetPanel(), wx.propgrid.PG_SUBID2, '...',
                            (x+w, y),
                            (bw, h), wx.WANTS_CHARS)
            return wx.propgrid.PGWindowList(self.tc, btn)
        except:
            log.fatal(u'Ошибка создания контролов редактора свойств <%s>' % self.__class__.__name__)

    #def UpdateControl(self, property, ctrl):
    #    ctrl.SetValue(property.GetDisplayedString())

    #def DrawValue(self, dc, rect, property, text):
    #    if not property.IsValueUnspecified():
    #        dc.DrawText(property.GetDisplayedString(), rect.x+5, rect.y)

    def OnEvent(self, propgrid, property, ctrl, event):
        """
        Обработчик событий редактора свойства.
        Return True if modified editor value should be committed to
            the property. To just mark the property value modified, call
            propgrid.EditorsValueWasModified().
        """
        if not ctrl:
            return False

        evtType = event.GetEventType()

        if evtType == wx.wxEVT_COMMAND_BUTTON_CLICKED:
            value = self._get_edit_dlg(attr=property.GetName(), value=self.tc.GetValue(),
                                       propEdt=self.property_edit_manager)
            property.SetValueInEvent(value)
            return True
        # elif evtType == wx.wxEVT_COMMAND_TEXT_ENTER:
        #     if propgrid.IsEditorsValueModified():
        #         return True
        # elif evtType == wx.wxEVT_COMMAND_TEXT_UPDATED:
        #     #
        #     # Pass this event outside wxPropertyGrid so that,
        #     # if necessary, program can tell when user is editing
        #     # a textctrl.
        #     event.Skip()
        #     event.SetId(propgrid.GetId())
        #
        #     propgrid.EditorsValueWasModified()
        #     return False

        return False

    #def GetValueFromControl(self, property, ctrl):
    #    """
    #    Return tuple (wasSuccess, newValue), where wasSuccess is True if
    #        different value was acquired successfully.
    #    """
    #    tc = ctrl
    #    textVal = tc.GetValue()

    #    if property.UsesAutoUnspecified() and not textVal:
    #        return True, None

    #    res, value = property.StringToValue(textVal, wx.propgrid.PG_FULL_VALUE)

    #    # Changing unspecified always causes event (returning
    #    # True here should be enough to trigger it).
    #    if not res and value is None:
    #        res = True

    #    return res, value

    # def SetValueToUnspecified(self, property, ctrl):
    #    ctrl.Remove(0, len(ctrl.GetValue()))

    #def SetControlStringValue(self, property, ctrl, text):
    #    ctrl.SetValue(text)

    #def OnFocus(self, property, ctrl):
    #    ctrl.setSelection(-1, -1)
