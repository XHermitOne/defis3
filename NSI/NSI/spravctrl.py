#!/usr/bin/env python
#  -*- coding: utf-8 -*-

"""
Модуль функций управления справочниками.
"""

from ic.utils.coderror import *
from ic.log import log

from ic.components import icResourceParser

# Версия
__version__ = (0, 0, 1, 1)

# --- Константы ---
# Основной менеджер справочников
SPRAV_MANAGER = None

# Имя менеджера справочников по умолчаню
DEFAULT_SPRAV_MANAGER_NAME = 'nsi_sprav'


def createSpravManager(SpravManagerResName_=DEFAULT_SPRAV_MANAGER_NAME):
    """
    Создать менеджер справочников.
    @param SpravManagerResName_: Имя ресурса менеджера справочнков.
        По умолчанию берется nsi_sprav.mtd.
    """
    global SPRAV_MANAGER
    if SPRAV_MANAGER is None:
        SPRAV_MANAGER = icResourceParser.icCreateObject(SpravManagerResName_, 'mtd')
    if SPRAV_MANAGER is None:
        log.warning(u'Ошибка создания менеджера справочников <%s>' % SpravManagerResName_)
    return SPRAV_MANAGER


def destroySpravManager():
    """
    Удалить менеджер справочников.
    """
    global SPRAV_MANAGER
    SPRAV_MANAGER = None


def getSprav(SpravName_, SpravManager_=None):
    """
    Получить доступ к объекту справочника по имени.
    @param SpravName_: Имя справочника.
    @param SpravManager: Имя менеджера спровочников, если не определен, то nsi_sprav.
    """
    try:
        if not SpravManager_:
            SpravManager_ = DEFAULT_SPRAV_MANAGER_NAME
        sprav_manager = createSpravManager(SpravManager_)
        return sprav_manager.getSpravByName(SpravName_)
    except:
        log.fatal(u'Ошибка получения доступа к справочнику <%s>' % SpravName_)
        return None


def HlpSprav(typSprav, ParentCode=(None,),
             field=None, datatime=None, form=None, parentForm=None, SpravManager=None):
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
    @param parentForm: Родительская форма.
    @param SpravManager: Имя менеджера спровочников, если не определен, то nsi_sprav.
    """
    try:
        if not SpravManager:
            SpravManager = DEFAULT_SPRAV_MANAGER_NAME
        sprav_manager = createSpravManager(SpravManager)
        sprav_obj = getattr(sprav_manager, typSprav)
        # print('<<<!>>>', sprav_manager.container.getAll().keys())
        return sprav_obj.Hlp(ParentCode, field, form, parentForm, DateTime_=datatime)
    except:
        # print(sprav_obj)
        log.fatal(u'Ошибка выбора из справочника <%s>' % typSprav)
        return None


def CtrlSprav(typSprav, val, old=None, 
              field='name', flds=None, datatime=None, bCount=True, cod='', SpravManager=None):
    """
    Функция контроля наличия в справочнике значения поля с указанным значением.
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
    @param SpravManager: Имя менеджера спровочников, если не определен, то nsi_sprav.
    @rtype: C{int}
    @return: Код возврата функции контроля.
    """
    try:
        if not SpravManager:
            SpravManager = DEFAULT_SPRAV_MANAGER_NAME
        sprav_manager = createSpravManager(SpravManager)
        sprav_obj = getattr(sprav_manager, typSprav)
        return sprav_obj.Ctrl(val, old, field, flds, bCount, cod, DateTime_=datatime)
    except:
        log.fatal(u'Ошибка контроля наличия значения <%s> в справочнике <%s>' % (str(val), typSprav))
        return None


def FSprav(typSprav, cod, field='name', datatime=None, SpravManager=None):
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
    @param SpravManager: Имя менеджера спровочников, если не определен, то nsi_sprav.
    @rtype: C{dictionary}
    @return: Значение либо словарь значений (если поле field задает список полей).
        None, если строка с заданным кодом не найдена.
    """
    try:
        if not SpravManager:
            SpravManager = DEFAULT_SPRAV_MANAGER_NAME
        sprav_manager = createSpravManager(SpravManager)
        sprav_obj = getattr(sprav_manager, typSprav)
        return sprav_obj.Find(cod, field, DateTime_=datatime)
    except:
        log.fatal(u'Ошибка поиска по коду <%s> в справочнике <%s>' % (str(cod), typSprav))
        return None
