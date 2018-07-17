#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль функций установки связи с COM серверами.
"""

# --- Подключение модулей ---
try:
    import win32com.client
    import pythoncom
except ImportError:
    print('win32com.client ImportError')
    
from ic.log import ic_log
import ic.interfaces.icsourcinterface as icsourcinterface

# --- Константы ---
# Тип БД
COMSRV_TYPE = 'COMServer'

# Спецификация БД
SPC_IC_COMSRV = {'type': COMSRV_TYPE,
                 'app_link': None,              # Указание связи с объектом приложения
                 'connection_string': None,     # Указание связи с БД в случае с 1С.
                 }

# Поддерживаемы сервера
COM_EXCEL_APP_LNK = 'Excel.Application'
COM_1CV8_APP_LNK = 'V8.Application'

__version__ = (0, 0, 1, 2)


# --- Класы ---
class icCOMServerPrototype(icsourcinterface.icSourceInterface):
    """
    Источник данных COM сервер.
    """
    def __init__(self, Resource_=None):
        """
        Конструктор.
        @param Resource_: Ресурс описания компонента.
        """
        icsourcinterface.icSourceInterface.__init__(self, Resource_)

        self._comsrv_app_link = Resource_['app_link']
        self._connection_string = Resource_['connection_string']
        
        # Объект приложения COM сервера
        self.app = None
     
    def getAppLinkStr(self):
        """
        Строка связи с объектом приложения COM сервера.
        """
        return self._comsrv_app_link
        
    def getConnectionString(self):
        """
        Указание связи с БД в случае с 1С.
        """
        return self._connection_string
        
    def connect(self):
        """
        Установить связь с COM сервером.
        """
        app_link = self.getAppLinkStr()
        self.app = win32com.client.Dispatch(app_link)
        if self._connection_string:
            # Наверно это 1С сервер
            try:
                self.app.Connect(self._connection_string)
            except:
                pass

    def disconnect(self):
        """
        Разорвать связь.
        """
        if self.app:
            try:
                self.app.Quit()
            except:
                pass
            self.app = None
            
    def getApp(self):
        """
        Объект приложения COM сервера.
        """
        return self.app
