#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс редактора списка строк из предлагаемого.
"""

# --- Imports ---
import wx
from ic.dlg import ic_dlg
from ic.kernel import io_prnt
from ic.utils import coderror
from . import passportobj

_ = wx.GetTranslation

__version__ = (0, 0, 0, 2)


class icMultiChoiceUserEdt(passportobj.ic_user_property_editor):
    """
    Класс редактора списка строк из предлагаемого.
    """

    @staticmethod
    def get_user_property_editor(value, pos, size, style, propEdt, *arg, **kwarg):
        """
        Стандартная функция для вызова пользовательских редакторов свойств
        (EDT_USER_PROPERTY).
        """
        if value is not None:
            parent = propEdt
            choice = [((row in value), row) for row in kwarg.get('choice', [])]
            title = _('Editor')
            if 'title' in kwarg:
                title = kwarg['title']
               
            edt_txt = _('Choose elements:')
            if 'edt_txt' in kwarg:
                edt_txt = kwarg['edt_txt']
                
            result = ic_dlg.icMultiChoiceDlg(parent,
                                             title, edt_txt,
                                             Choice_=tuple(choice))
            if result:
                result = [row[1] for row in result if row[0]]
            else:
                result = value
            
            return str(result)
            
    @staticmethod
    def property_editor_ctrl(value, propEdt, *arg, **kwarg):
        """
        Стандартная функция контроля.
        """
        #   Преобразем строку к значению
        value = icMultiChoiceUserEdt.str_to_val_user_property(value, propEdt)
        if value is None:
            return value

        if type(value) in (list, tuple):
            return coderror.IC_CTRL_OK
        else:
            return coderror.IC_CTRL_FAILED
            
        return coderror.IC_CTRL_OK
    
    @staticmethod
    def str_to_val_user_property(text, propEdt, *arg, **kwarg):
        """
        Стандартная функция преобразования текста в значение.
        """
        # Превращаем текс в картеж (представление паспорта)
        try:
            if type(text) in (str, unicode):
                value = eval(text)
            else:
                value = text
        except:
            io_prnt.outErr(u'>>> str_to_val_user_property ERROR in eval(text): text=%s' % text)
            return None
        return value
