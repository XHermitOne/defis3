#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import icobject


def to_passport(func):
    """
    Приводит пасспорт к базовому виду.
    """
    def wrapper(self, passport, *args, **kwargs):
        if type(passport) in (type([]), type(())):
            passport = icobject.icObjectPassport(*passport)
        return func(self, passport, *args, **kwargs)
    return wrapper


def init_context(func):
    """
    Инициализация контекста.
    """
    def wrapper(self, *args, **kwargs):
        if 'context' in kwargs:
            if not kwargs['context']:
                context = self.init_new_context()
            else:
                context = kwargs['context']
                
            kwargs['context'] = context
            return func(self, *args, **kwargs)
        else:
            return func(self, *args, **kwargs)
        
    return wrapper
