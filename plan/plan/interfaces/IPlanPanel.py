#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
import plan.interfaces.IYearEdtPanel as IYearEdtPanel
import ic.dlg.msgbox as msgbox
import ic.interfaces.icobjectinterface as icobjectinterface
### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'show': 1, 'recount': u'', 'keyDown': None, 'border': 0, 'size': (500, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': u'None', 'proportion': 0, 'source': u'', 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'onClose': u'WrapperObj.OnCloseFuncplanPanel(evt)', '_uuid': u'333e920c89ec596b0fae5ba9438adb0c', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'style': 0, 'activate': 1, 'prim': u'', 'name': u'Data', 'component_module': u'None', '_uuid': u'0653757b1663a86ec043d3f612f11bda', 'alias': u'None', 'init_expr': None, 'child': [{'activate': u'1', 'name': u'Plans', '_uuid': u'5576dda6e2faa25ec776cc1e7fac30d4', 'docstr': u'ic.db.icdataset-module.html', 'filter': u'', 'alias': u'', 'res_query': u'metadata_plan', 'init_expr': None, 'file': u'metadata_plan.mtd', 'type': u'DataLink', 'link_expr': u''}], 'type': u'Group'}, {'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'name': u'DefaultName_1146', 'position': wx.Point(55, 58), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'df1c29dbe191e71ef9053907a30d81c4', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'activate': u'0', 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (-1, -1), 'style': 2097668, 'foregroundColor': None, 'span': (1, 1), 'component_module': u'', 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'ToolBar', '_uuid': u'5170cce88e4cdf0a02e6b154d373f7a4', 'moveAfterInTabOrder': u'', 'flag': 8192, 'child': [{'activate': u'1', 'name': u'addElPlanTool', 'toolType': 0, 'shortHelpString': u'\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u044d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u043b\u0430\u043d\u0430', 'longHelpString': u'', '_uuid': u'ccf7fe929517d7dce3bd237c17bb8eed', 'pushedBitmap': u'', 'label': u'', 'isToggle': 0, 'init_expr': u'', 'position': wx.Point(23, 11), 'bitmap': u'@import ic.imglib.common as common\r\n_resultEval=common.imgAddRes', 'type': u'ToolBarTool', 'onTool': None}, {'activate': u'1', 'name': u'delElPlanTool', 'toolType': 0, 'shortHelpString': u'\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u044d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u043b\u0430\u043d\u0430', 'longHelpString': u'', '_uuid': u'651f351d30b90ca55755bc9c5e374a89', 'pushedBitmap': u'', 'label': u'', 'isToggle': 0, 'init_expr': None, 'position': wx.Point(23, 11), 'bitmap': u'@import ic.imglib.common as common\r\n_resultEval=common.imgDeleteRed', 'type': u'ToolBarTool', 'onTool': None}], 'name': u'DefaultName_1446_1640', 'keyDown': None, 'alias': u'', 'init_expr': None, 'position': wx.Point(0, 0), 'onInit': None, 'bitmap_size': (16, 15)}, {'activate': 1, 'show': 1, 'keyDown': None, 'border': 0, 'size': (-1, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'layout': u'vertical', 'component_module': None, 'win1': {'activate': 1, 'show': 1, 'recount': None, 'keyDown': None, 'border': 0, 'size': wx.Size(196, 449), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': (255, 255, 255), 'type': u'Panel', 'onClose': None, '_uuid': u'148abddf6dfb0f17ec755974926a2c29', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'name': u'DefaultName_1877', 'position': wx.Point(18, 65), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'95302a1dea386e2068b8425502d9158b', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'labels': [u'\u0421\u0442\u0440\u0443\u043a\u0442\u043a\u0440\u0430 \u043f\u043b\u0430\u043d\u043e\u0432'], 'activated': u'WrapperObj.activatedFuncplansTreeCtrl(evt)', 'refresh': None, 'border': 0, 'size': (-1, -1), 'treeDict': {}, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'onRightClick': u'', 'postDelItem': None, 'component_module': None, 'selected': u'WrapperObj.selectedFuncplansTreeCtrl(evt)', 'proportion': 1, 'source': None, 'backgroundColor': None, 'titleRoot': u'root', 'type': u'TreeListCtrl', 'postAddItem': None, '_uuid': u'04695ab1b838f7f331293657edeba8eb', 'style': 8201, 'preAddItem': u'True', 'flag': 8192, 'recount': None, 'preDelItem': u'True', 'name': u'plansTreeCtrl', 'wcols': [], 'fields': [], 'keyDown': u'None', 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': u"odb = _dict_obj['Plans']\r\n# print '>>>>---- odb=', odb\r\nodb.unLockAll()\r\nself.LoadTree(odb)"}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'name': u'leftPanel', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(0, 0), 'onInit': None}, 'proportion': 1, 'source': None, 'backgroundColor': None, 'type': u'SplitterWindow', 'win2': {'activate': 1, 'show': 1, 'recount': None, 'keyDown': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'onClose': None, '_uuid': u'8ad4de6318bd3e3fa2f7605cbafc9596', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'hgap': 0, 'style': 0, 'activate': u'0', 'layout': u'vertical', 'name': u'DefaultName_1896', 'position': wx.Point(29, 64), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'd01b38e3cc4a75d58a18f71ee475a53a', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'line_color': (200, 200, 200), 'activate': 1, 'show': 1, 'cols': [{'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'label': u'\u044d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u043b\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f', 'width': 140, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'4515d88b0254b668f7a45b8b5fcf6312', 'recount': None, 'getvalue': u'', 'name': u'default_2086', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'label': u'\u043a\u043e\u044d\u0444\u0438\u0446\u0438\u0435\u043d\u0442', 'width': 113, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'182f0733526295aa0befd962bdc8a4f9', 'recount': None, 'getvalue': u'', 'name': u'default_2182', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': u'', 'style': 0, 'label': u'\u0441\u0443\u043c\u043c\u0430', 'width': 50, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'438b60b6ddf4acbc0168fb1f1e69c2c0', 'recount': None, 'hlp': None, 'name': u'default_2326', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}], 'keyDown': None, 'border': 0, 'post_select': None, 'size': (-1, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'delRec': None, 'row_height': 20, 'selected': None, 'proportion': 1, 'getattr': None, 'label': u'Grid', 'source': None, 'init': None, 'backgroundColor': None, 'fixRowSize': 0, 'type': u'GridDataset', 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'fixColSize': 0, 'post_del': None, 'post_init': None, '_uuid': u'edeba9960297fc2b91355c17c63ac6b3', 'style': 0, 'docstr': u'ic.components.icgrid.html', 'flag': 8192, 'recount': None, 'label_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': None, 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'label_attr', 'alignment': (u'left', u'middle')}, 'name': u'planGrid', 'label_height': 20, 'changed': None, 'onSize': None, 'alias': None, 'init_expr': u'', 'position': wx.Point(18, 18), 'onInit': u'', 'refresh': None}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'name': u'rightPanel', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(104, 0), 'onInit': None}, 'min_panelsize': 20, '_uuid': u'de66686b146f7511b642d5f596c3cdeb', 'style': 768, 'docstr': u'ic.components.icsplitter-module.html', 'flag': 8192, 'recount': None, 'span': (1, 1), 'name': u'splitterPanel', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(-3, 25), 'sash_pos': 100, 'onInit': None}, {'activate': u'0', 'show': 1, 'mouseClick': u"import plan.calc_plan as calc_plan\r\nmetaObj = _dict_obj['Plans']\r\nval = calc_plan.getDayPlanValue('2005.01.15', metaObj, \r\n                    mVidProd='013',\r\n                    mReg='0191')\r\n# print '<<< PLAN VALUE >>>:', val", 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'button', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'8cbff8845e6bdc2a2280957ee24f6c59', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_2932', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None, 'refresh': None, 'mouseContextDown': None}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'name': u'planPanel', 'refresh': u'', 'alias': None, 'init_expr': u'None', 'position': (-1, -1), 'onInit': u"# print '----- OnInit Grid'\r\ngrid = _dict_obj['planGrid']\r\n\r\nbuff = [\r\n        ['a', 1, 100],\r\n        ['b', 2, 200],\r\n        ['c', 1, 100]\r\n    ]\r\ngrid.dataset.SetDataBuff(buff)\r\ngrid.RefreshGrid()"}

#   Версия объекта
__version__ = (1, 1, 7, 1)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'IPlanPanel'

class IPlanPanel(icobjectinterface.icObjectInterface):
    #   Буфер панелей
    edtPanelBuff = {}

    def __init__(self, parent):
        """
        """
        #   Указатель на левую панель
        self.ILeftPanel = None
        #   Чистим буфер панелей
        IPlanPanel.edtPanelBuff = {}
        
        #   Вызываем конструктор базового класса
        icobjectinterface.icObjectInterface.__init__(self, parent, resource)
    
    def GeneratePanTree(self, codYearPlan, func=None):
        """
        Функция генерирует дерево планов по статистике.
        """
        pass
        
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
            # print '!!! SaveData'
            
        if 1:#data._edit_form:

            if data.isLock():
                msgbox.MsgBox(split, 'Элемент плана заблокирован пользлвателем <%s>' % data.ownerLock())
            else:
                # print '????? >>>> lock() ??????'
                data.lock()
                
            ## print '{{{{{{ data name=', data.name
  
            # Сохраняем старую панель в буфере
            if self.ILeftPanel and not self.ILeftPanel.itemTree in tree.GetDelItemLst():
                oldItem = self.ILeftPanel.itemTree
#                # print '<<<<< Before >>>>>'
#                old_lev, old_data = tree.GetPyData(oldItem)
#                # print '<<<<< After >>>>>'
                if not IPlanPanel.edtPanelBuff.has_key(self.ILeftPanel.metatype):
                    IPlanPanel.edtPanelBuff[self.ILeftPanel.metatype] = self.ILeftPanel
                
                if oldItem == tree.root:
                    self.ILeftPanel.Show(False)
                else:
                    self.ILeftPanel.getObject().Show(False)
                    
            # Если панель сохранена достаем ее из буфера
            if IPlanPanel.edtPanelBuff.has_key(data.value.metatype):
                self.ILeftPanel = IPlanPanel.edtPanelBuff[data.value.metatype]
                
                if item == tree.root:
                    obj = self.ILeftPanel
                    self.ILeftPanel.metaObj = data
                    obj.Show()
                else:
                    obj = self.ILeftPanel.getObject()
                    self.ILeftPanel.metaObj = data
                    obj.Show()
                    self.ILeftPanel.LoadData()
                
            # В противном случае создаем
            elif item != tree.root:
                obj = data.Edit(split, data)
                self.ILeftPanel = obj.evalSpace['WrapperObj']
            # Для корневого элемента создаем панельку
            else:
                obj = wx.Panel(split, -1)
                self.ILeftPanel = obj
                self.ILeftPanel.metaObj = data
  
            self.ILeftPanel.tree = tree
            self.ILeftPanel.itemTree = item
            self.ILeftPanel.metatype = data.value.metatype
            
            split.Unsplit()
            split.SplitVertically(leftPanel, obj, pos)
            split.Refresh()
        
        return None
    
    def OnCloseFuncplanPanel(self, evt):
        """
        Функция обрабатывает событие <?>.
        """
        # print '@@@@@@@@@@@@ OnClose'
        tree = self.GetNameObj('plansTreeCtrl')
#        item = tree.GetSelection()
#        level, data = tree.GetPyData(item)
        if self.ILeftPanel:
            data = self.ILeftPanel.metaObj
            data.unLock()

        return None
    
    ###END EVENT BLOCK
    
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