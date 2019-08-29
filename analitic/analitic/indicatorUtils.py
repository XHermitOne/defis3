#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Модуль прикладной системы.
"""

import os
import os.path

# import ic.db.tabclass as tabclass
# import NSI.spravfunc as spravfunc
from ic.utils import util
# from sqlobject import *
# import analitic.plans as plans
from ic.dlg import progress
from ic.utils import resource
from ic.storage import objstore
from ic.utils import filefunc
from ic.log import log

from plan import plans
from analitic.interfaces import IAnaliticTable

# Версия
__version__ = (0, 1, 1, 1)

#   Указатель на хранилище свойств индикаторов
indStorage = None
FileIndProperty = 'IndProperty'


# --- Функции индикаторов
def GetIndicatorLst(dict_obj):
    """
    Возвращает список индикаторов.

    @type dict_obj: C{dictionary}
    @param dict_obj: Словарь объектов формы.
    """
    lst = []
    
    for name, obj in dict_obj.items():
        try:
            if obj.resource['type'] == 'ArrowIndicator':
                lst.append(obj)
        except:
            # print('Invalid type component name, obj=', name, obj)
            log.fatal(u'Ошибка')
    
    return lst
    
    
def GetCodDict():
    """
    """
    dct = {'dayRealiz': 'IRSD',
           'monthRealiz': 'IRSM',
           'qwartRealiz': 'IRSQ',
           'yearRealiz': 'IRSY',
           'dayRealizMass': 'IRVD',
           'monthRealizMass': 'IRVM',
           'qwartRealizMass': 'IRVQ',
           'yearRealizMass': 'IRVY',
            
           'dayZajav': 'IZSD',
           'monthZajav': 'IZSM',
           'qwartZajav': 'IZSQ',
           'yearZajav': 'IZSY',
           'dayZajavMass': 'IZVD',
           'monthZajavMass': 'IZVM',
           'qwartZajavMass': 'IZVQ',
           'yearZajavMass': 'IZVY',
            
           'dayPay': 'IPSD',
           'monthPay': 'IPSM',
           'qwartPay': 'IPSQ',
           'yearPay': 'IPSY',
           'dayPayMass': 'IPVD',
           'monthPayMass': 'IPVM',
           'qwartPayMass': 'IPVQ',
           'yearPayMass': 'IPVY'}
            
    return dct
    
    
def CloseIndPropStorage():
    """
    Закрывает хранилище свойств.
    """
    if indStorage:
        indStorage.Close()
    
        
def GetIndPropStorage():
    """
    Возвращет указатль на хранилище свойств индикаторов.
    """
    global indStorage
    
    if not indStorage:
        root = os.path.join(os.path.dirname(resource.icGetResPath()), 'AppStorage')
        indStorage = objstore.icObjectStorage(root)
        indStorage.Open()

        #   Создаем узел - файл с настройками индикаторов
        if FileIndProperty not in indStorage:
            indStorage[FileIndProperty] = objstore.icFileStorage()
            # print('>>>> Create FileStorage <%s> root:%s' % (FileIndProperty, root))
            
    return indStorage


def LoadIndicatorProperty(indicator, cod, typeSprav = 'Indicators'):
    """
    Востанавливает настройки индикатора из справочника индикаторов.
    
    @type indicator: C{icArrowIndicator}
    @param indicator: Указатель на индикатор.
    @type cod: C{string}
    @param cod: Код индикатора, под которым он зарегестрирован в справочнике
        индикаторов.
    """
    # return
    LoadIndicatorPropertyStorage(indicator, cod)
    # return
    
    _NsiStd = tabclass.CreateTabClass(spravfunc.getNsiStdClassName())

    #   Находим описание нужного справочника
    rs = _NsiStd.select(AND(_NsiStd.q.type == typeSprav,
                            _NsiStd.q.cod == cod))

    lrs = spravfunc.getRecordCount(rs)
    
    if lrs > 0:
        obj = rs[0]
    else:
        # print('### Запись с кодом %s не найдена' % cod)
        return None
    
    #   Заполняем минимальное значение
    min = obj.n1
    #   Заполняем максимальное значение
    max = obj.n2
    majorStep = obj.n3
    minorStep = obj.n4
    
    if majorStep:
        indicator.majorValues = range(min, max+1)[0::majorStep]
        
    if minorStep:
        indicator.minorValues = range(min, max+1)[0::minorStep]

    #   Цветовые зоны
    ret, val = util.ic_eval(obj.s1, 0, indicator.evalSpace)
    if ret:
        indicator.colorRegions = val
        
    ret, val = util.ic_eval(obj.s2, 0, indicator.evalSpace)
    if ret and val:
        indicator.ei = val[0]
        indicator.SetLabel(val[1])
    
    indicator.source = obj.s3
    
    ret, val = util.ic_eval(obj.s4, 0, indicator.evalSpace)
    if ret:
        indicator.attrVal = val[0]
        indicator.attrPlan = val[1]
        
        if val[2]:
            indicator.attrTime = val[2]

    ret, val = util.ic_eval(obj.s5, 0, indicator.evalSpace)
    if ret:
        indicator.aggregationType, indicator.aggregationFunc = val
        
    factor = obj.n5
    if factor > 0:
        indicator.factor = factor
    indicator.Refresh()


def LoadIndicatorPropertyStorage(indicator, cod, typeSprav = 'Indicators'):
    """
    Востанавливает настройки индикатора из справочника индикаторов.
    
    @type indicator: C{icArrowIndicator}
    @param indicator: Указатель на индикатор.
    @type cod: C{string}
    @param cod: Код индикатора, под которым он зарегестрирован в справочнике
        индикаторов.
    """
    #   Читаем настройки
    storage = GetIndPropStorage()
    keyName = indicator.name+'_'+indicator.cod+indicator.typPar
    # print('......... KeyName=', keyName)
    stRes=None
    
    if storage and keyName in storage[FileIndProperty]:
        stRes = storage[FileIndProperty][keyName]
        storage.Close()
        
    if stRes:
        #   Заполняем минимальное значение
        # min_value, max_value = stRes['majorValues']
    
        #   Заполняем максимальное значение
        majorStep = stRes['majorStep']
        minorStep = stRes['minorStep']
        
        indicator.majorValues = stRes['majorValues']
        indicator.minorValues = stRes['minorValues']
        min = indicator.majorValues[0]
        max = indicator.majorValues[-1]
    
        #   Цветовые зоны
        indicator.colorRegions = stRes['colorRegions']
            
        indicator.ei = stRes['ei']
        indicator.SetLabel(stRes['label'])
        
        # indicator.source = stRes['source']
        indicator.attrVal = stRes['attrVal']
        indicator.attrPlan = stRes['attrPlan']
        indicator.attrTime = stRes['attrTime']
        indicator.aggregationType = stRes['aggregationType']
        indicator.aggregationFunc = stRes['aggregationFunc']
            
        factor = stRes['factor']
        if factor > 0:
            indicator.factor = factor
            
        indicator.Refresh()
        return True
    else:
        log.warning(u'Не найдено свойство индикатора <%s>' % keyName)
    
    return False


def LoadCAMonitorProperty(monitor, cod):
    """
    Загружает настройки монитора сравнительного анализа из справочнике мониторов.
    
    @type monitor: C{wx.Window}
    @param monitor: Указатель на монитор.
    @type cod: C{string}
    @param cod: Код монитора, под которым он зарегестрирован в справочнике
        мониторов.
    """
    pass


def LoadMonitorProperties(dict_obj):
    """
    Загружает настройки индикаторов монитора.
    
    @type dict_obj: C{dictionary}
    @param dict_obj: Словарь объектов формы.
    """
    # return
    lst = GetIndicatorLst(dict_obj)
    codDict = GetCodDict()
    
    for name, obj in dict_obj.items():
        if name in codDict:
            cod = codDict[name]
            
            #   Загружаем настройки индикатора
            LoadIndicatorProperty(obj, cod)
            
            #   Устанавливаем фунцию определяющую дневной план наблюдаемого
            #   параметра
            if not obj.cod in (None, '', 'None'):
                if 'Mass' in name:
                    obj.SetDayPlanFunc(plans.countKolDayPlan)
                else:
                    # print('--->>> Load <plans.countSumDayPlan> function in indicator=', name, cod)
                    obj.SetDayPlanFunc(plans.countSumDayPlan)
            # obj.Refresh()


def RefreshFormRealizMonitor(dict_obj):
    """
    Обновляет представление монитора <formRealiz>.
    
    @type dict_obj: C{dictionary}
    @param dict_obj: Словарь объектов формы.
    """
    # return

    #   Чистим буфера весов
    plans.ClearWBuff()
    plans.ClearPlanBuff()
    
    t = dict_obj['currentDate'].GetValue()
    yy = str(t.GetYear())
    mm = ('00' + str(t.GetMonth()+1))[-2:]
    dd = ('00' + str(t.GetDay()))[-2:]
    t = '%s.%s.%s' % (yy, mm, dd)

    lst = GetIndicatorLst(dict_obj)
    progress.icOpenProgressBar("Обновляем состояния индикаторов", 0, len(lst))
    
    for obj in lst:
        obj.SetPeriodIzm([None, t])
        progress.icUpdateProgressBar("Обновляем индикатор: %s" % obj.name)
        try:
            obj.RefreshState()
        except:
            log.fatal(u'Не удалось обновить индикатор <%s>' % obj.name)
    
    progress.icCloseProgressBar()


def RefreshIndicatorValue(indicator):
    """
    Обновляет значение индикатора.

    @type indicator: C{icArrowIndicator}
    @param indicator: Указатель на индикатор.
    """
    pass


def SaveCAMonitorProperty(monitor, cod):
    """
    Сохраняет настройки монитора сравнительного анализа в справочнике мониторов.
    
    @type monitor: C{wx.Window}
    @param monitor: Указатель на монитор.
    @type cod: C{string}
    @param cod: Код монитора, под которым он зарегестрирован в справочнике
        мониторов.
    """
    pass


def SaveIndicatorProperty(indicator, cod, typeSprav='Indicators'):
    """
    Сохраняет настройки индикатора в справочнике индикаторов.
    
    @type indicator: C{icArrowIndicator}
    @param indicator: Указатель на индикатор.
    @type cod: C{string}
    @param cod: Код индикатора, под которым он зарегестрирован в справочнике
        индикаторов.
    @type typeSprav: C{string}
    @param typeSprav: Тип справочника, где хранятся настройки.
    """
    # return
    
    SaveIndicatorPropertyStorage(indicator, cod)

    _NsiStd = tabclass.CreateTabClass(spravfunc.getNsiStdClassName())
    # print('>>> _NsiStd=', _NsiStd)
    #   Находим описание нужного справочника
    rs = _NsiStd.select(AND(_NsiStd.q.type == typeSprav,
                            _NsiStd.q.cod == cod))

    lrs = spravfunc.getRecordCount(rs)
    
    if lrs > 0:
      obj = rs[0]
    
    if indicator.majorValues:
        #   Заполняем минимальное значение
        obj.n1 = min = indicator.majorValues[0]
        #   Заполняем максимальное значение
        obj.n2 = max = indicator.majorValues[-1]
     
        #   Шаг мажорной и минорной сетки
        obj.n3 = (max - min)/(len(indicator.majorValues)-1)
        
        #   Сохраняем множетель
        obj.n5 = indicator.factor
                
        if indicator.minorValues:
            obj.n4 = (max - min)/(len(indicator.minorValues)-1)
        else:
            obj.n4 = obj.n3
        
        #   Цветовые зоны
        obj.s1 = str(indicator.colorRegions)
        #   Единицы измерений и заголовок индикатора
        obj.s2 = '("%s", "%s")' % (indicator.ei, indicator.GetLabel())
        #   Источник данных
        obj.s3 = indicator.source
        #   Имена полей (значение, план, время)
        obj.s4 = str((indicator.attrVal, indicator.attrPlan, indicator.attrTime))
        #   Тип и функция агрегации
        obj.s5 = str((indicator.aggregationType, indicator.aggregationFunc))
        
        # Экперимент
        # SaveIndicatorPropertyStorage(indicator, cod)


def SaveIndicatorPropertyStorage(indicator, cod, typeSprav = 'Indicators'):
    """
    Сохраняет настройки индикатора в хранилище.
    
    @type indicator: C{icArrowIndicator}
    @param indicator: Указатель на индикатор.
    @type cod: C{string}
    @param cod: Код индикатора, под которым он зарегестрирован в справочнике
        индикаторов.
    @type typeSprav: C{string}
    @param typeSprav: Тип справочника, где хранятся настройки.
    """
    stRes = {}
    
    if indicator.majorValues:
        #   Заполняем минимальное значение
        min = indicator.majorValues[0]
        max = indicator.majorValues[-1]
        stRes['majorValues'] = indicator.majorValues
        stRes['minorValues'] = indicator.minorValues
     
        #   Шаг мажорной и минорной сетки
        stRes['majorStep'] = (max - min)/(len(indicator.majorValues)-1)
        
        #   Сохраняем множетель
        stRes['factor'] = indicator.factor
                
        if indicator.minorValues:
            stRes['minorStep'] = (max - min)/(len(indicator.minorValues)-1)
        else:
            stRes['minorStep'] = stRes['majorStep']
        
        #   Цветовые зоны
        stRes['colorRegions'] = indicator.colorRegions
        #   Единицы измерений и заголовок индикатора
        stRes['ei'] = indicator.ei
        stRes['label'] = indicator.GetLabel()
        
        #   Источник данных
        stRes['source'] = indicator.source
        #   Имена полей (значение, план, время)
        stRes['attrVal'] = indicator.attrVal
        stRes['attrPlan'] = indicator.attrPlan
        stRes['attrTime'] = indicator.attrTime
        
        #   Тип и функция агрегации
        stRes['aggregationType'] = indicator.aggregationType
        stRes['aggregationFunc'] = indicator.aggregationFunc
    
        #   Сохраняем в хранилище настройки
        storage = GetIndPropStorage()
        
        if storage:
            keyName = indicator.name+'_'+indicator.cod+indicator.typPar
            # print('KEY:', keyName)
            storage[FileIndProperty][keyName] = stRes
            storage.Close()


def AnaliticProduct(ianlt):
    """
    Аналитика в разрезе продукции.
    Функции для вызова более подробной информации в дереве аналитики
    по кнопке <Подробнее>.
    
    @type ianlt: C{analitic.IAnaliticTree.IAnaliticTree}
    @param ianlt: Указатель на интерфейст дерева аналитики.
    """
    t1, t2 = ianlt.period
    tree = ianlt.GetNameObj('AnaliticTreeList')
    
    className = tree.idataclass.getClassName()
    tableName = tree.idataclass.getDBTableName()
    
    item = tree.GetSelection()
    row = tree.GetPyData(item)
    cod = row[0]
    # print('---->', row, tree.idataclass)
    # print('----> t1, t2:', t1, t2)

    flt = "select record_id from %s where dtoper<='%s' and dtoper>='%s' and reg='%s' and mens='%s' and codt LIKE '%s" % (tableName, t1, t2, cod[1], '0'+cod[2], cod[3])

    flt += "%'"
    # print('----> tableName:', tableName)
    # print('----> SQL FILTER:', flt)
    buff = tree.GetSpravBuff()
    
    #   Устанавливаем буфер справочника
    if 'Product' in buff:
        IAnaliticTable.SetProductSpravBuff(buff['Product'])
    
    idlg = IAnaliticTable.IAnaliticTable(ianlt.GetNameObj('MsgCtrl'),
                                         tableName=className,
                                         filter=flt)
    dlg = idlg.getObject()
    reg = tree.GetValFromSpravBuff('Region', cod[1]).strip()
    mens = tree.GetValFromSpravBuff('Menager', cod[2]).strip()
    grp = tree.GetValFromSpravBuff('Product', cod[3]).strip()
    dlg.setTitle('%s %s %s %s' % (cod[0], reg, mens, grp))
