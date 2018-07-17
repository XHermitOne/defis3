#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль содержит функции, которые разбирают ресурсное описание и
создают визуальные компоненты.

ВНИМАНИЕ! Исправление этого модуля может привести
к не работаспособности всей программы.
После исправления обязательно проверить работу всех прикладных проектов.

Если при сборке ресурса не находиться какой-либо компонент
(например Panel), то можно попробовать удалить все *.pyc файлы в пакете ic.
Удаление всех *.pyc файлов в Linux:
find ./ic/ -type f -name "*.pyc" -delete
"""

import wx
import time
import ic.components as components_lib
from ic.components.icwidget import icNewId
import ic.components.icwidget as icwidget
# from ic.log.iclog import MsgLastError
from ic.dlg import ic_dlg

from .icFieldTempl import *
import ic.utils.util as util
import ic.utils.resource as resource
import ic.db.icdataset as icdataset
from ic.dlg import progress

import ic.imglib.common as common
import ic.components.user as user
import md5
import ic.interfaces.ictemplate as ictemplate
import ic.kernel.io_prnt as io_prnt
from ic.log import log

_ = wx.GetTranslation

__version__ = (1, 0, 1, 2)

#   Определяем словарь компонентов, которые могут парсится
componentModulDict = None


def ClearComponentModulDict():
    global componentModulDict
    componentModulDict = None


def GetComponentModulDict():
    global componentModulDict
    
    if not componentModulDict:
        componentModulDict = {}
        componentModulDict.update(components_lib.icGetSysModulDict())
        componentModulDict.update(user.icGetUserModulDict())

    return componentModulDict
    
#   Буфер перегружаемых фильтров. Ключ буффера задает алиас объекта данных, а значение фильтр.
#   Фильтр, который храниться  в буффере перегружает фильтр, который храниться в icDataLink (ключ 'filter').
#   Фильтр может быть задан двумя способами: словарем и строкой. Словарь задает фильтр на значение определенных
#   полей в объекте данных (Пример: {'peopleId': 5, 'town':'Moscow'}).
#   Строка задает SQL выражение на список уникальных идентивикаторов, по которому
#   происходит привязка к номеру строки (Пример: 'Select id from table where id < 1000').
DatasetFilterBuff = {}


def getDatasetFilterBuff():
    return DatasetFilterBuff


def setDatasetFilterBuff(obj):
    global DatasetFilterBuff
    DatasetFilterBuff = obj

DestroyDlgBuff = []


def getDatasetFilterBuff():
    return DestroyDlgBuff


def addDestroyDlgBuff(obj):
    global DestroyDlgBuff
    if len(DestroyDlgBuff) > 10:
        dlg = DestroyDlgBuff.pop(0)
        try:
            dlg.Destroy()
        except:
            pass
    else:
        DestroyDlgBuff.append(obj)


parserProgressDlg = None


def getProgressDlgBuff():
    return parserProgressDlg


def setProgressDlgBuff(obj):
    global parserProgressDlg
    parserProgressDlg = obj

#   В режиме отладки отличается способ импортирования - загруженные модули перегружаются.
#   Режим необходим для того, чтобы модуль перегружался после редактирования во внутреннем текстовом редакторе.
IS_TEST_MODE = False


def setTestMode(mode):
    """
    Устанавливает режим отладки.
    """
    global IS_TEST_MODE
    IS_TEST_MODE = mode


def isTestMode():
    """
    Возвращает признак отладки.
    """
    return IS_TEST_MODE


#   Признак режима дизайнера
IS_DESIGN_MODE = False
#   Указатвель на редактор форм
formEditorPoint = None


def setDesignMode(mode=True):
    global IS_DESIGN_MODE
    IS_DESIGN_MODE = mode


def getDesignMode():
    """
    Возвращает признак режима дезайнера.
    """
    return IS_DESIGN_MODE


def isEditorMode():
    """
    Возвращает признак режима дезайнера. Старая функция.
    Новая - getDesignMode().
    """
    return getDesignMode()


def setEditorPoint(editor, bDesign=True):
    """
    Функция устанавливает ссылку на редактор форм.
    """
    global formEditorPoint
    formEditorPoint = editor
    setDesignMode(bDesign)
    #   Дополнительно устанавливаем режим отладки
    setTestMode(True)


def getEditorPoint():
    """
    Функция возвращает ссылку на редактор форм.
    """
    return formEditorPoint

# Функции для работы с буфером форм
#   Буфер форм
ResultForm_Buff = {}
#   Размер буфера
SizeResultForm_Buff = 20


def clearFormBuffer():
    """
    Функция чистит буфер форм.
    """
    global ResultForm_Buff
    ResultForm_Buff = {}


def setStateFormInBuffer(formName, subsys, parent, flt='', state=False):
    """
    Устанавливает состояние формы (Используется уже или нет) из буфера.
    @type formName: C{string}
    @param formName: Имя формы.
    @type subsys: C{string}
    @param subsys: Имя подсистемы.
    @type parent: C{wx.Window}
    @param parent: Указатель на родительское окно.
    @type flt: C{dictionary | string}
    @param flt: Фильтр на форму.
    @type state: C{bool}
    @param state: True - форма взята из буфера и используется. False - форма
        свободна для использования.
    """
    from ic.components.icResourceParser import ResultForm_Buff
    key_frm = getFormKey(formName, subsys, parent, flt)
    try:
        ResultForm_Buff[key_frm][4] = state
        return True
    except:
        return False


def getFormKey(formName, subsys, parent, flt):
    """
    Функция генерирует уникальный ключ формы.
    @type formName: C{string}
    @param formName: Имя формы.
    @type subsys: C{string}
    @param subsys: Имя подсистемы.
    @type parent: C{wx.Window}
    @param parent: Указатель на родительское окно.
    @type flt: C{dictionary | string}
    @param flt: Фильтр на форму.
    @rtype: C{wx.Window}
    @return: Возвращает форму если находит в буфере, если нет то None.
    """
    if not subsys:
        subsys = ''
    flt_key = str(flt)
    prnt_key = ''
    if 'GetUniqId' in dir(parent):
        prnt_id_key = str(parent.GetUniqId())
    else:
        try:
            prnt_id_key = str(parent.GetId())
        except:
            prnt_id_key = '-1'
    
        try:
            prnt_key = '<%s>' % parent.type
        except:
            prnt_key = str(parent)
    
    str_key = formName + subsys + flt_key + prnt_key + prnt_id_key
    ret_key = md5.md5(str_key).hexdigest()
    return ret_key


def cmpTime(x, y):
    """
    Функция сравнения для сортировки списка в порядке уменьшения времени
    последнего обращения.
    """
    if x[2] > y[2]:
        return 1
    elif x[2] < y[2]:
        return -1
    else:
        return 0


def addFormToBuffer(frm, formName, subsys, parent, flt='', state=False):
    """
    Функция добавляет форму в буфер.
    @type frm: C{wx.Window}
    @param frm: Форму, которую надо сохранить в буфере.
    @type formName: C{string}
    @param formName: Имя формы.
    @type subsys: C{string}
    @param subsys: Имя подсистемы.
    @type parent: C{wx.Window}
    @param parent: Родительсое окно.
    @type flt: C{string | dictionary}
    @param flt: Фильтр, устанавливаемый на форму + дополнительный уникальный ключ.
    @type state: C{bool}
    @param state: Состояние окна. True - активное, False - пассивное. Получить
        ссылку на окно можно только, когда окно находится в пассивном состоянии.
    """
    global ResultForm_Buff
    bff = ResultForm_Buff
    sz = SizeResultForm_Buff
    if not subsys:
        subsys = ''
    
    #   По необходимости чистим буфер
    if sz*2 <= len(bff):
        mp = [[x[0], x[1][1], x[1][3], x[1][4]] for x in bff.items()]
        lst = [x for x in mp if int(x[3]) == 0]
        
        #   Сортируем в порядке уменьшения
        lst.sort(cmpTime)
        for x in lst[:sz]:
            win = bff.pop(x[0])
            try:
                win.Destroy()
            except:
                pass
                
    key_frm = getFormKey(formName, subsys, parent, flt)
    #   Определяем время сохранения формы в буфере.
    tm = time.clock()
    #   Четвертый элемент служит для хранения времени последнего обращения к
    #   к буферу данной формы
    if key_frm not in bff:
        bff[key_frm] = [frm, 1, tm, tm, state]
        return True
        
    return False


def getFormFromBuffer(formName, subsys, parent, flt=''):
    """
    Функция достает форму из буфера.
    @type formName: C{string}
    @param formName: Имя формы.
    @type subsys: C{string}
    @param subsys: Имя подсистемы.
    @type parent: C{wx.Window}
    @param parent: Указатель на родительское окно.
    @type flt: C{dictionary | string}
    @param flt: Фильтр на форму + дополнительный ключ уникальности.
    """
    global ResultForm_Buff
    bff = ResultForm_Buff
    key_frm = getFormKey(formName, subsys, parent, flt)
    #   Создаем форму
    try:
        if not bff[key_frm][4]:
            #   Получаем указатель на форму
            frm = bff[key_frm][0]
            #   Увеличиваем счетчик количеств обращений к данной форме
            bff[key_frm][1] += 1
            #   Записываем время последнего обращения
            bff[key_frm][3] = time.clock()
            #   На всякий случай если форма была разрушена (через Destroy)
            #   проверяем ее
            try:
                frm.GetId()
                #   На всякий случай если родитель был разрушен (через Destroy)
                if parent is not None:
                    parent.GetId()
            except:
                bff.pop(key_frm)
                frm = None
            
            io_prnt.outLog('\t[+] Form <%s> returned from buffer.' % formName)
            return frm
        else:
            io_prnt.outLog('key_frm=%s already is activated; struct=<%s>' % (key_frm, str(bff[key_frm])))
    except:
        io_prnt.outLog('\t[!] Form <%s> is not found in buffer.' % formName)
    
    return None


def CountResElements(res, count = 0):
    """
    Функция определяет количество элементов в ресурсном описании.
    """
    if isinstance(res, dict):
        if 'type' in res and res['type'] == 'DataLink':
            count += 1
        for key in res:
            if key in ['child', 'win1', 'win2']:
                count = CountResElements(res[key], count)
    elif isinstance(res, list):
        for el in res:
            count = CountResElements(el, count+1)

    return count
    
# Функции для работы с формами


def CreateForm(formName, fileRes=None, filter={}, bShow=False, logType=0,
               evalSpace=None, parent=None, formRes=None, bIndicator=True):
    """
    Функция создает форму по заданому ресурсному описанию.
    @type formName: C{string}
    @param formName: Имя подсистемы и имя формы через '/'. Если имя подсистемы не
         указано, то используется стандартный механизм поиска ресурса.
    @type fileRes: C{string}
    @param fileRes: Путь к ресурсному файлу. Если путь указан отностиельный, то
        это интерпретируется как имя подсистемы.
    @type filter: C{dictionary}
    @param filter: Словарь фильтров на объекты данных. В качестве ключей используются алиасы объектов данных, в качестве занчений
        либо картеж, либо строковое выражение. Если картеж, то фильтрация производится по значению поля, если строка, то по
        SQL  выражению специального вида.
    @type bShow: C{int}
    @param bShow: Признак того, что после создания объекта необходимо выполнить ф-ию Show(True).
    @type logType: C{int}
    @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
    @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
    @type evalSpace: C{dictionary}
    @type parent: C{wx.Window}
    @param parent: Указатель на родительское окно.
    @type formRes: C{dictionary}
    @param formRes: Ресурсное описание формы, если оно задано, то форма строится по этому описанию, а параметр fileRes игнорируется.
    @type bIndicator: C{bool}
    @param bIndicator: Признак индикатора процесса на создание формы.
    @rtype: C{wx.Window}
    @return: Возвращает форму.
    """
    log.info(u'Создание формы <%s>' % formName)
    try:
        frm = None
        #   Если ресурсное описание не задано берем его из ресурсного файла
        if formRes is None:
            #   По необходимости вычисляем имя ресурса
            if fileRes:
                fileRes = fileRes.replace('\\', '/')
                #   Если указан абсолютный путь
                if ':' in fileRes:
                    pathRes = fileRes
                #   В противном случае интнрпретируем как относительный путь
                else:
                    #   Определяем текущий системный путь
                    sys_path = resource.icGetSubsysResPaths()[0].replace('\\', '/')
                    pathRes = '/'.join(sys_path.split('/')[:-1])+'/'+fileRes
                    
                formRes = resource.icGetRes(formName, ext='frm', pathRes=pathRes, bRefresh=IS_TEST_MODE)
            else:
                formRes = resource.icGetRes(formName, ext='frm', bRefresh=IS_TEST_MODE, nameRes=formName)
            
        #   Заполняем буфер фильтрами
        setDatasetFilterBuff(filter)
        frm = icBuildObject(parent, formRes, evalSpace=evalSpace, bIndicator=bIndicator)
        #   Чистим буфер фильтров, чтобы он не влиял на работу icResourceParser в дальнейшем
        setDatasetFilterBuff({})
        if bShow and frm is not None:
            frm.Show(True)
            if bShow == 2:
                return frm
            return None
    except KeyError:
        MsgBox(None, _('Form <%s> is not found in resource: <%s>') % (formName, fileRes))
    except:
        io_prnt.outErr(_('Create form error'))
    
    return frm


def ModalForm(formName, fileRes=None, filter={}, logType=0,
              parent=None, bBuff=False, bIndicator=True, **kwargs):
    """
    Функция создает диалоговое окно. И возвращает введенные данные. Отличается
    от ResultForm тем, что evalSpace не передается - поскольку в ряде случаев
    это может (если этим пользоваться не аккуратно, например, передать простанство
    имен одной формы другой) приводить к печальным последствиям. Параметры
    формы передаются через **kwargs.
    @type formName: C{string}
    @param formName: Имя формы.
    @type fileRes: C{string}
    @param fileRes: Путь к ресурсному файлу. Если путь указан отностиельный, то
        это интерпретируется как имя подсистемы.
    @type filter: C{dictionary}
    @param filter: Словарь переопределяемых фильтров. В качестве ключей именна объектов данных (icSQLObjDataSet),
        в качестве значений фильты.
    @type logType: C{int}
    @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
    @type parent: C{wx.Window}
    @param parent: Указатель на родительское окно.
    @type bBuff: C{bool}
    @param bBuff: Признак буферизации диалоговой формы.
    @type bIndicator: C{bool}
    @param bIndicator: Признак индикатора процесса на создание формы.
    @param kwargs: Дополнительные именованные параметры, которые пропишутся в форме
        по ключу '_form_param'.
    @return: Возвращает введенные данные. Введенные данные должны быть сохранены
        формой в пространстве имен с ключем 'result'.
    """
    #   Если родитель не указан, то буферизация работает не стабильно, поэтому
    #   она отключается
    if not parent:
        bBuff = False

    #   Подготавливает пространство имен
    evalSpace = icwidget.icResObjContext()
    evalSpace['_form_param'] = kwargs
    if bBuff:
        frm = getFormFromBuffer(formName, fileRes, parent, filter)
    else:
        frm = None
        
    isAddToBuff = True
    st = None
    if frm:
        frm.Enable(True)
        setStateFormInBuffer(formName, fileRes, parent, filter, True)
        #   Обновляем параметры формы
        frm.evalSpace['_form_param'] = kwargs
    else:
        frm = CreateForm(formName, fileRes, filter, evalSpace=evalSpace, parent=parent, bIndicator=bIndicator)
        if bBuff:
            #   Если bBuff==False, следовательно форма с таким ключом уже
            #   существует и используется в данный момент
            bBuff = addFormToBuffer(frm, formName, fileRes, parent, filter, True)
       
    if frm is not None and frm.type == 'Dialog':
        frm.SetFocus()
        val = frm.ShowModal()
        try:
            if bBuff:
                setStateFormInBuffer(formName, fileRes, parent, filter, False)
            else:
                frm.Destroy()
        except:
            pass
    
        if val in [0, wx.ID_OK]:
            if 'result' in frm.evalSpace:
                return frm.evalSpace['result']
            else:
                return frm.evalSpace['_resultEval']
    return None


def ResultForm(formName, fileRes=None, filter={}, logType=0,
               evalSpace=None, parent=None, bBuff=False, bIndicator=True, key=''):
    """
    Функция создает диалоговое окно. И возвращает введенные данные.
    @type formName: C{string}
    @param formName: Имя формы.
    @type fileRes: C{string}
    @param fileRes: Путь к ресурсному файлу. Если путь указан отностиельный, то
        это интерпретируется как имя подсистемы.
    @type filter: C{dictionary}
    @param filter: Словарь переопределяемых фильтров. В качестве ключей именна объектов данных (icSQLObjDataSet),
        в качестве значений фильты.
    @type logType: C{int}
    @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
    @param evalSpace: Словарь дополнительных параметров.
    @type evalSpace: C{dictionary}
    @type parent: C{wx.Window}
    @param parent: Указатель на родительское окно.
    @type bBuff: C{bool}
    @param bBuff: Признак буферизации диалоговой формы.
    @type bIndicator: C{bool}
    @param bIndicator: Признак индикатора процесса на создание формы.
    @param key: Дополнительный ключ уникальности формы.
    @return: Возвращает введенные данные. Введенные данные должны быть сохранены формой в пространстве имен с ключем 'result'.
    """
    #   Если родитель не указан, то буферизация работает не стабильно, поэтому
    #   она отключается
    if not parent:
        bBuff = False

    oldSpace = evalSpace
    #   Подготавливает пространство имен
    if evalSpace in [None, {}]:
        evalSpace = icwidget.icResObjContext()

    if bBuff:
        if key:
            frm = getFormFromBuffer(formName, fileRes, parent, str(filter)+str(key))
        else:
            frm = getFormFromBuffer(formName, fileRes, parent, filter)
    else:
        frm = None
        
    isAddToBuff = True
    st = None
    if frm:
        frm.Enable(True)
        setStateFormInBuffer(formName, fileRes, parent, filter, True)
        #   Обновляем пространство имен, кроме служебных ключей (нач. с '_')
        if oldSpace:
            for key in oldSpace:
                if not frm.evalSpace.isSpecKey(key):
                    frm.evalSpace[key] = oldSpace[key]
    else:
        frm = CreateForm(formName, fileRes, filter, evalSpace=evalSpace, parent=parent, bIndicator=bIndicator)
                
        if bBuff:
            #   Если bBuff==False, следовательно форма с таким ключом уже
            #   существует и используется в данный момент
            bBuff = addFormToBuffer(frm, formName, fileRes, parent, str(filter)+str(key), True)
        
    if frm is not None and frm.type == 'Dialog':
        frm.SetFocus()
        val = frm.ShowModal()
        try:
            if bBuff:
                setStateFormInBuffer(formName, fileRes, parent, str(filter)+str(key), False)
            else:
                frm.Destroy()
        except:
            pass

        io_prnt.outLog(u'Dialog return value <%s> ok: %s' % (val, wx.ID_OK))

        if val in [0, wx.ID_OK]:
            if 'result' in frm.evalSpace:
                return frm.evalSpace['result']
            else:
                return frm.evalSpace['_resultEval']
    return None
    

# Функции парсера


def icBuildObject(parent, objRes, logType=0, evalSpace=None, bIndicator=False, id=None):
    """
    Функция собирает объект по ресурсному описанию.
    @type parent: C{wx.Window}
    @param parent: Указатель на родительское окно, на котором располагаются другие компоненты.
    @type objRes: C{Dictionary}
    @param objRes: Словарь с описанием компонента.
    @type logType: C{int}
    @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
    @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
    @type evalSpace: C{dictionary}
    @type bIndicator: C{bool}
    @param bIndicator: Признак отображения в ProgressBar-е. Иногда это не нужно -
        для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
        общего количества объектов.
    @param id: Идентификатор объекта. Если он не определен, то он генерируется автоматически.
    """
    log.info(u'Сборка объекта <%s>' % objRes['name'])
    #   Подготавливае пространство имен
    if evalSpace in [None, {}]:
        evalSpace = icwidget.icResObjContext()
    #   Запоминаем указатель на родительское окно объекта
    evalSpace['_main_parent'] = parent
    evalSpace['_root_obj'] = None
    dlg = None
    #   Устанавливаем режим работы формы
    #   Тестовый режим
    if isTestMode():
        evalSpace.setMode(util.IC_RUNTIME_MODE_TEST)
    #   Признак режима графического редактора
    elif isEditorMode():
        evalSpace.setMode(util.IC_RUNTIME_MODE_EDITOR)
    #   Режим runtime
    else:
        evalSpace.setMode(util.IC_RUNTIME_MODE_USUAL)
        
    if bIndicator:
        # ----------------------------------------------------------------------
        #   Создаем индикатор процесса разбора ресурсного описания
        max_elements = CountResElements([objRes])
        if max_elements > 50:
            max_elements += 10
        progress.icOpenProgressBar(_('Create form: <%s>') % objRes['name'], 0, max_elements+1)
    else:
        log.debug(_('Create form: <%s>') % objRes['name'])

    if parent:
        try:
            parent.type
        except:
            parent.type = 'ExternalWin'
            parent.components = {}
    #   Создаем объект.
    if id:
        ids = [id]
    else:
        ids = None
    try:
        if parent and parent.type == 'ResEditor':
            obj = icResourceParser(None, [objRes], logType=logType,
                                   evalSpace=evalSpace, bCounter=bIndicator, ids=ids)
            #   Корневой интерфейс может вернуть None
            if not obj:
                obj = evalSpace['_root_obj']
        else:
            icResourceParser(parent, [objRes], logType=logType,
                             evalSpace=evalSpace, bCounter=bIndicator, ids=ids)
            obj = evalSpace['_root_obj']
        
        #   Организуем очередь табуляции
        for ob in evalSpace['_dict_obj'].values():
            if issubclass(ob.__class__, icwidget.icWidget) and ob.moveAfterInTabOrder:
                try:
                    if ob.moveAfterInTabOrder in evalSpace['_dict_obj']:
                        after = evalSpace['_dict_obj'][ob.moveAfterInTabOrder]
                        ob.MoveAfterInTabOrder(after)
                except:
                    io_prnt.outErr('CREATE TAB ORDER ERROR')

        #   Посылаем сообщение о том, что форма создана для обычных объектов
        # Буфер объектов, которым сообщение onInit послано. Создаем буфер, чтобы
        # не посылать повторно сообщение из интерфейса
        post_buff_lst = []
        for ob in evalSpace['_dict_obj'].values():
            try:
                res = ob.GetResource()
                if 'onInit' in res and not res['onInit'] in ['', 'None', None]:
                    ob.PostOnInitEvent()
                    post_buff_lst.append(ob)
            except AttributeError:
                io_prnt.outWarning('### PostOnInitEvent() AttributeError <resource> obj: <%s>' % str(ob))

        #   Для объектов входящих в составной объект
        if '_interfaces' in evalSpace:
            for key, ifs in evalSpace['_interfaces'].items():
                for ob in ifs.getRegObjDict().values():
                    try:
                        res = ob.GetResource()
                        if ('onInit' in res and not res['onInit'] in ['', 'None', None]
                           and ob not in post_buff_lst):
                            ob.PostOnInitEvent()
                            post_buff_lst.append(ob)
                    except AttributeError:
                        io_prnt.outWarning('### PostOnInitEvent() AttributeError <resource> obj: <%s>' % ob)
    except:
        log.fatal(u'Создание формы (icBuildObject):')
        ic_dlg.icFatalBox(u'ОШИБКА', u'Создание формы (icBuildObject):')
        obj = None

    #   Уничтожаем индикатор процесса
    if bIndicator:
        progress.icCloseProgressBar()
    else:
        log.debug(_('End create form: <%s>') % objRes['name'])

    return obj


def createFrame(parent, id, component, logType, evalSpace):
    """
    Функция в зависимости от режима работы (работа | редактирование)
    создает фрейм.
    """
    if isEditorMode():
        evalSpace['__runtime_mode'] = util.IC_RUNTIME_MODE_EDITOR
        designer = components_lib.icframe.icFrame.GetDesigner()
        frm = designer(parent, id, component, logType, evalSpace)
    else:
        frm = components_lib.icframe.icFrame(parent, id, component, logType, evalSpace)
        frm.SetIcon(common.icoFrame)

    evalSpace['_root_obj'] = evalSpace.get('_root_obj', None) or frm
    return frm


def createDialog(parent, id, component, logType, evalSpace):
    """
    Функция в зависимости от режима работы (работа | редактирование)
    создает диалог.
    """
    log.info(u'Создание объекта диалога')
    if isEditorMode():
        evalSpace['__runtime_mode'] = util.IC_RUNTIME_MODE_EDITOR
        designer = components_lib.icdialog.icDialog.GetDesigner()
        dlg = designer(parent, id, component, logType, evalSpace)
    else:
        dlg = components_lib.icdialog.icDialog(parent, id, component, logType, evalSpace)
        dlg.SetIcon(common.icoDialog)
        
    evalSpace['_root_obj'] = evalSpace.get('_root_obj', None) or dlg
    return dlg


def Constructor(parent, id, component, logType=0, evalSpace=None,
                bCounter=False, progressDlg=None, bUserComponent=False, sizer=None):
    """
    Функция вызывает конструктор для создания объекта по ресурсному описанию.
    @type parent: C{wx.Window}
    @param parent: Указатель на родительское окно.
    @type id: C{int}
    @param id: Идентификатор окна.
    @type component: C{dictionary}
    @param component: Словарь описания компонента.
    @type logType: C{int}
    @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
    @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
    @type evalSpace: C{dictionary}
    @type bCounter: C{bool}
    @param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
        для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
        общего количества объектов.
    @type progressDlg: C{wx.ProgressDialog}
    @param progressDlg: Указатель на идикатор создания формы.
    """
    log.info(u'Вызов конструктора объекта <%s>' % component['name'])
    #   Вызываем конструктор
    modl = None
    try:
        # Переопределение компонентов
        if 'component_module' in component and not component['component_module'] in (None, 'None', ''):
            log.info(u'Импорт модуля <%s>' % component['component_module'])
            exec('import %s as modl' % component['component_module'])
        else:
            modl = GetComponentModulDict()[component['type']]
                        
        if '_root_obj' not in evalSpace or evalSpace['_root_obj'] is None:
            isParent = True
            oRoot = None
        else:
            isParent = False
            oRoot = evalSpace['_root_obj']

        # Если в конструкторе есть параметр 'sizer', то передаем его
        constr = getattr(modl, modl.ic_class_name)
        if isEditorMode():
            try:
                designer = constr.GetDesigner()
                if designer:
                    constr = designer
            except:
                io_prnt.outErr(_('Designer not found'))
                designer = None
        
        if 'sizer' in constr.__init__.im_func.func_code.co_varnames:
            wxw = constr(parent, id, component, logType, evalSpace,
                         bCounter=bCounter, progressDlg=progressDlg, sizer=sizer)
        else:
            wxw = constr(parent, id, component, logType, evalSpace,
                         bCounter=bCounter, progressDlg=progressDlg)
        # Некоторые компоненты могут совершать подмену объектов
        if hasattr(wxw, 'get_replace_object'):
            wxw = wxw.get_replace_object()
            
        #   Если компонент является шаблоном, то собираем по шаблону
        if issubclass(wxw.__class__, ictemplate.icTemplateInterface):
            # Для сложного компонента создаем новый контекст
            #   Регестрируем интверфейс шаблона
            if component['alias'] not in ('None', '', None):
                nm = component['alias']
            else:
                nm = component['name']
                
            res = wxw.GetResource()
            res['__interface__'] = nm
            parent = icResourceParser(parent, [res], sizer, logType=logType,
                                      evalSpace=evalSpace, bCounter=bCounter)
            wxw.init_component(evalSpace)
            wxw = None
        else:
            #   Определяем корневой элемент. Используем такое хитрое условие
            #   по причине того, что в парсере компонента, ['_root_obj'] может
            #   установить дочерний элемент, поскольку родительский еще не будет
            #   прописан в пространстве имен в качестве корневого.
            if wxw and isParent:
                evalSpace['_root_obj'] = wxw
        return wxw
    except:
        io_prnt.outErr('ERROR USER TYPE PARSE: <%s> mod=<%s>' % (component['type'], modl))


def icResourceParser(parent, components, sizer=None, logType=0,
                     evalSpace=None, bCounter=True, progressDlg=None, ids=None, **kwargs):
    """
    Парсер. Функция рекурсивного разбора ресурсного описания.
    @type parent: C{wx.Window}
    @param parent: Указатель на родительское окно, на котором располагаются другие компоненты.
    @type components: C{List}
    @param components: Список компонентов.
    @type sizer: C{wx.Sizer}
    @param sizer: Сайзер куда добавляются компоненты.
    @type logType: C{int}
    @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
    @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
    @type evalSpace: C{dictionary}
    @type bCounter: C{bool}
    @param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
        для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
        общего количества объектов.
    @type ids: {list | tuple}
    @param ids: Список идентификаторов объектов.
    """
    log.info(u'Сборка объектов')

    #   Получаем указатель на индикатор и указатель главного окна (Dialog, Frame)
    main_parent = evalSpace.get('_main_parent', None)
    
    # Создаем компоненты
    for cindx, component in enumerate(components):
        # Определяем идентификатор объекта
        if cindx < len(ids or []):
            component_id = ids[cindx]
        else:
            component_id = None

        #   Компонент создается только если установлен признак активации bActivated = True
        if util.isAcivateRes(component, evalSpace):
            #   Определяем имя родительского интерфейса, если он определен
            try:
                interface = parent.GetInterfaceName()
                if not interface and sizer:
                    interface = sizer.GetInterfaceName()
            except:
                interface = None
        
            wxw = None
            #   Если у компонета есть алиас, то разбор ведем с алиасным именем.
            #   Как правило алиас появляется при создании объета по ссылке через
            #   объект ссылки DataLink
            if 'alias' in component and not component['alias'] in [None, '', 'None']:
                name = component['alias']
            else:
                name = component['name']
            
            #   Прописываем имя родительского интерфеса в специальный ключ ресурса
            if interface and ('__interface__' not in component or
               ('__interface__' in component and not component['__interface__'])):
                component['__interface__'] = interface
            elif not interface and '__interface__' in component and component['__interface__']:
                interface = component['__interface__']
                
            if '__interface__' in component:
                interface = component['__interface__']
            #   Прописываем в пространстве имен имя файла ресурса
            if '__file_res' in component and component['__file_res']:
                evalSpace['__file_res'] = component['__file_res']
            #   Если определен индикатор процесса, то отображаем количество
            #   созданных компонентов ресурса
            if bCounter:
                progress.icUpdateProgressBar(u'Создаем компонент: <%s>' % name)
            else:
                log.debug(u'Создаем компонент: <%s> type: <%s>' % (name, component['type']))

            # Оконные компоненты
            if parent is None and component['type'] in ('Panel', 'Window',
               'ScrolledWindow', 'SplitterWindow'):
                parent = createFrame(main_parent, component_id or icNewId(), {'title': '',
                                     'size': component['size'],
                                     'position': component['position']}, logType, evalSpace)
            
            if component['type'] == 'Frame':
                parent = wxw = createFrame(main_parent, component_id or icNewId(), component, logType, evalSpace)
            elif component['type'] == 'Dialog':
                parent = wxw = createDialog(main_parent, component_id or icNewId(), component, logType, evalSpace)
            elif component['type'] == 'SizerSpace':
                # В режиме графического редактора заменяем на окно таких-же размеров
                if isEditorMode():
                    component['type'] = 'Panel'
                    wxw = components_lib.icwxpanel.icWXPanel(parent, -1, component, logType, evalSpace)
                    wxw.SetBackgroundColour(wx.Colour(200, 200, 250))
                else:
                    wxw = components_lib.sizers.icspacesizer.icSpaceSizer(parent, icNewId(), component,
                                                                          logType, evalSpace)

            # Служебные компоненты
            elif component['type'] == 'DataLink':
                link = icdataset.icDataLink(component, logType=logType,
                                            evalSpace=evalSpace, fltDict=DatasetFilterBuff)
                if isinstance(link.resource, dict):
                    parent = icResourceParser(parent, [link.resource],
                                              logType=logType, sizer=sizer,
                                              evalSpace=evalSpace, bCounter=False, ids=[component_id])

            # Импорт модулей и имен
            elif component['type'] == 'Import':
                imp = components_lib.icimport.icImport(parent, component_id or icNewId(), component, 0, evalSpace,
                                                       isDebug=IS_TEST_MODE)
                wxw = imp.GetObject()

            # Объект группы
            elif component['type'] == 'Group':
                if len(component['child']):
                    # Модуль ресурса грузится конструкторе icSimple, поэтому
                    # передаем имя модуля дочернему компоненту - все остальные
                    # компоненты системы наследники icSimple
                    if 'res_module' in component:
                        component['child'][0]['res_module'] = component['res_module']
                    parent = icResourceParser(parent, component['child'], sizer, logType=logType,
                                              evalSpace=evalSpace, bCounter=bCounter, ids=ids)

            # Стандартные и пользовательские компоненты
            else:
                wxw = Constructor(parent, component_id or icNewId(), component, logType, evalSpace,
                                  bCounter, progressDlg, sizer=sizer)

            # Выполняем выражения инициализации для не визуальных компонентов
            if wxw is None and 'init_expr' in component and not component['init_expr'] in (None, 'None', ''):
                if component.get('_uuid', None):
                    util.ic_eval(component['init_expr'], 0, evalSpace,
                                 'icResourceParser()<init_expr>. name:' + name,
                                 compileKey=component['_uuid']+'init_expr')
                else:
                    util.ic_eval(component['init_expr'], 0, evalSpace, 'icResourceParser()<init_expr>. name:' + name)

            # Регистрация компонентов
            if wxw:
                # Регестрируем компоненты в родительском интерфейсе
                if interface and interface in evalSpace['_interfaces']:
                    ifc = evalSpace['_interfaces'][interface]
                    ifc.reg_object(wxw, name)
                # Если корневой компонент еще не определен, определяем его
                if evalSpace['_root_obj'] is None:
                    evalSpace['_root_obj'] = wxw
                    parent = wxw
                # Регестрируем компоненты в контексте
                evalSpace['_dict_obj'][name] = wxw
                evalSpace['_list_obj'].append(wxw)
                evalSpace['self'] = wxw
                # В режиме редактирования регестрируем все компоненты в редакторе
                if isEditorMode():
                    edt = evalSpace['_root_obj']
                    if wxw != edt:
                        try:
                            edt.AddObject(wxw)
                        except:
                            io_prnt.outErr('### AddOject Error: <%s> edt=%s' % (wxw, edt))
                
            # Заполнение контейнеров
            if wxw is not None and parent is not None and name and component['type'] != 'Table':
                # Регестрируем компонены в родительском компоненте
                if parent.type != 'ExternalWin':
                    if not sizer:
                        parent.reg_child(wxw, name)
                    # NOTE: 7/05/08. Для того, чтобы можно было объект вставить в сайзер,
                    # который не является компонентом ic - для дизайнера форм
                    elif hasattr(sizer, 'reg_child'):
                        sizer.reg_child(wxw, name)
                elif sizer:
                    sizer.reg_child(wxw, name)
                # Выполняем выражения инициализации для компонентов
                if 'init_expr' in component and not component['init_expr'] in [None, 'None', '']:
                    evalSpace['evt'] = evalSpace.get('evt', None)
                    evalSpace['self'] = wxw
                    if '_uuid' in component and component['_uuid']:
                        util.ic_eval(component['init_expr'], 0, evalSpace,
                                     'icResourceParser()<init_expr>. name:' + name,
                                     compileKey=component['_uuid']+'init_expr')
                    else:
                        util.ic_eval(component['init_expr'], 0, evalSpace,
                                     'icResourceParser()<init_expr>. name:' + name)
                
                if 'source' in component and not component['source'] in ['', None, 'None']:
                        evalSpace['_has_source'][name] = wxw
                # Обрабатываем атрибут <show> - выражение, которое определяет
                #     показывать компонент или скрыть
                if 'show' in component:
                    bShow = component['show']
                    if bShow in ('1', 'True'):
                        bShow = True
                    elif bShow in ('0', 'False'):
                        bShow = False
                    else:
                        if '_uuid' in component and component['_uuid']:
                            res, val = util.ic_eval(component['show'], 0, evalSpace,
                                                    'icResourceParser()<show>. name:' + name,
                                                    compileKey=component['_uuid']+'show')
                        else:
                            res, val = util.ic_eval(component['show'], 0, evalSpace, 'Exception in icResourceParser()')

                        if res:
                            try:
                                bShow = bool(val)
                            except:
                                bShow = True
                    
                    if not bShow:
                        wxw.Show(bShow)
    return parent

# Создание объектов


def icCreateObject(ResName_, ResExt_, parent=None, context=None, subsys=None, className=None, **kwargs):
    """
    Функция создает объект по имени и типу ресурса.
    @type ResName_: C{string}
    @param ResName_: Имя ресурса, по которому создается объект.
    @type ResExt_: C{string}
    @param ResExt_: Расширения ресурсного файла для данного ресурса.
    @param parent: Родитель объекта (если необходим).
    @return: Возвращает объект или None в случае ошибки.
    """
    try:
        pathRes = None
        if subsys:
            pathRes = resource.getSubsysPath(subsys)
            
        if not className:
            className = ResName_
            
        res = resource.icGetRes(className, ResExt_, pathRes=pathRes, nameRes=ResName_)
        if res:
            # Если определен словарь замен используем его
            for attr_name, value in kwargs.get('replace_dct', {}).items():
                if attr_name not in ('type', 'style', 'name') and not attr_name.startswith('_'):
                    if attr_name in res:
                        res[attr_name] = value
                        io_prnt.outLog(u'Замена атрибута [%s] ресурса <%s>' % (attr_name, ResName_))
                    else:
                        # Если нет такого атрибута, значит это замена атрибутов дочернего объекта
                        if isinstance(value, dict):
                            res = resource.update_child_resource(attr_name, res, value)
                            io_prnt.outLog(u'Замена атрибутов дочернего объекта [%s] ресурса <%s>' % (attr_name, ResName_))
                        else:
                            io_prnt.outWarning(u'Не поддерживаемый тип %s замены ресурса дочернего объекта <%s>' % (type(value),
                                                                                                                    attr_name))
            
            if not context:
                context = icwidget.icResObjContext()
            
            return icBuildObject(parent, res, evalSpace=context, id=kwargs.get('id', None))
        return None
    except:
        io_prnt.outErr('CREATE OBJECT ERROR: [%s . %s]' % (ResName_, ResExt_))
        return None


#   Компилируем функцию разбора ресурсного описания, тут
#   могут быть большие накладные расходы на интерпретацию
try:
    import psyco
    icResourceParser = psyco.proxy(icResourceParser)
except:
    pass


if __name__ == '__main__':
    pass
