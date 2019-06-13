#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер управления индикациеей на гео-картах.
Реализация сделана на базе Leaflet (https://leafletjs.com/).
Python API для Leaflet - библиотека folium.
Установка: pip3 install folium.
Примеры использования библиотеки folium:
https://python-visualization.github.io/folium/quickstart.html

В качестве индикатора могут выступать
пятна, указатели, окружности покрытия и т.п.

В качестве системы определения геолокации по адресу используется Yandex.
"""

import os.path
import folium
import json
import urllib.request
import urllib.parse
import uuid

from . import map_indicator

from ic.log import log
from ic.utils import ic_file

__version__ = (0, 1, 1, 1)

# Спецификация компонента
SPC_IC_LEAFLETMAPINDICATORMANAGER = {}

# Ключ для геолокации Яндекса
GEO_LOCATOR_KEY = 'AHqsEk4BAAAAekkFTAMA9DGkZfo_WT9ci8K8X286J9ILWjIAAAAAAAAAAABhqxW74U1xylQQhCYKzVIxsQBPTQ=='
GEO_LACATOR_URL_FMT = 'http://geocode-maps.yandex.ru/1.x/?geocode=%s&key=%s&format=json'

# Коэффициент масштаба по умолчанию
DEFAULT_ZOOM = 14


class icLeafletMapIndicatorManagerProto(map_indicator.icMapIndicator):
    """
    Абстрактный индикатор карт.
    Реализует общий интерфейс к индикаторам карт.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        map_indicator.icMapIndicator.__init__(self, *args, **kwargs)

        # Контрол браузера карты
        self._browser = None

        # Объект управления картой
        self._geo_map = None

        # Текущий HTML файл браузера просмотра карт
        self._html_filename = None

    def get_geolocation(self, address_query, geo_key=None):
        """
        Получить данные геолокации по запрашиваемому адресу.
        @param address_query: Запрашиваемый адрес.
        @param geo_key: Ключ геолокатора.
        @return: Структура данных геолокации или None в случае ошибки.
        """
        if geo_key is None:
            geo_key = GEO_LOCATOR_KEY

        try:
            address = urllib.parse.quote(address_query)
            url = GEO_LACATOR_URL_FMT % (address, geo_key)
            response = urllib.request.urlopen(url)
            data = response.read()
            return json.loads(data)
        except Exception as e:
            log.fatal(u'Ошибка получения данных геолокации по адресу')
        return None

    def findGeoLocations(self, address_query):
        """
        Получить геграфические данные широты и долготы по запросу адреса.
        @param address_query: Запрос адреса в виде:
            Москва, улица Гагарина, дом 10.
        @return: Список кортежей найденных локаций:
            (Географическая широта, географическая долгота)
            либо (None, None) в случае ошибки.
        """
        try:
            geo_location_data = self.get_geolocation(address_query)
            find_geo = geo_location_data.get('response', dict()).get('GeoObjectCollection', dict()).get('featureMember', list())
            str_geo_locations = [item.get('GeoObject', dict()).get('Point', dict()).get('pos', None) for item in find_geo]
            # ВНИМАНИЕ! В API Yandex Maps сначала стоит долгота, а затем широта,
            # а правильно для использования наоборот---------V
            geo_locations = [tuple([float(pos) for pos in reversed(location.split(' '))]) if location is not None else (None, None) for location in str_geo_locations]
            return geo_locations
        except:
            log.fatal(u'Ошибка определения геолокаций по запросу адреса <%s>' % address_query)
        return list()

    def findGeoLocation(self, address_query, item=0):
        """
        Получить геграфические данные широты и долготы по запросу адреса.
        @param address_query: Запрос адреса в виде:
            Москва, улица Гагарина, дом 10.
        @param item: Индекс выбранного элемента.
        @return: Кортеж: Географическая широта, географическая долгота
            либо (None, None) в случае ошибки.
        """
        geo_locations = self.findGeoLocations(address_query)
        if geo_locations and item < len(geo_locations):
            return geo_locations[item]
        return None, None

    def setBrowser(self, browser):
        """
        Установить браузер для отображения карты.
        @param browser: Контрол браузера для отображения карты.
        """
        self._browser = browser

    def genMapBrowserFilename(self):
        """
        Сгенерировать имя HTML файла браузера для отображения карты.
        @return: Полное имя файла для отображения карты.
        """
        gen_uuid = str(uuid.uuid4())
        gen_path = os.path.join(ic_file.getPrjProfilePath(), gen_uuid+'.html')
        return gen_path

    def saveMapBrowserFile(self, geo_latitude, geo_longitude,
                           zoom=DEFAULT_ZOOM, html_filename=None, bReWrite=False):
        """
        Сохранить HTML файл для отображения карты.
        @param geo_latitude: Географическая широта.
        @param geo_longitude: Географическая долгота.
        @param zoom: Коэффициент масштаба по умолчанию.
        @param html_filename: Имя сохраняемого файла.
            Если не указано, то генерируется.
        @param bReWrite: Перезаписать существующий файл?
        @return: Полное имя HTML файла или None в случае ошибки.
        """
        if html_filename is None:
            html_filename = self.genMapBrowserFilename()
            self._html_filename = html_filename

        if os.path.exists(html_filename) and not bReWrite:
            # Если файл существует и перезаписывать его не надо,
            # то ничего не делаем
            return html_filename

        if geo_latitude is None or geo_longitude is None:
            log.warning(u'Не полное определение геолокации <%s : %s>' % (geo_latitude, geo_longitude))
            return None

        try:
            self._geo_map = folium.Map(location=[geo_latitude, geo_longitude],
                                       zoom_start=zoom)
            self._geo_map.save(html_filename)
            return html_filename
        except:
            log.fatal(u'Ошибка сохранения файла <%s> для отображения карты' % html_filename)
        return None

    def saveMapBrowserFileByAddress(self, address, zoom=DEFAULT_ZOOM,
                                    html_filename=None, bReWrite=False):
        """
        Сохранить HTML файл для отображения карты по запросу адреса.
        @param address: Запрашиваемый адрес.
            Нaпример:
                Москва, улица Гагарина, дом 10.
        @param zoom: Коэффициент масштаба по умолчанию.
        @param html_filename: Имя сохраняемого файла.
            Если не указано, то генерируется.
        @param bReWrite: Перезаписать существующий файл?
        @return: Полное имя HTML файла или None в случае ошибки.
        """
        geo_latitude, geo_longitude = self.findGeoLocation(address_query=address)
        return self.saveMapBrowserFile(geo_latitude, geo_longitude,
                                       zoom=zoom, html_filename=html_filename,
                                       bReWrite=bReWrite)

    def setMapBrowserFile(self, html_filename=None):
        """
        Установить в браузере HTML файл для просмотра карт.
        @param html_filename: Имя HTML файла браузера для просмотра карт.
            Если не указано, то берется последнее сгенерированное имя.
        @return: True/False.
        """
        if html_filename:
            self._html_filename = html_filename

        if not os.path.exists(self._html_filename):
            log.warning(u'HTML файл <%s> браузера просмотра карт не найден' % self._html_filename)
            return False

        url = 'file://%s' % self._html_filename
        try:
            self._browser.LoadURL(url)
            return True
        except:
            log.fatal(u'Ошибка открытия в браузере карт URL <%s>' % url)
        return False
