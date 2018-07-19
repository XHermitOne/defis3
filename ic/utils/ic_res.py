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
import wx
import pickle

from . import util
from . import ic_file

from . import ic_util
from ic.log import log
from ic.engine import ic_user
# Функции блокировки ресурсов
from . import lock

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
    @return: Возвращает структуру Python определенную в виде текста в файле FileName_
    """
    return util.readAndEvalFile(FileName_, *args, **kwargs)


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
    global CUR_MENU_RES_FILE_NAME
    global CUR_MENU_RES_FILE
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
    from . import resource
    return resource.icGetRes(Name_,
                             os.path.splitext(ResFile_)[1][1:],
                             nameRes=os.path.splitext(ResFile_)[0])
    

_InitFileDefault = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

\"\"\"

\"\"\"

# Version
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
        f = open(init_file, 'wt')
        f.write(_InitFileDefault)
        f.close()
        log.info(u'Создан файл <%s>' % init_file)
        return True
    except:
        log.fatal(u'Ошибка создания модуля <%s/__init__.py>' % Path_)
        if f:
            f.close()
        return False


def CreatePackage(PackageDir_):
    """
    Создать пакет. То же самое что и создать __init__ файл.
    """
    return CreateInitFile(ic_file.AbsolutePath(PackageDir_))


_PyFileDefault = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

\"\"\"

\"\"\"

# Version
__version__ = (0, 0, 0, 1)

# Functions
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
        f = open(PyFileName_, 'wt')
        if PyFileBody_ is None:
            f.write(_PyFileDefault)
        else:
            f.write(str(PyFileBody_))
        f.close()
        log.info(u'Создан модуль Python <%s>' % PyFileName_)
        return True
    except:
        log.fatal(u'Create module error: %s' % PyFileName_)
        if f:
            f.close()
        return False


def LoadResource(FileName_):
    """
    Получить ресурс в ресурсном файле.
    @param FileName_: Полное имя ресурсного файла.
    """
    FileName_ = ic_file.AbsolutePath(FileName_)
    # Сначала предположим что файл в формате Pickle.
    struct = LoadResourcePickle(FileName_)
    if struct is None:
        # Но если он не в формате Pickle, то скорее всего в тексте.
        struct = LoadResourceText(FileName_)
    if struct is None:
        # Но если не в тексте но ошибка!
        log.warning(u'Не корректный формат файла: %s.' % FileName_)
        return None
    return struct


def LoadResourcePickle(FileName_):
    """
    Получить ресурс из ресурсного файла в формате Pickle.
    @param FileName_: Полное имя ресурсного файла.
    """
    FileName_ = ic_file.AbsolutePath(FileName_)
    if os.path.isfile(FileName_):
        f = None
        try:
            f = open(FileName_, 'rb')
            struct = pickle.load(f)
            f.close()
            return struct
        except:
            if f:
                f.close()
            log.fatal(u'Ошибка чтения файла ресурса <%s>' % FileName_)
            return None
    else:
        log.warning(u'Файл ресурса <%s> не найден' % FileName_)
        return None


def LoadResourceText(FileName_):
    """
    Получить ресурс из ресурсного файла в текстовом формате.
    @param FileName_: Полное имя ресурсного файла.
    """
    FileName_ = ic_file.AbsolutePath(FileName_)
    if os.path.isfile(FileName_):
        f = None
        try:
            f = open(FileName_, 'rt')
            txt = f.read().replace('\r\n', '\n')
            f.close()
            return eval(txt)
        except:
            if f:
                f.close()
            log.fatal(u'Ошибка чтения файла ресурса <%s>' % FileName_)
            return None
    else:
        log.warning(u'Файл ресурса <%s> не найден' % FileName_)
        return None


def SaveResourcePickle(FileName_, Resource_):
    """
    Сохранить ресурс в файле в формате Pickle.
    @param FileName_: Полное имя ресурсного файла.
    @param Resource_: Словарно-списковая структура спецификации.
    @return: Возвращает результат выполнения операции True/False.
    """
    FileName_ = ic_file.AbsolutePath(FileName_)
    f = None
    try:
        # Если необходимые папки не созданы, то создать их
        dir_name = os.path.dirname(FileName_)
        try:
            os.makedirs(dir_name)
        except:
            pass

        f = open(FileName_, 'wb')
        pickle.dump(Resource_, f)
        f.close()
        log.info(u'Файл <%s> записан в pickle формате.' % FileName_)
        return True
    except:
        log.fatal(u'Ошибка записи файла <%s> в pickle формате.' % FileName_)
        if f:
            f.close()
        return False


def SaveResourceText(FileName_, Resource_, ToStruct_=False):
    """
    Сохранить ресурс в файле в текстовом формате.
    @param FileName_: Полное имя ресурсного файла.
    @param Resource_: Словарно-списковая структура спецификации.
    @param ToStruct_: Сохранить в структурном виде ресурс?
    @return: Возвращает результат выполнения операции True/False.
    """
    FileName_ = ic_file.AbsolutePath(FileName_)
    f = None
    try:
        # Если необходимые папки не созданы, то создать их
        dir_name = os.path.dirname(FileName_)
        try:
            os.makedirs(dir_name)
        except:
            pass

        f = open(FileName_, 'wt')
        if ToStruct_:
            text = ic_util.StructToTxt(Resource_)
        else:
            text = str(Resource_)
        f.write(text)
        f.close()
        log.info(u'Ресурс сохранен в файле <%s> в текстовом формате' % FileName_)
        return True
    except:
        log.fatal(u'Ошибка сохранения ресурса в текстовом формате в файле <%s>' % FileName_)
        if f:
            f.close()
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
        is_init_file = os.path.exists(os.path.join(Dir_, '__init__.py'))
    return bool(is_dir and is_init_file)
    

def lockRes(ResName_, ResFileName_, ResFileExt_, LockDir_=None):
    """
    Заблокировать ресурс.
        Имя файла блокировки гонерируется 
        как ИмяРесурса_ИмяФайлаРесурса_РасширениеФайлаРесурса.lck.
        В файл блокировки записывается информация о владельце блокировки 
        в виде словаря {'computer':Имя хоста с которого заблокировался ресурс}.
    @param ResName_: Имя ресурса. 
        Если имя ресурса None, то блокируется файл ресурса целиком.
    @param ResFileName_: Имя файла ресурса.
    @param ResFileExt_: Расширение файла ресурса/тип ресурса.    
    @param LockDir_: Папка блокировок.
    """
    if LockDir_ is None:
        LockDir_ = lock.getLockDir()
        try:
            os.makedirs(LockDir_)
        except:
            pass
    if ResName_ is None:
        ResName_ = ResFileName_
        
    lock_file = os.path.join(LockDir_,
                             '%s_%s_%s%s' % (ResName_.strip(),
                                             ResFileName_.strip(),
                                             ResFileExt_.strip(),
                                             lock.LOCK_FILE_EXT))
    comp_name = lock.ComputerName()
    user_name = ic_user.icGet('UserName')
    log.info(u'Блокировка ресурса <%s>' % lock_file)
    return lock.LockFile(lock_file, u'{\'computer\':\'%s\',\'user\':\'%s\'}' % (comp_name,
                                                                                user_name))


def unlockRes(ResName_, ResFileName_, ResFileExt_, LockDir_=None):
    """
    Разблокировать ресурс. Ресурс м.б. разблокирован только с хоста-владельца.
    @param ResName_: Имя ресурса. 
    @param ResFileName_: Имя файла ресурса.
    @param ResFileExt_: Расширение файла ресурса/тип ресурса.    
    @param LockDir_: Папка блокировок.
    """
    if LockDir_ is None:
        LockDir_ = lock.getLockDir()
        os.makedirs(LockDir_)
    if ResName_ is None:
        ResName_ = ResFileName_
        
    lock_file = os.path.join(ic_file.NormPathUnix(LockDir_),
                             '%s_%s_%s%s' % (ResName_.strip(),
                                             ResFileName_.strip(),
                                             ResFileExt_.strip(),
                                             lock.LOCK_FILE_EXT))
    user_name = ic_user.getCurUserName()
    log.info(u'Снятие блокировки ресурса <%s> : <%s>' % (lock_file, user_name))
    return lock.UnLockFile(lock_file, user=user_name)


def isLockRes(ResName_, ResFileName_, ResFileExt_, LockDir_=None):
    """
    Проверить заблокирован ли ресурс.
    @param ResName_: Имя ресурса. 
    @param ResFileName_: Имя файла ресурса.
    @param ResFileExt_: Расширение файла ресурса/тип ресурса.    
    @param LockDir_: Папка блокировок.
    """
    if LockDir_ is None:
        LockDir_ = lock.getLockDir()
        os.makedirs(LockDir_)
    if ResName_ is None:
        ResName_ = ResFileName_
        
    # Кроме проверки блокировки ресурса необходимо проверить блокировку файла ресурса
    lock_file = os.path.join(ic_file.NormPathUnix(LockDir_),
                             '%s_%s_%s%s' % (ResFileName_.strip(),
                                             ResFileName_.strip(),
                                             ResFileExt_.strip(),
                                             lock.LOCK_FILE_EXT))
        
    lock_res = os.path.join(ic_file.NormPathUnix(LockDir_),
                            '%s_%s_%s%s' % (ResName_.strip(),
                                            ResFileName_.strip(),
                                            ResFileExt_.strip(),
                                            lock.LOCK_FILE_EXT))
        
    is_lock_file = lock.IsLockedFile(lock_file)
    is_lock_res = lock.IsLockedFile(lock_res)
    is_lock = False
    if is_lock_file or is_lock_res:
        log.info(u'Ресурс заблокирован <%s> : [%s : %s]' % (lock_file, is_lock_file, is_lock_res))
            
        # Если файл блокировки есть, то
        # проверить кем он заблокирован
        if is_lock_file:
            is_lock_file = bool(getLockResOwner(ResFileName_, ResFileName_,
                                                ResFileExt_, LockDir_) != ic_user.getCurUserName())
        
        # Если файл блокировки есть, то
        # проверить кем он заблокирован
        if is_lock_res:
            is_lock_res = bool(getLockResOwner(ResName_, ResFileName_,
                                               ResFileExt_, LockDir_) != ic_user.getCurUserName())
        is_lock = is_lock_file or is_lock_res
    return is_lock


def delAllLockRes(LockDir_):
    """
    Удалить все файлы блокировок ресурсов данного хоста из папки блокировок.
    @param LockDir_: Папка блокировок.
    """
    if LockDir_ is None:
        LockDir_ = lock.getLockDir()
        os.makedirs(LockDir_)
    return lock.UnLockAllFile(LockDir_)


def getLockResOwner(ResName_, ResFileName_, ResFileExt_, LockDir_=None):
    """
    Определить владельца блокировки ресурса.
    """
    if LockDir_ is None:
        LockDir_ = lock.getLockDir()
        os.makedirs(LockDir_)
    if ResName_ is None:
        ResName_ = ResFileName_
        
    lock_file = os.path.join(LockDir_,
                             '%s_%s_%s%s' % (ResName_, ResFileName_,
                                             ResFileExt_, lock.LOCK_FILE_EXT))
    log.info(u'Владелец заблокированного ресурса <%s>' % lock_file)
    return lock.ReadLockRecord(lock_file)['user']


def getLockResRecord(ResName_, ResFileName_, ResFileExt_, LockDir_=None):
    """
    Определить запись блокировки ресурса.
    """
    if LockDir_ is None:
        LockDir_ = lock.getLockDir()
        os.makedirs(LockDir_)
    if ResName_ is None:
        ResName_ = ResFileName_
        
    lock_file = os.path.join(LockDir_,
                             '%s_%s_%s%s' % (ResName_, ResFileName_,
                                             ResFileExt_, lock.LOCK_FILE_EXT))
    return lock.ReadLockRecord(lock_file)


def getNewID():
    """
    Генерация нового идентификатора для ресурса.
    """
    return '_'+str(wx.NewId())


def findSpcInResource(Name_, Resource_):
    """
    Найти спецификацию в ресурсе по имени.
    @param Name_: Имя спецификации.
    @param Resource_: Дерево ресурсов.
    @return: Возвращает искомую спецификацию или None, если
        спецификация не найдена.
    """
    if isinstance(Resource_, list):
        for spc in Resource_:
            find_spc = findSpcInResource(Name_, spc)
            if find_spc:
                return find_spc
    elif isinstance(Resource_, dict):
        if Resource_['name'] == Name_:
            return Resource_
        # Поиск в дочерних элементах
        if 'child' in Resource_:
            return findSpcInResource(Name_, Resource_['child'])
        
    # Спецификация не найдена
    return None
