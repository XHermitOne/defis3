#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль содержит интерфейс для работы с простейшей таблицей. Таблица хранится в текстовом файле в виде питоновского словаря.
Ключ 'description' содержит описание полей таблицы (см. icDataSet) . Ключ 'data' содержит данные в виде списка записей. Запись в
свою очередь представляется в виде списка значений полей. Привязка к имени поля осуществляется через описание.

@type SPC_IC_SIMPLE_DATASET: C{Dictionary}
@var SPC_IC_SIMPLE_DATASET: Спецификация на ресурсное описание компонента.

    Описание ключей:
    - B{name = 'DefaultName'}: Имя объекта.
    - B{type='SimpleDataset'}: Тип объекта.
    - B{description=[]}: Описание колонок такое же как и у GridCell.
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
from ic.log.iclog import MsgLastError, LogLastError
from ic.engine import icUser as icuser
import ic.utils.coderror as coderror
import os
import wx.grid as grid
import copy
import ic.interfaces.icdatasetinterface as icdatasetinterface
import ic.utils.translate as translate
from ic.utils import ic_str
from ic.utils import ic_util
from ic.db import icsqlalchemy
import copy
from ic.kernel import io_prnt

SPC_IC_SIMPLE_DATASET = {'type': 'SimpleDataset',
                         'name': 'DefaultName',

                         'description': [],
                         'init': {},
                         'wxGridTypes': [],
                         'data_buff': []
                         }

#   Версия компонента
__version__ = (1, 0, 0, 8)


class CChangeBuff(object):
    """
    Буфер изменений датасета.
    """

    def __init__(self, key_col_lst=None):
        """
        Конструктор.
        """
        self.key_col_lst = key_col_lst or []
        self.add_rows_dct = {}
        self.del_rows_dct = {}
        self.update_rows_dct = {}

    def get_key(self, row):
        return tuple([row[col] for col in self.key_col_lst or xrange(len(row))])

    def reg_add(self, row):
        key = self.get_key(row)
        self.add_rows_dct[key] = copy.deepcopy(row)
        self.del_rows_dct.pop(key, None)

    def reg_del(self, row):
        key = self.get_key(row)
        self.del_rows_dct[key] = copy.deepcopy(row)
        self.add_rows_dct.pop(key, None)
        self.update_rows_dct.pop(key, None)

    def reg_update(self, row):
        key = self.get_key(row)
        self.update_rows_dct[key] = copy.deepcopy(row)

    def clear(self):
        """
        Чистит буфер.
        """
        self.add_rows_dct = {}
        self.del_rows_dct = {}
        self.update_rows_dct = {}


class icSimpleDataset(icdatasetinterface.icDatasetInterface):
    """
    Интерфейс для работы с табличными данными.
    """

    def __init__(self, id, component, logType=0, evalSpace={}, indxLst=None):
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
        @param indxLst: Список колонок задающих индекс строки.
        """
        component = icSpcDefStruct(SPC_IC_SIMPLE_DATASET, component)

        self.name = component['name']
        self.type = component['type']
        self.description = component['description']
        self.data = copy.deepcopy(component['data_buff'])
        self.logType = logType
        self.init = component['init']
        self.wxgridtypes = copy.deepcopy(component['wxGridTypes'])

        #   Буфер изменений строки
        self.changeRowBuff = None
        # Буфер всех изменений
        self.allChangeBuff = None

        #   Текстовое представление буфера
        self.text = ''
        self.source = None

        #   Атрибуты навигации
        self.cursor = -1
        self.bBof = False
        self.bEof = False

        self.listFld = range(len(self.description))

        for indx, fld in enumerate(self.description):
            self.listFld[indx] = fld['name']

        if not self.init:
            self.init = self.getDefaultInitLst()

        icdatasetinterface.icDatasetInterface.__init__(self)

    def getDataList(self):
        """
        Нобор записей.Каждая запись в виде списка.
        """
        return self.data

    def getDataDict(self):
        """
        Нобор записей.Каждая запись в виде словаря.
        """
        fields = self.getFieldList()
        return [dict([(fld, rec[i]) for i, fld in enumerate(fields)]) for rec in self.data]

    def __cmpField(self, x, y):
        """
        Функция сравнения.
        """
        col = self._getSortCol()
        if self._isSortDESC:
            d = 1
        else:
            d = -1

        sx = (x[col] or '').lower()
        sy = (y[col] or '').lower()

        return ic_str.cmpLowerU(sx, sy)*d

    def _getSortCol(self):
        """
        Возвращает номер колонки, по которой необходимо сортировать.
        """
        return self.__sort_col_num

    def _setSortCol(self, col):
        """
        Устанавливает номер колонки, по которой необходимо сортировать.
        """
        self.__sort_col_num = col

    def ConvertTxtToSruct(self):
        """
        Подготавливаем данные.
        """
        self.txt = self.txt.replace('\r\n', '\n')

        if self.txt != '':
            dict_file = eval(self.txt)

            try:
                if 'data' in dict_file:
                    self.data = dict_file['data']

                if self.rc_description is None or self.rc_description == {}:
                    self.description = dict_file['description']
                else:
                    self.description = self.rc_description
            except:
                self.description = self.rc_description
                self.data = dict_file
        else:
            if type(self.rc_description) in (str, unicode):
                self.description = eval(self.rc_description)
            else:
                self.description = self.rc_description

            self.data = []

    def getDefaultInitLst(self, gridtypes=None):
        """
        Определяет значение по умолчанию в зависимости от типа колонки.
        @type gridtypes: C{list}
        @param gridlist: Список типов колонок.
        """
        self.init = {}

        if not gridtypes:
            gridtypes = self.wxgridtypes

        if gridtypes:
            for indx, tp in enumerate(gridtypes):
                fld = self.getFieldList()[indx]

                if tp in [grid.GRID_VALUE_STRING, grid.GRID_VALUE_DATETIME]:
                    val = ''
                else:
                    val = 0

                self.init[fld] = val

    # ----- Интерфйс dataseta -----------------------------

    def setNameValue(self, fieldName, value, rec=None, bReal=False, bCtrl=True):
        """
        Устанавливает значение поля. Если имя поля не найдено в источнике данных,
        то функция пытается выполнить функцию на запись по описанию колонки из ресурсного
        описания по аттрибуту 'setvalue'.
        @param rec: Номер записи
        @type rec: C{int}
        @param fieldName: Имя поля
        @type fieldName: C{string}
        @param value: Значение
        @type bReal: C{bool}
        @param bReal: Параметр совместимости с icSQLObjDataSet.
        @type bCtrl: C{bool}
        @param bCtrl: Параметр совместимости с icSQLObjDataSet.
        @return: Возвращает в случае успеха код контроля (0,1,2), в противном случае None.
        """
        #   Проверка на права доступа к данному методу
        if not icuser.canAuthent('wr', self.name, icuser.ACC_DATA):
            return None

        #   Если номер строки не указан, то номер записи определяем по положению курсора
        if rec is None:
            rec = self.cursor

        #   Если задан фильтр, то значение берется из фильтра
        if isinstance(self.filter, dict) and fieldName in self.filter.keys():
            value = translate.InitValidValue(self.filter, fieldName, value)

        if self.changeRowBuff is None:
            self.changeRowBuff = {rec: {}}

        if rec in self.changeRowBuff:
            self.changeRowBuff[rec][fieldName] = value
        else:
            self.changeRowBuff[rec] = {fieldName: value}

        return coderror.IC_CTRL_OK

    def getNameValue(self, fieldName, rec=None, bReal=False, bFromBuff=True):
        """
        Функция по имени колонки и номеру записи возвращает значение
        из буфера.
        @type rec: C{int}
        @param rec: Номер строки.
        @type fieldName: C{string}
        @param fieldName: Имя поля.
        @type bReal: C{bool}
        @param bReal: Параметр совместимости с icSQLObjDataSet.
        @type bFromBuff: C{bool}
        @param bFromBuff: Параметр совместимости с icSQLObjDataSet.
        @rtype: C{...}
        @return: По имени колонки и номеру записи возвращает значение из буфера. Если поле или номер записи
            указаны не верно, то функция возвращает C{None}.
        """
        value = ''
        #   Проверка на права доступа к данному методу
        if not icuser.canAuthent('r', self.name, icuser.ACC_DATA, False):
            return ''
        #   Если номер строки не указан, то номер записи определяем по положению курсора
        if rec is None:
            rec = self.cursor
        #   Проверяем буфер изменений. Если там есть значение, то берем
        #   его из буфера.
        if bFromBuff and (self.changeRowBuff is not None and rec in self.changeRowBuff
           and fieldName in self.changeRowBuff[rec]):
            value = self.changeRowBuff[rec][fieldName]

        elif 0 <= rec < self.getRecordCount():
            #   Определяем индекс поля
            try:
                indxFld = self.getFieldList().index(fieldName)
                value = self.data[rec][indxFld]
            except:
                LogLastError(u'getNameValue ERROR')

        return value

    def update(self, values=None, rec=None, bReal=False, bCtrl=True):
        """
        Устанавливает значения полей заданной строки. Если имя поля не найдено
        в источнике данных, то функция пытается выполнить функцию на запись по
        описанию колонки из ресурсного описания по аттрибуту 'setvalue'. Если
        словарь обновлений (values) не определен, то обновления берутся из
        буфера изменений строки.

        @type rec: C{int}
        @param rec: Номер записи.
        @type values: C{dictionary}
        @param values: Словарь значений. В качестве ключей используются имена полей.
        @type bReal: C{bool}
        @param bReal: Параметр совместимости с icSQLObjDataSet.
        @type bCtrl: C{bool}
        @param bCtrl: Параметр совместимости с icSQLObjDataSet.
        @return: Возвращает код контроля записи = IC_CTRL_OK.
        """
        #   Если номер строки не указан, то номер записи определяем по положению курсора
        if rec is None:
            rec = self.cursor

        #   Берем значения из буфера изменений. В этом случае контроль поля
        #   проводить уже не надо

        if values is None and self.changeRowBuff is not None and rec in self.changeRowBuff:
            values = self.changeRowBuff[rec]

        if isinstance(values, dict):
            try:
                for fld, val in values.items():
                    indxFld = self.getFieldList().index(fld)
                    self.data[rec][indxFld] = val

                self._is_changed = True
                if self.allChangeBuff:
                    self.allChangeBuff.reg_update(self.data[rec])
            except:
                LogLastError(u'update ERROR')

            #   Чистим буфер изменений данной строки
            self.clearChangeRowBuff(rec)

        return coderror.IC_CTRL_OK

    def addRecord(self, values=None, postAddExpr=None, uuid_postAddExpr=None):
        """
        Функция добавляет новую запись.

        @param fieldName: Имя колонки.
        @type fieldName: C{string}
        @type values: C{dictionary}
        @param values: Словарь известных значений. В качестве ключей имена полей,
            значения полей в качестве значений.
        @type postAddExpr: C{string}
        @param postAddExpr: Параметр совместимости с icSQLObjDataSet.
        @type uuid_postAddExpr: C{string}
        @return uuid_postAddExpr: Параметр совместимости с icSQLObjDataSet.
        @return: Возвращает признак успешного выполнения.
        @rtype: C{bool}
        """
        #   Проверка на права доступа к данному методу
        if not icuser.canAuthent('a', self.name,  icuser.ACC_DATA,  True):
            return False

        rec = self.getRecordCount()

        if values is None and self.changeRowBuff is not None and rec in self.changeRowBuff:
            values = self.changeRowBuff[rec]

        try:
            lst = self.getFieldList()
            row_lst = range(len(lst))

            for indx, fld in enumerate(lst):
                if values and fld in values:
                    row_lst[indx] = values[fld]
                elif self.init and fld in self.init:
                    row_lst[indx] = self.init[fld]
                else:
                    row_lst[indx] = None

            value = self.data.append(row_lst)
            self._is_changed = True
            if self.allChangeBuff:
                self.allChangeBuff.reg_add(row_lst)

            #   Переводим курсор на последнюю запись
            self.Move(-1)
            #   Чистим буфер введенной записи
            self.clearChangeRowBuff(rec)
        except:
            LogLastError(u'addRecord ERROR')

        return True

    def delRecord(self, rec=None):
        """
        Удаляет запись из источника данных.

        @param rec: Номер записи.
        @type rec:  C{int}
        @return: Код завершение операции.
        @rtype: C{int}
        """
        #   Проверка на права доступа к данному методу
        if not icuser.canAuthent('d', self.name,  icuser.ACC_DATA,  True):
            return coderror.IC_DEL_FAILED

        if rec is None:
            rec = self.cursor

        #   Удаляем элемент из буфера идентификаторов
        if 0 <= rec < self.getRecordCount():

            r = self.data.pop(rec)
            if self.allChangeBuff:
                self.allChangeBuff.reg_del(r)

            if self.cursor >= self.getRecordCount():
                self.Move(-1)

        self._is_changed = True
        self.clearChangeRowBuff()
        return coderror.IC_DEL_OK

    def Lock(self, rec=-1):
        """
        Блокирует нужную запись для записи.
        """
        return 99

    def Unlock(self, rec=-1):
        """
        Разблокирует нужную запись.
        """
        return 0

    # *******************************************************
    #   Функции навигации
    # *******************************************************

    def Move(self, rec=0):
        """
        Устанавливает курсор в определенную позицию.

        @type rec: C{int}
        @param rec: Номер записи. По умолчанию C{rec=0}.
        @rtype: C{bool}
        @return: Возвращает признак успешного выполнения. При попытке установить значение курсора
            меньше нуля или больше номера последней записи функция вернет C{False}, в другом случае C{True}.
        """
        if rec == -1:
            rec = self.getRecordCount() - 1

        if 0 <= rec < self.getRecordCount():
            self.cursor = rec
            self.bBof = False
            self.bEof = False
            #   Чистим буфер изменений
            self.clearChangeRowBuff()
            return True
        elif rec < 0:
            self.bBof = True
            self.bEof = False
        elif rec >= self.getRecordCount():
            self.cursor = self.getRecordCount()
            self.bEof = True
            self.bBof = False

        return False

    def IsEOF(self):
        """
        Признак выхода за конец таблицы. Соответствующий флаг устанавливается при попытке
        сместится за последнюю запись.

        @rtype: C{bool}
        @return: Признак за конец таблицы.
        """
        return self.bEof

    def IsBOF(self):
        """
        Соответствующий флаг устанавливается при попытке
        получить запись c номером < 0.

        @rtype: C{bool}
        @return: Признак попытки C{Skip(-1)} на самой первой записи таблицы.
        """
        return self.bBof

    def Skip(self, offset=1):
        """
        Смещение на определенное количество записей относительно текущей.

        @type offset: C{int}
        @param offset: Смещение относительно текущей записи. По умолчанию C{offset=1}.
        @rtype: C{bool}
        @return: Признак успешного выполнения. При попытке установить значение курсора
            меньше нуля, положение курсора не изменится и функция вернет C{False}, а
            соответствующий флаг для функции C{IsBOF()} установится в положение C{True}. Если функция
            попытается установить положение курсора больше номера последней записи, то соответствующий
            флаг для функции C{IsEOF()} установится в C{True} и функция вернет C{False}.
        """

        if 0 <= self.cursor + offset < self.getRecordCount():
            self.cursor += offset
            self.bBof = False
            self.bEof = False

            #   Чистим буфер изменений
            self.clearChangeRowBuff()

            return True

        elif self.cursor + offset < 0:
            self.bBof = True
            self.bEof = False

        elif self.cursor + offset >= self.getRecordCount():
            self.cursor = self.getRecordCount()
            self.bEof = True
            self.bBof = False

        return False

    def Recno(self):
        """
        Возвращает положение курсора.

        @rtype: C{int}
        @return: Возвращает положение курсора.
        """

        return self.cursor

    def Refresh(self):
        """
        Обновление буфера данных.
        """
        pass

    def getRecordCount(self):
        """
        Возвращает количество записей в источнике данных.

        @rtype: C{int}
        @return: Количество записей в источнике данных.
        """
        return len(self.data)

    def getFieldCount(self):
        """
        Возвращает количество полей. Вычисляется по словарю описания полей.

        @rtype: C{int}
        @return: Количество полей.
        """
        return len(self.description)

    def isChangeRowBuff(self, rec=None):
        """
        Функция проверяет есль ли в буфере изменений какие-либо изменения.

        @type rec: C{int}
        @param rec: Номер записи, где проверяются изменения. Если rec = None,
            то проверяется текущая запись.
        @rtype: C{bool}
        @return: Если True, то буфер содержит изменения по заданной записи.
        """
        if self.changeRowBuff is None or self.changeRowBuff == {}:
            return False

        if rec is None:
            rec = self.cursor

        if (rec not in self.changeRowBuff) or self.changeRowBuff[rec] == {}:
            return False

        return True

    def clearChangeRowBuff(self, rec=None):
        """
        Функция чистит буфер изменений строки.

        @type rec: C{int}
        @param rec: Номер записи, буфер которой небходимо почистить. Если rec = None,
            то чистится буфер текущей записи, если rec < 0 то чистится буфер всех
            записей.
        """
        if self.changeRowBuff is None or self.changeRowBuff == {}:
            return

        if rec is None:
            rec = self.cursor

        self.changeRowBuff = {}

    def getFieldList(self):
        """
        Функция возвращает список полей.

        @rtype: C{list}
        @return: Возвращает список полей.
        """
        return self.listFld

    def getObj(self, rec=None):
        """
        Возвращает обект записи.
        """
        if rec is None:
            rec = self.cursor
        try:
            return self.data[rec]
        except IndexError:
            io_prnt.outErr(u'icSimpleDataset getObj IndexError, rec=%s data=%s' % (rec, self.data))
        return None

    def SortField(self, fld, direction=None):
        """
        Сортирует данные по заданному полю.

        @type fld: C{dictionary}
        @param fld: Словарное описание поля из схемы данных.
        @type direction: C{int}
        @param direction: Направление сортировки. 1 - по возрастанию, -1 по убыванию.
            Если не указано, то сортровка направления чередуются.
        @rtype: C{bool}
        @return: Признак успешной сортировки.
        """
        if fld in self.getFieldList():
            self._sortExprList = [fld]

            indx = self.getFieldList().index(fld)
            self._setSortCol(indx)

            if not direction:
                if self._isSortDESC:
                    self._isSortDESC = False
                else:
                    self._isSortDESC = True
            else:
                if direction == -1:
                    self._isSortDESC = True
                else:
                    self._isSortDESC = False

            self.data.sort(self.__cmpField)
            self.setSortPrzn()
            return True

        return False

    # -----------------------------------------------------
    #   Доступ к текущей строке
    rec = property(getObj)

    def Load(self):
        f = None
        try:
            f = open(self.source)
            self.txt = f.read()
            f.close()
        except:
            if f:
                f.close()
            LogLastError(u'Exception in Open ...')

    def Save(self):
        f = None
        try:
            f = open(self.source, 'wb')
            f.write(str({'description': self.description, 'data': self.data}))
            f.close()
        except:
            if f:
                f.close()
            LogLastError(u'Exception in Update ...', self.logType)
            raise Exception

    def SetDataBuff(self, buff):
        """
        Устанавливает буфер таблицы.
        """
        # ВНИМАНИЕ! Перекодировка необходима для грида!
        buff = ic_util.icStructStrRecode(buff, icsqlalchemy.DEFAULT_DB_ENCODING, 'unicode')
        self.data = buff
        self.clearChangeRowBuff()
        self.Move()

    def FindRowString(self, string, cursor=-1, fields=None, bILike=True):
        """
        Функция ищет подстроку в массиве данных.
        Это желательная функция для всех объектов данных, используется
        в для поиска в объекте навигации.

        @type string: C{string}
        @param string: Строка поиска
        @type cursor: C{int}
        @param cursor: Начальное положение курсора.
        @type fields: C{list}
        @param fields: Список полей по которым ведется поиск.
        @type bILike: C{bool}
        @param bILike: Признак поиска без учета регистра. Если False - то поиск ведется
            на точное соответствие.
        @rtype: C{tuple}
        @return: Возвращает номер строку и название поля, где найдена искомая строка.
        """
        try:
            # Без учета регистра?
            if bILike:
                string = string.upper()
            # Начальное положение курсора
            if cursor < 0:
                cursor = 0
            # Имена полей
            if fields is None:
                fields = self.getFieldList()

            # Перебор строк
            for i_row in range(cursor, len(self.data)):
                # Перебор полей
                for field in fields:
                    # Получить значение поля
                    if bILike:
                        value = self.getNameValue(field, i_row).upper()
                    else:
                        value = self.getNameValue(field, i_row)
                    # Проверка на совпадение подстроки
                    if string in value:
                        return i_row, field

            return -1, None
        except:
            LogLastError()
            # Подстрока не найдена
            return -1, None

    def isFieldIndexed(self, *arg, **kwarg):
        pass

if __name__ == '__main__':
    pass
