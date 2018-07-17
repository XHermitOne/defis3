#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Библиотека блокировок.
Формат:
Информация о координатах блокировок (таблица/запись) храняться:
таблица: имя директории
запись: имя файла в этой директории (если файл существует - запись заблокирована)

Если заблокирована таблица - добавляется к имени расширение '.lck'
"""

# --- Подключение пакетов ---
import wx
import os
import os.path as osp
from . import ic_file
from . import ic_util
from . import ic_str
import ic.engine.ic_user
from ic.kernel import io_prnt

_ = wx.GetTranslation

# --- Константы ---
# Расширение файла блокировки
LOCK_FILE_EXT = '.lck'

# Имя блокировки по умолчанию
DEFAULT_LOCK_NAME = 'default'

lockDir = '.'+os.sep+'lock'     # Это путь к общей директории блокировок

err = 0     # код текущей ошибки
# key - код оишбки, сообщение (строка)
errRes = {1: u'Таблица заблокирована. Не возможно заблокировать запись.',
          2: u'Запись заблокирована.',      # №2
          3: u'',                           # №3
          4: u'',                           # №4
          5: u'',                           # №5
          99: u'Не известная ошибка.'       # 99
          }


# --- Функции ---
def LockRecord(table, record, message=None):
    """
    Блокировка записи по имени/номеру таблицы и номеру записи
    @param table: -имя таблицы (int/String)
    @param record:  -номер записи (int/String)
    @param message: -тестовое сообщение (небязательное)
    """
    global err
    err = 0
    io_prnt.outLog(u'### LockRecord ic_lock path=%s' % os.getcwd())
    table = __norm(table)
    record = __norm(record)

    if isLockTable(record):
        err = 1     # Вся таблица уже заблокирована
                    # Запись заблокировать невозможно
        return err
    path = getLockDir()+os.sep+table    # это путь к директории флагов блокировок этой таблицы
    if osp.isdir(path) == 0:            # директории блокировок
                                        # под эту таблицу еще не создали
        try:
            os.makedirs(path)       # Создать директори. под эту таблицу
        except:
            io_prnt.outErr(u'Makedirs Error!')
            err = 99
    # Проверка на блокирвку всего файла недоделана!!!!!!!!!!!!!!!!
    # Генерация файла-флага блокировки
    name = path+os.sep+record
    try:
        # Попытка создать файл
        f = os.open(name, os.O_CREAT | os.O_EXCL, 0777)
    except OSError:
        err = 2     # Уже есть файл. Т.Е. уже заблокирован
    else:           # выполнено без ошибки
        if message is not None:
            os.close(f)
            f = os.open(name, os.O_WRONLY, 0777)
            os.write(f, message)
            
        os.close(f)
                
    return err


def unLockRecord(table, record):
    """
    Разблокировка записи по имени/номеру таблицы и номеру записи.
    @type table: C{int/string}
    @param table: Имя таблицы.
    @type record: C{int/string}
    @parma record: Номер записи.
    """
    global err
    err = 0
    table = __norm(table)
    record = __norm(record)
    # это путь к директории флагов блокировок этой таблицы
    path = getLockDir()+os.sep+table
    if osp.isdir(path):    # директории блокировок под эту таблицу еще не создали
        if osp.isfile(path+os.sep+record):
            try:
                # удалить этот файл флага
                os.remove(path+os.sep+record)
            except:
                err = 99  # оишбка удаления файла флага
        return err


def LockTable():
    pass


def UnLockTable():
    pass


def isLockTable(table):
    """
    Проверка на блокировку таблицы.
    """
    table = __norm(table)
    io_prnt.outLog('%s, %s' % (table, getLockDir()))
    # это путь к директории флагов блокировок этой таблицы
    path = os.path.join(getLockDir(), table+'.lck')
    return osp.isdir(path)


def readMessage(table, record):
    """
    Чтение текста собщения, если оно есть.
    @type table: C{int/string}
    @param table: Имя таблицы.
    @type record: C{int/string}
    @parma record: Номер записи.
    """
    ret = None
    f = None
    if isLockRecord(table, record) != 0:
        table = __norm(table)
        record = __norm(record)
        # это путь к директории флагов блокировок этой таблицы
        path = getLockDir()+os.sep+table
        name = path+os.sep+record
        try:
            # Попытка создать файл
            f = os.open(name, os.O_RDONLY | os.O_EXCL, 0777)
        except OSError:
            # Уже есть файл. Т.Е. уже заблокирован
            err = 2

    if f:
        # выполнено без ошибки
        ret = os.read(f, 65535)
        os.close(f)
    return ret


def isLockRecord(table, record):
    """
    Проверка на блокировку записи.
    @type table: C{int/string}
    @param table: Имя таблицы.
    @type record: C{int/string}
    @parma record: Номер записи.
    """
    ret = None
    global err
    table = __norm(table)
    record = __norm(record)
    ret = 0
    # это путь к директории флагов блокировок этой таблицы
    path = getLockDir()+os.sep+table
    # директории блокировок под эту таблицу еще не создали
    if osp.isdir(path):
        if osp.isfile(path+os.sep+record):
            ret = 1
        else:
            ret = 0
    return ret


def lastErr():
    """
    Вернуть последнне значение ошибки (число).
    """
    global err
    if err == 0:
        return 0
    else:
        return err


def lastErrMsg():
    """
    Вернуть последнне значение ошибки (Строковое сообщение).
    """
    global err
    if err == 0:
        return u''
    else:
        return errRes[err]


def __norm(var):
    """
    Служебная функция 'приведения' к виду имения файла имени таблицы
    и номера записи.
    """
    if isinstance(var, str):
        pass
    elif isinstance(var, int):
        var = str(var)          # нормализация имени номера записи
    elif isinstance(var, long):
        var = str(var)          # нормализация имени номера записи
    elif isinstance(var, float):
        var = str(int(var))     # нормализация имени номера записи
    return var


def getLockDir():
    """
    Определить папку блокировок.
    """
    lock_dir = ic.engine.ic_user.icGet('LOCK_DIR')
    if not lock_dir:
        io_prnt.outWarning(u'NOT DEFINE LOCK_DIR')
        return lockDir
    return lock_dir


def DelMyLockInDir(LockMyID_, LockDir_, DirFilesLock_):
    """
    Удалить блокировки только из указанной папки.
    @param LockMyID_: Идентификация хозяина блокировок.
    @param LockDir_: Папка блокировок.
    @param DirFilesLock_: Имена файлов и папок в директории LockDir_
    """
    try:
        # Отфильтровать только файлы
        lock_files = [x for x in [os.path.join(LockDir_, x) for x in DirFilesLock_] if os.path.isfile(x)]
        # Выбрать только свои файлы-блокировки
        for cur_file in lock_files:
            try:
                f = None
                f = open(cur_file)
                signature = f.read()
                f.close()
                f = None
                try:
                    signature = eval(signature)
                    # Если владелец в сигнатуре совпадает, то
                    # удалить этот файл-блокировку
                    if signature['computer'] == LockMyID_:
                        os.remove(cur_file)
                        io_prnt.outLog(u'Lock file %s is deleted.' % cur_file)
                except:
                    io_prnt.outWarning(u'Invalid lock signature: %s.' % signature)
            except:
                if f:
                    f.close()
                io_prnt.outErr(u'Read signature lock file error: %s.' % cur_file)
    except:
        io_prnt.outErr(u'Delete lock file error. Dir: %s' % LockDir_)


def DelMyLock(LockMyID_=None, LockDir_=lockDir):
    """
    Функция рекурсивного удаления блокировок записей.
    @param LockMyID_: Идентификация хозяина блокировок.
    @param LockDir_: Папка блокировок.
    """
    if not LockMyID_:
        LockMyID_ = GetMyHostName()
    return os.path.walk(LockDir_, DelMyLockInDir, LockMyID_)


# --- Блокировки ресурсов ---
def LockFile(FileName_, LockRecord_=None):
    """
    Блокировка файла.
    @param FileName_: Полное имя блокируемого файла.
    @param LockRecord_: Запись блокировки.
    @return: Возвращает кортеж:
        (результат выполения операции,запись блокировки).
    """
    lock_file_flag = False  # Флаг блокировки файла
    lock_rec = LockRecord_
    
    # Сгенерировать имя файла блокировки
    lock_file = os.path.splitext(FileName_)[0]+LOCK_FILE_EXT
    # Если файл не заблокирован, то заблокировать его
    if not os.path.isfile(lock_file):
        # Создать все директории для файла блокировки
        lock_dir = os.path.dirname(lock_file)
        if not os.path.isdir(lock_dir):
            os.makedirs(lock_dir)
        
        # Генерация файла-флага блокировки
        # ВНИМАНИЕ! Создавать файл надо на самом нижнем уровне!
        f = None
        try:
            #  Попытка создать файл
            f = os.open(lock_file, os.O_CREAT | os.O_EXCL, 0777)
        except OSError:
            #  Уже есть файл. Т.Е. уже заблокирован
            lock_file_flag = True
            # Прочитать кем хоть заблокирован
            if f:
                os.close(f)     # Закрыть сначала
            lock_rec = ReadLockRecord(lock_file)
        else:
            # выполнено без ошибки
            # Записать запись блокировки в файл
            if LockRecord_ is not None:
                os.close(f)     # Закрыть сначала
                # Открыть для записи
                f = os.open(lock_file, os.O_WRONLY, 0777)
                if isinstance(LockRecord_, str):
                    str_lock_rec = LockRecord_
                elif isinstance(LockRecord_, unicode):
                    str_lock_rec = LockRecord_.encode('utf-8')
                else:
                    str_lock_rec = str(LockRecord_)
                os.write(f, str_lock_rec)
            os.close(f)
    else:
        # Если файл заблокирован
        lock_file_flag = True
        lock_rec = ReadLockRecord(lock_file)

    return not lock_file_flag, lock_rec


def ReadLockRecord(LockFile_):
    """
    Прочитать запись блокировки из файла блокировки.
    @param LockFile_: Имя файла блокировки.
    @return: Возвращает запись блокировки или None в случае ошибки.
    """
    f = None
    try:
        lock_file = None
        lock_rec = None
        # На всякий случай преобразовать
        lock_file = os.path.splitext(LockFile_)[0]+LOCK_FILE_EXT
        # Если файла не существует, тогда и нечего прочитать
        if not os.path.exists(lock_file):
            return None
        # Открыть для чтения
        f = os.open(lock_file, os.O_RDONLY, 0777)
        lock_rec = os.read(f, 65535)
        os.close(f)
        try:
            # Если храниться какая-либо структура,
            # то сразу преобразовать ее
            return eval(lock_rec)
        except:
            return lock_rec
    except:
        if f:
            os.close(f)
        io_prnt.outErr(u'Read record lock: %s' % lock_file)
        return None


def IsLockedFile(FileName_):
    """
    Проверка блокировки файла.
    @param FileName_: Имя файла.
    @return: Возвращает результат True/False.
    """
    # Сгенерировать имя файла блокировки
    lock_file = os.path.splitext(FileName_)[0]+LOCK_FILE_EXT
    return os.path.isfile(lock_file)


def ComputerName():
    """
    Имя хоста.
    @return: Получит имя компа в сети.
    """
    comp_name = None
    if 'COMPUTERNAME' in os.environ:
        comp_name = os.environ['COMPUTERNAME']
    else:
        import socket
        comp_name = socket.gethostname()
        
    # ВНИМАНИЕ! Имена компьютеров должны задаваться только латиницей
    # Под Win32 можно задать имя компа русскими буквами и тогда
    # приходится заменять все на латиницу.
    if isinstance(comp_name, str):
        if ic_util.isOSWindowsPlatform():
            comp_name = unicode(comp_name, 'cp1251')
            comp_name = ic_str.rus2lat(comp_name)
    return comp_name


def GetMyHostName():
    """
    Получит имя компа в сети.
    """
    return ComputerName()


def UnLockFile(FileName_, **If_):
    """
    Разблокировать файл.
    @param FileName_: Имя файла.
    @param If_: Условие проверки разблокировки.
        Ключ записи блокировки=значение.
        Проверка производится по 'И'.
        Если такого ключа в записи нет,
        то его значение берется None.
    @return: Возвращает результат True/False.
    """
    # Сгенерировать имя файла блокировки
    lock_file = os.path.splitext(FileName_)[0]+LOCK_FILE_EXT
    io_prnt.outLog(u'UnLockInfo: %s, %s, %s' % (lock_file, If_, ic_file.Exists(lock_file)))
    if os.path.exists(lock_file):
        if If_:
            lck_rec = ReadLockRecord(lock_file)
            # Если значения по указанным ключам равны, то все ОК
            can_unlock = bool(len([key for key in If_.keys() if lck_rec.setdefault(key, None) == If_[key]]) == len(If_))
            io_prnt.outLog(u'UnLockInfo: %s, %s' % (lck_rec, can_unlock))
            if can_unlock:
                # Ресурс можно разблокировать
                os.remove(lock_file)
            else:
                # Нельзя разблокировать файл
                return False
        else:
            # Ресурс можно разблокировать
            os.remove(lock_file)
    return True


def _UnLockFileWalk(args, CurDir_, CurNames_):
    """
    Вспомогательная функция разблокировки файла на уровне каталога по имени
    компьютера. Используется в функции os.path.walk().
    @param args: Кортеж (Имя компьютера файлы которого нужно раблокировать,
        Имя пользователя).
    @param CurDir_: Текущий директорий.
    @param CurNames_: Имена поддиректорий и файлов в текущей директории.
    """
    computer_name = args[0]
    user_name = args[1]
    # Отфильтровать только файлы блокировок
    lock_files = [x for x in [ic_file.Join(CurDir_, x) for x in CurNames_] if ic_file.IsFile(x) and ic_file.SplitExt(x)[1] == LOCK_FILE_EXT]
    # Выбрать только свои файлы-блокировки
    for cur_file in lock_files:
        lock_record = ReadLockRecord(cur_file)
        if not user_name:
            if lock_record['computer'] == computer_name:
                os.remove(cur_file)
        else:
            if lock_record['computer'] == computer_name and \
               lock_record['user'] == user_name:
                os.remove(cur_file)


def UnLockAllFile(LockDir_, ComputerName_=None, UserName_=None):
    """
    Разблокировка всех файлов.
    @param LockDir_: Директория блокировок.
    @param ComputerName_: Имя компьютера файлы которого нужно раблокировать.
    @return: Возвращает результат True/False.
    """
    if not ComputerName_:
        ComputerName_ = ComputerName()
    if not UserName_:
        import ic.engine.ic_user
        UserName_ = ic.engine.ic_user.icGet('UserName')
    if LockDir_:
        return ic_file.Walk(LockDir_, _UnLockFileWalk, (ComputerName_, UserName_))


# --- Система блокировки произвольных ресурсов ---
class icLockSystem:
    """
    Система блокировки произвольных ресурсов.
    """

    def __init__(self, LockDir_=None):
        """
        Конструктор.
        @param LockDir_: Папка блокировки.
        """
        if LockDir_ is None:
            LockDir_ = lockDir
        
        self._LockDir = LockDir_
        
    # --- Папочные блокировки ---
    def lockDirRes(self, LockName_):
        """
        Поставить блокировку в виде директории.
        @param LockName_: Имя блокировки.
            М.б. реализовано в виде списка имен,
            что определяет путь к директории.
        """
        pass
        
    def unLockDirRes(self, LockName_):
        """
        Убрать блокировку в виде директории.
        @param LockName_: Имя блокировки.
            М.б. реализовано в виде списка имен,
            что определяет путь к директории.
        """
        pass

    # --- Файловые блокировки ---
    def _getLockFileName(self, LockName_):
        """
        Определитьимя файла блокировки по имени блокировки.
        @param LockName_: Имя блокировки.
        """
        lock_name = DEFAULT_LOCK_NAME
        try:
            if isinstance(LockName_, list):
                lock_name = LockName_[-1]
            elif isinstance(LockName_, str) or isinstance(LockName_, unicode):
                lock_name = os.path.splitext(os.path.basename(LockName_))[0]
            lock_file_name = os.path.join(self._LockDir, lock_name+LOCK_FILE_EXT)
            return lock_file_name
        except:
            io_prnt.outErr(u'Define lock file name error: %s %s' % (self._LockDir, LockName_))
        return lock_file_name
        
    def lockFileRes(self, LockName_, LockRec_=None):
        """
        Поставить блокировку в виде файла.
        @param LockName_: Имя блокировки.
            М.б. реализовано в виде списка имен,
            что определяет путь к файлу.
        @param LockRec_: Запись блокировки.
        """
        lock_file_name = self._getLockFileName(LockName_)
        if LockRec_ is None:
            import ic.engine.ic_user
            LockRec_ = {'computer': ComputerName(),
                        'user': ic.engine.ic_user.icGet('UserName')}
        return LockFile(lock_file_name, LockRec_)
        
    def unLockFileRes(self, LockName_):
        """
        Убрать блокировку в виде файла.
        @param LockName_: Имя блокировки.
            М.б. реализовано в виде списка имен,
            что определяет путь к файлу.
        """
        lock_file_name = self._getLockFileName(LockName_)
        return UnLockFile(lock_file_name)

    def isLockFileRes(self, LockName_):
        """
        Существует ли файловая блокировка с именем.
        @param LockName_: Имя блокировки.
        """
        lock_file_name = self._getLockFileName(LockName_)
        return IsLockedFile(lock_file_name)
    
    def getLockRec(self, LockName_):
        """
        Определить запись блокировки.
        @param LockName_: Имя блокировки.
        """
        lock_file_name = self._getLockFileName(LockName_)
        return ReadLockRecord(lock_file_name)
    
    # --- Общие функции блокировки ---
    def isLockRes(self, LockName_):
        """
        Существует ли блокировка с именем.
        @param LockName_: Имя блокировки.
        """
        pass
        
    def unLockAllMy(self):
        """
        Разблокировать все мои блокировки.
        """
        return UnLockAllFile(self._LockDir, ComputerName())
