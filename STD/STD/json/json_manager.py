#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер управления/преобразования JSON структур.
"""

import json
import os
import os.path

from ic.log import log

__version__ = (0, 1, 1, 1)


class icJSONManager(object):
    """
    Класс менеджера управления/преобразования JSON структур.
    """
    def dict2json(self, data_dict):
        """
        Преобразование словаря Python в JSON.
        @param data_dict: Словарь.
        @return: JSON структура.
        """
        return json.dumps(data_dict)

    def json2dict(self, data_json):
        """
        Преобразование JSON  в словарь Pytho.
        @param data_json: JSON структура.
        @return: Словарь Python.
        """
        return json.loads(data_json)

    def save_dict_as_json(self, json_filename, data_dict, bReWrite=True):
        """
        Сохранить JSON в файле.
        @param json_filename: Полное имя сохраняемого файла JSON.
        @param data_dict: Словарь Python.
        @param bReWrite: Переписать файл, если уже существует?
        @return: True - сохранение прошло успешно. False - ошибка.
        """
        if bReWrite and os.path.exists(json_filename):
            try:
                os.remove(json_filename)
            except:
                log.fatal(u'Ошибка удаления JSON файла <%s>' % json_filename)
                return False

        write_file = None
        try:
            write_file = open(json_filename, 'w')
            json.dump(data_dict, write_file)
            write_file.close()
            return True
        except:
            if write_file:
                write_file.close()
            log.fatal(u'Ошибка сохранения JSON файла <%s>' % json_filename)
        return False
