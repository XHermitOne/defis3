#!/usr/bin/env python
# -*- coding: utf-8 -*-


import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
#import plan.interfaces.IYearEdtPanel as IYearEdtPanel
import ic.dlg.msgbox as msgbox
import ic.interfaces.icobjectinterface as icobjectinterface
import ic.log.ic_log as ic_log
import copy
import ic.dlg.ic_proccess_dlg as ic_proccess_dlg

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource = {'activate': 1, 'show': 1, 'recount': u'', 'keyDown': None, 'border': 0, 'size': (500, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': u'None', 'proportion': 0, 'source': u'', 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'res_module': None, 'description': None, 'onClose': u'WrapperObj.OnCloseFuncplanPanel(evt)', '_uuid': u'dab55da9d238b220842324727db763f5', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'style': 0, 'activate': 1, 'prim': u'', 'name': u'Data', 'component_module': u'None', '_uuid': u'0653757b1663a86ec043d3f612f11bda', 'alias': u'None', 'init_expr': None, 'child': [{'activate': u'1', 'name': u'Plans', '_uuid': u'5576dda6e2faa25ec776cc1e7fac30d4', 'docstr': u'ic.db.icdataset-module.html', 'filter': u'', 'alias': u'', 'res_query': u'metadata_plan', 'init_expr': None, 'file': u'metadata_plan.mtd', 'type': u'DataLink', 'link_expr': u''}], 'type': u'Group'}, {'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'name': u'DefaultName_1146', 'position': wx.Point(55, 58), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'df1c29dbe191e71ef9053907a30d81c4', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'activate': u'0', 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (-1, -1), 'style': 2097668, 'foregroundColor': None, 'span': (1, 1), 'component_module': u'', 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'ToolBar', '_uuid': u'5170cce88e4cdf0a02e6b154d373f7a4', 'moveAfterInTabOrder': u'', 'flag': 8192, 'child': [{'activate': u'1', 'name': u'addElPlanTool', 'toolType': 0, 'shortHelpString': u'\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u044d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u043b\u0430\u043d\u0430', 'longHelpString': u'', '_uuid': u'ccf7fe929517d7dce3bd237c17bb8eed', 'pushedBitmap': u'', 'label': u'', 'isToggle': 0, 'init_expr': u'', 'position': wx.Point(23, 11), 'bitmap': u'@import ic.imglib.common as common\r\n_resultEval=common.imgAddRes', 'type': u'ToolBarTool', 'onTool': None}, {'activate': u'1', 'name': u'delElPlanTool', 'toolType': 0, 'shortHelpString': u'\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u044d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u043b\u0430\u043d\u0430', 'longHelpString': u'', '_uuid': u'651f351d30b90ca55755bc9c5e374a89', 'pushedBitmap': u'', 'label': u'', 'isToggle': 0, 'init_expr': None, 'position': wx.Point(23, 11), 'bitmap': u'@import ic.imglib.common as common\r\n_resultEval=common.imgDeleteRed', 'type': u'ToolBarTool', 'onTool': None}], 'name': u'DefaultName_1446_1640', 'keyDown': None, 'alias': u'', 'init_expr': None, 'position': wx.Point(0, 0), 'onInit': None, 'bitmap_size': (16, 15)}, {'activate': 1, 'show': 1, 'keyDown': None, 'border': 0, 'size': (-1, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'layout': u'vertical', 'alias': None, 'component_module': None, 'win1': {'activate': 1, 'show': 1, 'recount': None, 'keyDown': None, 'border': 0, 'size': wx.Size(196, 449), 'onRightMouseClick': None, 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': 'Panel', 'description': None, 'onClose': None, '_uuid': '148abddf6dfb0f17ec755974926a2c29', 'style': 524288, 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': 'vertical', 'description': None, 'position': wx.Point(18, 65), 'component_module': None, 'type': 'BoxSizer', '_uuid': '95302a1dea386e2068b8425502d9158b', 'proportion': 0, 'name': 'DefaultName_1877', 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'recount': None, 'keyDown': None, 'border': 0, 'size': (-1, 35), 'onRightMouseClick': None, 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': 'Panel', 'res_module': None, 'description': None, 'onClose': None, '_uuid': '438580093c73a92b0d0957cdc780f270', 'style': 524288, 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 8192, 'child': [{'activate': 1, 'show': 1, 'refresh': [], 'border': 0, 'size': wx.Size(142, 21), 'style': 33555520, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': (255, 255, 255), 'type': 'Choice', 'res_module': None, 'loseFocus': None, 'description': None, '_uuid': 'f9dc9d1512efcb29aa467d6ef3b5003f', 'moveAfterInTabOrder': '', 'choice': 'WrapperObj.choiceFuncVariantChoice(evt)', 'flag': 0, 'recount': [], 'field_name': None, 'setFocus': None, 'name': 'variantChoice', 'items': "['1','2','3','5']", 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (10, 11), 'onInit': 'WrapperObj.OnInitFuncVariantChoice(evt)'}, {'activate': 1, 'show': 1, 'mouseClick': 'WrapperObj.mouseClickFuncManageBtn(evt)', 'font': {}, 'border': 0, 'size': wx.Size(76, 23), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': '\xd3\xef\xf0\xe0\xe2\xeb\xe5\xed\xe8\xe5', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': 'Button', 'res_module': None, 'description': None, '_uuid': '4a7982643504c0eaccc2c2d90b436842', 'moveAfterInTabOrder': '', 'flag': 0, 'recount': None, 'name': 'manageBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (156, 10), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'show': 1, 'child': [], 'keyDown': None, 'border': 0, 'size': (0, 0), 'onRightMouseClick': None, 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': (128, 128, 192), 'type': 'Panel', 'description': None, 'onClose': None, '_uuid': '467b35ff30b0bee27a10e43d7a162579', 'style': 524288, 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 0, 'recount': None, 'name': 'defaultWindow_1123', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (237, 38), 'onInit': None}], 'name': 'managePlanPanel', 'refresh': None, 'alias': None, 'init_expr': 'import ic.utils.graphicUtils as graph\r\nclr = graph.GetMidColor(self.GetParent().GetBackgroundColour(), wx.Colour(255,255,255), 0.5)\r\n#self.SetRoundBoundMode((150,150,140), 2)\r\nself.SetBackgroundColour(clr)', 'position': wx.Point(0, 0), 'onInit': None}, {'activate': 1, 'show': 1, 'labels': ['\xd1\xf2\xf0\xf3\xea\xf2\xea\xf0\xe0 \xef\xeb\xe0\xed\xee\xe2'], 'activated': 'WrapperObj.activatedFuncplansTreeCtrl(evt)', 'refresh': None, 'onExpand': '', 'border': 3, 'size': (-1, -1), 'treeDict': {}, 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), 'onRightClick': '', 'postDelItem': None, 'component_module': None, 'selected': 'WrapperObj.selectedFuncplansTreeCtrl(evt)', 'proportion': 1, 'source': None, 'backgroundColor': None, 'titleRoot': 'root', 'type': 'TreeListCtrl', 'res_module': None, 'description': None, 'postAddItem': None, '_uuid': 'd42242d8fcd395bf2bc1cad32309cd76', 'style': 8201, 'preAddItem': 'True', 'flag': 8432, 'recount': None, 'preDelItem': 'True', 'name': 'plansTreeCtrl', 'wcols': [150, 100], 'fields': [], 'keyDown': 'None', 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': "odb = _dict_obj['Plans']\r\nprint '>>>>---- odb=', odb\r\nodb.unLockAll()\r\nself.LoadTree(odb)"}, {'style': 0, 'activate': 1, 'span': (1, 1), 'description': None, 'component_module': None, 'type': 'SizerSpace', '_uuid': 'cf31b97feeb54c441eade901b4a61f0c', 'proportion': 0, 'name': 'DefaultName_1318', 'alias': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'border': 0, 'size': (0, 0)}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'name': 'leftPanel', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(0, 0), 'onInit': None}, 'proportion': 1, 'source': None, 'backgroundColor': None, 'type': u'SplitterWindow', 'description': None, '_uuid': u'e30225079ae7fab132f465493668b1b6', 'style': 768, 'docstr': u'ic.components.icsplitter-module.html', 'flag': 8192, 'recount': None, 'span': (1, 1), 'name': u'splitterPanel', 'min_panelsize': 20, 'refresh': None, 'win2': {'activate': 1, 'show': 1, 'recount': None, 'keyDown': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': 'Panel', 'description': None, 'onClose': None, '_uuid': '8ad4de6318bd3e3fa2f7605cbafc9596', 'style': 524288, 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'hgap': 0, 'style': 0, 'activate': '0', 'layout': 'vertical', 'name': 'DefaultName_1896', 'position': wx.Point(29, 64), 'component_module': None, 'type': 'BoxSizer', '_uuid': 'd01b38e3cc4a75d58a18f71ee475a53a', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'line_color': (200, 200, 200), 'activate': 1, 'show': 1, 'cols': [{'activate': 1, 'ctrl': None, 'pic': 'S', 'hlp': None, 'style': 0, 'label': '\xfd\xeb\xe5\xec\xe5\xed\xf2 \xef\xeb\xe0\xed\xe8\xf0\xee\xe2\xe0\xed\xe8\xff', 'width': 140, 'init': None, 'valid': None, 'type': 'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'shortHelpString': '', '_uuid': '4515d88b0254b668f7a45b8b5fcf6312', 'recount': None, 'getvalue': '', 'name': 'default_2086', 'setvalue': '', 'attr': 'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': 'S', 'hlp': None, 'style': 0, 'label': '\xea\xee\xfd\xf4\xe8\xf6\xe8\xe5\xed\xf2', 'width': 113, 'init': None, 'valid': None, 'type': 'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'shortHelpString': '', '_uuid': '182f0733526295aa0befd962bdc8a4f9', 'recount': None, 'getvalue': '', 'name': 'default_2182', 'setvalue': '', 'attr': 'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': 'S', 'getvalue': '', 'style': 0, 'label': '\xf1\xf3\xec\xec\xe0', 'width': 50, 'init': None, 'valid': None, 'type': 'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'shortHelpString': '', '_uuid': '438b60b6ddf4acbc0168fb1f1e69c2c0', 'recount': None, 'hlp': None, 'name': 'default_2326', 'setvalue': '', 'attr': 'W', 'keyDown': None, 'alias': None, 'init_expr': None}], 'keyDown': None, 'border': 0, 'post_select': None, 'size': (-1, -1), 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), 'delRec': None, 'row_height': 20, 'selected': None, 'proportion': 1, 'getattr': None, 'label': 'Grid', 'source': None, 'init': None, 'backgroundColor': None, 'fixRowSize': 0, 'type': 'GridDataset', 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'fixColSize': 0, 'post_del': None, 'post_init': None, '_uuid': 'edeba9960297fc2b91355c17c63ac6b3', 'style': 0, 'docstr': 'ic.components.icgrid.html', 'flag': 8192, 'recount': None, 'label_attr': {'foregroundColor': (0, 0, 0), 'name': '', '_uuid': None, 'backgroundColor': None, 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'label_attr', 'alignment': ('left', 'middle')}, 'name': 'planGrid', 'label_height': 20, 'changed': None, 'onSize': None, 'alias': None, 'init_expr': '', 'position': wx.Point(18, 18), 'onInit': '', 'refresh': None}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'name': 'rightPanel', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(104, 0), 'onInit': None}, 'init_expr': None, 'position': wx.Point(0, 0), 'sash_pos': 250, 'onInit': None}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'name': u'planPanel', 'refresh': u'', 'alias': None, 'init_expr': u'None', 'position': (-1, -1), 'onInit': u''}

#   Версия объекта
__version__ = (1, 2, 1, 2)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'MetaTreeBrows'


class MetaTreeBrows(icobjectinterface.icObjectInterface):
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
        self.metatype = metatype
        self.res = copy.deepcopy(resource)
        
        #   Прописываем имя метатипа в ресурсе
        # Находим ссылку на описания метатипа
        res = self.GetObjectResource(nameObj='Plans', typeObj='DataLink',  resource=self.res)
        
        #   Если метокласс определен, то отключаем его построение по ресурсу
        if metaObj:
            res['activate'] = False
            par['Plans'] = metaObj
            
        elif res and metatype:
            res['res_query'] = metatype
            res['file'] = '%s.mtd' % metatype
        
        if treeRootTitle or treeLabels:
            res = self.GetObjectResource(nameObj='plansTreeCtrl', typeObj='TreeListCtrl',  resource=self.res)
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
        return self.GetNameObj('plansTreeCtrl').GetEditMode()
        
    def _getTypeBuffKey(self, metatype):
        """
        Генерирует уникальный ключ для панели браузера.
        """
        return self.GetNameObj('plansTreeCtrl').GetObjectUUID()+ metatype
        
    ###BEGIN EVENT BLOCK
    def activatedFuncplansTreeCtrl(self, evt):
        """
        Функция обрабатывает событие <activated>.
        """
        return None
    
    def selectedFuncplansTreeCtrl(self, evt):
        """
        Функция обрабатывает событие <selected>.
        """
        tree = self.GetNameObj('plansTreeCtrl')
        split = self.GetNameObj('splitterPanel')
        leftPanel = self.GetNameObj('leftPanel')
        pos = split.GetSashPosition()
        item = evt.GetItem()
        level, data = tree.GetPyData(item)

        #   Предварительно сохраняем
        if self.ILeftPanel and self.ILeftPanel.metaObj.isMyLock():
            if self.ILeftPanel.itemTree != tree.root:
                self.ILeftPanel.SaveData()
            self.ILeftPanel.metaObj.unLock()

        if 1:
            if data.isLock() and not data.isMyLock():
                msgbox.MsgBox(split, u'Элемент плана заблокирован пользлвателем <%s>' % data.ownerLock())
            else:
                data.lock()
                
            # --- Сохраняем старую панель в буфере
            if self.ILeftPanel and self.ILeftPanel.itemTree not in tree.GetDelItemLst():
                oldItem = self.ILeftPanel.itemTree
                metaKey = self._getTypeBuffKey(self.ILeftPanel.metatype)
                
                if metaKey not in MetaTreeBrows.edtPanelBuff:
                    MetaTreeBrows.edtPanelBuff[metaKey] = self.ILeftPanel
                
                if oldItem == tree.root:
                    self.ILeftPanel.Show(False)
                else:
                    self.ILeftPanel.getObject().Show(False)
                    
            # --- Если панель сохранена достаем ее из буфера
            metaKey = self._getTypeBuffKey(data.value.metatype)
            _fromBuff = False
            
            if metaKey in MetaTreeBrows.edtPanelBuff:
                self.ILeftPanel = MetaTreeBrows.edtPanelBuff[metaKey]
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
            elif item != tree.root:
                if not self.rootPanel:
                    if self.GetEditMode():
                        obj = data.Edit(split, data)
                    else:
                        obj = data.Edit(split, data)
                        
                    if obj:
                        self.ILeftPanel = obj.evalSpace['WrapperObj']
                else:
                    if self.GetEditMode():
                        obj = data.Edit(self.rootPanel, data)
                    else:
                        obj = data.Edit(self.rootPanel, data)

                    if obj:
                        obj.Reparent(split)
                        self.ILeftPanel = obj.evalSpace['WrapperObj']

            # Для корневого элемента создаем панельку
            else:
                self.rootPanel = obj = wx.Panel(split, -1)
                self.ILeftPanel = obj
                self.ILeftPanel.metaObj = data
                obj.SetBackgroundColour(wx.Colour(200,200,200))
  
            if self.ILeftPanel:
            
                self.ILeftPanel.tree = tree
                self.ILeftPanel.itemTree = item
                self.ILeftPanel.metatype = data.value.metatype

                # Загружаем данные
                try:
                    if item != tree.root:
                        self.ILeftPanel.LoadData()
                except:
                    ic_log.icLogErr()
                
                split.Unsplit()
                split.SplitVertically(leftPanel, obj, pos)
                split.Refresh()
            elif data:
                data.unLock()
        
        return None
    
    def OnCloseFuncplanPanel(self, evt):
        """
        Функция обрабатывает событие <?>.
        """
        tree = self.GetNameObj('plansTreeCtrl')

        if tree.treeDict:
            tree.treeDict.unLockAll()
        
        # --- Чистим буфер
        uuid = self.GetNameObj('plansTreeCtrl').GetObjectUUID()
        lst = [s for s in MetaTreeBrows.edtPanelBuff.keys() if s.startswith(uuid)]
        
        for key in lst:
            #   Перед уничтожением вызываем фукцию уведомляющую все дочерние компоненты
            try:
                cls = MetaTreeBrows.edtPanelBuff[key]
                cls.getObject().DestroyWin()
            except:
                pass
            MetaTreeBrows.edtPanelBuff.pop(key)
            
        return None
    
    def mouseClickFuncManageBtn(self, evt):
        """
        Функция обрабатывает событие <mouseClick>.
        """
        return None
    
    def choiceFuncVariantChoice(self, evt):
        """
        Функция обрабатывает событие <?>.
        """
        return None
    
    def OnInitFuncVariantChoice(self, evt):
        """
        Функция обрабатывает событие <?>.
        """
        return None

    ###END EVENT BLOCK
    def SetEditMode(self, bEdit=True):
        """
        Устанавливает признак разрешающий или запрещающий редактировать дерево.
        
        @type bEdit: C{bool}
        @param bEdit: Признак разрешающий или запрещающий редактировать дерево.
        """
        self.GetNameObj('plansTreeCtrl').SetEditMode(bEdit)


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
