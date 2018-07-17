#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль содержит интерфейс для работы с табличной частью документов. Таблица
хранится в текстовом файле в виде питоновского словаря.
Ключ 'description' содержит описание полей таблицы (см. icDataSet) . Ключ 'data'
содержит данные в виде списка записей. Запись в свою очередь представляется в
виде списка значений полей. Привязка к имени поля осуществляется через описание.

@type SPC_IC_DOC_DATASET: C{Dictionary}
@var SPC_IC_DOC_DATASET: Спецификация на ресурсное описание компонента.

    Описание ключей:
    - B{name = 'DefaultName'}: Имя объекта.
    - B{type='SimpleDataset'}:Тип объекта.
    - B{description=[]}:Описание колонок такое же как и у GridCell.
    - B{init={}}: Словарь значений добавляемых по умолчанию при добавлении новой записи.
    - B{wxGridTypes=[]}: Список типов каждой колонки. В качестве идентификаторов типов
        используются идентификаторы типов колонок wx.grid.PyGridTableBase.
        wx.grid.GRID_VALUE_STRING,
        wx.grid.GRID_VALUE_BOOL,
        wx.grid.GRID_VALUE_NUMBER,
        wx.grid.GRID_VALUE_FLOAT,
        wx.grid.GRID_VALUE_CHOICE,
        wx.grid.GRID_VALUE_LONG,
        wx.grid.GRID_VALUE_DATETIME.
        
    - B{data_buff=[]}: Буфер данных, список списков.
"""

import ic.utils.util as util
from ic.utils.util import icSpcDefStruct
import ic.utils.coderror as coderror
import os
import wx.grid as grid
import copy
import ic.utils.translate as translate
from ic.db import icsimpledataset
from ic.kernel import io_prnt
from ic.utils import ic_str

SPC_IC_DOC_DATASET = {'name': 'DefaultName',
                      'type': 'SimpleDataset',
                      'description': [],
                      'init': {},
                      'wxGridTypes': [],
                      'data_buff': []}

#   Версия компонента
__version__ = (1, 0, 1, 2)


class icDocDataset(icsimpledataset.icSimpleDataset):
    """
    Интерфейс для работы с табличными данными.
    """
    
    def __init__(self, id, component, logType = 0, evalSpace = {}):
        """
        Конструктор для создания таблицы.
        @type id: C{int}
        @param id: Идентификатор объекта.
        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        """
        component = icSpcDefStruct(SPC_IC_DOC_DATASET, component)
        # Ссылка на спецификацию
        self._spc = None
        # Номер колонки, по которой ведется сортировка
        self.__sort_col_num = 0
        
        icsimpledataset.icSimpleDataset.__init__(self, id, component, logType, evalSpace)

    def addRecord(self, values=None, postAddExpr = None, uuid_postAddExpr=None):
        """
        Функция добавляет новую запись.
        """
        if self.GetSpc():
            rec = self.cursor
            if values is None and self.changeRowBuff is not None and rec in self.changeRowBuff:
                values = self.changeRowBuff[rec]

            ret, uuid = self.GetSpc().add(values)
            if ret == coderror.IC_NEW_OK and uuid:
                ret = icsimpledataset.icSimpleDataset.addRecord(self, values)
                self.data[-1].append(uuid)
                return ret
        else:
            io_prnt.outWarning(u'Спецификация документа не определена')
            return icsimpledataset.icSimpleDataset.addRecord(self, values)
            
        return False
    
    def delRecord(self, rec=None):
        """
        Удаляет запись из источника данных.

        @param rec: Номер записи.
        @type rec:  C{int}
        @return: Код завершение операции.
        @rtype: C{int}
        """
        if self.GetSpc():
            uuid = self.getRecUUID()
            if uuid and self.GetSpc().delete(uuid) == coderror.IC_DEL_OK:
                return icsimpledataset.icSimpleDataset.delRecord(self, rec)
        else:
            return icsimpledataset.icSimpleDataset.delRecord(self, rec)
        
    def getRecUUID(self, rec=None):
        """
        Возвращает uuid записи спецификации. UUID хранится в последней колонку строки.
        """
        if self.GetSpc():
            if rec is None:
                rec = self.cursor
            if rec is not None and rec >= 0:
                return self.data[rec][-1]
        
    def GetSpc(self):
        """
        Возвращает ссылку на табличную часть документа (спецификацию).
        """
        return self._spc
        
    def setRecUUID(self, uuid, rec=None):
        """
        Возвращает uuid записи спецификации. UUID хранится в последней колонку строки.
        """
        if not rec:
            rec = -1
            
        if self.GetSpc():
            if self.data:
                self.data[rec][-1] = uuid

        return False
        
    def SetSpc(self, spc, lst):
        """
        Устанавливает ссылку на табличную часть документа (спецификацию).
        
        param spc: Указатель на спецификацию.
        param lst: Список имен реквизитов.
        """
        self._spc = spc
        data = spc.getTabData(lst)
        self.SetDataBuff(data)
        
    def update(self, values=None, rec=None, bReal=False, bCtrl=True):
        """
        Сохраняем изменения в строке спецификации документа.
        """
        if self.GetSpc():
            if rec is None:
                rec = self.cursor
                
            uuid = self.getRecUUID(rec)

            if values is None and self.changeRowBuff is not None and rec in self.changeRowBuff:
                values = self.changeRowBuff[rec]
            
            if uuid and self.GetSpc().update(uuid, values) == coderror.IC_CTRL_OK:
                return icsimpledataset.icSimpleDataset.update(self, values, rec)
                
        else:
            return icsimpledataset.icSimpleDataset.update(self, values, rec)


if __name__ == '__main__':
    pass
