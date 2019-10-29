#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Абстрактный индикатор карт.

Индикатор карт представляет собой информацию для отображения на
картах Yandex, Google или т.п. ГИС.
В качестве индикатора могут выступать
пятна, указатели, окружности покрытия и т.п.

Получение геолокации по умолчанию происходит с помощью Yandex Maps.
Для определения геолокаций необходимо испоьзовать в запросах к Web сервису API Key.
Можно получить через кабинет разработчика.
Суточное ограничение на определение геолокаций адресов - 25000.
Кабинет разработчика Yandex: https://developer.tech.yandex.ru/services/
API Key храниться в отдельном файле API_KEY_YANDEX_FILENAME.
"""

import os.path
import uuid

from ic.log import log
from ic.utils import filefunc
from ic.utils import wxfunc
from ic.utils import txtfunc

try:
    import yandex_maps
except ImportError:
    log.error(u'Ошибка импорта yandex_maps для определения геолокации по адресу')
    yandex_maps = None

import urllib.request
import urllib.parse
import json

__version__ = (0, 1, 1, 1)

# Коэффициент масштаба по умолчанию
DEFAULT_ZOOM = 14

# --- Функции определения геолокации по адресу ---
GEO_LOCATOR_DEFAULT = True

# Кеш геолокатора
# В кеше сохраняется соответствие адрес->(широта, долгота)
GEO_LOCATOR_CACHE = None

# Ключ для геолокации Яндекса
API_KEY_YANDEX_FILENAME = os.path.join(os.path.dirname(__file__), 'api_key_yandexmaps.txt')
YANDEX_GEO_LOCATOR_API_KEY = txtfunc.load_file_text(API_KEY_YANDEX_FILENAME).strip()
YANDEX_GEO_LACATOR_URL_FMT = 'http://geocode-maps.yandex.ru/1.x/?geocode=%s&apikey=%s&format=json'

API_KEY_2GIS_FILENAME = os.path.join(os.path.dirname(__file__), 'api_key_2gis.txt')
DOUBLEGIS_GEO_LOCATOR_API_KEY = txtfunc.load_file_text(API_KEY_2GIS_FILENAME).strip()
DOUBLEGIS_GEO_LACATOR_URL_FMT = 'https://catalog.api.2gis.ru/geo/search?q=%s&format=json&limit=1&version=2.0&key=%s'


def get_default_geolocations(address_query, geo_key=None):
    """
    Получить все данные геолокации по запрашиваемому адресу.
    @param address_query: Запрашиваемый адрес.
        Например:
            Москва, улица Гагарина, дом 10.
    @param geo_key: Ключ API геолокатора.
    @return: Список [(широта, долгота),...] данных геолокации или пустой список в случае ошибки.
    """
    if geo_key is None:
        geo_key = YANDEX_GEO_LOCATOR_API_KEY

    try:
        address = urllib.parse.quote(address_query)
        url = YANDEX_GEO_LACATOR_URL_FMT % (address, geo_key)
        log.debug(u'URL получения геоданных <%s>' % url)
        response = urllib.request.urlopen(url)
        data = response.read()
        geo_location_data = json.loads(data)

        find_geo = geo_location_data.get('response',
                                         dict()).get('GeoObjectCollection',
                                                     dict()).get('featureMember',
                                                                 list())
        str_geo_locations = [item.get('GeoObject', dict()).get('Point', dict()).get('pos', None) for item in find_geo]
        # ВНИМАНИЕ! В API Yandex Maps сначала стоит долгота, а затем широта,
        # а правильно для использования наоборот---------V
        geo_locations = [tuple([float(pos) for pos in reversed(location.split(' '))]) if location is not None else (None, None) for location in str_geo_locations]
        return geo_locations
    except Exception as e:
        log.fatal(u'Yandex default. Ошибка получения данных геолокации по адресу <%s>' % address_query)
    return list()


def get_default_geolocation(address_query, geo_key=None, item=0, bCache=True):
    """
    Получить все данные геолокации по запрашиваемому адресу.
    @param address_query: Запрашиваемый адрес.
        Например:
            Москва, улица Гагарина, дом 10.
    @param geo_key: Ключ API геолокатора.
    @param item: Индекс выбираемого элемента.
    @param bCache: Использовать внутренний кеш?
    @return: (широта, долгота) данных геолокации или (None, None) в случае ошибки.
    """
    if bCache:
        global GEO_LOCATOR_CACHE
        if GEO_LOCATOR_CACHE is None:
            GEO_LOCATOR_CACHE = dict()
        if address_query in GEO_LOCATOR_CACHE:
            # Если такой адрес есть в кеше, то берем из кеша
            return GEO_LOCATOR_CACHE[address_query]

    geo_locations = get_default_geolocations(address_query, geo_key=geo_key)
    if geo_locations and item < len(geo_locations):
        if bCache:
            # Сохраняем в кеше
            GEO_LOCATOR_CACHE[address_query] = geo_locations[item]
        return geo_locations[item]
    return None, None


def get_yandexmaps_geolocation(address_query, geo_key=None, bCache=True):
    """
    Получить данные геолокации по запрашиваемому адресу.
    Используется библиотека https://github.com/begyy/Yandexmaps.
    Установка: pip3 install Yandexmaps.
    @param address_query: Запрашиваемый адрес.
        Например:
            Москва, улица Гагарина, дом 10.
    @param geo_key: Ключ API геолокатора.
    @param bCache: Использовать внутренний кеш?
    @return: (широта, долгота) данных геолокации или [None, None] в случае ошибки.
    """
    if bCache:
        global GEO_LOCATOR_CACHE
        if GEO_LOCATOR_CACHE is None:
            GEO_LOCATOR_CACHE = dict()
        if address_query in GEO_LOCATOR_CACHE:
            # Если такой адрес есть в кеше, то берем из кеша
            return GEO_LOCATOR_CACHE[address_query]

    try:
        if not yandex_maps:
            log.warning(u'Не установлена библиотека Yandexmaps. Установить: pip3 install Yandexmaps')
            return None, None
        yandex = yandex_maps.Yandexmaps()
        geo_location = yandex.address(address=address_query)
        # ВНИМАНИЕ! В API Yandex Maps сначала стоит долгота, а затем широта,
        # а правильно для использования наоборот
        # --------------V
        geo_location_tuple = tuple(reversed(geo_location))
        if bCache:
            # Сохраняем в кеше
            GEO_LOCATOR_CACHE[address_query] = geo_location_tuple
        return geo_location
    except Exception as e:
        log.fatal(u'Yandexmaps. Ошибка получения данных геолокации по адресу <%s>' % address_query)
    return None, None


def get_2gis_geolocations(address_query, geo_key=None, bCache=True):
    """
    Получить все данные геолокации по запрашиваемому адресу.
    ВНИМАНИЕ! Функция не отлажена!!!!!
    @param address_query: Запрашиваемый адрес.
        Например:
            Москва, улица Гагарина, дом 10.
    @param geo_key: Ключ API геолокатора.
    @param bCache: Использовать внутренний кеш?
    @return: Список [(широта, долгота),...] данных геолокации или пустой список в случае ошибки.
    """
    if bCache:
        global GEO_LOCATOR_CACHE
        if GEO_LOCATOR_CACHE is None:
            GEO_LOCATOR_CACHE = dict()
        if address_query in GEO_LOCATOR_CACHE:
            # Если такой адрес есть в кеше, то берем из кеша
            return GEO_LOCATOR_CACHE[address_query]

    if geo_key is None:
        geo_key = DOUBLEGIS_GEO_LOCATOR_API_KEY

    try:
        address = urllib.parse.quote(address_query)
        url = DOUBLEGIS_GEO_LACATOR_URL_FMT % (address, geo_key)
        response = urllib.request.urlopen(url)
        data = response.read()
        geo_location_data = json.loads(data)

        find_geo = geo_location_data.get('response',
                                         dict()).get('GeoObjectCollection',
                                                     dict()).get('featureMember',
                                                                 list())
        str_geo_locations = [item.get('GeoObject', dict()).get('Point', dict()).get('pos', None) for item in find_geo]
        # ВНИМАНИЕ! В API Yandex Maps сначала стоит долгота, а затем широта,
        # а правильно для использования наоборот---------V
        geo_locations = [tuple([float(pos) for pos in reversed(location.split(' '))]) if location is not None else (None, None) for location in str_geo_locations]
        return geo_locations
    except Exception as e:
        log.fatal(u'2GIS. Ошибка получения данных геолокации по адресу <%s>' % address_query)
    return list()


class icMapIndicator(object):
    """
    Абстрактный индикатор карт.
    Реализует общий интерфейс к индикаторам карт.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        pass

    def getMap(self):
        """
        Объект карты.
        """
        return None

    def getHTMLFilename(self):
        """
        Текущий HTML файл браузера просмотра карт.
        """
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
        return list()

    def findGeoLocation(self, address_query):
        """
        Получить геграфические данные широты и долготы по запросу адреса.
        @param address_query: Запрос адреса в виде:
            Москва, улица Гагарина, дом 10.
        @return: Кортеж: Географическая широта, географическая долгота
            либо (None, None) в случае ошибки.
        """
        return None, None

    def getMapBitmap(self, geo_latitude, geo_longitude, img_filename=None):
        """
        Получить карту в виде картинки по заданным географическим координатам.
        @param geo_latitude: Географическая широта.
        @param geo_longitude: Географическая долгота.
        @param img_filename: Файл образа для сохранения.
            Если не указан, то файл автоматически не сохраняется.
        @return: wx.Bitmap запрашиваемой карты или None в случае ошибки.
        """
        return None

    def setCircleMarker(self, geo_latitude, geo_longitude,
                        radius=100, color='blue',
                        is_fill=True, fill_color='blue',
                        popup_text=u'', tooltip_text=u''):
        """
        Добавление на карту маркера в виде окружности.
        @param geo_latitude: Географическая широта.
        @param geo_longitude: Географическая долгота.
        @param radius: Радиус окружности.
        @param color: Цвет окружности.
        @param is_fill: Произвести заполнение внутренней области окружности?
        @param fill_color: Цвет заполнения окружности.
        @param popup_text: Текст всплывающей посказки маркера.
            Подсказка появляется по клику на маркере.
        @param tooltip_text: Текст всплывающей посказки маркера.
            Подсказка появляется при наведении мышки на маркер.
        @return: True/False.
        """
        log.warning(u'Метод setCircleMarker компонента <%s> не определен' % self.__class__.__name__)
        return False

    def setPinMarker(self, geo_latitude, geo_longitude,
                     color='blue', icon=None,
                     popup_text=u'', tooltip_text=u''):
        """
        Добавление на карту маркера-указателя.
        @param geo_latitude: Географическая широта.
        @param geo_longitude: Географическая долгота.
        @param color: Цвет маркера.
        @param icon: Иконка маркера.
        @param popup_text: Текст всплывающей посказки маркера.
            Подсказка появляется по клику на маркере.
        @param tooltip_text: Текст всплывающей посказки маркера.
            Подсказка появляется при наведении мышки на маркер.
        @return: True/False.
        """
        log.warning(u'Метод setPinMarker компонента <%s> не определен' % self.__class__.__name__)
        return False

    def setCircleMarkerByAddress(self, address,
                                radius=100, color='blue',
                                is_fill=True, fill_color='blue',
                                popup_text=u'', tooltip_text=u''):
        """
        Добавление на карту маркера в виде окружности по адресу.
        @param address: Запрашиваемый адрес.
            Нaпример:
                Москва, улица Гагарина, дом 10.
        @param radius: Радиус окружности.
        @param color: Цвет окружности.
        @param is_fill: Произвести заполнение внутренней области окружности?
        @param fill_color: Цвет заполнения окружности.
        @param popup_text: Текст всплывающей посказки маркера.
            Подсказка появляется по клику на маркере.
        @param tooltip_text: Текст всплывающей посказки маркера.
            Подсказка появляется при наведении мышки на маркер.
        @return: True/False.
        """
        geo_latitude, geo_longitude = self.findGeoLocation(address_query=address)
        return self.setCircleMarker(geo_latitude, geo_longitude,
                                    radius=radius, color=color,
                                    is_fill=is_fill, fill_color=fill_color,
                                    popup_text=popup_text, tooltip_text=tooltip_text)

    def setPinMarkerByAddress(self, address,
                              color='blue', icon=None,
                              popup_text=u'', tooltip_text=u''):
        """
        Добавление на карту маркера-указателя по адресу.
        @param address: Запрашиваемый адрес.
            Нaпример:
                Москва, улица Гагарина, дом 10.
        @param color: Цвет маркера.
        @param icon: Иконка маркера.
        @param popup_text: Текст всплывающей посказки маркера.
            Подсказка появляется по клику на маркере.
        @param tooltip_text: Текст всплывающей посказки маркера.
            Подсказка появляется при наведении мышки на маркер.
        @return: True/False.
        """
        geo_latitude, geo_longitude = self.findGeoLocation(address_query=address)
        return self.setPinMarker(geo_latitude, geo_longitude,
                                 color=color, icon=icon,
                                 popup_text=popup_text, tooltip_text=tooltip_text)

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
        log.warning(u'Метод saveMapBrowserFile компонента <%s> не определен' % self.__class__.__name__)
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
        log.warning(u'Метод saveMapBrowserFileByAddress компонента <%s> не определен' % self.__class__.__name__)
        return None

    def createMap(self, geo_latitude, geo_longitude,
                  zoom=DEFAULT_ZOOM,
                  html_filename=None, bReWrite=False):
        """
        Создать объект карты.
        @param geo_latitude: Географическая широта.
        @param geo_longitude: Географическая долгота.
        @param zoom: Коэффициент масштаба по умолчанию.
        @param html_filename: Имя сохраняемого файла.
            Если не указано, то генерируется.
        @param bReWrite: Перезаписать существующий файл?
        @return: Объект карты или None в случае ошибки.
        """
        log.warning(u'Метод createMap компонента <%s> не определен' % self.__class__.__name__)
        return None

    def createMapByAddress(self, address,
                           zoom=DEFAULT_ZOOM,
                           html_filename=None, bReWrite=False):
        """
        Создать объект карты по адресу.
        @param address: Запрашиваемый адрес.
            Нaпример:
                Москва, улица Гагарина, дом 10.
        @param zoom: Коэффициент масштаба по умолчанию.
        @param html_filename: Имя сохраняемого файла.
            Если не указано, то генерируется.
        @param bReWrite: Перезаписать существующий файл?
        @return: Объект карты или None в случае ошибки.
        """
        log.warning(u'Метод createMapByAddress компонента <%s> не определен' % self.__class__.__name__)
        return None


class icMapIndicatorManagerProto(icMapIndicator):
    """
    Абстрактный менеджер индикатора карт.
    Реализует общий интерфейс к индикаторам карт.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        icMapIndicator.__init__(self, *args, **kwargs)

        # Библиотека рендеринга карт
        self._rendering = None
        # Контрол браузера карты
        self._browser = None

        # Объект управления картой
        self._geo_map = None

        # Текущий HTML файл браузера просмотра карт
        self._html_filename = None

    def setRendering(self, rendering):
        """
        Установить библиотеку рендеринга.
        Может быть библиотека folium либо собственная библиотека double_gis.
        @param rendering: Библиотека рендеринга карт.
            По умолчанию собственная библиотека double_gis.
        """
        if rendering is None:
            from .. import double_gis
            rendering = double_gis
        self._rendering = rendering

    def getMap(self):
        """
        Объект карты.
        """
        return self._geo_map

    def getHTMLFilename(self):
        """
        Текущий HTML файл браузера просмотра карт.
        """
        return self._html_filename

    def setHTMLFilename(self, html_filename):
        """
        Текущий HTML файл браузера просмотра карт.
        """
        self.setMapBrowserFile(html_filename=html_filename)

    def findGeoLocations(self, address_query):
        """
        Получить геграфические данные широты и долготы по запросу адреса.
        @param address_query: Запрос адреса в виде:
            Москва, улица Гагарина, дом 10.
        @return: Список кортежей найденных локаций:
            (Географическая широта, географическая долгота)
            либо (None, None) в случае ошибки.
        """
        if yandex_maps and not GEO_LOCATOR_DEFAULT:
            geo_locations = [get_yandexmaps_geolocation(address_query)]
        else:
            geo_locations = get_default_geolocations(address_query)
        return geo_locations

    def findGeoLocation(self, address_query, item=0):
        """
        Получить геграфические данные широты и долготы по запросу адреса.
        @param address_query: Запрос адреса в виде:
            Москва, улица Гагарина, дом 10.
        @param item: Индекс выбранного элемента.
        @return: Кортеж: Географическая широта, географическая долгота
            либо (None, None) в случае ошибки.
        """
        if yandex_maps and not GEO_LOCATOR_DEFAULT:
            geo_location = get_yandexmaps_geolocation(address_query)
        else:
            geo_location = get_default_geolocation(address_query, item=item)
        return geo_location

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
        gen_path = os.path.join(filefunc.getPrjProfilePath(), gen_uuid + '.html')
        return gen_path

    def createMap(self, geo_latitude, geo_longitude,
                  zoom=DEFAULT_ZOOM,
                  html_filename=None, bReWrite=False, bAutoSave=True):
        """
        Создать объект карты.
        @param geo_latitude: Географическая широта.
        @param geo_longitude: Географическая долгота.
        @param zoom: Коэффициент масштаба по умолчанию.
        @param html_filename: Имя сохраняемого файла.
            Если не указано, то генерируется.
        @param bReWrite: Перезаписать существующий файл?
        @param bAutoSave: Автоматически сохранить файл?
        @return: Объект карты или None в случае ошибки.
        """
        if geo_latitude in (None, 0) or geo_longitude in (None, 0):
            log.warning(u'Не полное определение геолокации <%s : %s>' % (geo_latitude, geo_longitude))
            return None

        try:
            self._geo_map = self._rendering.Map(location=[geo_latitude, geo_longitude],
                                                zoom_start=zoom)
            log.info(u'Создан объект карты. Локация [%s x %s]' % (geo_latitude, geo_longitude))
            if bAutoSave:
                self.saveMapBrowserFile(geo_latitude, geo_longitude, zoom=zoom,
                                        html_filename=html_filename, bReWrite=bReWrite)
        except:
            log.fatal(u'Ошибка создания объекта карты')
            self._geo_map = None
        return self._geo_map

    def createMapByAddress(self, address,
                           zoom=DEFAULT_ZOOM,
                           html_filename=None, bReWrite=False,
                           bAutoSave=True):
        """
        Создать объект карты по адресу.
        @param address: Запрашиваемый адрес.
            Нaпример:
                Москва, улица Гагарина, дом 10.
        @param zoom: Коэффициент масштаба по умолчанию.
        @param html_filename: Имя сохраняемого файла.
            Если не указано, то генерируется.
        @param bReWrite: Перезаписать существующий файл?
        @param bAutoSave: Автоматически сохранить файл?
        @return: Объект карты или None в случае ошибки.
        """
        geo_latitude, geo_longitude = self.findGeoLocation(address_query=address)
        return self.createMap(geo_latitude, geo_longitude, zoom=zoom,
                              html_filename=html_filename, bReWrite=bReWrite,
                              bAutoSave=bAutoSave)

    def saveMapBrowserFile(self, geo_latitude, geo_longitude,
                           zoom=DEFAULT_ZOOM,
                           html_filename=None, bReWrite=False):
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
            if self._geo_map is None:
                self._geo_map = self._rendering.Map(location=[geo_latitude, geo_longitude],
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
            # log.debug(u'Установка в браузере <%s>' % url)
            self._browser.LoadURL(url)
            return True
        except:
            log.fatal(u'Ошибка открытия в браузере карт URL <%s>' % url)
        return False

    def setCircleMarker(self, geo_latitude, geo_longitude,
                        radius=100, color='blue',
                        is_fill=True, fill_color='blue',
                        popup_text=u'', tooltip_text=u''):
        """
        Добавление на карту маркера в виде окружности.
        @param geo_latitude: Географическая широта.
        @param geo_longitude: Географическая долгота.
        @param radius: Радиус окружности.
        @param color: Цвет окружности.
        @param is_fill: Произвести заполнение внутренней области окружности?
        @param fill_color: Цвет заполнения окружности.
        @param popup_text: Текст всплывающей посказки маркера.
            Подсказка появляется по клику на маркере.
        @param tooltip_text: Текст всплывающей посказки маркера.
            Подсказка появляется при наведении мышки на маркер.
        @return: True/False.
        """
        if self._geo_map is not None:
            try:
                # Приведение цветов к текстовому формату
                color = wxfunc.wxColour2StrRGB(color) if color else None
                fill_color = wxfunc.wxColour2StrRGB(color) if fill_color else None

                marker = self._rendering.CircleMarker(location=[geo_latitude, geo_longitude],
                                                      radius=radius,
                                                      popup=popup_text if popup_text else None,
                                                      color=color if color else None,
                                                      fill=is_fill,
                                                      fill_color=fill_color if fill_color else None,
                                                      tooltip=tooltip_text if tooltip_text else None)
                marker.add_to(self._geo_map)
                log.debug(u'Добавлен маркер-окружность. Локация [%s x %s]' % (geo_latitude, geo_longitude))
            except:
                log.fatal(u'Ошибка добавления на карту маркера-окружности')
        else:
            log.warning(u'Не определен объект карты для добавления маркера-окружности')
        return False

    def setPinMarker(self, geo_latitude, geo_longitude,
                     color='blue', icon=None,
                     popup_text=u'', tooltip_text=u''):
        """
        Добавление на карту маркера-указателя.
        @param geo_latitude: Географическая широта.
        @param geo_longitude: Географическая долгота.
        @param color: Цвет маркера.
        @param icon: Иконка маркера.
        @param popup_text: Текст всплывающей посказки маркера.
            Подсказка появляется по клику на маркере.
        @param tooltip_text: Текст всплывающей посказки маркера.
            Подсказка появляется при наведении мышки на маркер.
        @return: True/False.
        """
        if self._geo_map is not None:
            try:
                # Приведение цветов к текстовому формату
                color = wxfunc.wxColour2StrRGB(color) if color else None

                # marker_icon = None
                # if icon and color:
                #     marker_icon = folium.Icon(color=color, icon=icon)
                # elif icon and color:
                #     marker_icon = folium.Icon(color=color)

                marker = self._rendering.Marker(location=[geo_latitude, geo_longitude],
                                                popup=popup_text if popup_text else None,
                                                tooltip=tooltip_text if tooltip_text else None,
                                                icon=icon)
                marker.add_to(self._geo_map)
                # log.debug(u'Добавлен маркер-указатель. Локация [%s x %s]' % (geo_latitude, geo_longitude))
                return True
            except:
                log.fatal(u'Ошибка добавления на карту маркера-указателя')
        else:
            log.warning(u'Не определен объект карты для добавления маркера-указателя')
        return False
