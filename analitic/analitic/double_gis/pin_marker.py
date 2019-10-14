#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс управления маркером-указателем.
"""

import jinja2
from . import double_gis_util
from . import marker_icon

from ic.log import log

__version__ = (0, 1, 2, 1)


MARKER_TEMPLATE = '''
DG.marker({{ location }}{% if icon %}, {icon: DG.icon({iconUrl: '{{ icon }}', iconSize: [32, 32], iconAnchor: [16, 31]})}{% endif %}).addTo(map)
{% if tooltip %}.bindLabel('{{ tooltip }}'){% endif %}
{% if popup %}.bindPopup('{{ popup }}'){% endif %}
;
'''


class ic2GISMarker(object):
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

        self.icon = marker_icon.get_marker_icon_filename(icon)

    def render(self, **kwargs):
        """
        Генерирует HTML-представление элемента.
        @return: Сгенерированное HTML представление карты.
        """
        return self._marker_template.render(location=self.location,
                                            icon=self.icon,
                                            popup=self.popup,
                                            tooltip=self.tooltip,
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


# Для поддержки рендеринга имена классов необходимо переопределить
Marker = ic2GISMarker
