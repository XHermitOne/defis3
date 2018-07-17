#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
По ресурсному описанию формирует описание типов данных, выводимых гридом.

@type SPC_IC_KEY_ACTION: C{dictionary}
@var SPC_IC_KEY_ACTION: Спецификация на задание реакции на нажатие клавищи.
    - B{name='key'}: Имя.
    - B{type='KeyAction'}: Тип.
    - B{bShift=0}: Признак того, что для запуска выражения необходимо, чтобы
        был одновременно нажат Shift.
    - B{bCtrl=0}: Признак того, что для запуска выражения необходимо, чтобы
        был одновременно нажат Ctrl.
    - B{bAlt=0}: Признак того, что для запуска выражения необходимо, чтобы
        был одновременно нажат Alt.
    - B{expr=''}: Исполняемое выражение.

@type IC_RUNTIME_MODE_USUAL: C{int}
@var IC_RUNTIME_MODE_USUAL: Идентификатор режима работы приложения.
@type IC_RUNTIME_MODE_EDITOR: C{int}
@var IC_RUNTIME_MODE_EDITOR: Идентификатор режима работы графического редактора.
"""

import os
import os.path
import sys
import imp
import datetime
import wx
import types
import copy
import cPickle
import sets

# from ic.log.iclog import LogLastError
# from ic.log.iclog import MsgLastError
import ic.kernel.icContext as icContext
from ic.kernel import io_prnt
from ic.dlg import ic_dlg
from . import coderror
from . import ic_uuid
from ic.log import log
import ic

__version__ = (1, 0, 1, 2)

_ = wx.GetTranslation

#
#   Идентификаторы режим запуска формы
#
#   Режим приложения
IC_RUNTIME_MODE_USUAL = 0
#   В режиме графического редактора
IC_RUNTIME_MODE_EDITOR = 1
#   Режим отладки приложения
IC_RUNTIME_MODE_DEBUG = 2
#   Режим тестирования приложения
IC_RUNTIME_MODE_TEST = 3

#   Буферы откомпилированных выражений. В качестве ключей уникальные идентификаторы,
#   в качестве значений откомпилированное выражение.
icExecCompileBuff = {}
icEvalCompileBuff = {}

#   Протокол хранения сериализованных объектов модулем cPickle
# ВНИМАНИЕ! PICKLE_PROTOCOL = 1 и 2 использовать нельзя - ресурсы не востанавливаются
PICKLE_PROTOCOL = 0


def ClearCompileBuff():
    """
    Чистит буфер откомпилированных выражений.
    """
    global icExecCompileBuff
    global icEvalCompileBuff
    icExecCompileBuff = {}
    icEvalCompileBuff = {}


def delInfFromBuffByUUID(uuid):
    """
    Удаляет из буфера выражения заданного по uuid объекта.
    """
    global icExecCompileBuff
    global icEvalCompileBuff
    # Ищем ключи определенного объекта icExecCompileBuff
    lst = []
    for key in icExecCompileBuff.keys():
        if key.startswith(uuid):
            lst.append(key)
    # Удаляем найденные ключи
    for el in lst:
        icExecCompileBuff.pop(el)

    # Ищем ключи определенного объекта в буфере icEvalCompileBuff
    lst = []
    for key in icEvalCompileBuff.keys():
        if key.startswith(uuid):
            lst.append(key)
    # Удаляем найденные ключи
    for el in lst:
        icEvalCompileBuff.pop(el)


def isKeyInCompileBuff(key, kind):
    """
    Проверяет ключ в буферном словаре.
    """
    if kind == 'eval':
        return key in icEvalCompileBuff
    elif kind == 'exec':
        return key in icExecCompileBuff
    return False


def SetCompileString(UnicId, kind, compl):
    """
    Сохраняет откомпилированную строку в буфере.
    """
    global icExecCompileBuff
    global icEvalCompileBuff
    if kind == 'eval':
        icEvalCompileBuff[UnicId] = compl
    elif kind == 'exec':
        icExecCompileBuff[UnicId] = compl


def GetCompileString(UnicId, kind):
    """
    Возвращает откомпилированную строку из буфера.
    @type UnicId: C{string}
    @param UnicId: Уникальный идентификатор строки.
    @type kind: C{string}
    @param kind: Тип откомпилированной строки.
    """
    global icExecCompileBuff
    global icEvalCompileBuff

    if kind == 'eval' and UnicId in icEvalCompileBuff:
        return icEvalCompileBuff[UnicId]
    elif kind == 'exec' and UnicId in icExecCompileBuff:
        return icExecCompileBuff[UnicId]

    return None


#   Буфер транслированных ресурсных файлов
Buff_readAndEvalFile = {}


def prepareDictRpl(fileVar):
    """
    Подготавливает словарь замен по ресурсному описанию свойств системы
    (*.var) для функции readAndEvalFile.
    @type fileVar: C{string}
    @param fileVar: Имя файла, свойств (*.var)
    @rtype: C{dictionary}
    @return: Возвращает словрь замен. В качестве ключа %имя переменной%, в качестве значения аттрибут 'data' из описания
        свойств.
    """
    try:
        dictRpl = {}
        _dict = readAndEvalFile(fileVar, {})
        for key in _dict:
            dictRpl['%' + key +'%'] = _dict[key]['data']
    except:
        dictRpl = {}

    return dictRpl


def clearResourceBuff(fileName=None):
    """
    Функция чистит буфер прочитанных ресурсов.
    """
    global Buff_readAndEvalFile
    if not fileName:
        Buff_readAndEvalFile = {}
    elif fileName in Buff_readAndEvalFile:
        Buff_readAndEvalFile.pop(fileName)


def readAndEvalFile(filename, dictRpl={}, bRefresh=False, *arg, **kwarg):
    """
    Функция читает файл и выполняет его.
    @type filename: C{string}
    @param filename: Имя ресурсного файла.
    @type dictRpl: C{dictionary}
    @param dictRpl: Словарь замен.
    @type bRefresh: C{bool}
    @param bRefresh: Признак того, что файл надо перечитать даже если он
        буферезирован.
    """
    obj = None
    filename = filename.strip()
    try:
        #   Проверяем есть ли в буфферном файле такой объект, если есть, то его и возвращаем
        if not bRefresh and filename in Buff_readAndEvalFile:
            io_prnt.outLog(' '*3+'[b] ' + ('Return from buffer; file:%s' % filename))
            return Buff_readAndEvalFile[filename]

        nm = os.path.basename(filename)
        pt = nm.find('.')
        if pt >= 0:
            filepcl = os.path.dirname(filename) + '/' + nm[:pt] + '_pkl' + nm[pt:]
        else:
            filepcl = os.path.dirname(filename) + '/' + nm +'_pkl'

        #   Проверяем нужно ли компилировать данную структуру по следующим признакам:
        #   наличие скомпилированного файла, по времени последней модификации.
        try:
            if (os.path.isfile(filepcl) and not os.path.isfile(filename)) or \
                    (os.path.getmtime(filename) < os.path.getmtime(filepcl)):
                #   Пытаеся прочитать сохраненную структуру если время последней
                #   модификации текстового представления меньше, времени
                #   последней модификации транслированного варианта.
                fpcl = None
                try:
                    fpcl = open(filepcl)
                    obj = cPickle.load(fpcl)
                    fpcl.close()
                    #   Сохраняем объект в буфере
                    Buff_readAndEvalFile[filename] = obj
                    io_prnt.outLog('\t[+] Load from: %s' % filepcl)
                    return obj
                except IOError:
                    io_prnt.outErr(_('\t[-] readAndEvalFile: Open file error: %s.') % filepcl)
                except:
                    if fpcl:
                        fpcl.close()
                    io_prnt.outErr(_('readAndEvalFile: Open file error: %s.') % filepcl)
        except OSError:
            io_prnt.outWarning(u'Ошибка файла <%s>' % filename)
        #   Пытаемся прочитать cPickle, если не удается считаем, что в файле
        #   хранится текст. Читаем его, выполняем, полученный объект сохраняем
        #   на диске для последующего использования
        if os.path.isfile(filename):
            try:
                fpcl = open(filename)
                obj = cPickle.load(fpcl)
                fpcl.close()
                #   Сохраняем объект в буфере
                Buff_readAndEvalFile[filename] = obj
                io_prnt.outLog('\t[+] Load file <cPickle Format>: %s' % filename)
                return obj
            except Exception, msg:
                io_prnt.outLog('\t[*] <Non cPickle Format file:%s. Try to compile text>' % filename)

        #   Открываем текстовое представление, если его нет, то создаем его
        f = open(filename, 'rb')
        txt = f.read().replace('\r\n', '\n')
        f.close()
        for key in dictRpl:
            txt = txt.replace(key, dictRpl[key])

        #   Выполняем
        obj = eval(txt)
        #   Сохраняем объект в буфере
        Buff_readAndEvalFile[filename] = obj

        #   Сохраняем транслированный вариант
        fpcl = open(filepcl, 'w')
        io_prnt.outLog('create: %s' % filepcl)
        cPickle.dump(obj, fpcl, PICKLE_PROTOCOL)
        fpcl.close()
    except IOError:
        io_prnt.outErr(_('\t[*] readAndEvalFile: Open file error: %s.') % filename)
        obj = None
    except:
        io_prnt.outErr(_('\t[*] readAndEvalFile: translation error: %s.') % filename)
        obj = None

    return obj


def getFullSpc(spc):
    """
    Собирает полную спецификацию.
    """
    pass


def DeepCopy(struct):
    """
    Глубокое копирование.
    """
    return copy.deepcopy(struct)


def icSpcDefStruct(spc, struct, bAll=False, count=0):
    """
    Дополняет структуру описания объекта до требований спецификации.
    @type spc: C{dictionary}
    @param spc: Словарь описания спецификации.
    @type struct: C{dictionary}
    @param struct: Словарь описания структуры.
    @type bAll: C{bool}
    @param bAll: Признак того, чтобы дополнение шло по всем атрибутам, в
        том числе и служебным (__*) с учетом наследования по атрибуту '__parent__' .
    @rtype: C{dictionary}
    @return: Дополненная структура.
    """
    if struct is None:
        struct = {}

    if spc is None:
        spc = {}

    if bAll:
        if '__attr_types__' not in struct:
            struct['__attr_types__'] = {}
    try:
        for key in spc.keys():
            if bAll:
                if key == '__parent__' and isinstance(spc['__parent__'], dict):
                    count += 1
                    struct = icSpcDefStruct(spc['__parent__'], struct, bAll, count)
                #   Дополняем описание событий
                if (key == '__events__' and isinstance(spc[key], dict)
                    and key in struct and isinstance(struct[key], dict)):
                    for attr in spc[key].keys():
                        if attr not in struct[key].keys():
                            struct[key][attr] = spc[key][attr]
                #   Дополняем описание типов атрибутов
                elif (key == '__attr_types__' and key in struct and isinstance(struct[key], dict)
                    and isinstance(spc[key], dict)):
                    for attr in spc[key].keys():
                        if attr not in struct[key].keys():
                            struct[key][attr] = spc[key][attr]
                        else:
                            struct[key][attr] = list(sets.Set(struct[key][attr])
                                                | sets.Set(spc[key][attr]))
                elif key not in struct and key not in ('__parent__',):
                    if isinstance(spc[key], list):
                        struct[key] = copy.deepcopy(spc[key])
                    else:
                        struct[key] = spc[key]
            #   Служебные атрибуты не наследуем
            elif key not in ['__events__', '__lists__', '__attr_types__', '__styles__','__parent__'] and key not in struct:
                if isinstance(spc[key], list):
                    struct[key] = copy.deepcopy(spc[key])
                else:
                    struct[key] = spc[key]

    except Exception:
        io_prnt.outErr('icSpcDefStruct error')

    return struct


def AddAttrSpace(obj, localSpace):
    """
    Добавляет все аттрибуты объета в словарь кроме внутренних аттрибутов,
    имена котроых начинаются с '_' и '__'
    @param obj: Обеъект.
    @param localSpace: Словарь имен.
    @type localSpace: C{dictionary}
    """
    attr_obj = dir(obj)
    for attr in attr_obj:
        if attr[0] != '_':
            localSpace[attr] = getattr(obj, attr)


def MyExec(s):
    exec s


def transform_to_func(expr, compileKey=None):
    """
    Трансформирует текст скрипта к вызову функции.
    """
    if compileKey:
        fs = compileKey
    else:
        fs = ''
    beg = 'def __f__%s():' % fs
    end = '''
    globals().update(locals()); return _resultEval
_ret = __f__%s()
if _ret <> None:
    _resultEval = _ret
''' % fs
    return beg.replace('\r\n', '\n') + '\n    '+expr.replace('\n', '\n    ') + end.replace('\r\n', '\n')


def replReturn(s):
    """
    Заменяем 'return' на 'globals().update(locals());return' для того, чтобы пространство
    имен функции отобразилось на пространство имен объекта.
    """
    pos = 0
    ns = ''
    repl = 'globals().update(locals()); return'
    if s.find('return') == 0:
        s = '\n'+s

    while pos != -1:
        pos = s.find('return', pos)
        if pos > 0:
            if pos+6 >= len(s):
                pe = ''
            else:
                pe = s[pos+6]

            if s[pos-1] in ('\n', ' ', ';') and pe in ('', ' ', ';', '\n'):
                s = s[:pos] + repl + s[pos+6:]
                pos += len(repl)
            else:
                pos += 6
    return s


def ic_eval(expr, logType=-1, evalSpace=None, msg='', globSpace=None, compileKey=None):
    """
    Функция выполняет предобработку вычисляемого выражения, вычисляет с
    использование стандартной, функции eval(...), а также обрабатывает исключения.
    В качестве локального пространства имен используется словарь evalSpace.
    В качестве глобального пространства имен берется словарь возвращаемый функцией
    globals(). Если передается уникальный идентификатор выполняемого выражения,
    то функция откомпилирует выражение и сохранит в буфере для последующего
    использования.
    @type expr: C{string}
    @param expr: Вычисляемое выражение.
    @type logType: C{int}
    @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
    @param evalSpace: Пространство имен, необходимых для вычисления выражения
    @type evalSpace: C{dictionary}
    @type msg: C{string}
    @param msg: Сообщение, которое дополнительно выводится при ошибке. Если параметр None,
        то сообщение об ошибке не выводится.
    @param globSpace: Глобальное пространство имен.
    @type globSpace: C{dictionary}
    @type compileKey: C{int}
    @param compileKey: Идентификатор компилированного выражения.
    @return: Код ошибки из модуля coderror, Возвращаемое значение вычисляемого выржения.
    """
    # В режиме отладки если определены точки остонова в выражении,
    # вызовы перенаправляются в служебный модуль, в котором соответствующие
    # вычисляемые выражения представляются функциями с уникальным именами. Такой
    # прием позволяет воспользоваться стандартым отладчиком pdb.py.
    if (evalSpace and compileKey and '__runtime_mode' in evalSpace and
        evalSpace['__runtime_mode'] == IC_RUNTIME_MODE_DEBUG):
        try:
            # subsys = resource.icGetResPath().split('/')[-1]
            subsys = ic.icGet('SYS_RES').split('/')[-1]
            MyExec('import %s.debug as debugModul' % subsys)
            newSpace = eval('debugModul.f_%s(_esp)' % compileKey, globSpace, evalSpace)
            evalSpace.update(newSpace)
            if '_resultEval' in evalSpace:
                ret = evalSpace['_resultEval']

            io_prnt.outLog(u'### EXECUTE ATTRIBUTE DEBUG FUNCTION f%s(_esp)' % compileKey)
            return coderror.IC_EVAL_OK, ret
        except:
            io_prnt.outErr(msg)
            io_prnt.outWarning(u'''ВНИМАНИЕ! 
            Если GetManager(self) возвращает None, 
            то возможна ошибка в не корректном определении manager_class в модуле ресурса''')

    if globSpace is None:
        globSpace = globals()

    #   Отсекаем по типу выражения
    if type(expr) not in (str, unicode):
        return coderror.IC_EVAL_ERROR, None

    #   Отсекаем пустые строки
    if expr == '':
        return coderror.IC_EVAL_OK, ''

    bSuccess, ret = coderror.IC_EVAL_OK, None
    evalSpace['_resultEval'] = None

    #####################################################
    #   Если выражение уже откомпилировано, то пытаемся
    #   его выполнить
    bCompile = False
    if compileKey:
        try:
            s = GetCompileString(compileKey, 'eval')
            if s:
                ret = eval(s, globSpace, evalSpace)
                bCompile = True
            else:
                s = GetCompileString(compileKey, 'exec')
                if s:
                    exec(s, evalSpace)
                    bCompile = True
                    if '_resultEval' in evalSpace:
                        ret = evalSpace['_resultEval']
        except:
            if msg is not None:
                ret = u'EXEC[EVAL] EXCEPTION IN %s: exec(%s)' % (msg, expr)
                io_prnt.outErr(ret)
                io_prnt.outWarning(u'''ВНИМАНИЕ! 
                Если GetManager(self) возвращает None, 
                то возможна ошибка в не корректном определении manager_class в модуле ресурса''')
            return coderror.IC_EVAL_ERROR, ret
    #############################################
    #   Компилируем и выполняем, если выражение еще
    #   не компилировалось
    if not bCompile:
        try:
            if expr[0] == '@':
                expr = expr[1:]

            expr = expr.replace('\r\n', '\n').replace('\r', '\n')
            expr_ = replReturn(expr)
            s = compile(expr_, '<string>', 'eval')
            ret = eval(s, globSpace, evalSpace)
            if compileKey:
                SetCompileString(compileKey, 'eval', s)
        except:
            try:
                #   Скрипт преобразуем к вызову функции
                #   Это позволяет использовать в скриптах команду <return>
                expr = transform_to_func(expr, compileKey)
                s = compile(expr, '<string>', 'exec')
                exec(s, evalSpace)
                if compileKey:
                    SetCompileString(compileKey, 'exec', s)
                ret = evalSpace.get('_resultEval', None)
            except:
                bSuccess = coderror.IC_EVAL_ERROR
                if msg is not None:
                    ret = u'EXEC EXCEPTION IN %s: exec(%s)' % (msg, expr)
                    io_prnt.outErr(ret)
                    io_prnt.outWarning(u'''ВНИМАНИЕ! 
                    Если GetManager(self) возвращает None, 
                    то возможна ошибка в не корректном определении manager_class в модуле ресурса''')
    return bSuccess, ret


def icEvalExpr(expr, spcRepl = '', funcPath = ''):
    """
    Функция производит замены специальных символов в выражении на необходимые ссылки
    B{Пример:} C{icEvalExpr('@GetRowSum(_.row, 0)', 'self.parent.grid', 'ic.globfunc.grid') ->
    'ic.globfunc.grid.GetRowSum(self.parent.grid.row, 0)'}
    @type expr: C{string}
    @param expr: Преобразовываемое выражение.
    @type spcRepl: C{string}
    @param spcRepl: Строка замены. Специальное слово '_.' заменяется на данную
        строку. Позволяет значительно сократить размеры выражений, за счет
        упращения записи ссылок на некоторые объекты.
    @type funcPath: C{string}
    @param funcPath: Путь до функции.
        B{Пример:} C{'self.parent.owner', 'ic.globFunc.accounts'}
    """
    if type(expr) not in (str, unicode) or expr == '':
        return ''

    expr = expr.replace('_. ', spcRepl).replace('_.,', spcRepl+',').replace('_.', spcRepl+'.')
    if expr[0] == '@':
        expr = expr[1:]
    elif funcPath != '':
        expr = funcPath + expr

    return expr

# Функции достура к объектам пространства имен формы


def getICObj(objName, evalSpace):
    """
    Возвращает объект из пространства имен формы.
    @type objName: C{string}
    @param objName: Имя объекта.
    @param evalSpace: Пространство имен формы.
    @type evalSpace: C{dictionary}
    """
    try:
        obj = evalSpace['_dict_obj'][objName]
    except KeyError:
        obj = None

    return obj


def getICDataObj(objName, evalSpace):
    """
    Возвращает объект данных из пространства имен формы.
    @type objName: C{string}
    @param objName: Имя объекта.
    @param evalSpace: Пространство имен формы.
    @type evalSpace: C{dictionary}
    """
    try:
        obj = evalSpace['_sources'][objName]
    except:
        obj = None
    return obj

# Коды доступа
#   Код доступа недопускающий переопределения
CODE_NOBODY = 1234567
CODE_NODEL = 1


def setKey(evalSpace, key, obj, cod_access=None):
    """
    Функция добавляет объект в пространство имен.
    @param evalSpace: Пространство имен формы.
    @type evalSpace: C{dictionary}
    @param key: Ключ в пространстве имен.
    @type key: C{string}
    @param obj: Объект, который надо добавить.
    @param cod_access: Код доступа на изменение значения ключа.
    @rtype: C{bool}
    @return: Возвращает признак успешного добавления.
    """
    if '_access_keys' not in evalSpace:
        evalSpace['_access_keys'] = {}

    akey = evalSpace['_access_keys']
    try:
        if key not in akey.keys() or (key in akey.keys() and cod_access == akey[key]):
            if cod_access != CODE_NOBODY or (cod_access == CODE_NOBODY and key not in evalSpace):
                evalSpace[key] = obj
            if cod_access is not None:
                evalSpace['_access_keys'][key] = cod_access
            return True
    except:
        io_prnt.outLog('ERROR setKey')

    return False

# Функции пространства имен формы
bInit_var = False
icprs = None
icres = None
common = None


def init_eval_space_modules():
    global bInit_var
    global icprs, icres, common
    if not bInit_var:
        import ic.components.icResourceParser as _icprs
        import ic.utils.resource as _icres
        import ic.imglib.common as _common
        icprs, icres, common = _icprs, _icres, _common
        bInit_var = True

    return icprs, icres, common


def InitEvalSpace(evalSpace=None):
    """
    Функция создает структуру пространства имен для внешних функций при
    обработке сообщений в формах.
    Ключи:
    - B{_root_obj}: Содержит дерево объектов
    - B{_dict_obj}: Содержит словарь всех объектов. Имена объектов используются в
        качестве ключей.
    - B{_lfp}: Содержит описание параметров последней вызванной функции.
    - B{_self}: Содержит указатель на объект, где происходят вычисления.
    - B{_has_source}: Содержит словарь всех объектов, которые обращаются к
        источникам данных. Признаком таких объектов является ключ 'source' в их
        ресурсном описании.
    - B{_sources}: Содержит словарь всех источников данных.
    """
    init_eval_space_modules()
    if evalSpace is None:
        evalSpace = icContext.Context(ic.getKernel())
    else:
        space = icContext.Context()
        space.update(evalSpace)
        evalSpace = space

    evalSpace.setKey('CreateForm', icprs.CreateForm)
    evalSpace.setKey('ResultForm', icprs.ResultForm)
    evalSpace.setKey('ModalForm', icprs.ModalForm)
    evalSpace.setKey('method', icres.method)
    evalSpace.setKey('setKey', setKey)
    evalSpace.setKey('wx', wx)
    evalSpace.setKey('ic', ic)
    evalSpace.setKey('SetFilter', SetFilter)
    evalSpace.setKey('icImageLibName', common.icImageLibName)
    evalSpace.setKey('imglib', common)
    evalSpace.setKey('common', common)
    return evalSpace


def SetFilter(dataset, flt=None):
    """
    Устанавливаем фильтр на нужный объект данных.
    @type dataset: C{icSQLObjDataset}
    @param dataset: Объект индексного доступа к классу данных.
    @type flt: C{string | dictionary}
    @param flt: Фильтр, накладываемый на класс данных.
    """
    try:
        real_name = dataset.name
        #   Если буфер заполнен, то необходимо запросить потверждение на
        #   обновление данных и обновить данные. В противном случае изменения
        #   будут потеряны
        if dataset.isChangeRowBuff() and ic_dlg.icAskBox(None, _('Save changes?'),
                                                         style=wx.YES_NO | wx.ICON_QUESTION) == wx.ID_YES:
            dataset.update()

        dataset.FilterFields(flt)
        #   Уведомляем другие компоненты формы о том, что состояние объекта данных могло измениться
        for key, obj in dataset.evalSpace['_has_source'].items():
            try:
                dataset.evalSpace['_has_source'][key].UpdateViewFromDB(real_name)
                #   Обновляем связанные гриды
                dataset.evalSpace['_has_source'][key].UpdateDataView(real_name)
            except:
                pass
    except:
        log.fatal(u'SetFilter Error')


def ic_import(dict_names, evalSpace = {}, isDebug = False):
    """
    Функция формирует пространство имен выражений.
    @param dict_names: Словарь описания пространства имен. Пример: C{'{'ic.dlg.msgbox':['MsgBox','']}'}
    @type dict_names: C{dictionary}
    @param evalSpace: Пространство имен формы.
    @type evalSpace: C{dictionary}
    @param isDebug: Признак режима отладки. В режиме отладки, модули каждый раз
        перегружаются, поскольку они могут измениться - пользователь мог их
        отредактировать.
    @type isDebug: C{bool}
    @rtype: C{bool}
    @return: Возвращает признак успешного выполнения.
    """
    if not dict_names:
        return False

    for key in dict_names:
        try:
            # Загрузка модуля
            #   В режиме отладки, модули каждый раз перегружаем, поскольку они
            #   могут измениться - пользователь мог их отредактировать.
            if isDebug:
                try:
                    if not key[:3] == 'ic.':
                        pass
                except:
                    pass

                exec 'import %s' % key
            else:
                exec 'import %s' % key

            nm = ''

            #   Пытаемся загрузить имена в наше пространство имен
            try:
                evalSpace[key.split('.')[-1]] = sys.modules[key]
                for nm in dict_names[key]:
                    #   Грузим все имена, кроме тех, которые начинаются с '_'
                    if nm == '*':
                        AddAttrSpace(sys.modules[key], evalSpace)
                        break
                    else:
                        evalSpace[nm] = getattr(sys.modules[key], nm)
            except:
                log.fatal(_('Import error <%s> in <%s>.') % (nm, key))
                return False

        except:
            log.fatal(_('Import module error: %s') % key)
            return False

    return True


def icImport(name):
    """
    Импортирование модуля. Пример: subsys.usercomponents.component
    @type name: C{string}
    @param name: Имя модуля.
    """
    mod = __import__(name, globals(), locals(), [], -1)
    # Поскольку __import__ возвращает родительский модуль
    # получаем доступ до нужного нам модуля через
    # рекурсивный getattr
    c = name.split('.')
    for x in c[1:]:
        mod = getattr(mod, x)
    return mod


def icLoadSource(name, path):
    """
    Возвращает загруженный модуль.
    @type name: C{string}
    @param name: Имя модуля.
    @type path: C{string}
    @param path: Полный путь до модуля.
    """
    f = open(path)
    mod = imp.load_source(name, path, f)
    f.close()
    return mod


def icUnLoadSource(name):
    """
    Выгрузить модуль.
    @type name: C{string}
    @param name: Имя модуля.
    """
    if name in sys.modules:
        del sys.modules[name]
        return True
    return False


def icReLoadSource(name, path=None):
    """
    Перезагрузить модуль.
    @type name: C{string}
    @param name: Имя модуля.
    @type path: C{string}
    @param path: Полный путь до модуля.
    """
    if path is None:
        if name in sys.modules:
            try:
                py_file_name = sys.modules[name].__file__
                py_file_name = os.path.splitext(py_file_name)[0]+'.py'
                path = py_file_name
            except:
                io_prnt.outErr('Error')
                return None
        else:
            return None
    icUnLoadSource(name)
    return icLoadSource(name, path)


def isExprDict(expr):
    """
    Функция определяет, является выражение записью словаря.
    @type expr: C{string}
    @param expr: Строковое выражение.
    @rtype: C{bool}
    @return: Признак словаря.
    """
    if type(expr) in (str, unicode) and len(expr) > 0 and expr[0] == '{' and expr[-1] == '}':
        return True

    return False

def isAcivateRes(res, evalSpace):
    """
    Функция определяет активированный ресурс или нет.
    @param res: Ресурсное описание компонента.
    @type res: C{dictionary}
    @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
    @type evalSpace: C{dictionary}
    @rtype: C{bool}
    @return: Признак акивированного ресурсного описания компонента. В противном случае
        компонет не будет создан.
    """
    bActivated = True
    if 'activate' in res and res['activate'] != '1':
        exprKey = None
        if '_uuid' in res and res['_uuid']:
            exprKey = ic_uuid.get_uuid_attr(res['_uuid'], 'activate')

        ret, val = ic_eval(res['activate'], 0, evalSpace,
                           'Exception in util.isActivateRes <activate>', compileKey=exprKey)
        if ret:
            bActivated = val
        #   Если тип числовой
        elif res['activate'] == 0:
            bActivated = False
    return bActivated

# SPC_IC_KEY_ACTION = {...}
SPC_IC_KEY_ACTION = {'name': 'key',
                     'type': 'KeyAction',
                     'bShift': 0,
                     'bCtrl': 0,
                     'bAlt': 0
                     }


def getKeyExpr(expr, keycod, evt, evalSpace={}):
    """
    Функция возвращает выражения для обработки нажатия клавиш. Словарь
    expr задает способы реакции на некоторые клавиши.
    Пример: {'wx.WXK_F3':{'bShift':0, 'bCtrl':0, 'expr':'func_F3()'}, ...}
    @type expr: C{string | dictionary}
    @param expr: Вычисляемое выражение.
    @type keycod: C{string}
    @param keycod: Код нажатой клавиши (ключ).
    @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
    @type evalSpace: C{dictionary}
    """
    result = expr
    keyctrl = ic.utils.coderror.IC_CTRLKEY_OK
    key_val = None

    #   Выполняем выражение обработки нажатия клавиш клавиатуры
    if expr not in [None, '', 'None']:
        #   Если expr словарь, то он задает способы реакции на некоторые
        #   клавиши. Пример: {'wx.WXK_F3':{'bShift':0, 'bCtrl':0, 'expr':'func_F3()'}, ...}
        if type(expr) in (str, unicode):
            ret, val = ic_eval(expr, 0, evalSpace, 'getKeyExpr()')
            result = None
            if ret and isinstance(val, dict) and keycod in val.keys():
                key_val = val[keycod]
            elif ret and not isinstance(val, dict):
                try:
                    keyctrl = int(val)
                except:
                    pass

        elif isinstance(expr, dict) and keycod in expr.keys():
            key_val = expr[keycod]

        #   Если значение словарь, то разбираем дальше
        if isinstance(key_val, dict):
            #   Дополняем до спецификации
            act = icSpcDefStruct(SPC_IC_KEY_ACTION, key_val)
            if (act['bShift'] == evt.ShiftDown() and act['bCtrl'] == evt.ControlDown()
                    and act['bAlt'] == evt.AltDown()):
                result = act['expr']
            else:
                result = None

        #   Если значение строка,
        elif type(key_val) in (str, unicode):
            result = key_val

        #   Вычисляем выражение реакции на нажатие клавиши. Если такая реакция
        #   описана
        if result:
            ret, val = ic_eval(result, 0, evalSpace, 'getKeyExpr()')
            if ret:
                try:
                    keyctrl = int(val)
                except:
                    pass
    return keyctrl


def getSpcAttr(res, key, evalSpace={}, msg=None):
    """
    Функция возвращает атрибут ресурсного описания. Если атрибут вычисляемый,
    то она вычисляет его. Вычисляемый атрибут определяется по счиволу '@'. Считается,
    что нужный ключ у ресурса существует.
    @param res: Ресурсное описание компонента.
    @type res: C{dictionary}
    @param key: Имя атрибута.
    @type key: C{string}
    @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
    @type evalSpace: C{dictionary}
    @return: Возвращает значение атрибута.
    """
    if msg is None:
        msg = 'ERROR in getSpcAttr() key=<%s>, name=%s' % (key, res['name'])

    compileKey = None
    if '_uuid' in res and res['_uuid']:
        compileKey = res['_uuid']+key

    return getICAttr(res[key], evalSpace, msg, compileKey)


def getICAttr(attr_val, evalSpace=None, msg=None, compileKey=None):
    """
    Функция вычисляет значение атрибута. Если атрибут вычисляемый,
    то она вычисляет его. Вычисляемый атрибут определяется по счиволу '@'.
    @param attr_val: Не вычесленный атрибут.
    @type attr_val: C{dictionary}
    @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
    @type evalSpace: C{dictionary}
    @type msg: C{string}
    @param msg: Сообщение, которое дополнительно выводится при ошибке. Если параметр None,
        то сообщение об ошибке не выводится.
    @return: Возвращает значение атрибута. None - если произошла ошибка при
        вычислении атрибута.
    """
    if type(attr_val) not in (str, unicode):
        return attr_val

    try:
        if attr_val[0] == '@':
            if msg == '':
                msg = 'ERROR in countAttr() val=<%s>' % attr_val

            ret, val = ic_eval(attr_val[1:], 0, evalSpace, msg, compileKey=compileKey)
            if ret:
                return val
            else:
                return None
    except:
        pass

    return attr_val


def setFocusToForm(evalSpace, bFocus=True):
    """
    Устанавливает фокус на первую попавшуюся форму из пространства имен.
    """
    try:
        for key, obj in evalSpace['_dict_obj'].items():
            if obj.type in ['Frame', 'Dialog']:
                io_prnt.outLog('___ setFocusToForm: %s' % obj.name)
                obj.Enable(True)
                obj.SetFocus()
                break
    except:
        io_prnt.outLog('___ setFocusToForm ERROR')


def test1():
    spc1 = {'name': '1',
            'type': 't1',
            's1': None,
            'p1': None,
            '__styles__': {'ss1': 1},
            '__parent__': None,
            '__lists__': {'nest': []},
            '__events__': {'s1': [],
                           'p1': []},
            '__attr_types__': {1: ['s1', 'p1']}}

    spc2 = {'name': '2',
            'type': 't2',
            's1': None,
            'p2': None,
            'q2': None,
            '__styles__': {'ss2': 1},
            '__lists__': {'nest': [15, 16, 17]},
            '__parent__': spc1,
            '__events__': {'p2': [],
                           'q2': []},
            '__attr_types__': {1: ['s1'],
                               2: ['p2', 'q2']}}

    spc3 = {'name': '3',
            'type': 't3',
            'ss1': None,
            'pp1': None,
            '__styles__': {'ss3': 1},
            '__parent__': spc2,
            '__events__': {'ss1': [],
                           'pp1': []},
            '__attr_types__': {1: ['ss1', 'pp1']}}

    spc = icSpcDefStruct(spc3, spc3, True)
    spc = icSpcDefStruct(spc3, spc3, True)
    print('>>> spc=')
    spc.pop('__parent__')
    print(spc)

_SS = '''
def test2(s):
    if not s:
        return
    pos = 0
    ns = ''
    repl = 'globals().update(locals());return'

    while pos <> -1:
        pos = s.find('return ', pos)

        if pos > 0:
            if s[pos-1] in ('\n',' '):
                s = s[pos] + repl + s[pos+7]
                pos += len(repl)

    return s'''


def test2(s):
    return replReturn(s)


def test3():
    import time

    t1 = time.clock()
    for x in xrange(1000):
        s = test2(_SS)

    t2 = time.clock()
    print(s)
    print('TIME-0:', t2-t1)

    t1 = time.clock()
    for x in xrange(1000):
        s = _SS.replace(' return', 'globals().update(locals());return')
        s = _SS.replace('\nreturn', 'globals().update(locals());return')
        s = _SS.replace('return;', 'globals().update(locals());return')
        s = _SS.replace(';return', 'globals().update(locals());return')
        s = _SS.replace('return ', 'globals().update(locals());return')

    t2 = time.clock()
    print(s)
    print('TIME-1:', t2-t1)
    pass


if __name__ == '__main__':
    """
    Тестируем модуль.
    """
    test1()
