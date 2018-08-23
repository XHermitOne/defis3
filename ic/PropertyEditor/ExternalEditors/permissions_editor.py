#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Панель управления разрешениями на действие.
"""

from ic.utils import coderror

__version__ = (0, 1, 1, 1)


class icPermissionsEdt(object):
    """
    Класс редактора панели управления разрещениями на действия.
    """

    @staticmethod
    def get_user_property_editor(value, pos, size, style, propEdt, *arg, **kwarg):
        """
        Стандартная функция для вызова пользовательских редакторов
        свойств (EDT_USER_PROPERTY).
        """
        pass

    @staticmethod
    def property_editor_ctrl(value, propEdt, *arg, **kwarg):
        """
        Функция контроля.
        """
        return coderror.IC_CTRL_OK
    
    @staticmethod
    def str_to_val_user_property(text, propEdt, *arg, **kwarg):
        """
        Стандартная функция преобразования текста в значение.
        """
        value = text
        return value