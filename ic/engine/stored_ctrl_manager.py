#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль класса - менеджера управления хранением свойств контрола.
"""

# Подключение библиотек
import os
import os.path

from ic.log import log
from ic.utils import resfunc
from ic.utils import ic_file
from ic.utils import ic_res


__version__ = (0, 1, 2, 1)


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

    def save_data_file(self, save_filename, save_data=None):
        """
        Сохранить данные в конкретном файле.
        @param save_filename: Полное имя файла сохранения.
        @param save_data: Сохраняемые данные.
        @return: True/False.
        """
        if save_filename:
            # Просто записать в файл
            ic_res.SaveResourcePickle(save_filename, save_data)
        else:
            log.warning(u'Не определен файл для сохранения фильтра')
            return False
        return True

    def load_data_file(self, save_filename):
        """
        Прочитать данные из файла.
        @param save_filename: Полное имя файла сохранения.
        @return: Данные файла или None в случае ошибки.
        """
        if save_filename:
            # Просто записать в файл
            return ic_res.LoadResourcePickle(save_filename)
        else:
            log.warning(u'Не определен файл для сохранения фильтра')
        return None
