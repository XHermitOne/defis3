#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Абстрактный индикатор карт.

Индикатор карт представляет собой информацию для отображения на
картах Yandex, Google или т.п. ГИС.
В качестве индикатора могут выступать
пятна, указатели, окружности покрытия и т.п.
"""

__version__ = (0, 1, 1, 1)


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
