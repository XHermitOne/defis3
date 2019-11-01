#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Источник данных справочника в виде дерева.
"""

import ic
from ic.interfaces import ictreedatasourceinterface

from ic.log import log

# Version
__version__ = (0, 1, 1, 5)


def _str2unicode(text):
    """
    Т.к. мы ориентированы на контролы отображающие юникод,
    тогда надо делать корректное преобразование строк.
    """
    if isinstance(text, str):
        return text
    elif isinstance(text, bytes):
        return text.decode('utf-8')
    return str(text)


class icSpravItemDataSource(ictreedatasourceinterface.icTreeItemDataSourceInterface):
    """
    Элемент справочника.
    """

    def __init__(self, parent_item, code):
        """
        Конструктор.
        @param parent_item: Родительский элемент.
        """
        ictreedatasourceinterface.icTreeItemDataSourceInterface.__init__(self)
        
        # Родительский элемент
        self._parent_item = parent_item
        # Код справочника, соответствующий этому элементу
        self._code = code
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
        
    def setData(self, data):
        """
        Установить данные, прикрепленные к элементу.
        """
        self._data = data
        
    def getDescription(self):
        """
        Описание данных, прикрепленных к элементу.
        """
        root = self.getRoot()
        sprav = root.getSprav()
        if sprav:
            storage = sprav.getStorage()
            level_idx = sprav.getLevelByCod(self.getCode()).getIndex()
            rec = storage.getSpravFieldDict(self._data, level_idx=level_idx)
            return rec['name']
        return u'Не определено'
    
    def getLabel(self, label_func=None):
        """
        Надпись в контроле, соответствующая данному элементу.
        """
        if label_func:
            return label_func
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

    def _loadChildren(self, code=None, bAutoSort=True):
        """
        Згрузить данные дочерних элементов.
        @param bAutoSort: Сортировать записи автоматически по коду?
        @return: Возвращает список объектов дочерних элементов.
        """
        children = []
        root = self.getRoot()
        sprav = root.getSprav()
        if sprav:
            level_idx = sprav.getLevelByCod(code).getIndex() + 1 if code else 0
            storage = sprav.getStorage()
            tab_data = storage.getLevelTable(code)
            if bAutoSort:
                try:
                    # Произвести сортировку данных таблицы по полю кода
                    # tab_data.sort()
                    i_cod = storage.getSpravFieldNames(level_idx=level_idx).index('cod')
                    tab_data = sorted(tab_data, key=lambda rec: rec[i_cod])
                except ValueError:
                    log.fatal(u'Ошибка сортировки данных таблицы по полю кода. Уровень [%d]' % level_idx)
            for rec in tab_data:
                rec_dict = storage.getSpravFieldDict(rec, level_idx=level_idx)
                child_code = rec_dict['cod']
                if sprav.isActive(child_code):
                    # log.debug(u'1. Уровень %d: <%s : %s> %s' % (level_idx, code, child_code, str(rec_dict)))
                    item = icSpravItemDataSource(self, child_code)
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
            code = self.getCode()
            # log.debug(u'Код <%s : %s>' % (str(code), type(code)))
            level = sprav.getLevelByCod(code)
            if level:
                return level.getIndex()
        return -1

    def findItemByCode(self, code):
        """
        Найти рекурсивно элемент по коду.        
        @return: Возвращает объект элемента дерева данных.
        """
        find_child = None
        for child in self.getChildren():
            if child.getCode() == code:
                return child
            if child.hasChildren():
                find_child = child.findItemByCode(code)
                if find_child is not None:
                    return find_child
        return None


class icSpravTreeDataSource(ictreedatasourceinterface.icTreeDataSourceInterface):
    """
    Источник данных справочника в виде дерева.
    """

    def __init__(self, sprav_psp, root_code=None):
        """
        Конструктор.
        @param sprav_psp: Паспорт справочника - источника данных.
        @param root_code: Код корневого элемента справочника.
        """
        ictreedatasourceinterface.icTreeDataSourceInterface.__init__(self)
        
        self._sprav = self._createSprav(sprav_psp)
        self._children = self._loadChildren(root_code)

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

    def _createSprav(self, sprav_psp):
        """
        Создание справочника.
        """
        kernel = ic.getKernel()
        if kernel:
            return kernel.Create(sprav_psp)
        return None
    
    def _loadChildren(self, code=None):
        """
        Згрузить данные дочерних элементов.
        @return: Возвращает список объектов дочерних элементов.
        """
        children = []
        if self._sprav:
            storage = self._sprav.getStorage()
            tab_data = storage.getLevelTable(code)
            for rec in tab_data or []:
                level_idx = self._sprav.getLevelByCod(code).getIndex() + 1 if code else 0
                rec_dict = storage.getSpravFieldDict(rec, level_idx=level_idx)
                child_code = rec_dict['cod']
                # log.debug(u'2. Уровень %d: <%s : %s> %s' % (level_idx, code, child_code, str(rec_dict)))
                item = icSpravItemDataSource(self, child_code)
                item.setData(rec)
                children.append(item)
        
        return children
        
    def getChildren(self):
        """
        Дочерние элементы.
        """
        return self._children
    
    def find(self, find_text):
        """
        Поиск элемента по строке.
        @return: Функция возвращает лейбл найденного элемента и None, если 
            элемент не найден.
        """
        if self._sprav:
            code = find_text
            find_dict = self._sprav.Find(code, ['cod', 'name'])
            if not find_dict:
                label = None
            else:
                # label = _str2unicode(find_dict['cod'])+u' '+_str2unicode(find_dict['name'])
                # Переделано на НАИМЕНОВАНИЕ
                label = _str2unicode(find_dict['name'])
            return label
        return None
    
    def find_record(self, find_text, field_name=None):
        """
        Поиск записи по значению поля.
        @param find_text: Искомое значение.
        @param field_name: Имя поля, если None, то ищется по коду.
        @return: Возвращает словарь искомой записи или None если запись не найдена.
        """
        if self._sprav:
            if field_name is None:
                rec_dict = self._sprav.getRec(find_text)
            else:
                rec_dict = self._sprav.getStorage().getRecByFieldValue(field_name, find_text)
            return rec_dict
        return None

    def findItemByCode(self, code):
        """
        Найти рекурсивно элемент по коду.        
        @return: Возвращает объект элемента дерева данных.
        """
        for child in self.getChildren():
            if child.getCode() == code:
                return child
            if child.hasChildren():
                find_child = child.findItemByCode(code)
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
