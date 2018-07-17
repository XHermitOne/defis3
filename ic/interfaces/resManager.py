#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Интерфейс для менеджеров ресурсных файлов.
"""

# === Подключение библиотек ===
# === Константы ===

__version__ = (0, 0, 0, 3)


# === Описание классов ===
class ResourceManagerInterface:
    """
    Интерфейс для менеджеров ресурсных файлов.
    """

    def __init__(self):
        """
        Конструктор.
        """
        pass

    def new(self):
        """
        Метод создания ресурса.
        """
        pass

    def save(self):
        """
        Метод сохранения.
        """
        pass

    def saveAs(self, ResFileName_):
        """
        Сохранить как...
        @param ResFileName_: Имя ресурсного файла.
        """
        pass

    def load(self, ResFileName_):
        """
        Загрузить ресурс из файла.
        @param ResFileName_: Имя ресурсного файла.
        """
        pass

    def setResFileName(self, ResFileName_=None):
        """
        Установить имя ресурсного файла.
        """
        pass

    def lockRes(self):
        """
        Заблокировать ресурс.
        """
        pass

    def unlockRes(self):
        """
        Разблокировать ресурс.
        """
        pass

    def isLockRes(self):
        """
        Заблокирован ли ресурс.
        """
        pass

    def getRes(self):
        """
        Ресурс.
        """
        return None
