#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Панель управления разрешениями на действие."""
from ic.kernel import io_prnt
from ic.utils import coderror

class icPermissionsEdt(object):
    """ Класс редактора панели управления разрещениями на действия."""
    @staticmethod
    def get_user_property_editor(value, pos, size, style, propEdt, *arg, **kwarg):
        """ Стандартная функция для вызова пользовательских редакторов 
        свойств (EDT_USER_PROPERTY).
        """
#        #if value:
#        parent = propEdt.GetPropertyGrid().GetView().GetParent()
#        value=icPasswordExternalEdt.str_to_val_user_property(value, propEdt)            
#        res = icpasswordedit.icPasswordEditDlg(parent,None,value)
#        icPasswordExternalEdt._is_external_edit=True
#        return str(res)
            
    @staticmethod
    def property_editor_ctrl(value, propEdt, *arg, **kwarg):
        """ Функция контроля."""
        return coderror.IC_CTRL_OK
    
    @staticmethod
    def str_to_val_user_property(text, propEdt, *arg, **kwarg):
        """
        Стандартная функция преобразования текста в значение.
        """
        # Превращаем текс в картеж (представление паспорта)
        try:
            #if type(text) in (type(''),type(u'')):
            #    try:
            #        value = eval(text)
            #    except:
            #        value = text
            #else:
            value = text
        except:
            io_prnt.outErr('>>> str_to_val_user_property ERROR in eval(text): text=%s' % text)
            return None
        return value