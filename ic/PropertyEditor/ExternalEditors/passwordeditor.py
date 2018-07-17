#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс редактора пароля пользователя.
"""

from . import passportobj

from ic.editor import icpasswordedit
from ic.kernel import io_prnt
from ic.utils import coderror
from ic.dlg import ic_dlg

__version__ = (0, 0, 1, 2)


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
        res = icpasswordedit.icPasswordEditDlg(parent, None, value)
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
        
        if type(value) in (str, unicode):
            return coderror.IC_CTRL_OK
        else:
            parent = propEdt.GetPropertyGrid().GetView()
            ic_dlg.icWarningBox(u'ВНИМАНИЕ', u'Введенная информация не является паролем.')
            return coderror.IC_CTRL_FAILED
            
        return coderror.IC_CTRL_OK
    
    @staticmethod
    def str_to_val_user_property(text, propEdt, *arg, **kwarg):
        """
        Стандартная функция преобразования текста в значение.
        """
        # Превращаем текс в картеж (представление паспорта)
        try:
            value = text
        except:
            io_prnt.outErr(u'>>> str_to_val_user_property ERROR in eval(text): text=%s' % text)
            return None
        return value
