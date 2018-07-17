#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль содержит интерфейс для работы с табличными данными.
"""

import os.path
import wx
import pickle as pic

from ic.utils import *
from ic.utils.util import icSpcDefStruct
from .icdataset import *
from IC_FILE import *

SPC_IC_FILESET = {'name': 'default', 'type': 'FileSet', 'child': []}

icNormalFieldType = 0
icTextFieldType = 1
icNumberFieldType = 2
icDoubleFieldType = 3
icDataTimeFieldType = 4
icVirtualFieldType = 101


class icFileSet(icDataSet):
    """
    Интерфейс для работы с табличными данными.
    """
    
    def __init__(self, id, component={}, logType=0, evalSpace={}):
        """
        Конструктор для создания таблицы.
        
        @type id: C{int}
        @param id: Идентификатор объекта.
        @type data: C{List}
        @param data: Данные в виде списка картежей, т.к. большинство драйверов возвращает данные в таком виде.
        @type description: C{Dictionary}
        @param description: Описание колонок. В качестве ключа выступает имя поля, в качестве значения
            список состоящий из номера соответствующей колонке данных и объекта описания (тип, предствление, и. т. д.).
            B{Пример:}C{\{'field1':(0,{'type':(4,0,0,0), 'expr':'a+b'})\}}
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        """
        self.component = component
        self.evalSpace = evalSpace

    def getNameValue(self, fieldName, rec=None):
        """
        Функция по имени колонки и номеру записи возвращает значение.
        
        @type rec: C{int}
        @param rec: Номер ряда.
        @type fieldName: C{String}
        @param fieldName: Имя поля.
        """
        ret = None
        buffer = self.zzfile.read()
        buffer = pic.loads(buffer)
        if isinstance(buffer, dict):
            if fieldName in buffer:
                ret = buffer[fieldName]
        
        return ret
    
    def setNameValue(self, fieldName, value, rec=None, bUpdate=False):
        """
        Устанавливает значение поля. Если имя поля не найдено в источнике данных,
        то функция пытается выполнить функцию на запись по описанию колонки из ресурсного
        описания по аттрибуту 'setvalue'.

        @param row: Номер записи
        @type row: C{int}
        @param fieldName: Имя поля
        @type fieldName: C{string}
        @param value: Значение
        @return: Возвращает признак успешного выполнения
        @rtype: C{bool}
        """
        buffer = self.zzfile.read()
        if isinstance(buffer, dict):
            if fieldName in buffer:
                buffer[fieldName] = value
            else:
                buffer[fieldName] = value   # еще не знаЮ зачем
        
        buffer = pic.dumps(buffer)
        self.zzfile.put(buffer)
        
    def addRecord(self, fieldName='', value='', bUpdate=False):
        """
        Функция добавляет новую запись

        @param row: Номер записи в буфере
        @type row: C{int}
        @param fieldName: Имя колонки
        @type fieldName: C{int}
        @param value: Новое значение
        @return: Возвращает признак успешного выполнения.
        @rtype: C{bool}
        """
        buffer = {}
        buffer[fieldName] = value
        buffer = pic.dumps(buffer)
        self.zzfile.append(buffer)

    def delRecord(self, rec):
        """
        Удаляет запись из источника данных. Функция по номеру строки определяет уникальный
        идентификатор для удаления нужной записи.

        @param rec: Номер записи
        @type rec:  C{int}
        @return rec: Признак успешного выполнения
        @rtype: C{bool}
        """
        self.zzfile.delete()
    
    def Open(self,  name):
        # если нет такого файла -создать
        if not os.path.isfile(name):
            self.zzfile.create(name)
        self.zzfile = db_file()
        self.zzfile.open(name)
            
    def Close(self):
        self.zzfile.close()

    def IsEOF(self):
        self.zzfile.eof()
    
    def IsBOF(self):
        self.zzfile.bof()
    
    def Skip(self, offset=1):
        """
        """
        self.zzfile.skip(offset)
    
    def Recno(self):
        return self.Skip(0)


if __name__ == '__main__':
    dbfl = icFileSet(12)
    dbfl.Open('D:\\Python22\\_SAM\\Base\\ic\\db\\test.dat')
    for i in xrange(100):
        strtest = 'ПРОБАФФФФФФФФФФФФФФФФФф'
        strtest = pic.dumps(strtest)
        dbfl.addRecord('pole1', strtest)
    dbfl.Close()
    
    dbfl.Open('D:\\Python22\\_SAM\\Base\\ic\\db\\test.dat')
    while not dbfl.IsEOF():
          strtest = dbfl.getNameValue('pole1')
          strtest = pic.loads(strtest)
          print(strtest)
          dbfl.skip(1)
