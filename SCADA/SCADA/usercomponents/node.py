#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль базовых классов узлов-контроллеров SCADA системы.
"""

from ic.log import log

__version__ = (0, 0, 3, 1)

# Проверка наличия обрамляющих сигнатур топика
DO_CONTROL_TOPIC_SIGNATURES = True
TOPIC_BEGIN_SIGNATURE = u'['
TOPIC_END_SIGNATURE = u']'


class icSCADANodeProto(object):
    """
    Базовый класс узла-контроллера SCADA системы.
    Организует общий интерфейс к объектам узлов-контроллеров SCADA системы.
    """
    def read_value(self, address):
        """
        Чтение значения по адресу.
        @param address: Адрес значения в узле.
        @return: Запрашиваемое значение или None в случае ошибки чтения.
        """
        log.error(u'Функция чтения данных по адресу не реализована в <%s>' % self.__class__.__name__)
        return None

    def write_value(self, address, value):
        """
        Запись значения по адресу.
        @param address: Адрес значения в узле.
        @param value: Записываемое значение.
        @return: True - запись прошла успешно/False - ошибка.
        """
        log.error(u'Функция записи данных по адресу не реализована в <%s>' % self.__class__.__name__)
        return None

    def read_values(self, addresses):
        """
        Чтение значений по адресам.
        @param addresses: Список адресов значений в узле.
        @return: Список запрашиваемых значений или None в случае ошибки чтения.
        """
        log.error(u'Функция чтения списка данных по адресу не реализована в <%s>' % self.__class__.__name__)
        return None

    def readTags(self, *tags):
        """
        Прочитать список тегов.
        @param tags: Список объектов тегов.
        @return: True/False.
        """
        log.error(u'Функция чтения списка тегов не реализована в <%s>' % self.__class__.__name__)
        return False

    def setEnv(self, **environment):
        """
        Добавить дополнительное окружение узла.
        Необходимо для выполнения вычисляемых тегов.
        @param environment: Словарь дополнительных переменных окружения узла.
        @return: True/False.
        """
        if not hasattr(self, '_node_environment'):
            self._node_environment = dict()
        self._node_environment.update(environment)
        return True

    def getEnv(self):
        """
        Дополнительное окружение узла.
        Необходимо для выполнения вычисляемых тегов.
        @return: Словарь дополнительных переменных окружения узла.
        """
        if not hasattr(self, '_node_environment'):
            return dict()
        return self._node_environment

    def getSCADAEngine(self):
        """
        Объект SCADA движка. Берется из дополнительного контекста.
        @return: Объект SCADA движка или None если движок
            не был определен в дополнительном контексте объекта.
        """
        environment = self.getEnv()
        return environment.get('SCADA_ENGINE', None)
