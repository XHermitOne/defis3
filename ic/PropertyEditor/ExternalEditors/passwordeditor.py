#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс редактора пароля пользователя.
"""

from . import passportobj

from ic.editor import icpasswordedit
from ic.utils import coderror
from ic.dlg import dlgfunc

__version__ = (0, 1, 1, 1)


class icPasswordExternalEdt(passportobj.ic_user_property_editor):
    """
    Класс редактора пароля.
    """
    _is_external_edit = False
    
    @staticmethod
    def get_user_property_editor(value, pos, size, style, propEdt, *arg, **kwarg):
        """
        Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
        """
        parent = propEdt.GetPropertyGrid().GetView().GetParent()
        value = icPasswordExternalEdt.str_to_val_user_property(value, propEdt)
        res = icpasswordedit.open_password_edit_dlg(parent, None, value)
        icPasswordExternalEdt._is_external_edit = True
        return str(res)

    @staticmethod
    def property_editor_ctrl(value, propEdt, *arg, **kwarg):
        """
        Стандартная функция контроля.
        """
        #   Преобразем строку к значению
        value = icPasswordExternalEdt.str_to_val_user_property(value, propEdt)
        if value is None:
            return value

        if not icPasswordExternalEdt._is_external_edit:
            return coderror.IC_CTRL_FAILED_IGNORE
        icPasswordExternalEdt._is_external_edit = False
        
        if isinstance(value, str):
            return coderror.IC_CTRL_OK
        else:
            parent = propEdt.GetPropertyGrid().GetView()
            dlgfunc.openWarningBox(u'ВНИМАНИЕ', u'Введенная информация не является паролем.')
            return coderror.IC_CTRL_FAILED
            
        return coderror.IC_CTRL_OK
    
    @staticmethod
    def str_to_val_user_property(text, propEdt, *arg, **kwarg):
        """
        Стандартная функция преобразования текста в значение.
        """
        # Превращаем текс в картеж (представление паспорта)
        value = text
        return value
