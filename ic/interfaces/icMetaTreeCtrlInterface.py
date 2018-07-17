#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Интерфейс работы с методеревьями для TreeCtrl, TreeListCtrl.
"""

import wx
import ic.imglib.common as common
import ic.components.icwidget as icwidget
import time
from ic.kernel import io_prnt
import ic.dlg.ic_proccess_dlg as ic_proccess_dlg
import uuid


class MetaTreeCtrlInterface:
    """
    """
    def __init__(self, *arg, **kwarg):
        """
        Конструктор.
        """
        # Буфер справочников
        self.spravDict = {}
        # Буфер картинок
        self._picDict = {}
        # Список удаленных узлов
        self._delItemList = []

        #   Признак разрешающий редактировать дерево
        self._bEditMode = True
        #   Признак заполнения буфера
        self.bObjBuff = False
        #   Ссылка на реестр
        self.__reestr = None
        #   Максимальное количество уровеней. -1 - не ограниченное количество 
        #   уровней
        self.max_level = -1
        
        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        self.fldridx = fldridx = il.Add(common.imgFolder)
        self.fldropenidx = fldropenidx = il.Add(common.imgFolderOpen)
        self.fileidx = fileidx = il.Add(common.imgBlank)
        self.curidx = curidx = il.Add(common.imgPage)
        self.AssignImageList(il)

        #   Определяем корень
        self.root = self.AddRoot(self.titleRoot)
        self.SetItemImage(self.root, fldridx, which = wx.TreeItemIcon_Normal)
        self.SetItemImage(self.root, fldropenidx, which = wx.TreeItemIcon_Expanded)
        self.LoadTree()
   
    def addBranch(self, root, res, level=0, start_level=0):
        """
        Добавляет ветку в дерево.
        """
        if level > 1:
            return root

        id_pic, id_exp_pic = (self.fldridx, self.fldropenidx)
        lst = self.spravDict
            
        #   Если структура в интерфейсе списка
        if 0 <= self.max_level <= start_level + level:
            return root
        
        elif self.isList(res):
            for indx, el in enumerate(res):
                nm = self.getElementName(el, indx)
                child = self.AppendItem(root, nm, id_pic)
                self.SetItemImage(child, id_exp_pic, wx.TreeItemIcon_Expanded)
                self.SetPyData(child, (level+start_level, el))

                self.addBranch(child, el, level+1, start_level)
                
        #   Если структура в интерфейсе словаря
        elif self.isDict(res):
            lst = res.keys()
            lst.sort()
            for i, key in enumerate(lst):
                el = res[key]
                bmpLst = self.getBitmapLst()
                bmp1, bmp2 = (None, None)
                #
                if issubclass(el.__class__, icwidget.icSimple):
                    try:
                        bmp1 = el.getPic()
                        bmp2 = el.getPic2()
                        nm = el.value.description
                    except:
                        nm = el.value.name
                else:
                    try:
                        nm = lst[level][key]
                    except:
                        nm = str(key)

                if bmp1:
                    id_pic = self.GetImageId(bmp1)
                if bmp2:
                    id_exp_pic = self.GetImageId(bmp2)
                
                child = self.AppendItem(root, nm, id_pic)
                self.SetItemImage(child, id_exp_pic, wx.TreeItemIcon_Expanded)
                self.SetPyData(child, (level+start_level, el))
                self.addBranch(child, 0, level+1, start_level)
        else:
            child = self.AppendItem(root, str(res), self.fileidx)
            self.SetItemImage(child, self.curidx, wx.TreeItemIcon_Expanded)
            self.SetPyData(child, (level+start_level, res))

        return root
        
    def GetMetaObjItem(self, metaObj, parent_item):
        """
        Находит элемент дерева по метообъекту.
        """
        item, cookie = self.GetFirstChild(parent_item)

        if item.IsOk():
            lev, data = self.GetPyData(item)
            if data == metaObj:
                return item
        
        while 1:
            
            item, cookie = self.GetNextChild(parent_item, cookie)
            
            if item.IsOk():
                lev, data = self.GetPyData(item)
                if data == metaObj:
                    return item
            else:
                break
                
    def GetImageId(self, img):
        """
        """
        if img in self._picDict:
            id_pic = self._picDict[img]
        else:
            il = self.GetImageList()
            id_pic = il.Add(img)
            self._picDict[img] = id_pic
            
        return id_pic
        
    def GetDelItemLst(self):
        """
        """
        return self._delItemList

    def GetEditMode(self):
        """
        Возвращает признак разрешающий или запрещающий редактировать дерево.
        """
        return self._bEditMode
    
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        
        if self.IsSizer() and self.child:
            prs.icResourceParser(self.parent, self.child, self, evalSpace=self.evalSpace,
                                 bCounter=bCounter, progressDlg=progressDlg)
        elif self.child:
            prs.icResourceParser(self, self.child, None, evalSpace=self.evalSpace,
                                 bCounter=bCounter, progressDlg=progressDlg)
                                
    def getElementName(self, res, indx):
        """
        Возвращает имя элемента списка.
        """
        return 'element %s:' % str(indx)
        
    def getBitmapLst(self):
        """
        Возвращает список картинок, используемых в дереве.
        """
        il = self.GetImageList()
        n = il.GetImageCount()
        lst = range(n)
        for i in range(n):
            lst[i] = il.GetBitmap(i)
        
        return lst

    def GetReestr(self):
        """
        Устанавливаем указатель на реестр.
        """
        return self.__reestr
        
    def isDict(self, res):
        """
        Признак словарного интерфейса.
        """
        try:
            if res.resource['type'] in ('MetaTree', 'MetaItem', 'Reestr', 'ReestrObject'):
                return True
        except:
            if isinstance(res, dict):
                return True
            
        return False

    def isList(self, res):
        """
        Признак интерфейса последовательности.
        """
        return isinstance(res, list)
        
    def LoadTree(self, treeDict=None):
        """
        Заполняем дерево.
        
        @type treeDict: C{dictionary}
        @param treeDict: Словарно-списковая структура, отображаемая в дереве.
        """
        if not treeDict:
            treeDict = self.treeDict
        else:
            self.treeDict = treeDict
        
        self.SetPyData(self.root, (-1, treeDict))
        self.DeleteChildren(self.root)
        
        if treeDict:
            self.addBranch(self.root, treeDict)
        else:
            self._testTree()

    def ObjDestroy(self):
        """
        """
        if self.labels:
            self.wcols = range(len(self.labels))
            
            for indx, label in enumerate(self.labels):
                self.wcols[indx] = self.GetColumnWidth(indx)
    
            self.SaveUserProperty('wcols', self.wcols)

    def OnActivated(self, evt):
        """
        Обработчик события wx.EVT_TREE_ITEM_ACTIVATED, атрибут=activated.
        Событие посылается после выбора определенного пункт дерева по <Enter> или
        двойному щелчку мыщи.
        """
        self.evalSpace['evt'] = evt
        self.evalSpace['self'] = self
        ret, val = self.eval_attr('activated')
        if ret and val:
            evt.Skip()
        elif not ret:
            evt.Skip()

    def OnAddItem(self, evt):
        """
        Добавление нового узла.
        """
        id = evt.GetId()
        lst = self.treeDict.getRoot().components.values()
        for obj in lst:
            if obj.GetUniqId() == id:
                
                item = self.GetSelection()
                level, prnt_obj = self.GetPyData(item)
                id = None
                new_obj = prnt_obj.Add(id, obj.name)
                child = self.AppendItem(item, new_obj.name, self.fldridx)
                self.SetItemImage(child, self.fldropenidx, which=wx.TreeItemIcon_Expanded)
                self.SetPyData(child, (level+1, new_obj))

                #   Инициализируем документ, если он есть
                ifs = new_obj.GetComponentInterface()
                if ifs and hasattr(ifs, 'doc'):
                    ifs.doc.init_data()
                    new_obj.value.doc_uuid = ifs.doc.getDocId()
                    io_prnt.outLog(u'>>> Инициализирован документ: <%s> id=%s' % (ifs.doc.name, new_obj.value.doc_uuid))
                    new_obj.Save()
                
                #   Обновляем дерево
                if self.IsExpanded(item):
                    self.Collapse(item)
                    self.Expand(item)
                else:
                    self.Expand(item)
                self.SelectItem(item)
                break
                
    def OnCloneItem(self, evt):
        """
        Клонирование объекта плана.
        """
        item = self.GetSelection()
        level, data = self.GetPyData(item)
        clone = data.Clone()
        self.ReLoadParentItemData(item)
    
    def OnCopy(self, evt):
        """
        """
        item = self.GetSelection()
        level, data = self.GetPyData(item)
        self.bObjBuff = data.copyChildren()

    def OnDelItem(self, evt):
        """
        Удаляем элемент дерева.
        """
        item = self.GetSelection()
        prnt_item = self.GetItemParent(item)
        level, prnt_obj = self.GetPyData(item)
        prnt_obj.Del()
        self._delItemList.append(item)
        self.Delete(item)
        
        if self.root != prnt_item:
            self.SelectItem(prnt_item)
                
    def OnExpand(self, evt):
        """
        """
        root = evt.GetItem()
        if self.treeDict:
            level, res = self.GetPyData(root)
            self.DeleteChildren(root)
            
            t1 = time.clock()
            if 1:
                try:
                    ic_proccess_dlg.ProccessFunc(self, u'Подождите', res.ReLoad, tuple(), {}, bAutoIncr=True)
                except:
                    if not type(res) in (type({}), type([]), type(0,)):
                        iclog.LogLastError(u'### Reload Error')
            
            self.addBranch(root, res, 0, level+1)
            t2 = time.clock()

        #   Отрабатываем функционал, определенный пользователем
        self.evalSpace['evt'] = evt
        ret, val = self.eval_attr('onExpand')
        if ret and val:
            evt.Skip()
        elif not ret:
            evt.Skip()
    
    def OnRightClick(self, evt):
        """
        Обрабатываем сообщение <EVT_RIGHT_DOWN>.
        """
        if not self._bEditMode:
            return

        menuObj = wx.Menu()
        menuGroup = wx.Menu()
        itm = self.GetSelection()
        #   Если словарь является метокомпонентом, то создаем меню со списком
        #   компонентов, которые можно добавлять в текущий объект
        if self.treeDict and not isinstance(self.treeDict, dict):

            level, obj = self.GetPyData(itm)
            lst = obj.getMyContainerMetaItems()
            
            for cob in lst:
                id = cob.GetUniqId()

                if not cob.resource['description']:
                    label = cob.resource['name']
                else:
                    label = cob.resource['description']
                
                item = wx.MenuItem(menuGroup, id, label)
                
                if cob.getPic():
                    item.SetBitmap(cob.getPic())
                    
                menuGroup.AppendItem(item)
                self.Bind(wx.EVT_MENU, self.OnAddItem, id=id)

        id = icwidget.icNewId()
        menuObj.AppendMenu(id, u'Добавить объект', menuGroup)

        if self.treeDict and not isinstance(self.treeDict, dict) and itm != self.root:
            level, obj = self.GetPyData(itm)
            id = icwidget.icNewId()
            item = wx.MenuItem(menuObj, id, u'Удалить объект')
            item.SetBitmap(common.imgDeleteRed)
            menuObj.AppendItem(item)
            self.Bind(wx.EVT_MENU, self.OnDelItem, id=id)

            id = icwidget.icNewId()
            item = wx.MenuItem(menuObj, id, u'Клонировать объект')
            item.SetBitmap(common.imgClone)
            menuObj.AppendItem(item)
            self.Bind(wx.EVT_MENU, self.OnCloneItem, id=id)

            id = icwidget.icNewId()
            item = wx.MenuItem(menuObj, id, u'Копировать содержимое объекта')
            item.SetBitmap(common.imgEdtMnuCopy)
            menuObj.AppendItem(item)
            self.Bind(wx.EVT_MENU, self.OnCopy, id=id)

            if self.bObjBuff and obj.canPastChildren():
                id = icwidget.icNewId()
                item = wx.MenuItem(menuObj, id, u'Вставить из буфера в объект')
                item.SetBitmap(common.imgEdtMnuPaste)
                menuObj.AppendItem(item)
                self.Bind(wx.EVT_MENU, self.OnPaste, id=id)

        self.PopupMenu(menuObj, evt.GetPoint())

    def OnPaste(self, evt):
        """
        """
        item = self.GetSelection()
        level, data = self.GetPyData(item)
        #   Обновляем дерево
        if data.pastChildren():
            self.ReLoadParentItemData(item)

    def OnSelected(self, evt):
        """
        Обработчик события wx.EVT_TREE_SEL_CHANGED, атрибут=<selected>.
        Событие посылается после перемещения курсора на другой пункт дерева.
        """
        self.evalSpace['evt'] = evt
        ret, val = self.eval_attr('selected')
        if ret and val:
            evt.Skip()
        elif not ret:
            evt.Skip()
     
    def ReLoadItemData(self, item):
        """
        Переоткрываем ветку дерева.
        """
        if self.treeDict:
            self.Collapse(item)
            self.Expand(item)
            self.SelectItem(item)
        
    def ReLoadParentItemData(self, item):
        """
        Переоткрываем родительскую ветку дерева.
        """
        if self.treeDict:
            prnt_item = self.GetItemParent(item)
            self.Collapse(prnt_item)
            self.Expand(prnt_item)
            self.SelectItem(prnt_item)
            
    def ReLoadRoot(self):
        """
        Перегружаем методерево.
        """
        if self.root:
            self.Collapse(self.root)
            self._testTree(1)
            self.SelectItem(self.root)

    def getChildLst(self, prnt_item):
        """
        Возврвщает список дочерних элементов.
        """
        child, ck = self.GetFirstChild(prnt_item)
        lst = []
        
        if child.IsOk():
            lev, data = self.GetPyData(child)
            lst.append((child, data))
            while 1:
                child, ck = self.GetNextChild(prnt_item, ck)
                
                if child.IsOk():
                    lev, data = self.GetPyData(child)
                    lst.append((child, data))
                else:
                    break

        return lst
        
    def SelectItemByName(self, prnt_item, name):
        """
        Устанавливает в качестве ткущего узла элемент с определенным именем.
        """
        for el in self.getChildLst(prnt_item):
            item, metaObj = el
            if metaObj.value.name == name:
                self.SelectItem(item)
                break
        
    def SetEditMode(self, bEdit=True):
        """
        Устанавливает признак разрешающий или запрещающий редактировать дерево.
        
        @type bEdit: C{bool}
        @param bEdit: Признак разрешающий или запрещающий редактировать дерево.
        """
        self._bEditMode = bEdit
    
    def SetReestr(self, reestr):
        """
        Устанавливаем указатель на реестр.
        """
        self.__reestr = reestr
        
    def _testTree(self, n=5):
        """
        """
        for x in range(n):
            txt = 'Item %d' % x
            child = self.AppendItem(self.root, txt)
            self.SetItemText(child, txt + '(c1)')
            self.SetItemImage(child, self.fldridx, which = wx.TreeItemIcon_Normal)
            self.SetItemImage(child, self.fldropenidx, which = wx.TreeItemIcon_Expanded)
        
    #   Обработчики событий


def test(par=0):
    """
    Тестируем пользовательский класс.
    """

if __name__ == '__main__':
    test()
