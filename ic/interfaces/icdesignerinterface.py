#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Интерфейс визуального дизайнера компонентов.
"""

__version__ = (0, 1, 1, 2)


class icDesignerInterface(object):
    """
    Интерфейс визуального дизайнера компонентов.
    """
    def __init__(self, *arg, **kwarg):
        """
        Конструтор.
        """
        pass

    @staticmethod
    def getToolPanelCls():
        """
        Возвращает класс панели инструментов.
        """
        from ic.PropertyEditor import icstylepanel
        return icstylepanel.icStyleToolPanel
    
    def getToolPanel(self, parent, *arg, **kwarg):
        """
        Возвращает панель инструментов.
        """
        cls = self.getToolPanelCls()
        if cls:
            return cls(parent)


class icExtFormDesignerInterface(object):
    """
    Интерфейс внешнего визуального дизайнера форм/панелей.
    """

    def open_project(self, prj_filename):
        """
        Открыть файл проекта.

        :param prj_filename: Полное имя файла проекта.
        :return: True/False
        """
        return False

    def create_project(self, default_prj_filename=None):
        """
        Создание нового файла проекта.

        :param default_prj_filename: Имя файла проекта по умолчанию.
        :return: True/False.
        """
        return False

    def generate(self, prj_filename, *args, **kwargs):
        """
        Дополнительная генерация проекта.

        :param prj_filename: Полное имя файла проекта.
        :return: True/False.
        """
        return False
