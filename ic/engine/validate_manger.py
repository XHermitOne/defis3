#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль класса - менеджера контролера/валидатора вводимых данных в контролах WX.
"""

# Подключение библиотек
import wx
import wx.adv
import wx.gizmos
import wx.dataview

from ic.log import log
from ic.utils import ic_time

__version__ = (0, 1, 1, 1)

VALIDATIONS_ATTR_NAME = '_validations'


class icValidateManager(object):
    """
    Менеджер контролера/валидатора вводимых данных в контролах WX.
    """
    def get_validations(self):
        """
        Список проверок.
        Все проверки организуются в список и проверяются последовательно.
        Проверка представляет собой словарь:
            {'name': Наименование проверки,
             'function': Функция проверки правильного значения,
             'err_txt': Текст ошибки, в случае если проверка не прошла,
             'ctrl': Объект проверяемого контрола,
            }
        """
        if not hasattr(self, VALIDATIONS_ATTR_NAME):
            setattr(self, VALIDATIONS_ATTR_NAME, list())
        validations = getattr(self, VALIDATIONS_ATTR_NAME)
        return validations

    def add_validation_value(self, name, validation_func=None, error_msg=u'', ctrl=None):
        """
        Добавить простую проверку значения.
        Проверка представляет собой словарь:
            {'name': Наименование проверки,
             'function': Функция проверки правильного значения,
             'err_txt': Текст ошибки, в случае если проверка не прошла,
             'ctrl': Объект проверяемого контрола,
            }
        Все проверки организуются в список и проверяются последовательно.
        @param name: Наименование проверки.
        @param validation_func: Функция проверки правильного значения:
            Объект функции принимающий в качестве аргумента проверяемое значение.
            Функция должна возвращать True в случае если проверка прошла успешно и
            False если возникла проверяемая ошибка,
            либо lambda выражение с такамиже входными и выходными параметрами.
            Например:
                def notNone(value):
                    return value is not None
                или
                lambda value: value is not None
        @param error_msg: Текст ошибки, в случае если проверка возвращает False.
        @param ctrl: Контрол ввода значения в случае проверки по значению контрола.
        @return: True/False.
        """
        validations = self.get_validations()

        try:
            validation = dict(name=name,
                              func=validation_func,
                              err_txt=error_msg,
                              ctrl=ctrl)
            validations.append(validation)
            return True
        except:
            log.fatal(u'Ошибка добавления проверки по значению <%s>' % name)
        return False

    def _validate_values_dict(self, **values):
        """
        Запустить проверку значений.
        @param values: Словарь проверяемых значений:
            { 'Имя проверки': Проверяемое значение,
              ...
            }
        @return: Словарь проверок:
            { 'Имя проверки': Текст ошибки, если проверка не прошла или None в случае удачной проверки,
              ...
            }
        """
        validations = self.get_validations()

        validate_errors = dict()
        for validation_name, value in values.items():
            for validation in validations:
                if validation.get('name', None) == validation_name:
                    validate_msg = validation.get('err_txt', validation_name)
                    try:
                        validate_func = validation.get('function', None)
                        if validate_func:
                            is_ok = validate_func(value)
                            if not is_ok:
                                validate_errors[validation_name] = validation.get('err_txt',
                                                                                  u'Не определенный текст ошибки')
                        else:
                            validate_errors[validation_name] = u'Не определена функция проверки значения <%s>' % validate_msg
                    except:
                        err_msg = u'Ошибка выполнения проверки <%s>' % validate_msg
                        log.fatal(err_msg)
                        validate_errors[validation_name] = err_msg
        return validate_errors

    def validate_values_dict(self, **values):
        """
        Запустить проверку значений.
        @param values: Словарь проверяемых значений:
            { 'Имя проверки': Проверяемое значение,
              ...
            }
        @return: Словарь проверок:
            { 'Имя проверки': Текст ошибки, если проверка не прошла или None в случае удачной проверки,
              ...
            }
            либо None в случае ошибки.
        """
        try:
            return self._validate_values_dict(**values)
        except:
            log.fatal(u'Ошибка выполнения проверки значений')
        return None

    def _validate_ctrl_dict(self, *names):
        """
        Запустить проверку значений.
        @param names: Список имен проверок.
        @return: Словарь проверок:
            { 'Имя проверки': Текст ошибки, если проверка не прошла или None в случае удачной проверки,
              ...
            }
        """
        validations = self.get_validations()

        validate_errors = dict()
        for validation in validations:
            validation_name = validation.get('name', None)
            if validation_name in names:
                validate_msg = validation.get('err_txt', validation_name)
                try:
                    validate_func = validation.get('function', None)
                    validate_ctrl = validation.get('ctrl', None)
                    if validate_ctrl is None:
                        log.warning(u'Не определен контрол для проверки <%s>' % validate_msg)
                        continue

                    value = self.get_ctrl_value(validate_ctrl)
                    if validate_func:
                        is_ok = validate_func(value)
                        if not is_ok:
                            validate_errors[validation_name] = validation.get('err_txt',
                                                                              u'Не определенный текст ошибки')
                    else:
                        validate_errors[validation_name] = u'Не определена функция проверки значения <%s>' % validate_msg
                except:
                    err_msg = u'Ошибка выполнения проверки <%s>' % validate_msg
                    log.fatal(err_msg)
                    validate_errors[validation_name] = err_msg
        return validate_errors

    def validate_ctrl_dict(self, *names):
        """
        Запустить проверку значений контролов.
        @param names: Список имен проверок.
        @return: Словарь проверок:
            { 'Имя проверки': Текст ошибки, если проверка не прошла или None в случае удачной проверки,
              ...
            }
            либо None в случае ошибки.
        """
        try:
            return self._validate_ctrl_dict(*names)
        except:
            log.fatal(u'Ошибка выполнения проверки значений контролов')
        return None

    def get_ctrl_value(self, ctrl):
        """
        Получить значение контрола не зависимо от типа.
        @param ctrl: Объект контрола.
        @return: Значение контрола.
        """
        value = None
        if issubclass(ctrl.__class__, wx.Window) and ctrl.IsEnabled():
            if hasattr(ctrl, 'getValue'):
                # Обработка пользовательских контролов
                # Обычно все пользовательские контролы имеют
                # метод получения данных <getValue>
                value = ctrl.getValue()
            elif issubclass(ctrl.__class__, wx.CheckBox):
                value = ctrl.IsChecked()
            elif issubclass(ctrl.__class__, wx.TextCtrl):
                value = ctrl.GetValue()
            elif issubclass(ctrl.__class__, wx.adv.DatePickerCtrl):
                wx_dt = ctrl.GetValue()
                value = ic_time.wxdatetime2pydatetime(wx_dt)
            elif issubclass(ctrl.__class__, wx.DirPickerCtrl):
                value = ctrl.GetPath()
            elif issubclass(ctrl.__class__, wx.SpinCtrl):
                value = ctrl.GetValue()
            elif issubclass(ctrl.__class__, wx.dataview.DataViewListCtrl):
                value = self._get_wxDataViewListCtrl_data(ctrl)
            else:
                log.warning(u'icValidateManager. Получение данных контрола <%s> не поддерживается' % ctrl.__class__.__name__)
        return value
