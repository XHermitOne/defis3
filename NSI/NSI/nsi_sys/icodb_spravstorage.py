#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
Хранилище справочников.
"""

# Версия
__version__ = (0, 0, 0, 1)

#--- Подключение библиотек ---

from ic.components import icwidget

from ic.utils import ic_time
from ic.log import ic_log
#from ic.db import ic_sqlobjtab
#import NSI.nsi_sys.icspravstorage as icspravstorage
#import NSI.nsi_sys.icodb_spravobject.IODBNsi as IODBNsi
from . import icspravstorage
from .icodb_spravobject import IODBNsi
import time

#--- Спецификация ---
#--- Функции ---
#--- Классы ---
class icSpravODBStorage(IODBNsi, icspravstorage.icSpravStorageInterface):
    """
    Класс SQL хранилища справочника.
    """
    def __init__(self,spravObj, DBName_,TabName_):
        """
        Конструктор.
        @param spravObj: Объект справочника, к которому прикреплено
            хранилище справочников.
        @param DBName_: Имя источника.
        @param TabName_: Имя таблицы данных справочника.
        """
        IODBNsi.__init__(self, None, spravObj, DBName_,TabName_)
        icspravstorage.icSpravStorageInterface.__init__(self,spravObj,DBName_,TabName_)
        
        # Признак использования лога для хранения изменений
        self._bLog = True
        
    def getSpravParent(self):
        """
        Объект справочника, к которому прикреплено хранилище справочников.
        """
        return self._sprav_parent
        
    def getLevelTable(self,LevelCod_=None, DateTime_=None):
        """
        Таблица данных уровня.
        @param LevelCod_: Код, запрашиваемого уровня.
            Если None, то возвращаются данные самого верхнего уровня.
        @type DateTime_: C{string}
        @param DateTime_: Время актуальности данных.
        @return: Список кортежей, соответствующий данным запрашиваемого уровня.
            Или None в случае ошибки.
        """
        lst = []
        if not self.metaSprav:
            return lst
            
        if not LevelCod_:
            LevelCod_ = ''
            level=self.getSpravParent().getLevelByCod(LevelCod_)
        else:
            level=self.getSpravParent().getLevelByCod(LevelCod_).getNext()
            
        if level:
            level_len=len(LevelCod_) + level.getCodLen()
        else:
            print('')
            return []

        if not DateTime_:
            for r in self.metaSprav.value.data:
                cod = r[0]
                if len(cod) == level_len and cod.startswith(LevelCod_):
                    lst.append(r)
        else:
            # Отбираем нужные коды
            for cod, rr in self.metaSpravLog.value.log.items():
                if len(cod) == level_len and cod.startswith(LevelCod_):
                
                    # Отбираем строки с нужным временем актуальности
                    for r in rr:
                        t1, t2 = r[-2:]
                        if not t2:
                            t2 = '9999.12.31 23:59:59'
                        if t1 < DateTime_ and t2 > DateTime_:
                            lst.append(r)
                            break
        return lst
        
    def isLogMode(self):
        """
        Возвращает признак использования лога.
        """
        return self._bLog
        
    def setLevelTable(self,LevelCod_,Table_):
        """
        Сохранить таблицу данных уровня.
        @param LevelCod_: Код, запрашиваемого уровня.
            Если None, то данные самого верхнего уровня.
        @param Table_: Таблица данных уровня - список кортежей,
            соответствующий данным запрашиваемого уровня.
        @return: Возвращает результат выполнения операции True/False.
        """
        if not self.metaSprav:
            return False
        
        if not LevelCod_:
            LevelCod_ = ''
            
        level=self.getSpravParent().getLevelByCod(LevelCod_).getNext()
        if level:
            level_len=len(LevelCod_) + level.getCodLen()
        else:
            #ic_log.icLogErr('Не опрделен уровень кода <%s> справочник' % (LevelCod_,self.getSpravParent().getName()))
            return False
        
        lst = []
        # Словарь измененных значений
        updDct = {}
        # Словарь кодов
        codUpdDct = {}
        for r in Table_:
            codUpdDct[r[0]] = r
            
        codLst = range(len(self.metaSprav.value.data))
        # Удаляем старые записи
        for i, r in enumerate(self.metaSprav.value.data):
            codLst[i] = r[0]
            
            if not r[0].startswith(LevelCod_) or (len(r[0]) <> level_len):
                lst.append(r)
            # Словарь измененных значений
            elif r[0] in codUpdDct and codUpdDct[r[0]] <> r:
                updDct[r[0]] = codUpdDct[r[0]]#r
            
        # Добавляем измененные
        for r in Table_:
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
        #ic_log.icToLog('Лог: %s' % self.metaSpravLog.value.log)
        
    def SetLogMode(self, bLog=True):
        """
        Устанавливает режим работы с логом.
        """
        self._bLog = bLog