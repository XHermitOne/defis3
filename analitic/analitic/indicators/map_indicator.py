#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Абстрактный индикатор карт.

Индикатор карт представляет собой информацию для отображения на
картах Yandex, Google или т.п. ГИС.
В качестве индикатора могут выступать
пятна, указатели, окружности покрытия и т.п.
"""

from ic.log import log

__version__ = (0, 1, 1, 1)

# Коэффициент масштаба по умолчанию
DEFAULT_ZOOM = 14


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
