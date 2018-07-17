#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Браузер реестра документов.
"""

import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
#import plan.interfaces.IYearEdtPanel as IYearEdtPanel
import ic.dlg.msgbox as msgbox
import ic.interfaces.icobjectinterface as icobjectinterface
import ic.log.ic_log as ic_log
import copy
import ic.dlg.ic_proccess_dlg as ic_proccess_dlg
from ic.engine import ic_user

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'show': 1, 'recount': u'', 'keyDown': None, 'border': 0, 'size': (500, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': u'None', 'proportion': 0, 'source': u'', 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': u'WrapperObj.OnCloseFuncPanel(evt)', '_uuid': u'20c3de80524a1a295fbaf7741e7553c5', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'style': 0, 'activate': 1, 'prim': u'', 'name': u'Data', 'component_module': u'None', '_uuid': u'5cdbaaea0b3a15c4ca7166641b634964', 'alias': u'None', 'init_expr': None, 'child': [{'activate': u'1', 'name': u'ReestrData', '_uuid': u'52f4a4604213da7bed131c0b5b339d0a', 'docstr': u'ic.db.icdataset-module.html', 'filter': u'', 'alias': u'', 'res_query': u'reestr_doc', 'init_expr': None, 'file': u'reestr_doc.mtd', 'type': u'DataLink', 'link_expr': u''}], 'type': u'Group', 'description': None}, {'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'name': u'DefaultName_1146', 'position': wx.Point(55, 58), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'df1c29dbe191e71ef9053907a30d81c4', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'activate': u'0', 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (-1, -1), 'style': 2097668, 'foregroundColor': None, 'span': (1, 1), 'component_module': u'', 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'ToolBar', '_uuid': u'5170cce88e4cdf0a02e6b154d373f7a4', 'moveAfterInTabOrder': u'', 'flag': 8192, 'child': [{'activate': u'1', 'name': u'addElPlanTool', 'toolType': 0, 'shortHelpString': u'\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u044d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u043b\u0430\u043d\u0430', 'longHelpString': u'', '_uuid': u'ccf7fe929517d7dce3bd237c17bb8eed', 'pushedBitmap': u'', 'label': u'', 'isToggle': 0, 'init_expr': u'', 'position': wx.Point(23, 11), 'bitmap': u'@import ic.imglib.common as common\r\n_resultEval=common.imgAddRes', 'type': u'ToolBarTool', 'onTool': None}, {'activate': u'1', 'name': u'delElPlanTool', 'toolType': 0, 'shortHelpString': u'\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u044d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u043b\u0430\u043d\u0430', 'longHelpString': u'', '_uuid': u'651f351d30b90ca55755bc9c5e374a89', 'pushedBitmap': u'', 'label': u'', 'isToggle': 0, 'init_expr': None, 'position': wx.Point(23, 11), 'bitmap': u'@import ic.imglib.common as common\r\n_resultEval=common.imgDeleteRed', 'type': u'ToolBarTool', 'onTool': None}], 'name': u'DefaultName_1446_1640', 'keyDown': None, 'alias': u'', 'init_expr': None, 'position': wx.Point(0, 0), 'onInit': None, 'bitmap_size': (16, 15)}, {'activate': 1, 'show': 1, 'keyDown': None, 'border': 0, 'size': (-1, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'layout': u'vertical', 'component_module': None, 'win1': {'activate': 1, 'show': 1, 'recount': None, 'keyDown': None, 'border': 0, 'size': wx.Size(196, 449), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'148abddf6dfb0f17ec755974926a2c29', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'description': None, 'position': wx.Point(18, 65), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'95302a1dea386e2068b8425502d9158b', 'proportion': 0, 'name': u'DefaultName_1877', 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'recount': None, 'keyDown': None, 'border': 0, 'size': (-1, 35), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'bb00baab994f727a481e434c9208773e', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'child': [{'activate': 1, 'show': 1, 'refresh': [], 'border': 0, 'size': wx.Size(142, 21), 'style': 33555520, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': (255, 255, 255), 'type': u'Choice', 'loseFocus': None, 'description': None, '_uuid': u'f9dc9d1512efcb29aa467d6ef3b5003f', 'moveAfterInTabOrder': u'', 'choice': u'WrapperObj.choiceFuncVariantChoice(evt)', 'flag': 0, 'recount': [], 'field_name': None, 'setFocus': None, 'name': u'variantChoice', 'items': u"['1','2','3','5']", 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (10, 11), 'onInit': u'WrapperObj.OnInitFuncVariantChoice(evt)'}, {'activate': 1, 'show': 1, 'mouseClick': u'WrapperObj.mouseClickFuncManageBtn(evt)', 'font': {}, 'border': 0, 'size': wx.Size(76, 23), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u0423\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'description': None, '_uuid': u'59e84b09bee6a1dcb2128ab4fbc70c09', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'manageBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (156, 10), 'onInit': None, 'refresh': None, 'mouseContextDown': None}], 'name': u'managePlanPanel', 'refresh': None, 'alias': None, 'init_expr': u'import ic.utils.graphicUtils as graph\r\nclr = graph.GetMidColor(self.GetParent().GetBackgroundColour(), wx.Colour(255,255,255), 0.5)\r\nself.SetRoundBoundMode((150,150,140), 2)\r\nself.SetBackgroundColour(clr)', 'position': wx.Point(0, 0), 'onInit': None}, {'activate': 1, 'show': 1, 'labels': [u'\u0420\u0435\u0435\u0441\u0442\u0440'], 'activated': u'WrapperObj.activatedFuncTreeCtrl(evt)', 'refresh': None, 'onExpand': u'', 'border': 0, 'size': (-1, -1), 'treeDict': {}, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'onRightClick': u'', 'postDelItem': None, 'component_module': None, 'selected': u'WrapperObj.selectedFuncTreeCtrl(evt)', 'proportion': 1, 'source': None, 'backgroundColor': None, 'titleRoot': u'\u0420\u0435\u0435\u0441\u0442\u0440', 'type': u'TreeListCtrl', 'postAddItem': None, 'description': None, '_uuid': u'211a21b7881498b95c62c0756f4e64d9', 'style': 8201, 'preAddItem': u'True', 'flag': 8192, 'recount': None, 'preDelItem': u'True', 'name': u'reestrTreeCtrl', 'wcols': [300], 'fields': [u''], 'keyDown': u'None', 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': u"odb = self.GetContext().GetObject('ReestrData')\nprint '>>>>---- odb=', odb\nodb.unLockAll()\nself.LoadTree(odb)"}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'name': u'leftPanel', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(0, 0), 'onInit': None}, 'proportion': 1, 'source': None, 'backgroundColor': None, 'type': u'SplitterWindow', 'win2': {'activate': 1, 'show': 1, 'recount': None, 'keyDown': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': (192, 192, 192), 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'e99f7b946581617fe5c569b31ec42d61', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'hgap': 0, 'style': 0, 'activate': u'0', 'layout': u'vertical', 'description': None, 'position': wx.Point(29, 64), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'd01b38e3cc4a75d58a18f71ee475a53a', 'proportion': 0, 'name': u'DefaultName_1896', 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'line_color': (200, 200, 200), 'activate': 1, 'show': 1, 'cols': [{'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'label': u'\u044d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u043b\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f', 'width': 140, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'4515d88b0254b668f7a45b8b5fcf6312', 'recount': None, 'getvalue': u'', 'name': u'default_2086', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'label': u'\u043a\u043e\u044d\u0444\u0438\u0446\u0438\u0435\u043d\u0442', 'width': 113, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'182f0733526295aa0befd962bdc8a4f9', 'recount': None, 'getvalue': u'', 'name': u'default_2182', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': u'', 'style': 0, 'label': u'\u0441\u0443\u043c\u043c\u0430', 'width': 50, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'438b60b6ddf4acbc0168fb1f1e69c2c0', 'recount': None, 'hlp': None, 'name': u'default_2326', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}], 'keyDown': None, 'border': 0, 'post_select': None, 'size': (-1, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'delRec': None, 'alias': None, 'component_module': None, 'selected': None, 'proportion': 1, 'getattr': None, 'label': u'Grid', 'source': None, 'init': None, 'backgroundColor': None, 'fixRowSize': 0, 'type': u'GridDataset', 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'fixColSize': 0, 'description': None, 'post_del': None, 'post_init': None, '_uuid': u'bb27bcf0952a6224802de3026a97f55e', 'style': 0, 'docstr': u'ic.components.icgrid.html', 'flag': 8192, 'dclickEditor': None, 'recount': None, 'label_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': None, 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'label_attr', 'alignment': (u'left', u'middle')}, 'name': u'planGrid', 'label_height': 20, 'changed': None, 'onSize': None, 'row_height': 20, 'init_expr': u'', 'position': wx.Point(18, 18), 'onInit': u'', 'refresh': None}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'name': u'rightPanel', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(104, 0), 'onInit': None}, 'description': None, '_uuid': u'9ca3d902ff334b6edc284194ff41d90f', 'style': 768, 'docstr': u'ic.components.icsplitter-module.html', 'flag': 8192, 'recount': None, 'span': (1, 1), 'name': u'splitterPanel', 'min_panelsize': 20, 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-3, 25), 'sash_pos': 300, 'onInit': None}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'name': u'browsPanel', 'refresh': u'', 'alias': None, 'init_expr': u'None', 'position': (-1, -1), 'onInit': u''}

#   Версия объекта
__version__ = (1, 2, 1, 9)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'ReestrBrowser'

class ReestrBrowser(icobjectinterface.icObjectInterface):
    """
    Браузер реестра документов.
    """
    #   Буфер панелей
    edtPanelBuff = {}

    def __init__(self, parent, metatype=None, bPanelBuff=True, metaObj=None,
                    treeRootTitle=None, treeLabels=None, **par):
        """
        Конструктор.
        
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type metatype: C{string}
        @param metatype: Имя метатипа.
        @type bPanelBuff: C{string}
        @param bPanelBuff: Признак буферизации панелей.
        @type metaObj: C{MetaItem}
        @param metaObj: Метоописание дерева объектов. Если данный атрибут определен,
            то параметр <metatype> игнорируется.
        """
       
        #   Указатель на левую панель
        self.ILeftPanel = None
        
        #   Чистим буфер панелей
        #ReestrBrowser.edtPanelBuff = {}
        self.metatype = metatype
        self.res = copy.deepcopy(resource)
        
        #   Прописываем имя метатипа в ресурсе
        # Находим ссылку на описания метатипа
        res = self.GetObjectResource(nameObj='ReestrData', typeObj='DataLink',  resource=self.res)
        
        #   Если метокласс определен, то отключаем его построение по ресурсу
        if metaObj:
            res['activate']='False'
            par['ReestrData'] = metaObj
            
        elif res and metatype:
            print('>>>> Set metatype:', metatype)
            res['res_query'] = metatype
            res['file'] = '%s.mtd' % metatype
        
        if treeRootTitle or treeLabels:
            res = self.GetObjectResource(nameObj='reestrTreeCtrl', typeObj='TreeListCtrl',  resource=self.res)
            if treeRootTitle:
                res['titleRoot'] = treeRootTitle
            if treeLabels:
                res['labels'] = treeLabels
                
        #   Вызываем конструктор базового класса
        icobjectinterface.icObjectInterface.__init__(self, parent, self.res, **par)
        
        self.rootPanel = wx.Panel(self.GetNameObj('splitterPanel'), -1)
        self.rootPanel.Show(False)
        
    def GeneratePanTree(self, codYearPlan, func=None):
        """
        Функция генерирует дерево планов по статистике.
        """
        pass

    def GetEditMode(self):
        """
        Возвращает признак разрешающий или запрещающий редактировать дерево.
        """
        return self.GetNameObj('reestrTreeCtrl').GetEditMode()
        
    def _getTypeBuffKey(self, metatype):
        """
        Генерирует уникальный ключ для панели браузера.
        """
        return self.GetNameObj('reestrTreeCtrl').GetObjectUUID()+ metatype
        
    ###BEGIN EVENT BLOCK
    def activatedFuncTreeCtrl(self, evt):
        """
        Функция обрабатывает событие <activated>.
        """
        return None
    
    def selectedFuncTreeCtrl(self, evt):
        """
        Функция обрабатывает событие <selected>.
        """
        #print 'selectedFuncTreeCtrl START'
        tree = self.GetNameObj('reestrTreeCtrl')
        split = self.GetNameObj('splitterPanel')
        leftPanel = self.GetNameObj('leftPanel')
        obj=None
        pos = split.GetSashPosition()
        item = evt.GetItem()
        level, data = tree.GetPyData(item)
        #self.rootPanel = None
        
        #   Предварительно сохраняем
        if self.ILeftPanel and self.ILeftPanel.metaObj.isMyLock():
            if self.ILeftPanel.itemTree <> tree.root:
                print('SaveData START')
                self.ILeftPanel.SaveData()
            self.ILeftPanel.metaObj.unLock()
            print('!!! SaveData')
            
        if 1:#data._edit_form:

            if data.isLock() and not data.isMyLock():
                msgbox.MsgBox(split, u'Объект заблокирован пользователем <%s>' % data.ownerLock())
            else:
                print('????? >>>> lock() ??????')
                data.lock()
                
            #--- Сохраняем старую панель в буфере
            if self.ILeftPanel and not self.ILeftPanel.itemTree in tree.GetDelItemLst():
                oldItem = self.ILeftPanel.itemTree
                metaKey = self._getTypeBuffKey(self.ILeftPanel.metatype)
                
                if metaKey not in ReestrBrowser.edtPanelBuff:
                    ReestrBrowser.edtPanelBuff[metaKey] = self.ILeftPanel
                
                if oldItem == tree.root:
                    self.ILeftPanel.Show(False)
                else:
                    self.ILeftPanel.getObject().Show(False)
                    
            #--- Если панель сохранена достаем ее из буфера
            metaKey = self._getTypeBuffKey(data.value.metatype)
            _fromBuff = False
            
            if metaKey in ReestrBrowser.edtPanelBuff:
                self.ILeftPanel = ReestrBrowser.edtPanelBuff[metaKey]
                _fromBuff = True
                
                if item == tree.root:
                    obj = self.ILeftPanel
                    self.ILeftPanel.metaObj = data
                    obj.Show()
                else:
                    obj = self.ILeftPanel.getObject()
                    self.ILeftPanel.metaObj = data
                    obj.Show()
                
            # В противном случае создаем
            elif item <> tree.root:
                if not self.rootPanel:
                    if self.GetEditMode():
                        obj = data.Edit(split, data)
                    else:
                        obj = data.Edit(split, data)
                        
                    if obj:
                        self.ILeftPanel = obj.evalSpace['WrapperObj']
                        
                    print('>>>> Create Panel')
                else:
                    if self.GetEditMode():
                        obj = data.Edit(self.rootPanel, data)
                    else:
                        obj = data.Edit(self.rootPanel, data)

                    if obj:
                        obj.Reparent(split)
                        self.ILeftPanel = obj.evalSpace['WrapperObj']
                        print('>>>> Reparent Panel')
                    
            # Для корневого элемента создаем панельку
            else:
                self.rootPanel = obj = wx.Panel(split, -1)
                self.ILeftPanel = obj
                self.ILeftPanel.metaObj = data
  
            if self.ILeftPanel:
            
                self.ILeftPanel.tree = tree
                self.ILeftPanel.itemTree = item
                self.ILeftPanel.metatype = data.value.metatype

                # Загружаем данные
                try:
                    #self.ILeftPanel.LoadData()
#                    if _fromBuff:
#                        ic_proccess_dlg.ProccessFunc(split,'Обновляем состояние индикаторов', self.ILeftPanel.LoadData, tuple(), {}, bAutoIncr=True)
#                    else:
                    self.ILeftPanel.LoadData()
                        
                except:
                    print('#### LoadData() ERROR in ReestrBrowser', self.ILeftPanel)
                    print(self.ILeftPanel.__class__.__name__)
                    ic_log.icLogErr()
                
                split.Unsplit()
                if obj is None:
                    #Если правая панельне определена, тогда сделать пустую панель
                    obj=wx.Panel(split, -1)
                split.SplitVertically(leftPanel, obj, pos)
                split.Refresh()
                    #obj.Enable(False)
            elif data:
                data.unLock()
        
        return None
    
    def OnCloseFuncPanel(self, evt):
        """
        Функция обрабатывает событие <?>.
        """
        print('@@@@@@@@@@@@ OnClose')
        tree = self.GetNameObj('reestrTreeCtrl')

        if tree.treeDict:
            tree.treeDict.unLockAll()
        
        #--- Чистим буфер
        uuid = self.GetNameObj('reestrTreeCtrl').GetObjectUUID()
        lst = [s for s in ReestrBrowser.edtPanelBuff.keys() if s.startswith(uuid)]
        
        for key in lst:
            print(' pop key <%s> from Browser Panel Buffer' % key)
            #   Перед уничтожением вызываем фукцию уведомляющую все дочерние компоненты
            try:
                cls = ReestrBrowser.edtPanelBuff[key]
                cls.getObject().DestroyWin()
            except:
                pass
            ReestrBrowser.edtPanelBuff.pop(key)
            
        return None
    
    
    def mouseClickFuncManageBtn(self, evt):
        """
        Функция обрабатывает событие <mouseClick>.
        """
        print('...... manageBtn mouseClick')
        return None
    
    def choiceFuncVariantChoice(self, evt):
        """
        Функция обрабатывает событие <?>.
        """
        print('...... variantChoice onChoice')
        return None
    
    def OnInitFuncVariantChoice(self, evt):
        """
        Функция обрабатывает событие <?>.
        """
        print('...... variantChoice onInnit')
        return None
    ###END EVENT BLOCK
    def SetEditMode(self, bEdit=True):
        """
        Устанавливает признак разрешающий или запрещающий редактировать дерево.
        
        @type bEdit: C{bool}
        @param bEdit: Признак разрешающий или запрещающий редактировать дерево.
        """
        self.GetNameObj('reestrTreeCtrl').SetEditMode(bEdit)
        
def showReestrBrowser(MetaClass_):
    """
    Вывод формы браузера реестра.
    """
    #metaObj=prs.icCreateObject('reestr_doc','mtd') #IMetaplan.IMetaplan()
    metaclass=MetaClass_ #mydocsreestr.IMyDocsReestr()
    metaObj = metaclass.getObject()
#    cls=browser.ReestrBrowser(None, 'metadata_plan',
#                            metaObj=metaObj,
#                            treeRootTitle='Структура планов',
#                            treeLabels=['Планы'])
    print('>>>', metaObj.name)
    browser=ReestrBrowser(ic_user.icGetMainWin(), metaObj.name,
                            metaObj=metaObj,
                            treeRootTitle='',
                            treeLabels=[''])
                            
    #   Определяем функции пересчета модифицированных планов по базовому
    #brows.recountFunc = planUtils.genModifPlan
    #brows.recountModifPlanYear = planUtils.genModifPlanYear
    #brows.recountAllModifPlanMnth = planUtils.genAllPlanMonth
    
    # Устанавливает у метадерева указатель на браузер.
    #metaclass.SetUserData({'mode':'planning', 'browserInterface':brows})
    obj=browser.getObject()
    ic_user.icAddMainOrgPage(obj,u'Реестр документов')
    #obj.Show(True)
    
def test(par=0):
    """
    Тестируем класс new_form.
    """
    
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)

    ################
    # Тестовый код #
    ################
        
    frame.Show(True)
    app.MainLoop()
    
if __name__ == '__main__':
    test()