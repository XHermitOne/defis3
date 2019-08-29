#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
"""
Хранилище справочников.
"""

# --- Подключение библиотек ---
import time

from . import icspravstorage
from . import icodb_spravobject

# Версия
__version__ = (0, 1, 1, 2)


class icSpravODBStorage(icodb_spravobject.icODBNsiInterface, icspravstorage.icSpravStorageInterface):
    """
    Класс SQL хранилища справочника.
    """
    def __init__(self, sprav, db_name, table_name):
        """
        Конструктор.
        @param sprav: Объект справочника, к которому прикреплено
            хранилище справочников.
        @param db_name: Имя источника.
        @param table_name: Имя таблицы данных справочника.
        """
        icodb_spravobject.icODBNsiInterface.__init__(self, None, sprav, db_name, table_name)
        icspravstorage.icSpravStorageInterface.__init__(self, sprav, db_name, table_name)
        
        # Признак использования лога для хранения изменений
        self._bLog = True
        
    def getSpravParent(self):
        """
        Объект справочника, к которому прикреплено хранилище справочников.
        """
        return self._sprav_parent
        
    def getLevelTable(self, level_cod=None, dt=None):
        """
        Таблица данных уровня.
        @param level_cod: Код, запрашиваемого уровня.
            Если None, то возвращаются данные самого верхнего уровня.
        @type dt: C{string}
        @param dt: Время актуальности данных.
        @return: Список кортежей, соответствующий данным запрашиваемого уровня.
            Или None в случае ошибки.
        """
        lst = []
        if not self.metaSprav:
            return lst
            
        if not level_cod:
            level_cod = ''
            level = self.getSpravParent().getLevelByCod(level_cod)
        else:
            level = self.getSpravParent().getLevelByCod(level_cod).getNext()
            
        if level:
            level_len = len(level_cod) + level.getCodLen()
        else:
            return []

        if not dt:
            for r in self.metaSprav.value.data:
                cod = r[0]
                if len(cod) == level_len and cod.startswith(level_cod):
                    lst.append(r)
        else:
            # Отбираем нужные коды
            for cod, rr in self.metaSpravLog.value.log.items():
                if len(cod) == level_len and cod.startswith(level_cod):
                
                    # Отбираем строки с нужным временем актуальности
                    for r in rr:
                        t1, t2 = r[-2:]
                        if not t2:
                            t2 = '9999.12.31 23:59:59'
                        if t1 < dt < t2:
                            lst.append(r)
                            break
        return lst
        
    def isLogMode(self):
        """
        Возвращает признак использования лога.
        """
        return self._bLog
        
    def setLevelTable(self, level_cod, table):
        """
        Сохранить таблицу данных уровня.
        @param level_cod: Код, запрашиваемого уровня.
            Если None, то данные самого верхнего уровня.
        @param table: Таблица данных уровня - список кортежей,
            соответствующий данным запрашиваемого уровня.
        @return: Возвращает результат выполнения операции True/False.
        """
        if not self.metaSprav:
            return False
        
        if not level_cod:
            level_cod = ''
            
        level = self.getSpravParent().getLevelByCod(level_cod).getNext()
        if level:
            level_len = len(level_cod) + level.getCodLen()
        else:
            return False
        
        lst = []
        # Словарь измененных значений
        updDct = {}
        # Словарь кодов
        codUpdDct = {}
        for r in table:
            codUpdDct[r[0]] = r
            
        codLst = list(range(len(self.metaSprav.value.data)))
        # Удаляем старые записи
        for i, r in enumerate(self.metaSprav.value.data):
            codLst[i] = r[0]
            
            if not r[0].startswith(level_cod) or (len(r[0]) != level_len):
                lst.append(r)
            # Словарь измененных значений
            elif r[0] in codUpdDct and codUpdDct[r[0]] != r:
                updDct[r[0]] = codUpdDct[r[0]]#r
            
        # Добавляем измененные
        for r in table:
            lst.append(r)
            
            if not r[0] in codLst:
                updDct[r[0]] = r
            
        self.metaSprav.value.data = lst
        self.metaSprav.setValueChanged(True)
        self.metaSprav.Save()

        # Отражаем в логе изменения
        if self.isLogMode():
            logDct = self.metaSpravLog.value.log
            tm = '%d.%02d.%02d %02d:%02d:%02d' % time.localtime()[:6]
            
            for key, r in updDct.items():
                if key in logDct:
                    logDct[key][-1][-1] = tm
                    logDct[key].append(r+[tm, ''])
                else:
                    logDct[key] = [r+[tm,'']]

            self.metaSpravLog.value.log = logDct
            self.metaSpravLog.setValueChanged(True)
            self.metaSpravLog.Save()

    def SetLogMode(self, bLog=True):
        """
        Устанавливает режим работы с логом.
        """
        self._bLog = bLog
