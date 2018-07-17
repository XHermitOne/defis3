#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Представления каталога в виде списка и дерева.
"""
import ic
from ic.contrib.ObjectListView import ObjectListView, GroupListView, ColumnDefn
from ic.db import iccatalog
from ic.db.iccatalog import icItemCatalog
import wx

_ = wx.GetTranslation


class BackItem(icItemCatalog):
    catalog_type = 'back'
    
    def __init__(self, path=''):
        icItemCatalog.__init__(self, path, '', '', '', '')
        
    def get_name(self):
        return ''


def sort_with_folders(x, y):
    if x.catalog.has_child_items(x) and not y.catalog.has_child_items(y):
        return -1
    if not x.catalog.has_child_items(x) and y.catalog.has_child_items(y):
        return 1
    else:
        return 0


def cmpObj(func, obj1, obj2, *arg):
    if obj1.catalog_type == 'back':
        return 0
    elif obj2.catalog_type == 'back':
        return 1
    elif obj1.catalog_type == 'Folder' and obj2.catalog_type != 'Folder':
        return 0
    elif obj2.catalog_type == 'Folder' and obj1.catalog_type != 'Folder':
        return 1
    else:
        return func(obj1, obj2, *arg)


class BaseCatalogView(object):
    def __init__(self, cat):
        self.catalog = cat
        bck = BackItem(cat.get_parent_path())
        self.items = cat.get_child_items()
        self.items.sort(cmp=sort_with_folders)
        self.items = [bck] + self.items
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, id=-1)
        
    def OnItemActivated(self, evt):
        indx = evt.m_itemIndex
        item = self.GetObjectAt(indx)
        prnt = cat.get_parent_path(item.path)
        if isinstance(item, BackItem):
            bck = BackItem(prnt)
            self.items = cat.get_child_items(path=prnt)
            self.items.sort(cmp=sort_with_folders)
        else:
            bck = BackItem(item.path)
            self.items = cat.get_child_items(item)
        
        self.items.sort(cmp=sort_with_folders)
        self.items = [bck] + self.items
        self.SetObjects(self.items)
        self.RepopulateList()
        self.SortBy(0)
        evt.Skip()
        
    def InitObjectListView(self):
        """
        Создаем описание колонок.
        """
        from ic.imglib import newstyle_img
        objImage = self.AddImages(iccatalog.icItemCatalog.get_pic())
        fldImage = self.AddImages(iccatalog.icFolderItem.get_pic())
        backImage = self.AddImages(newstyle_img.getextEditor2Bitmap())
        
        def ObjectImageGetter(item):
            if isinstance(item, BackItem):
                return backImage
            elif hasattr(item, 'catalog_type') and item.catalog_type == 'Folder':
                return fldImage
            else:
                return objImage
        
        self.SetColumns([
            ColumnDefn(_('name'), "left", 120, "get_name", imageGetter=ObjectImageGetter),
            ColumnDefn(_('pointer'), "center", 100, "pointer"),
            ColumnDefn(_('title'), "left", 100, "title"),
            ColumnDefn(_('description'), "center", 100, "description"),
            ColumnDefn(_('registr.'), "center", 100, "reg_time"),
            ColumnDefn(_('act.'), "center", 100, "act_time"),
            ColumnDefn(_('catalog'), "left", 100, "catalog"),
        ])
        
    def isFolder(self, item):
        pass
    
    def SortListItemsBy(self, cmpFunc, ascending=None):
        """
        Sort the existing list items using the given comparison function.

        The comparison function must accept two model objects as parameters.

        The primary users of this method are handlers of the SORT event that want
        to sort the items by their own special function.
        """
        if ascending is None:
            ascending = self.sortAscending

        def _sorter(key1, key2):
            cmpVal = cmpObj(cmpFunc, self.innerList[key1], self.innerList[key2])
            if ascending:
                return cmpVal
            else:
                return -cmpVal
        self.SortItems(_sorter)


class SimpleCatalogView(ObjectListView, BaseCatalogView):
    """
    Каталог в виде списка.
    """

    def __init__(self, cat, *arg, **kwarg):
        """
        Конструктор.
        @type cat: C{ic.db.iccatalog.icCatalog}
        @param cat: Каталог.
        """
        ObjectListView.__init__(self, *arg, **kwarg)
        BaseCatalogView.__init__(self, cat)
        self.InitObjectListView()
        self.SetObjects(self.items)
    
    def SortListItemsBy(self, cmpFunc, ascending=None):
        BaseCatalogView.SortListItemsBy(self, cmpFunc, ascending)


class GroupCatalogView(GroupListView, BaseCatalogView):
    """
    Каталог в виде списка.
    """

    def __init__(self, cat, *arg, **kwarg):
        """ Конструктор.
        @type cat: C{ic.db.iccatalog.icCatalog}
        @param cat: Каталог.
        """
        GroupListView.__init__(self, *arg, **kwarg)
        BaseCatalogView.__init__(self, cat)
        self.InitObjectListView()
        self.SetObjects(self.items)
    
    def SortListItemsBy(self, cmpFunc, ascending=None):
        BaseCatalogView.SortListItemsBy(self, cmpFunc, ascending)


class CatalogFrame(wx.Frame):
    def __init__(self, cat, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        self.InitWidgets(cat)

    def InitWidgets(self, cat):
        panel = wx.Panel(self, -1)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(panel, 1, wx.ALL|wx.EXPAND)
        self.SetSizer(sizer_1)

        self.myOlv = SimpleCatalogView(cat, panel, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.myOlv, 1, wx.ALL|wx.EXPAND, 4)
        panel.SetSizer(sizer_2)
        self.Layout()


def get_test_catalog():
    """ """
    from ic.db import iccatalog, icdbcatalog
    from ic.db.resources import iccatalogtable
    prj_dir = '../test/testprj/testprj/'
    cat = None
    try:
        ic.Login('user', None, prj_dir)
        src = (('SQLiteDB', 'testsrc', None, 'testsrc.src', 'testprj'),)
        cat = icdbcatalog.icDBCatalog(src)
    finally:
        ic.Logout()
    
    return cat


if __name__ == '__main__':
    cat = get_test_catalog()
    app = wx.PySimpleApp()
    wx.InitAllImageHandlers()
    frame_1 = CatalogFrame(cat, None, -1, 'Simple catalog view')
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
