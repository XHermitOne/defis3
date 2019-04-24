#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер управления/преобразования JSON структур.
"""

import json
import os
import os.path
import urllib.request

from ic.log import log

__version__ = (0, 1, 2, 1)


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
            json.dump(data_dict, write_file, indent=4)
            write_file.close()
            return True
        except:
            if write_file:
                write_file.close()
            log.fatal(u'Ошибка сохранения JSON файла <%s>' % json_filename)
        return False

    def get_json_as_dict_by_url(self, url):
        """
        Получить данные JSON  в виде словаря по URL.
        @param url: URL адрес.
        @return: Словарь JSON или None в случае ошибки.
        """
        if not url:
            log.warning(u'Не определен URL для получения данных JSON')
            return None

        try:
            response = urllib.request.urlopen(url)
            json_content = response.read()
            json_dict = json.loads(json_content)
            return json_dict
        except:
            log.fatal(u'Ошибка получения данных JSON с адреса <%s>' % url)
        return None

