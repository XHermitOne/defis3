#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Стандартная панель для редактирования документа учета
статей постоянных затрат.
"""
import wx
import ic.interfaces.ictemplate as ictemplate
import ic.utils.util as util
import copy
from STD import reestr_img
import STD.interfaces.reestr.browsPanelInterface as ifs

try:
    from NSI import spravctrl
except:
    print('IMPORT ERROR: from NSI import spravctrl')

### Общий интерфейс компонента
ictemplate.init_component_interface(globals(), ic_class_name = 'CStdReestrZtrPanel')

ic_class_spc = {'name':'StdReestrZtrPanelName',
                'type':'StdReestrZtrPanel',
                '__parent__':ictemplate.SPC_IC_TEMPLATE}
                
### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'style': 0, 'activate': 1, 'span': (1, 1), 'description': u'\u0421\u0442\u0430\u043d\u0434\u0430\u0440\u0442\u043d\u0430\u044f \u043f\u0430\u043d\u0435\u043b\u044c \u0437\u0430\u0442\u0440\u0430\u0442', 'component_module': None, 'type': u'EditObjPanel', 'nest': u'Panel:ObjPanel', '_uuid': u'908c2f96515ed337451b9008ca7352f9', 'proportion': 0, 'name': u'ZtrPanel', 'alias': None, 'flag': 0, 'load_data': u"print '>>> LOAD_DATA'\r\nifs = self.GetComponentInterface()\r\nprint '------ IFS=', ifs, self.get_object()\r\nifs.set_object(self.get_object())\r\nifs.LoadData()\r\n", 'init_expr': None, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'description': None, 'position': (0, 0), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'a4f870f04add6cfd1fca4bb1a233ddb5', 'proportion': 1, 'name': u'DefaultName_1480', 'alias': None, 'flag': 8192, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': wx.Size(492, 156), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'f0f4595942f2406139a9d12e855e83f4', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'child': [{'activate': 1, 'proportion': 0, 'border': 0, 'size': (70, 18), 'borderColor': (111, 147, 179), 'style': 0, 'foregroundColor': (28, 70, 108), 'span': (1, 1), 'component_module': None, 'przn_border': [1, 1, 1, 1], 'label': u'Id', 'backgroundColor': (191, 217, 238), 'isSort': False, 'scheme': u'STD', 'type': u'StdLabelCell', 'description': None, 'shortHelpString': u'\u0418\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u044f', 'nest': None, '_uuid': u'e5a91a2691e73549f3efd6531c7524b3', 'flag': 0, 'child': [], 'name': u'doc_id_label', 'round_corner': [1, 1, 1, 1], 'alias': None, 'init_expr': None, 'position': wx.Point(7, 7)}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': None, 'value': u'', 'font': {}, 'border': 0, 'size': (60, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'7ac8a07d5760d926cbce6a33a4bdb6ee', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'edtID', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(82, 7), 'onInit': None, 'refresh': []}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'value': u'', 'font': {}, 'border': 0, 'size': wx.Size(160, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'223e3e9c0877a0424b7aa572b97fe4eb', 'moveAfterInTabOrder': u'edtID', 'flag': 0, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'edtName', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(250, 7), 'onInit': None, 'refresh': []}, {'activate': 1, 'proportion': 0, 'border': 0, 'size': (70, 18), 'borderColor': (111, 147, 179), 'style': 0, 'foregroundColor': (28, 70, 108), 'span': (1, 1), 'component_module': None, 'przn_border': [1, 1, 1, 1], 'label': u'\u0421\u0443\u043c\u043c\u0430 1', 'backgroundColor': (191, 217, 238), 'isSort': False, 'scheme': u'STD', 'type': u'StdLabelCell', 'description': None, 'shortHelpString': u'\u0421\u0443\u043c\u043c\u0430 \u043f\u043e \u0443\u043d\u0438\u043a\u0430\u043b\u044c\u043d\u044b\u043c \u0441\u0442\u0430\u0442\u044c\u044f\u043c \u0437\u0430\u0442\u0440\u0430\u0442 \u0443\u0437\u043b\u0430', 'nest': None, '_uuid': u'eac1d8a555b619fcc013bf68a92f4931', 'flag': 0, 'child': [], 'name': u'doc_summa1_label', 'round_corner': [1, 1, 1, 1], 'alias': None, 'init_expr': None, 'position': wx.Point(7, 37)}, {'activate': 1, 'ctrl': None, 'pic': u'999,999,999.99', 'hlp': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': wx.Size(90, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'223e3e9c0877a0424b7aa572b97fe4eb', 'moveAfterInTabOrder': u'edtTitle', 'flag': 0, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'edtSumma1', 'changed': None, 'value': u'', 'alias': None, 'init_expr': None, 'position': wx.Point(82, 37), 'onInit': None, 'refresh': []}, {'activate': 1, 'proportion': 0, 'border': 0, 'size': (70, 18), 'borderColor': (111, 147, 179), 'style': 0, 'foregroundColor': (28, 70, 108), 'span': (1, 1), 'component_module': None, 'przn_border': [1, 1, 1, 1], 'label': u'\u0421\u0443\u043c\u043c\u0430 2', 'backgroundColor': (191, 217, 238), 'isSort': False, 'scheme': u'STD', 'type': u'StdLabelCell', 'description': None, 'shortHelpString': u'\u0421\u0443\u043c\u043c\u0430 \u043f\u043e \u0432\u0441\u0435\u043c \u0441\u0442\u0430\u0442\u044c\u044f\u043c \u0437\u0430\u0442\u0440\u0430\u0442.\r\n\u0423\u043d\u0438\u043a\u0430\u043b\u044c\u043d\u044b\u0435 \u0441\u0442\u0430\u0442\u044c\u0438 \u0437\u0430\u0442\u0440\u0430\u0442 + \u0441\u0443\u043c\u043c\u0430 \r\n\u043f\u043e \u0434\u043e\u0447\u0435\u0440\u043d\u0438\u043c \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u0430\u043c \u0437\u0430\u0442\u0440\u0430\u0442', 'nest': None, '_uuid': u'fab5c7cc2195d3e14f8314e0da017037', 'flag': 0, 'child': [], 'name': u'doc_summa2_label', 'round_corner': [1, 1, 1, 1], 'alias': None, 'init_expr': None, 'position': wx.Point(178, 37)}, {'activate': 1, 'ctrl': None, 'pic': u'999,999,999.99', 'hlp': None, 'value': u'', 'font': {}, 'border': 0, 'size': wx.Size(90, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'223e3e9c0877a0424b7aa572b97fe4eb', 'moveAfterInTabOrder': u'edtSumma1', 'flag': 0, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'edtSumma2', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(252, 37), 'onInit': None, 'refresh': []}, {'activate': 1, 'proportion': 0, 'border': 0, 'size': (70, 18), 'borderColor': (111, 147, 179), 'style': 0, 'foregroundColor': (28, 70, 108), 'span': (1, 1), 'component_module': None, 'przn_border': [1, 1, 1, 1], 'label': u'\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', 'backgroundColor': (191, 217, 238), 'isSort': False, 'scheme': u'STD', 'type': u'StdLabelCell', 'description': None, 'shortHelpString': u'\u041a\u0440\u0430\u0442\u043a\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u0430 \u0437\u0430\u0442\u0440\u0430\u0442', 'nest': None, '_uuid': u'b1d91b7f60f8282723525f44a1f23165', 'flag': 0, 'child': [], 'name': u'doc_description_label', 'round_corner': [1, 1, 1, 1], 'alias': None, 'init_expr': None, 'position': wx.Point(7, 67)}, {'activate': 1, 'proportion': 0, 'border': 0, 'size': wx.Size(70, 18), 'borderColor': (111, 147, 179), 'style': 0, 'foregroundColor': (28, 70, 108), 'span': (1, 1), 'component_module': None, 'przn_border': [1, 1, 1, 1], 'label': u'\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435', 'backgroundColor': (191, 217, 238), 'isSort': False, 'scheme': u'STD', 'type': u'StdLabelCell', 'description': None, 'shortHelpString': u'\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u0430 \u0437\u0430\u0442\u0440\u0430\u0442', 'nest': None, '_uuid': u'ee20b8760099de4a69ff685e4c6fe801', 'flag': 0, 'child': [], 'name': u'doc_name_label', 'round_corner': [1, 1, 1, 1], 'alias': None, 'init_expr': None, 'position': wx.Point(176, 7)}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': None, 'value': u'', 'font': {}, 'border': 0, 'size': wx.Size(329, 50), 'style': 32, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'e092b5080b189c43225fd5c73a292fab', 'moveAfterInTabOrder': u'edtSumma2', 'flag': 0, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'edtDescr', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(82, 67), 'onInit': None, 'refresh': []}, {'activate': 1, 'show': 1, 'image': u'', 'mouseClick': None, 'border': 0, 'size': wx.Size(62, 20), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041f\u0435\u0440\u0435\u0441\u0447\u0435\u0442', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'ImageButton', 'description': None, 'shortHelpString': u'\u041f\u0435\u0440\u0435\u0441\u0447\u0435\u0442 \u0441\u0443\u043c\u043c \u0437\u0430\u0442\u0440\u0430\u0442', '_uuid': u'6a007364a5f97f8983c2945453133c14', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'countZtrBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(347, 37), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'show': 1, 'image': u'', 'mouseClick': None, 'border': 0, 'size': wx.Size(24, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'...', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'ImageButton', 'description': None, 'shortHelpString': u'', '_uuid': u'7f8a4000d6f66603a434cc40b931741a', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'HlpIdBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(144, 7), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'show': 1, 'child': [], 'keyDown': None, 'border': 0, 'size': (0, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'2de140c06b0595f25631782fdce48655', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'recount': None, 'name': u'defaultWindow_1435', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (42, 104), 'onInit': None}], 'name': u'defaultWindow_1485', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(0, 0), 'onInit': u'self.SetRoundBoundMode((166, 187, 206), 1)'}, {'activate': u'0', 'proportion': 0, 'border': 0, 'size': (120, 15), 'borderColor': (166, 187, 206), 'style': 0, 'foregroundColor': (117, 149, 179), 'span': (1, 1), 'component_module': None, 'przn_border': [1, 1, 1, 0], 'label': u'\u0421\u0442\u0430\u0442\u044c\u0438 \u0437\u0430\u0442\u0440\u0430\u0442', 'backgroundColor': None, 'isSort': False, 'scheme': u'STD', 'type': u'StdLabelCell', 'description': None, 'shortHelpString': u'\u0421\u0442\u0430\u0442\u044c\u0438 \u0437\u0430\u0442\u0440\u0430\u0442 \u043f\u043e \u0434\u0430\u043d\u043d\u043e\u043c\u0443 \r\n\u0443\u0437\u043b\u0443', 'nest': None, '_uuid': u'c6a7ef7dacc32601a2640068469867b4', 'flag': 1024, 'child': [], 'name': u'specLabel', 'round_corner': [1, 1, 0, 0], 'alias': None, 'init_expr': None, 'position': (10, 10)}, {'LabelBgrColor': (0, 98, 196), 'style': 0, 'activate': 1, 'span': (1, 1), 'description': None, 'LabelBorderColor': (0, 61, 121), 'component_module': None, 'type': u'StdDataGrid', 'nest': u'GridDataset:DataGrid', '_uuid': u'43c811238d11a8c11f6b331fff6fd577', 'proportion': 1, 'name': u'ZtrGrid', 'alias': None, 'flag': 8192, 'init_expr': u'', 'child': [{'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u0434', 'width': 62, 'init': u"@''", 'valid': None, 'type': u'GridCell', 'sort': u'1', 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'5c203fe190b79c444b05141a956d96b0', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'\u041a\u043e\u0434 \u0441\u0442\u0430\u0442\u044c\u0438 \u0437\u0430\u0442\u0440\u0430\u0442', '_uuid': u'1b1116b594b9bb298e5935ec1cef60c1', 'recount': None, 'getvalue': u'', 'name': u'cod', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435', 'width': 179, 'init': u"@''", 'valid': None, 'type': u'GridCell', 'sort': u'1', 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'\u041d\u0430\u0437\u0432\u043d\u0438\u0435 \u0441\u0442\u0430\u0442\u044c\u0438 \u0437\u0430\u0442\u0440\u0430\u0442', '_uuid': u'd0dc4c43e42e0b9fc8d4213eba36c9d2', 'recount': None, 'getvalue': u'', 'name': u'name', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'999,999,999.99', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u0421\u0443\u043c\u043c\u0430 1', 'width': 90, 'init': u'0', 'valid': None, 'type': u'GridCell', 'sort': u'1', 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'\u0421\u0443\u043c\u043c\u0430 \u043d\u0430 \u0441\u0442\u0440\u0430\u0442\u044c\u044e \u0437\u0430\u0442\u0440\u0430\u0442, \u0432\u043e\u0437\u043d\u0438\u043a\u0430\u044e\u0449\u0430\u044f\r\n\u043d\u0430 \u0434\u0430\u043d\u043d\u043e\u043c \u0443\u0437\u043b\u0435 \u0437\u0430\u0442\u0440\u0430\u0442', '_uuid': u'0789f99d0e46d487c8d066f80bb80a46', 'recount': None, 'hlp': None, 'attr': u'W', 'setvalue': u'', 'name': u'summ1', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'999,999,999.99', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u0421\u0443\u043c\u043c\u0430 2', 'width': 90, 'init': u'0', 'valid': None, 'type': u'GridCell', 'sort': u'1', 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'a46ad2132289c56d1cdfa47f867fc22d', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'\u0421\u0443\u043c\u043c\u0430 \u043d\u0430 \u0441\u0442\u0440\u0430\u0442\u044c\u044e \u0437\u0430\u0442\u0440\u0430\u0442, \u0441 \u0443\u0447\u0435\u0442\u043e\u043c\r\n\u0434\u043e\u0447\u0435\u0440\u043d\u0438\u0445 \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u043e\u0432', '_uuid': u'0789f99d0e46d487c8d066f80bb80a46', 'recount': None, 'hlp': None, 'name': u'summ2', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u041f\u0440\u0438\u043c\u0435\u0447\u0430\u043d\u0438\u0435', 'width': 195, 'init': u"@''", 'valid': None, 'type': u'GridCell', 'sort': u'1', 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u043c\u0435\u0441\u044f\u0446\u0430', '_uuid': u'6ab6b28a49adf4a85282bd45f17101d1', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'prim', 'keyDown': None, 'alias': None, 'init_expr': None}], 'position': (-1, -1), 'scheme': u'STD', 'border': 0, 'LabelFgrColor': (255, 255, 255), 'size': (50, -1)}, {'activate': u'0', 'ctrl': None, 'pic': u'S', 'hlp': u'_resultEval=GetInterface().GetComponentInterface().hlpMonthCod(evt)', 'keyDown': None, 'font': {}, 'border': 0, 'size': (-1, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'e26c4afbfe76093b45dbe9f2da1378fa', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'monthCodEdt', 'changed': None, 'value': u'', 'alias': None, 'init_expr': None, 'position': wx.Point(0, 464), 'onInit': None, 'refresh': []}, {'activate': u'0', 'ctrl': None, 'pic': u'S', 'getvalue': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': (-1, 18), 'style': 16, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'88bf96fedfd32f697786ddb566771d4f', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'monthNameEdt', 'changed': None, 'value': u'', 'alias': None, 'init_expr': None, 'position': wx.Point(122, 436), 'onInit': None, 'refresh': []}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (50, -1)}], 'position': wx.Point(0, 0), 'border': 0, 'save_data': u"print '>>> SAVE_DATA'\r\nifs = self.GetComponentInterface()\r\n#print '------ IFS=', ifs, self.get_object()\r\n#ifs.set_object(self.get_object())\r\nifs.SaveData()\r\n", 'size': (450, 430)}

#   Версия объекта
__version__ = (1, 0, 7, 3)
###END SPECIAL BLOCK

class CStdReestrZtrPanel(ictemplate.icTemplateInterface, ifs.icBrowsPanelReestrInterface):
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
        ifs.icBrowsPanelReestrInterface.__init__(self)
        
    def _init_template_resource(self):
        """
        Инициализация ресурса шаблона.
        """
        self._templRes = resource
    
    def _get_panel_interface(self):
        """
        Возвращает указатель на интерфейс панели.
        """
        return self.GetContext().GetInterface('ZtrPanel')
        
    def _get_grid_interface(self):
        """
        Возвращает указатель на интерфейс панели.
        """
        return self.GetContext().GetInterface('ZtrGrid').getRegObj('DataGrid')
        
    def _get_panel_obj(self, name):
        """
        Возвращает указатель на нужный объект панели.
        """
        return self._get_panel_interface().getRegObj(name)
        
    def LoadData(self):
        """
        Загружаем данные на панель.
        """
        #Документ
        obj = self.get_object()
        print('<<<LOAD DATA>>>')
        
        #Грид
        #grid=self._get_panel_obj('ZtrGrid')
        grid=self._get_grid_interface()
        grid.GetDataset().SetSpc(obj.requisites['staty'],['cod','name','summ1','summ2','prim'])
        grid.RefreshGrid()
        
        #НОмер
        edtId = self._get_panel_obj('edtID')
        edtId.SetValue(obj.requisites['doc_no'].getData())
        edtId.Refresh()
        #Описание
        edtName = self._get_panel_obj('edtName')
        edtName.SetValue(obj.requisites['doc_description'].getData())
        edtName.Refresh()
#        #Заголовок
#        edtTitle = self._get_panel_obj('edtTitle')
#        edtTitle.SetValue(obj.requisites['doc_title'].getData())
#        edtTitle.Refresh()
        #Дополнение/Примечание
        edtDescr = self._get_panel_obj('edtDescr')
        edtDescr.SetValue(obj.requisites['doc_note'].getData())
        edtDescr.Refresh()
        #Сумма1
        edtSumma1 = self._get_panel_obj('edtSumma1')
        edtSumma1.SetValue(str(obj.requisites['summ1'].getData()))
        edtSumma1.Refresh()
        #Сумма2
        edtSumma2 = self._get_panel_obj('edtSumma2')
        edtSumma2.SetValue(str(obj.requisites['summ2'].getData()))
        edtSumma2.Refresh()
#        #Месяц
#        edtMonthCod=self._get_panel_obj('monthCodEdt')
#        edtMonthCod.SetValue(str(obj.requisites['month'].getData()['month_cod']))
#        edtMonthCod.Refresh()
#        edtMonthName=self._get_panel_obj('monthNameEdt')
#        edtMonthName.SetValue(str(obj.requisites['month'].getData()['month']))
#        edtMonthName.Refresh()
        
    def SaveData(self):
        """
        Сохраняем данные.
        """
        #Документ
        obj=self.get_object()
        print('<<<SAVE DATA>>>')
        #Номер
        edtId = self._get_panel_obj('edtID')
        obj.requisites['doc_no'].setData(edtId.GetValue())
        #Описание
        edtName = self._get_panel_obj('edtName')
        obj.requisites['doc_description'].setData(edtName.GetValue())
#        #Заголовок
#        edtTitle=self._get_panel_obj('edtTitle')
#        obj.requisites['doc_title'].setData(edtTitle.GetValue())
        #Примечание
        edtDescr=self._get_panel_obj('edtDescr')
        obj.requisites['doc_note'].setData(edtDescr.GetValue())
        #Сумма1
        edtSumma1=self._get_panel_obj('edtSumma1')
        obj.requisites['summ1'].setData(float(edtSumma1.GetValue()))
        #Сумма2
        edtSumma2=self._get_panel_obj('edtSumma2')
        obj.requisites['summ2'].setData(float(edtSumma1.GetValue()))
        
        #
#        edtMonthCod=self._get_panel_obj('monthCodEdt')
#        obj.requisites['month'].setData({'month_cod':str(edtMonthCod.GetValue())})
#        edtMonthName=self._get_panel_obj('monthNameEdt')
#        obj.requisites['month'].setData({'month':str(edtMonthName.GetValue())})
        
        #Сохранить
        #obj.save()
        
    ###BEGIN EVENT BLOCK
    def hlpCodZtr(self, evt):
        """
        Выбор кода статьи затрат.
        """
        obj=self.get_object()
        hlp_result=spravctrl.HlpSprav(obj.requisites['staty'].requisites['cod'].getNSIType(),
            field=obj.requisites['staty'].requisites['cod'].getFields(),
            parentForm=self.parent)

        return hlp_result
        
    def hlpMonthCod(self,evt):
        """
        Выбор кода из справочника.
        """
        obj=self.get_object()
        hlp_result=spravctrl.HlpSprav(obj.requisites['month'].getNSIType(),
            field=obj.requisites['month'].getFields(),
            parentForm=self.parent)

        edtMonthName=self._get_panel_obj('monthNameEdt')
        edtMonthName.SetValue(str(hlp_result[2]['month']))
        edtMonthName.Refresh()
        return hlp_result
    
    def hlpFuncmonth_cod(self, evt):
        """
        Функция обрабатывает событие <?>.
        """
        obj=self.get_object()
        hlp_result=spravctrl.HlpSprav(obj.requisites['staty'].requisites['month2'].getNSIType(),
            field=obj.requisites['staty'].requisites['month2'].getFields(),
            parentForm=self.parent)
           
        return hlp_result
    ###END EVENT BLOCK
    
def test(par=0):
    """
    Тестируем класс CStdReestrZtrPanel.
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