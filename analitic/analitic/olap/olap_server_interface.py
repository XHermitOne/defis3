#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Общий интерфейс всех OLAP серверов.
"""

from ic.log import log

__version__ = (0, 1, 1, 1)


class icOLAPServerInterface:
    """
    Общий интерфейс всех OLAP серверов.
    """
    def run(self):
        """
        Запуск сервера.
        :return: True/False.
        """
        log.warning(u'Не определен метод запуска OLAP сервера <%s>' % self.__class__.__name__)
        return False

    def stop(self):
        """
        Остановка сервера.
        :return: True/False.
        """
        log.warning(u'Не определен метод останова OLAP сервера <%s>' % self.__class__.__name__)
        return False

    def is_running(self):
        """
        Проверка того что OLAP сервер запущен.
        :return: True - сервер запущен, False - нет.
        """
        log.warning(u'Не определен метод проверки запущенного OLAP сервера <%s>' % self.__class__.__name__)
        return False

    def restart(self):
        """
        Перезапуск OLAP сервера.
        :return: True/False.
        """
        self.stop()
        return self.run()

    def get_response(self, *args, **kwargs):
        """
        Запрос получения данных от сервера.
        Функция слишком общая.
        Поэтому реализация ее должна обрабатывать различные запросы в
        зависимости от входящих данных.
        :return: Запрашиваемые данные или None в случае ошибки.
        """
        log.warning(u'Не определен метод получения данных от OLAP сервера <%s>' % self.__class__.__name__)
        return None
