#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import ic.components.icResourceParser as prs
from ic.utils import util
import ic.interfaces.icobjectinterface as icobjectinterface

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource = {'activate': u'1', 'show': 1, 'recount': None, 'keyDown': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'c78e598d0ba7bf4765411427b5b8fe1f', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'hgap': 0, 'activate': 1, 'obj_module': None, 'minCellWidth': 4, 'minCellHeight': 5, 'flexCols': [], 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'flexRows': [], 'alias': None, 'component_module': None, 'border': 0, 'proportion': 0, 'type': u'GridBagSizer', 'res_module': None, 'description': None, '_uuid': '3f68881abc5207e9b79ff0e9e30d29d1', 'flag': 0, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'borderRightColor': (100, 100, 100), 'child': [], 'refresh': None, 'borderWidth': 1, 'borderTopColor': (250, 250, 250), 'font': {'style': 'bold', 'size': 8, 'underline': False, 'family': 'sansSerif', 'faceName': 'Arial'}, 'border': 0, 'alignment': u"('centred', 'middle')", 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'alias': u'None', 'component_module': None, 'proportion': 0, 'label': u'\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435', 'source': None, 'backgroundColor': (255, 255, 255), 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'description': None, 'shortHelpString': u'', 'backgroundColor2': None, '_uuid': u'41ebc9860273d4cc59987360320f7efa', 'moveAfterInTabOrder': u'', 'bgrImage': None, 'flag': 0, 'recount': None, 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'borderStyle': None, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'name', 'borderBottomColor': (100, 100, 100), 'keyDown': None, 'init_expr': None, 'position': (0, 0), 'backgroundType': 2, 'onInit': None}, {'activate': 1, 'obj_module': None, 'show': 1, 'borderRightColor': (100, 100, 100), 'child': [], 'refresh': u'None', 'borderTopColor': (250, 250, 250), 'font': {'style': 'bold', 'size': 8, 'underline': False, 'faceName': 'Arial', 'family': 'sansSerif'}, 'border': 0, 'alignment': u"('centred', 'middle')", 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u0422\u0438\u043f', 'source': None, 'backgroundColor': (255, 255, 255), 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': None, 'description': None, 'shortHelpString': u' \u0422\u0438\u043f \u0440\u0435\u0434\u0430\u043a\u0442\u043e\u0440\u0430, \u043a\u043e\u0442\u0440\u043e\u0440\u044b\u0439\r\n \u0431\u0443\u0434\u0435\u0442 \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u044c\u0441\u044f \u0432 \r\n \u0440\u0435\u0434\u0430\u043a\u0442\u043e\u0440\u0435 \u0444\u043e\u0440\u043c \u0434\u043b\u044f \u0440\u0435\u0434\u0430\u043a\u0442\u0438-\r\n \u0440\u043e\u0432\u0430\u043d\u0438\u044f \u0430\u0442\u0440\u0438\u0431\u0443\u0442\u0430.\r\n', 'backgroundColor2': None, '_uuid': '83cdd2182e0ea6e674c6ddeaa6bd2374', 'moveAfterInTabOrder': '', 'bgrImage': None, 'flag': 0, 'alias': None, 'recount': None, 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'backgroundType': 2, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'type', 'borderBottomColor': (100, 100, 100), 'keyDown': None, 'borderWidth': 1, 'position': (0, 1), 'borderStyle': None, 'onInit': None}, {'activate': 1, 'obj_module': None, 'show': 1, 'borderRightColor': (100, 100, 100), 'recount': None, 'refresh': None, 'borderTopColor': (250, 250, 250), 'font': {'style': 'bold', 'size': 8, 'underline': False, 'faceName': 'Arial', 'family': 'sansSerif'}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435 \u043f\u043e \u0443\u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044e', 'source': None, 'backgroundColor': (255, 255, 255), 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': None, 'description': None, 'shortHelpString': '', 'backgroundColor2': None, '_uuid': '7b2426afbf1ffbfc3dc28eb743227462', 'moveAfterInTabOrder': '', 'bgrImage': None, 'flag': 0, 'alias': None, 'child': [], 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'backgroundType': 2, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'defaultVal', 'borderBottomColor': (100, 100, 100), 'keyDown': u'None', 'borderWidth': 1, 'position': (0, 2), 'borderStyle': None, 'onInit': None}, {'activate': 0, 'obj_module': None, 'show': 1, 'borderRightColor': (100, 100, 100), 'recount': None, 'refresh': None, 'borderTopColor': (250, 250, 250), 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (100, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': None, 'description': None, 'shortHelpString': '', 'backgroundColor2': None, '_uuid': '56ad67fcca8199acfbe8cd3bfd1b9946', 'moveAfterInTabOrder': '', 'bgrImage': None, 'flag': 0, 'alias': None, 'child': [], 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'backgroundType': 2, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'HeadCell_1383', 'borderBottomColor': (100, 100, 100), 'keyDown': None, 'borderWidth': 1, 'position': (0, 3), 'borderStyle': None, 'onInit': None}], 'keyDown': None, 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'border': 0, 'alignment': (u'left', u'middle'), 'size': (450, 31), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'alias': None, 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'Head', 'res_module': None, 'description': None, '_uuid': u'8d7a8e217d6aaabe45230ac31cea59cc', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'Head', 'refresh': None, 'init_expr': None, 'position': (3, 1), 'onInit': None}, {'line_color': (200, 200, 200), 'activate': u'1', 'obj_module': None, 'show': u'1', 'init_expr': u"header = _dict_obj['Head']\r\nself.SetHeader(header, False, True)\r\nself.ReconstructHeader()", 'cols': [{'sort': None, 'activate': u'1', 'obj_module': None, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'alias': None, 'component_module': None, 'show': u'1', 'label': u'type', 'width': 156, 'init': u'attr*', 'valid': None, 'type': u'GridCell', 'res_module': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': 'bb55e754f541c10709227e29b4b6f95c', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'name', 'keyDown': None, 'init_expr': None}, {'sort': u'None', 'activate': u'1', 'obj_module': None, 'ctrl': u"self.GetView().setNameValue('defaultVal', '')\r\n_resultEval = 0\r\n", 'pic': u'CH', 'hlp': u'None', 'style': 0, 'component_module': None, 'show': u'1', 'label': u'name', 'width': 142, 'init': u'EDT_TEXTFIELD', 'valid': u'EDT_TEXTFIELD,EDT_NUMBER,EDT_PY_SCRIPT,EDT_COLOR,EDT_FONT,EDT_POINT,EDT_SIZE,EDT_CHOICE,EDT_CHECK_BOX,EDT_TEXTLIST,EDT_TEXTDICT,EDT_DICT,EDT_COMBINE', 'type': u'GridCell', 'res_module': None, '_uuid': u'81c2e33e8942f844e48221da6c13ead6', 'description': None, 'shortHelpString': u'', 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '_uuid': None, 'activate': '1', 'init_expr': None, 'backgroundColor': (255, 255, 255), 'font': {'style': 'bold', 'name': 'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'alias': u'None', 'recount': u'None', 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'type', 'keyDown': None, 'init_expr': u'None'}, {'sort': None, 'pic': u'S', 'attr': u'W', 'ctrl': u"# \u0414\u0435\u043b\u0430\u0435\u043c \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0443 \u0442\u0438\u043f\u0430\r\nimport wx\r\nimport ic.dlg.msgbox as msgbox\r\nimport ic.utils.coderror as coderror\r\n\r\n_val = value\r\ntyp = self.GetView().getNameValue('type')\r\n_resultEval = coderror.IC_CTRL_OK\r\n\r\nprint 'type =', typ\r\nbTypeError = False\r\nbInputError = False\r\n\r\nif typ == 'EDT_COLOR':\r\n    try:\r\n        ret = eval(_val)\r\n            \r\n        if ret <> None and type(ret) <> type(wx.Colour(0,0,0)) and type(ret) <> type((0,0)) or (type(ret) == type((0,0)) and len(ret) <> 3 ):\r\n            bTypeError = True\r\n    except:\r\n        bInputError = True\r\n\r\nelif typ == 'EDT_SIZE':\r\n    try:\r\n        ret = eval(_val)\r\n        \r\n        if ret <> None and type(ret) <> type(wx.Size(0,0)) and type(ret) <> type((0,0)) or (type(ret) == type((0,0)) and len(ret) <> 2 ):    \r\n            bTypeError = True\r\n    except:\r\n        bInputError = True\r\n\r\nelif typ == 'EDT_POINT':\r\n    try:\r\n        ret = eval(_val)\r\n        \r\n        if ret <> None and type(ret) <> type(wx.Point(0,0)) and type(ret) <> type((0,0)) or (type(ret) == type((0,0)) and len(ret) <> 2 ):    \r\n            bTypeError = True\r\n    except:\r\n        bInputError = True\r\n\r\nelif typ == 'EDT_FONT':\r\n    try:\r\n        ret = eval(_val)\r\n        \r\n        if type(ret) <> type({}):\r\n            bTypeError = True\r\n    except:\r\n        bInputError = True\r\n\r\nelif typ == 'EDT_NUMBER':\r\n    try:\r\n        ret = eval(_val)\r\n        \r\n        if type(ret) <> type(0) and type(ret) <> type(100.123):\r\n            bTypeError = True\r\n    except:\r\n        bInputError = True\r\n\r\nif _val:\r\n    if bTypeError:\r\n        msgbox.MsgBox(self.GetView(), '\u041d\u0435\u0441\u043e\u043e\u0442\u0432\u0435\u0442\u0441\u0442\u0432\u0438\u0435 \u0442\u0438\u043f\u0430 :' + str(_val))\r\n        _resultEval = coderror.IC_CTRL_FAILED_IGNORE\r\n\r\n    if bInputError:\r\n        msgbox.MsgBox(self.GetView(), '\u041e\u0448\u0438\u0431\u043a\u0430 \u0432\u0432\u043e\u0434\u0430:' + str(_val))\r\n        _resultEval = coderror.IC_CTRL_FAILED_IGNORE\r\n", 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'getvalue': u'', 'keyDown': u'None', 'label': u'col', 'width': 159, 'init': u'@u""', 'setvalue': u'', 'activate': u'1', 'init_expr': None, 'shortHelpString': u'', 'recount': None, 'show': u'1', 'hlp': u"# \u0412 \u0437\u0430\u043f\u0438\u0441\u0438\u043c\u043e\u0441\u0442\u0438 \u043e\u0442 \u0442\u0438\u043f\u0430 \u0432\u044b\u0437\u044b\u0432\u0430\u0435\u043c \u043d\u0443\u0436\u043d\u044b\u0439 \u0440\u0435\u0434\u0430\u043a\u0442\u043e\u0440\r\nimport wx\r\nfrom ic.components import icfont\r\n\r\ntyp = self.getNameValue('type')\r\n_val = self.getNameValue('defaultVal')\r\n\r\nprint 'type =', typ, _val\r\n\r\n##  All posible types:\r\n##  EDT_TEXTFIELD,EDT_NUMBER,EDT_PY_SCRIPT,EDT_COLOR,EDT_FONT,\r\n##  EDT_POINT,EDT_SIZE,EDT_CHOICE,EDT_CHECK_BOX,EDT_TEXTLIST,\r\n##  EDT_TEXTDICT,EDT_DICT,EDT_EXTERNAL,EDT_COMBINE,EDT_ADD_PROPERTY,EDT_NEW_PROPERTY\r\n\r\nif typ == 'EDT_COLOR':\r\n    dlg = wx.ColourDialog(self.parent)\r\n    dlg.GetColourData().SetChooseFull(True)\r\n\r\n    if _val:\r\n        clr = eval(_val)\r\n    else:\r\n        clr = None\r\n\r\n    if clr <> None:\r\n        dlg.GetColourData().SetColour(clr)\r\n    else:\r\n        dlg.GetColourData().SetColour(wx.Colour(0,0,0))\r\n            \r\n    if dlg.ShowModal() == wx.ID_OK:\r\n        data = dlg.GetColourData()\r\n        clr = data.GetColour()#.Get()\r\n        _resultEval = 'wx.Colour(%d, %d, %d)' % (clr.Red(), clr.Green(), clr.Blue())\r\n        \r\n    dlg.Destroy()\r\n\r\nelif typ == 'EDT_SIZE':\r\n    _resultEval = 'wx.Size(-1,-1)'\r\n\r\nelif typ == 'EDT_POINT':\r\n    _resultEval = 'wx.Point(-1,-1)'\r\n\r\nelif typ == 'EDT_FONT':\r\n    newval = {}\r\n\r\n    try:\r\n        data = wx.FontData()\r\n        data.EnableEffects(True)\r\n\r\n        if _val:\r\n            curFont = icfont.icFont(eval(_val))\r\n        else:\r\n            curFont = icfont.icFont({})\r\n\r\n        data.SetInitialFont(curFont)\r\n    \r\n        dlg = wx.FontDialog(self.GetView(), data)\r\n    \r\n        if dlg.ShowModal() == wx.ID_OK:\r\n            data = dlg.GetFontData()\r\n            font = data.GetChosenFont()\r\n        \r\n            newval['size'] = font.GetPointSize()\r\n            newval['family'] = icfont.getICFamily(font)\r\n            newval['style'] = icfont.getICFontStyle(font)\r\n            newval['faceName'] = font.GetFaceName()\r\n            newval['underline'] = font.GetUnderlined()\r\n            _resultEval = str(newval)\r\n\r\n        dlg.Destroy()\r\n    except:\r\n        pass\r\n\r\nelif typ == 'EDT_NUMBER':\r\n    _resultEval = '0.0'\r\n\r\nelif typ == 'EDT_CHECK_BOX':\r\n    _resultEval = 'False'\r\n\r\nelif typ in ('EDT_CHOICE', 'EDT_TEXTLIST'):\r\n    _resultEval = '[]'\r\n\r\nelif typ in ('EDT_DICT', 'EDT_COMBINE', 'EDT_TEXTDICT'):\r\n    _resultEval = '{}'\r\n", 'type': u'GridCell', 'valid': None, 'name': u'defaultVal'}], 'keyDown': None, 'border': 0, 'post_select': u'None', 'size': (455, 200), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'delRec': u'None', 'row_height': 20, 'selected': u'None', 'proportion': 1, 'getattr': u'None', 'label': u'Grid', 'source': u'', 'backgroundColor': None, 'fixRowSize': 0, 'type': u'GridDataset', 'res_module': None, '_uuid': u'acbaaf673cef7648d198bbdbf24798a4', 'fixColSize': 0, 'description': None, 'post_del': u'None', 'post_init': u'None', 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'style': 0, 'docstr': 'ic.components.icgrid.html', 'flag': 0, 'dclickEditor': None, 'recount': u'None', 'label_attr': {'foregroundColor': (255, 255, 255), 'name': '', '_uuid': None, 'backgroundColor': (100, 100, 100), 'font': {'style': None, 'name': 'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'label_attr', 'alignment': ('left', 'middle')}, 'init': u'None', 'name': u'AttrGrid', 'label_height': 20, 'changed': u'None', 'onSize': None, 'alias': u'None', 'component_module': None, 'position': (4, 1), 'onInit': None, 'refresh': u'None'}, {'activate': 1, 'obj_module': None, 'show': 1, 'borderRightColor': None, 'recount': None, 'keyDown': u'None', 'borderTopColor': None, 'font': {'style': 'boldItalic', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Arial', 'type': 'Font', 'underline': False, 'size': 12}, 'border': 2, 'alignment': u"('left', 'middle')", 'size': (450, 30), 'style': 0, 'foregroundColor': (0, 98, 196), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u' \u0410\u0442\u0440\u0438\u0431\u0443\u0442\u044b \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c\u0441\u043a\u043e\u0433\u043e \u043a\u043b\u0430\u0441\u0441\u0430', 'source': u'None', 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': u'None', 'description': None, 'shortHelpString': u'', 'backgroundColor2': None, '_uuid': 'ed797fdf02013c248f5922f21e75701f', 'moveAfterInTabOrder': '', 'bgrImage': None, 'flag': 0, 'alias': u'None', 'child': [], 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': None, 'name': u'HeadCell_1250', 'borderBottomColor': (0, 98, 196), 'refresh': None, 'borderWidth': 1, 'position': (0, 1), 'borderStyle': None, 'onInit': None}, {'activate': 1, 'show': 1, 'borderRightColor': None, 'child': [], 'refresh': None, 'borderTopColor': None, 'font': {'style': 'bold', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Arial', 'type': 'Font', 'underline': False, 'size': 8}, 'border': 2, 'alignment': u"('left', 'middle')", 'size': (450, 40), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'proportion': 0, 'label': u'\u041d\u0430 \u0434\u0430\u043d\u043d\u043e\u0439 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0435 \u043e\u043f\u0440\u0435\u0434\u0435\u043b\u044f\u044e\u0442\u0441\u044f \u0430\u0442\u0440\u0438\u0431\u0443\u0442\u044b \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c\u0441\u043a\u043e\u0433\u043e\r\n\u043a\u043b\u0430\u0441\u0441\u0430 (\u0438\u043c\u044f, \u0442\u0438\u043f \u0438 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435 \u043f\u043e \u0443\u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044e).', 'source': u'None', 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'shortHelpString': u'', 'flag': 0, 'recount': None, 'borderStep': 0, 'borderLeftColor': None, 'name': u'HeadCell_1250_1586', 'borderBottomColor': (0, 98, 196), 'keyDown': u'None', 'alias': u'None', 'init_expr': u'None', 'position': (1, 1), 'backgroundType': 0}, {'activate': 1, 'show': 1, 'refresh': [], 'border': 0, 'check': None, 'size': (-1, -1), 'uncheck': None, 'style': 33554432, 'foregroundColor': None, 'checked': 0, 'proportion': 0, 'label': u'\u041f\u0440\u0438\u0437\u043d\u0430\u043a \u043a\u043e\u0442\u043d\u0435\u0439\u043d\u0435\u0440\u0430', 'source': None, 'init': None, 'backgroundColor': None, 'type': u'CheckBox', 'loseFocus': None, 'flag': 0, 'recount': [], 'span': (1, 1), 'field_name': None, 'name': u'przContainer', 'setFocus': None, 'attr': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (9, 1)}, {'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'horizontal', 'name': u'DefaultName_2924', 'border': 0, 'span': (1, 1), 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'borderRightColor': (100, 100, 100), 'recount': None, 'refresh': None, 'borderTopColor': (250, 250, 250), 'font': {'style': 'boldItalic', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Times New Roman', 'type': 'Font', 'underline': False, 'size': 10}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (40, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'DEL', 'source': u'None', 'backgroundColor': (255, 255, 255), 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': None, 'description': None, 'shortHelpString': '', 'backgroundColor2': None, '_uuid': '934124d845411f7094cab3a2de203f83', 'moveAfterInTabOrder': '', 'bgrImage': None, 'flag': 0, 'alias': None, 'child': [], 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'backgroundType': 2, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'HeadCell_2965', 'borderBottomColor': (100, 100, 100), 'keyDown': u'None', 'borderWidth': 1, 'position': wx.Point(4, 279), 'borderStyle': None, 'onInit': None}, {'activate': 1, 'obj_module': None, 'show': 1, 'text': u'  \u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0430\u0442\u0440\u0438\u0431\u0443\u0442', 'keyDown': None, 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'border': 0, 'size': (100, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', 'res_module': None, 'description': None, '_uuid': 'bb64e5c8fd7bba35322150247f2975e1', 'moveAfterInTabOrder': '', 'flag': 2048, 'alias': None, 'recount': None, 'name': u'default_2979', 'refresh': None, 'init_expr': None, 'position': wx.Point(44, 280), 'onInit': None}, {'activate': 1, 'obj_module': None, 'show': 1, 'borderRightColor': (100, 100, 100), 'child': [], 'keyDown': u'None', 'borderTopColor': (250, 250, 250), 'font': {'style': 'boldItalic', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Times New Roman', 'type': 'Font', 'underline': False, 'size': 10}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (40, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'INS', 'source': u'None', 'backgroundColor': (255, 255, 255), 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': None, 'description': None, 'shortHelpString': '', 'backgroundColor2': None, '_uuid': '25af315096176805d48acb27880593a6', 'moveAfterInTabOrder': '', 'bgrImage': None, 'flag': 0, 'alias': None, 'recount': None, 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'backgroundType': 2, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'HeadCell_2965_3902', 'borderBottomColor': (100, 100, 100), 'refresh': None, 'borderWidth': 1, 'position': wx.Point(144, 279), 'borderStyle': None, 'onInit': None}, {'activate': 1, 'obj_module': None, 'show': 1, 'text': u'  \u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c', 'keyDown': None, 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'border': 0, 'size': (100, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', 'res_module': None, 'description': None, '_uuid': 'e40143882f70757131fcf3e4d9e6fa3c', 'moveAfterInTabOrder': '', 'flag': 2048, 'alias': None, 'recount': None, 'name': u'default_2979_4431', 'refresh': None, 'init_expr': None, 'position': wx.Point(44, 280), 'onInit': None}, {'activate': 1, 'obj_module': None, 'show': 1, 'borderRightColor': (100, 100, 100), 'child': [], 'keyDown': u'None', 'borderTopColor': (250, 250, 250), 'font': {'style': 'boldItalic', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Times New Roman', 'type': 'Font', 'underline': False, 'size': 10}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (40, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'ESC', 'source': u'None', 'backgroundColor': (255, 255, 255), 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': None, 'description': None, 'shortHelpString': '', 'backgroundColor2': None, '_uuid': 'b9fefe3124b1af43d923065ee0de3a3b', 'moveAfterInTabOrder': '', 'bgrImage': None, 'flag': 0, 'alias': None, 'recount': None, 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'backgroundType': 2, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'HeadCell_2965_4729', 'borderBottomColor': (100, 100, 100), 'refresh': None, 'borderWidth': 1, 'position': wx.Point(284, 279), 'borderStyle': None, 'onInit': None}, {'activate': 1, 'show': 1, 'text': u'  \u041e\u0442\u043c\u0435\u043d\u0430 \u0432\u0432\u043e\u0434\u0430', 'keyDown': None, 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'border': 0, 'size': (100, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', 'flag': 2048, 'recount': None, 'name': u'default_2979_4936', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(324, 280)}], 'position': (5, 1), 'type': u'BoxSizer', 'vgap': 0, 'size': (-1, -1)}], 'name': u'DefaultName_1588_1417', 'init_expr': u"_dict_obj['AttrGrid'].ReconstructHeader()", 'position': wx.Point(158, 63), 'vgap': 0}], 'name': u'defaultWindow_1221', 'refresh': None, 'alias': u'None', 'init_expr': u'None', 'position': (-1, -1), 'onInit': None}

#   Версия объекта
__version__ = (1, 0, 1, 7)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'icInputAttrClass'


class icInputAttrClass(icobjectinterface.icObjectInterface):
    def __init__(self, parent):

        #   Вызываем конструктор базового класса
        self.res = resource['child'][0]
        icobjectinterface.icObjectInterface.__init__(self, parent, self.res)


def test(par=0):
    """
    Тестируем класс icInputAttrClass.
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
