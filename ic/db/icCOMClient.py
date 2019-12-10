#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль функций работы с COM серверами - COM клиент.
"""

# --- Подключение модулей ---
try:
    import pythoncom
except ImportError:
    print('pythoncom ImportError')
    
from ic.log import ic_log

# --- Константы ---
# Тип
COMCLIENT_TYPE = 'COMClient'

# Спецификация БД
SPC_IC_COMCLIENT = {'type': COMCLIENT_TYPE,
                    'get_data': None,   # Функция получения данных
                    'set_data': None,   # Функция установки данных
                    'server': None,     # Имя COM сервера
                    }


__version__ = (0, 1, 1, 1)


# --- Класы ---
class icCOMClientProto:
    """
    COM клиент.
    """
    def __init__(self, resource_data=None):
        """
        Конструктор.

        :param resource_data: Ресурс описания компонента.
        """
        self._com_server_name = resource_data['server']

    def getCOMServer(self):
        """
        COM сервер.
        """
        pass
        
    def getData(self, *args, **kwargs):
        """
        Функция получения данных из COM сервера.
        """
        pass
        
    def setData(self, *args, **kwargs):
        """
        Функция сохранения данных в COM сервере.
        """
        pass
