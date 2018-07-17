#!/usr/bin/env python
# -*- coding: utf-8 -*-
### TEMPLATE_MODULE:
"""
Стилизованный грид. Функциональность такаяже как и у icGridDataset
Для настройки используются схемы представления в атрибуте <scheme>.

"""
import wx
import ic.interfaces.ictemplate as ictemplate
import ic.PropertyEditor.icDefInf as icDefInf
import ic.utils.util as util
import copy

### Общий интерфейс компонента
ictemplate.init_component_interface(globals(), ic_class_name = 'CStdDataGrid')

ic_class_spc = {'name':'defaultPanel',
                'type':'StdDataGrid',
                'scheme':'BLUE',
                'LabelFgrColor': None,
                'LabelBgrColor': None,
                'LabelBorderColor': None,
                'init':None,
                'delRec':None,
                'getattr':None,
                'keyDown':None,
                'source':None,
                'changed':None,
                'nest':'GridDataset:DataGrid',
                '__events__':{'keyDown':('wx.EVT_KEY_DOWN','OnKeyDown', False)},
                '__attr_types__': {0: ['name', 'type'],
                        icDefInf.EDT_COLOR:['LabelFgrColor', 'LabelBgrColor', 'LabelBorderColor'],
                        icDefInf.EDT_CHOICE:['scheme']},
                '__lists__':{'scheme':['WHITE','FLAT_GRAY','BLUE','LIGHT_BLUE','STD',
                                       'GRAY','LIGHT_BROWN','GOLD','GREEN','BLACK', 'RED'],
                             'nest':['GridDataset:DataGrid']},
                '__parent__':ictemplate.SPC_IC_TEMPLATE}

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['GridCell']
                
### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'obj_module': None, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (50, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'res_module': None, 'description': None, 'onClose': None, '_uuid': u'06999d630ab17df3ce63a18fdc811b8c', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'child': [{'hgap': 0, 'style': 0, 'activate': u'1', 'layout': u'vertical', 'description': None, 'position': (0, 0), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'f614de928a181082f50696600095e073', 'proportion': 0, 'name': u'GBSizer', 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'recount': None, 'keyDown': None, 'font': {}, 'border': 0, 'alignment': (u'left', u'middle'), 'size': wx.Size(379, 31), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'Head', 'res_module': None, 'description': None, '_uuid': u'8536c73753c10daba66b06065bdf8853', 'style': 0, 'flag': 8192, 'child': [{'activate': 1, 'obj_module': None, 'proportion': 0, 'border': 0, 'size': (100, -1), 'borderColor': None, 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'przn_border': [1, 1, 1, 1], 'label': u'Left', 'backgroundColor': None, 'isSort': None, 'scheme': u'BLUE', 'type': u'StdLabelCell', 'res_module': None, 'description': None, 'shortHelpString': u'', 'nest': None, '_uuid': u'd8919314dfaf22e468f1c7bbe471705a', 'flag': 0, 'child': [], 'nest_name': u'', 'nest_type': u'', 'name': u'ICellLeft', 'round_corner': [1, 0, 0, 0], 'alias': None, 'init_expr': None, 'position': (0, 0)}, {'activate': 1, 'obj_module': None, 'proportion': 0, 'border': 0, 'size': (100, -1), 'borderColor': None, 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'przn_border': [0, 1, 1, 1], 'label': u'Mid', 'backgroundColor': None, 'isSort': False, 'scheme': u'GREEN', 'type': u'StdLabelCell', 'res_module': None, 'description': None, 'shortHelpString': u'\u041a\u043e\u0440\u043e\u0442\u043a\u0430\u044f \u043f\u043e\u0434\u0441\u043a\u0430\u0437\u043a\u0430\r\n\u0434\u043b\u044f \u0437\u0430\u0433\u043e\u043b\u043e\u0432\u043a\u0430 \u043a\u043e\u043b\u043e\u043d\u043a\u0438', 'nest': None, '_uuid': u'5fcb2bf62786a496a6a217629b3171a7', 'flag': 0, 'child': [], 'nest_name': u'', 'nest_type': u'', 'name': u'ICellMid', 'round_corner': [0, 0, 0, 0], 'alias': None, 'init_expr': None, 'position': (0, 1)}, {'activate': 1, 'obj_module': None, 'proportion': 0, 'border': 0, 'size': (100, -1), 'borderColor': None, 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'przn_border': [0, 1, 1, 1], 'label': u'Right', 'backgroundColor': None, 'isSort': False, 'scheme': u'GOLD', 'type': u'StdLabelCell', 'res_module': None, 'description': None, 'shortHelpString': u'', 'nest': None, '_uuid': u'3689ecce80930044322f741770acdbaa', 'flag': 0, 'child': [], 'nest_name': u'', 'nest_type': u'', 'name': u'ICellRight', 'round_corner': [0, 1, 0, 0], 'alias': None, 'init_expr': None, 'position': (0, 2)}], 'name': u'LabelGridHead', 'refresh': None, 'alias': None, 'init_expr': u'', 'position': (1, 1), 'onInit': None}, {'line_color': (200, 200, 200), 'activate': 1, 'show': 1, 'init_expr': u"header = GetObject('LabelGridHead')\r\nself.SetHeader(header, False, True)\r\nself.ReconstructHeader()\r\n\r\nif not self.GetResource()['source']:\r\n    import ic.db.icdocdataset as mod\r\n    dataset = mod.icDocDataset(-1,\r\n                {'description':self.GetTable().exCols,\r\n                 'wxGridTypes':self.GetTable().dataTypes})\r\n    self.GetTable().SetDataset(dataset)\r\n", 'cols': [{'activate': u'1', 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'col', 'width': 87, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': u'None', 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'8509e9a721f4ff9ff9339d84e22a1c11', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'aad6ca349720ab7da17d4a360c239048', 'recount': None, 'getvalue': u'', 'name': u'default_2273', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(9, 19)}, {'activate': u'1', 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'col', 'width': 98, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'b389fea9b98016ea9e075b39cf235a81', 'recount': None, 'getvalue': u'', 'name': u'default_2295', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(9, 16)}, {'activate': u'1', 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'col', 'width': 99, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'881e684673f8a760bce1d2c514fa3fc7', 'recount': None, 'getvalue': u'', 'name': u'default_2317', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(8, 18)}], 'keyDown': None, 'border': 0, 'post_select': None, 'size': wx.Size(318, 190), 'moveAfterInTabOrder': u'', 'dclickEditor': None, 'span': (1, 1), 'delRec': None, 'row_height': 18, 'selected': None, 'proportion': 1, 'getattr': None, 'label': u'Grid', 'source': None, 'init': None, 'backgroundColor': None, 'fixRowSize': 0, 'type': u'GridDataset', 'res_module': None, '_uuid': u'9a36245d3d6d61e7fee3887b9bc36d99', 'fixColSize': 0, 'description': None, 'post_del': None, 'post_init': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'43ea2c07574442e450f3b1fd648dc601', 'backgroundColor': None, 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'style': 0, 'docstr': u'ic.components.icgrid.html', 'flag': 8192, 'foregroundColor': None, 'recount': None, 'label_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'7913b7c7a34691849f0ee2f2aaac9aa1', 'backgroundColor': (0, 87, 174), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'label_attr', 'alignment': (u'left', u'middle')}, 'name': u'DataGrid', 'label_height': 18, 'changed': None, 'onSize': None, 'alias': None, 'component_module': None, 'position': (2, 1), 'onInit': None, 'refresh': None}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}, {'activate': u'0', 'minCellWidth': 1, 'minCellHeight': 1, 'border': 0, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'flexRows': [2], 'component_module': None, 'flexCols': [1], 'proportion': 1, 'type': u'GridBagSizer', 'hgap': 0, 'description': None, '_uuid': u'313202d9b3a80895cbb41313c4f41f35', 'flag': 8192, 'child': [{'style': 0, 'activate': 1, 'span': (1, 1), 'description': None, 'component_module': None, 'border': 0, '_uuid': u'3ef57ae607ec6c162727d8ed0f12292d', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': (1, 2), 'size': (0, 0), 'type': u'SizerSpace', 'name': u'DefaultName_1246_2817'}, {'style': 0, 'activate': 1, 'span': (1, 1), 'description': None, 'component_module': None, 'border': 0, '_uuid': u'3ef57ae607ec6c162727d8ed0f12292d', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': (3, 1), 'size': (0, 0), 'type': u'SizerSpace', 'name': u'DefaultName_1246_1487'}, {'activate': 1, 'show': 1, 'recount': None, 'keyDown': None, 'font': {}, 'border': 0, 'alignment': (u'left', u'middle'), 'size': wx.Size(379, 31), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'source': None, 'backgroundColor': (235, 235, 235), 'type': u'Head', 'description': None, '_uuid': u'e131204a3df36188577f3b9c654ba7b3', 'style': 0, 'flag': 8192, 'child': [{'activate': 1, 'proportion': 0, 'border': 0, 'size': (100, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'przn_border': [1, 1, 0, 1], 'label': u'Left', 'isSort': None, 'scheme': u'BLUE', 'type': u'StdLabelCell', 'description': None, 'shortHelpString': u'', 'nest': None, '_uuid': u'd8919314dfaf22e468f1c7bbe471705a', 'flag': 0, 'child': [], 'nest_name': u'', 'nest_type': u'', 'name': u'ICellLeft', 'round_corner': [1, 0, 0, 0], 'alias': None, 'init_expr': None, 'position': (0, 0)}, {'activate': 1, 'proportion': 0, 'border': 0, 'size': (100, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'przn_border': [1, 1, 0, 1], 'label': u'Mid', 'isSort': False, 'scheme': u'GREEN', 'type': u'StdLabelCell', 'description': None, 'shortHelpString': u'\u041a\u043e\u0440\u043e\u0442\u043a\u0430\u044f \u043f\u043e\u0434\u0441\u043a\u0430\u0437\u043a\u0430\r\n\u0434\u043b\u044f \u0437\u0430\u0433\u043e\u043b\u043e\u0432\u043a\u0430 \u043a\u043e\u043b\u043e\u043d\u043a\u0438', 'nest': None, '_uuid': u'5fcb2bf62786a496a6a217629b3171a7', 'flag': 0, 'child': [], 'nest_name': u'', 'nest_type': u'', 'name': u'ICellMid', 'round_corner': [0, 0, 0, 0], 'alias': None, 'init_expr': None, 'position': (0, 1)}, {'activate': 1, 'proportion': 0, 'border': 0, 'size': (100, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'przn_border': [1, 1, 1, 1], 'label': u'Right', 'isSort': False, 'scheme': u'GOLD', 'type': u'StdLabelCell', 'description': None, 'shortHelpString': u'', 'nest': None, '_uuid': u'3689ecce80930044322f741770acdbaa', 'flag': 0, 'child': [], 'nest_name': u'', 'nest_type': u'', 'name': u'ICellRight', 'round_corner': [0, 1, 0, 0], 'alias': None, 'init_expr': None, 'position': (0, 2)}], 'name': u'LabelGridHead', 'refresh': None, 'alias': None, 'init_expr': u'', 'position': (1, 1), 'onInit': None}, {'line_color': (200, 200, 200), 'activate': 1, 'show': 1, 'cols': [{'activate': u'1', 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'col', 'width': 87, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': u'None', 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'8509e9a721f4ff9ff9339d84e22a1c11', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'aad6ca349720ab7da17d4a360c239048', 'recount': None, 'getvalue': u'', 'name': u'default_2273', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(9, 19)}, {'activate': u'1', 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'col', 'width': 98, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'b389fea9b98016ea9e075b39cf235a81', 'recount': None, 'getvalue': u'', 'name': u'default_2295', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(9, 16)}, {'activate': u'1', 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'col', 'width': 99, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'881e684673f8a760bce1d2c514fa3fc7', 'recount': None, 'getvalue': u'', 'name': u'default_2317', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(8, 18)}], 'keyDown': None, 'border': 0, 'post_select': None, 'size': wx.Size(318, 190), 'moveAfterInTabOrder': u'', 'dclickEditor': None, 'span': (1, 1), 'delRec': None, 'row_height': 18, 'selected': None, 'proportion': 1, 'getattr': None, 'label': u'Grid', 'source': None, 'init': None, 'backgroundColor': None, 'fixRowSize': 0, 'type': u'GridDataset', 'init_expr': u"header = GetObject('LabelGridHead')\r\nself.SetHeader(header, False, True)\r\nself.ReconstructHeader()\r\n\r\nimport ic.db.icdocdataset as mod\r\ndataset = mod.icDocDataset(-1,\r\n            {'description':self.GetTable().exCols,\r\n             'wxGridTypes':self.GetTable().dataTypes})\r\nself.GetTable().SetDataset(dataset)\r\n", '_uuid': u'c29ec030bf4319650928763d8393e590', 'fixColSize': 0, 'description': None, 'post_del': None, 'post_init': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'43ea2c07574442e450f3b1fd648dc601', 'backgroundColor': (247, 247, 247), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'style': 0, 'docstr': u'ic.components.icgrid.html', 'flag': 8192, 'foregroundColor': None, 'recount': None, 'label_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'7913b7c7a34691849f0ee2f2aaac9aa1', 'backgroundColor': (0, 87, 174), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'label_attr', 'alignment': (u'left', u'middle')}, 'name': u'DataGrid', 'label_height': 18, 'changed': None, 'onSize': None, 'alias': None, 'component_module': None, 'position': (2, 1), 'onInit': None, 'refresh': None}], 'name': u'GBSizer_1298', 'alias': None, 'init_expr': None, 'position': (-1, -1), 'vgap': 0}], 'name': u'testGridPanel', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}

#   Версия объекта
__version__ = (1, 0, 5, 5)
###END SPECIAL BLOCK

class CStdDataGrid(ictemplate.icTemplateInterface):
    """
    Описание пользовательского компонента.
    
    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{type='defaultType'}:
        - B{name='default'}:
    """
    component_spc = ic_class_spc
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace = None, bCounter=False, progressDlg=None):
        """
        Конструктор интерфейса.
        """
        #   Дополняем до спецификации
        component = util.icSpcDefStruct(ic_class_spc, component)
        self.scheme = component['scheme']
        self._LBgrClr = component['LabelBgrColor']
        self._LFgrClr = component['LabelFgrColor']
        self._LBrClr = component['LabelBorderColor']
        
        ictemplate.icTemplateInterface.__init__(self, parent, id, component, logType, evalSpace,
                                                bCounter, progressDlg)
        self._build_head_by_cols()
        self.resource['name'] = component['name']
        grid_res = self.GetObjectResource('DataGrid')
        grid_res['keyDown'] = component['keyDown']
        grid_res['init'] = component['init']
        grid_res['delRec'] = component['delRec']
        grid_res['getattr'] = component['getattr']
        grid_res['source'] = component['source']
        grid_res['_uuid'] = component['_uuid']
        grid_res['changed'] = component['changed']
        
    def _build_head_by_cols(self):
        """
        Функция генерирует описание шапки грида по описанию колонок.
        """
        
        #   Находим нужные ресурсные описания
        grid_res = self.GetObjectResource('DataGrid')
        head_res = self.GetObjectResource('LabelGridHead')
        head_lst = []#[None for x in grid_res['cols']]
        
        cell_left = self.GetObjectResource('ICellLeft',resource=head_res)
        cell_mid = self.GetObjectResource('ICellMid',resource=head_res)
        cell_right = self.GetObjectResource('ICellRight',resource=head_res)
        i = 0
        for col in grid_res['cols']:
            
            if util.isAcivateRes(col, self.GetContext()):
                if i==0:
                    cell = copy.deepcopy(cell_left)
                elif i == len(grid_res['cols']) -1:
                    cell = copy.deepcopy(cell_right)
                else:
                    cell = copy.deepcopy(cell_mid)
                
                #   Переопределяем атрибуты
                #print '### res=', self.resource.keys()
                cell['position'] = (0, i)
                cell['label'] = col['label']
                cell['activate'] = col['activate']
                cell['shortHelpString'] = col['shortHelpString']
                cell['scheme'] = self.scheme
                cell['isSort'] = col['sort']
                cell['foregroundColor'] = self._LFgrClr
                cell['backgroundColor'] = self._LBgrClr
                cell['borderColor'] = self._LBrClr
                #print '---- col label =', i, col['label']
                
                #head_lst[i] = cell
                head_lst.append(cell)
                i += 1
        
        #   Определяем старую колонку, если некоторые колонки не активированы
        #   activate==0
        if len(head_lst) < len(grid_res['cols']):
            lcell = head_lst[-1]
            cell = copy.deepcopy(cell_right)
            cell['position'] = lcell['position']
            cell['label'] = lcell['label']
            cell['shortHelpString'] = lcell['shortHelpString']
            cell['scheme'] = lcell['scheme']
            cell['isSort'] = lcell['isSort']
            cell['foregroundColor'] = lcell['foregroundColor']
            cell['backgroundColor'] = lcell['backgroundColor']
            cell['borderColor'] = lcell['borderColor']
            head_lst[-1] = cell
            
        head_res['child'] = head_lst
        
    def _init_template_resource(self):
        """
        Инициализация ресурса шаблона.
        """
        self._templRes = resource
    
    def get_grid(self):
        """
        Возвращает указатель на грид.
        """
        return self.getRegObj('DataGrid')
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK
    
def test(par=0):
    """
    Тестируем класс CStdDataGrid.
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