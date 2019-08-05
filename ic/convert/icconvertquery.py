#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Классы драйверов конвертера данных в табличное представление.
"""

# --- Подключение библиотек ---
from ic.db import icsqlalchemy

from ic.log import log
from ic.utils import util

from ic.components.user import ic_tab_wrp
from ic.components.user import ic_field_wrp

from ic.engine import glob_functions

# --- Спецификации ---
CONVERTQUERY_TYPE = 'ConvertQuery'

SPC_IC_CONVERTQUERY = {'type': CONVERTQUERY_TYPE,
                       'name': 'default',

                       'driver': None,      # Драйвер доступа к данным
                       'auto_clear': True,  # Автоматическое очищение результирующей таблицы
                       '__parent__': icsqlalchemy.SPC_IC_TABLE,
                       '__attr_hlp__': {'driver': u'Драйвер доступа к данным',
                                        'auto_clear': u'Автоматическое очищение результирующей таблицы',
                                        },
                       }


CONVERTFIELD_TYPE = 'ConvertField'

SPC_IC_CONVERTFIELD = {'type': CONVERTFIELD_TYPE,
                       'name': 'default',

                       'driver': None,      # Драйвер доступа к данным
                       'src_name': None,    # Имя источника данных, идентифицирующего значения поля
                       '__parent__': icsqlalchemy.SPC_IC_FIELD,
                       '__attr_hlp__': {'driver': u'Драйвер доступа к данным',
                                        'src_name': u'Имя источника данных, идентифицирующего значения поля',
                                        },
                       }

__version__ = (0, 1, 1, 1)


# --- Классы ---
class icConvertQueryPrototype:
    """
    Класс конвертера данных в табличное представление.
    """
    def __init__(self, component_spc=None):
        """
        Конструктор.
        """
        self.resource = component_spc

        # Объект управления проектом.
        self._prj_res_ctrl = None
        # Результирующая таблица
        self._tab = None
        
    def getName(self):
        """
        Имя объекта.
        """
        return self.resource['name']
        
    def getTableName(self):
        """
        Имя результирующей таблицы.
        """
        return self.resource['table']

    def getDBName(self):
        """
        Имя источника данных/БД результирующей таблицы.
        """
        return self.resource['source']
        
    def getDriverName(self):
        """
        Имя драйвера источника данных.
        """
        return self.resource['driver']
        
    def getAutoClear(self):
        """
        Автоматическое очищение результирующей таблицы.
        """
        return self.resource['auto_clear']
        
    def _isTableRes(self, table_res_name=None):
        """
        Проверить есть ли ресурсное описание результирующей таблицы.
        @param table_res_name: Имя ресурсного описание результирующей таблицы.
        Если None, тогда имя берется из ресурсного описания этого компонента.
        """
        if table_res_name is None:
            table_res_name = self.getTableName()
            
        # Открыть проект
        self._prj_res_ctrl = glob_functions.getKernel().getProjectResController()
        self._prj_res_ctrl.openPrj()
        
        return self._prj_res_ctrl.isRes(table_res_name, 'tab')

    def createTableResource(self):
        """
        Построить ресурсное описание по этому компоненту.
        """
        if not self._isTableRes():
            tab_res = self._createTabSpc()
            
            children_fld = self._getChildrenFields()
            for child_fld in children_fld:
                fld_spc = self._createFieldSpc(child_fld)
                tab_res['child'].append(fld_spc)
            self._saveTabRes(tab_res)
            
    def _saveTabRes(self, table_res):
        """
        Сохранить ресурс результирующей таблицы.
        """
        table_name = table_res['name']
        # Сохранить ресурс
        self._prj_res_ctrl.saveRes(table_name, 'tab', table_res)
        # И сразу удалить за ненадобностью
        self._prj_res_ctrl = None
        
    def _getChildrenFields(self):
        """
        Описание дочерних полей.
        """
        return [chld for chld in self.resource['child'] if chld['type'] == CONVERTFIELD_TYPE]
        
    def _createTabSpc(self, table_name=None):
        """
        Создать спецификацию результирующей таблицы.
        @param table_name: Имя результирующей таблицы.
        """
        tab_spc = util.icSpcDefStruct(util.DeepCopy(ic_tab_wrp.ic_class_spc), None)
        # Установить свойства таблицы
        if table_name is None:
            table_name = self.getTableName()
        tab_spc['name'] = table_name
        tab_spc['description'] = self.resource['description']
        tab_spc['table'] = table_name.lower()
        tab_spc['source'] = self.getDBName()

        return tab_spc

    def _createFieldSpc(self, convert_field_spc):
        """
        Создать спецификацию поля результирующей таблицы из поля конвертации.
        """
        field_spc = util.icSpcDefStruct(util.DeepCopy(ic_field_wrp.ic_class_spc), None)
        field_spc['name'] = convert_field_spc['name']
        field_spc['description'] = convert_field_spc['description']
        field_spc['field'] = convert_field_spc['field']
        field_spc['type_val'] = convert_field_spc['type_val']
        field_spc['len'] = convert_field_spc['len']
        field_spc['attr'] = convert_field_spc['attr']
        field_spc['default'] = convert_field_spc['default']

        return field_spc
   
    def convert(self):
        """
        Запуск конвертации.
        """
        self.createTableResource()
        
        # Определить базисное поле.
        # Поле относительно которого будет производится итерация записей.
        basis_field = self.getFirstField()
        if basis_field:
            # Определить драйвер
            driver = basis_field.initDriver()
            fields = self.getFields()
            # Проинициализирогвать все драйвера в полях
            for field in fields:
                field.initDriver()
            
            self._tab = icsqlalchemy.icSQLAlchemyTabClass(self.getTableName())
            if self.getAutoClear():
                self._tab.clear()
                
            # Перебор по записям
            driver.First()
            log.debug(u'START! <%s>' % driver.IsEnd())
            while not driver.IsEnd():
                print('.')
                # Перебор по полям и формирование результирующей записи
                rec = {}
                for field in fields:
                    value = field.getValue()
                    field_name = field.getName()
                    rec[field_name] = value
                # Сохранить сформированную запись в результирующей таблице.
                self._tab.add(**rec)
                
                driver.Next()            
            log.debug('OK')

    def getFirstField(self):
        """
        Первое поле.
        """
        return None
        
    def getField(self):
        """
        Список полей.
        """
        return None
        
    def getDriver(self):
        """
        Объект драйвера источника данных.
        """
        return None


class icConvertFieldPrototype:
    """
    Класс поля конвертера данных в табличное представление.
    """
    def __init__(self, parent_convert_query, component_spc=None):
        """
        Конструктор.
        """
        self.resource = component_spc
        
        self._convert_query = parent_convert_query

        # Драйвер источника данных
        self._driver = None

    def getName(self):
        """
        Имя объекта.
        """
        return self.resource['name']
        
    def getDriverName(self):
        """
        Имя драйвера источника данных.
        """
        return self.resource['driver']
        
    def getDriver(self):
        """
        Объект драйвера источника данных.
        """
        return None
        
    def initDriver(self):
        """
        Инициализация объекта драйвера источника данных.
        """
        self._driver = self.getDriver()
        if self._driver is None:
            self._driver = self._convert_query.getDriver()
        return self._driver

    def getSrcName(self):
        """
        Имя поля в источнике.
        """
        return self.resource['src_name']
        
    def getDefault(self):
        """
        Значение поля по умолчанию.
        """
        return self.resource['default']
        
    def getGetValueFunc(self):
        """
        Функцмя получения значения.
        """
        return self.resource['getvalue']
        
    def getValue(self):
        """
        Текущее значение.
        """
        if self._driver:
            src_name = self.getSrcName()
            getvalue = self.getGetValueFunc()
            if getvalue:
                # Выполнение функции получения данных
                evs = util.InitEvalSpace({'self': self,
                                          'driver': self._driver,
                                          'src_name': src_name})
                return util.ic_eval(getvalue, evalSpace=evs)[1]
            elif src_name:
                return self._driver.getDataByName(src_name)
            else:
                return self.getDefault()
        return None
