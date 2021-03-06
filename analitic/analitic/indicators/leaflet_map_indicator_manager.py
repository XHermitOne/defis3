#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер управления индикациеей на гео-картах.
Реализация сделана на базе Leaflet (https://leafletjs.com/).
Python API для Leaflet - библиотека folium.
Установка: pip3 install folium.
Примеры использования библиотеки folium:
https://python-visualization.github.io/folium
Примеры использования:
https://python-visualization.github.io/folium/quickstart.html

В качестве индикатора могут выступать
пятна, указатели, окружности покрытия и т.п.

В качестве системы определения геолокации по адресу используется Yandex.
"""

import folium

from . import map_indicator

__version__ = (0, 1, 1, 1)

# Спецификация компонента
SPC_IC_LEAFLETMAPINDICATORMANAGER = {}


class icLeafletMapIndicatorManagerProto(map_indicator.icMapIndicatorManagerProto):
    """
    Индикатор карт Leaflet.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        map_indicator.icMapIndicatorManagerProto.__init__(self, *args, **kwargs)

        self.setRendering(folium)
