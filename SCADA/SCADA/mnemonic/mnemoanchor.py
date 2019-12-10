#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс якоря для прикрепления контролов к мнемосхеме.

Для позиционирования контролов на мнемосхеме используются компоненты-якоря,
которые определяют положение и размер контролов ввода вывода относительно
элементов SVG фона мнемосхемы.
"""

from ic.log import log

from ic.components import icwidget


# Version
__version__ = (0, 1, 1, 1)

# Указание направления смещения якоря
ANCHOR_DIRECTION_FROM_LEFT_TO_RIGHT = 1  # Слева направо
ANCHOR_DIRECTION_FROM_RIGHT_TO_LEFT = 2  # Справа налево
ANCHOR_DIRECTION_FROM_TOP_TO_BOTTOM = 4  # Сверху вниз
ANCHOR_DIRECTION_FROM_BOTTOM_TO_TOP = 8  # Снизу вверх

# --- Спецификация ---
SPC_IC_MNEMOANCHOR = {'__parent__': icwidget.SPC_IC_SIMPLE,

                      '__attr_hlp__': {
                                       },
                      }


class icMnemoAnchorProto(object):
    """
    Якорь мнемосхемы.
    """
    def __init__(self, pos=None, size=None,
                 direction=ANCHOR_DIRECTION_FROM_LEFT_TO_RIGHT | ANCHOR_DIRECTION_FROM_TOP_TO_BOTTOM,
                 min_size=None, max_size=None):
        """
        Конструктор.
        :param pos: Опорная позиция якоря.
        :param size: Размер ячейки якоря.
        :param direction: Указание направления смещения якоря.
        :param min_size: Указание ограничения размера по минимуму.
        :param max_size: Указание ограничения размера по максимуму.
        """
        self._position = pos
        self._size = size
        self._direction = direction
        self._min_size = min_size
        self._max_size = max_size

    def setControlPosition(self, ctrl=None):
        """
        Установить позицию и размер контрола в ссответствии с данным якорем.
        :param ctrl: Объект контрола.
        :return: True/False.
        """
        return False
