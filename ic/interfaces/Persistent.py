#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Интерфейс элемента хранилища.
"""


class icPersistentInterface:
    """
    Интерфейс класса, объекты которого могут сохраняться 
    в абстрактном хранилище.
    """

    def __init__(self):
        """
        Конструктор.
        """
        pass
        
    def getValue(self):
        """
        Свойства метакомпонента.
        """
        pass
        
    def setValue(self, NewValue_, NewConst_=None):
        """
        Свойства метакомпонента.
        """
        pass
        
    def Add(self, Name_=None, Type_=None):
        """
        Добавить дочерний метакомпонент.
        @param Name_: Имя добавляемого объекта,
            если None, то имя генерируется.
        @param Type_: Имя компонента, объект которого
            будет добавлен в дерево.
            Если None, то будет сделан запрос имени.
        @return: Созданный объект метакомпонента.
        """
        pass
        
    def Del(self):
        """
        Удалить метакомпонент.
        """
        pass
        
    def getPic(self):
        pass
    
    def getPic2(self):
        pass

    def getDoc(self):
        pass
        
    def rename(self, NewName_):
        """
        Переименование.
        """
        pass
        
    def View(self, *args, **kwargs):
        """
        Открыть форму просмотра метакомпонента.
        """
        pass
        
    def getItemParent(self):
        pass
        
    def Edit(self, *args, **kwargs):
        """
        Открыть форму редактирования метакомпонента.
        """
        pass
        
    def Save(self, Persistent_=None):
        """
        Сохранить в хранилище Persistent_.
        @param Persistent_: ОБъект, который необходимо сохранить.
        """
        pass
        
    def Load(self, Persistant_=None):
        """
        Загрузить из хранилище значение объекта.
        @param Persistant_: Объект, который необходимо загрузить.
        """
        pass        
    
    def SaveAllChildren(self, ParentMetaObject_=None):
        """
        Сохранить себя и все дочерние узлы.
        @param ParentMetaObject_: Сохраняемый метаобъект.
        """
        pass

    def ReLoad(self):
        """
        Перечитать все объекты из хранилища.
        """
        pass

    def Clone(self, CloneName_=None, doCopyChildren_=True):
        """
        Создать клон метаобъекта.
        @param CloneName_: Имя клона, если None,то имя генерируется.
        @param doCopyChildren_: Признак копирования дочерних узлов.
        @return: Возвращает объект клона или None в случае неудачи.
        """
        pass
        
    def isRoot(self):
        """
        Является ли метаобъект главным/рутовым?
        """
        pass

    def commit(self):
        """
        Подтвердить изменения.
        """
        pass
        
    def lock(self):
        """
        Заблокировать.
        """
        pass
        
    def unLock(self):
        """
        Разблокировать.
        """
        pass
        
    def isLock(self):
        """
        Проверить блокировку.
        """
        pass
        
    def ownerLock(self):
        """
        Владелец блокировки.
        """
        pass

    def isMyLock(self):
        """
        Моя блокировка?
        """
        pass

    # --- Поддержка интерфейса словаря ---
    def __getitem__(self, key):
        pass
        
    def __setitem__(self, key, item):
        pass
        
    def __delitem__(self, key):
        pass
        
    def has_key(self, key):
        pass

    def __contains__(self, item):
        """
        ВНИМАНИЕ! Это функция - замена has_key для Python3.
        """
        return item in self

    def keys(self):
        pass

    def items(self):
        pass
        
    def values(self):
        pass
        
    def setdefault(self, key, default=None):
        pass
        
    def get(self, key, default=None):
        pass


class icMetaComponentInterface(icPersistentInterface):
    """
    Интерфейс абстрактного метакомпонента.
    Метакомпонент может сохранять свое состояние 
    в хранилище.
    """

    def __init__(self):
        """
        Конструктор.
        """
        icPersistentInterface.__init__(self)
