#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс управления маркером-указателем.
"""

import jinja2
from . import double_gis_util

from ic.log import log

MARKER_TEMPLATE = '''
DG.marker({{ location }}).addTo(map);
'''


class Marker(object):
    """
    Маркер-указатель.
    """
    _marker_template = jinja2.Template(MARKER_TEMPLATE)

    def __init__(self, location,
                 popup=None, tooltip=None,
                 icon=None,
                 **kwargs):
        """
        Конструктор. Создание маркера.
        @param location: Геолокация маркера.
        @param popup: Текст всплывающей посказки маркера.
            Подсказка появляется по клику на маркере.
        @param tooltip: Текст всплывающей посказки маркера.
            Подсказка появляется при наведении мышки на маркер.
        @param icon: Параметры иконки.
        """
        if location is None:
            # If location is not passed we center and zoom out.
            self.location = [0, 0]
        else:
            self.location = double_gis_util.validate_location(location)

        self.popup = popup
        self.tooltip = tooltip

    def render(self, **kwargs):
        """
        Генерирует HTML-представление элемента.
        @return: Сгенерированное HTML представление карты.
        """
        return self._marker_template.render(location=self.location,
                                            **kwargs)

    def add_to(self, geo_map):
        """
        Добавить маркер на карту.
        @param geo_map: Объект карты.
        @return: True/False.
        """
        try:
            geo_map.add_marker(self)
            return True
        except:
            log.fatal(u'Ошибка добавления маркера-указателя на карту')
        return False
