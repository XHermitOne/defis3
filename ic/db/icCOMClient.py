#!/usr/bin/env python
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


__version__ = (0, 0, 1, 2)


# --- Класы ---
class icCOMClientPrototype:
    """
    COM клиент.
    """
    def __init__(self, Resource_=None):
        """
        Конструктор.
        @param Resource_: Ресурс описания компонента.
        """
        self._com_server_name = Resource_['server']

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
