#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер управления индикациеей на гео-картах.
Реализация сделана на базе 2GIS.
Документация по API 2GIS https://api.2gis.ru/doc/maps/ru/quickstart/.

В качестве индикатора могут выступать
пятна, указатели, окружности покрытия и т.п.

В качестве системы определения геолокации по адресу используется Yandex.
"""

from .. import double_gis

from . import map_indicator

__version__ = (0, 1, 1, 1)

# Спецификация компонента
SPC_IC_2GISMAPINDICATORMANAGER = {}


class ic2GISMapIndicatorManagerProto(map_indicator.icMapIndicatorManagerProto):
    """
    Индикатор карт 2GIS.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        map_indicator.icMapIndicatorManagerProto.__init__(self, *args, **kwargs)

        self.setRendering(double_gis)
