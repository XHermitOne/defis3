#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Интерфейс источника данных для абстрактного контрола дерева.
"""

# --- Imports ---
# --- Constants ---


# --- Classes ---
class icTreeItemDataSourceInterface(object):
    """
    Интерфейс источника данных для элемента дерева.
    Данный интерфейс должен поддерживать интерфейс словаря и списка.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструтор.
        """
        pass
    
    def getData(self):
        """
        Данные, соответствующие узлу.
        """
        assert None, 'Abstract method getData in class %s!' % self.__class__.__name__
        
    def setData(self,Data_):
        """
        Установить данные соответствующие узлу.
        """
        assert None, 'Abstract method setData in class %s!' % self.__class__.__name__

    def getChildren(self):
        """
        Список дочерних элементов.
        """
        assert None, 'Abstract method getChildren in class %s!' % self.__class__.__name__
        
    def __getitem__(self, i):
        return self.getChildren()[i]
    
    def __len__(self):
        return len(self.getChildren())
    
    def getParent(self):
        """
        Родительский элемент.
        """
        assert None, 'Abstract method getParent in class %s!' % self.__class__.__name__
        
    def getRoot(self):
        """
        Корневой элемент.
        """
        if self.isRoot():
            return self
        else:
            parent = self.getParent()
            if parent:
                return parent.getRoot()
        return None
        
    def isRoot(self):
        """
        Проверка является текущий элемент корневым.
        """
        return self.getParent() is None
    
    def hasChildren(self):
        """
        Есть у элемента дочерние элементы?
        """
        assert None, 'Abstract method hasChildren in class %s!' % self.__class__.__name__


class icTreeDataSourceInterface(icTreeItemDataSourceInterface):
    """
    Интерфейс источника данных для абстрактного контрола дерева.
    Данный интерфейс должен поддерживать интерфейс словаря и списка.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        icTreeItemDataSourceInterface.__init__(self, *args, **kwargs)
    
    def getParent(self):
        """
        Родительский элемент.
        """
        # У корня дерева нет родительского элемента
        return None
