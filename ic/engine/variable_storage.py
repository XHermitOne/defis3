#!/usr/bin/env python3
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

from ic.utils import resfunc
from ic.log import log

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

__version__ = (0, 1, 1, 2)


class icVarStorage:
    """    
    Класс хранителя глобальных объектов системы.
    """
    def __init__(self, res_filename='', bLog=True):
        """
        Конструктор класса.
        @param res_filename: Ресурсный файл глобальных переменных.
        @param bLog: Разрешение включения регистратора.
        """
        # === Атрибуты класса ===
        # Ресурсный файл глобальных переменных
        self._res_filename = res_filename
        # Разрешение включения регистратора.
        self._can_log = bLog
        # Само хранилище данных (В ВИДЕ СЛОВАРЯ)
        self._storage = {}
        # Загрузить сразу из ресурсного файла
        if res_filename != '':
            self._load(res_filename)

    def getStorage(self):
        return self._storage
        
    # --- Функции получения доступа к объекту ---
    def Add(self, name, data, security='*rw'):
        """
        Записать в хранилище объект.
        @param name: Имя-идентификатор объекта .
        @param data: Тело объекта.
        @param security: Строка прав доступа к переменной.
        """
        try:
            path = split(r'[/]', name)
            return self.addToPath(path, data, security)
        except:
            log.fatal(u'Ошибка записи в хранилище объекта %s' % name)
        return False, None

    def addToPath(self, path, data, security='*rw', storage=None):
        """
        Записать в хранилище объект (в качестве пути передается список имен).
        @param path: в качестве пути передается список имен.
        @param data: Тело объекта.
        @param security: Строка прав доступа к переменной.
        """
        node = ''
        try:
            # Проверка аргументов
            if not isinstance(path, list):
                self._log(u'Неверный тип аргумента path')
                return False, None
            if storage is None:
                storage = self._storage
            
            node = path[0]     # Берем первый элемент
            # Если остался последний элемент, тогда добавить в него данные
            if len(path) == 1:
                if node in storage and \
                   STORE_DATA_KEY in storage[node] and \
                   storage[node][STORE_SECURITY_KEY].find(WRITE_SYMB) == -1:
                    self._log(u'Элемент под именем <%s> уже существует в хранилище' % node)
                    return False, None
                else:
                    # Добавить элемент
                    storage[node] = {}
                    storage[node][STORE_LOCK_KEY] = None
                    storage[node][STORE_DATA_KEY] = data
                    storage[node][STORE_SECURITY_KEY] = security
                    storage[node][STORE_ITEMS_KEY] = {}
            else:
                if node not in storage:
                    # Если узел не гайден, тогда создать его
                    storage[node] = {}
                    storage[node][STORE_LOCK_KEY] = None
                    storage[node][STORE_SECURITY_KEY] = security
                    storage[node][STORE_ITEMS_KEY] = {}
                storage = storage[node][STORE_ITEMS_KEY]
                return self.addToPath(path[1:], data, security, storage)
            return True, None
        except:
            log.fatal(u'Ошибка записи в хранилище объекта %s' % node)
        return False, None

    def Clear(self):
        """
        Полностью очистить хранилище.
        """
        self._storage = dict()

    def Del(self, name):
        """
        Получить объект из хранилища с удалением.
        @param name: Имя-идентификатор объекта.
        @return: Возвращает ссылку на объект или None.
        """
        try:
            path = split(r'[/]', name)
            return self.delToPath(path)
        except:
            log.fatal(u'Ошибка удаления объекта <%s> из хранилища' % name)
        return False, None

    def delToPath(self, path, storage=None):
        """
        Получить объект из хранилища с удалением.
        @param path: в качестве пути передается список имен.
        @return: Возвращает ссылку на объект или None.
        """
        node = ''
        try:
            # Проверка аргументов
            if not isinstance(path, list):
                self._log(u'Неверный тип аргумента path')
                return False, None
            if storage is None:
                storage = self._storage
            
            node = path[0]     # Берем первый элемент
            # Если остался последний элемент, тогда удаляем
            if len(path) == 1:
                if node not in storage:
                    self._log(u'Элемент <%s> не найден' % node)
                    return False, None
                else:
                    if storage[node][STORE_LOCK_KEY]:
                        self._log(u'Объект <%s> заблокирован' % node)
                        return False, None
                    elif storage[node][STORE_SECURITY_KEY][WRITE_IDX] != WRITE_SYMB:
                        self._log(u'Запрещен доступ к объекту <%s>' % node)
                        return False, None
                    else:
                        if STORE_DATA_KEY in storage[node]:
                            obj = storage[node][STORE_DATA_KEY]
                        elif STORE_ITEMS_KEY in storage[node]:
                            obj = storage[node][STORE_ITEMS_KEY]
                        else:
                            obj = None
                        del storage[node]
                        return True, obj
            else:
                if node not in storage:
                    self._log(u'Элемент <%s> не найден' % node)
                    return False, None
                storage = storage[node][STORE_ITEMS_KEY]
                return self.delToPath(path[1:], storage)
        except:
            log.fatal(u'Ошибка удаления объекта <%s> из хранилища' % node)
        return False, None

    def getCopy(self, name, lock_key=None):
        """
        Получить копию объекта в хранилище, для редактирования.
        Если lock_key==None, то доступ к объекту не блокируется
        @param name: Имя-идентификатор объекта.
        @param lock_key: Ключ блокировки доступа
            Если lock_key==None, то доступ к объекту не блокируется.
        @return: Копия объекта не связанная с оригиналом.
        """
        try:
            path = split(r'[/]', name)
            node = self._getNode(path)[1]

            if node is None:
                return False, None
            # Проверка существования ключа
            if STORE_LOCK_KEY not in node:
                node[STORE_LOCK_KEY] = None
            # Проверка блокировки объекта владельцем
            if not node[STORE_LOCK_KEY]:
                node[STORE_LOCK_KEY] = lock_key
            else:
                self._log(u'Объект <%s> заблокирован' % name)
                return False, None
            if STORE_SECURITY_KEY in node:
                if node[STORE_SECURITY_KEY][READ_IDX] == READ_SYMB:
                    # ВНИМАНИЕ!!! Функция deepcopy из модуля copy
                    # возвращает полную копию объекта не связанную с оригиналом
                    return True, copy.deepcopy(node[STORE_DATA_KEY])
                else:
                    self._log(u'Запрет на чтение объекта <%s>' % name)
        except:
            log.fatal()
        return False, None

    def putCopy(self, name, data, lock_key=None):
        """
        Положить отредактированную копию объекта.
        Если lock_key==None, то доступ к объекту не блокируется.
        @param name: Имя-идентификатор объекта.
        @param data: Тело объекта.
        @param lock_key: Ключ блокировки доступа.
        @return: True, а в случае неудачи возвращает False.
        """
        try:
            path = split(r'[/]', name)
            node = self._getNode(path)[1]

            if node is None:
                return False, None
            # Проверка существования ключа
            if STORE_LOCK_KEY not in node:
                node[STORE_LOCK_KEY] = None
            # Проверка блокировки объекта владельцем
            if node[STORE_LOCK_KEY] != lock_key:
                self._log(u'Объект <%s> заблокирован' % name)
                return False, None
            if STORE_SECURITY_KEY in node:
                if node[STORE_SECURITY_KEY][WRITE_IDX] == WRITE_SYMB:
                    del node[STORE_DATA_KEY]        # Сначала удалить
                    node[STORE_DATA_KEY] = data    # Затем восстановить
                else:
                    self._log(u'Запрет на модификацию объекта <%s>' % name)
                    return False, None
            return True, None
        except:
            log.fatal()
        return False, None

    def Ref(self, name, lock_key=None):
        """
        Получить ссылку на объект в хранилище, для чтения.
        Если lock_key==None, то доступ к объекту не блокируется.
        @param name: Имя-идентификатор объекта.
        @param lock_key: Ключ блокировки доступа.
        @return: Ссылку на объект.
        """
        try:
            path = split(r'[/]', name)
            node = self._getNode(path)[1]

            if node is None:
                return False, None

            if node[STORE_SECURITY_KEY][REF_IDX] != REF_SYMB:
                self._log(u'Запрет на доступ к объекту <%s>' % name)
                return False, None

            # Проверка существования ключа
            if STORE_LOCK_KEY not in node:
                node[STORE_LOCK_KEY] = None
            # Проверка блокировки объекта владельцем
            if node[STORE_LOCK_KEY] is None:
                node[STORE_LOCK_KEY] = lock_key
            else:
                self._log(u'Объект <%s> заблокирован' % name)
                return False, None
            if STORE_SECURITY_KEY in node:
                if node[STORE_SECURITY_KEY][READ_IDX] == READ_SYMB:
                    return True, node[STORE_DATA_KEY]
        except:
            log.fatal()
        return False, None

    def _getNode(self, path, storage=None):
        """
        Получить узел объекта из хранилища по пути.
        @param path: в качестве пути передается список имен.
        """
        node = ''
        try:
            # Проверка аргументов
            if not isinstance(path, list):
                self._log(u'Неверный тип аргумента path')
                return False, None
            if storage is None:
                storage = self._storage
            
            node = path[0]     # Берем первый элемент
            if node not in storage:
                return False, None
            # Если остался последний элемент, тогда возвращаем его
            if len(path) == 1:
                return True, storage[node]
            else:
                storage = storage[node][STORE_ITEMS_KEY]
                return self._getNode(path[1:], storage)
        except:
            log.fatal(u'Ошибка определения узла <%s>' % node)
        return False, None
        
    # --- Функции чтения/записи на диск ---
    def _save(self, res_filename=''):
        """
        Сохранить хранилище в ресурсном файле.
        @param res_filename: Имя ресурсного файла.
        """
        try:
            if res_filename != '':
                self.setResFilename(res_filename)
            if self._res_filename is None or self._res_filename == '':
                return False, None

            resfunc.SaveResourceText(self._res_filename, self._storage)
        except:
            log.fatal()

    def _load(self, res_filename=''):
        """
        Загрузить хранилище из ресурсного файла.
        @param res_filename: Имя ресурсного файла.
        """
        try:
            if res_filename != '':
                self.setResFilename(res_filename)
            if self._res_filename != '':
                self._storage = resfunc.LoadResourceText(self._res_filename)
        except:
            log.fatal()

    # --- Сервисные функции ---
    def Is(self, name):
        """
        Проверка существует ли такой объект.
        @param name: Имя объекта.
        """
        try:
            path = split(r'[/]', name)
            node = self._getNode(path)[1]
            if node is None:
                return False
            return True
        except:
            log.fatal()
        return False

    def canRead(self, name, lock_key=None):
        """
        Проверка возможности чтения объекта из хранилища.
        @param name: Имя объекта.
        @param lock_key: Ключ блокировки доступа.
        """
        try:
            path = split(r'[/]', name)
            node = self._getNode(path)[1]
            if node is None:
                return False
            if node[STORE_SECURITY_KEY][READ_IDX] != READ_SYMB:
                return False
            return True
        except:
            log.fatal()
        return False

    def canWrite(self, name, lock_key=None):
        """
        Проверка возможности изменения объекта из хранилища.
        @param name: Имя объекта.
        @param lock_key: Ключ блокировки доступа.
        """
        try:
            path = split(r'[/]', name)
            node = self._getNode(path)[1]
            if node is None:
                return False
            if node[STORE_SECURITY_KEY][WRITE_IDX] != WRITE_SYMB:
                return False
            return True
        except:
            log.fatal()
        return False

    def canRef(self, name, lock_key=None):
        """
        Проверка возможности получения ссылки на объект
        @param name: Имя объекта.
        @param lock_key: Ключ блокировки доступа.
        """
        try:
            path = split(r'[/]', name)
            node = self._getNode(path)[1]
            if node is None:
                return False
            if node[STORE_SECURITY_KEY][REF_IDX] != REF_SYMB:
                return False
            return True
        except:
            log.fatal()
        return False

    def printTextStorage(self):
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
            txt += self._getTextListAll(self._storage)
            txt += line
            return txt
        except:
            log.fatal(u'Ошибка преобразования в виде текста объектов ХРАНИЛИЩА')
        return None
        
    def _getTextListAll(self, storage=None, path=''):
        """
        Функция выводит в виде текста все имена объектов ХРАНИЛИЩА.
        Функция применяется при отладке.
        Используется рекурсивный вызов.
        @param storage: Текущий уровень(папка) ХРАНИЛИЩА.
        @param path: Путь до объекта.
        """
        txt = u''
        for obj_name in storage.keys():
            name = path + obj_name
            value = str(storage[obj_name][STORE_DATA_KEY])
            security = storage[obj_name][STORE_SECURITY_KEY]
            lock = u'-'
            
            if storage[obj_name][STORE_LOCK_KEY] is not None:
                lock = u'+'
            txt += u'%-20s %-40s %-9s %-7s' % (name, value, security, lock)
            if STORE_ITEMS_KEY in storage[obj_name] and \
                storage[obj_name][STORE_ITEMS_KEY] != {}:
                txt += self._getTextListAll(storage[obj_name][STORE_ITEMS_KEY],
                                            name +'/')
            txt += u'\n'
        return txt

    def _log(self, message):
        """
        Регистрация сообщения/ошибки.
        @param message: Текст сообщения.
        """
        if self._can_log:
            log.warning(message)

    # --- Функции-свойства класса ---

    def getResFilename(self):
        return self._res_filename

    def setResFilename(self, res_filename):
        if isinstance(res_filename, str):
            self._res_filename = res_filename
        else:
            self._log(u'Неверный тип аргумента res_filename')
