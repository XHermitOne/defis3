#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль базовых классов моделей регистрацинных
временных (исторических) данных.
Для упрощения называемых ИСТОРИЕЙ.
"""

__version__ = (0, 1, 1, 1)


class icHistoryProto(object):
    """
    Базовый класс исторических данных.
    Организует общий интерфейс к объектам моделей исторических данных.
    """

    def get(self, start_dt, stop_dt):
        """
        Получить исторические данные указанного диапазона.
        :type start_dt: datetime.datetime.
        :param start_dt: Начальное дата-время диапазона кеширования.
        :type stop_dt: datetime.datetime.
        :param stop_dt: Конечная дата-время диапазона кеширования.
        :return: Список записей широкого формата указанного диапазона.
            Или None в случае ошибки.
        """
        return None

    def get_tag_data(self, tag_name, start_dt, stop_dt):
        """
        Получить исторические данные указанного диапазона по определенному тегу.
        :param tag_name: Имя тега.
        :type start_dt: datetime.datetime.
        :param start_dt: Начальное дата-время диапазона кеширования.
        :type stop_dt: datetime.datetime.
        :param stop_dt: Конечная дата-время диапазона кеширования.
        :return: Список записей {'dt': дата-время из указанного диапазона,
                                 'data': значение тега}.
            Или None в случае ошибки.
        """
        return None


class icWideHistoryProto(icHistoryProto):
    """
    Базовый класс исторических данных ШИРОКОГО формата.
    Широкий формат файла (Wide):
        В файле широкого формата в одной строке хранится
        одна дата, одно время и несколько значений тегов. На
        нижеследующей иллюстрации показано, как значения
        тегов хранятся в таком файле.
            ====================================================
            Date1 | Time1 | Tag1 value | Tag2 value | Tag3 value >=> Это один снимок данных
            Date2 | Time2 | Tag1 value | Tag2 value | Tag3 value
             ...  |  ...  |  ...       |  ...       |  ...
            DateN | TimeN | Tag1 value | Tag2 value | Tag3 value
            ====================================================
    """
    pass


class icNarrowHistoryProto(icHistoryProto):
    """
    Базовый класс исторических данных УЗКОГО формата.
    Узкий формат файла (Narrow):
        В файле узкого формата в одной строке хранится одна
        дата, одно время и одно значение тега. На
        нижеследующей иллюстрации показано, как значения
        тегов хранятся в таком файле.
        ==========================
        Date1 | Time1 | Tag1 value \
        Date1 | Time1 | Tag2 value  >=> Это один снимок данных
        Date1 | Time1 | Tag3 value /
        Date2 | Time2 | Tag1 value
        Date2 | Time2 | Tag2 value
        Date2 | Time2 | Tag3 value
        ==========================
    """
    pass
