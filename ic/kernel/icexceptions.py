#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Определение классов исключений.
"""

__version__ = (0, 1, 1, 1)


class KernelAccessException(Exception):
    """
    Запретщен доступ к ядру.
    """
    def __init__(self, args=None, user=None):
        self.args = args


class LoginErrorException(Exception):
    """
    Ошибка логина пользователя: Пользователь уже зарегистрирован
    """
    def __init__(self, args=None, user=None):
        self.args = args


class LoginInvalidException(Exception):
    """
    Ошибка логина пользователя: Неправильный пользователь или пароль
    """
    def __init__(self, args=None, user=None):
        self.args = args


class LoginDBExclusiveException(Exception):
    """
    Ошибка при логине: БД открыта в монополльном режиме
    """
    def __init__(self, args=None, user=None):
        self.args = args


class LoginWorkTimeException(Exception):
    """
    Ошибка при логине: Попытка входа в системы в не рабочее время
    """
    def __init__(self, args=None, user=None):
        self.args = args


class MethodAccessDeniedException(Exception):
    """
    Access denied: Доступ к методу запрещен.
    """
    def __init__(self, args=None, user=None):
        self.args = args
