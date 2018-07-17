#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Источник данных справочника в виде дерева.
"""

# Version
__version__ = (0, 0, 0, 3)

# Imports
import ic
from ic.interfaces import ictreedatasourceinterface

from ic.utils import util


def _str2unicode(Str_):
    """
    Т.к. мы ориентированы на контролы отображающие юникод,
    тогда надо делать корректное преобразование строк.
    """
    if isinstance(Str_, unicode):
        return Str_
    else:
        return unicode(str(Str_), 'utf-8')


class icSpravItemDataSource(ictreedatasourceinterface.icTreeItemDataSourceInterface):
    """
    Элемент справочника.
    """

    def __init__(self, ParentItem_, Code_):
        """
        Конструктор.
        @param ParentItem_: Родительский элемент.
        """
        ictreedatasourceinterface.icTreeItemDataSourceInterface.__init__(self)
        
        # Родительский элемент
        self._parent_item = ParentItem_
        # Код справочника, соответствующий этому элементу
        self._code = Code_
        # Данные, прикрепленные к этому элементу
        self._data = None
        # Дочерние элементы
        self._children = None
    
    def getRecDict(self):
        """
        Прикрепленные данные к элементу в виде словаря.
        """
        sprav = self.getRoot().getSprav()
        if sprav:
            storage = sprav.getStorage()
            if storage:
                rec_dict = storage.getRecByCod(self.getCode())
                return rec_dict
        return None
        
    def getCode(self):
        """
        Код справочника, соответствующего этому элементу.
        """
        return self._code
        
    def getParent(self):
        """
        Родительский элемент.
        """
        return self._parent_item
        
    def setData(self, Data_):
        """
        Установить данные, прикрепленные к элементу.
        """
        self._data = Data_
        
    def getDescription(self):
        """
        Описание данных, прикрепленных к элементу.
        """
        return self._data[1]
    
    def getLabel(self, LabelFunc_=None):
        """
        Надпись в контроле, соответствующая данному элементу.
        """
        if LabelFunc_:
            return LabelFunc_
        # По умолчанию надпис: Код+Наименование
        # return _str2unicode(self._code)+u' '+_str2unicode(self.getDescription())
        # Изменено для тупых пользователей: Наименование
        return _str2unicode(self.getDescription())

    def hasChildren(self):
        """
        Есть у элемента дочерние элементы?
        """
        root = self.getRoot()
        sprav = root.getSprav()
        if sprav:
            return sprav.isSubCodes(self._code)
        return False

    def _loadChildren(self, Code_=None, AutoSort_=True):
        """
        Згрузить данные дочерних элементов.
        @param AutoSort_: Сортировать записи автоматически по коду?
        @return: Возвращает список объектов дочерних элементов.
        """
        children = []
        root = self.getRoot()
        sprav = root.getSprav()
        if sprav:
            storage = sprav.getStorage()
            tab_data = storage.getLevelTable(Code_)
            if AutoSort_:
                tab_data.sort()
            for rec in tab_data:
                code = rec[0]
                item = icSpravItemDataSource(self, code)
                item.setData(rec)
                
                children.append(item)
        
        return children

    def getChildren(self):
        """
        Дочерние элементы.
        """
        if self._children is None:
            self._children = self._loadChildren(self._code)
        return self._children
  
    def getLevelIdx(self):
        """
        Индекс уровня справочника, к которому принадлежит элемент.
        """
        sprav = self.getRoot().getSprav()
        if sprav:
            level = sprav.getLevelByCod(self.getCode())
            if level:
                return level.getIndex()
        return -1

    def findItemByCode(self, Code_):
        """
        Найти рекурсивно элемент по коду.        
        @return: Возвращает объект элемента дерева данных.
        """
        find_child = None
        for child in self.getChildren():
            if child.getCode() == Code_:
                return child
            if child.hasChildren():
                find_child = child.findItemByCode(Code_)
                if find_child is not None:
                    return find_child
        return None


class icSpravTreeDataSource(ictreedatasourceinterface.icTreeDataSourceInterface):
    """
    Источник данных справочника в виде дерева.
    """

    def __init__(self, SpravPsp_, RootCode_=None):
        """
        Конструктор.
        @param SpravPsp_: Паспорт справочника - источника данных.
        @param RootCode_: Код корневого элемента справочника.
        """
        ictreedatasourceinterface.icTreeDataSourceInterface.__init__(self)
        
        self._sprav = self._createSprav(SpravPsp_)
        self._children = self._loadChildren(RootCode_)

    def getSprav(self):
        """
        Объект справочника.
        """
        return self._sprav

    def getSpravDescription(self):
        """
        Описание справочника.
        """
        if self._sprav:
            return self._sprav.getDescription()
        return None

    def _createSprav(self, SpravPsp_):
        """
        Создание справочника.
        """
        kernel = ic.getKernel()
        if kernel:
            return kernel.Create(SpravPsp_)
        return None
    
    def _loadChildren(self, Code_=None):
        """
        Згрузить данные дочерних элементов.
        @return: Возвращает список объектов дочерних элементов.
        """
        children = []
        if self._sprav:
            storage = self._sprav.getStorage()
            tab_data = storage.getLevelTable(Code_)
            for rec in tab_data or []:
                code = rec[0]
                item = icSpravItemDataSource(self, code)
                item.setData(rec)
                children.append(item)
        
        return children
        
    def getChildren(self):
        """
        Дочерние элементы.
        """
        return self._children
    
    def find(self, FindStr_):
        """
        Поиск элемента по строке.
        @return: Функция возвращает лейбл найденного элемента и None, если 
            элемент не найден.
        """
        if self._sprav:
            code = FindStr_
            find_dict = self._sprav.Find(code, ['cod', 'name'])
            if not find_dict:
                label = None
            else:
                # label = _str2unicode(find_dict['cod'])+u' '+_str2unicode(find_dict['name'])
                # Переделано на НАИМЕНОВАНИЕ
                label = _str2unicode(find_dict['name'])
            return label
        return None
    
    def find_record(self, FindStr_, FieldName_=None):
        """
        Поиск записи по значению поля.
        @param FindStr_: Искомое значение.
        @param FieldName_: Имя поля, если None, то ищется по коду.
        @return: Возвращает словарь искомой записи или None если запись не найдена.
        """
        if self._sprav:
            if FieldName_ is None:
                rec_dict = self._sprav.getRec(FindStr_)
            else:
                rec_dict = self._sprav.getStorage().getRecByFieldValue(FieldName_, FindStr_)
            return rec_dict
        return None

    def findItemByCode(self, Code_):
        """
        Найти рекурсивно элемент по коду.        
        @return: Возвращает объект элемента дерева данных.
        """
        for child in self.getChildren():
            if child.getCode() == Code_:
                return child
            if child.hasChildren():
                find_child = child.findItemByCode(Code_)
                if find_child is not None:
                    return find_child
        return None


def test():
    """
    Тестовая функция.
    """
    ok_login = ic.Login(None, None, 'c:/defis/NSI/NSI', True)
    print('START SpravTreeDataSource TEST ... Login:', ok_login)
    if ok_login:
        sprav_psp = (('Sprav', 'Regions', None, 'nsi_sprav.mtd', 'NSI'),)
        data_src = icSpravTreeDataSource(sprav_psp)
        print('CHILDREN:', data_src.getChildren())
        
        ic.Logout()        
        print('STOP SpravTreeDataSource TEST ... OK')


if __name__ == '__main__':
    test()
