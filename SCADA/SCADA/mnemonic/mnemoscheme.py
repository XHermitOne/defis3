#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс мнемосхемы.

Мнемосхема представляет собой панель с размещенными на ней
контролами-индикаторами и контролами-манипуляторами
параметров абстрактного технологического процесса.
В качестве фона мнемосхема использует SVG файл схемы.
В качестве контролов используются обычные контролы ввода-вывода.
Для позиционирования контролов на мнемосхеме используются компоненты-якоря,
которые определяют положение и размер контролов ввода вывода относительно
элементов SVG фона мнемосхемы.
"""

import wx
import os.path

from ic.log import log
from ..scada_proto import scada_form_manager

from ic.components import icwxpanel

# Version
__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_MNEMOSCHEME = {'engines': list(),
                      'scan_class': None,
                      'auto_run': False,
                      'svg_background': None,

                      '__parent__': icwxpanel.SPC_IC_PANEL,

                      '__attr_hlp__': {'engines': u'Список движков SCADA системы',
                                       'scan_class': u'Класс сканирования',
                                       'auto_run': u'Признак автозапуска и автоостанова всех движков при создании/закрытии окна',
                                       'svg_background': u'SVG файл фона мнемосхемы'
                                       },
                      }


class icMnemoSchemeProto(scada_form_manager.icSCADAFormManager):
    """
    Мнемосхема.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        scada_form_manager.icSCADAFormManager.__init__(self)

        # Фон мнемосхемы
        self._svg_background = None

    def setSVGBackground(self, svg_filename):
        """
        Установить фон мнемосхемы.
        :param svg_filename: Полное имя SVG файла фона мнемосхемы.
        :return: True - фон успешно установлен.
        """
        if not svg_filename:
            log.warning(u'Не определен SVG файл фона мнемосхемы')
            return False

        if not os.path.exists(svg_filename):
            log.warning(u'Не найден SVG файл фона мнемосхемы <%s>' % svg_filename)
            return False

        self._svg_background = svg_filename
        return True

    def getAnchors(self):
        """
        Список якорей мнемосхемы.
        """
        log.warning(u'Не определен метод получения списка якорей мнемосхемы')
        return list()

    def getControls(self):
        """
        Список активных контролов мнемосхемы.
        """
        log.warning(u'Не определен метод получения списка контролов мнемосхемы')
        return list()

    def setControlPositions(self):
        """
        Метод расстановки и образмеривания контролов мнемосхемы согласно якорям.
        :return: True/False.
        """
        log.warning(u'Не определен метод расстановки и образмеривания контролов мнемосхемы')
        return False