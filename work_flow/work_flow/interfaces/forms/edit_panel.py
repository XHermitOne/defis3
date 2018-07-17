#!/usr/bin/env python
#  -*- coding: utf-8 -*-
'''
Базовый интерфейс редактируемой панели.
Автор(ы):
'''
import ic.interfaces.icobjectinterface as icobjectinterface
#from ic.dlg import progress
import ic.dlg.ic_proccess_dlg as ic_proccess_dlg

# Версия
__version__ = (0, 0, 0, 1)

#--- Функции
#--- Классы
COL_GRID_KEY = 8


class IEditPanel(icobjectinterface.icObjectInterface):
    '''
    Панель редактирования метообъекта.
    '''
    
    def __init__(self, parent, resource, metaObj=None, tree=None, evalSpace=None, bIndicator=False):
        """
        """
        self.metaObj = metaObj
        self.tree = tree
        self.itemTree = None
        self.__changed = False
        
        #   Вызываем конструктор базового класса
        icobjectinterface.icObjectInterface.__init__(self, parent, resource, evalSpace, bIndicator)

    def IsChanged(self):
        """
        Признак изменения метообъекта.
        """
        return self.metaObj.getRoot().isValueChanged()

    def LoadChildData(self):
        """
        Загружаем данные по дочерним.
        """
        pass
        
    def LoadData(self):
        """
        Загружаем данные.
        """
        pass
        
    def setChangePrz(self, prz=True):
        """
        Устанавливает признак изменения панели.
        """
        self.__changed = prz
        
    def SaveData(self):
        """
        Сохранение данных.
        """
        pass

            
    def RefreshPanel(self):
        """
        Функция обнавления представления панели.
        """
        if self.tree and self.itemTree:
            if self.tree.IsExpanded(self.itemTree):
                self.tree.Collapse(self.itemTree)
                self.tree.Expand(self.itemTree)
                
            self.tree.SelectItem(self.tree.root)
            self.tree.SelectItem(self.itemTree)
            
    def SaveChildrenData(self, data, bRefresh=False):
        """
        Сохраняет данные дочерних элементов, если они были изменены.
        
        @type data: C{list}
        @param data: Данные грида.
        @type bRefresh: C{bool}
        @param bRefresh: Признак полного обновления ветки дерева. Иногда нужно
            принудительно обновить.
        @rtype: C{bool}
        @return: Признак того, что данные были изменены пользователем.
        """
        for r in data:
            name = r[0]
            
            if r[COL_GRID_KEY] in self.metaObj:
                mm = self.metaObj[r[COL_GRID_KEY]]
                old_descr = mm.value.description
                
                mm.value.description = r[1].strip()
                mm.value.w = float(r[2])
                mm.value.summa = float(r[3])
                mm.value.w_kol = float(r[4])
                mm.value.kol = float(r[5])
                mm.value.ei = r[6]
                mm.value.marja = float(r[7])
                
                if not bRefresh :
                    bRefresh = mm.isValueChanged()
                    print('>>> mm.isValueChanged()=', bRefresh)
                    
                    if self.itemTree and self.tree and mm.value.description <> old_descr:
                        item = self.tree.GetMetaObjItem(mm, self.itemTree)
                        print('>>> item=', item, mm.value.description)
                        if item:
                            print(' Change text:', mm.value.description)
                            self.tree.SetItemText(item, mm.value.description, 0)
                    
                if name <> r[COL_GRID_KEY]:
                    mm.rename(name)
                    bRefresh = True
        
        if bRefresh:
            print('>>> ValChanged SaveAllChildren()-before')
            self.metaObj.SaveAllChildren()
            print('>>> ValChanged SaveAllChildren()')
        elif self.metaObj.isValueChanged():
            print('>>> ValChanged Save')
            self.metaObj.Save()

        return bRefresh
