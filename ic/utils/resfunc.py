#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль интерфейсных функций работы с файлом ресурсов.

@var DEFAULT_MENU_RES_FILE: Имя ресурсного файла движка по умолчанию
@var STRUCT_PADDING: Наполнитель позиций при отображении вложенности пунктов в структуре
"""

# Подключение библиотек
import os
import os.path

try:
    import wx
except ImportError:
    print('Import Error wx')
    wx = None

try:
    from types import *
except ImportError:
    print('Import Error types')

try:
    import cPickle
except ImportError:
    print('Import Error cPickle')
    cPickle = None


from . import util
from ic.log import log
from . import ic_util
from . import resource
from . import lock

__version__ = (0, 0, 0, 5)

# === Основные константы ===

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


def ReadAndEvalFile(FileName_):
    """
    Загрузить информацию из файла ресурсов.
    @param FileName_: имя файла ресурсов.
    @return: Возвращает структуру Python определенную в виде текста в файле FileName_
    """
    return util.readAndEvalFile(FileName_)


def icOpenResFile(ResFileName_):
    """
    Загрузить информацию из файла ресурсов в память.
    @param ResFileName_: имя файла ресурсов.
    @return: Возвращает словарь Python из файла ResFileName_
    """
    global CUR_MENU_RES_FILE_NAME
    global CUR_MENU_RES_FILE
    CUR_MENU_RES_FILE_NAME = ResFileName_
    CUR_MENU_RES_FILE = ReadAndEvalFile(ResFileName_)
    return CUR_MENU_RES_FILE


def icCloseResFile():
    """
    Выгрузить информацию о файле ресурсов из памяти.
    """
    CUR_MENU_RES_FILE = None
    CUR_MENU_RES_FILE_NAME = ''


def LoadObjStruct(Name_, ResFile_=''):
    """
    Загрузить атрибуты компонента из файла ресурсов в виде словаря(структуры).
    @param Name_:  имя объекта.
    @param ResFile_: имя ресурсного файла.
    @return: Возвращает атрибуты компонента в виде словаря
        или пустой словарь в случае ошибки.
    """
    return resource.icGetRes(Name_,
                             os.path.splitext(ResFile_)[1][1:],
                             nameRes=os.path.splitext(ResFile_)[0])
    

_InitFileDefault = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-
\"\"\"
Пакет прикладной системы.
\"\"\"

# Версия
__version__ = (0, 0, 0, 1)

'''


def CreateInitFile(Path_):
    """
    Создает файл __init__.py в директории Path_ если его там нет.
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
        f = open(init_file, 'w')
        f.write(_InitFileDefault)
        f.close()
        log.info(u'Создан файл: <%s>.' % init_file)
        return True
    except:
        if f:
            f.close()
        log.fatal(u'Ошибка создания модуля %s/__init__.py %s' % Path_)
        return False


def CreatePackage(PackageDir_):
    """
    Создать пакет. То же самое что и создать __init__ файл.
    """
    return CreateInitFile(os.path.abspath(PackageDir_))


_PyFileDefault = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-
\"\"\"
Модуль прикладной системы.
\"\"\"

# Версия
__version__ = (0, 0, 0, 1)

# --- Функции ---
'''


def CreatePyFile(PyFileName_, PyFileBody_=None):
    """
    Создать файл питоновского модуля.
    @param PyFileName_: Имя файла *.py.
    @param PyFileBody_: Тело файла. 
        Если None, то заполняется по умолчанию.
    @return: Возвращает True, если файл был создан или уже есть.
    """
    if os.path.isfile(PyFileName_):
        return True
    f = None
    try:
        try:
            os.makedirs(os.path.dirname(PyFileName_))
        except:
            pass
        f = open(PyFileName_, 'w')
        if PyFileBody_ is None:
            f.write(_PyFileDefault)
        else:
            f.write(str(PyFileBody_))
        f.close()
        log.info(u'Создан файл: <%s>.' % PyFileName_)
        return True
    except:
        if f:
            f.close()
        log.fatal(u'Ошибка создания модуля Python <%s>' % PyFileName_)
        return False


def LoadResource(FileName_):
    """
    Получить ресурс в ресурсном файле.
    @param FileName_: Полное имя ресурсного файла.
    """
    # Сначала предположим что файл в формате Pickle.
    struct = LoadResourcePickle(FileName_)
    if struct is None:
        # Но если он не в формате Pickle, то скорее всего в тексте.
        struct = LoadResourceText(FileName_)
    if struct is None:
        # Но если не в тексте но ошибка!
        log.warning(u'Ошибка формата файла <%s>.' % FileName_)
        return None
    return struct
    
    
def LoadResourcePickle(FileName_):
    """
    Получить ресурс из ресурсного файла в формате Pickle.
    @param FileName_: Полное имя ресурсного файла.
    """
    if os.path.isfile(FileName_):
        f = None
        try:
            f = open(FileName_)
            struct = cPickle.load(f)
            f.close()
            return struct
        except:
            if f:
                f.close()
            log.fatal(u'Ошибка чтения файла <%s>.' % FileName_)
            return None
    else:
        log.warning(u'Файл <%s> не найден.' % FileName_)
        return None


def LoadResourceText(FileName_):
    """
    Получить ресурс из ресурсного файла в текстовом формате.
    @param FileName_: Полное имя ресурсного файла.
    """
    if os.path.isfile(FileName_):
        f = None
        try:
            f = open(FileName_)
            txt = f.read().replace('\r\n', '\n')
            f.close()
            return eval(txt)
        except:
            if f:
                f.close()
            log.fatal(u'Ошибка чтения файла <%s>.' % FileName_)
            return None
    else:
        log.warning(u'Файл <%s> не найден.' % FileName_)
        return None


def SaveResourcePickle(FileName_, Resource_):
    """
    Сохранить ресурс в файле в формате Pickle.
    @param FileName_: Полное имя ресурсного файла.
    @Resource_: Словарно-списковая структура спецификации.
    @return: Возвращает результат выполнения операции True/False.
    """
    f = None
    try:
        # Если необходимые папки не созданы, то создать их
        dir_name = os.path.dirname(FileName_)
        try:
            os.makedirs(dir_name)
        except:
            pass

        f = open(FileName_, 'w')
        cPickle.dump(Resource_, f)
        f.close()
        log.info(u'Файл <%s> сохранен в формате Pickle.' % FileName_)
        return True
    except:
        if f:
            f.close()
        log.fatal(u'Ошибка сохраненения файла <%s> в формате Pickle.' % FileName_)
        
        return False


def SaveResourceText(FileName_, Resource_):
    """
    Сохранить ресурс в файле в текстовом формате.
    @param FileName_: Полное имя ресурсного файла.
    @Resource_: Словарно-списковая структура спецификации.
    @return: Возвращает результат выполнения операции True/False.
    """
    f = None
    try:
        # Если необходимые папки не созданы, то создать их
        dir_name = os.path.dirname(FileName_)
        try:
            os.makedirs(dir_name)
        except:
            pass

        f = open(FileName_, 'w')
        text = ic_util.StructToTxt(Resource_)
        f.write(text)
        f.close()
        log.info(u'Файл <%s> сохранен в текстовом формате.' % FileName_)
        return True
    except:
        if f:
            f.close()
        log.fatal(u'Ошибка сохраненения файла <%s> в текстовом формате.' % FileName_)
        return False


def isPackage(Dir_):
    """
    Проверка является ли директория пакетом.
    @param Dir_: Указание директории.
    @return: Возвращает True/False.
    """
    is_dir = os.path.isdir(Dir_)
    is_init_file = False
    if is_dir:
        init_filename = os.path.join(Dir_, '__init__.py')
        is_init_file = os.path.exists(init_filename)
    return bool(is_dir and is_init_file)
    

# --- Функции блокировки ресурсов --
def lockRes(ResName_, ResFileName_, ResFileExt_, LockDir_=None):
    """
    Заблокировать ресурс.
        Имя файла блокировки гонерируется 
        как ИмяРесурса_ИмяФайлаРесурса_РасширениеФайлаРесурса.lck.
        В файл блокировки записывается информация о владельце блокировки 
        в виде словаря {'owner':Имя хоста с которого заблокировался ресурс}.
    @param ResName_: Имя ресурса. 
        Если имя ресурса None, то блокируется файл ресурса целиком.
    @param ResFileName_: Имя файла ресурса.
    @param ResFileExt_: Расширение файла ресурса/тип ресурса.    
    @param LockDir_: Папка блокировок.
    """
    if LockDir_ is None:
        LockDir_ = os.getcwd()+'/lock'
        try:
            os.makedirs(LockDir_)
        except:
            pass
    lock_filename = '%s_%s_%s%s' % (ResName_, ResFileName_,
                                    ResFileExt_, lock.LOCK_FILE_EXT)
    lock_full_filename = os.path.join(LockDir_, lock_filename)
    log.debug('LOCK_RES <%s>' % lock_full_filename)
    return lock.LockFile(lock_full_filename, '{\'owner\':\'%s\'}' % lock.ComputerName())


def unlockRes(ResName_, ResFileName_, ResFileExt_, LockDir_=None):
    """
    Разблокировать ресурс.
        Ресурс м.б. разблокирован только с хоста-владельца.
    @param ResName_: Имя ресурса. 
    @param ResFileName_: Имя файла ресурса.
    @param ResFileExt_: Расширение файла ресурса/тип ресурса.    
    @param LockDir_: Папка блокировок.
    """
    if LockDir_ is None:
        LockDir_ = os.getcwd()+'/lock'
        try:
            os.makedirs(LockDir_)
        except:
            pass
    lock_filename = '%s_%s_%s%s' % (ResName_, ResFileName_,
                                    ResFileExt_, lock.LOCK_FILE_EXT)
    lock_full_filename = os.path.join(LockDir_, lock_filename)
    comp_name = lock.ComputerName()
    log.debug('UNLOCK_RES <%s>' % lock_full_filename)
    return lock.UnLockFile(lock_full_filename, owner=comp_name)


def isLockRes(ResName_, ResFileName_, ResFileExt_, LockDir_=None):
    """
    Проверить заблокирован ли ресурс.
    @param ResName_: Имя ресурса. 
    @param ResFileName_: Имя файла ресурса.
    @param ResFileExt_: Расширение файла ресурса/тип ресурса.    
    @param LockDir_: Папка блокировок.
    """
    if LockDir_ is None:
        LockDir_ = os.getcwd()+'/lock'
        try:
            os.makedirs(LockDir_)
        except:
            pass
    lock_filename = '%s_%s_%s%s' % (ResName_, ResFileName_,
                                    ResFileExt_, lock.LOCK_FILE_EXT)
    lock_full_filename = os.path.join(LockDir_, lock_filename)

    log.debug('IS_LOCK_RES <%s>' % lock_full_filename)
    is_lock = lock.IsLockedFile(lock_full_filename)
    if is_lock:
        # Если файл блокировки есть, то
        # проверить кем он заблокирован
        is_lock = bool(getLockResOwner(ResName_, ResFileName_,
                                       ResFileExt_, LockDir_) != lock.ComputerName())
    return is_lock    


def delAllLockRes(LockDir_):
    """
    Удалить все файлы блокировок ресурсов данного хоста из папки блокировок.
    @param LockDir_: Папка блокировок.
    """
    if LockDir_ is None:
        LockDir_ = os.path.join(os.getcwd(), 'lock')
        try:
            os.makedirs(LockDir_)
        except:
            pass
    return lock.UnLockAllFile(LockDir_)


def getLockResOwner(ResName_, ResFileName_, ResFileExt_, LockDir_=None):
    """
    Определить владельца блокировки ресурса.
    """
    if LockDir_ is None:
        LockDir_ = os.path.join(os.getcwd(), 'lock')
        try:
            os.makedirs(LockDir_)
        except:
            pass
    lock_filename = '%s_%s_%s%s' % (ResName_, ResFileName_,
                                    ResFileExt_, lock.LOCK_FILE_EXT)
    lock_full_filename = os.path.join(LockDir_, lock_filename)
    log.debug('LOCK_RES OWNER <%s>' % lock_full_filename)
    return lock.ReadLockRecord(lock_full_filename)['owner']


def getNewID():
    """
    Генерация нового идентификатора для ресурса.
    """
    if wx:
        return '_'+str(wx.NewId())
    return '_XXX'
