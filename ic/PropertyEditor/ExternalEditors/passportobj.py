#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс редактора паспорта объекта.
"""

from ic.editor import icpassportchoice
from ic.utils import coderror
from ic.log import log

__version__ = (0, 0, 2, 2)


class ic_user_property_editor:
    """
    Базовый класс пользовательского редактора свойства.
    """
    def __init__(self, *arg, **kwarg):
        """
        Конструктор.
        """
        pass

    @staticmethod
    def get_user_property_editor(value, pos, size, style, propEdt, *arg, **kwarg):
        """
        Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
        
        @type value: C{string}
        @param value: Текущее значение цвета в виде 'wx.Colour(r,g,b)'.
        @type pos: C{wx.Point}
        @param pos: Позиция окна.
        @type size: C{wx.Size}
        @param size: Размер диалогового окна.
        @type style: C{int}
        @param style: Стиль диалога.
        @type metaclass: C{tuple}
        @param metaclass: Паспорт объекта, описывающего метадерево базового плана.
        @type propEdt: C{ic.components.user.objects.PropNotebookEdt}
        @param propEdt: Указатель на редактор свойств.
        """
        pass

    @staticmethod
    def property_editor_ctrl(value, propEdt, *arg, **kwarg):
        """
        Стандартная функция контроля.
        """
        pass

    @staticmethod
    def str_to_val_user_property(text, propEdt, *arg, **kwarg):
        """
        Стандартная функция преобразования текста в значение.
        """
        pass


class icObjectPassportUserEdt(ic_user_property_editor):
    """
    Класс редактора паспорта объекта.
    """

    @staticmethod
    def get_user_property_editor(value, pos, size, style, propEdt, *arg, **kwarg):
        """
        Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
        """
        if value:
            parent = propEdt
            res = icpassportchoice.icPassportChoiceDlg(parent)
            log.debug(u'passport = %s' % res)
            return str(res)

    @staticmethod
    def get_user_property_editor2(value, pos, size, style, propEdt, *arg, **kwarg):
        """
        Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
        """
        if value:
            parent = propEdt
            res = icpassportchoice.icPassportChoiceDlg(parent)
            return res
            
    @staticmethod
    def property_editor_ctrl(value, propEdt, *arg, **kwarg):
        """
        Стандартная функция контроля.
        """
        #   Преобразем строку к значению
        value = icObjectPassportUserEdt.str_to_val_user_property(value, propEdt)
        if value is None:
            return value

        if type(value) not in (list, tuple):
            return coderror.IC_CTRL_FAILED
            
        return coderror.IC_CTRL_OK
    
    @staticmethod
    def str_to_val_user_property(text, propEdt, *arg, **kwarg):
        """
        Стандартная функция преобразования текста в значение.
        """
        # Превращаем текст в кортеж (представление паспорта)
        try:
            if type(text) in (str, unicode) and text.strip():
                value = eval(text)
            else:
                value = text
        except:
            log.fatal(u'>>> str_to_val_user_property ERROR in eval(text): text=%s' % text)
            return None
        return value


class icObjectPassportListUserEdt(ic_user_property_editor):
    """
    Класс редактора списка паспортов объекта.
    """

    @staticmethod
    def get_user_property_editor(value, pos, size, style, propEdt, *arg, **kwarg):
        """
        Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
        """
        if value:
            parent = propEdt
            value = icObjectPassportListUserEdt.str_to_val_user_property(value, propEdt)
            res = icpassportchoice.icPassportListDlg(parent, None, value)
            log.debug(u'passports = %s' % res)
            return str(res)

    @staticmethod
    def get_user_property_editor2(value, pos, size, style, propEdt, *arg, **kwarg):
        """
        Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
        """
        if value:
            parent = propEdt
            value = icObjectPassportListUserEdt.str_to_val_user_property(value, propEdt)
            res = icpassportchoice.icPassportListDlg(parent, None, value)
            return res
            
    @staticmethod
    def property_editor_ctrl(value, propEdt, *arg, **kwarg):
        """
        Стандартная функция контроля.
        """
        #   Преобразем строку к значению
        value = icObjectPassportListUserEdt.str_to_val_user_property(value, propEdt)
        if value is None:
            return value

        if type(value) not in (list, tuple):
            return coderror.IC_CTRL_FAILED
            
        return coderror.IC_CTRL_OK
    
    @staticmethod
    def str_to_val_user_property(text, propEdt, *arg, **kwarg):
        """
        Стандартная функция преобразования текста в значение.
        """
        # Превращаем текс в картеж (представление паспорта)
        try:
            if type(text) in (str, unicode) and text.strip():
                value = eval(text)
            else:
                value = text
        except:
            log.fatal(u'>>> str_to_val_user_property ERROR in eval(text): text=%s' % text)
            return None
        return value
