#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Интерфейс элемента хранилища типовых объектов.
"""

# --- Подключение библиотек ---

__version__ = (0, 0, 0, 3)


# --- Описание интерфейсов ---
class icElementStorageInterface:
    """
    Интерфейс элемента хранилища типовых объектов.
    """

    def __init__(self):
        """
        Конструктор.
        """
        self._ParentNode = None
        self._Name = None
        self._isOpen = False
        # Признак необходимости сохранения
        self._mustSave = False
        
    def Open(self):
        """
        Открыть.
        """
        self._isOpen = True
        
    def Close(self):
        """
        Закрыть.
        """
        self._isOpen = False
        
    def isOpen(self):
        """
        Открыт элемент хранилища?
        """
        return self._isOpen
        
    def setParentNode(self, ParentNode_, Name_):
        """
        Установить родительский узел.
        @param ParentNode_: Родительский узел.
        @param Name_: Имя данного узла.
        """
        self._ParentNode = ParentNode_
        self._Name = Name_

    def mustSave(self, MustSave_=True):
        """
        Установить/убрать признак необходимости сохранения.
        """
        self._mustSave = MustSave_
        
    def getName(self):
        return self._Name
    
    def setName(self, Name_):
        self._Name = Name_
        
    def save(self):
        """
        Сорхранить изменения в хранилище.
        """
        pass
        
    def _getPathList(self, CurPath_=None):
        """
        Определить полный путь текущего элемента хранилища.
        @param CurPath_: Путь текущего элемента хранилища.
        """
        if CurPath_ is None:
            CurPath_ = [self.getName()]
        else:
            CurPath_ = [self.getName()]+CurPath_
        if self._ParentNode:
            return self._ParentNode._getPathList(CurPath_)
        return CurPath_
        
    def setProperty(self, NewProperty_):
        """
        Установить свойства узла.
        @param NewProperty_: Словарь свойств.
        """
        pass
        
    def getProperty(self):
        """
        Свойства узла.
        """
        pass
        
    def Clone(self, CloneName_):
        """
        Клонировать узел.
        @param CloneName_: Имя клона.
        """
        pass
        
    # --- Функции блокироовки ---
    def nameLock(self):
        """
        Имя блокировки.
        """
        path_lst = self._getPathList()
        if path_lst:
            return '_'.join(path_lst)
        else:
            return self.getName()
        
    def lock(self, Name_=None):
        """
        Заблокировать.
        @param Name_: Имя блокируемого объекта.
        @return: Возвращает результат успешной блокировки True/False.
        """
        if Name_ is None:
            Name_ = self.nameLock()
        if self._ParentNode:
            return self._ParentNode.lock(Name_)
        return False
        
    def unLock(self, Name_=None):
        """
        Разблокировать.
        @param Name_: Имя блокируемого объекта.
        @return: Возвращает результат успешной разблокировки True/False.
        """
        if Name_ is None:
            Name_ = self.nameLock()
        if self._ParentNode:
            return self._ParentNode.unLock(Name_)
        return False
        
    def isLock(self, Name_=None):
        """
        Проверить блокировку.
        """
        if Name_ is None:
            Name_ = self.nameLock()
        if self._ParentNode:
            # Если родительский узел не заблокирован,
            # то проверить блокировку на текущий узел
            if not self._ParentNode.isLock():
                return self._ParentNode.isLock(Name_)
            else:
                return True
        return False
    
    def ownerLock(self, Name_=None):
        """
        Владелец блокировки.
        @return: Имя компьютера-владельца блокировки. Если None, то блокирвки нет.
        """
        if Name_ is None:
            Name_ = self.nameLock()
        if self._ParentNode:
            # Если родительский узел не заблокирован,
            # то проверить блокировку на текущий узел
            if not self._ParentNode.isLock():
                return self._ParentNode.ownerLock(Name_)
            else:
                return self._ParentNode.ownerLock()
        return None
        
    def isMyLock(self, Name_=None):
        """
        Проверка, является ли эта блокировка моей.
        """
        if Name_ is None:
            Name_ = self.nameLock()
        if self._ParentNode:
            # Если родительский узел не заблокирован,
            # то проверить блокировку на текущий узел
            if not self._ParentNode.isLock():
                return self._ParentNode.isMyLock(Name_)
            else:
                return self._ParentNode.isMyLock()
        return None
        
    # --- Функции поддержки транзакционного механизма ---
    def transact(self):
        """
        Начать транзакцию.
        """
        pass
        
    def commit(self):
        """
        Подтвердить транзакцию.
        """
        pass
        
    def rollback(self):
        """
        Откат всех невыполненной транзакции.
        """
        pass


class icObjectStorageSourceInterface:
    """
    Тип хранилища типовых объектов.
    Стандартизует интерфейс к виду хранения объектов.
    """

    def __init__(self, Resource_=None):
        """
        Конструктор.
        """
        # Ресурс
        self._res = Resource_
        self._isOpen = False
        self._Name = None
        
    def Connect(self):
        """
        Соединиться.
        """
        pass
        
    def CloseConnection(self):
        """
        Закрыть соединение.
        """
        pass

    def Open(self):
        """
        Открыть.
        """
        self._isOpen = True
        
    def Close(self):
        """
        Закрыть.
        """
        self._isOpen = False
        
    def isOpen(self):
        """
        Открыт элемент хранилища?
        """
        return self._isOpen
        
    def Init(self):
        """
        Инициализация объекта.
        """
        pass
        
    def getName(self):
        return self._Name
        
    def save(self):
        """
        Сорхранить изменения в хранилище.
        """
        pass
        
    # --- Функции блокироовки ---
    def lock(self, Name_):
        """
        Заблокировать.
        @param Name_: Имя блокируемого объекта.
        @return: Возвращает результат успешной блокировки True/False.
        """
        pass
        
    def unLock(self, Name_):
        """
        Разблокировать.
        @param Name_: Имя блокируемого объекта.
        @return: Возвращает результат успешной разблокировки True/False.
        """
        pass
        
    # --- Функции поддержки транзакционного механизма ---
    def transact(self):
        """
        Начать транзакцию.
        """
        pass
        
    def commit(self):
        """
        Подтвердить транзакцию.
        """
        pass
        
    def rollback(self):
        """
        Откат всех невыполненной транзакции.
        """
        pass


class icObjectStorageInterface:
    """
    Интерфейс абстрактного хранилища объектов.
    Аналог Dataset/Table.
    """

    def __init__(self, Resource_=None):
        """
        Конструктор.
        @param Resource_: Ресурс описания объекта.
        """
        # Ресурс
        self._res = Resource_
