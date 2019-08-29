#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс управления картой 2GIS.
"""

import jinja2

from . import double_gis_util

from ic.utils import extfunc

# Шаблон результирующего HTML документа
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>{{ title }}</title>
        <script src="https://maps.api.2gis.ru/2.0/loader.js?pkg=full"></script>
        {{ map }}
    </head>
    <body>
        <div record_id="map" style="width:{{ width[0] }}{{ width[1] }}; height:{{ height[0] }}{{ height[1] }}"></div>
    </body>
</html>
'''

# Шаблон карты
MAP_TEMPLATE = '''
<script type="text/javascript">
    var map;

    DG.then(function () {
        map = DG.map('map', {
            center: {{ location }},
            zoom: {{ zoom }}
        });
        
        {% for marker in markers %}
            {{ marker.render() }}
        {% endfor %}
    });
</script>
'''


class Map(object):
    """
    Класс управления картой 2GIS.
    """
    _map_template = jinja2.Template(MAP_TEMPLATE)
    _html_template = jinja2.Template(HTML_TEMPLATE)

    def __init__(self, location=None,
                 width='2000px', height='1300px',
                 left='0%', top='0%',
                 position=None,
                 tiles='OpenStreetMap',
                 attr=None,
                 min_zoom=0,
                 max_zoom=18,
                 zoom_start=10,
                 min_lat=-90,
                 max_lat=90,
                 min_lon=-180,
                 max_lon=180,
                 max_bounds=False,
                 crs='EPSG3857',
                 control_scale=False,
                 prefer_canvas=False,
                 no_touch=False,
                 disable_3d=False,
                 png_enabled=False,
                 zoom_control=True,
                 **kwargs):
        """
        Конструктор. Создание карты.
        @param location: Точка геолокации (ширина, долгота) центра карты.
        @param width: Ширина карты.
        @param height: Высота карты.
        @param left:
        @param top:
        @param position:
        @param tiles: Карта набора плиток для использования.
        @param attr: Атрибуция плитки карты; требуется только при передаче пользовательского URL плитки.
        @param min_zoom: Минимально допустимый уровень масштабирования для создаваемого слоя листов.
        @param max_zoom: Максимально допустимый уровень масштабирования для создаваемого слоя листов.
        @param zoom_start: Начальный уровень масштабирования для карты.
        @param min_lat:
        @param max_lat:
        @param min_lon:
        @param max_lon:
        @param max_bounds:
        @param crs:
        @param control_scale: Независимо от того, чтобы добавить масштаб управления на карте.
        @param prefer_canvas:
        @param no_touch:
        @param disable_3d:
        @param png_enabled:
        @param zoom_control: Отображение управления масштабированием на карте.
        """
        if location is None:
            # If location is not passed we center and zoom out.
            self.location = [0, 0]
            zoom_start = 1
        else:
            self.location = double_gis_util.validate_location(location)

        # Размеры
        self.width = double_gis_util.parse_size(width)
        self.height = double_gis_util.parse_size(height)
        self.left = double_gis_util.parse_size(left)
        self.top = double_gis_util.parse_size(top)
        # self.position = position

        # Масштабирование
        self.zoom = zoom_start

        # Маркеры
        self.markers = list()

    def add_marker(self, marker):
        """
        Добавить маркер на карту.
        @param marker: Объект маркера.
        @return: True/False.
        """
        self.markers.append(marker)
        return True

    def render(self, **kwargs):
        """
        Генерирует HTML-представление элемента.
        @return: Сгенерированное HTML представление карты.
        """
        return self._map_template.render(location=self.location,
                                         zoom=self.zoom,
                                         markers=self.markers,
                                         **kwargs)

    def save(self, html_filename):
        """
        Сохранить карту в HTML файле.
        @param html_filename: Полное имя HTML файла.
        @return: True/False.
        """
        map_html = self.render()
        html = self._html_template.render(map=map_html,
                                          width=self.width,
                                          height=self.height)

        return extfunc.save_file_text(html_filename, html)
