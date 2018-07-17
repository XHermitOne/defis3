#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
#import ic.interfaces.icobjectinterface as icobjectinterface

from work_flow.interfaces.forms import edit_panel

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': (192, 192, 192), 'type': u'Panel', 'description': u'\u041f\u0430\u043d\u0435\u043b\u044c \u0440\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f \u043f\u0430\u043f\u043a\u0438', 'onClose': None, '_uuid': u'1af59d4fd097738a6215cd4439815ec9', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'description': None, 'position': (0, 0), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'61eb7c69eeca215eb6d1e226a58e12d5', 'proportion': 0, 'name': u'DefaultName_2268', 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'style': 0, 'activate': 1, 'span': (1, 1), 'description': None, 'component_module': None, 'type': u'SizerSpace', '_uuid': u'ec3ea450cf948ce0ed0f117f1d3f414c', 'proportion': 0, 'name': u'DefaultName_2489', 'alias': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'border': 0, 'size': (0, 0)}, {'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': (192, 192, 192), 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'9b2b929d3af98fae73ee0cdbca713c30', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'activate': 1, 'minCellWidth': 10, 'minCellHeight': 10, 'flexCols': [], 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'flexRows': [], 'component_module': None, 'border': 0, 'proportion': 0, 'type': u'GridBagSizer', 'hgap': 0, 'description': None, '_uuid': u'413416300210ed5f647bef60b409a000', 'flag': 0, 'child': [{'activate': 1, 'show': 1, 'text': u'\u0418\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440', 'keyDown': None, 'font': {}, 'border': 0, 'size': (100, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', 'description': None, '_uuid': u'dd8cf01868ecf0d1bcbf154b2ecd13e5', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_1824', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (1, 1), 'onInit': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'value': u'', 'font': {}, 'border': 0, 'size': (-1, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'bcc318141636c1b69fc27338b1262441', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'nameEditBox', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (1, 2), 'onInit': None, 'refresh': []}, {'activate': 1, 'show': 1, 'text': u'\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', 'keyDown': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', 'description': None, '_uuid': u'8e74e0d41f1fb0a2e5888b2a1be2916b', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_2046', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (1, 4), 'onInit': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': None, 'value': u'', 'font': {}, 'border': 0, 'size': (-1, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'e3c9cb877253a0ef10d2f29f2c202bc4', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'descriptionEditBox', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (1, 5), 'onInit': None, 'refresh': []}], 'name': u'DefaultName_1713', 'alias': None, 'init_expr': None, 'position': (-1, -1), 'vgap': 0}], 'name': u'editPanel', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}, {'style': 0, 'activate': 1, 'span': (1, 1), 'description': None, 'component_module': None, 'type': u'SizerSpace', '_uuid': u'04d281f31f1e5a2d88a1c954872960d6', 'proportion': 0, 'name': u'DefaultName_1491_3041', 'alias': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'border': 0, 'size': (0, 0)}, {'line_color': (200, 200, 200), 'activate': u'0', 'show': 1, 'cols': [], 'row_height': 20, 'keyDown': None, 'border': 0, 'post_select': None, 'size': (-1, -1), 'moveAfterInTabOrder': u'', 'dclickEditor': None, 'span': (1, 1), 'delRec': None, 'component_module': None, 'selected': None, 'proportion': 1, 'getattr': None, 'label': u'Grid', 'source': None, 'init': None, 'backgroundColor': None, 'fixRowSize': 0, 'type': u'GridDataset', 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'fixColSize': 0, 'description': None, 'post_del': None, 'post_init': None, '_uuid': u'a7523cbe07152b819266045073a41096', 'style': 0, 'docstr': u'ic.components.icgrid.html', 'flag': 8192, 'foregroundColor': None, 'recount': None, 'label_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': None, 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'label_attr', 'alignment': (u'left', u'middle')}, 'name': u'docGrid', 'label_height': 20, 'changed': None, 'onSize': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None, 'refresh': None}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'name': u'folder_edit_panel', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}

#   Версия объекта
__version__ = (1, 0, 1, 2)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'IFolderEditPanel'

class IFolderEditPanel(edit_panel.IEditPanel):
    '''
    Панель редактирования свойств папки документов.
    '''
    def __init__(self, parent,metaObj=None,tree=None):
        '''
        Конструктор интерфейса.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type metaObj: C{icMetaItem}
        @param metaObj: Указатель на метаобъект.
        @type tree: C{ic.components.user.ictreelistctrl.icTreeListCtrl}
        @param tree: Указатель на дерево метаобъектов.
        '''
        #
        
        #   Вызываем конструктор базового класса
        edit_panel.IEditPanel.__init__(self, parent, resource, metaObj, tree)
            
    def LoadData(self):
        """
        Загружаем данные.
        """
        if self.metaObj:
            #СВойства метаобъекта
            self.GetNameObj('nameEditBox').SetValue(self.metaObj.value.name)
            self.GetNameObj('descriptionEditBox').SetValue(self.metaObj.value.description)
            #self.GetNameObj('planGrid').dataset.SetDataBuff(self._data)
            #self.GetNameObj('planGrid').RefreshGrid()
                
            #return self._data
            
    def SaveData(self, bRefresh=False):
        """
        Сохранение плана.
        """
        if self.metaObj:
            #bChange = False
            old_name = self.metaObj.value.name
            old_description = self.metaObj.value.description
            #   Сохраняем основные свойства
            self.metaObj.value.description = self.GetNameObj('descriptionEditBox').GetValue().strip()
            #   По необходимости переименовываем
            #print 'enter SaveData!!!',self.GetNameObj('nameEditBox').GetValue().strip()
            self.metaObj.rename(self.GetNameObj('nameEditBox').GetValue().strip())

            #bRefresh = self.SaveChildrenData(data, bRefresh)
                
            #   Обновляем Дерево
            if self.metaObj.value.description <> old_description and self.tree and self.itemTree:
                self.tree.SetItemText(self.itemTree, self.metaObj.value.description, 0)
                
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK
    
def test(par=0):
    '''
    Тестируем класс IFolderEditPanel.
    '''
    
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
