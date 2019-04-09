#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Модуль прикладной системы.
Базовый интерфейс редактируемой панели плана.
Автор(ы):
"""
import ic.interfaces.icobjectinterface as icobjectinterface
#from ic.dlg import progress
import ic.dlg.ic_proccess_dlg as ic_proccess_dlg

# Версия
__version__ = (0, 0, 0, 1)

#--- Функции
#--- Классы
COL_GRID_KEY = 8

def CountParPlan(metaObj):
    """
    Вычисление весовых коэфициентов плана по агрегированным суммам планов.
    @type metaObj: C{icMetaItem}
    @param metaObj: Указатель на метаобъект классификатора мониторов.
    """
    if not metaObj.isRoot():
        #print '>>> Enter To CountParPlan', metaObj.value.metatype, metaObj.value.summa
        S = metaObj.value.summa
        Sk = metaObj.value.kol
        
    L = len(metaObj.values())
    
    for obj in metaObj.values():
        if not metaObj.isRoot():
            #print '   ::: name, typ:', obj.value.name, obj.value.summa, S, L
            if S <> 0:
                obj.value.w = L*obj.value.summa/S
                
            if Sk <> 0:
                obj.value.w_kol = L*obj.value.kol/Sk
                
        CountParPlan(obj)

def CountWeightBySum(metaObj):
    """
    Вычисляем весовой коэфициент по сумме и другим элементам плана.
    """
    parentObj = metaObj._Parent
    
    if not parentObj.isRoot():
        #   Вычисляем суммы
        S=0
        Sw=0
        Sk=0
        Swk=0
        lst = parentObj.values()
            
        for el in lst:
        
            #   Если сумма 0, то и вес тоже должен быть 0
            if el.value.summa == 0:
                el.value.w = 0
            if el.value.kol == 0:
                el.value.w_kol = 0
                
            S += el.value.summa
            Sk += el.value.kol
            Sw += el.value.w
            Swk += el.value.w_kol
            
        Sp = Sw - metaObj.value.w
        Spk = Swk - metaObj.value.w_kol
        
        if S <> 0:
            alph = metaObj.value.summa/S
        else:
            alph = 0
            
        if Sk <> 0:
            alph_k = metaObj.value.kol/Sk
        else:
            alph_k = 0
            
        if Sp > 0:
            metaObj.value.w = alph*Sp/(1-alph)
        else:
            metaObj.value.w = 1
            
        if Spk > 0:
            metaObj.value.w_kol = alph_k*Spk/(1-alph_k)
        else:
            metaObj.value.w_kol = 1
    
def recount_prnt(metaObj, bIndicator=True, bSave=True):
    """
    Пересчитывает суммы, весовые коэфициенты и количественные параметры
    родительских планов.
    """
    parentObj = metaObj._Parent
    
    if not parentObj.isRoot():
        #   Вычисляем суммы
        S=0
        Sk=0
        lst = parentObj.values()
            
        for el in lst:
            S += el.value.summa
            Sk += el.value.kol
        
        #   Пересчитываем весовой коэфициент w
        if parentObj.value.w<>0 and parentObj.value.summa<>0:
            k = parentObj.value.summa/parentObj.value.w
            parentObj.value.w = S/k
        
        parentObj.value.summa = S

        #   Пересчитываем весовой коэфициент w_kol
        if parentObj.value.w_kol<>0 and parentObj.value.kol<>0:
            k = parentObj.value.kol/parentObj.value.w_kol
            parentObj.value.w_kol = Sk/k
        
        parentObj.value.kol = Sk
            
        #   Рекурсивно вычисляем суммы в родительских элементах
        recount_prnt(parentObj, False, bSave)
        
    #   У корневого элемента вызываем функцию синхронизации
    elif bSave:
        metaObj.SaveAllChildren()

def recount_prnt_sum(metaObj, bIndicator=True, bSave=True):
    """
    Пересчитывает суммы родительских планов.
    """
    parentObj = metaObj._Parent
    
    if not parentObj.isRoot():
        #   Вычисляем суммы
        S=0
        lst = parentObj.values()
            
        for el in lst:
            S += el.value.summa
        
        #   Пересчитываем весовой коэфициент w
        if parentObj.value.w<>0 and parentObj.value.summa<>0:
            k = parentObj.value.summa/parentObj.value.w
            parentObj.value.w = S/k
        
        parentObj.value.summa = S
            
        #   Рекурсивно вычисляем суммы в родительских элементах
        recount_prnt_sum(parentObj, False, bSave)
        
    #   У корневого элемента вызываем функцию синхронизации
    elif bSave:
        metaObj.SaveAllChildren()

def recount_prnt_kol(metaObj, bIndicator=True, bSave=True):
    """
    Пересчитывает суммы родительских планов в натуральных показателях.
    """
    parentObj = metaObj._Parent
    if not parentObj.isRoot():
        #   Вычисляем суммы
        S=0
        lst = parentObj.values()
            
        for el in lst:
            S += el.value.kol
        
        #   Пересчитываем весовой коэфициент w
        if parentObj.value.w_kol<>0 and parentObj.value.kol<>0:
            k = parentObj.value.kol/parentObj.value.w_kol
            parentObj.value.w_kol = S/k
        
        parentObj.value.kol = S
            
        #   Рекурсивно вычисляем суммы в родительских элементах
        recount_prnt_kol(parentObj, False, bSave)
        
    #   У корневого элемента вызываем функцию синхронизации
    elif bSave:
        metaObj.SaveAllChildren()

def recount_child_sum(metaObj, bIndicator=True):
    """
    Пересчитывает суммы дочерних планов.
    """
    lst = metaObj.values()
    S = metaObj.value.summa
    
    #   Вычисляем сумму весовых коэфициентов
    if lst:
        sw = reduce(lambda x,y: x+y, map(lambda x: x.value.w, lst))
            
        #   Вычисляем суммы
        if sw <> 0:
            for i, el in enumerate(lst):
                el.value.summa = el.value.w*S/sw
                
                #   Рекурсивно вычисляем дочерние элементы
                recount_child_sum(el, False)

def recount_child_kol(metaObj, bIndicator=True):
    """
    Пересчитывает суммы дочерних планов в натуральных показателях.
    """
    lst = metaObj.values()
    S = metaObj.value.kol
    
    #   Вычисляем сумму весовых коэфициентов
    if lst:
        sw = reduce(lambda x,y: x+y, map(lambda x: x.value.w_kol, lst))
            
        #   Вычисляем суммы
        if sw <> 0:
            for i, el in enumerate(lst):
                el.value.kol = el.value.w_kol*S/sw
                
                #   Рекурсивно вычисляем дочерние элементы
                recount_child_kol(el, False)

#--- Виды пересчетов
# После любых изменений
id_recount_evt_default = 0
# После изменения суммы или количества
id_recount_evt_changed_summa = 1
# После изменения коэфициентов
id_recount_evt_changed_w = 2
# Пересчет по требованию
id_recount_evt_button = 3

id_recount_evt_dct = {
    id_recount_evt_default:'После любых изменений',
    id_recount_evt_changed_summa:'После изменения суммы или количества',
    id_recount_evt_changed_w:'После изменения коэфициентов',
    id_recount_evt_button:'Пересчет по требованию (соотв. кнопка)'}

#--- Виды нормировок коэфициентов
# Без нормировки
id_norma_default = 0
# В процентах
id_norma_procent = 1
# Нормировка на 1
id_norma1 = 2
# По максимуму - максимум 1
id_norma_max = 3
# По минимуму - минимум 1
id_norma_min = 4

id_norma_dct = {
    id_norma_default:'Без нормировки',
    id_norma_procent:'В процентах',
    id_norma1:'Нормировка на 1',
    id_norma_max:'Нормировка по максимуму',
    id_norma_min:'Нормировка по минимуму'}

class IEdtPanel(icobjectinterface.icObjectInterface):
    
    def __init__(self, parent, resource, metaObj=None, tree=None, evalSpace=None, bIndicator=False):
        """
        """
        self.metaObj = metaObj
        self.tree = tree
        self.itemTree = None
        self.__changed = False
        
        #   Тип нормировки коэфициентов
        self._normaType = id_norma_default
        self.idNormaDct = id_norma_dct
        #   Тип пересчета значений значений 
        self._recountType = id_recount_evt_default
        self.idRecountDct = id_recount_evt_dct
        
        #   Вызываем конструктор базового класса
        icobjectinterface.icObjectInterface.__init__(self, parent, resource, evalSpace, bIndicator)

    def getNormaType(self):
        """
        Возвращает тип нормировки.
        """
        return self._normaType

    def getRecountEventType(self):
        """
        Возвращает тип нормировки.
        """
        return self._normaType
        
    def IsChanged(self):
        """
        Признак изменения метообъекта.
        """
        return self.metaObj.getRoot().isValueChanged()

    def LoadChildData(self):
        """
        Загружаем данные по дочерним планам.
        """
        pass
        
    def setChangePrz(self, prz=True):
        """
        Устанавливает признак изменения панели.
        """
        self.__changed = prz
        
    def SaveData(self):
        """
        Сохранение плана.
        """
        pass

    def ReCount(self, bRefresh=False, metaObj=None):
        """
        Функция пересчитывает значения дочерних элементов плана.
        """
        if not metaObj:
            metaObj = self.metaObj

        if self.metaObj and self.metaObj.isMyLock():
            self.metaObj.transact()
            self.SaveData(bRefresh)
            self.RecountChildSum(metaObj=metaObj)
            self.RecountParentSum(metaObj=metaObj, bSave=False)
            self.metaObj.commit()
            
            self.LoadChildData()

    def ReCountKol(self, bRefresh=False, metaObj=None):
        """
        Функция пересчитывает количественные значения дочерних элементов плана.
        """
        if not metaObj:
            metaObj = self.metaObj

        if self.metaObj and self.metaObj.isMyLock():
            self.metaObj.transact()
            self.SaveData(bRefresh)
            self.RecountChildKol(metaObj=metaObj)
            self.RecountParentKol(metaObj=metaObj, bSave=False)
            self.metaObj.commit()
            
            self.LoadChildData()
    
    def RecountChildSum(self, metaObj=None, bIndicator=True):
        """
        Пересчитывает суммы дочерних планов.
        """
        if not metaObj:
            metaObj = self.metaObj

        recount_child_sum(metaObj, bIndicator)
#        ic_proccess_dlg.ProccessFunc(self.parent,'Пересчитываем суммы дочерних планов',
#            recount_child_sum, (metaObj, bIndicator), {}, bAutoIncr=True)

    def RecountChildKol(self, metaObj=None, bIndicator=True):
        """
        Пересчитывает натуральные показатели дочерних планов.
        """
        if not metaObj:
            metaObj = self.metaObj

        recount_child_kol(metaObj, bIndicator)
#        ic_proccess_dlg.ProccessFunc(self.parent,'Пересчитываем кол. показ. дочерних планов',
#            recount_child_kol, (metaObj, bIndicator), {}, bAutoIncr=True)

    def RecountParentSum(self, metaObj=None, bIndicator=True, bSave=True):
        """
        Пересчитывает суммы родительских планов.
        """
        if not metaObj:
            metaObj = self.metaObj

        recount_prnt_sum(metaObj, bIndicator, bSave)
#        ic_proccess_dlg.ProccessFunc(self.parent,'Пересчитываем суммы родительских планов',
#                    recount_prnt_sum, (metaObj, bIndicator, bSave), {}, bAutoIncr=True)

    def RecountParentKol(self, metaObj=None, bIndicator=True, bSave=True):
        """
        Пересчитывает суммы родительских планов в натуральных показателях.
        """
        if not metaObj:
            metaObj = self.metaObj
        
        recount_prnt_kol(metaObj, bIndicator, bSave)        
#        ic_proccess_dlg.ProccessFunc(self.parent,'Пересчитываем кол. показ. родительских планов',
#                    recount_prnt_kol, (metaObj, bIndicator, bSave), {}, bAutoIncr=True)
            
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
            
            if self.metaObj.has_key(r[COL_GRID_KEY]):
                mm = self.metaObj[r[COL_GRID_KEY]]
                old_descr = mm.value.description
                
                mm.value.description = r[1].strip()
                mm.value.w = float(r[2])
                mm.value.summa = float(r[3])
                mm.value.w_kol = float(r[4])
                mm.value.kol = float(r[5])
                print '---------------> mm.value.ei, r[6]=', mm.value.ei, r[6]
                mm.value.ei = r[6]
                mm.value.marja = float(r[7])
                #mm.Save()
                
                if not bRefresh :
                    bRefresh = mm.isValueChanged()
                    print '>>> mm.isValueChanged()=', bRefresh
                    
                    if self.itemTree and self.tree and mm.value.description <> old_descr:
                        item = self.tree.GetMetaObjItem(mm, self.itemTree)
                        print '>>> item=', item, mm.value.description
                        if item:
                            print ' Change text:', mm.value.description
                            self.tree.SetItemText(item, mm.value.description, 0)
                    
                if name <> r[COL_GRID_KEY]:
                    mm.rename(name)
                    bRefresh = True
        
        if bRefresh:
            print '>>> ValChanged SaveAllChildren()-before'
            self.metaObj.SaveAllChildren()
            print '>>> ValChanged SaveAllChildren()'
        elif self.metaObj.isValueChanged():
            print '>>> ValChanged Save'
            self.metaObj.Save()

        return bRefresh

    def setNormaType(self, typ):
        """
        Возвращает тип нормировки.
        """
        self._normaType = typ

    def setRecountEventType(self, typ):
        """
        Возвращает тип нормировки.
        """
        self._normaType = typ