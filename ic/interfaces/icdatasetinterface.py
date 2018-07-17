#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Интерфейс dataset (Набора данных).
"""


class icDatasetInterface(object):
    """
    Интерфефес объектов данных для работы с объектами GridDatase/ListDataset.
    """

    def __init__(self, *arg, **kwarg):
        """
        Конструктор.
        """
        #   Признак, указывающий направление сортировки
        self._isSortDESC = False
        self._isSorted = False
        self.filter = None
        self._is_changed = False
        # Буфер всех изменений
        self.allChangeBuff = None

        self.dataclass = None

    def setFilter(self, cur_filter):
        assert None, 'Abstract method setFilter!'

    def getFilter(self):
        assert None, 'Abstract method getFilter!'

    def set_change_buff(self, buff):
        """
        Устанавливает буфер изменений.
        """
        self.allChangeBuff = buff
        self.allChangeBuff.clear()
        
    def isChanged(self):
        """
        Возвращает признак того, что данные таблицы были изменены.
        """
        return self._is_changed

    def isAdded(self):
        """
        Функция определяет появились ли в источнике данных новые записи.

        @rtype: C{bool}
        @return: Возвращает True - в случае если в буфере появились данные о добавленных записях, False в противном
            случае.
        """
        return False

    def isDeleted(self, cursor):
        """
        Функция определяет удалена ли соответствующая запись из источника данных или нет.

        @type cursor: C{long}
        @param cursor: Положение курсора.
        @rtype: C{bool}
        @return: Возвращает True - в случае если соответствующая запись удалена из источника данных, False в противном
            случае.
        """
        return False

    def set_change_prz(self, prz=True):
        if self.allChangeBuff and not prz:
            self.allChangeBuff.clear()
        self._is_changed = prz
        
    def getDataList(self):
        """
        Нобор записей. Каждая запись в виде списка.
        """
        assert None, 'Abstract method getDataList!'
        
    def getDataDict(self):
        """
        Нобор записей.Каждая запись в виде словаря.
        """
        assert None, 'Abstract method getDataDict!'
        
    def getNameValue(self, fieldName, rec=None, bReal=False, bFromBuff=True):
        """
        Функция по имени колонки и номеру записи возвращает значение из буфера.
        
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
        pass
        
    def isSorted(self):
        """
        """
        return self._isSorted
        
    def setSortPrzn(self):
        """
        """
        self._isSorted = True
        
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
        pass
        
    def update(self, values=None, rec=None, bReal=False, bCtrl=True):
        """
        Устанавливает значения полей заданной строки. Если имя поля не найдено
        в источнике данных, то функция пытается выполнить функцию на запись по 
        описанию колонки из ресурсного описания по аттрибуту 'setvalue'. Если 
        словарь обновлений (values) не определен, то обновления берутся из буфера
        изменений строки.
        
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
        pass
        
    def addRecord(self, values=None, postAddExpr=None, uuid_postAddExpr=None):
        """
        Функция добавляет новую запись.

        @type values: C{dictionary}
        @param values: Словарь известных значений. В качестве ключей имена полей,
            значения полей в качестве значений.
        @type postAddExpr: C{string}
        @param postAddExpr: Параметр совместимости с icSQLObjDataSet.
        @type uuid_postAddExpr: C{string}
        @param uuid_postAddExpr: Параметр совместимости с icSQLObjDataSet.
        @return: Возвращает признак успешного выполнения.
        @rtype: C{bool}
        """
        pass
        
    def delRecord(self, rec=None):
        """
        Удаляет запись из источника данных.

        @param rec: Номер записи.
        @type rec:  C{int}
        @return: Код завершение операции.
        @rtype: C{int}
        """
        pass

    def Lock(self, rec=-1):
        """
        Блокирует нужную запись для записи.

        @type rec: C{int}
        @param rec: Номер записи. По умолчанию B{rec=-1}. Если номер записи C{None}, то блокируется
            вся таблица. Если номер записи < 0, то блокируется текущая запись.
        @rtype: C{bool}
        @return: Возвращает код ошибки.
        """
        pass

    def Unlock(self, rec=-1):
        """
        Разблокирует нужную запись.

        @type rec: C{int}
        @param rec: Номер записи. По умолчанию B{rec=-1}.  Если номер записи C{None}, то разблокируется
            вся таблица. Если номер записи < 0, то разблокируется текущая запись.
        @rtype: C{bool}
        @return: Возвращает код ошибки.
        """
        pass

    # Функции навигации
    def Move(self, rec=0):
        """
        Устанавливает курсор в определенную позицию.
        
        @type rec: C{int}
        @param rec: Номер записи. По умолчанию C{rec=0}.
        @rtype: C{bool}
        @return: Возвращает признак успешного выполнения. При попытке установить значение курсора
            меньше нуля или больше номера последней записи функция вернет C{False}, в другом случае C{True}.
        """
        pass

    def SetStructFilter(self, flt):
        """
        Устанавливаем значение структурному фильтру.
        
        @param flt: Структурный фильтр (подробнее в описании ic.utils.translate.InitValidValue()).
        """
        self.filter = flt
