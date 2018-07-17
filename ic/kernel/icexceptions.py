#!/usr/bin/env python
# -*- coding: utf-8 -*-

import exceptions


class KernelAccessException(exceptions.Exception):
    """
    Запретщен доступ к ядру.
    """
    def __init__(self, args=None, user=None):
        self.args = args


class LoginErrorException(exceptions.Exception):
    """
    Ошибка логина пользователя: Пользователь уже зарегистрирован
    """
    def __init__(self, args=None, user=None):
        self.args = args


class LoginInvalidException(exceptions.Exception):
    """
    Ошибка логина пользователя: Неправильный пользователь или пароль
    """
    def __init__(self, args=None, user=None):
        self.args = args


class LoginDBExclusiveException(exceptions.Exception):
    """
    Ошибка при логине: БД открыта в монополльном режиме
    """
    def __init__(self, args=None, user=None):
        self.args = args


class LoginWorkTimeException(exceptions.Exception):
    """
    Ошибка при логине: Попытка входа в системы в не рабочее время
    """
    def __init__(self, args=None, user=None):
        self.args = args


class MethodAccessDeniedException(exceptions.Exception):
    """
    Access denied: Доступ к методу запрещен.
    """
    def __init__(self, args=None, user=None):
        self.args = args
