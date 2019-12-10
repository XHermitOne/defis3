#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс управления круговым маркером.
"""

import jinja2
import json
from . import double_gis_util

from ic.log import log

__version__ = (0, 1, 1, 1)

MARKER_TEMPLATE = '''
DG.circleMarker({{ location }}).setRadius({{ radius }}).setStyle({{ options }}){% if popup %}.bindPopup('{{ popup }}'){% endif %}{% if tooltip %}.bindLabel('{{ tooltip }}'){% endif %}.addTo(map);
'''


class ic2GISCircleMarker(object):
    """
    Маркер-окружность.
    """
    _marker_template = jinja2.Template(MARKER_TEMPLATE)

    def __init__(self, location, radius=10,
                 popup=None, tooltip=None,
                 color='blue',
                 fill=True,
                 fill_color='blue',
                 **kwargs):
        """
        Конструктор. Создание маркера.
        :param location: Геолокация маркера.
        :param radius: Радиус окружности маркера.
        :param color: Цвет окружности.
        :param fill: Произвести заполнение внутренней области окружности?
        :param fill_color: Цвет заполнения окружности.
        :param popup: Текст всплывающей посказки маркера.
            Подсказка появляется по клику на маркере.
        :param tooltip: Текст всплывающей посказки маркера.
            Подсказка появляется при наведении мышки на маркер.
        """
        if location is None:
            # If location is not passed we center and zoom out.
            self.location = [0, 0]
        else:
            self.location = double_gis_util.validate_location(location)

        self.radius = int(radius)

        self.popup = popup
        self.tooltip = tooltip

        self.color = color
        self.fill = fill
        self.fill_color = fill_color

    def render(self, **kwargs):
        """
        Генерирует HTML-представление элемента.
        :return: Сгенерированное HTML представление карты.
        """
        options = dict(color=self.color)
        json_options = json.dumps(options)
        return self._marker_template.render(location=self.location,
                                            radius=self.radius,
                                            options=json_options,
                                            popup=self.popup,
                                            tooltip=self.tooltip,
                                            **kwargs)

    def add_to(self, geo_map):
        """
        Добавить маркер на карту.
        :param geo_map: Объект карты.
        :return: True/False.
        """
        try:
            geo_map.add_marker(self)
            return True
        except:
            log.fatal(u'Ошибка добавления кругового маркера на карту')
        return False


# Для поддержки рендеринга имена классов необходимо переопределить
CircleMarker = ic2GISCircleMarker
