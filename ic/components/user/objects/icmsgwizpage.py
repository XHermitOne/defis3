#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import ic.components.icResourceParser as prs
from ic.utils import util
import ic.interfaces.icobjectinterface as icobjectinterface

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource = {'activate': 1, 'obj_module': None, 'show': 1, 'child': [{'hgap': 0, 'activate': 1, 'obj_module': None, 'minCellWidth': 4, 'child': [{'activate': u'0', 'obj_module': None, 'show': 1, 'borderRightColor': None, 'child': [], 'keyDown': None, 'borderWidth': 1, 'borderTopColor': (0, 98, 196), 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (420, 10), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'description': None, 'shortHelpString': u'', 'backgroundColor2': None, '_uuid': 'a99dfa81e638bb67a397d6bb163f4a56', 'moveAfterInTabOrder': '', 'bgrImage': None, 'flag': 0, 'recount': None, 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'borderStyle': None, 'borderStep': 0, 'borderLeftColor': None, 'name': u'HeadCell_7583_1419', 'borderBottomColor': None, 'refresh': None, 'alias': None, 'init_expr': None, 'position': (3, 1), 'backgroundType': 0, 'onInit': None}, {'hgap': 0, 'activate': u'1', 'obj_module': None, 'minCellWidth': 10, 'child': [{'activate': u'1', 'obj_module': None, 'show': 1, 'text': u'\u041f\u0440\u0438\u043c\u0435\u0440:', 'keyDown': None, 'font': {'style': 'bold', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Arial', 'type': 'Font', 'underline': False, 'size': 8}, 'border': 0, 'size': (-1, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'alias': None, 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', 'res_module': None, 'description': None, '_uuid': '5542d0ca5e2f86850e43e405caa4701f', 'moveAfterInTabOrder': '', 'flag': 2048, 'recount': None, 'name': u'default_1636', 'refresh': None, 'init_expr': None, 'position': (1, 0), 'onInit': None}, {'activate': u'1', 'obj_module': None, 'show': 1, 'borderRightColor': (192, 192, 192), 'recount': None, 'refresh': None, 'borderTopColor': (192, 192, 192), 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': wx.Size(67, 20), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'alias': None, 'component_module': None, 'proportion': 0, 'label': u'', 'source': None, 'backgroundColor': (255, 255, 255), 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': None, 'description': None, 'shortHelpString': u'', 'backgroundColor2': None, '_uuid': '2ce4cde999dca161287b8ae562605797', 'moveAfterInTabOrder': '', 'bgrImage': None, 'flag': 0, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'borderRightColor': (128, 128, 128), 'recount': None, 'refresh': None, 'borderTopColor': (128, 128, 128), 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (14, 14), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': None, 'description': None, 'shortHelpString': u'', 'backgroundColor2': None, '_uuid': '895c129aad9f20ac2a97f1290093194c', 'moveAfterInTabOrder': '', 'bgrImage': None, 'flag': 0, 'child': [], 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': (128, 128, 128), 'name': u'HeadCell_5930', 'borderBottomColor': (128, 128, 128), 'keyDown': None, 'alias': None, 'borderWidth': 1, 'position': (5, 3), 'borderStyle': None, 'onInit': None}], 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': (192, 192, 192), 'name': u'HeadCell_1783', 'borderBottomColor': (192, 192, 192), 'keyDown': None, 'borderWidth': 1, 'position': (2, 3), 'borderStyle': None, 'onInit': None}, {'activate': u'1', 'obj_module': None, 'show': 1, 'borderRightColor': None, 'recount': None, 'refresh': None, 'borderTopColor': (192, 192, 192), 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'border': 0, 'alignment': u"('centred', 'middle')", 'size': (100, 20), 'style': 0, 'foregroundColor': (128, 128, 128), 'span': (1, 1), 'alias': None, 'component_module': None, 'proportion': 0, 'label': u'keyDown', 'source': None, 'backgroundColor': (255, 255, 255), 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': None, 'description': None, 'shortHelpString': u'', 'backgroundColor2': None, '_uuid': '52f45e3c434b8f8412fcd50ed24a5af2', 'moveAfterInTabOrder': '', 'bgrImage': None, 'flag': 8192, 'child': [], 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': (192, 192, 192), 'name': u'HeadCell_3294', 'borderBottomColor': (192, 192, 192), 'keyDown': None, 'borderWidth': 1, 'position': (2, 0), 'borderStyle': None, 'onInit': None}, {'activate': u'1', 'obj_module': None, 'show': 1, 'borderRightColor': None, 'recount': None, 'refresh': None, 'borderTopColor': (192, 192, 192), 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': wx.Size(117, 20), 'style': 0, 'foregroundColor': (128, 128, 128), 'span': (1, 1), 'alias': None, 'component_module': None, 'proportion': 0, 'label': u'wx.EVT_KEY_DOWN', 'source': None, 'backgroundColor': (255, 255, 255), 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': None, 'description': None, 'shortHelpString': u'', 'backgroundColor2': None, '_uuid': '77a3f7d11e15ed7581084630c917b240', 'moveAfterInTabOrder': '', 'bgrImage': None, 'flag': 0, 'child': [], 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': (192, 192, 192), 'name': u'HeadCell_3318', 'borderBottomColor': (192, 192, 192), 'keyDown': None, 'borderWidth': 1, 'position': (2, 1), 'borderStyle': None, 'onInit': None}, {'activate': u'1', 'obj_module': None, 'show': 1, 'borderRightColor': None, 'recount': None, 'refresh': None, 'borderTopColor': (192, 192, 192), 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': wx.Size(110, 20), 'style': 0, 'foregroundColor': (128, 128, 128), 'span': (1, 1), 'alias': None, 'component_module': None, 'proportion': 0, 'label': u'OnKeyDown', 'source': None, 'backgroundColor': (255, 255, 255), 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': None, 'description': None, 'shortHelpString': u'', 'backgroundColor2': None, '_uuid': '4ef595867c7a95df1644943cef245afc', 'moveAfterInTabOrder': '', 'bgrImage': None, 'flag': 8192, 'child': [], 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': (192, 192, 192), 'name': u'HeadCell_3343', 'borderBottomColor': (192, 192, 192), 'keyDown': None, 'borderWidth': 1, 'position': (2, 2), 'borderStyle': None, 'onInit': None}, {'activate': u'1', 'obj_module': None, 'border': 0, 'size': (10, 5), 'style': 0, 'span': (1, 1), 'proportion': 0, 'type': u'SizerSpace', 'res_module': None, 'description': None, '_uuid': '1bbc020cdff1a6e1e3c370961bd30099', 'flag': 0, 'component_module': None, 'name': u'DefaultName_4304', 'alias': None, 'init_expr': None, 'position': (6, 0)}, {'activate': u'1', 'obj_module': None, 'border': 0, 'size': wx.Size(11, 23), 'style': 0, 'span': (1, 1), 'proportion': 0, 'type': u'SizerSpace', 'res_module': None, 'description': None, '_uuid': '16f05ba5c545a234c71a12aaba396dd1', 'flag': 0, 'component_module': None, 'name': u'DefaultName_5060', 'alias': None, 'init_expr': None, 'position': (1, 1)}, {'activate': u'1', 'obj_module': None, 'show': 1, 'text': u'# self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)', 'refresh': None, 'font': {'style': 'boldItalic', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Arial', 'type': 'Font', 'underline': False, 'size': 8}, 'border': 0, 'size': (-1, 18), 'style': 0, 'foregroundColor': (0, 98, 196), 'span': (1, 4), 'alias': u'', 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', 'res_module': None, 'description': None, '_uuid': 'a88d2de021aa2e99babb001ae781260f', 'moveAfterInTabOrder': u'', 'flag': 8192, 'recount': None, 'name': u'default_8704', 'keyDown': None, 'init_expr': u'', 'position': (5, 0), 'onInit': None}, {'activate': u'1', 'obj_module': None, 'show': 1, 'borderRightColor': None, 'recount': None, 'refresh': None, 'borderTopColor': None, 'font': {'style': 'bold', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Arial', 'type': 'Font', 'underline': False, 'size': 8}, 'border': 0, 'alignment': u"('left', 'middle')", 'size': (459, 35), 'style': 0, 'foregroundColor': None, 'span': (1, 4), 'alias': u'None', 'component_module': None, 'proportion': 0, 'label': u'\u0414\u0430\u043d\u043d\u0430\u044f \u0441\u0442\u0440\u043e\u043a\u0430 \u043f\u0440\u0435\u043e\u0431\u0440\u0430\u0437\u0443\u0435\u0442\u0441\u044f (\u0432 \u0442\u0435\u043a\u0441\u0442 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u044b \u0431\u0443\u0434\u0435\u0442 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\r\n\u0441\u043e\u043e\u0442\u0432\u0435\u0442\u0441\u0442\u0432\u0443\u044e\u0449\u0438\u0439 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a): ', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': None, 'description': None, 'shortHelpString': u'', 'backgroundColor2': None, '_uuid': 'b4901114aaf39f9a23e17032376e87e3', 'moveAfterInTabOrder': '', 'bgrImage': None, 'flag': 8192, 'child': [], 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': None, 'name': u'HeadCell_9619', 'borderBottomColor': None, 'keyDown': None, 'borderWidth': 1, 'position': (4, 0), 'borderStyle': None, 'onInit': None}], 'minCellHeight': 5, 'flexCols': [], 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'flexRows': [], 'alias': None, 'border': 0, 'proportion': 0, 'type': u'GridBagSizer', 'res_module': None, 'description': None, '_uuid': 'b817c177863a36c74438941f67b6221e', 'flag': 0, 'component_module': None, 'name': u'DefaultName_1581_1676', 'init_expr': None, 'position': (2, 1), 'vgap': 0}, {'activate': 1, 'obj_module': None, 'show': 1, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'borderRightColor': (100, 100, 100), 'recount': None, 'refresh': None, 'borderTopColor': (250, 250, 250), 'font': {'style': 'bold', 'size': 8, 'underline': False, 'family': 'sansSerif', 'faceName': 'Arial'}, 'border': 0, 'alignment': u"('centred', 'middle')", 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435', 'source': None, 'backgroundColor': (255, 255, 255), 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': None, 'description': None, 'shortHelpString': '', 'backgroundColor2': None, '_uuid': '9dccdc06591e9aa11203d598fac66087', 'moveAfterInTabOrder': '', 'bgrImage': None, 'flag': 0, 'child': [], 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'backgroundType': 2, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'name', 'borderBottomColor': (100, 100, 100), 'keyDown': None, 'alias': u'None', 'borderWidth': 1, 'position': (1, 0), 'borderStyle': None, 'onInit': None}, {'activate': 1, 'obj_module': None, 'show': 1, 'borderRightColor': (100, 100, 100), 'recount': None, 'refresh': None, 'borderTopColor': (250, 250, 250), 'font': {'style': 'bold', 'size': 8, 'underline': False, 'faceName': 'Arial', 'family': 'sansSerif'}, 'border': 0, 'alignment': u"('centred', 'middle')", 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u0422\u0438\u043f \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u044f', 'source': None, 'backgroundColor': (255, 255, 255), 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': None, 'description': None, 'shortHelpString': '', 'backgroundColor2': None, '_uuid': '6d7dfe599915e0bb3a45a9e97a2ef0da', 'moveAfterInTabOrder': '', 'bgrImage': None, 'flag': 0, 'child': [], 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'backgroundType': 2, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'type', 'borderBottomColor': (100, 100, 100), 'keyDown': None, 'alias': None, 'borderWidth': 1, 'position': (1, 1), 'borderStyle': None, 'onInit': None}, {'activate': 1, 'obj_module': None, 'show': 1, 'borderRightColor': (100, 100, 100), 'recount': None, 'refresh': u'None', 'borderTopColor': (250, 250, 250), 'font': {'style': 'bold', 'size': 8, 'underline': False, 'faceName': 'Arial', 'family': 'sansSerif'}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a', 'source': None, 'backgroundColor': (255, 255, 255), 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': None, 'description': None, 'shortHelpString': u'\u0418\u043c\u044f \u0444\u0443\u043d\u043a\u0446\u0438\u0438,\r\n\u043e\u0431\u0440\u0430\u0431\u0430\u0442\u044b\u0432\u0430\u044e\u0449\u0435\u0439\r\n\u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435.', 'backgroundColor2': None, '_uuid': '8e590e7381f5d37402dee9b211b1d1d3', 'moveAfterInTabOrder': '', 'bgrImage': None, 'flag': 0, 'child': [], 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'backgroundType': 2, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'function', 'borderBottomColor': (100, 100, 100), 'keyDown': u'None', 'alias': None, 'borderWidth': 1, 'position': (1, 2), 'borderStyle': None, 'onInit': None}, {'activate': 1, 'obj_module': None, 'show': 1, 'borderRightColor': (100, 100, 100), 'recount': None, 'refresh': None, 'borderTopColor': (250, 250, 250), 'font': {'family': 'sansSerif', 'style': 'bold', 'underline': False, 'faceName': 'Arial', 'size': 8}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (100, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041f\u0440\u0438\u0437\u043d\u0430\u043a', 'source': None, 'backgroundColor': (255, 255, 255), 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': None, 'description': None, 'shortHelpString': u'\u041f\u0440\u0438\u0437\u043d\u0430\u043a \u043a\u043e\u043c\u0430\u043d\u0434\u044b', 'backgroundColor2': None, '_uuid': '226dafd1adb0dbc5de5630794e444c02', 'moveAfterInTabOrder': '', 'bgrImage': None, 'flag': 0, 'child': [], 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'backgroundType': 2, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'przCommand', 'borderBottomColor': (100, 100, 100), 'keyDown': None, 'alias': None, 'borderWidth': 1, 'position': (1, 3), 'borderStyle': None, 'onInit': None}], 'keyDown': None, 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'border': 0, 'alignment': (u'left', u'middle'), 'size': wx.Size(234, 31), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'Head', 'res_module': None, 'description': None, '_uuid': '00afa9f8aa8550d9d85d0131a4eff2d4', 'moveAfterInTabOrder': '', 'flag': 0, 'recount': None, 'name': u'Head', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (4, 1), 'onInit': None}, {'line_color': (200, 200, 200), 'activate': 1, 'obj_module': None, 'show': 1, 'recount': None, 'cols': [{'sort': None, 'pic': u'S', 'attr': None, 'ctrl': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'getvalue': u'', 'keyDown': None, 'label': u'type', 'width': 114, 'init': u'evt*', 'setvalue': u'', 'activate': u'1', 'init_expr': None, 'shortHelpString': u'', 'recount': None, 'show': u'1', 'hlp': u'', 'type': u'GridCell', 'valid': None, 'name': u'name'}, {'sort': u'None', 'activate': u'1', 'obj_module': None, 'ctrl': u'None', 'pic': u'S', 'hlp': u'', 'style': 0, 'alias': None, 'component_module': None, 'show': u'1', 'label': u'name', 'width': 101, 'init': u'wx.EVT_*', 'valid': u'', 'type': u'GridCell', 'res_module': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': '5b5708f9ac2b1c8f06bebd6588d21d33', 'recount': u'None', 'getvalue': u'', 'name': u'type', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'init_expr': None}, {'sort': None, 'pic': u'S', 'attr': u'W', 'ctrl': u'None', 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'getvalue': u'', 'keyDown': None, 'label': u'col', 'width': 146, 'init': u'On*', 'setvalue': u'', 'activate': u'1', 'init_expr': None, 'shortHelpString': u'', 'recount': None, 'show': u'1', 'hlp': None, 'type': u'GridCell', 'valid': None, 'name': u'function'}, {'sort': None, 'pic': u'B', 'attr': None, 'ctrl': None, 'type': u'GridCell', 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'keyDown': None, 'getvalue': u'', 'width': 50, 'init': u'@False', 'setvalue': u'', 'activate': u'1', 'init_expr': u'None', 'shortHelpString': u'', 'recount': None, 'show': u'1', 'label': u'col', 'hlp': None, 'valid': None, 'name': u'przCommand'}], 'onSize': None, 'border': 0, 'post_select': None, 'size': (420, 120), 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), 'delRec': None, 'alias': None, 'row_height': 20, 'selected': None, 'proportion': 1, 'init': None, 'label': u'Grid', 'source': u'', 'backgroundColor': None, 'fixRowSize': 0, 'type': u'GridDataset', 'res_module': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'fixColSize': 0, 'description': None, 'getattr': None, 'post_del': None, 'post_init': None, '_uuid': '12562fa70266128c77b48008397147ce', 'style': 0, 'docstr': 'ic.components.icgrid.html', 'flag': 0, 'dclickEditor': None, 'component_module': None, 'label_attr': {'foregroundColor': (255, 255, 255), 'name': '', '_uuid': None, 'backgroundColor': (100, 100, 100), 'font': {'style': None, 'name': 'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'label_attr', 'alignment': ('left', 'middle')}, 'name': u'MsgGrid', 'label_height': 20, 'changed': None, 'keyDown': None, 'init_expr': u'GetInterface().MsgGrid_init_expr(self, evt)', 'position': (5, 1), 'onInit': None, 'refresh': None}, {'activate': u'1', 'obj_module': None, 'show': 1, 'borderRightColor': None, 'recount': None, 'keyDown': u'None', 'borderTopColor': None, 'font': {'style': 'boldItalic', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Arial', 'type': 'Font', 'underline': False, 'size': 12}, 'border': 2, 'alignment': u"('left', 'middle')", 'size': (420, 30), 'style': 0, 'foregroundColor': (0, 98, 196), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u' \u0410\u0442\u0440\u0438\u0431\u0443\u0442\u044b \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0439', 'source': u'None', 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': u'None', 'description': None, 'shortHelpString': u'', 'backgroundColor2': None, '_uuid': '6a135268bf7e66ad11509a80ebea85a2', 'moveAfterInTabOrder': '', 'bgrImage': None, 'flag': 0, 'child': [], 'onLeftDown': None, 'cursorColor': None, 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': None, 'name': u'HeadCell_1250', 'borderBottomColor': (0, 98, 196), 'refresh': None, 'alias': u'None', 'borderWidth': 1, 'position': (0, 1), 'borderStyle': None, 'onInit': None}, {'activate': u'0', 'obj_module': None, 'show': 1, 'borderRightColor': None, 'recount': None, 'refresh': None, 'borderTopColor': None, 'font': {'style': 'bold', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Arial', 'type': 'Font', 'underline': False, 'size': 8}, 'border': 2, 'alignment': u"('left', 'middle')", 'size': (420, 50), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'', 'source': u'None', 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': u'None', 'description': None, 'shortHelpString': '', 'backgroundColor2': None, '_uuid': '882d4dbe849924fcba370d2242f14ee4', 'moveAfterInTabOrder': '', 'bgrImage': None, 'flag': 0, 'child': [], 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': None, 'name': u'HeadCell_1250_1586', 'borderBottomColor': (0, 98, 196), 'keyDown': u'None', 'alias': u'None', 'borderWidth': 1, 'position': (2, 1), 'borderStyle': None, 'onInit': None}, {'activate': u'1', 'obj_module': None, 'border': 0, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'type': u'BoxSizer', 'res_module': None, 'hgap': 0, 'description': None, '_uuid': '93da14d8e4d48e37b7d0a6be8ebc6332', 'flag': 0, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'borderRightColor': (100, 100, 100), 'recount': None, 'refresh': None, 'borderTopColor': (192, 192, 192), 'font': {'style': 'boldItalic', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Times New Roman', 'type': 'Font', 'underline': False, 'size': 10}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (40, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'alias': None, 'component_module': None, 'proportion': 0, 'label': u'DEL', 'source': u'None', 'backgroundColor': (255, 255, 255), 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': None, 'description': None, 'shortHelpString': '', 'backgroundColor2': None, '_uuid': '9dfca4609e02e9421b23f8fd1bb6f52c', 'moveAfterInTabOrder': '', 'bgrImage': None, 'flag': 0, 'child': [], 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'backgroundType': 2, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'HeadCell_2965', 'borderBottomColor': (100, 100, 100), 'keyDown': u'None', 'borderWidth': 1, 'position': wx.Point(4, 279), 'borderStyle': None, 'onInit': None}, {'activate': 1, 'show': 1, 'text': u'  \u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0430\u0442\u0440\u0438\u0431\u0443\u0442', 'keyDown': None, 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'border': 0, 'size': (100, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', 'flag': 2048, 'recount': None, 'name': u'default_2979', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(44, 280)}, {'activate': 1, 'obj_module': None, 'show': 1, 'borderRightColor': (100, 100, 100), 'child': [], 'keyDown': u'None', 'borderTopColor': (192, 192, 192), 'font': {'style': 'boldItalic', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Times New Roman', 'type': 'Font', 'underline': False, 'size': 10}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (40, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'alias': None, 'component_module': None, 'proportion': 0, 'label': u'INS', 'source': u'None', 'backgroundColor': (255, 255, 255), 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': None, 'description': None, 'shortHelpString': '', 'backgroundColor2': None, '_uuid': '5060b2d85e30f5bef5a94739a99f2ee8', 'moveAfterInTabOrder': '', 'bgrImage': None, 'flag': 0, 'recount': None, 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'backgroundType': 2, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'HeadCell_2965_3902', 'borderBottomColor': (100, 100, 100), 'refresh': None, 'borderWidth': 1, 'position': wx.Point(144, 279), 'borderStyle': None, 'onInit': None}, {'activate': 1, 'obj_module': None, 'show': 1, 'text': u'  \u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c', 'keyDown': None, 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'border': 0, 'size': (100, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', 'res_module': None, 'description': None, '_uuid': '6740fee6c7f9cd2196107c0cfa43f124', 'moveAfterInTabOrder': '', 'flag': 2048, 'recount': None, 'name': u'default_2979_4431', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(44, 280), 'onInit': None}, {'activate': 1, 'obj_module': None, 'show': 1, 'borderRightColor': (100, 100, 100), 'child': [], 'keyDown': u'None', 'borderTopColor': (192, 192, 192), 'font': {'style': 'boldItalic', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Times New Roman', 'type': 'Font', 'underline': False, 'size': 10}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (40, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'alias': None, 'component_module': None, 'proportion': 0, 'label': u'ESC', 'source': u'None', 'backgroundColor': (255, 255, 255), 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': None, 'description': None, 'shortHelpString': '', 'backgroundColor2': None, '_uuid': 'a5fd9549d4245539c741c00a519e6693', 'moveAfterInTabOrder': '', 'bgrImage': None, 'flag': 0, 'recount': None, 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'backgroundType': 2, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'HeadCell_2965_4729', 'borderBottomColor': (100, 100, 100), 'refresh': None, 'borderWidth': 1, 'position': wx.Point(284, 279), 'borderStyle': None, 'onInit': None}, {'activate': 1, 'show': 1, 'text': u'  \u041e\u0442\u043c\u0435\u043d\u0430 \u0432\u0432\u043e\u0434\u0430', 'keyDown': None, 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'border': 0, 'size': (100, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', 'flag': 2048, 'recount': None, 'name': u'default_2979_4936', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(324, 391)}], 'layout': u'horizontal', 'name': u'DefaultName_2924', 'alias': None, 'init_expr': None, 'position': (6, 1), 'vgap': 0}], 'minCellHeight': 5, 'border': 0, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'flexRows': [], 'alias': None, 'flexCols': [], 'proportion': 1, 'type': u'GridBagSizer', 'res_module': None, 'description': None, '_uuid': u'89978ff8dba85769d78c9e07225d5068', 'flag': 8192, 'component_module': None, 'name': u'MsgGridBS_2051', 'init_expr': u'', 'position': wx.Point(158, 63), 'vgap': 0}], 'keyDown': u"import wx\r\ncd = evt.m_keyCode\r\nprint '!!!@ >>> KeyDown key=', cd\r\nif cd == 27:\r\n    _root_obj.Close()\r\n\r\n", 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': '', 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'res_module': None, 'description': None, 'onClose': u'None', '_uuid': u'a24751f5fb4f14844a1d4a0cf8291ed8', 'style': 524288, 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 0, 'recount': None, 'name': u'defaultWindow_1855', 'refresh': None, 'alias': None, 'init_expr': u'None', 'position': (-1, -1), 'onInit': None}

#   Версия объекта
__version__ = (1, 0, 1, 7)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'icInputMsgAttrClass'


class icInputMsgAttrClass(icobjectinterface.icObjectInterface):
    """
    Страница описания обрабатываемых сообщений.
    """
    def __init__(self, parent):
        if hasattr(parent, 'type'):
            res = resource
        else:
            res = resource['child'][0]
            
        icobjectinterface.icObjectInterface.__init__(self, parent, res)

    def MsgGrid_init_expr(self, obj, evt):
        """
        Инициализация грида.
        """
        header = self.GetNameObj('Head')
        # Привязываем шапку к гриду
        obj.SetHeader(header, False, True)
        obj.ReconstructHeader()


def test(par=0):
    """
    Тестируем класс icInputMsgAttrClass.
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
