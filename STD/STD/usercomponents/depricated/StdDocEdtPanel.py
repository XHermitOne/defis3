#!/usr/bin/env python
# -*- coding: utf-8 -*-
### TEMPLATE_MODULE:
"""
Панель редактирования страндартного документа.
"""
import wx
import ic.interfaces.ictemplate as ictemplate
import ic.utils.util as util
import copy

### Общий интерфейс компонента
ictemplate.init_component_interface(globals(), ic_class_name = 'CStdDocEdtPanel')

ic_class_spc = {'name':'defaultPanel',
                'type':'StdDocEdtPanel',
                '__parent__':ictemplate.SPC_IC_TEMPLATE}
                
### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'style': 0, 'activate': 1, 'span': (1, 1), 'description': None, 'component_module': None, 'type': u'EditObjPanel', 'nest': u'Panel:ObjPanel', '_uuid': u'2490f4102aa707705dbd2d9273d2175e', 'proportion': 0, 'name': u'XPanel', 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'description': None, 'position': (0, 0), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'a4f870f04add6cfd1fca4bb1a233ddb5', 'proportion': 0, 'name': u'DefaultName_1480', 'alias': None, 'flag': 8192, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'child': [{'activate': 1, 'proportion': 0, 'border': 0, 'size': wx.Size(70, 20), 'style': 0, 'span': (1, 1), 'component_module': None, 'przn_border': [1, 1, 1, 1], 'label': u'ID \u0414\u043e\u043a.', 'isSort': False, 'scheme': u'WHITE', 'type': u'StdLabelCell', 'description': None, 'shortHelpString': u'', 'nest': None, '_uuid': u'87033e6c388ad7ebddd2b3c12836909f', 'flag': 0, 'child': [], 'name': u'defaultPanel_2859_4425', 'round_corner': [1, 1, 1, 1], 'alias': None, 'init_expr': None, 'position': (10, 10)}, {'activate': 1, 'proportion': 0, 'border': 0, 'size': wx.Size(70, 20), 'style': 0, 'span': (1, 1), 'component_module': None, 'przn_border': [1, 1, 1, 1], 'label': u'\u0410\u0442\u0440\u0438\u0431\u0443\u0442 \u04101', 'isSort': False, 'scheme': u'WHITE', 'type': u'StdLabelCell', 'description': None, 'shortHelpString': u'', 'nest': None, '_uuid': u'5eef3e5c7abfeed09087d29811340f8c', 'flag': 0, 'child': [], 'name': u'defaultPanel_2859', 'round_corner': [1, 1, 1, 1], 'alias': None, 'init_expr': None, 'position': wx.Point(10, 40)}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': None, 'value': u'', 'font': {}, 'border': 0, 'size': wx.Size(200, 20), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'501e017c9934715d043f4f3a28e16f6a', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'edtA1', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(85, 40), 'onInit': None, 'refresh': []}, {'activate': 1, 'proportion': 0, 'border': 0, 'size': wx.Size(70, 20), 'style': 0, 'span': (1, 1), 'component_module': None, 'przn_border': [1, 1, 1, 1], 'label': u'\u0410\u0442\u0440\u0438\u0431\u0443\u0442 \u04102', 'isSort': False, 'scheme': u'WHITE', 'type': u'StdLabelCell', 'description': None, 'shortHelpString': u'', 'nest': None, '_uuid': u'6d3182142b46f39966db79fe19f5ba9a', 'flag': 0, 'child': [], 'name': u'defaultPanel_2859_3240', 'round_corner': [1, 1, 1, 1], 'alias': None, 'init_expr': None, 'position': wx.Point(10, 70)}, {'activate': 1, 'proportion': 0, 'border': 0, 'size': wx.Size(70, 20), 'style': 0, 'span': (1, 1), 'component_module': None, 'przn_border': [1, 1, 1, 1], 'label': u'\u0410\u0442\u0440\u0438\u0431\u0443\u0442 \u04103', 'isSort': False, 'scheme': u'WHITE', 'type': u'StdLabelCell', 'description': None, 'shortHelpString': u'', 'nest': None, '_uuid': u'f76f493be9949e198aaa616d87dee31f', 'flag': 0, 'child': [], 'name': u'LabelA3', 'round_corner': [1, 1, 1, 1], 'alias': None, 'init_expr': None, 'position': wx.Point(10, 100)}, {'activate': 1, 'proportion': 0, 'border': 0, 'size': wx.Size(65, 20), 'style': 0, 'span': (1, 1), 'component_module': None, 'przn_border': [1, 1, 1, 1], 'label': u'\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435', 'isSort': False, 'scheme': u'WHITE', 'type': u'StdLabelCell', 'description': None, 'shortHelpString': u'\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430', 'nest': None, '_uuid': u'83f105c593a47ab71acb75c939a85ece', 'flag': 0, 'child': [], 'name': u'LabelName', 'round_corner': [1, 1, 1, 1], 'alias': None, 'init_expr': None, 'position': wx.Point(155, 10)}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': None, 'value': u'', 'font': {}, 'border': 0, 'size': wx.Size(200, 20), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'e092b5080b189c43225fd5c73a292fab', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'edtA2', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(85, 70), 'onInit': None, 'refresh': []}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': None, 'value': u'', 'font': {}, 'border': 0, 'size': wx.Size(200, 20), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'2e81900313aa97bc216367c3348703d7', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'edtA3', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(85, 100), 'onInit': None, 'refresh': []}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': None, 'value': u'', 'font': {}, 'border': 0, 'size': wx.Size(60, 20), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'61585baa73fb81e290556d1a6c01a012', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'edtID', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(85, 10), 'onInit': None, 'refresh': []}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': wx.Size(100, 20), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'223e3e9c0877a0424b7aa572b97fe4eb', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'edtName', 'changed': None, 'value': u'', 'alias': None, 'init_expr': None, 'position': wx.Point(225, 10), 'onInit': None, 'refresh': []}], 'keyDown': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': (238, 242, 249), 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'393642dc2330ab8695a0cc32fce65abd', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'recount': None, 'name': u'defaultWindow_1485', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(0, 0), 'onInit': None}, {'style': 0, 'activate': 1, 'span': (1, 1), 'description': None, 'component_module': None, 'type': u'StdDataGrid', 'nest': u'GridDataset:DataGrid', '_uuid': u'186162e8d6e4205116edad98b8f6fe01', 'proportion': 0, 'name': u'defaultPanel_1972', 'alias': None, 'flag': 8192, 'init_expr': None, 'child': [{'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'id', 'width': 50, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'1b1116b594b9bb298e5935ec1cef60c1', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'id', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435', 'width': 135, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': u'1', 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'd0dc4c43e42e0b9fc8d4213eba36c9d2', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'name', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'S1', 'width': 72, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'2e02ee8f3d8bbac3f9f09e8027709aeb', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u's1', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'S2', 'width': 65, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'0789f99d0e46d487c8d066f80bb80a46', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u's2', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'S3', 'width': 65, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'0789f99d0e46d487c8d066f80bb80a46', 'recount': None, 'getvalue': u'', 'name': u's3', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}], 'position': (-1, -1), 'scheme': u'WHITE', 'border': 0, 'size': (-1, -1)}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'position': wx.Point(0, 0), 'border': 0, 'size': (-1, 400)}

#   Версия объекта
__version__ = (1, 0, 2, 0)
###END SPECIAL BLOCK

class CStdDocEdtPanel(ictemplate.icTemplateInterface):
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
        ictemplate.icTemplateInterface.__init__(self, parent, id, component, logType, evalSpace,
                                                bCounter, progressDlg)
    def _init_template_resource(self):
        """
        Инициализация ресурса шаблона.
        """
        self._templRes = resource
    
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK
    
def test(par=0):
    """
    Тестируем класс CStdDocEdtPanel.
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