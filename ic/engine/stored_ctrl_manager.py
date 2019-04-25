#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль класса - менеджера управления хранением свойств контрола.
"""

# Подключение библиотек
import os
import os.path

from ic.utils import resfunc
from ic.utils import ic_file


__version__ = (0, 1, 1, 1)


class icStoredCtrlManager(object):
    """
    Менеджер управления хранением свойств контрола.
    """
    def save_ext_data(self, name, **kwargs):
        """
        Запись дополнительных данных окна.
        @param name: Наименование файла для записи.
        @param kwargs: Словарь данных для записи.
        @return: True/False.
        """
        # Определить имя файла для хранения данных
        res_filename = os.path.join(ic_file.getPrjProfilePath(),
                                    name+'.ext')
        return resfunc.SaveResourcePickle(res_filename, kwargs)

    def load_ext_data(self, name):
        """
        Загрузка дополнительных данных окна.
        @param name: Наименование файла хранения данных.
        @return: Загруженные данные в виде словаря или
            пустой словарь если данных нет.
        """
        res_filename = os.path.join(ic_file.getPrjProfilePath(),
                                    name+'.ext')
        data = resfunc.LoadResourcePickle(res_filename)
        if data is None:
            data = dict()
        return data

