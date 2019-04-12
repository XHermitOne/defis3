#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Постоянный атрибут метакомпонента.

"""

from ic.components import icwidget

# --- Спецификация ---
SPC_IC_METACONST = {'value': None,     # Значение атрибута
                    '__parent__': icwidget.SPC_IC_SIMPLE,
                    '__attr_hlp__': {'value': u'Значение атрибута',
                                     },
                    }

#   Версия компонента
__version__ = (0, 1, 1, 1)


class icMetaConstPrototype:
    """
    Постоянный атрибут метакомпонента.
    """

    def __init__(self, Resource_):
        """
        Конструктор.
        @param Resource_: Ресурс описания.
        """
        self._value = None
        
    def defaultValue(self):
        """
        Инициализировать значение по умолчанию.
        """
        self._value = self.eval_attr('value')[1]
        return self._value

    def getValue(self):
        """
        Получить значение.
        """
        return self._value
