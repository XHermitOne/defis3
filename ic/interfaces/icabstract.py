#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Функции для абстрактных классов.
"""

__version__ = (0, 1, 1, 1)


def abstract():
    import inspect
    caller = inspect.getouterframes(inspect.currentframe())[1][3]
    raise NotImplementedError(caller + ' must be implemented in subclass')


def singleton(object, instantiated=[]):
    """
    Raise an exception if an object of this class has been instantiated before.
    """
    assert object.__class__ not in instantiated, \
        '%s is a Singleton class but is already instantiated' % object.__class__
    instantiated.append(object.__class__)


if __name__ == '__main__':
    pass
