#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Хранилище типовых объектов.
Хранилище представляет собой папку
организующую древовидной представление данных.
Каждай подпапка определяет узел дерева.
В узлах дерева находится файл хранилища,
который представляет собой серилизованный словарь
(см. описание библиотеки shelve).
"""

# --- Подключение библиотек ---
import shelve
import copy
import time

import ic.utils.lock
from ic.utils import ic_util
from ic.utils import ic_file
from ic.interfaces import StorageInterface as storage_interface
from ic.utils import ic_exec

from ic.kernel import io_prnt

__version__ = (0, 0, 1, 3)

# --- Константы и спецификации ---
DEFAULT_STORAGE_DIR = ic_file.getProfilePath()
FILE_STORAGE_EXT = '.db'
SYSTEM_DIR_PREFIX = '#'

# Протокол файлового хранилища
FILE_STORAGE_PROTOCOL = 2

# Режимы работы файлового хранилища
FILE_STORAGE_AUTOCOMMIT_MODE = 0    # Сохранение автоматическое
FILE_STORAGE_TRANSACT_MODE = 1      # Сохранение отключено

# Режимы работы папочного хранилища
DIR_STORAGE_AUTOCOMMIT_MODE = 0     # Сохранение автоматическое
DIR_STORAGE_TRANSACT_MODE = 1       # Сохранение отключено

# Имя файла свойств папочного хранилища
DIR_STORAGE_PROPERTY_FILE_NAME = 'property.db'
DIR_STORAGE_PROPERTY_NAME = 'property'

# Тип объекта вида хранения
OBJ_STORAGE_SRC_TYPE = 'ObjectStorageSource'
# Спецификация вида хранения
SPC_IC_OBJ_STORAGE_SRC = {'type': OBJ_STORAGE_SRC_TYPE,
                          'storage_dir': 'C:/#STORAGE',
                          }


class icFileNodeStorage(storage_interface.icElementStorageInterface):
    """
    Узел файлового хранилища.
    """

    def __init__(self):
        """
        Конструктор.
        """
        storage_interface.icElementStorageInterface.__init__(self)
        
        # Данные узла
        self._data = {'type': 'icFileNodeStorage'}
        
    def Open(self):
        """
        Открыть.
        """
        return storage_interface.icElementStorageInterface.Open(self)
        
    def Close(self):
        """
        Закрыть.
        """
        return storage_interface.icElementStorageInterface.Close(self)
        
    def setParentNode(self, ParentNode_, Name_):
        """
        Установить родительский узел.
        @param ParentNode_: Родительский узел.
        @param Name_: Имя данного узла.
        """
        return storage_interface.icElementStorageInterface.setParentNode(self, ParentNode_, Name_)
      
    def setName(self, NewName_):
        """
        Установить имя узла.
        @param NewName_: НОвое имя.
        """
        if NewName_ == self.getName():
            return
        # Переименовать в списке родителя
        if issubclass(self._ParentNode.__class__, icFileNodeStorage):
            if self.getName() in self._ParentNode._data:
                del self._ParentNode._data[self.getName()]
            self._ParentNode[NewName_] = self
        elif issubclass(self._ParentNode.__class__, icFileStorage):
            if self.getName() in self._ParentNode._children:
                del self._ParentNode[self.getName()]
            # !!!Установку/переименование делать только через _children!!!
            self._ParentNode._children[NewName_] = self
            # !!!Прочь шаловливые руки от кода !!!
        # Поменять свое имя
        self._data['property']['name'] = NewName_
        storage_interface.icElementStorageInterface.setName(self, NewName_)

    def save(self):
        """
        Сорхранить изменения в хранилище.
        """
        if self._ParentNode:
            self._ParentNode.save()

    def getData(self):
        """
        Получить данные.
        """
        data = {}
        for data_key, data_value in self._data.items():
            if issubclass(data_value.__class__, icFileNodeStorage) or\
               issubclass(data_value.__class__, icFileStorage):
                data[data_key] = data_value.getData()
            else:
                data[data_key] = copy.deepcopy(data_value)
        return data

    def setData(self, Data_):
        """
        Установить данные узла.
        """
        self._data = Data_
        # Установить имя узла,такое же как и имя объекта в нем хранящегося
        if isinstance(self._data, dict) and 'property' in self._data and \
           'name' in self._data['property']:
            self.setName(self._data['property']['name'])
        if isinstance(self._data, dict):
            for child_name in self._data.keys():
                if child_name != 'property' and child_name != 'type':
                    child = self._data[child_name]
                else:
                    continue
                if isinstance(child, dict) and \
                   'type' in child and child['type'] == 'icFileNodeStorage':
                    self._data[child_name] = icFileNodeStorage()
                    self._data[child_name].setParentNode(self, child_name)
                    self._data[child_name].setData(child)
                    
    def setProperty(self, NewProperty_):
        """
        Установить свойства узла.
        @param NewProperty_: Словарь свойств.
        """
        return self.__setitem__('property', NewProperty_)
        
    def getProperty(self):
        """
        Свойства узла.
        """
        return self.__getitem__('property')
        
    def loadProperty(self):
        """
        Загрузить свойства из хранилища.
        """
        if self._ParentNode:
            if issubclass(self._ParentNode.__class__, icFileStorage):
                self._ParentNode.ReLoad()
            elif issubclass(self._ParentNode.__class__, icFileNodeStorage):
                self._ParentNode.loadProperty()
        return self.getProperty()
        
    def saveProperty(self):
        """
        Сохранить свойства в хранилище.
        """
        self.save()
        
    # --- Поддержка интерфейса словаря ---
    def __len__(self):
        if not self.isOpen():
            self.Open()
        return len(self._data)

    def __getitem__(self, key):
        if not self.isOpen():
            self.Open()
        return self._data[str(key)]
        
    def __setitem__(self, key, item):
        if not self.isOpen():
            self.Open()
        self._data[str(key)] = item

    def __delitem__(self, key):
        if not self.isOpen():
            self.Open()
        if str(key) in self._data:
            del self._data[str(key)]

    def clear(self):
        if not self.isOpen():
            self.Open()
        self._data.clear()

    def keys(self):
        if not self.isOpen():
            self.Open()
        return self._data.keys()
        
    def update(self, dict):
        if not self.isOpen():
            self.Open()
        return self._data.update(dict)

    def has_key(self, key):
        if not self.isOpen():
            self.Open()
        return str(key) in self._data

    def __contains__(self, item):
        """
        ВНИМАНИЕ! Это функция - замена has_key для Python3.
        """
        return self.has_key(item)

    def items(self):
        if not self.isOpen():
            self.Open()
        return self._data.items()
        
    def values(self):
        if not self.isOpen():
            self.Open()
        return self._data.values()
        
    def setdefault(self, key, default=None):
        if not self.isOpen():
            self.Open()
        return self._data.setdefault(str(key), default)
        
    def get(self, key, default=None):
        if not self.isOpen():
            self.Open()
        return self._data.get(str(key), default)

    # --- Функции поддержки транзакционного механизма ---
    def transact(self):
        """
        Начать транзакцию.
        """
        if self._ParentNode:
            return self._ParentNode.transact()
            
    def commit(self):
        """
        Подтвердить транзакцию.
        """
        if self._ParentNode:
            return self._ParentNode.commit()
        
    def rollback(self):
        """
        Откат всех невыполненной транзакции.
        """
        if self._ParentNode:
            return self._ParentNode.rollback()
        
    # --- Блокировки ---
    def lock(self, Name_=None):
        """
        Заблокировать.
        ВНИМАНИЕ!!! Блокировать необходимо весь файл целиком.
        @param Name_: Имя блокируемого объекта.
        @return: Возвращает результат успешной блокировки True/False.
        """
        if self._ParentNode:
            return self._ParentNode.lock()
        return False
        
    def unLock(self, Name_=None):
        """
        Разблокировать.
        @param Name_: Имя блокируемого объекта.
        @return: Возвращает результат успешной разблокировки True/False.
        """
        if self._ParentNode:
            return self._ParentNode.unLock()
        return False


class icFileStorage(storage_interface.icElementStorageInterface):
    """
    Файловое хранилище.
    """

    # Текущее открытое файловое хранилище
    CUR_FILE_STORAGE_OPEN = None
    
    def __init__(self):
        """
        Конструктор.
        """
        storage_interface.icElementStorageInterface.__init__(self)
        self._FileName = None
        self._file = None
        self._is_open_file = False
        
        self._children = {}
        
        # Режим работы файлового хранилища
        self._mode = FILE_STORAGE_AUTOCOMMIT_MODE
        # Признак автоматического кэширования файла
        self._cache = False

    def setCache(self, Cache_=True):
        """
        Признак автоматического кэширования файла.
        """
        if Cache_ != self._cache:
            # Сначала закрыть
            self.Close()
            # Поменять признак
            self._cache = Cache_

    def getCache(self):
        """
        Признак автоматического кэширования файла.
        """
        return self._cache
        
    def Open(self):
        """
        Открытие файла хранилища.
        """
        self._open()
        storage_interface.icElementStorageInterface.Open(self)
        # Инициализация структуры файлового хранилища
        if self._file:
            for file_key in self._file.keys():
                if isinstance(self._file[file_key], dict) and \
                   'type' in self._file[file_key] and \
                   self._file[file_key]['type'] == 'icFileNodeStorage':
                    self._children[file_key] = icFileNodeStorage()
                    self._children[file_key].setParentNode(self, file_key)
                    self._children[file_key].setData(dict(self._file[file_key]))
                    
        return self._file

    def _open(self):
        """
        Функция низкоуровнего открытия.
        """
        # Если открыт другой файл, то закрыть его
        if self != icFileStorage.CUR_FILE_STORAGE_OPEN:
            if icFileStorage.CUR_FILE_STORAGE_OPEN:
                # ВНИМАНИЕ!!! Закрытие последнего файла необходимо делать для обеспечения
                # совместного доступа к разным файлам хранилища
                # Оптимизировать здесь нельзя!!!
                icFileStorage.CUR_FILE_STORAGE_OPEN._close()
                icFileStorage.CUR_FILE_STORAGE_OPEN = None
                
        self._file = shelve.open(self._FileName, protocol=FILE_STORAGE_PROTOCOL,
                                 writeback=self._cache)
        # Отметить файловое хранилище как текущее открытое
        icFileStorage.CUR_FILE_STORAGE_OPEN = self
        self._is_open_file = True
        
    def Close(self):
        """
        Закрыть.
        """
        storage_interface.icElementStorageInterface.Close(self)
        self._children = {}
        return self._close()
            
    def _close(self):
        """
        Функция низкоуровнего закрытия.
        """
        if self._file:
            if self == icFileStorage.CUR_FILE_STORAGE_OPEN:
                icFileStorage.CUR_FILE_STORAGE_OPEN = None
            ok = self._file.close()
            self._file = None
            self._is_open_file = False
            return ok
        return None
        
    def setParentNode(self, ParentNode_, Name_):
        """
        Привязать узел к родительскому.
        @param ParentNode_: Узел, в котором находится папка.
            Родительский узел.
        @param Name_: Имя узла.
        """
        storage_interface.icElementStorageInterface.setParentNode(self, ParentNode_, Name_)
        self.setFileName(Name_)

    def renameFile(self, NewFileName_):
        """
        Переименовать файл хранилища.
        """
        if NewFileName_ and ic_file.Exists(self._FileName):
            self.closeFile()
            ic_file.Rename(self._FileName, NewFileName_)
        
    def setFileName(self, Name_):
        """
        Определить имя файла по имени узла.
        """
        if self._ParentNode is not None:
            self._FileName = self._ParentNode.getNodeDir()+'/'+Name_+FILE_STORAGE_EXT
        
    def getFileName(self):
        """
        Имя файла файлового хранилища.
        """
        return self._FileName
        
    def setName(self, NewName_):
        """
        Новое имя узла.
        """
        if NewName_ == self.getName():
            return
            
        if self._ParentNode is not None:
            new_file_name = self._ParentNode.getNodeDir()+'/'+NewName_+FILE_STORAGE_EXT
            # Необходимо переименовать файл
            self.renameFile(new_file_name)

            # Если родительский узел-папочное хранилище, то необходимо
            # поменять имя текущего узла в списке родительского хранилища
            if issubclass(self._ParentNode.__class__, icDirStorage):
                if self._Name in self._ParentNode:
                    del self._ParentNode[self._Name]
                self._ParentNode[NewName_] = self
        # Обычное переименование
        self.setFileName(NewName_)
        storage_interface.icElementStorageInterface.setName(self, NewName_)

    def save(self, Data_=None):
        """
        Сорхранить изменения в хранилище.
        """
        ok = None
        
        if self._mode == FILE_STORAGE_TRANSACT_MODE:
            # Автоматическое сохранение отключено
            return ok
            
        if self._file is not None:
            # Поставить блокировку на файл
            lock_name = self._getPathList()
            self.lock(lock_name)
            
            # Сначала подготовить данные для записи, затем записать их
            Data_ = self._readyData(Data_)

            ok = self._file.update(Data_)
            self._file.sync()

            # Снять блокировку
            self.unLock(lock_name)
        return ok
    
    def ReLoad(self):
        """
        Перегрузить.
        """
        self.save()
        self.Close()
        self.Open()
        
    def _readyData(self, Data_=None):
        """
        Подготовка данных для записи.
        @param Data_: Данные (дерево узлов), которые надо записать.
        """
        # Если данные не определены, то получить их
        if Data_ is None:
            return self.getData()

        data = None
        if self._file is not None:
            data = self._get_data(Data_)
        return data
        
    def _get_data(self, DataUpdate_):
        """
        Низкоуровневая функция чтения данных из файла БД.
        """
        data = dict(self._file)
        # Добавить новые узлы в файловое хранилище
        data.update(DataUpdate_)
        for data_key in data.keys():
            if issubclass(data[data_key].__class__, icFileNodeStorage) or\
               issubclass(data[data_key].__class__, icFileStorage):
                data[data_key] = data[data_key].getData()
        return data
        
    def getData(self):
        """
        Получить данные.
        """
        data = None
        if self._file is not None:
                data = self._get_data(self._children)
        else:
            # Если файл БД существует, то он может быть
            # просто не открыт
            if ic_file.Exists(self.getFileName()):
                self.Open()
                data = self._get_data(self._children)
                
        return data
        
    def setProperty(self, NewProperty_):
        """
        Установить свойства узла.
        @param NewProperty_: Словарь свойств.
        """
        return self.__setitem__('property', NewProperty_)
        
    def getProperty(self):
        """
        Свойства узла.
        """
        return self.__getitem__('property')
        
    def loadProperty(self):
        """
        Загрузить свойства из хранилища.
        """
        self.ReLoad()
        return self.getProperty()
        
    def saveProperty(self):
        """
        Сохранить свойства в хранилище.
        """
        self.save()
        
    def Clone(self, CloneName_):
        """
        Клонировать узел.
        @param CloneName_: Имя клона.
        """
        new_file_name = ic_file.DirName(self._FileName)+'/'+CloneName_+FILE_STORAGE_EXT
        # Клонировать только если такого файла нет
        if not ic_file.Exists(new_file_name):
            self.closeFile()
            ic_file.icCopyFile(self._FileName, new_file_name, False)
            # Заменить имя узла в файле
            file = None
            try:
                file = shelve.open(new_file_name, protocol=FILE_STORAGE_PROTOCOL,
                                   writeback=self._cache)
                property = dict(file['property'])
                property['name'] = CloneName_
                file['property'] = property
                file.sync()
                file.close()
            except:
                if file:
                    file.close()
            if self._ParentNode:
                self._ParentNode.ReLoad()
        
    # --- Поддержка интерфейса словаря ---
    def __len__(self):
        if not self.isOpen():
            self.Open()
        # Проверка на низкоуровневый доступ
        if not self._is_open_file:
            self._open()
            
        if self._file:
            return len(self._file)
        return 0

    def __getitem__(self, key):
        if not self.isOpen():
            self.Open()
        # Проверка на низкоуровневый доступ
        if not self._is_open_file:
            self._open()
            
        key = str(key)
        if key in self._children.keys():
            item = self._children[key]
        else:
            item = self._file[key]
        if isinstance(item, dict) and 'type' in item and item['type'] == 'icFileNodeStorage':
            node = icFileNodeStorage()
            node.setParentNode(self, key)
            node.setData(item)
            item = node
        return item
        
    def __setitem__(self, key, item):
        if not self.isOpen():
            self.Open()
        # Проверка на низкоуровневый доступ
        if not self._is_open_file:
            self._open()
            
        # Проверка на сохранение узлов файлового хранилища
        if issubclass(item.__class__, icFileNodeStorage):
            self._children[item.getName()] = item
            item = item.getData()

        # Только если значение изменено, только тогда записать
        self._file[str(key)]=item

    def __delitem__(self, key):
        if not self.isOpen():
            self.Open()
        # Проверка на низкоуровневый доступ
        if not self._is_open_file:
            self._open()
            
        if str(key) in self._file:
            del self._file[str(key)]
        if str(key) in self._children:
            del self._children[str(key)]

    def clear(self):
        if not self.isOpen():
            self.Open()
        # Проверка на низкоуровневый доступ
        if not self._is_open_file:
            self._open()
            
        self._file.clear()

    def keys(self):
        if not self.isOpen():
            self.Open()
        # Проверка на низкоуровневый доступ
        if not self._is_open_file:
            self._open()
            
        return self._file.keys()
        
    def update(self, dict):
        if not self.isOpen():
            self.Open()
        # Проверка на низкоуровневый доступ
        if not self._is_open_file:
            self._open()
            
        for item in dict.items():
            if issubclass(item[1].__class__, icFileNodeStorage):
                self._children[item[0]] = item[1]
        if self._file is not None:
            data = self._readyData(dict)
            return self._file.update(data)
        return None
        
    def has_key(self, key):
        if not self.isOpen():
            self.Open()
        # Проверка на низкоуровневый доступ
        if not self._is_open_file:
            self._open()

        if self._file is not None:
            return str(key) in self._file
        return False

    def __contains__(self, item):
        """
        ВНИМАНИЕ! Это функция - замена has_key для Python3.
        """
        return self.has_key(item)

    def items(self):
        if not self.isOpen():
            self.Open()
        # Проверка на низкоуровневый доступ
        if not self._is_open_file:
            self._open()
            
        return self._file.items()
        
    def values(self):
        if not self.isOpen():
            self.Open()
        # Проверка на низкоуровневый доступ
        if not self._is_open_file:
            self._open()
            
        return self._file.values()
        
    def setdefault(self, key, default=None):
        if not self.isOpen():
            self.Open()
        # Проверка на низкоуровневый доступ
        if not self._is_open_file:
            self._open()
            
        return self._file.setdefault(str(key), default)
        
    def get(self, key, default=None):
        if not self.isOpen():
            self.Open()
        # Проверка на низкоуровневый доступ
        if not self._is_open_file:
            self._open()
            
        return self._file.get(str(key), default)
        
    # --- Функции блокировок ---
    def closeFile(self):
        """
        Разблокировать.
        """
        self.save()
        self._close()
        if icFileStorage.CUR_FILE_STORAGE_OPEN == self:
            icFileStorage.CUR_FILE_STORAGE_OPEN = None

    # --- Функции поддержки транзакционного механизма ---
    def transact(self):
        """
        Начать транзакцию.
        """
        self._mode = FILE_STORAGE_TRANSACT_MODE

    def commit(self):
        """
        Подтвердить транзакцию.
        """
        self._mode = FILE_STORAGE_AUTOCOMMIT_MODE

    def rollback(self):
        """
        Откат всех невыполненной транзакции.
        """
        self.Close()
        self.Open()


class icDirStorage(storage_interface.icElementStorageInterface):
    """
    Папочное хранилище типовых объектов.
    """

    def __init__(self):
        """
        Конструктор.
        """
        storage_interface.icElementStorageInterface.__init__(self)
            
        self._NodeDir = None
        # Словарь файлов хранилищ
        self._StorageDB = {}
        
        # Свойства папочного хранилища
        self.property = None

        # Режим работы папочного хранилища
        self._mode = DIR_STORAGE_AUTOCOMMIT_MODE
        
        # Признак кэширования
        self._cache = False

    def setCache(self, Cache_=True):
        """
        Признак автоматического кэширования файла.
        """
        if Cache_ != self._cache:
            # Сначала закрыть
            self.Close()
            # Поменять признак
            self._cache = Cache_
            
            # Рекурсивно поменять у всех дочерних узлов
            for child in self._StorageDB.values():
                child.setCache(self._cache)
        
    def getCache(self):
        """
        Признак автоматического кэширования файла.
        """
        return self._cache
        
    def Open(self):
        """
        Открыть узел.
        """
        self.makeNodeDir()
            
        self._StorageDB = {}
        
        list_dir = ic_file.ListDir(self._NodeDir)
        for name in list_dir:
            # Отфильтровать папки системного назначения
            if name[0] != SYSTEM_DIR_PREFIX:
                full_name = self._NodeDir+'/'+name
                if ic_file.IsDir(full_name):
                    self._StorageDB[name] = icDirStorage()
                    self._StorageDB[name].setParentNode(self, name)
                    self._StorageDB[name].Open()
                elif ic_file.IsFile(full_name):
                    if name != DIR_STORAGE_PROPERTY_FILE_NAME:
                        node_name = ic_file.SplitExt(name)[0]
                        self._StorageDB[node_name] = icFileStorage()
                        self._StorageDB[node_name].setParentNode(self, node_name)
                    else:
                        self.property = icFileStorage()
                        self.property.setParentNode(self, DIR_STORAGE_PROPERTY_NAME)

        storage_interface.icElementStorageInterface.Open(self)

    def Close(self):
        """
        Закрыть узел.
        """
        self._StorageDB = {}
        storage_interface.icElementStorageInterface.Close(self)

    def makeNodeDir(self, NodeDir_=None):
        """
        Создать папку-узел.
        """
        if NodeDir_:
            self._NodeDir = NodeDir_

        if not ic_file.Exists(self._NodeDir):
            ic_file.MakeDirs(self._NodeDir)

    def renameNodeDir(self, NewNodeDir_):
        """
        Переименовать папку.
        @param NewNodeDir_: Новая папка узла.
        """
        try:
            if not ic_file.SamePathWin(NewNodeDir_, self._NodeDir):
                if NewNodeDir_ and ic_file.Exists(self._NodeDir):
                    self.closeAllFiles()
                    ic_file.Rename(self._NodeDir, NewNodeDir_)
                    # Переименовать имя узла
        except:
            print('icDirStorage renameNodeDir ERROR')
            raise
            
    def copyNodeDir(self, NewNodeDir_):
        """
        Скопировать папку.
        @param NewNodeDir_: Новая папка узла.
        """
        try:
            if not ic_file.SamePathWin(NewNodeDir_, self._NodeDir):
                if NewNodeDir_ and ic_file.Exists(self._NodeDir):
                    self.closeAllFiles()
                    ic_file.CopyTreeDir(self._NodeDir, NewNodeDir_)
        except:
            print('icDirStorage copyNodeDir ERROR')
            raise
            
    def setName(self, NewName_):
        """
        Новое имя узла.
        """
        if NewName_ == self.getName():
            return
            
        if self._ParentNode is not None:
            new_node_dir = self._ParentNode.getNodeDir()+'/'+NewName_

            # Необходимо переименовать папку
            self.copyNodeDir(new_node_dir)
            
            if issubclass(self._ParentNode.__class__, icDirStorage):
                # Удалить старое имя из словаря
                if self._Name in self._ParentNode:
                    del self._ParentNode[self._Name]
                    
                # Прописать по новому имени
                self._ParentNode[NewName_] = self
                
        # Обычное переименование
        self.setNodeDir(NewName_)

        storage_interface.icElementStorageInterface.setName(self, NewName_)
        
        # Кроме того что необходимо поменять путь до папки
        # необходимо поменять имя файла свойств узла
        # Поменять имя файла property
        if self.property is not None:
            self.property.setFileName(self.property.getName())
            self.property['name'] = NewName_

    def getNodeDir(self):
        return self._NodeDir

    def setNodeDir(self, Name_):
        """
        Установить папку узла.
        @param Name_: Имя узла.
        """
        if self._ParentNode is not None:
            self._NodeDir = self._ParentNode.getNodeDir()+'/'+Name_
        else:
            self._NodeDir = Name_
        # Кроме того что необходимо поменять путь до папки
        # необходимо поменять имя файла свойств узла

    def setParentNode(self, ParentNode_, Name_):
        """
        Привязать узел к родительскому.
        @param ParentNode_: Узел, в котором находится папка.
            Родительский узел.
        @param Name_: Имя узла.
        """
        storage_interface.icElementStorageInterface.setParentNode(self, ParentNode_, Name_)

        self.setNodeDir(Name_)
        self.makeNodeDir()

    def save(self):
        """
        Сорхранить изменения в хранилище.
        """
        if self._mode == DIR_STORAGE_TRANSACT_MODE:
            # Автоматическое сохранение отключено
            return
        
        # Сохранить свои свойства
        if self._NodeDir and (not ic_file.Exists(self._NodeDir)):
            self.makeNodeDir()
        if self.property:
            self.property.save()
        # Сохранить все дочерние узлы
        for child in self._StorageDB.values():
            child.save()

    def ReLoad(self):
        """
        Перечитать собственное дерево объектов.
        """
        self.Close()
        self.Open()
        
    def setProperty(self, NewProperty_):
        """
        Установить свойства узла.
        @param NewProperty_: Словарь свойств.
        """
        self.property = icFileStorage()
        self.property.setParentNode(self, DIR_STORAGE_PROPERTY_NAME)
        self.property.update(NewProperty_)

    def getProperty(self):
        return dict(self.property._file)

    def reloadProperty(self):
        """
        Перегрузить свойства.
        """
        self.property.save()
        self.property.Close()
        self.property.Open()
        
    def loadProperty(self):
        """
        Загрузить свойства из хранилища.
        """
        self.reloadProperty()
        return self.getProperty()
     
    def saveProperty(self):
        """
        Сохранить свойства в хранилище.
        """
        if self.property:
            self.property.save()
    
    def Clone(self, CloneName_):
        """
        Клонировать узел.
        @param CloneName_: Имя клона.
        """
        new_dir_name = ic_file.DirName(self._NodeDir)+'/'+CloneName_
        # Клонировать только если такого директория нет
        if not ic_file.Exists(new_dir_name):
            self.closeAllFiles()
            ic_file.CloneDir(self._NodeDir, new_dir_name, False)
            # Установить имя в файле свойств
            file = None
            try:
                file = shelve.open(new_dir_name+'/'+DIR_STORAGE_PROPERTY_FILE_NAME,
                                   protocol=FILE_STORAGE_PROTOCOL, writeback=self._cache)
                file['name'] = CloneName_
                file.sync()
                file.close()
            except:
                if file:
                    file.close()
            if self._ParentNode:
                self._ParentNode.ReLoad()
        
    # --- Поддержка интерфейса словаря ---
    def __len__(self):
        if not self.isOpen():
            self.Open()
        return len(self._StorageDB)
        
    def __getitem__(self, key):
        if not self.isOpen():
            self.Open()
        return self._StorageDB.get(str(key), None)
        
    def __setitem__(self, key, item):
        if not self.isOpen():
            self.Open()
        key = str(key)
        
        if isinstance(item, dict):
            # Проверка на свойства объекта папочного хранилища
            self.setProperty(item)
        else:
            # Файловое/папочное хранилище следующего уровня
            self._StorageDB[key] = item
            self._StorageDB[key].setParentNode(self, key)

    def __delitem__(self, key):
        if not self.isOpen():
            self.Open()
        
        if issubclass(self._StorageDB[str(key)].__class__, icFileStorage):
            # Проверка на удаление файла
            self._StorageDB[str(key)].closeFile()
            file_name = self._StorageDB[str(key)].getFileName()
            if ic_file.Exists(file_name) and ic_file.IsFile(file_name):
                ic_file.Remove(file_name)
        elif issubclass(self._StorageDB[str(key)].__class__, icDirStorage):
            # Проверка на удаление директории
            self._StorageDB[str(key)].closeAllFiles()
            dir_name = self._StorageDB[str(key)].getNodeDir()
            if ic_file.Exists(dir_name) and ic_file.IsDir(dir_name):
                ic_file.RemoveTreeDir(dir_name, 1)
        if str(key) in self._StorageDB:
            del self._StorageDB[str(key)]

    def has_key(self, key):
        if not self.isOpen():
            self.Open()
        return str(key) in self._StorageDB
        
    def __contains__(self, item):
        """
        ВНИМАНИЕ! Это функция - замена has_key для Python3.
        """
        return self.has_key(item)

    def keys(self):
        if not self.isOpen():
            self.Open()
        return self._StorageDB.keys()

    def update(self, dict):
        if not self.isOpen():
            self.Open()
            
        for item in dict.items():
            self.__setitem__(item[0], item[1])
        
    def items(self):
        if not self.isOpen():
            self.Open()
        return self._StorageDB.items()
        
    def values(self):
        if not self.isOpen():
            self.Open()
        return self._StorageDB.values()
        
    def setdefault(self, key, default=None):
        if not self.isOpen():
            self.Open()
        return self._StorageDB.setdefault(str(key), default)
        
    def get(self, key, default=None):
        if not self.isOpen():
            self.Open()
        return self._StorageDB.get(str(key), default)
        
    # --- Функции блокировок ---
    def closeAllFiles(self):
        """
        Разблокировать все узлы.
        """
        if self._StorageDB:
            for storage in self._StorageDB.values():
                if issubclass(storage.__class__, icFileStorage):
                    storage.closeFile()
                if issubclass(storage.__class__, icDirStorage):
                    storage.property.closeFile()
                    storage.closeAllFiles()
        if self.property:
            self.property.closeFile()

    # --- Транзакционный механизм ---
    def transact(self):
        """
        Начать транзакцию.
        """
        self._mode = DIR_STORAGE_TRANSACT_MODE

        if self.property:
            self.property.transact()
        for child in self._StorageDB.values():
            child.transact()
            
    def commit(self):
        """
        Подтвердить транзакцию.
        """
        self._mode = DIR_STORAGE_AUTOCOMMIT_MODE

        if self.property:
            self.property.commit()
        for child in self._StorageDB.values():
            child.commit()

    def rollback(self):
        """
        Откат всех невыполненной транзакции.
        """
        self.Close()
        self.Open()


class icTreeDirStorage(icDirStorage):
    """
    Хранилище типовых объектов в виде дерева каталогов.
    Для системного использования.
    """

    def __init__(self, StorageDir_=None):
        """
        Конструктор.
        """
        # Система блокировки
        self._lockSys = None
        icDirStorage.__init__(self)
        self.setParentNode(None, StorageDir_)
        # Инициализировать папку-узел для
        self.makeStorageDir(StorageDir_)
        
    def makeStorageDir(self, StorageDir_=None):
        """
        Создать папку-узел.
        """
        # Создать системму блокировки
        if StorageDir_:
            self._lockSys = ic.utils.lock.icLockSystem(StorageDir_+'/#lock')
        return self.makeNodeDir(StorageDir_)

    def clearStorageDir(self, StorageDir_=None):
        """
        Полное очищение главной папки.
        """
        if StorageDir_ is None:
            StorageDir_ = self._NodeDir
        if ic_file.Exists(StorageDir_):
            try:
                ic_file.RemoveTreeDir(StorageDir_, True)
                ic_file.MakeDirs(StorageDir_)
            except:
                io_prnt.outErr(u'Ошибка очистки папки объектного хранилища <%s>' % StorageDir_)
        
    def getStorageDir(self):
        return self.getNodeDir()
       
    def save(self):
        """
        Сорхранить изменения в хранилище.
        Сохранение свойств не происходит.
        """
        if self._mode == DIR_STORAGE_TRANSACT_MODE:
            # Автоматическое сохранение отключено
            return
            
        # Сохранить свои свойства
        if self._NodeDir and (not ic_file.Exists(self._NodeDir)):
            self.makeNodeDir()
        # !!! У корня не надо сохранять свойства!!!

        # Сохранить все дочерние узлы
        for child in self._StorageDB.values():
            child.save()
            
    # --- Функции блокировок ---
    def lock(self, Name_=None):
        """
        Заблокировать ресурс папочного хранилища.
        @param Name_: Имя блокируемого объекта.
        """
        if Name_ is None:
            Name_ = self.nameLock()
        if self._lockSys and Name_:
            return self._lockSys.lockFileRes(Name_)
        return False
        
    def unLock(self, Name_=None):
        """
        Разблокировать ресурс папочного хранилища.
        @param Name_: Имя блокируемого объекта.
        """
        if Name_ is None:
            Name_ = self.nameLock()
        if self._lockSys and Name_:
            return self._lockSys.unLockFileRes(Name_)
        return False
        
    def isLock(self, Name_=None):
        """
        Проверить блокировку на ресурс.
        """
        if Name_ is None:
            Name_ = self.nameLock()
        if self._lockSys and Name_:
            return self._lockSys.isLockFileRes(Name_)
        return False
        
    def ownerLock(self, Name_=None):
        """
        Владелец блокировки.
        @return: Имя компьютера-владельца блокировки. Если None, то блокирвки нет.
        """
        if Name_ is None:
            Name_ = self.nameLock()
        if self._lockSys and Name_:
            lock_rec = self._lockSys.getLockRec(Name_)
            if lock_rec and isinstance(lock_rec, dict):
                return lock_rec['computer']
        return None
        
    def isMyLock(self, Name_=None):
        """
        Проверка, является ли эта блокировка моей.
        """
        return ic.utils.lock.ComputerName() == self.ownerLock(Name_)
        
    def unLockAllMy(self):
        """
        Удалить все мои блокировки.
        """
        if self._lockSys:
            return self._lockSys.unLockAllMy()
        return False
        
    def Connect(self):
        """
        Открыть узел.
        """
        return self.Open()


class icObjectStorageSource(icTreeDirStorage,
                            storage_interface.icObjectStorageSourceInterface):
    """
    Хранилище типовых объектов.
    Стандартизует интерфейс к хранению объектов.
    """

    def __init__(self, Res_=None):
        """
        Конструктор.
        """
        storage_interface.icObjectStorageSourceInterface.__init__(self, Res_)
        self._spc = ic_util.SpcDefStruct(SPC_IC_OBJ_STORAGE_SRC, self._res)
        storage_dir = ic_file.AbsolutePath(ic_exec.ExecuteCode(self._spc['storage_dir'], self))
        icTreeDirStorage.__init__(self, storage_dir)


class icObjStorageSrc(icObjectStorageSource):
    """
    Хранилище типовых объектов.
    Стандартизует интерфейс к хранению объектов.
    Доступ по имени.
    """

    def __init__(self, Name_=None):
        """
        Конструктор.
        """
        from ic.utils import resource
        res = resource.icGetRes(Name_, 'src', nameRes=Name_)
        icObjectStorageSource.__init__(self, res)
