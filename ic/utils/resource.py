# ! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль функций работы с ресурсными файлами системы.
"""

# Подключение библиотек
import time
import datetime
import os
import os.path
import copy
import wx

from ic.dlg import ic_dlg
from ic.log import log
from ic.imglib import common
from . import lock
from ic.kernel import io_prnt
import ic.PropertyEditor.icDefInf as icDefInf
import ic.storage.storesrc
from . import util
from ic.engine import ic_user

_ = wx.GetTranslation

#   Указатель на пользовательское хранилище
isUserObjectStorage = None

__version__ = (1, 0, 1, 2)

IC_DOC_PATH = '%s%sic%sdoc%shtml' % (os.getcwd(), os.sep, os.sep, os.sep)

# Функции определения ресурсных файлов системы


def icGetKernel():
    """
    Возвращает ссылку на ядро системы.
    """
    return ic_user.getKernel()


def icGetResPath():
    """
    Возвращает путь до директории, где располагаются ресурсные файлы
    """
    return ic_user.icGet('SYS_RES')


def icGetSysPath():
    """
    Возвращает путь до папки системы.
    """
    pth = icGetResPath()
    if pth:
        pth = pth.replace('\\', '/')
        lst = pth.split('/')
        if lst[-1]:
            return '/'.join(lst[:-1])
        else:
            return '/'.join(lst[:-2])


def icGetSubsys():
    """
    Возвращает имя текущей подсистемы.
    """
    pth = icGetResPath()
    if pth:
        pth = pth.replace('\\', '/')
        lst = pth.split('/')
        if lst[-1]:
            return lst[-1]
        else:
            return lst[-2]


def IsDebugMode():
    """
    Признак режима отладки.
    """
    if ic_user.icIs('DEBUG_MODE'):
        return ic_user.icGet('DEBUG_MODE')
    else:
        return False


def icGetUserPath():
    """
    Возвращает путь до директории пользователя.
    """
    userName = ic_user.icGet('UserName')
    path = icGetResPath()
    if not userName:
        return None

    res = icGetRes(userName, 'acc', path, nameRes='users')
    if res:
        user_path = res['local_dir']
        return user_path

    return None


def icSetUserVariable(varName, value, subsys='', bClose = False):
    """
    Функция устанавливает переменную пользователя.
    @type varName: C{string}
    @param varName: Имя переменной.
    @type value: C{string}
    @param value: Значение переменной.
    @type subsys: C{string}
    @param subsys: Имя подсистемы
    """
    global isUserObjectStorage
    res_path = icGetUserPath()
    if not res_path:
        return None

    #   По необходимости создаем хранилище
    if not isUserObjectStorage:
        isUserObjectStorage = storage = ic.storage.storesrc.icTreeDirStorage(res_path)
        storage.Open()
    else:
        storage = isUserObjectStorage

    keyObj = lock.GetMyHostName()+'Property'
    #   По необходимости создаем файл
    # ВНИМАНИЕ! При работе с хранилищем используем исключительно функцию
    # наличия ключа <has_key> т.к. она определена в классе
    if keyObj not in storage:
        storage[keyObj] = ic.storage.storesrc.icFileStorage()

    storage[keyObj][varName] = value
    if bClose:
        storage.save()
        storage.Close()
        isUserObjectStorage = None

    return True


def icCloseLocalStorage():
    """
    Закрывает и сохраняет локальное хранилище.
    """
    global isUserObjectStorage
    if isUserObjectStorage:
        isUserObjectStorage.save()
        isUserObjectStorage.Close()
        log.info('*** save and close local storage ***')


def icGetUserVariable(varName, subsys='', bClose = False):
    """
    Функция устанавливает переменную пользователя.
    @type varName: C{string}
    @param varName: Имя переменной.
    @type value: C{string}
    @param value: Значение переменной.
    @type subsys: C{string}
    @param subsys: Имя подсистемы.
    """
    global isUserObjectStorage
    res_path = icGetUserPath()
    if not res_path:
        return None
    #   По необходимости создаем хранилище
    if not isUserObjectStorage:
        isUserObjectStorage = storage = ic.storage.storesrc.icTreeDirStorage(res_path)
        storage.setCache()
        storage.Open()
    else:
        storage = isUserObjectStorage

    keyObj = lock.GetMyHostName()+'Property'
    result = None
    #   По необходимости создаем файл
    # ВНИМАНИЕ! При работе с хранилищем используем исключительно функцию
    # наличия ключа <has_key> т.к. она определена в классе
    if keyObj in storage and varName in storage[keyObj]:
        result = storage[keyObj][varName]

    if bClose:
        storage.Close()
        isUserObjectStorage = None

    return result


def icGetCfgFrame():
    """
    Возвращает путь до директории, где располагаются ресурсные файлы.
    """
    appx = ic_user.icRef('CFG_APP')
    return appx.appFrame


def icGetSubsysResPaths():
    """
    Возвращает список путей до всех подсистем.
    """
    paths = ic_user.icGet('SUBSYS_RES')
    if not paths:
        paths = [icGetResPath()]

    return paths


def icGetICPath():
    """
    Возвращает путь до пакета ic.
    """
    return common.icpath


def icGetUserClassesPath():
    return icGetICPath()+'/components/user'


def icGetHlpPath():
    """
    Возвращает путь до директории, где располагаются файлы документации.
    """
    return IC_DOC_PATH

def icGetResFileName(Ext_='tab'):
    """
    Ресурсный файл.
    @return: Функцмя возвращает полное имя ресурсного файла по его расширению.
    """
    res_file = icGetResPath()+'resource.'+Ext_
    res_file = res_file.replace('\\', '/')
    print(res_file)
    return res_file


def inherit(prnt_res, resource, lstExcept=[]):
    """
    Наследуем атрибуты родительского описания.
    @type prnt_res: C{dictionary}
    @param prnt_res: Родительское описание.
    @type resource: C{dictionary}
    @param resource: Описание потомка.
    @type lstExcept: C{list}
    @param lstExcept: Список не наследуемых атрибутов.
    @rtype: C{dictionary}
    @return: Возвращает наследованное ресурсное описание.
    """
    for key, attr in resource.items():
        if key not in lstExcept and not attr and key in prnt_res:
            resource[key] = prnt_res[key]

    return resource


def inheritDataClass(prnt_res, resource):
    """
    Функция наследования ресурсных описаний классов данных.
    @type prnt_res: C{dictionary}
    @param prnt_res: Родительское описание.
    @type resource: C{dictionary}
    @param resource: Описание потомка.
    @rtype: C{dictionary}
    @return: Возвращает наследованное ресурсное описание класса данных.
    """
    #   Наследуем атрибуты родительского класса данных
    inherit(prnt_res, resource, ['parent'])

    #   Наследуем описания полей
    #   1. Создаем словарь схемы дочернего ресурса
    res_dict = {}
    for fld in resource['scheme']:
        res_dict[fld['name']] = fld

    for fld in prnt_res['scheme']:
        #   Если имена совпали, то используем наследование
        if fld['name'] in res_dict.keys():
            inherit(fld, res_dict[fld['name']])
        #   В противном случае добавляем описание поля в схему
        else:
            resource['scheme'].append(fld)

    return resource


def buildDataClassRes(resource, nameRes='resource'):
    """
    Собирает ресурсное описание класса данных с испольозованием механизма
    наследования.
    @type resource: C{dictionary}
    @param resource: Ресурсное описание без наследования.
    @type nameRes: C{string}
    @param mameRes: Имя ресурсного файла. Если оно не указано, то используется 'resource'. В
        старых версиях все ресурсы одного типа хранились в одном файле, поэтому этот параметр не
        использовался.
    """
    if isinstance(resource, dict) or 'parent' not in resource:
        return resource
    #   Организуем наследование классов данных
    prnt_name = resource['parent']
    tableName = None
    while prnt_name:
        #   Выделяем имя подсистемы
        if '/' in prnt_name:
            subsys, clsName = prnt_name.split('/')
            subsys_path = getSubsysPath(subsys)
            prnt_res = icGetRes(clsName, 'tab', subsys_path, bCopy=True, nameRes=nameRes)
        else:
            prnt_res = icGetRes(prnt_name, 'tab', bCopy=True, nameRes=nameRes)

        if prnt_res:
            if not tableName and resource['type'] == 'icQuery' and prnt_res['type'] == 'icDataClass':
                tableName = prnt_res['name']
            resource = inheritDataClass(prnt_res, resource)
            prnt_name = prnt_res['parent']
        else:
            break

    #   Для запроосов в атрибут 'parent' записываем имя класса данных, от которого наследуется
    #   запрос. Для классов данных None.
    resource['parent'] = tableName
    return resource


def icGetRes(className, ext='tab', pathRes=None, bCopy=True, bRefresh=False, nameRes='resource'):
    """
    Возврвщает ресурсное описание объекта. После того как функция находит
    нужное ресурсное описание в служебном атрибуте ресурса '__file_res' прописывается
    полный путь до файла ресурса, где он был найден.
    @type className: C{string}
    @param className: Имя ресурса.
    @type ext: C{string}
    @param ext: Расширения ресурсного файла для данного ресурса.
    @type pathRes: C{string}
    @param pathRes: Имя ресурсного файла. Если путь не указан, то нужный ресурсный файл
        последовательно ищется во всех папках подсистем, начиная с папки текущего проекта.
    @type bCopy: C{bool}
    @param bCopy: Признак указывающий, что надо возвращать копию ресурса, в противном
        случае возвращается указатель на ресурс. Поскольку он буферезируется то
        с ним необходимо очень акуратно работать.
    @type bRefresh: C{bool}
    @param bRefresh: Признак того, что ресурс надо перечитать даже если он
        буферезирован.
    @type nameRes: C{string}
    @param nameRes: Имя ресурсного файла. Если оно не указано, то используется 'resource'. В
        старых версиях все ресурсы одного типа хранились в одном файле, поэтому этот параметр не
        использовался.
    @rtype: C{dictionary}
    @return: Ресурсное описание объекта. None если ресурс не найден.
    """
    if not pathRes:
        paths = icGetSubsysResPaths()
    else:
        paths = [pathRes]

    #   Перебираем все пути подсистем
    resource_data = None
    sp_ok = ' '*3+'[+] '
    sp_f = ' '*3+'[-] '
    for pathRes in paths:
        fileRes = os.path.join(pathRes, nameRes+'.'+ext)    # .replace('\\', '/').replace('//', '/')
        if os.path.isfile(fileRes):
            #   Читаем ресурсное описание
            res = util.readAndEvalFile(fileRes, bRefresh=bRefresh)
            try:
                if bCopy and className:
                    if className not in res:
                        bFindRes = False
                        for val in res.values():
                            if val['name'] == className:
                                resource_data = copy.deepcopy(val)
                                bFindRes = True
                                break
                        if not bFindRes:
                            raise KeyError, className
                    else:
                        resource_data = copy.deepcopy(res[className])
                elif className:
                    resource_data = res[className]
                #   Если имя ресурса не указано, берется корневой элемент
                elif bCopy:
                    resource_data = copy.deepcopy(res.values()[0])
                else:
                    resource_data = res.values()[0]

                #   Организуем наследование классов данных
                if ext == 'tab':
                    resource_data = buildDataClassRes(resource_data)

                #   Прописываем в ресурсе имя файла
                resource_data['__file_res'] = fileRes
                return resource_data
            except KeyError:
                io_prnt.outWarning(sp_f + (_('icGetRes: component <%s> is not found in resource <%s>.') % (className,
                                                                                                           fileRes)))
        else:
            io_prnt.outWarning(sp_f + (_('icGetRes: resource file <%s> is not found.') % fileRes))

    ic_dlg.icWarningBox(u'ОШИБКА', u'icGetRes: Компонент <%s> не найден в ресурсном файле.' % className)
    return None


def getResFilesByType(ext='tab', pathRes=None):
    """
    Получить список файлов по типу.
    @type ext: C{string}
    @param ext: Расширения ресурсного файла для данного ресурса.
    @type pathRes: C{string}
    @param pathRes: Имя ресурсного файла. Если путь не указан, то нужный ресурсный файл
        последовательно ищется во всех папках подсистем, начиная с папки текущего проекта.
    @return: Возвращает список полных имен ресурсных файлов с заданным расширением.
    """
    result = []
    ext = ext.lower()
    if not pathRes:
        paths = icGetSubsysResPaths()
    else:
        paths = [pathRes]

    for pathRes in paths:
        path_res = (pathRes+'/').replace('\\', '/').replace('//', '/')
        file_names=os.listdir(pathRes)
        full_file_res_name = [path_res+file_name for file_name in file_names if os.path.splitext(file_name)[1][1:].lower() == ext]
        result = result+full_file_res_name
    # Отфильтровываем откомпилированные ресурсы

    res = []
    pr = '_pkl.%s' % ext
    for el in result:
        if pr in el:
            el2 = el.replace(pr, '.%s' % ext)
            if el2 not in result:
                res.append(el2)
        else:
            res.append(el)
    return res


def getResourcesByType(ext='tab', pathRes=None, bRefresh=False):
    """
    Получить список ресурсов по типу.
    @type ext: C{string}
    @param ext: Расширения ресурсного файла для данного ресурса.
    @type pathRes: C{string}
    @param pathRes: Имя ресурсного файла. Если путь не указан, то нужный ресурсный файл
        последовательно ищется во всех папках подсистем, начиная с папки текущего проекта.
    @type bRefresh: C{bool}
    @param bRefresh: Признак того, что ресурс надо перечитать даже если он
        буферезирован.
    @return: Возвращает словарь {имя ресурсного файла:содержимого ресурсного файла} с заданным расширением.
    """
    res_file_names = getResFilesByType(ext, pathRes)
    # Отфильтровать переопределенные ресурсы
    filter_res_file_names = []
    for file_name in res_file_names:
        if os.path.basename(file_name) not in \
           [os.path.basename(res_file_name) for res_file_name in filter_res_file_names]:
            filter_res_file_names.append(file_name)

    return dict([(res_file_name, util.readAndEvalFile(res_file_name,
                                                      bRefresh=bRefresh)) for res_file_name in filter_res_file_names])


def RefreshResUUID(res, prnt_res, new_uuid):
    """
    Обновляет UUID ресурса. Для некоторых ресурсов (GridCell) обновление надо проводить в
    родительском ресурсе, так как они описывают один состовной объект.
    @type res: C{dictionary}
    @param res: Ресурсное описание компонента.
    @type prnt_res: C{dictionary}
    @param prnt_res: Ресурсное описание родительского компонента.
    @type new_uuid: C{string}
    @param new_uuid: Новый uuid компонента.
    """
    if res['type'] == 'GridCell' and prnt_res:
        prnt_res['_uuid'] = new_uuid
    else:
        res['_uuid'] = new_uuid


def delResServiceInfo(res):
    """
    Удаляет служебную информацию из ресурса.
    """
    if not res or isinstance(res, dict):
        return False
    for key, val in res.items():
        if key.startswith('__'):
            res.pop(key)
        elif key in ['cell_attr', 'label_attr'] and isinstance(val, dict):
            delResServiceInfo(val)
        elif key in ['child', 'win1', 'win2', 'cols'] and isinstance(val, list):
            for el in val:
                delResServiceInfo(el)
        elif key in ['win1', 'win2'] and isinstance(val, dict):
            delResServiceInfo(val)


def genNextVersion(version=None):
    """
    По старой версии генерирует новую.
    """
    if version:
        lst = list(version)
        ver = reduce(lambda x,y: x*10+y, lst)
        return [int(s) for s in str(ver+1)]
    else:
        return 1, 0, 0, 1


def genClassFromRes(className, res, version=None):
    """
    Генерирует класс по ресурсу.
    """
    #   Удаляем служебную информацию
    delResServiceInfo(res)
    version = genNextVersion(version)
    class_txt = u'''#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.interfaces.icobjectinterface as icobjectinterface

### !!!! NO CHANGE !!!!
###BEGIN SPECIAL BLOCK

#   Object resource
resource = %s

#   Object version
__version__ = %s
###END SPECIAL BLOCK

#   Class name
ic_class_name = '%s'


class %s(icobjectinterface.icObjectInterface):
    def __init__(self, parent):
        \"\"\"
        Constructor.
        \"\"\"
        #

        #   Base class constructor
        icobjectinterface.icObjectInterface.__init__(self, parent, resource)

    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK


def test(par=0):
    \"\"\"
    Test %s class.
    \"\"\"

    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)

    #
    # Test code
    #

    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
'''
    class_txt = class_txt % (res, str(version), className, className, className)
    return class_txt


def MyExec(s):
    exec s


def genResModuleHead(rn, fn, descr=_('Resource module'), ver=u'(0, 0, 0, 1)'):
    """
    Генерирует заголовок модуля ресурса.
    """
    mngr = 'ResObjectManager'
    mod_txt = u'''#!/usr/bin/env python
# -*- coding: utf-8 -*-

\"\"\"
Resource module <%s>
File            <%s>
Description     <%s>
\"\"\"

from ic.interfaces import icmanagerinterface

### RESOURCE_MODULE: %s

### ---- Import external modules -----
### RESOURCE_MODULE_IMPORTS

#   Version
__version__ = %s


class %s(icmanagerinterface.icWidgetManager):

    def onInit(self, evt):
        pass

    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK

manager_class = %s
''' % (rn, fn, descr, rn, ver, mngr, mngr)
    return mod_txt.encode('utf-8')


def genObjModuleHead(on, fn, descr=_('Object module'), ver=u'(0, 0, 0, 1)'):
    """
    Генерирует заголовок модуля объекта.
    @param on: Имя объекта.
    @param fn: Путь до модуля.
    @param descr: Описание объекта.
    @param ver: Версия.
    """
    st = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y')
    mod_txt = u'''#!/usr/bin/env python
# -*- coding: utf-8 -*-

\"\"\"
Object module   <%s>
File            <%s>
Description     <%s>
\"\"\"

#   Version
__version__ = %s
''' % (on, fn, descr, st, ver)
    return mod_txt.encode('utf-8')


def getICObjectResource(path):
    """
    Возвращает ресурсное описание и имя класса системного объекта.
    """
    try:
        #   Импортируем модуль
        mod = util.icLoadSource('modulRes', path)
        res = mod.resource
        #   Читаем имя класса
        try:
            className = mod.ic_class_name
        except:
            className = 'icObjectClass'
        #   Читаем версию
        try:
            version = mod.__version__
        except:
            version = (1, 0, 0, 1)

        del mod

        if isinstance(res, dict):
            return res, className, version
    except:
        io_prnt.outErr(_('Import module error: %s') % path)

    return None, None, None


def saveICObject(path, className, res):
    """
    Генерирует по ресурсу питоновский класс и сохраняет в нужном модуле.
    @type path: C{string}
    @param path: Путь до файла.
    @type className: C{string}
    @param className: Имя класса.
    @type res: C{dictionary}
    @param res: Ресурсное описание.
    """
    text = genClassFromRes(className, res)
    file = open(path, 'w')
    file.write(text)
    file.close()


def updateICObject(path, className, res, version=None):
    """
    Обновляет ресурсное описание питоновского класса.
    @type path: C{string}
    @param path: Путь до файла.
    @type className: C{string}
    @param className: Имя класса.
    @type res: C{dictionary}
    @param res: Ресурсное описание.
    """
    #   Читаем текст файла
    file = open(path, 'rb')
    text = file.read()
    file.close()
    #   Обновляем текст
    version = genNextVersion(version)
    n1 = text.find('###BEGIN')
    n2 = text.find('###END')
    text = '''%s###BEGIN SPECIAL BLOCK
#   Resource description of class
resource = %s

#   Version
__version__ = %s
%s''' % (text[:n1], str(res), str(tuple(version)), text[n2:])

    file = open(path, 'wb')
    file.write(text)
    file.close()


def getSubsysPath(subsys=None):
    """
    Функция по имени подсистемы определяет полный путь до подсистемы.
    @type subsys: C{string}
    @param subsys: Имя подсистемы.
    """
    sys_path = icGetSubsysResPaths()[0].replace('\\', '/')
    if subsys:
        return '/'.join(sys_path.split('/')[:-1])+'/'+subsys
    else:
        return sys_path


def method(id_meth, subsys, esp=locals(), **params):
    """
    Находит и выполняет метод подсистемы.
    @type id_meth: C{string}
    @param id_meth: Идентификатор метода.
    @type subsys: C{string}
    @param subsys: Имя подсистемы.
    @type params: C{dict}
    @param params: Дополнительные параметры метода.
    """
    if subsys:
        subsys_path = getSubsysPath(subsys)
    else:
        subsys_path = None

    evalSpace = esp
    for par, val in params.items():
        evalSpace[par] = val

    meth_expr = icGetRes(id_meth, 'mth', subsys_path, False)

    if meth_expr and isinstance(meth_expr, dict) and 'body' in meth_expr:
        keyExpr = str(id_meth)+'_'+str(subsys)+'_method'
        ret, val = util.ic_eval(meth_expr['body'], 0, evalSpace,
                                '<method>=%s, <subsys>=%s' % (id_meth, subsys),
                                compileKey=keyExpr)
        if ret:
            return val

    elif subsys_path:
        io_prnt.outErr(_('Don\'t find method <%s> in subsystem %s.') % (id_meth, subsys))
    else:
        io_prnt.outErr(_('Don\'t find method <%s> in subsystems.') % id_meth)

    return None

# Форматы ресурса.
PICKLE_RES_FMT = 0
TEXT_RES_FMT = 1
from . import ic_res


def icSaveRes(className, ext, pathRes=None, nameRes='resource',
              resData=None, ResFmt=PICKLE_RES_FMT):
    """
    Сохранить ресурсное описание объекта.
    @type className: C{string}
    @param className: Имя ресурса.
    @type ext: C{string}
    @param ext: Расширения ресурсного файла для данного ресурса.
    @type pathRes: C{string}
    @param pathRes: Имя ресурсного файла. Если путь не указан, то ресурсный файл
        в папке текущего проекта.
    @type nameRes: C{string}
    @param nameRes: Имя ресурсного файла. Если оно не указано, то используется
        'resource'. В старых версиях все ресурсы одного типа хранились в одном
        файле, поэтому этот параметр не использовался.
    @type ResFmt: C{bool}
    @param ResFmt: Формат ресурса 0 - pickle, 1 - text.
    @rtype: C{dictionary}
    @return: Ресурсное описание объекта. None если ресурс не найден.
    """
    if not pathRes:
        pathRes = ic_user.icGet('PRJ_DIR')
    fileResName = (pathRes+'/'+nameRes+'.'+ext).replace('\\', '/').replace('//', '/')

    if ResFmt == PICKLE_RES_FMT:
        return ic_res.SaveResourcePickle(fileResName, {className: resData})
    elif ResFmt == TEXT_RES_FMT:
        return ic_res.SaveResourceText(fileResName, {className: resData})


def updateImporsObjModule(fn, imp_path):
    """
    Добавляет строку импорта на модуль объекта в модуль ресурса.
    @param fn: Имя модуля ресурса.
    @param imp_path: Имя модуля объекта.
    """
    # Читаем текст модуля
    fn = fn.replace('\\', '/')
    imp_path = imp_path.replace('\\', '/')
    f = open(fn, 'rb')
    text = f.read()
    f.close()
    n = text.find('### RESOURCE_MODULE_IMPORTS')
    if n < 0:
        n = text.find('### RESOURCE_MODULE:')

    p1, n1 = os.path.split(fn)
    p2, n2 = os.path.split(imp_path)

    subsys = icGetSubsys()
    if subsys:
        pack = '%s.%s' % (subsys, p2.replace(p1, '')[1:].replace('/', '.'))
    else:
        pack = p2.replace(p1, '')[1:].replace('/', '.')

    mod = n2.replace('.py', '')

    imp = 'from %s import %s' % (pack, mod)

    if n >= 0:
        text = text[:n] + imp + '\n' + text[n:]
    else:
        text = text + '\n' + imp

    file = open(fn, 'wb')
    file.write(text)
    file.close()


def _findres(res, nameObj, typeObj):
    """
    Ищет ресурс нужного объекта по дереву ресурса.
    @param res: Ресурсное описание.
    @param nameObj: Имя объекта.
    @param typeObj: Тип объекта.
    @return: Ресурсное описание найденного объекта.
    """
    if ((typeObj is None and res['name'] == nameObj) or
       (res['type'] == typeObj and res['name'] == nameObj)):
        return res

    optLst = list(set(res.keys()) & set(icDefInf.icContainerAttr))
    for key in optLst:
        if isinstance(res[key], list):
            for rs in res[key]:
                r = _findres(rs, nameObj, typeObj)
                if r:
                    return r
        elif isinstance(res[key], dict):
            r = _findres(res[key], nameObj, typeObj)
            if r:
                return r


def FindResInRes(res, nameObj, typeObj=None):
    """
    Ищет ресурс нужного объекта по дереву ресурса.
    @type res: C{dictionary}
    @param res: Ресурсное описание.
    @param res: Ресурс.
    @type nameObj: C{string}
    @param nameObj: Имя объекта.
    @type typeObj: C{string}
    @param typeObj: Тип объекта.
    @rtype: C{dictionary}
    @return: Ресурсное описание найденного объекта.
    """
    return _findres(res, nameObj, typeObj)


def find_child_resource(name, res):
    """
    Поиск ресурса дочернего объекта рекурсивно по имени.
    @param name: Имя дочернего объекта.
    @param res: Ресурс.
    @return: Словарь ресурса найденного объекта или None
        если не найдено.
    """
    if res['name'] == name:
        return res
    elif res['child']:
        find_res = None
        for child in res['child']:
            find_res = find_child_resource(name, child)
            if find_res is not None:
                return find_res
        return find_res
    return None


def update_child_resource(child_name, res, child_res):
    """
    Обновить ресурс дочернего объекта.
    @param child_name: Имя дочернего объекта.
    @param res: Ресурс.
    @return: Измененный словарь ресурса объекта или None
        если такой дочерний объект не найден.
    """
    if res['name'] == child_name:
        # Обновлять необходимо сам этот объект
        res.update(child_res)
        return res
    elif 'child' in res and res['child']:
        for i, child in enumerate(res['child']):
            new_res = update_child_resource(child_name, child, child_res)
            if new_res is not None:
                res['child'][i] = new_res
    return res


def getResByPsp(passport):
    """
    Возвращает ресурса объекта по его паспорту.
    @type passport: C{tuple}
    @param passport: идентификатор описания (паспорт) объекта.
    """
    res = None
    try:
        objType = passport[0][0]
        className = passport[0][1]
        resName, extName = os.path.basename(passport[0][3]).split('.')
        subsys = passport[0][4]
        res = icGetRes(resName, extName, pathRes=getSubsysPath(subsys), nameRes=resName)
        if res and objType:
            res_mod = res.get('res_module', None)
            file_res = res.get('__file_res')
            res = FindResInRes(res, className, objType)
            if res:
                res['res_module'] = res_mod
                res['__file_res'] = file_res
    except:
        log.fatal(u'Ошибка определения ресурса объекта по его паспорту %s' % passport)

    return res


if __name__ == '__main__':
    prnt_res = {'1': 1, '3': 3, 'scheme': [{'name': 1, 'p1': 1}, {'name': 2, 'p2': 'p'}]}
    resource = {'2': 22, '3': '', 'scheme': [{'name': 1, 'p1': ''}, {'name': 2}]}
    res = inheritDataClass(prnt_res, resource)
    print('RES:', res)
