#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль описания класса ХРАНИЛИЩА ПЕРЕМЕННЫХ.

@var REF_IDX: Индекс символа ссылки в строке прав доступа к переменной.
@var REF_SYMB: Символ ссылки (данные передаются по значению/ссылке (-/*)).

@var READ_IDX: Индекс символа чтения в строке прав доступа к переменной.
@var READ_SYMB: Символ чтения.

@var WRITE_IDX: Индекс символа записи в строке прав доступа к переменной.
@var WRITE_SYMB: Символ записи.

@var LOCK_SYMB: Символ блокировки флага.
"""

# --- Подключение библиотек ---
import copy
from re import split

from ic.kernel import io_prnt
from ic.utils import resfunc

# --- Константы ---
# Для защиты данных есть 3 флага (в виде строки '*r-'):
# val_ref - данные передаются по значению/ссылке (-/*)
REF_IDX = 0
REF_SYMB = '*'
# read - блокировка на чтение данных (r/-)
READ_IDX = 1
READ_SYMB = 'r'
# write - блокировка на запись данных (w/-)
WRITE_IDX = 2
WRITE_SYMB = 'w'

# Символ блокировки флага
LOCK_SYMB = '-'

# --- Список ключей ---
STORE_LOCK_KEY = 'lock_key'         # <ключ блокировки записи переменной, (флаг, целое, строка)>
STORE_SECURITY_KEY = 'security'     # <строка прав пользования переменной, строка из 3-х символов>
STORE_DATA_KEY = 'data'     # <значение переменной, любые данные (флаги, целое, строка, список, словарь и т.п.)>
STORE_ITEMS_KEY = 'folder'  # <структура аналогичная головной описывающая следующий уровень папок>

# Спецификации:
# Спецификация узла хранилища
SPC_IC_STORENODE = {STORE_LOCK_KEY: None,       # Ключ блокировки данных узла
                    STORE_SECURITY_KEY: '*rw',  # Права доступа к данным узла
                    STORE_DATA_KEY: None,       # Данные узла
                    STORE_ITEMS_KEY: {},        # Вложенные узлы
                    }

__version__ = (0, 0, 0, 2)


class icVarStorage:
    """    
    Класс хранителя глобальных объектов системы.
    """
    def __init__(self, ResFile_='', CanLog_=True):
        """
        Конструктор класса.
        @param ResFile_: Ресурсный файл глобальных переменных.
        @param CanLog_: Разрешение включения регистратора.
        """
        # === Атрибуты класса ===
        # Ресурсный файл глобальных переменных
        self._ResFile = ResFile_
        # Разрешение включения регистратора.
        self._CanLog = CanLog_
        # Само хранилище данных (В ВИДЕ СЛОВАРЯ)
        self._storage = {}
        # Загрузить сразу из ресурсного файла
        if ResFile_ != '':
            self._Load(ResFile_)

    def getStorage(self):
        return self._storage
        
    # --- Функции получения доступа к объекту ---
    def Add(self, Name_, Data_, Security_='*rw'):
        """
        Записать в хранилище объект.
        @param Name_: Имя-идентификатор объекта .
        @param Data_: Тело объекта.
        @param Security_: Строка прав доступа к переменной.
        """
        try:
            path = split(r'[/]', Name_)
            return self.AddToPath(path, Data_, Security_)
        except:
            io_prnt.outErr(u'Ошибка записи в хранилище объекта %s' % Name_)
            return False, None

    def AddToPath(self, Path_, Data_, Security_='*rw',storage_=None):
        """
        Записать в хранилище объект (в качестве пути передается список имен).
        @param Path_: в качестве пути передается список имен.
        @param Data_: Тело объекта.
        @param Security_: Строка прав доступа к переменной.
        """
        node = ''
        try:
            # Проверка аргументов
            if not isinstance(Path_, list):
                self._Log(u'Неверный тип аргумента Path_')
                return False, None
            if storage_ is None:
                storage_ = self._storage
            
            node = Path_[0]     # Берем первый элемент
            # Если остался последний элемент, тогда добавить в него данные
            if len(Path_) == 1:
                if node in storage_ and \
                   STORE_DATA_KEY in storage_[node] and \
                   storage_[node][STORE_SECURITY_KEY].find(WRITE_SYMB) == -1:
                    self._Log(u'Элемент под именем <%s> уже существует в хранилище' % node)
                    return False, None
                else:
                    # Добавить элемент
                    storage_[node] = {}
                    storage_[node][STORE_LOCK_KEY] = None
                    storage_[node][STORE_DATA_KEY] = Data_
                    storage_[node][STORE_SECURITY_KEY] = Security_
                    storage_[node][STORE_ITEMS_KEY] = {}
            else:
                if node not in storage_:
                    # Если узел не гайден, тогда создать его
                    storage_[node] = {}
                    storage_[node][STORE_LOCK_KEY] = None
                    storage_[node][STORE_SECURITY_KEY] = Security_
                    storage_[node][STORE_ITEMS_KEY] = {}
                storage_ = storage_[node][STORE_ITEMS_KEY]
                return self.AddToPath(Path_[1:], Data_, Security_, storage_)
            return True, None
        except:
            io_prnt.outErr(u'Ошибка записи в хранилище объекта %s' % node)
            return False, None

    def Clear(self):
        """
        Полностью очистить хранилище.
        """
        try:
            self._storage = {}
        except:
            io_prnt.outErr(u'Ошибка очистки хранилища данных')

    def Del(self, Name_):
        """
        Получить объект из хранилища с удалением.
        @param Name_: Имя-идентификатор объекта.
        @return: Возвращает ссылку на объект или None.
        """
        try:
            path = split(r'[/]', Name_)
            return self.DelToPath(path)
        except:
            io_prnt.outErr(u'Ошибка удаления объекта <%s> из хранилища' % Name_)
            return False, None

    def DelToPath(self, Path_, storage_=None):
        """
        Получить объект из хранилища с удалением.
        @param Path_: в качестве пути передается список имен.
        @return: Возвращает ссылку на объект или None.
        """
        try:
            node = ''
            # Проверка аргументов
            if not isinstance(Path_, list):
                self._Log(u'Неверный тип аргумента Path_')
                return False, None
            if storage_ is None:
                storage_ = self._storage
            
            node = Path_[0]     # Берем первый элемент
            # Если остался последний элемент, тогда удаляем
            if len(Path_) == 1:
                if node not in storage_:
                    self._Log(u'Элемент <%s> не найден' % node)
                    return False, None
                else:
                    if storage_[node][STORE_LOCK_KEY]:
                        self._Log(u'Объект <%s> заблокирован' % node)
                        return False, None
                    elif storage_[node][STORE_SECURITY_KEY][WRITE_IDX] != WRITE_SYMB:
                        self._Log(u'Запрещен доступ к объекту <%s>' % node)
                        return False, None
                    else:
                        if STORE_DATA_KEY in storage_[node]:
                            obj = storage_[node][STORE_DATA_KEY]
                        elif STORE_ITEMS_KEY in storage_[node]:
                            obj = storage_[node][STORE_ITEMS_KEY]
                        else:
                            obj = None
                        del storage_[node]
                        return True, obj
            else:
                if node not in storage_:
                    self._Log(u'Элемент <%s> не найден' % node)
                    return False, None
                storage_ = storage_[node][STORE_ITEMS_KEY]
                return self.DelToPath(Path_[1:], storage_)
            return False, None
        except:
            io_prnt.outErr(u'Ошибка удаления объекта <%s> из хранилища' % node)
            return False, None

    def GetCopy(self, Name_, LockKey_=None):
        """
        Получить копию объекта в хранилище, для редактирования.
        Если LockKey_==None, то доступ к объекту не блокируется
        @param Name_: Имя-идентификатор объекта.
        @param LockKey_: Ключ блокировки доступа 
            Если LockKey_==None, то доступ к объекту не блокируется.
        @return: Копия объекта не связанная с оригиналом.
        """
        try:
            path = split(r'[/]', Name_)
            node = self._GetNode(path)[1]

            if node is None:
                return False, None
            # Проверка существования ключа
            if STORE_LOCK_KEY not in node:
                node[STORE_LOCK_KEY] = None
            # Проверка блокировки объекта владельцем
            if not node[STORE_LOCK_KEY]:
                node[STORE_LOCK_KEY] = LockKey_
            else:
                self._Log(u'Объект <%s> заблокирован' % Name_)
                return False, None
            if STORE_SECURITY_KEY in node:
                if node[STORE_SECURITY_KEY][READ_IDX] == READ_SYMB:
                    # ВНИМАНИЕ!!! Функция deepcopy из модуля copy
                    # возвращает полную копию объекта не связанную с оригиналом
                    return True, copy.deepcopy(node[STORE_DATA_KEY])
                else:
                    self._Log(u'Запрет на чтение объекта <%s>' % Name_)
            return False, None
        except:
            io_prnt.outErr()

    def PutCopy(self, Name_, Data_, LockKey_=None):
        """
        Положить отредактированную копию объекта.
        Если LockKey_==None, то доступ к объекту не блокируется.
        @param Name_: Имя-идентификатор объекта.
        @param Data_: Тело объекта.
        @param LockKey_: Ключ блокировки доступа.
        @return: True, а в случае неудачи возвращает False.
        """
        try:
            path = split(r'[/]', Name_)
            node = self._GetNode(path)[1]

            if node is None:
                return False, None
            # Проверка существования ключа
            if STORE_LOCK_KEY not in node:
                node[STORE_LOCK_KEY] = None
            # Проверка блокировки объекта владельцем
            if node[STORE_LOCK_KEY] != LockKey_:
                self._Log(u'Объект <%s> заблокирован' % Name_)
                return False, None
            if STORE_SECURITY_KEY in node:
                if node[STORE_SECURITY_KEY][WRITE_IDX] == WRITE_SYMB:
                    del node[STORE_DATA_KEY]        # Сначала удалить
                    node[STORE_DATA_KEY] = Data_    # Затем восстановить
                else:
                    self._Log(u'Запрет на модификацию объекта <%s>' % Name_)
                    return False, None
            return True, None
        except:
            io_prnt.outErr()

    def Ref(self, Name_, LockKey_=None):
        """
        Получить ссылку на объект в хранилище, для чтения.
        Если LockKey_==None, то доступ к объекту не блокируется.
        @param Name_: Имя-идентификатор объекта.
        @param LockKey_: Ключ блокировки доступа.
        @return: Ссылку на объект.
        """
        try:
            path = split(r'[/]', Name_)
            node = self._GetNode(path)[1]

            if node is None:
                return False, None

            if node[STORE_SECURITY_KEY][REF_IDX] != REF_SYMB:
                self._Log(u'Запрет на доступ к объекту <%s>' % Name_)
                return False, None

            # Проверка существования ключа
            if STORE_LOCK_KEY not in node:
                node[STORE_LOCK_KEY] = None
            # Проверка блокировки объекта владельцем
            if node[STORE_LOCK_KEY] is None:
                node[STORE_LOCK_KEY] = LockKey_
            else:
                self._Log(u'Объект <%s> заблокирован' % Name_)
                return False, None
            if STORE_SECURITY_KEY in node:
                if node[STORE_SECURITY_KEY][READ_IDX] == READ_SYMB:
                    return True, node[STORE_DATA_KEY]
            return False, None
        except:
            io_prnt.outErr()

    def _GetNode(self, Path_, storage_=None):
        """
        Получить узел объекта из хранилища по пути.
        @param Path_: в качестве пути передается список имен.
        """
        try:
            node = ''
            # Проверка аргументов
            if not isinstance(Path_, list):
                self._Log(u'Неверный тип аргумента Path_')
                return False, None
            if storage_ is None:
                storage_ = self._storage
            
            node = Path_[0]     # Берем первый элемент
            if node not in storage_:
                return False, None
            # Если остался последний элемент, тогда возвращаем его
            if len(Path_) == 1:
                return True, storage_[node]
            else:
                storage_ = storage_[node][STORE_ITEMS_KEY]
                return self._GetNode(Path_[1:], storage_)
            return False, None
        except:
            io_prnt.outErr(u'Ошибка определения узла <%s>' % node)
            return False, None
        
    # --- Функции чтения/записи на диск ---
    def _Save(self, ResFile_=''):
        """
        Сохранить хранилище в ресурсном файле.
        @param ResFile_: Имя ресурсного файла.
        """
        try:
            if ResFile_ != '':
                self.SetResFile(ResFile_)
            if self._ResFile is None or self._ResFile == '':
                return False, None

            resfunc.SaveResourceText(self._ResFile, self._storage)
        except:
            io_prnt.outErr()

    def _Load(self, ResFile_=''):
        """
        Загрузить хранилище из ресурсного файла.
        @param ResFile_: Имя ресурсного файла.
        """
        try:
            if ResFile_ != '':
                self.SetResFile(ResFile_)
            if self._ResFile != '':
                self._storage = resfunc.LoadResourceText(self._ResFile)
        except:
            io_prnt.outErr()

    # --- Сервисные функции ---
    def Is(self, Name_):
        """
        Проверка существует ли такой объект.
        @param Name_: Имя объекта.
        """
        try:
            path = split(r'[/]', Name_)
            node = self._GetNode(path)[1]
            if node is None:
                return False
            return True
        except:
            io_prnt.outErr()

    def CanRead(self, Name_, LockKey_=None):
        """
        Проверка возможности чтения объекта из хранилища.
        @param Name_: Имя объекта.
        @param LockKey_: Ключ блокировки доступа.
        """
        try:
            path = split(r'[/]', Name_)
            node = self._GetNode(path)[1]
            if node is None:
                return False
            if node[STORE_SECURITY_KEY][READ_IDX] != READ_SYMB:
                return False
            return True
        except:
            io_prnt.outErr()

    def CanWrite(self, Name_, LockKey_=None):
        """
        Проверка возможности изменения объекта из хранилища.
        @param Name_: Имя объекта.
        @param LockKey_: Ключ блокировки доступа.
        """
        try:
            path = split(r'[/]', Name_)
            node = self._GetNode(path)[1]
            if node is None:
                return False
            if node[STORE_SECURITY_KEY][WRITE_IDX] != WRITE_SYMB:
                return False
            return True
        except:
            io_prnt.outErr()

    def CanRef(self, Name_, LockKey_=None):
        """
        Проверка возможности получения ссылки на объект
        @param Name_: Имя объекта.
        @param LockKey_: Ключ блокировки доступа.
        """
        try:
            path = split(r'[/]', Name_)
            node = self._GetNode(path)[1]
            if node is None:
                return False
            if node[STORE_SECURITY_KEY][REF_IDX] != REF_SYMB:
                return False
            return True
        except:
            io_prnt.outErr()

    def TextStorage(self):
        """
        Функция выводит в виде текста все имена объектов ХРАНИЛИЩА.
        Функция применяется при отладке.
        """
        try:
            line = u'-------------------------------------------------------------------------------'
            txt = line
            txt += u'\n'
            txt += u'Имя                                                    Права доступа Блокировка'
            txt += u'\n'
            txt += line
            txt += u'\n'
            txt += self._TextListAll(self._storage)
            txt += line
            return txt
        except:
            io_prnt.outErr(u'Ошибка преобразования в виде текста объектов ХРАНИЛИЩА')
        
    def _TextListAll(self, Storage_=None, Path_=''):
        """
        Функция выводит в виде текста все имена объектов ХРАНИЛИЩА.
        Функция применяется при отладке.
        Используется рекурсивный вызов.
        @param Storage_: Текущий уровень(папка) ХРАНИЛИЩА.
        @param Path_: Путь до объекта.
        """
        txt = u''
        for obj_name in Storage_.keys():
            name = Path_+obj_name
            value = str(Storage_[obj_name][STORE_DATA_KEY])
            security = Storage_[obj_name][STORE_SECURITY_KEY]
            lock = u'-'
            
            if Storage_[obj_name][STORE_LOCK_KEY]<>None:
                lock = u'+'
            txt += u'%-20s %-40s %-9s %-7s' % (name, value, security, lock)
            if STORE_ITEMS_KEY in Storage_[obj_name] and \
                Storage_[obj_name][STORE_ITEMS_KEY] != {}:
                txt += self._TextListAll(Storage_[obj_name][STORE_ITEMS_KEY],
                                         name+'/')
            txt += u'\n'
        return txt

    def _Log(self, Msg_):
        """
        Регистрация сообщения/ошибки.
        @param Msg_: Текст сообщения.
        """
        if self._CanLog:
            io_prnt.outWarning(Msg_)

    # --- Функции-свойства класса ---

    def GetResFile(self):
        return self._ResFile

    def SetResFile(self, ResFile_):
        if isinstance(ResFile_, str):
            self._ResFile = ResFile_
        else:
            self._Log(u'Неверный тип аргумента ResFile_')
