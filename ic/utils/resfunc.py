#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль интерфейсных функций работы с файлом ресурсов.

@var DEFAULT_MENU_RES_FILE: Имя ресурсного файла движка по умолчанию
@var STRUCT_PADDING: Наполнитель позиций при отображении вложенности пунктов в структуре
"""

# Подключение библиотек
import os
import os.path
import wx
import pickle

from . import util
from . import filefunc

from . import toolfunc
from ic.log import log
from ic.engine import glob_functions
# Функции блокировки ресурсов
from . import lockfunc

__version__ = (0, 1, 1, 1)

_ = wx.GetTranslation

# Основные константы

# Образ ресурсного файла в памяти
CUR_MENU_RES_FILE_NAME = ''
CUR_MENU_RES_FILE = None

# Наполнитель позиций при отображении вложенности пунктов в структуре
STRUCT_PADDING = '    '

# Расширения ресурсных файлов
RES_EXT_MENU = '.mnu'
RES_EXT_ACCESS = '.acc'
RES_EXT_VAR = '.var'
RES_EXT_TABLE = '.tab'
RES_EXT_FORM = '.frm'
RES_EXT_WIN = '.win'
RES_EXT_CHOICE = '.svb'
RES_EXT_PRJ = '.pro'


def ReadAndEvalFile(FileName_, *args, **kwargs):
    """
    Загрузить информацию из файла ресурсов.
    @param FileName_: имя файла ресурсов.
    @return: Возвращает структуру Python определенную в виде текста в файле filename
    """
    return util.readAndEvalFile(FileName_, *args, **kwargs)


def openResFile(res_filename):
    """
    Загрузить информацию из файла ресурсов в память.
    @param res_filename: имя файла ресурсов.
    @return: Возвращает словарь Python из файла res_filename
    """
    global CUR_MENU_RES_FILE_NAME
    global CUR_MENU_RES_FILE
    CUR_MENU_RES_FILE_NAME = res_filename
    CUR_MENU_RES_FILE = ReadAndEvalFile(res_filename)
    return CUR_MENU_RES_FILE


def closeResFile():
    """
    Выгрузить информацию о файле ресурсов из памяти.
    """
    global CUR_MENU_RES_FILE_NAME
    global CUR_MENU_RES_FILE
    CUR_MENU_RES_FILE = None
    CUR_MENU_RES_FILE_NAME = ''


def loadObjStruct(Name_, ResFile_=''):
    """
    Загрузить атрибуты компонента из файла ресурсов в виде словаря(структуры).
    @param Name_:  имя объекта.
    @param ResFile_: имя ресурсного файла.
    @return: Возвращает атрибуты компонента в виде словаря
        или пустой словарь в случае ошибки.
    """
    from . import resource
    return resource.icGetRes(Name_,
                             os.path.splitext(ResFile_)[1][1:],
                             nameRes=os.path.splitext(ResFile_)[0])
    

_INIT_FILE_TXT_DEFAULT = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

\"\"\"

\"\"\"

# Version
__version__ = (0, 0, 0, 1)

'''


def createInitFile(Path_):
    """
    Создает файл __init__.py в директории path если его там нет.
    @return: Возвращает True, если файл был создан или уже есть.
    """
    if not Path_:
        return False

    try:
        os.makedirs(Path_)
    except:
        pass

    init_file = os.path.join(Path_, '__init__.py')
    if os.path.isfile(init_file):
        return True

    f = None
    try:
        f = open(init_file, 'wt')
        f.write(_INIT_FILE_TXT_DEFAULT)
        f.close()
        log.info(u'Создан файл <%s>' % init_file)
        return True
    except:
        log.fatal(u'Ошибка создания модуля <%s/__init__.py>' % Path_)
        if f:
            f.close()
        return False


def createPackage(PackageDir_):
    """
    Создать пакет. То же самое что и создать __init__ файл.
    """
    return createInitFile(filefunc.get_absolute_path(PackageDir_))


_PY_FILE_TXT_DEFAULT = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

\"\"\"

\"\"\"

# Version
__version__ = (0, 0, 0, 1)

# Functions
'''


def createPyFile(py_filename, py_file_body=None):
    """
    Создать файл питоновского модуля.
    @param py_filename: Имя файла *.py.
    @param py_file_body: Тело файла.
        Если None, то заполняется по умолчанию.
    @return: Возвращает True, если файл был создан или уже есть.
    """
    if os.path.isfile(py_filename):
        return True
    f = None
    try:
        try:
            os.makedirs(os.path.dirname(py_filename))
        except:
            pass
        f = open(py_filename, 'wt')
        if py_file_body is None:
            f.write(_PY_FILE_TXT_DEFAULT)
        else:
            f.write(str(py_file_body))
        f.close()
        log.info(u'Создан модуль Python <%s>' % py_filename)
        return True
    except:
        log.fatal(u'Create module error: %s' % py_filename)
        if f:
            f.close()
    return False


def loadResource(res_filename):
    """
    Получить ресурс в ресурсном файле.
    @param res_filename: Полное имя ресурсного файла.
    """
    res_filename = filefunc.get_absolute_path(res_filename)
    # Сначала предположим что файл в формате Pickle.
    struct = loadResourcePickle(res_filename)
    if struct is None:
        # Но если он не в формате Pickle, то скорее всего в тексте.
        struct = loadResourceText(res_filename)
    if struct is None:
        # Но если не в тексте но ошибка!
        log.warning(u'Не корректный формат файла: %s.' % res_filename)
        return None
    return struct


def loadResourcePickle(res_filename):
    """
    Получить ресурс из ресурсного файла в формате Pickle.
    @param res_filename: Полное имя ресурсного файла.
    """
    res_filename = filefunc.get_absolute_path(res_filename)
    if os.path.isfile(res_filename):
        f = None
        try:
            f = open(res_filename, 'rb')
            struct = pickle.load(f)
            f.close()
            return struct
        except:
            if f:
                f.close()
            log.fatal(u'Ошибка чтения файла ресурса <%s>' % res_filename)
            return None
    else:
        log.warning(u'Файл ресурса <%s> не найден' % res_filename)
        return None


def loadResourceText(res_filename):
    """
    Получить ресурс из ресурсного файла в текстовом формате.
    @param res_filename: Полное имя ресурсного файла.
    """
    res_filename = filefunc.get_absolute_path(res_filename)
    if os.path.isfile(res_filename):
        f = None
        try:
            f = open(res_filename, 'rt')
            txt = f.read().replace('\r\n', '\n')
            f.close()
            return eval(txt)
        except:
            if f:
                f.close()
            log.fatal(u'Ошибка чтения файла ресурса <%s>' % res_filename)
            return None
    else:
        log.warning(u'Файл ресурса <%s> не найден' % res_filename)
    return None


def saveResourcePickle(res_filename, resource_data):
    """
    Сохранить ресурс в файле в формате Pickle.
    @param res_filename: Полное имя ресурсного файла.
    @param resource_data: Словарно-списковая структура спецификации.
    @return: Возвращает результат выполнения операции True/False.
    """
    res_filename = filefunc.get_absolute_path(res_filename)
    f = None
    try:
        # Если необходимые папки не созданы, то создать их
        dir_name = os.path.dirname(res_filename)
        try:
            os.makedirs(dir_name)
        except:
            pass

        f = open(res_filename, 'wb')
        pickle.dump(resource_data, f)
        f.close()
        log.info(u'Файл <%s> записан в pickle формате.' % res_filename)
        return True
    except:
        log.fatal(u'Ошибка записи файла <%s> в pickle формате.' % res_filename)
        if f:
            f.close()
    return False


def saveResourceText(res_filename, resource_data, bToStruct=False):
    """
    Сохранить ресурс в файле в текстовом формате.
    @param res_filename: Полное имя ресурсного файла.
    @param resource_data: Словарно-списковая структура спецификации.
    @param bToStruct: Сохранить в структурном виде ресурс?
    @return: Возвращает результат выполнения операции True/False.
    """
    res_filename = filefunc.get_absolute_path(res_filename)
    f = None
    try:
        # Если необходимые папки не созданы, то создать их
        dir_name = os.path.dirname(res_filename)
        try:
            os.makedirs(dir_name)
        except:
            pass

        f = open(res_filename, 'wt')
        if bToStruct:
            text = toolfunc.StructToTxt(resource_data)
        else:
            text = str(resource_data)
        f.write(text)
        f.close()
        log.info(u'Ресурс сохранен в файле <%s> в текстовом формате' % res_filename)
        return True
    except:
        log.fatal(u'Ошибка сохранения ресурса в текстовом формате в файле <%s>' % res_filename)
        if f:
            f.close()
        return False


def isPackage(dir_path):
    """
    Проверка является ли директория пакетом.
    @param dir_path: Указание директории.
    @return: Возвращает True/False.
    """
    is_dir = os.path.isdir(dir_path)
    is_init_file = False
    if is_dir:
        is_init_file = os.path.exists(os.path.join(dir_path, '__init__.py'))
    return bool(is_dir and is_init_file)
    

def lockRes(res_name, res_filename, res_file_ext, lock_dir=None):
    """
    Заблокировать ресурс.
        Имя файла блокировки гонерируется 
        как ИмяРесурса_ИмяФайлаРесурса_РасширениеФайлаРесурса.lck.
        В файл блокировки записывается информация о владельце блокировки 
        в виде словаря {'computer':Имя хоста с которого заблокировался ресурс}.
    @param res_name: Имя ресурса. 
        Если имя ресурса None, то блокируется файл ресурса целиком.
    @param res_filename: Имя файла ресурса.
    @param res_file_ext: Расширение файла ресурса/тип ресурса.    
    @param lock_dir: Папка блокировок.
    """
    if lock_dir is None:
        lock_dir = lockfunc.getLockDir()
        try:
            os.makedirs(lock_dir)
        except:
            pass
    if res_name is None:
        res_name = res_filename
        
    lock_file = os.path.join(lock_dir,
                             '%s_%s_%s%s' % (res_name.strip(),
                                             res_filename.strip(),
                                             res_file_ext.strip(),
                                             lockfunc.LOCK_FILE_EXT))
    comp_name = lockfunc.ComputerName()
    user_name = glob_functions.getVar('UserName')
    log.info(u'Блокировка ресурса <%s>' % lock_file)
    return lockfunc.LockFile(lock_file, u'{\'computer\':\'%s\',\'user\':\'%s\'}' % (comp_name,
                                                                                    user_name))


def unlockRes(res_name, res_filename, res_file_ext, lock_dir=None):
    """
    Разблокировать ресурс. Ресурс м.б. разблокирован только с хоста-владельца.
    @param res_name: Имя ресурса. 
    @param res_filename: Имя файла ресурса.
    @param res_file_ext: Расширение файла ресурса/тип ресурса.    
    @param lock_dir: Папка блокировок.
    """
    if lock_dir is None:
        lock_dir = lockfunc.getLockDir()
        os.makedirs(lock_dir)
    if res_name is None:
        res_name = res_filename
        
    lock_file = os.path.join(os.path.normpath(lock_dir),
                             '%s_%s_%s%s' % (res_name.strip(),
                                             res_filename.strip(),
                                             res_file_ext.strip(),
                                             lockfunc.LOCK_FILE_EXT))
    user_name = glob_functions.getCurUserName()
    log.info(u'Снятие блокировки ресурса <%s> : <%s>' % (lock_file, user_name))
    return lockfunc.UnLockFile(lock_file, user=user_name)


def isLockRes(res_name, res_filename, res_file_ext, lock_dir=None):
    """
    Проверить заблокирован ли ресурс.
    @param res_name: Имя ресурса. 
    @param res_filename: Имя файла ресурса.
    @param res_file_ext: Расширение файла ресурса/тип ресурса.    
    @param lock_dir: Папка блокировок.
    """
    if lock_dir is None:
        lock_dir = lockfunc.getLockDir()
        os.makedirs(lock_dir)
    if res_name is None:
        res_name = res_filename
        
    # Кроме проверки блокировки ресурса необходимо проверить блокировку файла ресурса
    lock_file = os.path.join(os.path.normpath(lock_dir),
                             '%s_%s_%s%s' % (res_filename.strip(),
                                             res_filename.strip(),
                                             res_file_ext.strip(),
                                             lockfunc.LOCK_FILE_EXT))
        
    lock_res = os.path.join(os.path.normpath(lock_dir),
                            '%s_%s_%s%s' % (res_name.strip(),
                                            res_filename.strip(),
                                            res_file_ext.strip(),
                                            lockfunc.LOCK_FILE_EXT))
        
    is_lock_file = lockfunc.IsLockedFile(lock_file)
    is_lock_res = lockfunc.IsLockedFile(lock_res)
    is_lock = False
    if is_lock_file or is_lock_res:
        log.info(u'Ресурс заблокирован <%s> : [%s : %s]' % (lock_file, is_lock_file, is_lock_res))
            
        # Если файл блокировки есть, то
        # проверить кем он заблокирован
        if is_lock_file:
            is_lock_file = bool(getLockResOwner(res_filename, res_filename,
                                                res_file_ext, lock_dir) != glob_functions.getCurUserName())
        
        # Если файл блокировки есть, то
        # проверить кем он заблокирован
        if is_lock_res:
            is_lock_res = bool(getLockResOwner(res_name, res_filename,
                                               res_file_ext, lock_dir) != glob_functions.getCurUserName())
        is_lock = is_lock_file or is_lock_res
    return is_lock


def delAllLockRes(lock_dir):
    """
    Удалить все файлы блокировок ресурсов данного хоста из папки блокировок.
    @param lock_dir: Папка блокировок.
    """
    if lock_dir is None:
        lock_dir = lockfunc.getLockDir()
        os.makedirs(lock_dir)
    return lockfunc.UnLockAllFile(lock_dir)


def getLockResOwner(res_name, res_filename, res_file_ext, lock_dir=None):
    """
    Определить владельца блокировки ресурса.
    """
    if lock_dir is None:
        lock_dir = lockfunc.getLockDir()
        os.makedirs(lock_dir)
    if res_name is None:
        res_name = res_filename
        
    lock_file = os.path.join(lock_dir,
                             '%s_%s_%s%s' % (res_name, res_filename,
                                             res_file_ext, lockfunc.LOCK_FILE_EXT))
    lock_record = lockfunc.ReadLockRecord(lock_file)
    lock_user = lock_record.get('user', u'Не определен') if lock_record else u'Не определен'
    log.info(u'Владелец <%s> заблокированного ресурса <%s>' % (lock_user, lock_file))
    return lock_user


def getLockResRecord(res_name, res_filename, res_file_ext, lock_dir=None):
    """
    Определить запись блокировки ресурса.
    """
    if lock_dir is None:
        lock_dir = lockfunc.getLockDir()
        os.makedirs(lock_dir)
    if res_name is None:
        res_name = res_filename
        
    lock_file = os.path.join(lock_dir,
                             '%s_%s_%s%s' % (res_name, res_filename,
                                             res_file_ext, lockfunc.LOCK_FILE_EXT))
    return lockfunc.ReadLockRecord(lock_file)


def getNewID():
    """
    Генерация нового идентификатора для ресурса.
    """
    return '_'+str(wx.NewId())


def findSpcInResource(name, resource_data):
    """
    Найти спецификацию в ресурсе по имени.
    @param name: Имя спецификации.
    @param resource_data: Дерево ресурсов.
    @return: Возвращает искомую спецификацию или None, если
        спецификация не найдена.
    """
    if isinstance(resource_data, list):
        for spc in resource_data:
            find_spc = findSpcInResource(name, spc)
            if find_spc:
                return find_spc
    elif isinstance(resource_data, dict):
        if resource_data['name'] == name:
            return resource_data
        # Поиск в дочерних элементах
        if 'child' in resource_data:
            return findSpcInResource(name, resource_data['child'])
        
    # Спецификация не найдена
    return None
