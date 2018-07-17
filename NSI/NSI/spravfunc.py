#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль функций работы со справочниками.
"""

# --- Подключение модулей ---
import wx
from sqlobject import *
from sqlobject.styles import mixedToUnder

from ic.log.iclog import MsgLastError, LogLastError
from ic.dlg.msgbox import *
from ic.db import tabclass
from ic.utils.coderror import *
import ic.utils.util as util
from ic.components.icResourceParser import *
import ic.components.icwidget as icwidget

from ic.dlg.ic_dlg import icAskDlg

__version__ = (0, 0, 0, 2)

# ---- Идентификаторы классов данных, используемых в НСИ
CLASS_NSI_LIST = 'NsiList'
CLASS_NSI_LEVEL = 'NsiLevel'
CLASS_NSI_NOTICE = 'NsiNotice'
CLASS_NSI_STD = 'NsiStd'
CLASS_NSI_STD_T = 'NsiStdT'

NSI_STD_EDIT_FORM = 'FrmStdSprav'
NSI_STD_EDIT_FORM_T = 'FrmStdSpravT'
NSI_STD_HLP_FORM = 'FrmHlpSprav'

# ---- Функции определяют имена классов данных используемых в справочной системе
def GetRecordCount(rs):
    """
    Возвращает количество выбранных записей в объекте SelectResults после использования
    функции select(...). Функция написана для того, чтобы отвязаться от версии SQLObject -
    в версии 0.5 для определяния количества записей используется len(rs), в версии >= 0.6
    rs.count()

    @type rs: C{SQLObject.SelectResults}
    @param rs: Набор отобранных записей.
    """
    #   ver 0.6
    try:
        return rs.count()
    #   ver 0.5
    except:
        return len(rs)


def GetRecordDict(Record_):
    """
    Преобразовать запись SQLObject в словарь.
        {'field1':value1,'field2':value2,...}.
    """
    return dict([(field, getattr(Record_, field)) for field in Record_._SO_columnDict.keys()])


def getNsiListClassName():
    """
    Возвращает имя класса, описывающего типы справочников.
    """
    return CLASS_NSI_LIST


def getNsiLevelClassName():
    """
    Возвращает имя класса, описывающего структуры кодов справочников.
    """
    return CLASS_NSI_LEVEL


def getNsiNoticeClassName():
    """
    Возвращает имя класса, описывающего дополнительные поля справочников.
    """
    return CLASS_NSI_NOTICE


def getNsiStdClassName():
    """
    Возвращает имя класса, описывающего структуру стандартного справочников.
    """
    return CLASS_NSI_STD


def getNsiStdTClassName(name=None):
    """
    Возвращает имя класса, описывающего структуру справочника изменяемых во
        времени параметров. Это имя генерируется по имени класса справочника.
        
    @type name: C{string}
    @param name: Имя класса данных, для хранения справочников.
    """
    if name:
        return name + 'T'
    else:
        return getNsiStdClassName() + 'T'


# -------------------------------------------------------------------------------
def GetTabResName():
    """
    Функция возвращает имя ресурсного файла с описанием классов данных.
    """
    return 'c:/pythonprj/workdata/db/resource.tab'

# ---- Основные функции НСИ


def FSprav(typSprav, cod, field='name', datatime=None):
    """
    Поиск по коду.
    
    @type typeSprav: C{...}
    @param typeSprav: Тип справочника.
    @type cod: C{...}
    @param cod: Код строки справочника.
    @type field: C{string | list }
    @param field: Имя поля или список полей.
    @type datatime: C{string}
    @param datatime: Время актуальности справочной информации.
    @rtype: C{dictionary}
    @return: Значение либо словарь значений (если поле field задает список полей).
        None, если строка с заданным кодом не найдена.
    """
    print('FSPRAV ENTER')
    if isinstance(field, str):
        flds = [field]
        isRetDict = False
    else:
        flds = [x for x in field]
        isRetDict = True
        
    fldDict = {}
    
    #   Формируем словарь соотношений для функции контроля
    for x in flds:
        fldDict[x] = x
    
    #   Используем функцию для контроля. Она возвращает словарь значений.
    ctrlCod, dict = CtrlSprav(typSprav, cod, None, 'cod', fldDict, datatime)
    
    if ctrlCod != IC_CTRL_OK:
        ret = None
    elif isRetDict:
        ret = dict
    else:
        ret = dict[field]
    
    return ret


def FSpravId(typSprav, id, field='name', datatime=None, tab=None):
    """
    Поиск значения справочника по идентификатору.
    
    @type typeSprav: C{...}
    @param typeSprav: Тип справочника.
    @type id: C{int}
    @param id: Идентификатор строки справочника.
    @type field: C{string | list }
    @param field: Имя поля или список полей.
    @type datatime: C{string}
    @param datatime: Время актуальности справочной информации.
    @rtype: C{... | dictionary}
    @return: Значение или словарь значений (ключи - имена полей). Если None, то
        необходимые значения не найдены.
    """
    print('FSPRAV_ID ENTER, id=', id)
    if isinstance(field, str):
        flds = [field]
        isRetDict = False
    else:
        flds = [x for x in field]
        isRetDict = True
        
    fldDict = {}
    
    #   Формируем словарь соотношений для функции контроля
    for x in flds:
        fldDict[x] = x
    
    #   Используем функцию для контроля. Она возвращает словарь значений.
    ctrlCod, dict = CtrlSpravId(typSprav, id, None, fldDict, datatime, tab=tab)
    
    if ctrlCod != IC_CTRL_OK:
        ret = None
    elif isRetDict:
        ret = dict
    else:
        ret = dict[field]
    print('DSpravId Result=', ret)
    return ret


def CtrlSprav(typSprav, val, old=None, field='name', flds=None, datatime=None, bCount=True, cod=''):
    """
    @type typSprav: C{string}
    @param typSprav: Тип справочника.
    @type cod: C{string}
    @param cod: Начальная подстрока структурного кода, ограничивающая множество возможных кодов.
    @type val: C{...}
    @param val: Проверяемое значение. Если тип картеж, то это означает, что проверяем структурное
        значение (например иерархический код справочника).
    @type old: C{...}
    @param old: Старое значение.
    @type field: C{string}
    @param filed: Поле, по которому проверяется значение.
    @type flds: C{dictionary}
    @param flds: Словарь соответствий между полями определенного класса данных и
        полями справочника. Если контроль значения пройдет успешно, то
        соответствующие значения из справочника будут перенесены в поля класса
        данных. Пример: {'summa':'f1', 'summa2':'f2'}
    @type datatime: C{string}
    @param datatime: Время актуальности кода.
    @type bCount: C{string}
    @param bCount: признак того, что необходимо вести количество ссылок.
    @rtype: C{int}
    @return: Код возврата функции контроля.
    """
    result = IC_CTRL_OK
    res_val = {}
    
    #   Создаем все необходимые классы данных.
    #   1. Типы справочников (getNsiListClassName())
    #   2. Класс хранения справочника (поле tab класса типов)
    #   3. Класс хранения изменяемых во времени параметров
    #       (поле tab класса типов + 'T').
    try:
        #   Определяем имя класса данных справочника
        #   Создаем класс данных типов справочников
        _NsiList = tabclass.CreateTabClass(getNsiListClassName())
        
        #   Находим описание нужного справочника
        rs = _NsiList.select(_NsiList.q.type==typSprav)
    
        if GetRecordCount(rs) == 0:
            print('Invalid sprav type')
            return IC_CTRL_FAILED_TYPE_SPRAV, res_val
        
        spr = rs[0]

        #   Создаем классы данных справочника и изменяемых во времени параметров
        
        _Sprav = tabclass.CreateTabClass(spr.tab)
        
        cnList = _NsiList._connection.getConnection()
        cnSprav = _Sprav._connection.getConnection()
        cnSpravT = None
        
        result = IC_CTRL_FAILED
        
        # -----------------------------------------------------------------------
        if isinstance(val, tuple):
            value = ''.join([str(x) for x in val])
        else:
            value = val
        
        # -----------------------------------------------------------------------
        #   Если указана дата актуальности
        if datatime:
            _SpravT = tabclass.CreateTabClass(spr.tab+'T')
            cnSpravT = _SpravT._connection.getConnection()
            
            rs = _SpravT.select(AND(_Sprav.q.id_nsi_listID == spr.id,
                                _SpravT.q.id_nsi_stdID == _Sprav.q.id,
                                _SpravT.q.time_start <= datatime,
                                _SpravT.q.time_end >= datatime,
                                getattr(_SpravT.q, field) == value,
                                _SpravT.q.cod.startswith(cod)))

        #-----------------------------------------------------------------------
        #   Если дата актуальности не указана либо в таблице актуальности нет инф.
        #   за нужный период, то проверяем по справочной таблице
        #if not datatime or len(rs) == 0:
        if not datatime or GetRecordCount(rs) == 0:
            rs = _Sprav.select(
                AND(_Sprav.q.id_nsi_listID==spr.id,
                    getattr(_Sprav.q, field)==value,
                    _Sprav.q.cod.startswith(cod)))
        
        try:
            row = rs[0]
            result = IC_CTRL_OK
            
            #   Формируем словарь значений, которые необходимо вернуть
            if type(flds) == type({}):
                for key in flds:
                    fld_sprav = flds[key]
                            
                    try:
                        res_val[key] = getattr(row, fld_sprav)
                    except:
                        print('Invalid attribute name "%s" in CtrlSprav class=%s' % (fld_sprav, spr.tab))
                
        except IndexError:
            result = IC_CTRL_FAILED
            
    except:
        print('__ except CtrlSprav:', typSprav, val, old, field, flds)
        LogLastError('CtrlSprav ERROR')
        result = IC_CTRL_FAILED_TYPE_SPRAV

    cnList.commit()
    cnSprav.commit()
    
    if cnSpravT:
        cnSpravT.commit()

    return (result, res_val)

def CtrlSpravId(typSprav, value, old=None, flds=None, datatime=None, bCount=True, tab=None):
    """
    @type typSprav: C{string}
    @param typSprav: Тип справочника.
    @type cod: C{string}
    @param cod: Код справочника.
    @type value: C{...}
    @param value: Проверяемое значение идентификатора.
    @type old: C{...}
    @param old: Старое значение.
    @type field: C{string}
    @param filed: Поле, по которому проверяется значение.
    @type flds: C{dictionary}
    @param flds: Словарь соответствий между полями определенного класса данных и
        полями справочника. Если контроль значения пройдет успешно, то
        соответствующие значения из справочника будут перенесены в поля класса
        данных. Пример: {'summa':'f1', 'summa2':'f2'}
    @type datatime: C{string}
    @param datatime: Время актуальности кода.
    @type bCount: C{string}
    @param bCount: признак того, что необходимо вести количество ссылок.
    @type tab: C{string}
    @param tab: Имя класса данных справочника, если оно не указано, то функция определит
        имя класса данных справочника по таблице типов справочников.
    @rtype: C{int}
    @return: Код возврата функции контроля.
    """

    result = IC_CTRL_OK
    res_val = {}
    
    #   Создаем все необходимые классы данных.
    #   1. Типы справочников (getNsiListClassName())
    #   2. Класс хранения справочника (поле tab класса типов)
    #   3. Класс хранения изменяемых во времени параметров
    #       (поле tab класса типов + 'T').
    print('CtrlSprav_id, id, flds, tab=',value, flds,tab)
    try:
        
        if not tab:
            #   Определяем имя класса данных справочника
            #   Создаем класс данных типов справочников
            _NsiList = tabclass.CreateTabClass(getNsiListClassName())
            
            #   Находим описание нужного справочника
            rs = _NsiList.select(_NsiList.q.type==typSprav)
            print(rs)
            #if len(rs) == 0:
            if GetRecordCount(rs) == 0:
                print('Invalid sprav type')
                return (IC_CTRL_FAILED_TYPE_SPRAV, res_val)
            
            tab = rs[0].tab
    
        result = IC_CTRL_FAILED
        
        #   Если указано время актуальности, ищем в таблице изм. во времени
        #   параметров
        if datatime:
            tab = tab+'T'
            
        _Sprav = tabclass.CreateTabClass(tab)
        row = _Sprav(value)
        
        try:
            result = IC_CTRL_OK
            
            #   Формируем словарь значений, которые необходимо вернуть
            if type(flds) == type({}):
                for key in flds:
                    fld_sprav = flds[key]
                            
                    try:
                        res_val[key] = getattr(row, fld_sprav)
                    except:
                        print('Invalid attribute name "%s" in CtrlSprav class=%s, id=%s' % (fld_sprav, tab, str(value)))
                
        except IndexError:
            result = IC_CTRL_FAILED
            
    except:
        LogLastError('CtrlSprav ERROR')
        result = IC_CTRL_FAILED_TYPE_SPRAV

    return (result, res_val)

def NsiEdtFormName(typSprav, level_num=1):
    """
    Определяет название формы редактирования справочника.
    
    @type typSprav: C{string}
    @param typSprav: Тип справочника.
    @type level_num: C{int}
    @param level_num: Номер уровня кода справочника.
    @rtype: C{string}
    @return: Возвращает имя формы для редактирования справочника. None - в случае
        если тип справочника не определен.
    """
    
    #   Создаем класс данных типов справочников
    _NsiList = tabclass.CreateTabClass(getNsiListClassName())
    _NsiLevel = tabclass.CreateTabClass(getNsiLevelClassName())
    cnList = _NsiList._connection.getConnection()
    cnLevel = _NsiLevel._connection.getConnection()
    
    result = NSI_STD_EDIT_FORM

    try:
        #   Находим описание нужного справочника
        rs = _NsiList.select(_NsiList.q.type==typSprav)

        #if len(rs) == 0:
        if GetRecordCount(rs) == 0:
            print('Invalid sprav type')
            return None
    
        obj = rs[0]
        
        #   Если не указано количество уровней кода, то считаем, что структура кода
        #   одноуровневая, код представляется тексовым полем и используются стандартные
        #   формы для редактирования и выбора.
        if int(obj.level_num) <= 0:
            return result
        
        rs_lev = _NsiLevel.select(_NsiLevel.q.id_nsi_listID==obj.id)
        
        for lev in rs_lev:
            if str(lev.level) == str(level_num):
                result = lev.edit_form_id
                print('find edit form name (NsiEdtFormName) :', result)
                break
    except:
        LogLastError('ERROR in NsiEdtFormName')

    cnList.commit()
    cnLevel.commit()
        
    return result

def NsiHlpFormName(typSprav, level_num=1):
    """
    Определяет название формы для выбора из справочника структур кодов (NsiLevel).
    
    @type typSprav: C{string}
    @param typSprav: Тип справочника.
    @type level_num: C{int}
    @param level_num: Номер уровня кода справочника.
    @rtype: C{string}
    @return: Возвращает имя формы выбора. None - в случае если тип справочника не определен.
    """
    
    #   Создаем класс данных типов справочников
    _NsiList = tabclass.CreateTabClass(getNsiListClassName())
    _NsiLevel = tabclass.CreateTabClass(getNsiLevelClassName())
    cnList = _NsiList._connection.getConnection()
    cnLevel = _NsiLevel._connection.getConnection()
    
    result = NSI_STD_HLP_FORM

    try:
        #   Находим описание нужного справочника
        rs = _NsiList.select(_NsiList.q.type==typSprav)

        #if len(rs) == 0:
        if GetRecordCount(rs) == 0:
            print('Invalid sprav type')
            return None
    
        obj = rs[0]
        
        #   Если не указано количество уровней кода, то считаем, что структура кода
        #   одноуровневая, код представляется тексовым полем и используются стандартные
        #   формы для редактирования и выбора.
        if int(obj.level_num) <= 0:
            return result
        
        rs_lev = _NsiLevel.select(_NsiLevel.q.id_nsi_listID==obj.id)
        
        for lev in rs_lev:
            if str(lev.level) == str(level_num):
                result = lev.hlp_form_id
                print('find help form name (NsiEdtFormName) :', result)
                break
    except:
        LogLastError('ERROR in NsiHlpFormName')

    cnList.commit()
    cnLevel.commit()
        
    return result

def HlpSprav(typSprav,ParentCode=(None,),field=None,datatime=None,form=None,rec=None,parentForm=None):
    """
    Запуск визуального интерфейса просмотра,  поиска и выбора значений поля
        или группы полей из отмеченной строки указанного справочника.
    @type typSprav: C{string}
    @param typSprav: Код типа (номер) справочника.
    @type ParentCode: C{...}
    @param ParentCode: Код более верхнего уровня.
    @param field: Задает поле или группу полей, которые надо вернуть.
    @type datatime: C{string}
    @param datatime: Время актуальности кода.
    @param form: имя формы визуального интерфейса работы со справочником.
    @param rec: Текущая запись справочника.
    @param parentForm: Родительская форма.
    """
    result = IC_HLP_OK
    res_val = None

    print('Start HlpSprav FIELD:',field)
    try:
        if ParentCode is None:
            ParentCode=(None, )

        #Для обработки необходимо преобразовать в список
        parent_code=list(ParentCode)
        #Запрашиваемый уровень
        try:
            x_level=parent_code.index(None)
            parent_code_str=''.join(parent_code[:x_level])
            x_level+=1
            print('HlpSprav Level:', x_level)
        except:
            x_level=None
            #Весь код заполнен
            res_val=(ParentCode,get_fields(field,rec))
            str_code=get_hlp_code_str(typSprav,ParentCode)
            print('HlpSprav Resultation: ',field,rec,res_val,str_code)
            return (result,res_val[0],res_val[1],str_code)

        #Получить информацию о справочнике
        _NsiList = tabclass.CreateTabClass(getNsiListClassName())

        #   Находим описание нужного справочника
        rs = _NsiList.select(_NsiList.q.type==typSprav)
    
        #if len(rs) == 0:
        if GetRecordCount(rs) == 0:
            print('Invalid sprav type')
            return (IC_HLP_FAILED_TYPE_SPRAV, res_val)
        
        spr = rs[0]

        #Если запрашиваемый уровень больше общего количества уровней, то выйти
        #Нет такого уровня в справочнике
        if spr.level_num<x_level:
            print('Invalid level %d'%(x_level))
            return (IC_HLP_FAILED_LEVEL, res_val)

        #определить длину кода уровня
        _NsiLevel=tabclass.CreateTabClass(getNsiLevelClassName())
        rs = _NsiLevel.select(_NsiLevel.q.type==typSprav)
        level_len=None
        for rec in rs:
            if rec.level==x_level:
                level_len=rec.level_len
                break

        if level_len is None:
            MsgBox(None,'Не определена длина кода уровня!')
            return (IC_HLP_FAILED_LEVEL, res_val)

        parent_len=len(parent_code_str)

        result = IC_HLP_FAILED

        #--- Если указана дата актуальности ---
        if datatime:
            sprav_t=spr.tab+'T'
            sql='''SELECT id FROM %s
                WHERE SUBSTR(cod,1,%d) LIKE(\'%s\') AND
                LENGTH(SUBSTR(cod,%d,LENGTH(cod)-%d))=%d AND
                time_start<=%s AND time_end>=%s'''%(sprav_t,
                parent_len,parent_code_str,
                parent_len+1,parent_len,level_len,
                str(datatime),str(datatime))
                    
        #---  Если дата актуальности не указана либо в таблице актуальности нет инф.
        #   за нужный период, то проверяем по справочной таблице
        if not datatime:
            sql='''SELECT id FROM %s
                WHERE %s.id_nsi_list=%d AND
                SUBSTR(%s.cod,1,%d) LIKE(\'%s\') AND
                LENGTH(SUBSTR(%s.cod,%d,LENGTH(%s.cod)-%d))=%d'''%(spr.tab,
                spr.tab,spr.id,spr.tab,parent_len,parent_code_str,
                spr.tab, parent_len+1,spr.tab,parent_len,level_len)

        sprav=spr.tab
        
        #Завершить транзакцию
        _NsiList._connection.getConnection().commit()
        _NsiLevel._connection.getConnection().commit()
        #Определить форму выбора кода
        if form is None:
            form=NsiHlpFormName(typSprav,x_level)
        #Вывести окно и возвратить выбранный код
        print('SQL Query: ', sql)
        #evsp=util.InitEvalSpace({'sprav_type':typSprav, 'sprav_code':parent_code,'sprav_field':field,'parent_form':parentForm})
        evsp = icwidget.icResObjContext()
        evsp.update({'sprav_type':typSprav, 'sprav_code':parent_code,'sprav_field':field,'parent_form':parentForm})
        res_val=ResultForm(form,filter={sprav:sql},evalSpace=evsp, parent=parentForm,bBuff=True)
        result = IC_HLP_OK
    except:
        LogLastError('HlpSprav ERROR')
        result = IC_HLP_FAILED_TYPE_SPRAV

    print('HlpSprav Result: ',result, ' HlpSprav Value: ', res_val)
    return res_val

#--- Функции буфферизации справочников ---
#Буфар справочников,
#необходимый для работы функций FSpravBuff и FSpravIdBuff
#Структура:
#   {
#   typeSprav:{
#             cod/id:{cod:___,name:___,s1:___,...}
#             }
#   }
_SpravBuffer={}
_SpravIdBuffer={}

def getSpravDict(typSprav,CurCode_=None,CurLevel_=1):
    """
    Получить справочник заданного типа в виде словаря в представлении дерева.
    @type typeSprav: C{...}
    @param typeSprav: Тип справочника.
    @type CurCode_: C{...}
    @param CurCode_: Код строки справочника.
        Для конвертации начиная с корня указывать не надо.
    @return: Возвращает словарь следующей структуры:
        {
        'COD1':{'COD1':{...},'cod':'COD1','name':'name1','s1':'',...},
        .
        .
        .
        'COD_N':{'COD_N':{...},'cod':'COD_N','name':'name_N','s1':'',...},
        }
    """
    #определить длину кода уровня
    _NsiStd=tabclass.CreateTabClass(getNsiStdClassName())
    cod_len=getLevelLen(typeSprav,CurLevel_)
    if CurCode_ is None:
        try:
            sprav_recs=_NsiStd.select('''type='%s' AND LENGTH(cod)=%d'''%(typSprav,cod_len))
        except:
            sprav_recs={}
    elif CurCode_:
        try:
            sprav_recs=_NsiStd.select('''type='%s' AND
                LENGTH(cod)=%d'''%(typSprav,cod_len))
        except:
            sprav_recs={}
        
    #Завершить транзакцию
    _NsiStd._connection.getConnection().commit()
    return dict([(rec.cod,dict(rec)) for rec in sprav_recs])
  
def getSpravDictSimple(typSprav):
    """
    Получить справочник заданного типа в виде словаря.
    @type typeSprav: C{...}
    @param typeSprav: Тип справочника.
    @return: Возвращает словарь следующей структуры:
        {
        'COD1':{'cod':'COD1','name':'name1','s1':'',...},
        .
        .
        .
        'COD_N':{'cod':'COD_N','name':'name_N','s1':'',...},
        }
    """
    try:
        #   Определяем имя класса данных справочника
        #   Создаем класс данных типов справочников
        _NsiList = tabclass.CreateTabClass(getNsiListClassName())
        
        #   Находим описание нужного справочника
        rs = _NsiList.select(_NsiList.q.type==typSprav)
    
        if GetRecordCount(rs) == 0:
            print('Invalid sprav type')
            return None
        
        spr = rs[0]

        #   Создаем классы данных справочника и изменяемых во времени параметров
        _Sprav = tabclass.CreateTabClass(spr.tab)
        cnList = _NsiList._connection.getConnection()
        cnSprav = _Sprav._connection.getConnection()

        rs = _Sprav.select(_Sprav.q.id_nsi_listID==spr.id)

        sprav_dict={}
        if GetRecordCount(rs):
            #sprav_dict=dict(map(lambda r: (r.cod,dict(r)),rs))
            for r in rs:
                sprav_dict[r.cod]=GetRecordDict(r)
        
        cnList.commit()
        cnSprav.commit()
    except:
        LogLastError('>>> Error in getSpravDictSimple')
        sprav_dict = None
    return sprav_dict

def getSpravRecDict(typSprav,cod):
    """
    Подучить словарь записи, соответствующий записи справочника.
    @type typeSprav: C{...}
    @param typeSprav: Тип справочника.
    @type cod: C{...}
    @param cod: Код строки справочника.
    """
    #определить длину кода уровня
    _NsiStd=tabclass.CreateTabClass(getNsiStdClassName())
    try:
        sprav_rec=_NsiStd.select(AND(_NsiStd.q.type==typSprav,
            _NsiStd.q.cod==cod))[0]
    except:
        sprav_rec=None
    #Завершить транзакцию
    _NsiStd._connection.getConnection().commit()
    print('>>>getSpravRecDict: ',typSprav,cod,sprav_rec)
    return dict(sprav_rec)

def getSpravIdRecDict(typSprav,id):
    """
    Подучить словарь записи, соответствующий записи справочника.
    @type typeSprav: C{...}
    @param typeSprav: Тип справочника.
    @type id: C{int}
    @param id: Идентификатор строки справочника.
    """
    #определить длину кода уровня
    _NsiStd=tabclass.CreateTabClass(getNsiStdClassName())
    try:
        sprav_rec=_NsiStd.select(AND(_NsiStd.q.type==typSprav,
            _NsiStd.q.id==id))[0]
    except:
        sprav_rec=None
    #Завершить транзакцию
    _NsiStd._connection.getConnection().commit()
    print('>>>getSpravIdRecDict: ',typSprav,id,sprav_rec)
    return dict(sprav_rec)
    
def FSpravBuff(typSprav,cod,field='name',datatime=None,tab=None):
    """
    Поиск по коду с возможным буферизированием.
    
    @type typeSprav: C{...}
    @param typeSprav: Тип справочника.
    @type cod: C{...}
    @param cod: Код строки справочника.
    @type field: C{string | list }
    @param field: Имя поля или список полей.
    @type datatime: C{string}
    @param datatime: Время актуальности справочной информации.
    @rtype: C{dictionary}
    @return: Значение либо словарь значений (если поле field задает список полей).
        None, если строка с заданным кодом не найдена.
    """
    #Проверка наличия в буффере такого справочника
    global _SpravBuffer
    if typSprav in _SpravBuffer and cod in _SpravBuffer[typSprav]:
        if type(field)==type([]):
            return dict([item for item in _SpravBuffer[typSprav][cod].items() if item[0] in fields])
        elif type(field)==type(''):
            return _SpravBuffer[typSprav][cod][field]
        else:
            return None
    
    #Придется всетаки прочитать из БД
    if typSprav not in _SpravBuffer:
        _SpravBuffer[typSprav]={}
    if not _SpravBuffer[typSprav].haks_key(cod):
        _SpravBuffer[typSprav][cod]={}

    sprav_rec=getSpravRecDict(typSprav,cod)
    _SpravBuffer[typSprav][cod]=sprav_rec
    
    if type(field)==type(''):
        return _SpravBuffer[typSprav][cod][field]
    elif type(field)==type([]):
        return dict([item for item in _SpravBuffer[typSprav][cod].items() if item[0] in fields])
    else:
        return None
    
def FSpravIdBuff(typSprav,id,field='name',datatime=None,tab=None):
    """
    Поиск по идентификатору с возможным буферизированием.
    
    @type typeSprav: C{...}
    @param typeSprav: Тип справочника.
    @type id: C{int}
    @param id: Идентификатор строки справочника.
    @type field: C{string | list }
    @param field: Имя поля или список полей.
    @type datatime: C{string}
    @param datatime: Время актуальности справочной информации.
    @rtype: C{dictionary}
    @return: Значение либо словарь значений (если поле field задает список полей).
        None, если строка с заданным кодом не найдена.
    """
    #Проверка наличия в буффере такого справочника
    global _SpravIdBuffer
    if typSprav in _SpravIdBuffer and id in _SpravIdBuffer[typSprav]:
        if type(field)==type([]):
            return dict([item for item in _SpravBuffer[typSprav][id].items() if item[0] in fields])
        elif type(field)==type(''):
            return _SpravBuffer[typSprav][id][field]
        else:
            return None
    
    #Придется всетаки прочитать из БД
    if typSprav not in _SpravBuffer:
        _SpravBuffer[typSprav]={}
    if not _SpravBuffer[typSprav].haks_key(id):
        _SpravBuffer[typSprav][id]={}

    sprav_rec=getSpravIdRecDict(typSprav,id)
    _SpravBuffer[typSprav][id]=sprav_rec
    
    if type(field)==type(''):
        return _SpravBuffer[typSprav][id][field]
    elif type(field)==type([]):
        return dict([item for item in _SpravBuffer[typSprav][id].items() if item[0] in fields])
    else:
        return None
        
#Буффер справочников, одного поля
#Структура:
#   {
#   typeSprav:{
#             cod : значение поля field для этого справочника,
#             }
#   }
_SpravBufferRepl={}

def FSpravBuffRepl(typSprav,cod,field='name'):
    """
    Поиск по коду значения по одному полю с возможным буферизированием.
    
    @type typeSprav: C{...}
    @param typeSprav: Тип справочника.
    @type cod: C{...}
    @param cod: Код строки справочника.
    @type field: C{string | list }
    @param field: Имя поля или список полей.
    @return: Значение. None, если строка с заданным кодом не найдена.
    """
    #Проверка наличия в буффере такого справочника
    global _SpravBufferRepl
    if typSprav in _SpravBufferRepl:
        if cod in _SpravBufferRepl[typSprav]:
            return _SpravBufferRepl[typSprav][cod]
        else:
            return None
    
    #Придется всетаки прочитать из БД
    if typSprav not in _SpravBufferRepl:
        _SpravBufferRepl[typSprav]=getReplDict(typSprav,'cod',field)
        if cod in _SpravBufferRepl[typSprav]:
            return _SpravBufferRepl[typSprav][cod]
        else:
            return None
  
def refreshSpravBuffRepl(typSprav,field='name'):
    """
    Обновить буффур справочника.
    @type typeSprav: C{...}
    @param typeSprav: Тип справочника.
    @type field: C{string | list }
    @param field: Имя поля или список полей.
    """
    global _SpravBufferRepl
    _SpravBufferRepl[typSprav]=getReplDict(typSprav,'cod',field)
    
#---- Вспомогательные функции
def get_fields(field=None,rec=None):
    """
    Заполнение полей для возврата функцией HlpSprav().
    @param field: Задает поле или группу полей, которые надо вернуть.
    @param rec: Объект записи из которой беруться значения.
    """
    res_val=None
    #   Формируем словарь значений, которые необходимо вернуть
    if type(field)==type({}):
        res_val={}
        for key in field.keys():
            fld_sprav = field[key]
            try:
                res_val[key] = getattr(rec, fld_sprav)
            except:
                print('Invalid attribute name "%s" in HlpSprav record=%s'%(fld_sprav,str(rec)))
    elif type(field)==type(''):
        res_val=getattr(rec,field)
    return res_val

def get_hlp_code_str(typSprav,Code):
    """
    Определить строковое представление кода.
    @type typSprav: C{string}
    @param typSprav: Код типа (номер) справочника.
    @type Code: C{...}
    @param Code: Код.
    """
    try:
        code=''
        full_code=Code

        #Получить информацию о справочнике
        _NsiList = tabclass.CreateTabClass(getNsiListClassName())
        _NsiLevel=tabclass.CreateTabClass(getNsiLevelClassName())
        #   Находим описание нужного справочника
        level_count = _NsiList.select(_NsiList.q.type==typSprav)[0].level_num
        levels = _NsiLevel.select(_NsiLevel.q.type==typSprav)
        #Достроить код до полного
        full_code=list(full_code)
        for i in range(level_count-len(full_code)):
            full_code.append(None)
        full_code=tuple(full_code)

        for i_sub_code in range(len(full_code)):
            sub_code=full_code[i_sub_code]
            if sub_code:
                code+=sub_code
            else:
                level_len=0
                for rec in levels:
                    if rec.level==i_sub_code:
                        level_len=rec.level_len
                        break
                code+=''.zfill(level_len).replace('0',' ')
                
        #Завершить транзакцию
        _NsiList._connection.getConnection().commit()
        _NsiLevel._connection.getConnection().commit()
        return code
    except:
        print('Error in get_hlp_code_str')
        #Завершить транзакцию
        _NsiList._connection.getConnection().commit()
        _NsiLevel._connection.getConnection().commit()
        return None

def get_hlp_code(typSprav,ParentCode=(None,), CurCodeStr=''):
    """
    Определить текущий код справочника.
    @type typSprav: C{string}
    @param typSprav: Код типа (номер) справочника.
    @type ParentCode: C{...}
    @param ParentCode: Код более верхнего уровня.
    @type CurCodeStr: C{string}
    @param CurCodeStr: Текущий строковый код справочника.
    """
    try:
        parent_code=list(ParentCode)
        #Запрашиваемый уровень
        try:
            x_level=parent_code.index(None)+1
        except:
            return ParentCode
        #Получить информацию о справочнике
        _NsiList = tabclass.CreateTabClass(getNsiListClassName())
        #   Находим описание нужного справочника
        rs = _NsiList.select(_NsiList.q.type==typSprav)
    
        #if len(rs) == 0:
        if GetRecordCount(rs) == 0:
            print('Invalid sprav type')
            #Завершить транзакцию
            _NsiList._connection.getConnection().commit()
            _NsiLevel._connection.getConnection().commit()
            return ParentCode
        
        spr = rs[0]

        #Если запрашиваемый уровень больше общего количества уровней, то выйти
        #Нет такого уровня в справочнике
        if spr.level_num<x_level:
            print('Invalid level %d'%(x_level))
            return ParentCode

        #определить длину кода уровня
        _NsiLevel=tabclass.CreateTabClass(getNsiLevelClassName())
        rs = _NsiLevel.select(_NsiLevel.q.type==typSprav)
        level_len=None
        for rec in rs:
            if rec.level==x_level:
                level_len=rec.level_len
                break

        #Завершить транзакцию
        _NsiList._connection.getConnection().commit()
        _NsiLevel._connection.getConnection().commit()

        if level_len is None:
            MsgBox(None,'Не определена длина кода уровня!')
            return ParentCode

        print('CurCodeStr: ',parent_code, x_level, CurCodeStr, level_len)
        parent_code[x_level-1]=CurCodeStr.strip()[-level_len:]
        return tuple(parent_code)
    except:
        print('Error in get_hlp_code')
        #Завершить транзакцию
        _NsiList._connection.getConnection().commit()
        _NsiLevel._connection.getConnection().commit()
        return ParentCode
#

def getLevelLen(typeSprav,Level=1):
    """
    Получить длину уровня.
    """
    #определить длину кода уровня
    _NsiLevel=tabclass.CreateTabClass(getNsiLevelClassName())
    try:
        rs = _NsiLevel.select(_NsiLevel.q.type==typeSprav)
        print('getLevelLen: ',rs)
        level_len=None
        for rec in rs:
            print('getLevelLen: ',rec)
            if rec.level==Level:
                level_len=rec.level_len
                break
    except:
        level_len=0
    #Завершить транзакцию
    _NsiLevel._connection.getConnection().commit()
    return level_len

def getFieldNotice(typSprav, field):
    """
    Функция возвращает описание поля, которое храниться в таблице NsiNotice.

    @type typSprav: C{string}
    @param typSprav: Код типа (номер) справочника.
    @type field: C{string}
    @param field: Имя поля для которого необходимо получить описание.
    """
    #
    _NsiLevel = tabclass.CreateTabClass(getNsiLevelClassName())
    _NsiNotice = tabclass.CreateTabClass(getNsiNoticeClassName())

    rs = _NsiNotice.select(AND(_NsiLevel.q.type==typSprav,
                                            _NsiLevel.q.level==1,
                                            _NsiLevel.q.id==_NsiNotice.q.id_nsi_levelID,
                                            _NsiNotice.q.fld_name==field))
    #if len(rs) > 0:
    if GetRecordCount(rs) > 0:
        descr = rs[0].descr
    else:
        descr = field
    
    #Завершить транзакцию
    _NsiNotice._connection.getConnection().commit()

    return descr

def MaxVal(cls, typSpr, field):
    """
    Возвращает максимальное значение поля.

    @type cls: C{SQLObject}
    @param cls: Класс данных.
    @type typSpr: C{string}
    @param typSpr: Тип справочника.
    @type field: C{string}
    @param field: Имя поля.
    @rtype: C{int | float}
    @return: Максимальное значение поля.
    """
    sql = "Select max(%s) from %s where type='%s'" % (field, cls._table, typSpr)
    print('SCRIPT MaxVal SQL=', sql)
    rs = cls._connection.queryOne(sql)
    print(rs)
    if rs:
        if rs[0] <> None:
            return rs[0]
    return 0

def getSpravId(typSprav):
    """
    Получить идентификатор справочника по его типу.
    @type typSprav: C{string}
    @param typSprav: Код типа (номер) справочника.
    """
    #определить длину кода уровня
    _NsiList=tabclass.CreateTabClass(getNsiListClassName())
    try:
        sprav_id=_NsiList.select(_NsiList.q.type==typSprav)[0].id
    except:
        sprav_id=None
    #Завершить транзакцию
    _NsiList._connection.getConnection().commit()
    print('>>>getSpravId: ',typSprav,sprav_id)
    return sprav_id

def getSpravCodeId(typSprav,codSprav):
    """
    Получить идентификатор записи справочника по его типу и коду.
    @type typSprav: C{string}
    @param typSprav: Код типа (номер) справочника.
    @type codSprav: C{string}
    @param codSprav: Код записи.
    """
    #определить длину кода уровня
    _NsiStd=tabclass.CreateTabClass(getNsiStdClassName())
    try:
        sprav_id=_NsiStd.select(AND(_NsiStd.q.type==typSprav,
            _NsiStd.q.cod==codSprav))[0].id
    except:
        sprav_id=None
    #Завершить транзакцию
    _NsiStd._connection.getConnection().commit()
    print('>>>getSpravCodeId: ',typSprav,codSprav,sprav_id)
    return sprav_id
    
def DelSprav(typSprav,Code):
    """
    Удалить справочник.
    @param typSprav: Тип удаляемого справочника.
    @param Code: Структурный код удаляемого справочника.
    """
    if type(Code)==type(''):
        str_code=Code
    else:
        str_code=''.join(Code)
    len_code=len(str_code)
    del_sql='''type=\'%s\' AND
        SUBSTR(cod,1,%d) LIKE(\'%s%%\')'''%(str(typSprav),len_code,str_code)
    if icAskDlg('Удаление','Удалить справочник %s код %s?'%(typSprav,str_code))==wx.YES:
        #определить длину кода уровня
        _NsiStd=tabclass.CreateTabClass(getNsiStdClassName())
        del_res=_NsiStd.del_filter(del_sql)
        print('DelSprav: ',del_sql,del_res)
        if del_res: #==IC_DEL_OK:
            return IC_DEL_USER
        else:
            return del_res
    return IC_DEL_FAILED_IGNORE

def isLevel(typSprav,Level):
    """
    Функция определяет может ли являтся запрашиваемый уровень уровнем
        данного справочника.
    @param typSprav: Тип справочника.
    @param Level: Уровень.
    """
    _NsiList=tabclass.CreateTabClass(getNsiListClassName())
    try:
        sprav_level=_NsiList.select(_NsiList.q.type==typSprav)[0].level_num
    except:
        sprav_level=None
    #Завершить транзакцию
    _NsiList._connection.getConnection().commit()
    print('>>>isLevel: ',typSprav,Level,sprav_level)
    return (sprav_level>Level)

def getReplDict(typSprav, fieldKey, fieldVal, exprSelect=None):
    """
    Функция формируем словарь соответствий по справочнику.

    @type typSpr: C{string}
    @param typSpr: Тип справочника.
    @type fieldKey: C{string}
    @param fieldKey: Поле, которое будет выступать в качестве ключа.
    @type fieldVal: C{string}
    @param filedVal: Поле, которое будет выступать в качестве значения.
    @type exprSelect: C{<function>}
    @param exprSelect: Выражения фильтации.
    @rtype: C{dictionary}
    @return: Cловарь соответствий между полями справочника.
    """
    dict = {}

    try:
        #   Определяем имя класса данных справочника
        #   Создаем класс данных типов справочников
        _NsiList = tabclass.CreateTabClass(getNsiListClassName())
        
        #   Находим описание нужного справочника
        rs = _NsiList.select(_NsiList.q.type==typSprav)
    
        #if len(rs) == 0:
        if GetRecordCount(rs) == 0:
            print('Invalid sprav type')
            return None
        
        spr = rs[0]

        #   Создаем классы данных справочника и изменяемых во времени параметров
        _Sprav = tabclass.CreateTabClass(spr.tab)
        cnList = _NsiList._connection.getConnection()
        cnSprav = _Sprav._connection.getConnection()

        if exprSelect:
            rs = _Sprav.select(exprSelect)
        else:
            rs = _Sprav.select(_Sprav.q.id_nsi_listID==spr.id)

        for r in rs:
            key = getattr(r, fieldKey)
            value = getattr(r, fieldVal)
            dict[key] = value
        
        cnList.commit()
        cnSprav.commit()
    except:
        LogLastError('>>> Error in getReplDict')
        dict = None
    

    return dict

def newSprav(Type_,Cod_,Name_,**KWSprav_):
    """
    Создать новую запись в справочнике.
    """
    try:
        #   Создаем класс данных типов справочников
        _NsiStd=tabclass.CreateTabClass(getNsiStdClassName())
        nsi_listID=getSpravId(Type_)
        
        rec=_NsiStd(type=Type_,id_nsi_list=nsi_listID,
            cod=Cod_,name=Name_,count=0,
            access='',**KWSprav_)
        
        return rec
    except:
        LogLastError('>>> Error in newSprav')
        return None

def getLevelCodLen(typeSprav,Level=1):
    """
    Получить длину кода уровня.
    """
    #определить длину кода уровня
    _NsiLevel=tabclass.CreateTabClass(getNsiLevelClassName())
    try:
        rs=_NsiLevel.select(_NsiLevel.q.type==typeSprav)
        print('getLevelCodLen: ',rs)
        level_len=0
        for rec in rs:
            print('getLevelCodLen: ',rec)
            if rec.level<=Level:
                level_len+=rec.level_len
    except:
        level_len=0
    #Завершить транзакцию
    _NsiLevel._connection.getConnection().commit()
    return level_len

def getSpravLevel(Type_,Level_=1):
    """
    Получить записи справочника определенного уровня.
    @param Type_: Тип справочника.
    @param Level_: Запрашиваемый уровень.
    """
    try:
        #Получить информацию о справочнике
        _NsiList = tabclass.CreateTabClass(getNsiListClassName())
        #   Находим описание нужного справочника
        rs=_NsiList.select(_NsiList.q.type==Type_)

        if GetRecordCount(rs)==0:
            print('Invalid sprav type')
            return None
        
        #Запись данных о справочнике
        spr=rs[0]
        
        cod_level_len=getLevelCodLen(Type_,Level_)
        
        nsi_std_name=spr.tab
        nsi_listID=spr.id
        #sql='''SELECT * FROM %s
        #    WHERE %s.id_nsi_list=%d AND
        #    LENGTH(%s.cod)=%d'''%(spr.tab,
        #    spr.tab,spr.id,spr.tab,cod_level_len)
        #Завершить транзакцию
        _NsiList._connection.getConnection().commit()

        _NsiStd=tabclass.CreateTabClass(nsi_std_name)
        nsi_std_name_db=mixedToUnder(nsi_std_name)
        rs=_NsiStd.select('''%s.id_nsi_list_id=%d AND LENGTH(%s.cod)=%d'''%(nsi_std_name_db,
            nsi_listID,nsi_std_name_db,cod_level_len))
        #_NsiStd._connection.getConnection().commit()
        #print 'getSpravLevel',rs.count()
        return rs
    except:
        LogLastError('>>> Error in getSpravLevel')
        return None
    
    
if __name__ == '__main__':
    pass

