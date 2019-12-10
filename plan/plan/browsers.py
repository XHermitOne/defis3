#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль прикладной системы.
"""

import ic.components.user.objects.icmetatreebrows as brows
import plan.interfaces.IManagePlans as iplan
import plan.interfaces.IODBSprav as IODBSprav
import ic.storage.objstore as objstore
import ic.utils.system_cache as ic_cache

# Версия
__version__ = (0, 1, 1, 1)


# --- Функции
def getCanContainLst(modifId, metatype, bBuff=True, plan_sys = None):
    """
    Возвращает список типов компонентов, которые могут содержатся в
    определенном компоненте - разрешающее правило. Список генерится по
    объекту описания модификации плана.

    :type modifId: C{string}
    :param modifId: Идентификатор модификации плана.
    :type metatype: C{string}
    :param metatype: Тип узла метадерева планов.
    :type bBuff: C{bool}.
    :param bBuff: Признак разрешающий брать значения из буфера.
    """
    #   Список, описывающий структуру модификации
    #   Пример: ['p1', 'p2', 'p3']
    # print '<!>.....<!>', modifId, metatype
    lst = None
    spr = IODBSprav.getModifLst(bBuff, plan_sys=plan_sys)
    for r in spr:
        id, descr, pl, struct = r
        if id == modifId:
            lst = eval(struct)
            break
            
    if lst and metatype in lst:
        i = lst.index(metatype)
        
        if i+1 < len(lst):
            return [lst[i+1]]
    
    return []


def getModifIdLst(plan_sys):
    """
    Возвращает список идентификаторов модификаций планов.
    """
    lst = IODBSprav.getModifLst(plan_sys=plan_sys)
    if lst:
        return [x[0] for x in lst]
    else:
        return []


# --- Классы
class icPlanMenager_old:
    """
    Класс менеджера планов.
    """
    def __init__(self, metaclass, modif_id=None, plan_sys=None):
        """
        Конструктор.
        
        :param modif_id: Идентификатор текущей модификации планов.
        :param plan_sys: Имя системы планирования, определяет имя хранилища, где
            будут храниться описания модификаций планов.
        """
        self.plan_sys = plan_sys
        self.metaclass = metaclass
        self.metaObj = metaclass.getObject()
        self._modifPlanId = modif_id
        
        #   Устанавливаем ссылку у метакласса на менеджер планов
        metaclass.planMenager = self
        
        if self.metaObj:
            self._baseStorageName = self.metaObj.getRoot().getStorage().getNodeDir()
        else:
            self._baseStorageName = None

        #   Чистим буфер модификаций
        ic_cache.systemCache.clear('IODBSprav')
    
    def getCanContainLst(self, modifId, metatype, bBuff=True):
        """
        Возвращает список типов компонентов, которые могут содержатся в
        определенном компоненте - разрешающее правило. Список генерится по
        объекту описания модификации плана.
        """
        print('================ getCanContainLst=', modifId, self.plan_sys)
    
        return getCanContainLst(modifId, metatype, bBuff=True, plan_sys=self.plan_sys)
        
    def getDescrDct(self):
        """
        Возвращает словарь описаний модификаций.
        """
        lst = IODBSprav.getModifLst(plan_sys=self.plan_sys)
        if not lst:
            lst = [['m1', 'Модификация 1', 'm1', '[]']]
            
        # self._modificationLst = lst
        return dict([x[:2] for x in lst])
        
    def getModifLst(self, modifId):
        """
        """
        spr = IODBSprav.getModifLst(plan_sys=self.plan_sys)
        for r in spr:
            id, descr, pl, struct = r
            if id == modifId:
                lst = eval(struct)
                return lst
        
    def getModifPlanId(self):
        """
        """
        return self._modifPlanId
        
    def setMetaplanById(self, id=None):
        """
        Возвращает указатель на базовый либо модифицированный план.
        
        :rtype: C{ic.components.user.ic_metatree_wrp.icMetaTree}
        :return: Возвращает указатель на базовый план.
        """
        if self._baseStorageName:
            if id in (None, '__base__'):
                storage_name = self._baseStorageName
            else:
                storage_name = self._baseStorageName+'_'+id
                
            metatree = self.metaObj.getRoot()
            object_storage = objstore.CreateObjectStorageByDir(storage_name)
            metatree.setStorage(object_storage)
            self._modifPlanId = id
            return metatree


class icPlanMenager:
    """
    Класс менеджера планов.
    """
    def __init__(self, metaclass, modif_id=None, plan_sys=None, plan_mod=None):
        """
        Конструктор.
        
        :param modif_id: Идентификатор текущей модификации планов.
        :param plan_sys: Имя подсистемы планирования.
        :type plan_mod: C{icplanmodifmanager.PlanModifManager}
        :param plan_mod: Cистема планирования - объект определяет модификации планов.
        """
        self.plan_sys = plan_sys
        self.plan_mod = plan_mod
        print('--------- plan_mod in icPlanMenager=', plan_mod)
        self.metaclass = metaclass
        self.metaObj = metaclass.getObject()
        self._modifPlanId = modif_id
        
        #   Устанавливаем ссылку у метакласса на менеджер планов
        metaclass.planMenager = self
        
        if self.metaObj:
            self._baseStorageName = self.metaObj.getRoot().getStorage().getNodeDir()
        else:
            self._baseStorageName = None
#
#        #   Чистим буфер модификаций
#        ic_cache.systemCache.clear('IODBSprav')
    
    def getCanContainLst(self, modifId, metatype, bBuff=True):
        """
        Возвращает список типов компонентов, которые могут содержатся в
        определенном компоненте - разрешающее правило. Список генерится по
        объекту описания модификации плана.
        """
        if self.plan_mod:
            lst = self.plan_mod.getCanContainLst(modifId, metatype)
            print('=====>>> getCanContainLst', lst)
            return lst
        return []

    def getDescrDct(self):
        """
        Возвращает словарь описаний модификаций.
        """
        if self.plan_mod:
            return self.plan_mod.getDescrDct()
        return {}
            
    def getModifPlanId(self):
        """
        """
        return self._modifPlanId

    def getModifLst(self, id):
        """
        """
        if self.plan_mod:
            return self.plan_mod.getModifLst(id)
        
    def setMetaplanById(self, id=None):
        """
        Возвращает указатель на базовый либо модифицированный план.
        
        :rtype: C{ic.components.user.ic_metatree_wrp.icMetaTree}
        :return: Возвращает указатель на базовый план.
        """
        if self._baseStorageName:
            if id in (None, '__base__'):
                storage_name = self._baseStorageName
            else:
                storage_name = self._baseStorageName+'_'+id
                
            metatree = self.metaObj.getRoot()
            object_storage = objstore.CreateObjectStorageByDir(storage_name)
            metatree.setStorage(object_storage)
            self._modifPlanId = id
            return metatree


class icMultiSrcBrows(brows.MetaTreeBrows, icPlanMenager):
    """
    Базовый класс для браузеров подсистем планирования и мониторинга.
    Браузер с возможностью переключения между несколькими базами.
    """
    def __init__(self, parent, metatype=None, bPanelBuff=True, metaclass=None,
                 treeRootTitle=None, treeLabels=None, plan_sys=None,
                 default_id=None, **par):
        """
        Конструктор.
        
        :type parent: C{wx.Window}
        :param parent: Указатель на родительское окно.
        :type metatype: C{string}
        :param metatype: Имя метатипа.
        :type bPanelBuff: C{string}
        :param bPanelBuff: Признак буферизации панелей.
        :param metaclass: Интерфейс к метоописанию дереву планов. Если данный
            атрибут определен, то параметр <metatype> игнорируется.
        :param treeRootTitle: Заголовок корневого элемента дерева.
        :param treeLabels: Заголовки колонок TreeListCtrl.
        :param plan_sys: Имя системы планирования, определяет имя хранилища, где
            будут храниться описания модификаций планов.
        """
#        #   Указатель на интерфейс к дереву планов
#        self.metaclass = metaclass
        metaObj = metaclass.getObject()
        icPlanMenager.__init__(self, metaclass, plan_sys=plan_sys, **par)
        
        brows.MetaTreeBrows.__init__(self, parent, metatype, bPanelBuff, metaObj,
                                     treeRootTitle, treeLabels, **par)

        self.default_id = default_id
        
    def choiceFuncVariantChoice(self, event):
        """
        Функция обрабатывает событие <onChoice>.
        """
        ctrl = self.GetNameObj('variantChoice')
        tree = self.GetNameObj('plansTreeCtrl')
        # Определяем идентификатор плана
        id = ctrl.GetValue()
        
        if tree.treeDict:
            #   Пересоздаем методерево - оно должно быть настроено на
            #   другую модификацию плана (другой источник, другая структура)
            #   Перегружаем методерево
            if self.setMetaplanById(id):
                # tree = self.GetNameObj('plansTreeCtrl')
                print('..... ReLoadRoot record_id=', id)
                tree.ReLoadRoot()
                
                # print '...... re variantChoice onChoice storage_name=', storage_name
        
    def intiVariantChoice(self):
        """
        Инициализирует список модификаций планов.
        """
#        lst = IODBSprav.getModifLst(plan_sys=self.plan_sys)
#        if not lst:
#            lst = [['m1','Модификация 1','m1','[]']]
#            
#        self._modificationLst = lst
#        varDict = dict([x[:2] for x in lst])
        varDict = self.getDescrDct()
        varDict['__base__'] = '<Базовый план>'
        choice = self.GetNameObj('variantChoice')
        choice.setDictRepl(varDict)
        
    def mouseClickFuncManageBtn(self, event):
        """
        Функция обрабатывает событие <mouseClick>.
        """
        pass
        
    def OnInitFuncVariantChoice(self, event):
        """
        Функция обрабатывает событие <?>.
        """
        self.intiVariantChoice()
        ctrl = self.GetNameObj('variantChoice')
        
        tree = self.GetNameObj('plansTreeCtrl')
        if tree and self.default_id:
            self.setMetaplanById(self.default_id)
            ctrl.SetValue(self.default_id)
            tree.ReLoadRoot()
        else:
            ctrl.setSelection(0)

        # self.choiceFuncVariantChoice(event)

        # print '...... re variantChoice onInnit'
        return None
        
    def RefreshTree(self):
        """
        
        """
        pass

    def setVariantById(self, modif_id):
        """
        Функция обрабатывает событие <onChoice>.
        """
        ctrl = self.GetNameObj('variantChoice')
        ctrl.SetValue(modif_id)


class icMonitoringBrows(icMultiSrcBrows):
    """
    Браузер для подсистемы мониторинга.
    """
    def __init__(self, parent, metatype=None, bPanelBuff=True, metaclass=None,
                 treeRootTitle=None, treeLabels=None, plan_sys=None, **par):
        """
        Конструктор.
        
        :type parent: C{wx.Window}
        :param parent: Указатель на родительское окно.
        :type metatype: C{string}
        :param metatype: Имя метатипа.
        :type bPanelBuff: C{string}
        :param bPanelBuff: Признак буферизации панелей.
        :param metaclass: Интерфейс к метоописанию дереву планов. Если данный
            атрибут определен, то параметр <metatype> игнорируется.
        :param treeRootTitle: Заголовок корневого элемента дерева.
        :param treeLabels: Заголовки колонок TreeListCtrl.
        :param plan_sys: Имя системы планирования, определяет имя хранилища, где
            будут храниться описания модификаций планов.
        """
        #   Функции пересчета модификаций планов по базовому плану
        #   1. Пересчет модификации плана за один месяц
        self.recountFunc = None
        #   2. Пересчет модификации плана за год
        self.recountModifPlanYear = None
        #   3. Пересчет всех модификаций плана за один месяц
        self.recountAllModifPlanMnth = None

        icMultiSrcBrows.__init__(self, parent, metatype, bPanelBuff, metaclass,
                                 treeRootTitle, treeLabels, plan_sys=plan_sys, **par)

        self.GetNameObj('manageBtn').Show(False)


class icPlanBrows(icMultiSrcBrows):
    """
    Браузер для подсистемы планирования.
    """
    def __init__(self, parent, metatype=None, bPanelBuff=True, metaclass=None,
                    treeRootTitle=None, treeLabels=None, plan_sys='Modif2', **par):
        """
        Конструктор.
        
        :type parent: C{wx.Window}
        :param parent: Указатель на родительское окно.
        :type metatype: C{string}
        :param metatype: Имя метатипа.
        :type bPanelBuff: C{string}
        :param bPanelBuff: Признак буферизации панелей.
        :param metaclass: Интерфейс к метоописанию дереву планов. Если данный
            атрибут определен, то параметр <metatype> игнорируется.
        :param treeRootTitle: Заголовок корневого элемента дерева.
        :param treeLabels: Заголовки колонок TreeListCtrl.
        :param plan_sys: Имя системы планирования, определяет имя хранилища, где
            будут храниться описания модификаций планов.
        """
        #   Функция пересчета модифицированного плана по базовому плану
        self.recountFunc = None

        icMultiSrcBrows.__init__(self, parent, metatype, bPanelBuff, metaclass,
                                 treeRootTitle, treeLabels, plan_sys=plan_sys, **par)
        
        self.GetNameObj('manageBtn').Show(False)
        
    def mouseClickFuncManageBtn(self, event):
        """
        Функция обрабатывает событие <mouseClick>.
        """
        ctrl = self.GetNameObj('variantChoice')
        print('............. self.metaclass:', self.metaclass)
        try:
            plan_struct_lst = self.metaclass.plan_struct_lst
            
        except:
            print('WARRNING: Attribute Error in <self.metaclass.plan_struct_lst>')
            plan_struct_lst = None
            
        cls = iplan.IManagePlans(ctrl, metaplan_lst=plan_struct_lst, 
                                browser=self, plan_sys = self.plan_sys)
        dlg = cls.GetNameObj('ManageDialog')
        # print '.... dlg', dlg
        
        # cls.setRecountFunc(self._recountFunc)
        
        old = ctrl.GetValue()
        dlg.ShowModal()
        self.intiVariantChoice()
        # print '.... Can Contain List [p2,"mYear"] :', self.getCanContainLst('p2', 'mYear')
        if old and old in ctrl.getDictRepl().keys():
            ctrl.SetValue(old)
        else:
            ctrl.setSelection(0)
        
        self.choiceFuncVariantChoice(event)
        dlg.Destroy()
