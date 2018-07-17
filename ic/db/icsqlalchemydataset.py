#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс для работы с SQLAlchemy.
@type SPC_IC_SQLOBJ_DATACLASS: C{Dictionary}
@var SPC_IC_SQLOBJ_DATACLASS: Спецификация на ресурсное описание класса данных для SQLObject.

    Описание ключей SPC_IC_SQLOBJ_DATACLASS:
    - B{name = 'DefaultName'}: Имя объекта.
    - B{type='icDataClass'}:Тип объекта.
    - B{filter=None ['@']}:Фильтр на объект данных. Фильтр может быть задан двумя способами: словарем и строкой.
        Словарь задает фильтр на значение определенных полей в объекте данных (Пример: {'peopleId': 5, 'town':'Moscow'}).
        Строка задает SQL выражение на список уникальных идентификаторов, по которым происходит привязка к номеру строки
        более подробнее см. описание функцию db.translate.InitValidValue()
        (Пример: C{Select id from table where id < 1000'}).

    - B{scheme/child=[]}: Схема данных - содержит список описаний полей.
    - B{init=None,['@']}: Выражение, вычисляемое при добавлении записи после вычисления всех полей записи
        (по атрибуту 'init' описания поля). Если оно возвращает True, то запись добавляется, в противном случае нет.
    - B{post_init=None,['@']}: Выражение, вычисляемое после добавления записи. Если оно возвращает False,
        то удалаяем созданный объект.
    - B{ctrl=None}: Выражение контроля записи. Если возвращается:
        0 - запись обновляется;
        1 - запись обновляется, но необходимо подтверждение;
        2 - запись не обновляется.
    - B{del=None}: Выражение, контроля удаления записи. Если оно возвращает True,
        то запись удаляется, в противном случае нет.
    - B{post_del=None}: Выражение, выполняется после удаления записи.
    - B{source=SPC_IC_SQLOBJ_SOURCE}: Словарь, описывающий источник данных.

@type SPC_IC_SQLOBJ_SOURCE: C{Dictionary}
@var SPC_IC_SQLOBJ_SOURCE: Спецификация на ресурсное описание источника данных.
    - B{name = 'DefaultName'}: Имя объекта.
    - B{type='SQLObjectSource'}:Тип объекта.
    - B{path=None}: Путь расположения базы данных,
    - B{filename=None}: Названия файла базы данных,
    - B{connect=None}: Строка соединения,
    - B{user='user'}: Имя пользователя,
    - B{password='pwd'}: Пароль пользователя.

@type SPC_IC_SQLOBJ_FIELD: C{Dictionary}
@var SPC_IC_SQLOBJ_FIELD: Спецификация на ресурсное описание поля.

    Описание ключей SPC_IC_SQLOBJ_FIELD:
    - B{name = 'default'}: Имя объекта.
    - B{type=tabclass.FIELD_TYPE}: Тип объекта.
    - B{description=''}: Описание поле,
    - B{label='',['@']}: Краткое описание поля,
    - B{type_val='T'}: Тип значения ('I' - целое значение, 'F' - вещественное,
        'D' - значение датa-время, 'T' - строка символов,
        'P' - ссылка на другой объект;)
    - B{len=None}: Размер хранения поля в байтах,
    - B{store=None}: - ,
    - B{dict=None,['@']}: Словарь возможных значений поля,
    - B{field=None}: Имя поля в источнике данных,
    - B{attr=0,['@']}: Аттрибут поля (0 - редактируемое поле, 1- вычисляемое,
        2 - только для чтения, 3 - вычисляемое только для чтения),
    - B{getvalue = None}: Выражение, вычисляющее значение поля для вычисляемого поля.
    - B{setvalue = None}: Функция, сохраняющее значение поля в источнике данных для вычисляемого поля.
    - B{init=None,['@']}: Выражение, вычисляющее значение поля при инициализации поля (например при добавлении записи).
    - B{ctrl:None}: Выражение для контроля значения. Если
        0 - то запись разрешена,
        1 - разрешено, но требуется продтверждение,
        2 - запрещено с предупреждением,
        3 - запрещено без предупреждения.
    - B{recount=None}: Выражение, возвращающее список пересчитываемых полей.
    - B{idx=None}: Выражение, возвращающее признак индексируемого поля:
        True - поле индексируемое, False- поле неиндексируемое.
"""

import sys
import os
import copy
import string
import time
import ic.utils.util as util
import ic.utils.resource as resource
from ic.utils import ic_uuid
import ic.utils.translate as translate

from ic.utils.coderror import *
# from ic.log.iclog import MsgLastError, LogLastError
from ic.dlg.msgbox import MsgBox
from ic.kernel import io_prnt

from . import icdataset

from ic.db import icsqlalchemy
import ic.utils.lock as ic_lock

from ic.engine import icUser as icuser
import ic.components.icwidget as icwidget
import ic.interfaces.icdatasetinterface as icdatasetinterface


SPC_IC_SQLOBJ_SOURCE = {'type': 'SQLObjectSource',
                        'name': 'default',

                        'path': None,
                        'filename': None,
                        'connect': None,
                        'user': 'user',
                        'password': 'pwd',
                        }

SPC_IC_SQLOBJ_FIELD = {'type': icsqlalchemy.FIELD_TYPE,
                       'name': 'default',
                       'description': '',

                       'label': '',
                       'type_val': 'T',
                       'len': None,
                       'store': None,
                       'dict': {},
                       'field': None,
                       'attr': 0,
                       'init': None,
                       'ctrl': None,
                       'setvalue': None,
                       'getvalue':  None,
                       'idx': None,
                       'group': [],
                       }
                        
SPC_IC_SQLOBJ_DATACLASS = {'type': 'icDataClass',
                           'name': 'DefaultName',
                           'child': [],
                           '_uuid': None,

                           'filter': None,
                           'init': None,
                           'post_init': None,
                           'ctrl': None,
                           'del': None,
                           'post_del': None,
                           'source': None,
                           }

# -------------------------------------------------------------------------------
#   Типы буферов, поддерживаемых компонентом

#   Буферизируется группа записей
BUFF_TYPE_PAGE = 0
#   Буферезируются все записи
BUFF_TYPE_ALL = 1
#   Буферизация не проводится
BUFF_TYPE_NONE = 2

msgEvalAttrError = ''' eval_attr(...)
###########################################################
#### EVAL ATTRIBUTE Error in component=%s,
####                         attribute=%s
#### <UUID = %s>
###########################################################
'''

#   Версия компонента
__version__ = (1, 0, 1, 3)


class icSQLAlchemyDataSet(icdatasetinterface.icDatasetInterface):
    """
    Интерфейс для работы с табличными данными.
    
    @type _bInspectDB: C{bool}
    @cvar _bInspectDB: Если данный флаг = True, то при каждом обращении к объекту по индексу будет проверятся изменилась ли
           таблица (см. ф-ию isTableChanged).
    """
    ISInspectDB = False
    
    def convSQL(self, query):
        """
        Заменяем в SQL запросе имена нашего из класса данных на имена табличного представления.
        """
        return query

    def __convSQL(self, query):
        """
        !!!Функция устаревшая использовалась с SQLObject!!!
        Заменяем в SQL запросе имена нашего из класса данных на имена табличного представления.
        """
        old = query
        
        #   Словарь замен
        replaceDict = {}
        
        try:
            
            ls = [x.GetIDataclass().getClassName() for x in self.evalSpace['_sources'].values()]

            if not self.GetIDataclass().getClassName() in ls:
                ls.append(self.GetIDataclass().getClassName())

            query = translate.convQueryToSQL(query, ls)
            return query
        except:
            io_prnt.ouErr(u'cinvert ERROR in Query: <%s>' % query)
            return old
            
    def GetIDataclass(self):
        """
        Возвращает указатель на интерфейс работы с классом данных.
        """
        return self.dataclassInterface
        
    def GetUniqId(self):
        """
        Возвращает уникальный идентификатор объекта.
        """
        return self._uniqId

    def GetUUID(self):
        """
        Возвращает универсальный идентификатор ресурса компонента.
        """
        return self._uuid

    def GetUUIDAttr(self, *attrs):
        """
        Возвращает уникальный иденификатор атрибута.
        """
        return ic_uuid.get_uuid_attr(self.GetUUID(), *attrs)

    def eval_attr(self, attr):
        """
        Функция вычисления атрибутов.
        
        @type attr: C{string}
        @param attr: Имя атрибута.
        """
        expr = self.resource[attr]

        if self.GetUUID():
            compileKey = self.GetUUIDAttr(attr)
        else:
            compileKey = None
        
        msg = msgEvalAttrError % (self.name, attr, compileKey)
        return util.ic_eval(expr, self.logType, self.evalSpace, msg, None, compileKey)
        
    def __init__(self, id, component={}, logType=0, evalSpace={},
                 subsys_path=None, preCreateDataclass=None):
        """
        Конструктор для создания таблицы.
        @type id: C{int}
        @param id: Идентификатор объекта.
        @type component: C{dictionary}
        @param component: Описание компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        @type subsys_path: C{string}
        @param subsys_path: Путь до подсистемы, где расположен ресурс.
        """
        if id < 0:
            self._uniqId = icwidget.icNewId()
        else:
            self._uniqId = id
            
        util.icSpcDefStruct(SPC_IC_SQLOBJ_DATACLASS, component)
        # Конструктор базового класса
        icdatasetinterface.icDatasetInterface.__init__(self, id, component, logType, evalSpace)

        self.logType = logType
        self.evalSpace = evalSpace
        self.name = component['name']
        self.type = component['type']
        self.source = component['source']
        self.resource = component
        self._uuid = component['_uuid']
        
        if not self._uuid:
            self._uuid = ic_uuid.get_uuid()
        
        self.filter = util.getSpcAttr(component, 'filter', evalSpace)
        
        if self.filter in ['None', '', None]:
            self.filter = {}

        #   Для совместимости атрибутов со старыми версиями, проверяем
        #   существования атрибута 'scheme'
        if 'scheme' in component and 'child' not in component:
            component['child'] = component['scheme']
        
        #   В схему отбираем только описания полей
        self.scheme = [x for x in component['child'] if x['type'] == icsqlalchemy.FIELD_TYPE and util.isAcivateRes(x, evalSpace)]
        
        #   Отдельно отбираем описание ссылок (links_classes содержит словарь
        #   связанных классов)
        self.links = [x for x in component['child'] if x['type'] == icsqlalchemy.LINK_TYPE and util.isAcivateRes(x, evalSpace)]
        self.link_names = [x['name']+'_id' for x in self.links]
        
        #   Аттрибут содержит идентификаторы родительских объектов, куда будут
        #   добавлятся новые объекты. Без знания идентификаторов невозможно
        #   создать новый объект текущего класса данных, если он связан с другими
        #   кдассами данных через объект icLink.
        self._prnts_id = {}
        
        #   Атрибуты выражений контроля записи
        self.ctrl_rec = component['ctrl']
        self.del_rec = component['del']
        self.init_rec = component['init']
        self.post_init_rec = component['post_init']
        self.post_del_rec = component['post_del']
        
        #   Максимальное значение идентификатора до добавления новой записи
        self.oldMaxId = -1
        
        # ----- Аттрибуты для работы с буфером страницы -------------------------
        
        #   Тип буфера ()
        self.typeBufferPage = BUFF_TYPE_PAGE
        
        #   Размер страницы
        self.sizePage = 30
        
        #   Время жизни буфферной страницы
        self.time_page_life = 3.25
        
        #   Буффер страницы
        self.bufferPageDict = {}
        
        #   Время последнего обращения к буферу страницы
        self._oldtime = 0

        # ----- Класс данных
        
        #   Атрибут остался для совместимости работы со старым прикладным кодом
        self.dataclass = None
        
        #   Интерфейс работы с классом данных
        self.dataclassInterface = preCreateDataclass
        
        #   Родительский класс данных, в который вкладываются группы -
        #   корневой класс, от которого ведется наследование.
        self.main_class = None
        
        #   Родительский класс, от которого ведется наследование.
        self.parent_class = None
        
        #   Связанные классы (через ссылки)
        self.links_classes = []
        
        #   Cловари соответствия имен полей в базе и имен аттрибутов класса.
        #   Словарь _dbColumnDict в качестве ключей содержит имена полей в
        #   таблице б.д., в качестве значений имена класса данных, _сolumnDict наоборот.
        self._dbColumnDict = {}
        self._columnDict = {}

        #   Путь до группы в классе данных, для которой создается объект навигации
        #   Пример: ['Table1','group1', 'address']
        self._groupPath = []

        #   Расположение курсора
        self.cursor = 0
        
        #   Номер буфферизированной записи
        self.cursorBuff = -1

        #   Буфферный список идентификаторов
        self.indexBuff = []
        
        #   Буфферный словарь удаленных (имеется ввиду удаленных другим
        #   пользователем или потоком) идентификаторов. В  качестве ключей
        #   используются номера строк, в качестве значений идентификаторы записей.
        self._del_indexBuff = {}

        #   Буфферный список добавленных (имеется ввиду добавленных другим поль-
        #   зователем или потоком) идентификаторов. В  качестве ключей используются
        #   номера строк, в качестве значений идентификаторы записей.
        self._add_indexBuff = []
        
        #   Выражение для фильтрации данных
        self._filterQuery = None
        
        # ----- Атрибуты для работы с фильтрами ---------------------------------
        #   Словарный фильтр. В качестве ключей имена атрибутов, в качестве
        #   значений значения поля.

        #   Признак структурного фильтра. Если на объект данных не установлен
        #   фильтр в виде SQL запроса, то установлен структурный фильтр.
        self._bStructedFilter = False
        
        #   Признак аварийного фильтра - фильтр, на основе которого генерируется
        #   синтаксически ошибочный SQL запрос.
        self._bInvalidFilter = False
        
        #   Буфер для хранения текущей записи в виде SQLObect объекта
        self.rowBuff = None

        #   Буфер накопления изменений в виде словаря
        self.changeRowBuff = None
        
        #   Список заблокированных записей компонентом
        self._lockBuff = []
        
        # ----- Атрибуты, используемые для сортировок и поиска ------------------
        
        #   Список полей или выражений, по которым сортируется таблица
        self._sortExprList = ['id']
        
        #   Признак, указывающий направление сортировки
        self._isSortDESC = False

        #   Список параметров последнего поиска:
        #   1 - строка поиска
        #   2 - словарь полей, где проводился поиск
        self._lastSearchPar = [None, None]
        
        #   Буфер идентификаторов найденных строк
        self._lastSearchIds = []
        
        # ----- Открываем источник данных ---------------------------------------
        self.Open(self.filter)
        
        # ----- Подготавливаем необходимые структуры ---------------------------
        
        #   Признаки начала и конца файла
        self.bBof = True
        self.bEof = True
        
        #   Словарь индексов полей
        self.indexFld = {}

        #   Список полей
        self.listFld = range(len(self.scheme))
        
        #   Заполняем словарь индексов полей и список полей
        for indx, fld in enumerate(self.scheme):
            
            #   Заодно проверяем на соответствии описания поля спецификации
            util.icSpcDefStruct(SPC_IC_SQLOBJ_FIELD, fld)
            
            self.indexFld[fld['name']] = indx
            self.listFld[indx] = fld['name']

    def setTimePageLife(self, tm):
        """
        Устанавливает время актуальности информации в буферной странице.
        """
        self.time_page_life = tm
        
    def getTimePageLife(self):
        """
        Возвращает время актуальности информации в буферной странице.
        """
        return self.time_page_life
    
    def buffAllData(self, tm=-1):
        """
        Устанавливает режим полной буферизации и буферизирует данные.
        
        @type tm: C{float}
        @param tm: Время актуальности информации.
        """
        #   Устанавливаем время актуальности информации
        self.setTimePageLife(tm)
        
        #   Устанавливаем тип буферизации (буферезируем все данные)
        self.setTypePageBuff(BUFF_TYPE_ALL)
    
        if self._filterQuery:
            
            query = self._filterQuery.replace('FROM', 'from').replace('From', 'from')
            nf = query.find('from')
            
            if nf >= 0:
                query = 'select * ' + self._filterQuery[nf:]
                
            result = self.GetIDataclass().queryAll(query)
            if result is None:
                rss = []
            else:
                rss = list(result)
            
            #   Чистим буфер
            self.bufferPageDict = {}
        
            #   Заполняем буфер
            for rs in rss:
                dict = {}
                    
                for indx, dbName in enumerate(self.GetIDataclass().getFieldNames(True)):
                
                    if dbName in self._dbColumnDict:
                        fldName = self._dbColumnDict[dbName]
                        dict[fldName] = rs[indx]
                        
                id = dict[self.CetIDataclass().getIdName()]
                self.bufferPageDict[id] = dict

    def setTypePageBuff(self, typeBuff=BUFF_TYPE_PAGE):
        """
        Устанавливает тип буфера.
        
        @type typeBuff: C{int}
        @param typeBuff: Тип буферизации.
        """
        self.typeBufferPage = typeBuff
    
    def getTypePageBuff(self):
        """
        Возвращает признак поддержки буфера страницы.
        
        @rtype: C{bool}
        @return: Возвращает признак поддержки буфера страницы.
        """
        return self.typeBufferPage
        
    def clearPageBuff(self, tm=None, typeBuff=BUFF_TYPE_PAGE):
        """
        Чистит буфер страницы.
        
        @type tm: C{float}
        @param tm: Время актуальности информации.
        @type typeBuff: C{int}
        @param typeBuff: Тип буферизации.
        """
        self.time_page_life = tm or self.time_page_life
        self.typeBufferPage = typeBuff
        self.bufferPageDict = {}
        
    def createPageBuff(self, rec, sz=None):
        """
        Создает буфер страницы. Последней записью буфера будет строка с номером rec.
        
        @type rec: C{int}
        @param rec: Номер последней записи буфера.
        """
        #   Вычисляем интервал идентификаторов, которые попали в буферную страницу
        if sz is None or sz <= 0:
            sz = self.sizePage
            
        beg = rec - sz
        
        if beg < -1:
            beg = -1

        idn = self.GetIDataclass().getIdName()
        
        id_beg = self.getId(beg+1, True)
        id_rec = self.getId(rec, True)
        bSortExpr = False

        #   В режиме сортировки буферезировать лишние записи смысла нет
        bSortId = False

        if self._sortExprList and self._sortExprList[0] == idn:
            bSortId = True
        
        if 'order by' in self._filterQuery.lower() and not bSortId:
            bSortExpr = True
            id_beg = id_rec
        
        #   Если буфер идентификаторов пуст
        if id_beg is None and id_rec is None:
            self.bufferPageDict = {}
            return self.bufferPageDict

        #
        if id_beg is None and id_rec is not None:
            id_beg = id_rec

        if id_rec - id_beg > 3 * sz:
            id_beg = id_rec - sz
        elif id_beg - id_rec > 3 * sz:
            id_beg = id_rec + sz
        
        #
        if id_beg > id_rec:
            _b = id_beg
            id_beg = id_rec
            id_rec = _b
        
        if id_beg == id_rec:
            query = 'select * from %s where %s=%d' % (self.getDBTableName(), idn, id_rec)

        #   Если конец промежутка совпадает с последней записью буфера, то запрос делаем с небольшим превышением
        #   на тот случай если в таблице появились новые записи
        elif id_rec == self.getMaxId():
            query = 'select * from %s where %s>=%d and %s<%d' % (self.getDBTableName(), idn, id_beg, idn, id_rec+sz)
        else:
            query = 'select * from %s where %s>=%d and %s<=%d' % (self.getDBTableName(), idn, id_beg, idn, id_rec)

        #   Чистим буфер
        self.bufferPageDict = {}
        cur = beg+1
        
        #   Формируем буфер
        result = self.GetIDataclass().queryAll(query)
        if result is None:
            rss = []
        else:
            rss = list(result)
        
        for rs in rss:
            dict = {}
                    
            for indx, col_name in enumerate(self.GetIDataclass().getFieldNames(True)):
                dbName = col_name
                
                if dbName in self._dbColumnDict:
                    fldName = self._dbColumnDict[dbName]
                    dict[fldName] = rs[indx]
                        
            id = dict[self.GetIDataclass().getIdName()]
            self.bufferPageDict[id] = dict
                
            #   Буфферизируем идентификаторы, значение которых больше, значения
            #   максимального идентификатора объекта данных, если на объект не
            #   установлено ни каких фильтров. Это возможно в случае дабавление
            #   записей другим пользователем или потоком. Если установлен фильтр
            #   или задано выражение для сортировки, то механизм добавления будет
            #   работать непредсказуемо, то будет добавлять, то не будет, поскольку
            #   идентификаторы могут распологаться неравномерно. Поэтому оставляем
            #   один вариант, когда фильтр и выражение для сортировки (за исключением
            #   сортировки по id) для объекта данных не определены.
            if (id > self.getMaxId() and self._bStructedFilter and self.filter == {} and
                    not bSortExpr and id not in self._add_indexBuff):
                self._add_indexBuff.append(id)
            
        return self.bufferPageDict

    def createPageBuff2(self, rec, sz=None):
        """
        Создает буфер страницы. Последней записью буфера будет строка с номером rec.
        Работает медленно, но железно.
        
        @type rec: C{int}
        @param rec: Номер последней записи буфера.
        """
        #   Вычисляем интервал идентификаторов, которые попали в буферную страницу
        if sz is None or sz <= 0:
            sz = self.sizePage
            
        beg = rec - sz
        
        if beg < -1:
            beg = -1

        idn = self.GetIDataclass().getIdName()
        bSortId = False
        bSortExpr = False
        if self._sortExprList and self._sortExprList[0] == idn:
            bSortId = True
        if 'order by' in self._filterQuery.lower() and not bSortId:
            bSortExpr = True
        
        #   Создаем список идентификаторов буферезируемых строк
        idLst = [self.getId(cur) for cur in xrange(beg+1, rec+1)]

        if not idLst or (idLst and None in idLst):
            self.bufferPageDict = {}
            return self.bufferPageDict

        sRecId = '%s>%d' % (idn, self.getMaxId())
        for id_rec in idLst:
            sRecId = '%s or %s=%d' % (sRecId, idn, id_rec)
            
        query = 'select * from %s where %s' % (self.getDBTableName(), sRecId)
        
        #   Чистим буфер
        self.bufferPageDict = {}
        cur = beg+1
        
        #   Формируем буфер
        result = self.GetIDataclass().queryAll(query)
        if result is None:
            rss = []
        else:
            rss = list(result)
        
        for rs in rss:
            dict = {}
                    
            for indx, dbName in enumerate(self.GetIDataclass().getFieldNames(True)):
                
                if dbName in self._dbColumnDict:
                    fldName = self._dbColumnDict[dbName]
                    dict[fldName] = rs[indx]
                        
            id = dict[self.GetIDataclass().getIdName()]
            self.bufferPageDict[id] = dict
                
            #   Буфферизируем идентификаторы, значение которых больше, значения
            #   максимального идентификатора объекта данных, если на объект не
            #   установлено ни каких фильтров. Это возможно в случае дабавление
            #   записей другим пользователем или потоком. Если установлен фильтр
            #   или задано выражение для сортировки, то механизм добавления будет
            #   работать непредсказуемо, то будет добавлять, то не будет, поскольку
            #   идентификаторы могут распологаться неравномерно. Поэтому оставляем
            #   один вариант, когда фильтр и выражение для сортировки (за исключением
            #   сортировки по id) для объекта данных не определены.
            if (id > self.getMaxId() and self._bStructedFilter and self.filter == {} and
                    not bSortExpr and id not in self._add_indexBuff):
                self._add_indexBuff.append(id)
            
        return self.bufferPageDict
    
    def getNameValue(self, fieldName, rec=None, bReal=False, bFromBuff=True):
        """
        Функция по имени колонки и номеру записи возвращает значение из буфера.
        
        @type rec: C{int}
        @param rec: Номер строки.
        @type fieldName: C{string}
        @param fieldName: Имя поля.
        @type bReal: C{bool}
        @param bReal: Признак возвращения реального значения из таблицы данных, а не вычисленного значения либо значения по справочнику.
        @type bFromBuff: C{bool}
        @param bFromBuff: Признак, который указывает, что значения можно брать из
            буфера измененных значений.
        @rtype: C{...}
        @return: По имени колонки и номеру записи возвращает значение из буфера. Если поле или номер записи
            указаны не верно, то функция возвращает C{None}.
        """
        #   Проверка на права доступа к данному методу
        if not icuser.canAuthent('r', self.name,  icuser.ACC_DATA,  False):
            return ''

        #   Если номер строки не указан, то номер записи определяем по положению курсора
        if rec is None:
            rec = self.cursor
        
        try:
            info = self.getFieldInfo(fieldName)
            
            if info:
                
                #   Получаем доступ к буферу текущей записи
                if rec < self.getRecordCount():
                    self.rowBuff = self.getDict(rec, True)
                else:
                    self.rowBuff = None
                    
                #   self.rowBuff == None может быть по следующим причинам:
                #   - база заблокирована транзакцией
                #   - проблемы с сеткой
                value = None
                
                #   Проверяем буфер изменений. Если там есть значение, то берем
                #   его из буфера.
                if bFromBuff and (self.changeRowBuff is not None and rec in self.changeRowBuff
                   and fieldName in self.changeRowBuff[rec]):
                    value = self.changeRowBuff[rec][fieldName]
                
                elif self.rowBuff is not None and fieldName in self.rowBuff:
                    value = self.rowBuff[fieldName]
                    
                #   Если определен атрибут getvalue, то вычисляем его значение
                if info['getvalue'] and not bReal:
                    self.evalSpace['rec'] = rec
                    self.evalSpace['value'] = value
                    self.evalSpace['fieldName'] = fieldName
                    self.evalSpace['self'] = self
                        
                    res, val = util.ic_eval(info['getvalue'], 0, self.evalSpace,
                                            'Exception in icbase.icDataSet.getNameValue()<getvalue>',
                                            compileKey=self.GetUUIDAttr('getvalue', fieldName))
                    if res:
                        value = val
                        
                # ---- Для ссылок по id заменяем id на значение из справочника ---------
                pt = self.pointType(info)

                if pt == 'R' and not bReal and value is not None:
                    try:
                        value = self.spravBuff[fieldName][value]
                    except:
                        io_prnt.outLastErr()
                    
                # -------------------------------------------------------------------------------
                if value is None:
                    value = ''
                
                return value
                    
        except:
            io_prnt.outErr('Error in field = \'%s\'' % fieldName)
        
        return None

    def convertToDBVal(self, fieldName, value):
        """
        Конвертирует значение в вид, в котором будет хранится в базе данных (например для хранения ссылок).
        
        @type fieldName: C{string}
        @param fieldName: Название поля.
        @param value: Конвертируемое значение.
        @return: Возвращает преобразованное значение.
        """
        #   Определяем тип ссылки. 'D' - ссылка по значению, 'R '- по идентификатору.
        info = self.getFieldInfo(fieldName)
        pt = self.pointType(info)
        
        if type(value) in (str, unicode):
            value = value.strip()
                                
        if pt == 'D':
                        
            #   Определяем есть ли такое значение в справочнике, если есть то заносим в базу, если нет,
            #   выдадим сообщение о том, что такое значение в справочнике не определено
            if value in self.spravBuff[fieldName].values():
                return value
            else:
                MsgBox(None, u' (D) Значение %s в справочнике %s не определено' % (str(value), str(info['dict'])))
                            
        elif pt == 'R':
                        
            #   Ищем соответствующий идентификатор
            for key in self.spravBuff[fieldName].keys():
                if self.spravBuff[fieldName][key] == value:
                    return key
                            
            MsgBox(None, u' (R) Значение %s в справочнике %s не определено' % (str(value), str(info['dict'])))
        else:
            return value
            
        return None
        
    def ctrlVal(self, fieldName, value, rec, bReal=False, bCtrl=True):
        """
        Функция возвращает код выражения контроля поля и реальное значение, которое
        будет храниться в базе.
        
        @param fieldName: Имя поля
        @type fieldName: C{string}
        @param value: Значение
        @type value: C{...}
        @param rec: Номер записи
        @type rec: C{int}
        @type bReal: C{bool}
        @param bReal: Признак сохранения значения без вызова функционала аттрибута 'setvalue'.
        @type bCtrl: C{bool}
        @param bCtrl: Признак указывающий на необходимость контроля значения поля.
        @return: Возвращает картеж из кода контроля и реального значения поля в базе.
            Коды контроля - 0 или 1 в случае успеха, в противном случае 2 или None.
        """
        info = self.getFieldInfo(fieldName)
        ctrl_val = IC_CTRL_OK
        val = None
        
        if info != {}:
            
            #   Определяем выражение для контроля
            try:
                _ctrl = info['ctrl']
            except:
                _ctrl = None
                
            # --- Обрабатываем фильтры
                    
            #   Конвертируем в нужный вид хранения, если не задан признак прямого сохранения.
            if not bReal:
                val = self.convertToDBVal(fieldName, value)
                
            #   Если задан фильтр, то значение берется из фильтра
            if isinstance(self.filter, dict) and fieldName in self.filter.keys():
                #   Если есть значение хранения, то подставляем его
                if val is not None:
                    val = translate.InitValidValue(self.filter, fieldName, val)
                else:
                    val = translate.InitValidValue(self.filter, fieldName, value)
                    
            #   Если задан признак прямого сохранения, проверяем есть ли у данного поля словрь
            #   приемлемых значений. Если справочник задан и значение не
            #   содержится в этом справочнике, то значение не записывается в базу
            elif bReal and not (fieldName in self.spravBuff and value in self.spravBuff[fieldName].values()):
                val = None
            else:
                val = value
                
            # --- Подготавливаем пространство имен
            self.evalSpace['rec'] = rec
            self.evalSpace['fieldName'] = fieldName
            self.evalSpace['value'] = value
            self.evalSpace['val'] = val
            
            # -------------------------------------------------------------------
            #   Если задано выражение для сохранения значения, то вычисляем его
            if info['setvalue'] and not bReal:
                ret, ret_val = util.ic_eval(info['setvalue'], 0, self.evalSpace,
                                            'Exception in icbase.icsqlobjdataset.ctrlVal()<setvalue>',
                                            compileKey=self.GetUUIDAttr('setvalue', fieldName))
                if ret:
                    val = ret_val
                            
            # -------------------------------------------------------------------
            #   Если задано выражения для контроля и установлен соответствующий
            #   признак, то вычисляем его
            if val is not None and _ctrl and bCtrl:
                ret, ctrl_ret = util.ic_eval(_ctrl, 0, self.evalSpace,
                                             'Exception in icbase.icsqlobjdataset.ctrlVal()<ctrl>',
                                              compileKey=self.GetUUIDAttr('ctrl', fieldName))
                if ret:
                    try:
                        #   Если тип выражения картеж, то первый
                        #   элемент код контроля, второй словарь значений
                        if isinstance(ctrl_ret, tuple):
                            
                            ctrl_val = ctrl_ret[0]
                            values = ctrl_ret[1]
                            
                            if isinstance(values, dict):
                                for fld in values:
                                    val = values[fld]
                                    self.setNameValue(fld, val)
                        else:
                            ctrl_val = int(ctrl_ret)
                    except:
                        io_prnt.outErr(u'INVALID RETURN CODE in CtrlVal')
                        ctrl_val = IC_CTRL_OK
                        
                    if ctrl_val == IC_CTRL_FAILED:
                        io_prnt.outWarning(u'control Error cod=IC_CTRL_FAILED')
                        val = None
        
        return ctrl_val, val
                    
    def setNameValue(self, fieldName, value, rec = None, bReal = False, bCtrl = True):
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
        @param bReal: Признак сохранения значения без вызова функционала аттрибута 'setvalue'.
        @type bCtrl: C{bool}
        @param bCtrl: Признак указывающий на необходимость контроля изменяемого значения.
        @return: Возвращает в случае успеха код контроля (0,1,2), в противном случае None.
        """
        #   Проверка на права доступа к данному методу
        if not icuser.canAuthent('wr', self.name, icuser.ACC_DATA):
            return None

        #   Код контроля
        ctrl_val = 0
        if rec is None:
            rec = self.cursor
        try:
            info = self.getFieldInfo(fieldName)
            #   Получаем доступ к буферу записи
            if rec != self.cursorBuff or self.rowBuff is None or isinstance(self.rowBuff, dict):
                self.rowBuff = self.getObj(rec, True)
                self.cursorBuff = rec
            #   Если запись заблокирована, то корректировка отменяется. Блокировка производится по имени таблицы и
            #   идентификатору записи
            try:
                id = getattr(self.rowBuff, self.GetIDataclass().getIdName())
                bLock = self.GetIDataclass().IsLockObject(id)
            except:
                id = -1
                bLock = False
            
            # ---- Заносим изменения если запись не заблокирована либо
            #   заблокирована текущим объектом
            if info != {} and (not bLock or (id in self._lockBuff and bLock)):
                
                #   Преобразуем значение поля к виду хранения и осуществляем
                #   контроль значения
                ctrl_val, val = self.ctrlVal(fieldName, value, rec, bReal, bCtrl)
                
                #   Если поле нормальное, то вносим в буффер изменений
                #   соответствующий ключ и значение
                if (ctrl_val in [IC_CTRL_OK, IC_CTRL_REPL] and val is not None and
                   int(info['attr']) == icdataset.icNormalFieldType):
                    
                    if self.changeRowBuff is None:
                        self.changeRowBuff = {rec: {}}
                    
                    if rec in self.changeRowBuff:
                        self.changeRowBuff[rec][fieldName] = val
                    else:
                        self.changeRowBuff[rec] = {fieldName: val}
                        
                    io_prnt.outLog(u'BUFF_ROW=%s' % self.changeRowBuff[rec])

                return ctrl_val
        except:
            io_prnt.outErr('Error in \'%s\'' % fieldName)
        
        return None
    
    def update(self, values=None, rec=None, bReal=False, bCtrl=True):
        """
        Устанавливает значения полей заданной строки. Если имя поля не
        найдено в источнике данных, то функция пытается выполнить функцию
        на запись по описанию колонки из ресурсного описания по аттрибуту
        'setvalue'. Если словарь обновлений (values) не определен, то
        обновления берутся из буфера изменений строки.
        @type rec: C{int}
        @param rec: Номер записи.
        @type values: C{dictionary}
        @param values: Словарь значений. В качестве ключей используются имена полей.
        @type bReal: C{bool}
        @param bReal: Признак сохранения значения без вызова функционала аттрибута 'setvalue'.
        @type bCtrl: C{bool}
        @param bCtrl: Признак указывающий на необходимость контроля изменяемого значения.
        @return: Возвращает код контроля записи.
        """
        ctrl_val = 0
        bCtrlField = True
        if rec is None:
            rec = self.cursor
        
        #   Берем значения из буфера изменений. В этом случае контроль поля
        #   проводить уже не надо
        if values is None and self.changeRowBuff is not None and rec in self.changeRowBuff:
            values = self.changeRowBuff[rec]
            bCtrlField = False
        
        #   Если словарь изменений пуст, то выходим из процедуры
        if values is None or values == {}:
            return ctrl_val
        
        try:
            #   Получаем доступ к буферу записи
            if rec != self.cursorBuff or self.rowBuff is None or isinstance(self.rowBuff, dict):
                self.rowBuff = self.getObj(rec, True)
                self.cursorBuff = rec
            #   Если запись заблокирована, то корректировка отменяется. Блокировка
            #   производится по имени таблицы и идентификатору записи
            try:
                id_name = self.GetIDataclass().getIdName()
            except AtributeError:
                id = 'id'

            id = list(self.rowBuff)[-1][0]
            bLock = self.GetIDataclass().IsLockObject(id)
            # -------------------------------------------------------------------
            #   Заносим изменения если запись не заблокирована либо заблокирована
            #   текущим объектом
            if not bLock or (id in self._lockBuff and bLock):
                record = {}
                if not bCtrlField:
                    record = values
                else:
                    for fieldName in values:
                        value = values[fieldName]
                        #   Преобразуем значение поля к виду хранения и осуществляем
                        #   контроль значения
                        ctrl_fld, val = self.ctrlVal(fieldName, value, rec, bReal, bCtrl)
                        if ctrl_fld == IC_CTRL_FAILED:
                            record = None
                            return ctrl_fld
                        elif val is not None:
                            record[fieldName] = val
                # ---------------------------------------------------------------
                #   Если задано выражения для контроля записи и установлен
                #   соответствующий признак, то вычисляем его
                if record is None and self.ctrl_rec and bCtrl:
                    ret, ctrl_ret = self.eval_attr('ctrl')
                    if ret:
                        try:
                            ctrl_val = int(ctrl_ret)
                        except:
                            ctrl_val = IC_CTRL_OK
                        if ctrl_val == IC_CTRL_FAILED:
                            io_prnt.outWarning(u'control Error cod=IC_CTRL_FAILED')
                            record = {}
                # ---------------------------------------------------------------
                #   Если поле нормальное, то изменяем соответствующий атрибут
                #   объекта данных
                io_prnt.outLog(u'UPDATE RECORD=%s: %s' % (rec, record))
                if record is not None and record != {}:
                    tab = self.GetIDataclass()
                    if tab:
                        record = tab._record_norm(record)
                        tab.update(id, **record)
                    
                    #   Чистим буфер изменений данной строки
                    self.clearChangeRowBuff(rec)
                    #   Обновляем буфер страницы
                    self.createPageBuff(rec)
                        
                return ctrl_val
        except:
            io_prnt.outErr('Error in set(\'%s\')' % values)
        
        return None
    
    def getChangeRowBuff(self):
        """
        Возвращает буфер изменений.
        """
        return self.changeRowBuff
        
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
            
        if rec < 0:
            self.changeRowBuff = {}
        else:
            try:
                self.changeRowBuff.pop(rec)
            except:
                pass
        
    def getFieldList(self):
        """
        Функция возвращает список полей.
        
        @rtype: C{list}
        @return: Возвращает список полей.
        """
        return self.listFld
    
    def getFieldInfo(self, fieldName):
        """
        Возвращает описание поля.
 
        @type fieldName: C{string}
        @param fieldName: Имя колонки
        @return: Возвращает описание поля. Если описание не найдено, то возвращает {}. Поле описывается словарем.
        @rtype: C{dictionary}
        """
        try:
            indx = self.indexFld[fieldName]
            
            if fieldName == self.GetIDataclass().getIdName():
                return {'name': 'id', 'attr': 0, 'init': None, 'ctrl': None}
            
            #
            if self.scheme[indx]['attr'] is None:
                self.scheme[indx]['attr'] = icdataset.icNormalFieldType
                
            return self.scheme[indx]
        
        except KeyError:
            #   Штатная ситуация если поле вычисляемое
            fld = {'name': fieldName, 'attr': icdataset.icVirtualFieldType, 'init': None, 'ctrl': None}
            util.icSpcDefStruct(SPC_IC_SQLOBJ_FIELD, fld)
            return fld

    def isFieldIndexed(self, fieldName):
        """
        Возвращает признак индексированного поля.
 
        @type fieldName: C{string}
        @param fieldName: Имя колонки
        @return: Возвращает признак индексированного поля.
        @rtype: C{dictionary}
        """
        fld_info = self.getFieldInfo(fieldName)
        
        if fld_info != {}:
            return bool(fld_info['idx'])
            
        return False
        
    def AddExternal(self):
        """
        Функция добавляет в наш объект идентификаторы записей , добавленных другими пользователями либо другим
        объектом данных.
        
        @rtype: C{bool}
        @return: Количество добавленных записей в объект данных.
        """
        lenBuff = len(self._add_indexBuff)
        
        for id in self._add_indexBuff:
            self.indexBuff.append((id,))
            
            if id > self.oldMaxId:
                self.oldMaxId = id
        
        #   Чистим буфер внешних идентификаторов
        self._add_indexBuff = []
        
        #   Переводим курсор на последнюю запись
        self.Move(-1)
        
        return lenBuff
     
    def addRecord(self, values=None, postAddExpr=None, uuid_postAddExpr=None):
        """
        Функция добавляет новую запись.

        @param fieldName: Имя колонки.
        @type fieldName: C{string}
        @type values: C{dictionary}
        @param values: Словарь известных значений. В качестве ключей имена полей,
            значения полей в качестве значений.
        @type postAddExpr: C{string}
        @param postAddExpr: Выражение, выполняемое после добавления объекта. Если
            оно возвращает False, то добавленный объект уничтожается. Если параметр
            не определен, то выполняется выражение определенное в ресурсном описании
            в атрибуте <post_init>.
        @type uuid_postAddExpr: C{string}
        @return uuid_postAddExpr: Универсальный идентификатор выражения postAddExpr.
        @return: Возвращает признак успешного выполнения.
        @rtype: C{bool}
        """
        #   Проверка на права доступа к данному методу
        if not icuser.canAuthent('a', self.name,  icuser.ACC_DATA,  True):
            return False

        rec = self.getRecordCount()
        
        try:
            isFromBuff = False
            
            if values is None and self.changeRowBuff is not None and rec in self.changeRowBuff:
                values = self.changeRowBuff[rec]
                
                if values:
                    isFromBuff = True
        
            if values == None:
                values = {}
            
            # ---- Формируем пространство имен
            self.evalSpace['_lfp'] = {'func': 'addRecord', 'values': values}
            self.evalSpace['self'] = self
            self.evalSpace['values'] = values
            record = {}
            fldList = self.getFieldList()
                        
            #   Определяем значения полей при добавлении записи
            for indx, fld in enumerate(fldList):
                
                self.evalSpace['col'] = indx
                inf = self.getFieldInfo(fld)
                val = None
                ctrl_val = IC_CTRL_OK
                bValFromBuff = False

                #   Если поле принадлежит словарю определенных значений и не
                #   принадлежит структурному фильтру
                if fld in values.keys():
                    
                    #   Конвертируем в нужный вид хранения, если значения не из буфера
                    #   измененных полей. Т.к. в буфере значения уже преобразованные
                    val = values[fld]
                    
                    if isFromBuff:
                        bValFromBuff = True
                                                     
                #   Если значение поля не определено, то вычисляем его по
                #   атрибуту поля 'init'.
                if val is None:
                    val = util.getICAttr(inf['init'], self.evalSpace,
                                         'Exception in icsqlobjdataset.addRecord()')

                #   Если задан структурный фильтр, то значение берется из фильтра.
                #   self._bInvalidFilter - признак того, что на основе фильтра
                #   не генерируется синтаксически верный SQL запрос
                if isinstance(self.filter, dict) and fld in self.filter.keys():
                    #
                    if self._bInvalidFilter:
                        io_prnt.outWarning(u'Invalid Filter in addRecord <return False>')
                        return False
                    
                    val = translate.InitValidValue(self.filter, fld, val)

                # ---- Контроль значения ----------------------------------------
                #   Проводим контроль значения, если значение не из буфера. Т.к.
                #   для них контроль уже проведен
                
                if val and not bValFromBuff:
                    #   Преобразуем значение поля к виду хранения и осуществляем
                    #   контроль значения
                    ctrl_val, obj = self.ctrlVal(fld, val, rec)
                    io_prnt.outLog(u'CTRL FIELD: [%s : %s : %s]' % (val, ctrl_val, obj))
                                      
                    #   Если контроль не прошел, сообщаем об этом
                    if ctrl_val == IC_CTRL_FAILED:
                        MsgBox(None, u'Конфликт атрибутов поля <init> и <ctrl>. Контроль поля %s значение' % (fld, val))
                        return False
                    elif ctrl_val == IC_CTRL_FAILED_IGNORE:
                        return False

                # ---- Преобразум значение к нужному типу ------------------------
                if inf['type_val'] in [icdataset.icNumberFieldType, 'I', 'P']:
                    try:
                        val = int(val)
                    except:
                        val = 0
                        
                elif inf['type_val'] in [icdataset.icDoubleFieldType, 'F']:
                    try:
                        val = float(val)
                    except:
                        val = 0.0
                        
                else:
                    if val is None:
                        val = u''

                #   Заполняем буфер записи
                if fld != self.GetIDataclass().getIdName():
                    record[fld] = val
            
            # ---- Выполняем выражения для контроля записи по атрибуту таблицы или
            #   группы 'init'
            isAdd = True
            
            if self.init_rec not in ['', None]:
                self.evalSpace['record'] = record
                res, val = self.eval_attr('init')
                
                if res:
                    isAdd = bool(val)
            if isAdd:
                # ---- Если определены ссылки с другими классами, то получаем нужные
                #   объекты данных классов и прописываем их в параментрах нового
                #   объекта
                if self.links != []:
                    for lnk in self.links:

                        if not lnk['table']:
                            MsgBox(None,u'DATASET: <%s> Не определена ссылка на таблицу.' % self.name)
                            continue
                        #   Создает
                        prnt_class = icsqlalchemy.icSQLAlchemyTabClass(lnk['table'][0][1])
                        
                        try:
                            id_class = self.filter[lnk['name']]
                            
                        #   Если фильтр не содержит идентификатора родительской
                        #   таблицы, то ищем в спецальном атрибута класса, который
                        #   устанавливается через функцию setParentIdDict().
                        except:
                            id_class = self.getParentId(lnk['table'][0][1])
                            
                        record[lnk['name']] = id_class
                
                tab = self.GetIDataclass()
                record = tab._record_norm(record)
                newobj = tab.add(**record)
                if newobj is None:
                    # Ошибка добавления записи в таблицу
                    return False
                new_id = newobj.last_inserted_ids()[-1]
                old_max_id = self.oldMaxId
                self.oldMaxId = new_id
                
                # ---- Выполняем выражение <post_init>. Если оно возвращает False,
                #   то удалаяем созданный объект
                res = True
                
                if postAddExpr and uuid_postAddExpr:
                    res, val = util.ic_eval(postAddExpr, 0, self.evalSpace,
                                            'Exception in icbase.icsqlobjdataset.addRecord() <post_init>',
                                            compileKey=uuid_postAddExpr)
                elif postAddExpr:
                    res, val = util.ic_eval(postAddExpr, 0, self.evalSpace,
                                            'Exception in icbase.icsqlobjdataset.addRecord() <post_init>')
                elif not self.resource['post_init'] in (None, '', 'None'):
                    res, val = self.eval_attr('post_init')
                    
                if res:
                    #   Дополняем буфер индексов
                    self.indexBuff.append((new_id,))
                    
                    #   Переводим курсор на последнюю запись
                    self.Move(-1)
                    
                    #   Чистим буфер введенной записи
                    self.clearChangeRowBuff(rec)
                else:
                    self.GetIDataclass().delete(new_id)
                    self.oldMaxId = old_max_id
                    io_prnt.outLog(u'addRecord Rollback on <post_init>')
                    return False
        except:
            io_prnt.outErr(u'Error in AddRecord')
            return False
        
        return True

    def delRecord(self, rec=None):
        """
        Удаляет запись из источника данных.

        @param rec: Номер записи.
        @type rec:  C{int}
        @return: Признак успешного выполнения.
        @rtype: C{bool}
        """
        #   Проверка на права доступа к данному методу
        if not icuser.canAuthent('d', self.name, icuser.ACC_DATA,  True):
            return IC_DEL_FAILED

        if rec is None:
            rec = self.cursor
              
        codDel = IC_DEL_OK
        
        try:
            #   Если запись помечена как удаленная из источника данных,
            #   удаляем из буфера помеченных записей
            if self.isDeleted(rec):
                del self._del_indexBuff[rec]
            else:
                id = self.getId(rec, True)
                
                #   Если запись заблокирована, то отменяем удаление записи
                if not self.GetIDataclass().IsLockObject(id):
                    
                    # ---------------------------------------------------------------
                    #   Если в атрибуте ресурсного описания 'del' опрелено выражение,
                    #   то выполняем его. Если вырвжие возыращает 0 или 1, то разрешаем
                    #   удаление объекта, если None или > 2, то запрещаем удаление.
                    #   Этот атрибут анализируется в функции del_rec, т. к. эта
                    #   функция контролирует каскадное удаление.

                    # ---------------------------------------------------------------
                    #   Функция удаляет объект по схеме, если связи с подчиненными
                    #   таблицами жесткие, то удаляются все подчиненные записи
                    codDel = self.GetIDataclass().delete(id)
                else:
                    codDel = IC_DEL_FAILED
                    MsgBox(None, u'Удаление не возможно, т. к. запись заблокирована!')
                    
            #   Если объект успешно удален из класса данных
            if codDel == IC_DEL_OK:
                #   Чистим буфер строки
                self.rowBuff = None
                self.clearChangeRowBuff()
                
                #   Удаляем элемент из буфера идентификаторов
                del self.indexBuff[rec]
                                
                if self.cursor >= self.getRecordCount():
                    #   Если удалили последнюю запись, то изменяем сохраняемое значение максимального идентификатора
                    self.getMaxId(recount=True)
                    self.Move(-1)
                
            #   <post_del> обрабатываем в любом случае
            if self.post_del_rec:
                self.eval_attr('post_del')
        except:
            io_prnt.outErr(u'DELETE RECORD ERROR')
            codDel = IC_DEL_FAILED
            
        return codDel
    
    def write(self, rec=-1):
        """
        Сохранение записи непосредственно в источник данных.
        
        @param rec: Номер записи. Если rec =-1, то записывается текущая запись.
        @type rec: C{int}
        @rtype: C{bool}
        @return: Признак успешной записи.
        """
        pass
    
    def read(self, rec=-1):
        """
        Обновление буфера записи непосредственно из источника данных.
        
        @param rec: Номер записи. Если rec =-1, то читается текущая запись.
        @type rec:  C{int}
        @rtype: C{bool}
        @return: Признак успешной записи.
        """
        if self.GetIDataclass() is not None:
            if rec == -1:
                rec = self.cursor

    def Open(self, filter_tab=None):
        """
        Открытие источника данных.
        
        @type filter_tab: C{string | dictionary}
        @param filter_tab: SQL выражение для фильтрации данных. Пример: C{ds.Open('select id from table where id > 100 and id < 200')}
        @rtype: C{bool}
        @return: Признак успешного открытия.
        """
        
        self._groupPath = self.name.split('.')
        
        #   По схеме создаем класс данных и соединяемся с источником данных
        self.name = self.resource['name'] = self._groupPath[0]
        
        #   Определяем путь до подсистемы откуда взят ресурс. Это нужно tabclass-у
        #   для создания каскада таблиц
        if '__subsys_path' in self.resource:
            subsys_path = self.resource['__subsys_path']
        else:
            subsys_path = None
            
        if not self.dataclassInterface:
            self.dataclassInterface = icsqlalchemy.icSQLAlchemyDataClass(self.resource, subsys_path, False)
        self.dataclass = self.dataclassInterface.dataclass
        
        self.parent_class = None
        self.main_class = self.GetIDataclass()

        if self.GetIDataclass() is None:
            return False
        
        # ---- Создаем словари соответствия имен полей в базе и имен аттрибутов класса -------------------------------
        
        self._columnDict = {}
        self._columnDict[self.GetIDataclass().getIdName()] = self.GetIDataclass().getIdName()
        self._dbColumnDict = self.GetIDataclass().getDBColumnNameDict()
        
        for dbName, name in self._dbColumnDict.items():
            self._columnDict[name] = dbName
            
        #   При первом обращении заполняем буфер индексов и сортируем
        if filter_tab is not None:
            
            #   Если в фильтре задано выражение для соритровки, то чистим список
            #   выражений для сортировки по умолчанию self._sortExprList
            if type(filter_tab) in (str, unicode) and 'order' in filter_tab.replace('ORDER', 'order').replace('Order', 'order'):
                self._sortExprList = []
                
            self.FilterFields(filter_tab)
        else:
            self.buffIndexes()
        
        #   Запоминаем текущий размер выборки
        self.oldSize = self.getRecordCount()
        self.Move(0)
        
        # ---- Создаем справочные словари
        self.spravBuff = {}
        
        return True
    
    def Close(self):
        """
        Закрытие источника данных.
        
        @rtype: C{bool}
        @return: Признак успешного закрытия.
        """
        self.dataclass = None
        self.dataclassInterface = None
    
    def getDBTableName(self):
        """
        Возвращает имя таблицы, используемой для хранения объектов данных в реляционной базе.
        """
        if self.GetIDataclass():
            return self.GetIDataclass().getDBTableName()
        
        return None
    
    def getDBColumnDict(self):
        """
        Возвращает словарь, содержащий описание колонок в SQLObject.
        """
        
        if self.GetIDataclass():
            return self._columnDict
        
        return None
        
    def FilterData(self, filt=None, bReplNames=True):
        """
        Фильтрация данных. B{Данная функция чистит буфер изменений}, поэтому анализ
        буфера изменений должен проводится (функцией C{isChangeRowBuff()}) перед вызовом этой функции.
        
        @type filt: C{string}
        @param filt: Строка запроса на фильтрацию. Пример: 'select id from table1 where id > 10 and id < 1000 order by ...'
        @type bReplNames: C{bool}
        @param bReplNames: Признак того, что предварительно необходимо провести
            замену имен из SQLObject представления в представление SQL базы.
        @rtype: C{bool}
        @return: Признак успешного завершения.
        """
        #   Чистим буфер изменений. Анализ буфера изменений должен проводится
        #   перед вызовом этой функции.
        self.clearChangeRowBuff(-1)
        
        #   Признак повторного использования фильтра
        isSelfFilter = False
        
        if filt == None:
            filt = self._filterQuery
            isSelfFilter = True
        
        #   Приводим ORDER BY к верхнему регистру
        filt = filt.replace('Order by', 'ORDER BY').replace('order by', 'ORDER BY').replace('Order By', 'ORDER BY')
        
        #   Дополняем запрос выражением сортировки
        if self._sortExprList not in [[], None] and filt not in ['None', None, ''] and \
           not (not isSelfFilter and 'ORDER' in filt):
            nf = filt.find('ORDER BY')
            
            #   Заменяем выражение сортировки на новое
            if nf >= 0:
                filt = filt[:nf]+'ORDER BY '+self.convSQL(str(self._sortExprList)[1:-1].replace('\'', ''))
            else:
                filt += ' ORDER BY '+self.convSQL(str(self._sortExprList)[1:-1].replace('\'', ''))
            
        #   Заменяем имена нашего класса данных на имена табличного представления
        if bReplNames:
            self._filterQuery = self.convSQL(filt)
        else:
            self._filterQuery = filt
        
        io_prnt.outLog(u'____ FILTER: <%s>' % filt)
        io_prnt.outLog(u'REAL FILTER: <%s>' % self._filterQuery)
        try:
            self.oldSize = self.getRecordCount()
        except:
            self.oldSize = -1
        
        return self.buffIndexes()
    
    def FilterField(self, fldName, val, bReplNames=True):
        """
        Функция отфильторвывает записи, у которых значение определенного поля <fldName> соответствуют выбранному занчению <id>.
        @type fldName: C{string}
        @param fldName: Имя поля, по которому фильтруются записи.
        @type val: C{int}
        @param val: Значение, по которому фильтруются объекты.
        @type bReplNames: C{bool}
        @param bReplNames: Признак того, что предварительно необходимо провести
            замену имен из SQLObject представления в представление SQL базы.
        @rtype:
        @return:
        """
        try:
            fld = self._columnDict[fldName]
        except KeyError:
            MsgBox(None, u'Поле %s в класс данных %s не определенно' % (fldName, self.name))
            return False
        
        if type(val) in (str, unicode):
            conv_val = ' + val + '
        else:
            conv_val = val

        filter = 'select id from %s where %s=%s' % (self.getDBTableName(), fld, str(conv_val))
        self.FilterData(filter, bReplNames=bReplNames)

        self.filter = {fldName: val}
        self._bStructedFilter = True

    def FilterFields(self, filter_tab=0, bReplNames=True):
        """
        Функция отфильторвывает записи, у которых значение определенного поля
        <fldName> соответствуют выбранному занчению <id>.
        
        @type filter_tab: C{string | dictionary}
        @param filter_tab: Фильтр объекта данных.
        @type bReplNames: C{bool}
        @param bReplNames: Признак того, что предварительно необходимо провести
            замену имен из SQLObject представления в представление SQL базы.
        @rtype: C{bool}
        @return: Признак успешной фильтрации
        """
        
        #   В случае если фильтр не указан пользуемся старым фильтром
        if isinstance(filter_tab, int):
            filetr_tab = self.filter
        try:
            #   Если фильтр не определен, то вызываем стандартный метод фильтрации
            if filter_tab in [None, '', 'None']:
                self.FilterData(filter_tab, bReplNames=bReplNames)
            
            #   Если фильтр определен в виде словаря
            if util.isExprDict(filter_tab):
                ret, val = util.ic_eval(filter_tab, 0, self.evalSpace,
                                        'ERROR in FilterFields() filter=<%s>' % str(filter_tab))
                if ret:
                    filter_tab = val
                else:
                    filetr_tab = ''
            
            self.filter = filter_tab
            
            #   Если фильтр является SQL выражением, то вызываем стандартный метод фильтрации
            if type(filter_tab) in (str, unicode):
                self.FilterData(filter_tab, bReplNames=bReplNames)
                
            #   Если фильтр является словарем, то создаем SQL выражение
            elif isinstance(filter_tab, dict):
                filterSQL = translate.dictFilterToSQL(filter_tab, self.getDBTableName(),
                                                      self.GetIDataclass().getIdName())
                self.FilterData(filterSQL, bReplNames=bReplNames)
                self._bStructedFilter = True
                return True

        except:
            io_prnt.outErr(u'Filter ERROR in filter:%s' % filter_tab)
        
        return False
        
    def isInStructFilter(self, dict):
        """
        Проверяет принадлежит ли запись к структурной фильтрованной выборке.
        """
        if self._bStructedFilter and len(self.filter.keys()) > 0:
            bret = True
            
            for key in self.filter.keys():
                if dict[key] != self.filter[key]:
                    bret = False
                    break
                
            return bret
        else:
            return False
        
    def getRecordCount(self):
        """
        Возвращает количество записей в источнике данных.

        @rtype: C{int}
        @return: Количество записей в источнике данных.
        """
        return len(self.indexBuff)

    def getFieldCount(self):
        """
        Возвращает количество полей. Вычисляется по словарю описания полей.

        @rtype: C{int}
        @return: Количество полей.
        """
        return len(self.scheme)
    
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
        
        if self.cursor + offset >= 0 and  self.cursor + offset < self.getRecordCount():
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
        
        if rec >= 0 and rec < self.getRecordCount():
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
    
    def Recno(self):
        """
        Возвращает положение курсора.

        @rtype: C{int}
        @return: Возвращает положение курсора.
        """
        return self.cursor
    
    def Lock(self, rec=-1):
        """
        Блокирует нужную запись для записи.
        
        @type rec: C{int}
        @param rec: Номер записи. По умолчанию B{rec=-1}. Если номер записи C{None}, то блокируется
            вся таблица. Если номер записи < 0, то блокируется текущая запись.
        @rtype: C{bool}
        @return: Возвращает код ошибки.
        """
        result = 99
        
        if rec < 0:
            rec = self.cursor
            
        try:
            id = self.indexBuff[rec][0]
            result = self.GetIDataclass().LockObject(id)
            if result:
                self._lockBuff.append(id)
        except IndexError:
            pass
        
        return result
    
    def Unlock(self, rec=-1):
        """
        Разблокирует нужную запись.
        
        @type rec: C{int}
        @param rec: Номер записи. По умолчанию B{rec=-1}.  Если номер записи C{None}, то разблокируется
            вся таблица. Если номер записи < 0, то разблокируется текущая запись.
        @rtype: C{bool}
        @return: Возвращает код ошибки.
        """
        result = 0
        
        if rec < 0:
            rec = self.cursor
        
        try:
            id = self.indexBuff[rec][0]
            
            if id in self._lockBuff:
                result = self.GetIDataclass().unLockObject(id)
                self._lockBuff.remove(id)
        except IndexError:
            pass
        
        return result

    def UnlockAll(self):
        """
        Разблокирует все записи, которые были заблокированы данным компонентом.
        """
        try:
            for id in self._lockBuff:
                self.GetIDataclass().unLockObject(id)
        except:
            io_prnt.outLastErr(u'SQLAlchemy Dataset. UnlockAll')
        
    def isLock(self, rec=-1):
        """
        Возпращает признак блокированной записи.
        
        @type rec: C{int}
        @param rec: Номер записи. По умолчанию B{rec=-1}.  Если номер записи C{None}, то возвращается признак блокировки
            всей таблицы. Если номер записи < 0, то возвращается признак блокировки текущей записи.
        @rtype: C{bool}
        @return: Возвращает признак блокировки.
        """
        ret = False
        
        if rec < 0:
            rec = self.cursor
            
        try:
            id = self.indexBuff[rec][0]
            ret = self.GetIDataclass().IsLockObject(id)
        except IndexError:
            io_prnt.outLastErr(u'SQLAlchemy Dataset. isLock')

        return ret

    def isTableChanged(self):
        """
        Функция определяет изменилось ли состояние таблицы.
        
        @rtype: C{bool}
        @return: Признак изменения состояния таблицы.
        """
        return False
    
    def getMaxId(self, recount=False):
        """
        Функция возвращает максимальное значение идентификатора записей.
        
        @type recount: C{bool}
        @param recount: Признак того, что значение надо пересчитать.
        @rtype: C{int}
        @return: Максимальное значение идентификатора записей. None в случае ошибки.
        """
        if recount:
            self.oldMaxId = -1
            buff = self.getIndexBuff()
            for x in buff:
                if x[0] > self.oldMaxId:
                    self.oldMaxId = x[0]
                    
        return self.oldMaxId
        
    def getObj(self, cursor=-1, bIgnore = True):
        """
        Возвращает объект по положению курсора.
        @type cursor: C{long}
        @param cursor: Значение порядкового номера в таблицы данных.
        @type bIgnore: C{bool}
        @param bIgnore: Признак игнорирования изменения таблицы. Если он False, то как только таблица кем-либо изменяется,
            буфер индексов тоже изменяется.
        @rtype: C{SQLObject}
        @return:
        """
        if cursor < 0:
            cursor = self.cursor

        if not bIgnore and self.isTableChanged():
            self.buffIndexes()
        try:
            id = self.indexBuff [cursor][0]
            
            #   Получаем доступ к объекту
            obj = self.GetIDataclass().get(id)
        except:
            obj = None
            
        return obj
    
    #   Доступ к текущему объекту класса данных
    rec = property(getObj)
    
    def getIndexBuff(self):
        """
        Возвращает буфер идентификаторов
        """
        return self.indexBuff
        
    def setIndexBuff(self, newbuff):
        """
        Устанавливает новый буфер идентификаторов.
        """
        self.indexBuff = newbuff
        self.oldSize = self.getRecordCount()
        
        #   Чистим структуру параметров последнего поиска
        self._lastSearchPar = [None, None]
        
        #   Пересчитываем максимальное значение идентификатора
        self.getMaxId(recount=True)
        self._bInvalidFilter = False
        
        #   Чистим буфер строки
        #   !!! По хорошему надо сначало его сохранить !!!
        self.rowBuff = None
        
    def getId(self, cursor=-1, bIgnore = True):
        """
        Возвращает идентификатор заданной строки.
        
        @type cursor: C{long}
        @param cursor: Положение курсора.
        @type bIgnore: C{bool}
        @param bIgnore: Признак игнорирования изменения таблицы. Если он False, то как только таблица кем-либо изменяется,
            буфер индексов тоже изменяется.
        @rtype: C{SQLObject}
        @return: Возвращает идентификатор заданной строки.
        """
        if cursor < 0:
            cursor = self.cursor
            
        if not bIgnore and self.isTableChanged():
            self.buffIndexes()
        try:
            id = self.indexBuff[cursor][0]
        except:
            id = None
            
        return id
    
    def isDeleted(self, cursor):
        """
        Функция определяет удалена ли соответствующая запись из источника данных или нет.
        
        @type cursor: C{long}
        @param cursor: Положение курсора.
        @rtype: C{bool}
        @return: Возвращает True - в случае если соответствующая запись удалена из источника данных, False в противном
            случае.
        """
        return cursor in self._del_indexBuff

    def isAdded(self):
        """
        Функция определяет появились ли в источнике данных новые записи.
        
        @rtype: C{bool}
        @return: Возвращает True - в случае если в буфере появились данные о добавленных записях, False в противном
            случае.
        """
        return len(self._add_indexBuff)
        
    def getDict(self, cursor, bIgnore = False):
        """
        Возвращает строку таблицы по положению курсора.
        
        @type cursor: C{long}
        @param cursor: Положение курсора.
        @type bIgnore: C{bool}
        @param bIgnore: Признак игнорирования изменения таблицы. Если он False, то как только таблица кем-либо изменяется,
            буфер индексов тоже изменяется.
        """
        if not bIgnore and self.isTableChanged():
            self.buffIndexes()
        
        #   Вычисляем время последнего обращения к буферу. Если оно > 0.5 сек, то буфер перегружается.
        #   Это позволяет отсеч события перерисовки грида от событий генерируемых человеком
        t = time.clock()
        dt = t - self._oldtime
        self._oldtime = t
        dict = None
        
        try:
            #   Определяем тип буфера
            buffType = self.getTypePageBuff()
            id = self.getId(cursor)
                        
            #   Если необходимо буферизировать всю таблицу то
            #   считаем, что курсор установлен на последнюю запись, а размер
            #   буферной таблицы равен размеру реальной таблицы
            if buffType == BUFF_TYPE_ALL:
                cur = self.getRecordCount()-1
                sz = cur+1
                
            #   Для постаничной буферезации используем текущий размер буфера
            elif buffType == BUFF_TYPE_PAGE:
                cur = cursor
                sz = self.sizePage
                
            #   Если установле другой тип буферезации, то устанавливаем размер=1
            else:
                cur = cursor
                sz = 1
                
            #   Перечитываем данные в буфер если нет нужной строки в буфере либо
            #   если время жизни буфера истекло. Если время жизни < 0, это озна-
            #   чает, что время жизни не ограничено.
            if (id not in self.bufferPageDict.keys() or
               (id in self.bufferPageDict.keys() and dt > self.time_page_life and self.time_page_life > 0)):
                self.createPageBuff(cur, sz)
                        
            #   Если в буфере нет записи с нужным идентификатором, это означает, что запись удалена.
            #   В этом случае отмечаем, что запись удалена в специальном буфере
            if id in self.bufferPageDict:
                dict = self.bufferPageDict[id]
            elif len(self.bufferPageDict.keys()) > 0:
                io_prnt.outLog(u'DEL row from indexBuff id=%s' % id)
                self._del_indexBuff[cursor] = id
        except KeyError:
            io_prnt.outErr(u'KEY ERROR in getDict row=%d, id=%d' % (cursor, id))
            dict = None
        except:
            io_prnt.outErr(u'ERROR in getDict row=%d, autocomit=' % cursor)
            dict = None
            
        return dict
    
    def Refresh(self):
        """
        Функция обновляет представление класса данных.
        """
        self.clearPageBuff()
        self.buffIndexes()
        
    def buffIndexes(self):
        """
        Буфферизирует идентификаторы, изпользуея выражение для фильтрации данных.
        """
        self.oldSize = self.getRecordCount()
        
        #   Чистим структуру параметров последнего поиска
        self._lastSearchPar = [None, None]
        
        try:
            if self._filterQuery in [None, '', 'None']:
                self._bStructedFilter = True
                
                #   Если поля сортировки не заданы
                if self._sortExprList in [[], None]:
                    self._filterQuery = 'SELECT %s FROM %s' % (self.GetIDataclass().getIdName(), self.getDBTableName())
                    
                #   Если поля сортировки заданы
                else:
                    #   Формируем список полей учавствующих в сортировке
                    ord = str(self._sortExprList)[1:-1].replace('\'','')
                    self._filterQuery = 'SELECT %s FROM %s ORDER BY %s' % (self.GetIDataclass().getIdName(),
                                                                           self.getDBTableName(), ord)

            # Приводим к списку, т.к. mssql драйвер возвращает картеж, а другие драйвера
            # список
            result = self.GetIDataclass().queryAll(self._filterQuery)
            if result:
                self.indexBuff = list(result)
            else:
                self.indexBuff = []
            if isinstance(self.indexBuff, tuple):
                self.indexBuff = list(self.indexBuff)
            self._bInvalidFilter = False
            
            if len(self.indexBuff) > 0:
                #   Пересчитываем максимальное значение идентификатора
                self.getMaxId(recount=True)
                #   Если установлен признак обратного порядка сортировки
                if self._isSortDESC:
                    self.indexBuff.reverse()
        except:
            io_prnt.outErr(u'Error in buffIndexes filter=%s' % self._filterQuery)
            self._bInvalidFilter = True
            self.indexBuff = []
            self.oldMaxId = - 1
            return False
        
        self.rowBuff = None
        return True

    def FindRowString(self, string, cursor=-1, fields=None, bILike=True):
        """
        Функция ищет подстроку в массиве данных. Это желательная функция для всех объектов данных, используется
        в для поиска в объекте навигации.
    
        @type string: C{string}
        @param string: Строка поиска
        @type cur: C{int}
        @param cur: Начальное положение курсора.
        @type fields: C{list}
        @param fields: Список полей по которым ведется поиск.
        @type bILike: C{bool}
        @param bILike: Признак поиска без учета регистра. Если False - то поиск ведется
            на точное соответствие.
        @rtype: C{tuple}
        @return: Возвращает номер строку и название поля, где найдена искомая строка.
        """
        if cursor < 0:
            cursor = self.cursor

        ret = (None, cursor)
            
        #   Если параметры поиска не изменились берем значение из буфера
        if self._lastSearchPar != (string, fields):
            self._lastSearchIds = self.FindStringFromId(string, fields, bILike=bILike)
            self._lastSearchPar = (string, fields)
        
        if self._lastSearchIds:
            
            #   Ищем номер строки после курсора
            for cur, x in enumerate(self.indexBuff[(cursor+1):]):
                if x[0] in self._lastSearchIds:
                    return fields, cur+cursor+1
        
            #   Ищем номер строки до курсора
            for cur, x in enumerate(self.indexBuff[:cursor]):
                if x[0] in self._lastSearchIds:
                    return fields, cur
        
        self._lastSearchPar = (string, fields)
        return ret
            
    def FindStringFromId(self, string, fields=None, id=0, bILike=True):
        """
        Ищет подстроку начиная с определенного значения идентификатора. Поиск ведется
        в нижнем регистре.
        
        @type string: C{string}
        @param string: Строка поиска.
        @type fields: C{list}
        @param fields: Список полей по которым ведется поиск.
        @type id: C{int}
        @param id: Идентификатор строки, с которой ведется поиск.
        @type bILike: C{bool}
        @param bILike: Признак поиска без учета регистра. Если False - то поиск ведется
            на точное соответствие.
        @rtype: C{dict}
        @return: Возвращает список идентификаторов строк.
        """
        ret_list = []
            
        if string in [None, ''] or len(self.indexBuff) == 0:
            return ret_list
            
        #   Подготавливаем шаблон
        string = str(string).strip()
            
        if fields is None:
            fields = self.getFieldList()
    
        #   Определяем выражение для фильтрации по шаблону
        like_expr = ''
        fld_lst = '%s,' % self.GetIDataclass().getIdName()
        for fld in fields:
            inf = self.getFieldInfo(fld)

            #   В выражение для фильтрации используем только не вычисляемые
            #   поля
            if inf['attr'] in [icdataset.icNormalFieldType, icdataset.icNormalReadOnlyFieldType]:

                if bILike:
                    fld_lst += ' LOWER(%s) as %s,' % (fld, fld)
                    like_expr += 'or %s LIKE LOWER(\'%s\')' %(fld, string)
                else:
                    fld_lst += ' %s,' % fld
                    like_expr += 'or %s LIKE \'%s\'' %(fld, string)
                        
        if not like_expr:
            return ret_list
        else:
            like_expr = 'and (%s)' % like_expr[2:]
 
        # Убираем последнюю запятую
        fld_lst = fld_lst[:-1]
        
        # -------------------------------------------------------------------
            
        t1 = time.clock()

        s = self._filterQuery.replace('FROM', 'from').replace('From', 'from')
        s = s.replace('ORDER', 'order').replace('Order', 'order')
            
        nf = s.find('order')
            
        if nf >= 0:
            s = s[:nf]
 
        #   Преобразуем результаты текущего фильтра к нижнему регистру
        s = 'select %s %s' % (fld_lst, s[s.find('from'):])
        s = 'select * from (%s) as ftbl where %s>%s %s order by %s' % (s, self.GetIDataclass().getIdName(),
                                                                       str(id), like_expr,
                                                                       self.GetIDataclass().getIdName())
            
        io_prnt.outLog(u'SEARCH SQL: <%s>' % s)
            
        result = self.GetIDataclass().queryAll(s.lower())
        if result is None:
            rs = []
        else:
            rs = list(result)
        
        indx_id = -1

        if rs and len(rs) > 0:
            #   Ищем номер поля, где лежит идентификатор
            for indx, field_name in enumerate(self.GetIDataclass().getFieldNames(True)):
                fldName = self._dbColumnDict[field_name]
                        
                if fldName == self.GetIDataclass().getIdName():
                    indx_id = indx
                    break
                
            for r in rs:
                ret_list.append(r[indx_id])
        
        return ret_list

    def pointType(self, fld):
        """
        Функция возвращает тип ссылочного поля.

        @type fld: C{dictionary}
        @param fld: Словарное описание поля из схемы данных.
        @rtype: C{bool}
        @return: Возвращает тип ссылкочного поля (None - поле ссылкой не является, 'D' - ссылка по значению,
        'R' - ссылка по идентификатору).
        """
        if not fld['dict'] in ['', None] and not fld['store'] in ['', None]:
            return fld['store']
        else:
            return None

    def getPropList(self, fieldName):
        """
        Возвращает список значений определенного поля.
        
        @type fieldName: C{string}
        @param fieldName: Имя поля.
        @rtype: C{list}
        @return: Возвращает список значений определенного поля либо если такого поля
            в таблице нет, возвращает None.
        """
        s = None
        
        try:

            prop = []
            
            s = self._filterQuery.replace('FROM', 'from').replace('From', 'from')
            s = ('select %s ' + s[s.find('from'):]) % (self._columnDict[fieldName])
                                    
            while 1:
                result = self.GetIDataclass().queryAll(s)
                if result is None:
                    rs = []
                else:
                    rs = list(result)
                            
                if not rs:
                    break
                
                prop.append(rs[0])
                                                    
            return prop
        
        except:
            io_prnt.outErr(u'Error in getPropList SQL:%s' % s)
            
    def setParentIdDict(self, prnts):
        """
        Функция устанавливает текущие идентификаторы родительских объектов, на
        которые будет ссылаться новый объект класса данных.
        
        @type prnts: C{dictionary}
        @param prnts: Словарь идентификаторов на родительские объекты. В качестве
            ключа класс в качестве значения уникальный идентификатор.
        """
        self._prnts_id = prnts
        
    def getParentId(self, className):
        """
        Функция возвращает идентификатор родительского объекта, на
        который будет ссылаться новый объект класса данных.
        
        @type className: C{string}
        @param className: Имя родительского класса данных.
        @rtype: C{int}
        @return: Возвращает идентификатор родительского объекта. Если не найден,
            то None.
        """
        try:
            return self._prnts_id[className]
        except:
            io_prnt.outLastErr(u'ICSQLOBJDATASET: Invalid key in getParentId(%s)' % className)

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
                    
            self.setSortPrzn()
            return self.FilterData()
            
        return False


def getDataset(className, subsys=None, logType=0, evalSpace=None):
    """
    Функция создает объект навигации для класса данных.
    
    @type className: C{string}
    @param className:  Имя класса данных.
    @type subsys: C{string}
    @param subsys: Имя подсистемы. Если подсистема не указана, то описание ищется
        стандартным образом: сначала в текущей, затем в импортированных подсистемах.
    @rtype: C{icSQLObjDataset}
    @return: Возвращает объект навигации.
    """
    dataset = None
    subsys_path = '<subsys>'
    
    if not evalSpace:
        evalSpace = icwidget.icResObjContext()

    try:
        subsys_path = resource.getSubsysPath(subsys)
        res = resource.icGetRes(className, 'tab', subsys_path)
        dataset = icSQLObjDataSet(-1, res, logType=logType, evalSpace=evalSpace)
        
        evalSpace['self'] = dataset
        dataset.eval_attr('init_expr')
    except:
        io_prnt.outErr(u'Ошибка при создании объекта данных \'%s\' подсистемы \'%s\'' % (className, subsys_path))
        
    return dataset


if __name__ == '__main__':

    dataset = getDataset('FACTURE_ACC', 'C:/pydb/resource.tab')
    print(str(dataset._dbColumnDict))
