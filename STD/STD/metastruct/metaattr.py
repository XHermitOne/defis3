#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Атрибут метакомпонента.
"""

from ic.components import icwidget

# --- Спецификация ---
SPC_IC_METAATTR = {'value': None,  # Значение атрибута
                   '__attr_hlp__': {'value': u'Значение атрибута',
                                    },
                   '__parent__': icwidget.SPC_IC_SIMPLE,
                   }

#   Версия компонента
__version__ = (0, 1, 1, 1)


class icMetaAttrPrototype:
    """
    Атрибут метакомпонента.
    """
    def __init__(self, Resource_):
        """
        Конструктор.
        :param Resource_: Ресурс описания.
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

    def setValue(self, Value_):
        """
        Установить значение.
        """
        self._value = Value_
