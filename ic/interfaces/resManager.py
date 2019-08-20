#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Интерфейс для менеджеров ресурсных файлов.
"""

__version__ = (0, 1, 1, 1)


# === Описание классов ===
class icResourceManagerInterface(object):
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

    def saveAs(self, res_filename):
        """
        Сохранить как...
        @param res_filename: Имя ресурсного файла.
        """
        pass

    def load(self, res_filename):
        """
        Загрузить ресурс из файла.
        @param res_filename: Имя ресурсного файла.
        """
        pass

    def setResFileName(self, res_filename=None):
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
