#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль класса прототипа уровня каталога.
"""

# Имя папки уровня по умолчанию
DEFAULT_LEVEL_FOLDER_NAME = 'unknown'


class icCatalogLevelProto(object):
    """
    Класс прототипа уровня каталога.
    self._get_folder_name_func(obj) - Внешняя функция определения
        имени папки уровня по размещаемому в каталоге объекту.
    """

    def __init__(self):
        """
        Конструктор.
        """
        self._get_folder_name_func = None

    def getFolderName(self, obj):
        """
        Определить имя папки уровня по размещаемому объекту.
        @param obj: Размещаемый объект.
        @return: Строковое имя папки.
        """
        if self._get_folder_name_func:
            return self._get_folder_name_func(obj)
        if hasattr(self, 'name'):
            # Если определено имя уровня, то
            # оно является именем папки по умолчанию
            return self.name
        return DEFAULT_LEVEL_FOLDER_NAME