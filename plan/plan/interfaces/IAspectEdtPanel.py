#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
import plan.interfaces.ieditpanel as ieditpanel
#import NSI.spravfunc as spravfunc
from NSI import spravctrl

import ic.utils.coderror as coderror
import ic.dlg.msgbox as msgbox
import time
from ic.kernel import io_prnt

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'show': 1, 'recount': None, 'keyDown': None, 'border': 0, 'size': (-1, 400), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'res_module': None, 'description': None, 'onClose': None, '_uuid': u'195b78e0f6d4c7b8c73878476c1ccc8d', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'description': None, 'position': (0, 0), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'cee699b6e30fabcb333ac365797d72fc', 'proportion': 0, 'name': u'BSZ', 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'recount': u'', 'keyDown': None, 'border': 0, 'size': (-1, 400), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': (248, 248, 239), 'type': u'Panel', 'res_module': None, 'description': None, 'onClose': None, '_uuid': u'e6ba1f93b688647521a39bf35ea29dc3', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'child': [{'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncedtId(value, evt)', 'pic': u'S', 'getvalue': None, 'value': u'', 'font': {}, 'border': 0, 'size': (80, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'res_module': None, 'description': None, '_uuid': u'd55e1e8aff07854072bf72c6b32804d8', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': [], 'hlp': u'WrapperObj.hlpFuncedtId(evt)', 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'edtId', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(105, 10), 'onInit': None, 'refresh': []}, {'activate': 1, 'show': 1, 'borderRightColor': (167, 166, 152), 'child': [], 'refresh': None, 'borderWidth': 1, 'borderTopColor': (167, 166, 152), 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (18, 18), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'...', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'description': None, 'shortHelpString': u'\u041f\u043e\u043c\u043e\u0449\u044c', 'backgroundColor2': None, '_uuid': u'd2166ef02484cc46fedaf11ede24d3c4', 'style': 0, 'bgrImage': None, 'flag': 0, 'recount': None, 'onLeftDown': u"res = GetInterface().hlpFuncedtId(evt)\r\nctrl = GetInterface().GetNameObj('edtId')\r\n\r\nif res[1]:\r\n    if ctrl.SetValueCtrl(res[1]):\r\n        ctrl.SetFocus()\r\n    else:\r\n        descr = GetInterface().GetNameObj('edtDescription')\r\n        print '==== DESCR=', descr, descr._oldValue\r\n        descr.Restore()", 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': None, 'name': u'edtIdHlp', 'borderBottomColor': (167, 166, 152), 'keyDown': None, 'alias': None, 'init_expr': u'#self.SetRoundCorners((1,1,1,1))\r\nself.SetButtonStyle()', 'position': (185, 10), 'borderStyle': None, 'onInit': None}, {'activate': 1, 'show': 1, 'text': u'\u0421\u0443\u043c\u043c\u0430 (\u0442\u044b\u0441. \u0440\u0443\u0431.)', 'keyDown': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'6d1e34966faad788a569880e3523c5e7', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_2145', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(10, 40), 'onInit': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': None, 'value': u'', 'font': {}, 'border': 0, 'size': wx.Size(373, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': u'', 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'res_module': None, 'description': None, '_uuid': u'141bbf55fe06cd6579b102e122aeb048', 'moveAfterInTabOrder': u'edtId', 'flag': 0, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'edtDescription', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(315, 10), 'onInit': None, 'refresh': []}, {'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncEdtSumma(value, evt)', 'pic': u'999,999,999.99', 'hlp': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': (-1, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'res_module': None, 'description': None, '_uuid': u'1351eba365d17ea4600c32cf03b061f8', 'moveAfterInTabOrder': u'edtDescription', 'flag': 0, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': u'', 'name': u'edtSumma', 'changed': None, 'value': u'0', 'alias': None, 'init_expr': None, 'position': wx.Point(105, 40), 'onInit': None, 'refresh': []}, {'activate': 1, 'show': 1, 'text': u'\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043f\u043b\u0430\u043d\u0430', 'keyDown': None, 'font': {}, 'border': 0, 'size': wx.Size(82, 13), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'faeb3cbc89d3de592e19618078e28739', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_1221', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(225, 10), 'onInit': None}, {'activate': 1, 'show': 1, 'text': u'\u0418\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440', 'keyDown': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', 'description': None, '_uuid': u'efff0de03f88df3e9e34d53c3bfd64ce', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_1107', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(10, 10), 'onInit': None}, {'activate': 1, 'show': 1, 'borderRightColor': (167, 166, 152), 'recount': None, 'keyDown': None, 'borderTopColor': (167, 166, 152), 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': wx.Size(80, 18), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041a\u043e\u044d\u0444\u0438\u0446\u0438\u0435\u043d\u0442', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': u'self.SetRoundCorners((1,1,1,1))', 'description': None, 'shortHelpString': u'\u0414\u043e\u043b\u044f \u0432 \u043e\u0431\u0449\u0435\u0439 \u0441\u0443\u043c\u043c\u0435\r\n\u043f\u043b\u0430\u043d\u0430 \u0432\u0435\u0440\u0445\u043d\u0435\u0433\u043e \u0443\u0440\u043e\u0432\u043d\u044f', 'backgroundColor2': None, '_uuid': u'8cdf9fb8a7bed3e461f0766d99412a14', 'style': 0, 'bgrImage': None, 'flag': 0, 'child': [], 'cursorColor': (100, 100, 100), 'borderStyle': None, 'borderStep': 0, 'borderLeftColor': (167, 166, 152), 'name': u'HeadCell_LabelPar', 'borderBottomColor': (167, 166, 152), 'refresh': None, 'alias': None, 'borderWidth': 1, 'position': wx.Point(225, 40), 'backgroundType': 0, 'onInit': None}, {'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncEdtPar(evt)', 'pic': u'9999.9999', 'hlp': None, 'value': u'', 'font': {}, 'border': 0, 'size': (-1, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'res_module': None, 'description': None, '_uuid': u'22ebdf3e4504fb3ecfbba7ac7ee47bb3', 'moveAfterInTabOrder': u'edtSumma', 'flag': 0, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'edtPar', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(315, 40), 'onInit': None, 'refresh': []}, {'activate': 1, 'ctrl': u"import ic.utils.coderror as coderror\r\nimport ic.dlg.msgbox as msg\r\n\r\nif float(value) > 1:\r\n   _resultEval = coderror.IC_CTRL_FAILED_IGNORE\r\n   msg.MsgBox(self, '\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435 \u043c\u0430\u0440\u0436\u0438\u043d\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u043a\u043e\u044d\u0444\u0438\u0446\u0438\u0435\u043d\u0442\u0430 \u043d\u0435 \u043c\u043e\u0436\u0435\u0442 \u0431\u044b\u0442\u044c \u0431\u043e\u043b\u044c\u0448\u0435 1')\r\nelse:\r\n   _resultEval = coderror.IC_CTRL_OK", 'pic': u'99.9999', 'getvalue': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': (88, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'res_module': None, 'description': None, '_uuid': u'2fc6b683da670dd9411e09c67c5ba52d', 'moveAfterInTabOrder': u'edtPar', 'flag': 0, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'edtMarja', 'changed': None, 'value': u'', 'alias': None, 'init_expr': None, 'position': (485, 40), 'onInit': None, 'refresh': []}, {'activate': 1, 'show': 1, 'text': u'\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e', 'refresh': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', 'res_module': None, 'description': None, '_uuid': u'abbda862f6c84042515d397c949e9857', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_1771', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(10, 70), 'onInit': None}, {'activate': 1, 'show': 1, 'borderRightColor': (167, 166, 152), 'child': [], 'refresh': None, 'borderWidth': 1, 'borderTopColor': (167, 166, 152), 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': wx.Size(80, 18), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041a\u043e\u043b. \u043a\u043e\u044d\u0444.', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'description': None, 'shortHelpString': u'\u0414\u043e\u043b\u044f \u0432 \u043e\u0431\u0449\u0435\u043c \u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u0435\r\n\u043f\u043b\u0430\u043d\u0430 \u0432\u0435\u0440\u0445\u043d\u0435\u0433\u043e \u0443\u0440\u043e\u0432\u043d\u044f', 'backgroundColor2': None, '_uuid': u'9dc5aeab5921d31e2cf197a51b8f42a1', 'style': 0, 'bgrImage': None, 'flag': 0, 'recount': None, 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': (167, 166, 152), 'name': u'HeadCell_LabelKolPar', 'borderBottomColor': (167, 166, 152), 'keyDown': None, 'alias': None, 'init_expr': u'self.SetRoundCorners((1,1,1,1))', 'position': wx.Point(225, 70), 'borderStyle': None, 'onInit': None}, {'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncEdtKol(value, evt)', 'pic': u'999,999,999.99', 'getvalue': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': (-1, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'res_module': None, 'description': None, '_uuid': u'28fda84dfa0de682d66015c19448e05f', 'moveAfterInTabOrder': u'edtMarza', 'flag': 0, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'edtKol', 'changed': None, 'value': u'', 'alias': None, 'init_expr': None, 'position': wx.Point(105, 70), 'onInit': None, 'refresh': []}, {'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncEdtKolPar(evt)', 'pic': u'9999.9999', 'getvalue': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': (-1, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'res_module': None, 'description': None, '_uuid': u'84363b77bade30c057160d66f9494999', 'moveAfterInTabOrder': u'edtKol', 'flag': 0, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'edtKolPar', 'changed': None, 'value': u'', 'alias': None, 'init_expr': None, 'position': wx.Point(315, 70), 'onInit': None, 'refresh': []}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'res_module': None, 'description': None, '_uuid': u'865dc3ac47ac8e05369f2b17e545783b', 'moveAfterInTabOrder': u'edtKolPar', 'flag': 0, 'recount': [], 'hlp': u'WrapperObj.hlpFuncEi(self, evt)', 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'edtEI', 'changed': None, 'value': u'', 'alias': None, 'init_expr': None, 'position': (485, 70), 'onInit': None, 'refresh': []}, {'activate': 1, 'show': 1, 'borderRightColor': (167, 166, 152), 'recount': None, 'keyDown': None, 'borderTopColor': (167, 166, 152), 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (18, 18), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'...', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': u'#self.SetRoundCorners((1,1,1,1))\r\nself.SetButtonStyle()', 'description': None, 'shortHelpString': u'\u041f\u043e\u043c\u043e\u0449\u044c', 'backgroundColor2': None, '_uuid': u'383d7a443d7e0959c808aa7a371243ea', 'style': 0, 'bgrImage': None, 'flag': 0, 'child': [], 'onLeftDown': u"res = WrapperObj.hlpFuncEi(self, evt)\r\n#print '===== INTERFACE=', GetInterface()\r\nctrl = WrapperObj.GetNameObj('edtEI')\r\nprint '========== CTRL=', ctrl, self\r\nif res[1]:\r\n    ctrl.SetValue(res[1], 1, False)\r\n    ctrl.SetFocus()\r\n", 'cursorColor': (100, 100, 100), 'borderStyle': None, 'borderStep': 0, 'borderLeftColor': None, 'name': u'edtEIHlp', 'borderBottomColor': (167, 166, 152), 'refresh': None, 'alias': None, 'borderWidth': 1, 'position': (555, 70), 'backgroundType': 0, 'onInit': None}, {'activate': 1, 'show': 1, 'borderRightColor': (167, 166, 152), 'recount': None, 'keyDown': None, 'borderTopColor': (167, 166, 152), 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': wx.Size(50, 18), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u0415\u0434. \u0438\u0437\u043c.', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'init_expr': u'self.SetRoundCorners((1,1,1,1))', 'description': None, 'shortHelpString': u'\u0415\u0434\u0438\u043d\u0438\u0446\u044b \u0438\u0437\u043c\u0435\u0440\u0435\u043d\u0438\u044f \r\n\u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u0430', 'backgroundColor2': None, '_uuid': u'9b296094469932568739fd0a044661ae', 'style': 0, 'bgrImage': None, 'flag': 0, 'child': [], 'cursorColor': (100, 100, 100), 'borderStyle': None, 'borderStep': 0, 'borderLeftColor': (167, 166, 152), 'name': u'HeadCell_LabelEdIzm', 'borderBottomColor': (167, 166, 152), 'refresh': None, 'alias': None, 'borderWidth': 1, 'position': wx.Point(428, 70), 'backgroundType': 0, 'onInit': None}, {'activate': 1, 'show': 1, 'borderRightColor': (167, 166, 152), 'recount': None, 'keyDown': None, 'borderTopColor': (167, 166, 152), 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': wx.Size(50, 18), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041c\u0430\u0440\u0436\u0430', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': u'self.SetRoundCorners((1,1,1,1))', 'description': None, 'shortHelpString': u'\u0414\u043e\u043b\u044f \u043c\u0430\u0440\u0436\u0438\u043d\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u0434\u043e\u0445\u043e\u0434\u0430.\r\n\u041f\u0440\u0438\u043c\u0435\u0440: 0.1 \u0441\u043e\u043e\u0442\u0432\u0435\u0442\u0441\u0442\u0432\u0443\u0435\u0442 10%\r\n\u043e\u0442 \u043f\u043b\u0430\u043d\u0438\u0440\u0443\u0435\u043c\u043e\u0439 \u0441\u0443\u043c\u043c\u044b', 'backgroundColor2': None, '_uuid': u'0ae093a190834bb37e6ccfd56b73f038', 'style': 0, 'bgrImage': None, 'flag': 0, 'child': [], 'cursorColor': (100, 100, 100), 'borderStyle': None, 'borderStep': 0, 'borderLeftColor': (167, 166, 152), 'name': u'HeadCell_LabelMarja', 'borderBottomColor': (167, 166, 152), 'refresh': None, 'alias': None, 'borderWidth': 1, 'position': wx.Point(428, 40), 'backgroundType': 0, 'onInit': None}, {'activate': 1, 'show': 1, 'mouseClick': u'WrapperObj.mouseClickFuncRecountBtn(evt)', 'font': {}, 'border': 0, 'size': wx.Size(100, 19), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041f\u0435\u0440\u0435\u0441\u0447\u0435\u0442 \u0441\u0443\u043c\u043c', 'source': u'', 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'res_module': None, 'description': None, '_uuid': u'cd88a2441a5ad21ca7facc5429a3ed40', 'moveAfterInTabOrder': u'edtEI', 'flag': 0, 'recount': None, 'name': u'recountBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(590, 39), 'onInit': None, 'refresh': None, 'mouseContextDown': u''}, {'activate': 1, 'show': 1, 'mouseClick': u'WrapperObj.mouseClickFuncRecountKolBtn(evt)', 'font': {}, 'border': 0, 'size': wx.Size(100, 19), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041f\u0435\u0440\u0435\u0441\u0447\u0435\u0442 \u043a\u043e\u043b.', 'source': u'', 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'res_module': None, 'description': None, '_uuid': u'bc0638cbe0426f54f54e1e1cbae885fd', 'moveAfterInTabOrder': u'recountBtn', 'flag': 0, 'recount': None, 'name': u'recountKolBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(590, 70), 'onInit': None, 'refresh': None, 'mouseContextDown': u''}, {'activate': 1, 'show': 1, 'child': [], 'keyDown': None, 'border': 0, 'size': wx.Size(0, 20), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'1f8e140ea992073fbeda6e4744ecce40', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'recount': None, 'name': u'defaultWindow_2835', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(715, 78), 'onInit': None}], 'name': u'baseParPanel', 'refresh': None, 'alias': None, 'init_expr': u'self.SetRoundBoundMode((208, 198, 153),1)', 'position': wx.Point(0, 0), 'onInit': None}, {'line_color': (200, 200, 200), 'activate': u'0', 'show': 1, 'cols': [{'activate': 1, 'ctrl': u'WrapperObj.ctrlFunccodPlan(self.GetView(), value, row, col, evt)', 'pic': u'S', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u0434', 'width': 77, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'cbd1158f8ad4e84e3b8eb0b5e71ce969', 'recount': None, 'hlp': u'WrapperObj.hlpFunccodPlan(evt, self.GetView(), row, col)', 'name': u'codPlan', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u043b\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f', 'width': 135, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'5e9846f54da2e935c00ba7b51ff75852', 'backgroundColor': (255, 255, 255), 'font': {'style': u'boldItalic', 'name': u'defaultFont', 'family': u'sansSerif', '__attr_types__': {}, 'faceName': u'Times New Roman', 'type': u'Font', 'underline': False, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'cbd1158f8ad4e84e3b8eb0b5e71ce969', 'recount': None, 'hlp': None, 'name': u'descrPlan', 'setvalue': u'', 'attr': u'R', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncParPlan(self.GetView(), value, row, evt)', 'pic': u'F:3,4', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u044d\u0444\u0444\u0438\u0446\u0438\u0435\u043d\u0442', 'width': 82, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'5d11a26066293674f18777e702129614', 'recount': None, 'hlp': None, 'attr': u'W', 'setvalue': u'', 'name': u'parPlan', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncSummaPlan(self.GetView(), value, row, evt)', 'pic': u'999,999,999.99', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u0421\u0443\u043c\u043c\u0430', 'width': 99, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'926e12e31dafba1c9a83644e0cd69faa', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': u"('right', 'middle')"}, 'description': None, 'shortHelpString': u'', '_uuid': u'ebf635b610909713247183a1d134c42f', 'recount': None, 'getvalue': u'', 'name': u'summaPlan', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': u'0', 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'key', 'width': 50, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'b56cfbe4d33c37b83e07a2b9dd26cab6', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'keyPlan', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncParKolPlan(self.GetView(), value, row, evt)', 'pic': u'F:3,4', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u043b. \u043a\u043e\u044d\u0444\u0444.', 'width': 97, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'f76c0e938d13423107e7fa76f9b4cb9e', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'5d11a26066293674f18777e702129614', 'recount': None, 'getvalue': u'', 'name': u'parKolPlan', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncKolPlan(self.GetView(), value, row, evt)', 'pic': u'999,999,999.99', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e', 'width': 101, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'9bb2a86b3a77d7199b081d56d2886c25', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': u"('right', 'middle')"}, 'description': None, 'shortHelpString': u'', '_uuid': u'ebf635b610909713247183a1d134c42f', 'recount': None, 'hlp': None, 'attr': u'W', 'setvalue': u'', 'name': u'kolPlan', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u'', 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u0415\u0434. \u0438\u0437\u043c.', 'width': 73, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'9bb2a86b3a77d7199b081d56d2886c25', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': u"('right', 'middle')"}, 'description': None, 'shortHelpString': u'', '_uuid': u'ebf635b610909713247183a1d134c42f', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'ei', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u"import ic.utils.coderror as coderror\r\nimport ic.dlg.msgbox as msg\r\n\r\nif float(value) > 1:\r\n   _resultEval = coderror.IC_CTRL_FAILED_IGNORE\r\n   msg.MsgBox(self.GetView(), '\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435 \u043c\u0430\u0440\u0436\u0438\u043d\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u043a\u043e\u044d\u0444\u0438\u0446\u0438\u0435\u043d\u0442\u0430 \u043d\u0435 \u043c\u043e\u0436\u0435\u0442 \u0431\u044b\u0442\u044c \u0431\u043e\u043b\u044c\u0448\u0435 1')\r\nelse:\r\n   _resultEval = coderror.IC_CTRL_OK", 'pic': u'99.9999', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u041c\u0430\u0440\u0436\u0430', 'width': 58, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'4b3c2cd8510b9449e111def458ca84b4', 'recount': None, 'hlp': None, 'attr': u'W', 'setvalue': u'', 'name': u'marja', 'keyDown': None, 'alias': None, 'init_expr': None}], 'row_height': 20, 'keyDown': u'WrapperObj.keyDownFuncplanGrid(self, evt)', 'border': 0, 'post_select': None, 'size': (-1, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'delRec': u'WrapperObj.delRecFuncplanGrid(self.GetView(), row, evt)', 'component_module': None, 'selected': None, 'proportion': 1, 'getattr': None, 'label': u'Grid', 'source': None, 'init': u'WrapperObj.initFuncplanGrid(self.GetView(), row, evt)', 'backgroundColor': None, 'fixRowSize': 0, 'type': u'GridDataset', 'res_module': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'9e3f5e784eb96f556801bfbd78bbeeef', 'backgroundColor': None, 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'fixColSize': 0, 'description': None, 'post_del': None, 'post_init': None, '_uuid': u'b6d40f5e73ffaec2b511a96049dd4ef0', 'style': 0, 'docstr': u'ic.components.icgrid.html', 'flag': 8192, 'dclickEditor': None, 'recount': u'', 'label_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'd0dc83465afa248c91dbda25825b9278', 'backgroundColor': None, 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'label_attr', 'alignment': (u'left', u'middle')}, 'name': u'planGrid', 'label_height': 20, 'changed': None, 'onSize': None, 'alias': None, 'init_expr': u'import ic.utils.graphicUtils as graph\r\nclr = graph.GetMidColor(self.GetParent().GetBackgroundColour(), wx.Color(255,255,255), 0.5)\r\n#self.SetRoundBoundMode((150,150,140), 2)\r\nself.SetDefaultCellBackgroundColour(clr)', 'position': wx.Point(44, 27), 'onInit': None, 'refresh': None}, {'activate': u'0', 'show': 1, 'child': [{'activate': u'1', 'show': u'1', 'child': [], 'keyDown': None, 'border': 0, 'size': (0, 22), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': (128, 128, 192), 'type': u'Panel', 'res_module': None, 'description': None, 'onClose': None, '_uuid': u'047af9cf1d617f276e0d356af658d11f', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'recount': None, 'name': u'defaultWindow_3416', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(421, 17), 'onInit': None}, {'activate': 1, 'show': 1, 'borderRightColor': (167, 166, 152), 'child': [], 'refresh': None, 'borderWidth': 1, 'borderTopColor': (167, 166, 152), 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': wx.Size(80, 18), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041d\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u043a\u0430', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'description': None, 'shortHelpString': u'\u041e\u043f\u0440\u0435\u0434\u0435\u043b\u044f\u0435\u0442 \u0441\u043f\u043e\u0441\u043e\u0431 \u043d\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u043a\u0438 \u043a\u043e\u044d\u0444\u0438\u0446\u0438\u0435\u043d\u0442\u043e\u0432', 'backgroundColor2': None, '_uuid': u'bb0e914c75cee5800c8d7e6aee737294', 'style': 0, 'bgrImage': None, 'flag': 0, 'recount': None, 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': (167, 166, 152), 'name': u'normaLabel', 'borderBottomColor': (167, 166, 152), 'keyDown': None, 'alias': None, 'init_expr': u'self.SetRoundCorners((1,1,1,1))', 'position': (10, 10), 'borderStyle': None, 'onInit': None}, {'activate': 1, 'show': 1, 'keyDown': None, 'border': 0, 'size': (100, -1), 'style': 33555520, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': (255, 255, 255), 'type': u'Choice', 'res_module': None, 'loseFocus': None, 'description': None, '_uuid': u'28c7abc43bdfd812a2738a349df86435', 'moveAfterInTabOrder': u'', 'choice': u'WrapperObj.choiceFuncNormaChoice(evt)', 'flag': 0, 'recount': [], 'field_name': None, 'setFocus': None, 'name': u'normaChoice', 'items': u'', 'refresh': [], 'alias': None, 'init_expr': None, 'position': (105, 10), 'onInit': u'self.setDictRepl(GetInterface().idNormaDct)\r\nself.SetValue(0)'}, {'activate': 1, 'show': 1, 'borderRightColor': (167, 166, 152), 'recount': None, 'keyDown': None, 'borderTopColor': (167, 166, 152), 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': wx.Size(80, 18), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041f\u0435\u0440\u0435\u0441\u0447\u0435\u0442', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': u'self.SetRoundCorners((1,1,1,1))', 'description': None, 'shortHelpString': u'\u0421\u043f\u043e\u0441\u043e\u0431 \u043f\u0435\u0440\u0441\u0447\u0435\u0442\u0430 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0439', 'backgroundColor2': None, '_uuid': u'e3c8ad44ed9d21a4535cd1717e9afdce', 'style': 0, 'bgrImage': None, 'flag': 0, 'child': [], 'cursorColor': (100, 100, 100), 'borderStyle': None, 'borderStep': 0, 'borderLeftColor': (167, 166, 152), 'name': u'recountTypeLabel', 'borderBottomColor': (167, 166, 152), 'refresh': None, 'alias': None, 'borderWidth': 1, 'position': wx.Point(225, 10), 'backgroundType': 0, 'onInit': None}, {'activate': 1, 'show': 1, 'refresh': [], 'border': 0, 'size': (200, -1), 'style': 33555520, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': (255, 255, 255), 'type': u'Choice', 'res_module': None, 'loseFocus': None, 'description': None, '_uuid': u'8221369ed768eef9e24bd10a4fbef6a2', 'moveAfterInTabOrder': u'', 'choice': u'WrapperObj.choiceFuncRecountTypeChoice(evt)', 'flag': 0, 'recount': [], 'field_name': None, 'setFocus': None, 'name': u'recountTypeChoice', 'items': u'', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(315, 10), 'onInit': u'self.setDictRepl(GetInterface().idRecountDct)\r\nself.SetValue(0)'}], 'keyDown': None, 'border': 0, 'size': (240, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': (247, 245, 234), 'type': u'Panel', 'res_module': None, 'description': None, 'onClose': None, '_uuid': u'8a8be3b478b859171f8fdbc03dd3baf7', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'recount': None, 'name': u'addCtrlPanel', 'refresh': None, 'alias': None, 'init_expr': u'self.SetRoundBoundMode((208, 198, 153),1)', 'position': wx.Point(0, 98), 'onInit': None}, {'LabelBgrColor': (247, 245, 234), 'activate': 1, 'LabelBorderColor': (208, 198, 153), 'border': 0, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'delRec': u'WrapperObj.delRecFuncplanGrid(self.GetView(), row, evt)', 'component_module': None, 'proportion': 1, 'init': u'WrapperObj.initFuncplanGrid(self.GetView(), row, evt)', 'source': None, 'getattr': None, 'scheme': u'STD', 'type': u'StdDataGrid', 'LabelFgrColor': (0, 0, 0), 'res_module': None, 'description': None, 'nest': u'GridDataset:DataGrid', '_uuid': u'876379e69ea8c215e793f6b43ec4e525', 'flag': 8192, 'child': [{'activate': 1, 'ctrl': u'WrapperObj.ctrlFunccodPlan(self.GetView(), value, row, col, evt)', 'pic': u'S', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u0434', 'width': 77, 'init': None, 'valid': None, 'type': u'GridCell', 'res_module': None, 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'cbd1158f8ad4e84e3b8eb0b5e71ce969', 'recount': None, 'hlp': u'WrapperObj.hlpFunccodPlan(evt, self.GetView(), row, col)', 'attr': u'W', 'setvalue': u'', 'name': u'codPlan', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u043b\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f', 'width': 135, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'5e9846f54da2e935c00ba7b51ff75852', 'backgroundColor': (255, 255, 255), 'font': {'style': u'boldItalic', 'name': u'defaultFont', 'family': u'sansSerif', '__attr_types__': {}, 'faceName': u'Times New Roman', 'type': u'Font', 'underline': False, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'cbd1158f8ad4e84e3b8eb0b5e71ce969', 'recount': None, 'hlp': None, 'name': u'descrPlan', 'setvalue': u'', 'attr': u'R', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncParPlan(self.GetView(), value, row, evt)', 'pic': u'999.9999', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u044d\u0444\u0444\u0438\u0446\u0438\u0435\u043d\u0442', 'width': 82, 'init': None, 'valid': None, 'type': u'GridCell', 'res_module': None, 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'5d11a26066293674f18777e702129614', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'parPlan', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncSummaPlan(self.GetView(), value, row, evt)', 'pic': u'999,999,999.99', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u0421\u0443\u043c\u043c\u0430', 'width': 99, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'926e12e31dafba1c9a83644e0cd69faa', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': u"('right', 'middle')"}, 'description': None, 'shortHelpString': u'', '_uuid': u'ebf635b610909713247183a1d134c42f', 'recount': None, 'getvalue': u'', 'name': u'summaPlan', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncParKolPlan(self.GetView(), value, row, evt)', 'pic': u'999.9999', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u043b. \u043a\u043e\u044d\u0444\u0444.', 'width': 97, 'init': None, 'valid': None, 'type': u'GridCell', 'res_module': None, 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'f76c0e938d13423107e7fa76f9b4cb9e', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'5d11a26066293674f18777e702129614', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'parKolPlan', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncKolPlan(self.GetView(), value, row, evt)', 'pic': u'999,999,999.99', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e', 'width': 101, 'init': None, 'valid': None, 'type': u'GridCell', 'res_module': None, 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'9bb2a86b3a77d7199b081d56d2886c25', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': u"('right', 'middle')"}, 'description': None, 'shortHelpString': u'', '_uuid': u'ebf635b610909713247183a1d134c42f', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'kolPlan', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u'', 'pic': u'S', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u0415\u0434. \u0438\u0437\u043c.', 'width': 73, 'init': None, 'valid': None, 'type': u'GridCell', 'res_module': None, 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'9bb2a86b3a77d7199b081d56d2886c25', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': u"('right', 'middle')"}, 'description': None, 'shortHelpString': u'', '_uuid': u'ebf635b610909713247183a1d134c42f', 'recount': None, 'hlp': u'WrapperObj.hlpFuncEi(self.GetView(), evt)', 'attr': u'W', 'setvalue': u'', 'name': u'ei', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u"import ic.utils.coderror as coderror\r\nimport ic.dlg.msgbox as msg\r\n\r\nif float(value) > 1:\r\n   _resultEval = coderror.IC_CTRL_FAILED_IGNORE\r\n   msg.MsgBox(self.GetView(), '\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435 \u043c\u0430\u0440\u0436\u0438\u043d\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u043a\u043e\u044d\u0444\u0438\u0446\u0438\u0435\u043d\u0442\u0430 \u043d\u0435 \u043c\u043e\u0436\u0435\u0442 \u0431\u044b\u0442\u044c \u0431\u043e\u043b\u044c\u0448\u0435 1')\r\nelse:\r\n   _resultEval = coderror.IC_CTRL_OK", 'pic': u'99.9999', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u041c\u0430\u0440\u0436\u0430', 'width': 58, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'4b3c2cd8510b9449e111def458ca84b4', 'recount': None, 'getvalue': u'', 'name': u'marja', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}], 'name': u'planGridPanel', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1)}, {'activate': u'0', 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'e981776d48f50fbe36f8c6da79496d03', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'child': [], 'name': u'defaultWindow_1630', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}, {'activate': u'0', 'minCellWidth': 0, 'minCellHeight': 10, 'border': 0, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'flexRows': [0], 'component_module': None, 'flexCols': [1], 'proportion': 0, 'type': u'GridBagSizer', 'hgap': 0, 'description': None, '_uuid': u'5be99d3ac9e9afba2ed6b122554f43d3', 'flag': 8192, 'child': [{'activate': u'0', 'show': 1, 'child': [{'activate': 1, 'show': 1, 'text': u'\u0414\u0435\u043a\u0430\u0434\u043d\u044b\u0435 \u043a\u043e\u044d\u0444\u0438\u0446\u0438\u0435\u043d\u0442\u044b \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u044e\u0442\u0441\u044f \u0434\u043b\u044f \r\n\u0432\u044b\u0447\u0438\u0441\u043b\u0435\u043d\u0438\u044f \u043f\u043e\u043f\u0440\u0430\u0432\u043e\u043a \u043a \u0434\u043d\u0435\u0432\u043d\u044b\u043c \u043f\u043b\u0430\u043d\u0430\u043c \u0438\r\n\u043e\u043f\u0440\u0435\u0434\u0435\u043b\u044f\u044e\u0442\u0441\u044f \u0442\u043e\u043b\u044c\u043a\u043e \u043d\u0430 \u0443\u0437\u043b\u0430\u0445 \u043c\u0435\u0441\u044f\u0447\u043d\u044b\u0445 \r\n\u043f\u043b\u0430\u043d\u043e\u0432', 'keyDown': None, 'font': {'style': u'bold', 'size': 8, 'underline': False, 'family': u'sansSerif', 'faceName': u'Tahoma'}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', 'description': None, '_uuid': u'd8b5e1c86dad9e2ee5b1a987751d9b8b', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_3007_3555', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(21, 15), 'onInit': None}], 'keyDown': None, 'border': 0, 'size': (80, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': (189, 230, 214), 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'20490a955c6e0f2c10a7cf6b789a2ecd', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'recount': None, 'name': u'defaultWindow_1829', 'refresh': None, 'alias': None, 'init_expr': u'import ic.utils.graphicUtils as graph\r\nself.SetRoundBoundMode((150,150,150),2)\r\nbgr = self.GetParent().GetBackgroundColour()\r\nclr = graph.GetMidColor(bgr, wx.Color(255,255,255), 0.5)\r\nself.SetBackgroundColour(clr)', 'position': (0, 1), 'onInit': None}, {'style': 0, 'activate': u'1', 'span': (1, 1), 'description': None, 'component_module': None, 'type': u'SizerSpace', '_uuid': u'261bd37f1a106e47de3362c58ee6d76d', 'proportion': 0, 'name': u'DefaultName_1943', 'alias': None, 'flag': 0, 'init_expr': None, 'position': (0, 1), 'border': 0, 'size': (7, 150)}, {'activate': u'1', 'show': 1, 'child': [{'line_color': (200, 200, 200), 'activate': u'1', 'show': 1, 'cols': [{'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u0414\u0435\u043a\u0430\u0434\u0430', 'width': 46, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'96daac6ce9229c31951a767d383fc780', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'4cfe98bb2517cd5be2fa420f21619e4c', 'recount': None, 'getvalue': u'', 'name': u'codDecade', 'setvalue': u'', 'attr': u'R', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'9999.999', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u044d\u0444\u0444\u0438\u0446\u0438\u0435\u043d\u0442', 'width': 75, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'0a38721df26c609aa5dfcff60f07cee4', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'd737975eea1cbec6036adf2844a26b17', 'recount': None, 'hlp': None, 'name': u'param', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': u'1', 'ctrl': None, 'pic': u'9999.999', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u043b. \u043a\u043e\u044d\u0444\u0444.', 'width': 95, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'5d5810cb3c0a99e82bb559be52270de6', 'recount': None, 'hlp': None, 'attr': u'W', 'setvalue': u'', 'name': u'kolParam', 'keyDown': None, 'alias': None, 'init_expr': None}], 'row_height': 20, 'onSize': u'', 'border': 0, 'post_select': None, 'size': wx.Size(250, 128), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'delRec': u'WrapperObj.delRecFuncdecadeGrid(evt)', 'component_module': None, 'selected': None, 'proportion': 2, 'getattr': None, 'label': u'Grid', 'source': None, 'init': u'False', 'backgroundColor': None, 'fixRowSize': 0, 'type': u'GridDataset', 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'41cca5d586020d44afa8cb40cde46c20', 'backgroundColor': None, 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'fixColSize': 0, 'description': None, 'post_del': None, 'post_init': None, '_uuid': u'4c74456614d901becf48bb0ac99291ca', 'style': 0, 'docstr': u'ic.components.icgrid.html', 'flag': 8192, 'dclickEditor': None, 'recount': None, 'label_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'6272dcaade955f85bd9ba56fc8cf5525', 'backgroundColor': None, 'font': {'style': u'regular', 'name': u'defaultFont', 'family': u'sansSerif', '__attr_types__': {}, 'faceName': u'Tahoma', 'type': u'Font', 'underline': False, 'size': 8}, 'type': u'label_attr', 'alignment': (u'left', u'middle')}, 'name': u'decadeGrid', 'label_height': 20, 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (7, 7), 'onInit': u'', 'refresh': None}, {'activate': u'0', 'show': u'1', 'child': [], 'keyDown': None, 'border': 0, 'size': wx.Size(1, 3), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': (128, 128, 192), 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'8fa1f5b94e71b9d5a0a11c7ec7af2b6f', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'recount': None, 'name': u'defaultWindow_3416', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(241, 51), 'onInit': None}], 'keyDown': None, 'border': 0, 'size': (240, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': (248, 248, 239), 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'9f8648108392815975d1688a4a5a6b13', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'recount': None, 'name': u'forDecPanel', 'refresh': None, 'alias': None, 'init_expr': u'self.SetRoundBoundMode((187, 187, 115),1)', 'position': (0, 0), 'onInit': None}], 'name': u'DefaultName_1182', 'alias': None, 'init_expr': None, 'position': (-1, -1), 'vgap': 0}, {'activate': u'1', 'show': 1, 'child': [{'line_color': (200, 200, 200), 'activate': u'1', 'show': 1, 'cols': [{'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u0414\u0435\u043a\u0430\u0434\u0430', 'width': 46, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'96daac6ce9229c31951a767d383fc780', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'4cfe98bb2517cd5be2fa420f21619e4c', 'recount': None, 'hlp': None, 'attr': u'R', 'setvalue': u'', 'name': u'codDecade', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'9999.999', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u044d\u0444\u0444\u0438\u0446\u0438\u0435\u043d\u0442', 'width': 75, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'0a38721df26c609aa5dfcff60f07cee4', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'd737975eea1cbec6036adf2844a26b17', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'param', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': u'1', 'ctrl': None, 'pic': u'9999.999', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u043b. \u043a\u043e\u044d\u0444\u0444.', 'width': 95, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'5d5810cb3c0a99e82bb559be52270de6', 'recount': None, 'getvalue': u'', 'name': u'kolParam', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}], 'onSize': u'', 'border': 0, 'post_select': None, 'size': wx.Size(250, 128), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'delRec': u'WrapperObj.delRecFuncdecadeGrid(evt)', 'row_height': 20, 'selected': None, 'proportion': 2, 'getattr': None, 'label': u'Grid', 'source': None, 'init': u'False', 'backgroundColor': (248, 248, 239), 'fixRowSize': 0, 'type': u'GridDataset', 'init_expr': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'41cca5d586020d44afa8cb40cde46c20', 'backgroundColor': None, 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'fixColSize': 0, 'description': None, 'post_del': None, 'post_init': None, '_uuid': u'4348ee9ec20124cddaaeb7c4d4cc112b', 'style': 0, 'docstr': u'ic.components.icgrid.html', 'flag': 8192, 'dclickEditor': None, 'recount': None, 'label_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'6272dcaade955f85bd9ba56fc8cf5525', 'backgroundColor': (248, 248, 239), 'font': {'style': u'regular', 'name': u'defaultFont', 'family': u'sansSerif', '__attr_types__': {}, 'faceName': u'Tahoma', 'type': u'Font', 'underline': False, 'size': 8}, 'type': u'label_attr', 'alignment': (u'left', u'middle')}, 'name': u'decadeGrid', 'label_height': 20, 'changed': None, 'keyDown': None, 'alias': None, 'component_module': None, 'position': (7, 7), 'onInit': u'', 'refresh': None}, {'activate': u'1', 'show': u'1', 'child': [], 'keyDown': None, 'border': 0, 'size': wx.Size(0, 22), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': (128, 128, 192), 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'047af9cf1d617f276e0d356af658d11f', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'recount': None, 'name': u'defaultWindow_3416', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(267, 118), 'onInit': None}, {'hgap': 0, 'style': 0, 'activate': u'0', 'layout': u'vertical', 'description': None, 'position': (0, 0), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'8e6c74dfbe99988b76da8f2920b87544', 'proportion': 0, 'name': u'DefaultName_1303', 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'LabelBgrColor': None, 'activate': 1, 'LabelBorderColor': None, 'border': 0, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'delRec': u'WrapperObj.delRecFuncdecadeGrid(evt)', 'component_module': None, 'proportion': 0, 'init': u'False', 'scheme': u'STD', 'type': u'StdDataGrid', 'LabelFgrColor': None, 'description': None, 'nest': u'GridDataset:DataGrid', '_uuid': u'edf448d3d9f9493bf3e3429ab0d3762b', 'flag': 0, 'child': [{'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u0414\u0435\u043a\u0430\u0434\u0430', 'width': 46, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'96daac6ce9229c31951a767d383fc780', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'4cfe98bb2517cd5be2fa420f21619e4c', 'recount': None, 'hlp': None, 'name': u'codDecade', 'setvalue': u'', 'attr': u'R', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'9999.999', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u044d\u0444\u0444\u0438\u0446\u0438\u0435\u043d\u0442', 'width': 75, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'0a38721df26c609aa5dfcff60f07cee4', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'd737975eea1cbec6036adf2844a26b17', 'recount': None, 'getvalue': u'', 'name': u'param', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': u'1', 'ctrl': None, 'pic': u'9999.999', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u043b. \u043a\u043e\u044d\u0444\u0444.', 'width': 95, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'5d5810cb3c0a99e82bb559be52270de6', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'kolParam', 'keyDown': None, 'alias': None, 'init_expr': None}], 'name': u'decadeGridPanel', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1)}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'keyDown': None, 'border': 0, 'size': (240, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': (248, 248, 239), 'type': u'Panel', 'res_module': None, 'description': None, 'onClose': None, '_uuid': u'a16e1278c9c3ee22efcf9c6336f1bca8', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'recount': None, 'name': u'forDecPanel', 'refresh': None, 'alias': None, 'init_expr': u'self.SetRoundBoundMode((208, 198, 153),1)', 'position': wx.Point(0, 351), 'onInit': None}], 'span': (1, 1), 'res_module': None, 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'name': u'edtPanel', 'refresh': None, 'alias': None, 'init_expr': u'', 'position': wx.Point(0, 0), 'onInit': u'WrapperObj.OnInitGrids(evt)'}

#   Версия объекта
__version__ = (1, 1, 2, 6)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'IAspectEdtPanel'

COL_GRID_KEY = ieditpanel.COL_GRID_KEY

class IAspectEdtPanel(ieditpanel.IEdtPanel):
    def __init__(self, parent, metaObj=None, tree = None):
        """
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type metaObj: C{icMetaItem}
        @param metaObj: Указатель на метаобъект плана в определенном разрезе.
        @type tree: C{ic.components.user.ictreelistctrl.icTreeListCtrl}
        @param tree: Указатель на дерево планов.
        """
        self._decade_data = None
        self._data = None
        
        ieditpanel.IEdtPanel.__init__(self, parent, resource, metaObj, tree)
        if metaObj and metaObj.value.metatype <> 'mMonth':
            self.GetNameObj('forDecPanel').Show(False)
            self.get_dec_grid().Show(False)
    
    def _findParentNodeByMetatype(self, metaObj, metaType):
        """
        Ищет родительский узел с заданным метатипом.
        """
        while metaObj:
            if metaObj.value.metatype == metaType:
                return metaObj
                
            metaObj = metaObj.getItemParent()
                        
    def _findFullCode(self, metaObj, mType):
        """
        Возвращает родительский код.
        """
        cod = []
        
        while 1:
            metaObj = self._findParentNodeByMetatype(metaObj, mType)    
            if not metaObj:
                break

            if type(metaObj.value.sprav) == type(''):
                cod.append(metaObj.value.name)
                break
            else:
                sprav, mType, lev = metaObj.value.sprav
                
            cod.append(metaObj.value.name)

        cod.reverse()
        return cod
    
    def get_plan_grid(self):
        """
        Возвращает указатель на грид планирования.
        """
        #return self.GetNameObj('planGrid') (198, 217, 227) | (184, 205, 220)
        #print '*************** self.GetContext()=', self.GetContext()
        return self.GetNameObj('edtPanel').GetContext().GetInterface('planGridPanel').get_grid()
        
    def get_dec_grid(self):
        """
        Возвращает указатель на грид декадных коэфициентов.
        """
        return self.GetNameObj('decadeGrid')
        
    def LoadChildData(self):
        """
        Загружаем данные по дочерним планам.
        """

        if self.metaObj:
            lst = self.metaObj.keys()
            lst.sort()
            
            #--- Коэфициенты элементов планов
            self._data = range(len(lst))
            for i, key in enumerate(lst):
                obj = self.metaObj[key]
                self._data[i] = [key, obj.value.description, obj.value.w,
                                obj.value.summa, obj.value.w_kol,
                                obj.value.kol, obj.value.ei, obj.value.marja, key]

            self.get_plan_grid().dataset.SetDataBuff(self._data)
            self.get_plan_grid().RefreshGrid()
                
            return self._data
        
    def LoadData(self):
        """
        Загружаем данные по планам
        """
        if self.metaObj:
            descr = self.GetNameObj('edtDescription')
            edtId = self.GetNameObj('edtId')
            edtPar = self.GetNameObj('edtPar')
            edtSumma = self.GetNameObj('edtSumma')
            edtKolPar = self.GetNameObj('edtKolPar')
            edtKol = self.GetNameObj('edtKol')
            edtEI = self.GetNameObj('edtEI')
            
            self.summa = self.metaObj.value.summa
            self.kol = self.metaObj.value.kol
            self.decadePar = self.metaObj.value.decadWeight
            self.decadeKolPar = self.metaObj.value.decadWeightKol
            self.ei = self.metaObj.value.ei
            
            descr.SetValue(self.metaObj.value.description)
            edtId.SetValue(self.metaObj.value.name)
            edtPar.SetValue(self.metaObj.value.w)
            edtSumma.SetValue(self.summa)
            edtKolPar.SetValue(self.metaObj.value.w_kol)
            edtKol.SetValue(self.metaObj.value.kol)
            edtEI.SetValue(self.metaObj.value.ei)
            self.GetNameObj('edtMarja').SetValue(self.metaObj.value.marja)
            
            #--- Дочерние планы
            self.LoadChildData()

            #--- Декадные коэфициенты
            self._decade_data = (['I',1,1],
                        ['II',1,1],
                        ['III',1,1])

            if self.get_dec_grid().IsShown():
                for i, name in enumerate(self._decade_data):
                    self._decade_data[i][1] = self.decadePar[i]
                    self._decade_data[i][2] = self.decadeKolPar[i]

                self.get_dec_grid().dataset.SetDataBuff(self._decade_data)
                self.get_dec_grid().RefreshGrid()
                
            return (self._data, self._decade_data)
        
    ###BEGIN EVENT BLOCK
    def OnInitGrids(self, evt=None):
        """
        Функция обрабатывает событие <OnInit>.
        """
        self.LoadData()
    
    def hlpFuncedtId(self, evt):
        """
        Функция обрабатывает событие <F1> на поле ввода идентификатора плана.
        """
        if self.metaObj:
            prnt = self.GetNameObj('edtId')
            lev = None
            
            # Определяем имя справочника и родительский код (у иерархического справочника)
            try:
                # sprav, mType,lev - <Имя справочника>, <метатип узла, в котором хранится
                # родительский код>, <уровень справочник> 
                sprav, mType, lev = self.metaObj.value.sprav
                sprav_obj = spravctrl.getSprav(sprav)
                
                if lev > 0:
                    #cod = self.metaObj.getItemParent().name
#                    cod = self._findParentNodeByMetatype(self.metaObj, mType).name
#                    sprav_obj = spravctrl.getSprav(sprav)
#                    ParentCode = sprav_obj.StrCode2ListCode(cod)
#                    ParentCode = ParentCode[:lev] + [None]
                    ob = self._findFullCode(self.metaObj, mType)
                    ParentCode = ob[:lev] + [None]
                else:
                    ParentCode = (None,)
            except:
                sprav = self.metaObj.value.sprav
                sprav_obj = spravctrl.getSprav(sprav)
                ParentCode = (None, )

#            ret = spravctrl.HlpSprav(sprav, ParentCode = ParentCode,
#                    field={'descr':'name','cod':'cod'}, parentForm=prnt)
            ret = sprav_obj.Hlp(ParentCode = ParentCode,
                    field={'descr':'name','cod':'cod'}, parentForm=prnt)

            try:
                if ret[1] and lev:
                    ret = (ret[0], sprav_obj.StrCode2ListCode(ret[1])[lev], ret[2])
            except IndexError, TypeError:
                print '<ESCAPE>=', ret

            if ret and ret[2]:
                self.GetNameObj('edtDescription').SetValue(ret[2]['descr'], 1, False)
            
            #self.GetContext()['WrapperObj'] = None
            return ret
    
    def ctrlFuncEdtSumma(self, value, evt):
        """
        Функция контроля на изменения значения суммы текстового поля.
        """
        if self.metaObj and self.metaObj.isMyLock():
            S0=self.metaObj.value.summa
            self.metaObj.value.summa = float(value)
            self.ReCountPar(S0, self.metaObj.value.summa)
            #self.RecountChildSum()
            self.ReCount(True)
            #self.LoadChildData()

        return coderror.IC_CTRL_OK

    def ctrlFuncEdtKol(self, value, evt):
        """
        Функция контроля на изменения значения суммы текстового поля.
        """
        if self.metaObj and self.metaObj.isMyLock():
            S0=self.metaObj.value.kol
            self.metaObj.value.kol = float(value)
            self.ReCountKolPar(S0, self.metaObj.value.kol)
#            self.RecountChildKol()
#            self.LoadChildData()
            self.ReCountKol(True)

        return coderror.IC_CTRL_OK
    
    def ctrlFuncSummaPlan(self, grid, value, row, evt):
        """
        Функция контроля на изменения поля <summa> грида.
        """
        key = grid.dataset.data[row][0]
        
        if self.metaObj and self.metaObj.isMyLock() and key and self.metaObj.has_key(key):
            data = grid.dataset.data
            
            #   Вычисляем сумму весов без текущей строки
            S = 0
            for i, r in enumerate(data):
                if i <> row:
                    S += float(r[3])
            
            #   Определяем параметр в гриде
            if self.metaObj[key].value.summa<> 0 and self.metaObj[key].value.w <>0:
                data[row][2] = value/(self.metaObj[key].value.summa/self.metaObj[key].value.w)
            else:
                data[row][2] = 1
                
            self.metaObj[key].value.summa = float(value)
            self.SetSumma(S+value)
            self.ReCount(True)

    def ctrlFuncKolPlan(self, grid, value, row, evt):
        """
        Функция контроля на изменения поля <kolPlan> грида.
        """
        key = grid.dataset.data[row][0]
        
        if self.metaObj and self.metaObj.isMyLock() and key and self.metaObj.has_key(key):
            data = grid.dataset.data
            
            #   Вычисляем сумму весов без текущей строки
            S = 0
            for i, r in enumerate(data):
                if i <> row:
                    S += float(r[5])
            
            #   Определяем параметр в гриде
            if self.metaObj[key].value.kol<> 0 and self.metaObj[key].value.w_kol <>0:
                data[row][4] = value/(self.metaObj[key].value.kol/self.metaObj[key].value.w_kol)
            else:
                data[row][4] = 1
                
            self.metaObj[key].value.kol = float(value)
            self.SetKol(S+value)
            self.ReCountKol(True)
    
    def ctrlFuncParPlan(self, grid, value, row, evt):
        """
        Функция контроля на изменения поля весового параметра <param> грида.
        """
        if self.metaObj and self.metaObj.isMyLock():
            key = grid.dataset.data[row][0]
            self.metaObj[key].value.w = float(value)
            self.RecountChildSum()
            self.LoadChildData()
        return None

    def ctrlFuncParKolPlan(self, grid, value, row, evt):
        """
        Функция контроля на изменения поля весового параметра <parKolPlan> грида.
        """
        if self.metaObj and self.metaObj.isMyLock():
            key = grid.dataset.data[row][0]
            self.metaObj[key].value.w_kol = float(value)
            self.RecountChildKol()
            self.LoadChildData()
        return None
    
    def hlpFunccodPlan(self, evt, grid, row, col):
        """
        Функция обрабатывает запрос на подсказку по <F1> на поле кода
        элемента плана грида.
        """
        print '===== len(grid.dataset.data[row])=', len(grid.GetDataset().data[row]), row, COL_GRID_KEY
        key = grid.GetDataset().data[row][COL_GRID_KEY]
        
        if self.metaObj and key and self.metaObj.has_key(key):
            # Получаем доступ к справочнику
            obj = self.metaObj[key]
            prnt = self.GetNameObj('edtPanel')
            lev = None
            try:
                sprav, mType, lev = obj.value.sprav
                sprav_obj = spravctrl.getSprav(sprav)
                if lev > 0:
                    ob = self._findFullCode(obj, mType)
                    ParentCode = ob[:lev] + [None]
                else:
                    ParentCode = (None,)
            except:
                io_prnt.outErr('Ошибка:')
                ParentCode = (None, )
                sprav_obj = spravctrl.getSprav(obj.value.sprav)
                
            print '-------->>>> sprav,ParentCode=', ParentCode, obj.value.sprav
#            ret = spravctrl.HlpSprav(sprav,ParentCode=ParentCode,
#                    field={'descrPlan':'name','cod':'cod'}, parentForm=grid)
            ret = sprav_obj.Hlp(ParentCode=ParentCode,
                    field={'descrPlan':'name','cod':'cod'}, parentForm=grid)

#            if ret and lev and not ret[0] in (coderror.IC_DEL_FAILED_IGNORE, 
#                                                coderror.IC_CTRLKEY_FAILED):
            #if ret and lev:
            try:
                if ret[1] and lev:
                    ret = (ret[0], sprav_obj.StrCode2ListCode(ret[1])[lev], ret[2])
            except IndexError:
                print '<ESCAPE>'
               
            print '********** ret=', ret
            return ret
        
        return None
    
    def ctrlFunccodPlan(self, grid, value, row, col, evt):
        """
        Контроль поля кода плана <codPlan>.
        """
        try:
            key = grid.dataset.data[row][COL_GRID_KEY]
            obj = self.metaObj[key]

            if value == key:
                return coderror.IC_CTRL_OK
                
            elif value in [r[0] for r in grid.dataset.data]:
                prnt = self.GetNameObj('edtPanel')
                msgbox.MsgBox(prnt, 'Элемент плана уже введен')
                return coderror.IC_CTRL_FAILED_IGNORE
            
            ParentCode = ''
            try:
                sprav,  mType, lev = obj.value.sprav
                sprav_obj = spravctrl.getSprav(sprav)
                if lev > 0:
                    ob = self._findFullCode(obj, mType)
                    ParentCode = ''.join(ob[:lev])
            except:
                sprav = obj.value.sprav
                sprav_obj = spravctrl.getSprav(sprav)
                
            ret =  sprav_obj.Ctrl(ParentCode+value, field='cod', cod=ParentCode, flds={'descrPlan':'name'})
            print '----------- CTRL ret, ParentCode=', ret, ParentCode
            return ret
        except:
            return coderror.IC_CTRL_FAILED_IGNORE
            
    def keyDownFuncplanGrid(self, grid, evt):
        """
        Функция обрабатывает событие <?>.
        """
        return True
    
    def mouseClickFuncRecountBtn(self, evt):
        """
        Функция обрабатывает нажатие на кнопку <пересчитать >.
        """
        self.ReCount()

    def mouseClickFuncRecountKolBtn(self, evt):
        """
        Функция обрабатывает нажатие на кнопку <пересчитать >.
        """
        self.ReCountKol()
    
    def ctrlFuncEdtPar(self, evt):
        """
        Контроль поля <edtPar>.
        """
        #   Пересчитываем сумму
        if self.metaObj and self.metaObj.isMyLock():
            self.metaObj.value.w = float( self.GetNameObj('edtPar').GetValue())
            self.ReCount(metaObj=self.metaObj.getItemParent())
            self.GetNameObj('edtSumma').SetValue(self.metaObj.value.summa)
            self.GetNameObj('edtSumma').Refresh()
            
        return coderror.IC_CTRL_OK

    def ctrlFuncEdtKolPar(self, evt):
        """
        Контроль поля <edtPar>.
        """
        #   Пересчитываем сумму
        if self.metaObj and self.metaObj.isMyLock():
            self.metaObj.value.w_kol = float( self.GetNameObj('edtKolPar').GetValue())
            self.ReCountKol(metaObj=self.metaObj.getItemParent())
            self.GetNameObj('edtKol').SetValue(self.metaObj.value.kol)
            self.GetNameObj('edtKol').Refresh()
        
        return coderror.IC_CTRL_OK
            
    def initFuncplanGrid(self, grid, row, evt):
        """
        Функция обрабатывает после добавления записи в грид.
        """
        return False
    
    def delRecFuncplanGrid(self, grid, row, evt):
        """
        Функция обрабатывает событие <delRec>.
        """
        prnt = self.GetNameObj('edtPanel')
        if (self.metaObj and self.metaObj.isMyLock() and
            msgbox.MsgBox(prnt, 'Вы действительно хотите удалить запись?',
            style = wx.YES_NO | wx.NO_DEFAULT) == wx.ID_YES):
            
            key = grid.dataset.data[row][COL_GRID_KEY]
            self.metaObj[key].Del()
            print '$$$ DEL OBJECT key=', key
            self.ReCount()
            self.RefreshPanel()
            
        return coderror.IC_DEL_USER
    
    def ctrlFuncedtId(self, value, evt):
        """
        Функция контроля изменения идентификатора плана <ctrl>.
        """
        print '<<<< ctrlFuncedtId >>>>'
        if self.metaObj and self.metaObj.isMyLock():
            prnt_item = self.metaObj.getItemParent()
            
            if value in prnt_item.keys() and value <> self.metaObj.name:
                prnt = self.GetNameObj('edtPanel')
                msgbox.MsgBox(prnt, 'Такой мдентификатор плана уже есть')
                return coderror.IC_CTRL_FAILED_IGNORE
    
            try:
                ParentCode = ''
                try:
                    sprav,  mType, lev = self.metaObj.value.sprav
                    sprav_obj = spravctrl.getSprav(sprav)
                    if lev > 0:
                        ob = self._findFullCode(self.metaObj, mType)
                        ParentCode = ''.join(ob[:lev])
                except:
                    sprav = self.metaObj.value.sprav
                    sprav_obj = spravctrl.getSprav(sprav)
                    
                ret = sprav_obj.Ctrl(ParentCode+value, field='cod', cod=ParentCode)
                print '----------- CTRL ParentCode=', ParentCode, ret
                return ret
                #return spravctrl.CtrlSprav(sprav, value, field='cod')
            except:
                return coderror.IC_CTRL_FAILED_IGNORE
        else:
            return coderror.IC_CTRL_FAILED_IGNORE
        
    
    def delRecFuncdecadeGrid(self, evt):
        """
        Функция обрабатывает событие <delRec> на гриде декадных параметров.
        """
        return coderror.IC_DEL_FAILED_IGNORE
    
    
    def mouseClickFuncrecountKolBtn(self, evt):
        """
        Функция обрабатывает событие <?>.
        """
        return None
    
    def choiceFuncNormaChoice(self, evt):
        """
        Функция обрабатывает событие <?>.
        """
        id = self.GetNameObj('normaChoice').GetValue()
        self.setNormaType(id)

    def choiceFuncRecountTypeChoice(self, evt):
        """
        Функция обрабатывает событие <choice> на recountTypeChoice.
        """
        id = self.GetNameObj('recountTypeChoice').GetValue()
        self.setRecountEventType(id)
    
    
    def hlpFuncEi(self, grid, evt):
        """
        Функция обрабатывает событие <hlp> на GridCell:<ei> и TextField:<edtEI> .
        """
        sprav = spravctrl.getSprav('Edizm')
        ret = sprav.Hlp(ParentCode=(None,), field={'ei':'name'}, parentForm=grid)
        
        try:
            if ret[2]:
                return (ret[0], ret[2]['ei'], None)
        except IndexError, TypeError:
            print '<ESCAPE>'
            return ret

        return ret
    ###END EVENT BLOCK
            
    def ReCountPar(self, oldSum, summa):
        """
        Функция пересчитывает значение весового кофэфициента по старой и новой
        сумме.
        """
        
        #   Пересчитываем вес
        if oldSum <> 0 and self.metaObj.value.w<>0:
            k = oldSum/self.metaObj.value.w
            self.metaObj.value.w = summa/k
            self.GetNameObj('edtPar').SetValue(self.metaObj.value.w)
            self.GetNameObj('edtPar').Refresh()

    def ReCountKolPar(self, oldKol, kol):
        """
        Функция пересчитывает значение весового кофэфициента по старой и новой
        сумме.
        """
        
        #   Пересчитываем вес
        if oldKol <> 0 and self.metaObj.value.w_kol<>0:
            k = oldKol/self.metaObj.value.w_kol
            self.metaObj.value.w_kol = kol/k
            self.GetNameObj('edtKolPar').SetValue(self.metaObj.value.w_kol)
            self.GetNameObj('edtKolPar').Refresh()
            
    def SetSumma(self, summa):
        """
        Функция устанавливает сумму и заодно пересчитывает весовой параметр.
        """
        edt = self.GetNameObj('edtSumma')
        S0=self.metaObj.value.summa
        self.metaObj.value.summa = summa
        
        self.ReCountPar(S0, summa)
        
        edt.SetValue(summa)
        edt.Refresh()

    def SetKol(self, kol):
        """
        Функция устанавливает количество и заодно пересчитывает
        соответствующий весовой параметр.
        """
        edt = self.GetNameObj('edtKol')
        K0=self.metaObj.value.kol
        self.metaObj.value.kol = kol
        
        self.ReCountKolPar(K0, kol)
        
        edt.SetValue(kol)
        edt.Refresh()
        
    def SaveData(self, bRefresh=False):
        """
        Сохранение плана.
        """
        if self.metaObj:
            grid = self.get_plan_grid()
            decadeGrid = self.get_dec_grid()
            data = grid.dataset.data
            bChange = False
            oldS = self.metaObj.value.summa
            old_descr = self.metaObj.value.description
            #   Сохраняем основные свойства
            self.metaObj.value.summa = float(self.GetNameObj('edtSumma').GetValue())
            self.metaObj.value.w = float(self.GetNameObj('edtPar').GetValue())
            self.metaObj.value.kol = float(self.GetNameObj('edtKol').GetValue())
            self.metaObj.value.ei = self.GetNameObj('edtEI').GetValue()
            self.metaObj.value.w_kol = float(self.GetNameObj('edtKolPar').GetValue())
            self.metaObj.value.marja = float(self.GetNameObj('edtMarja').GetValue())
            self.metaObj.value.description = self.GetNameObj('edtDescription').GetValue().strip()
            #   По необходимости переименовываем
            self.metaObj.rename(self.GetNameObj('edtId').GetValue())

            #   Сохраняем декадные параметры
            decLst = map(lambda r: float(r[1]), decadeGrid.dataset.data)
            if self.metaObj.value.metatype == 'mMonth' and self.metaObj.value.decadWeight <> decLst:
                self.metaObj.value.decadWeight = decLst

            decKolLst = map(lambda r: float(r[2]), decadeGrid.dataset.data)
            if self.metaObj.value.metatype == 'mMonth' and self.metaObj.value.decadWeightKol <> decKolLst:
                self.metaObj.value.decadWeightKol = decKolLst
            
            bRefresh = self.SaveChildrenData(data, bRefresh)
                
            #   Обновляем Дерево
            if self.metaObj.value.description <> old_descr and self.tree and self.itemTree:
                self.tree.SetItemText(self.itemTree, self.metaObj.value.description, 0)

            if self.tree and self.itemTree:
                for el in self.tree.getChildLst(self.itemTree):
                    item, obj = el
                    try:
                        if self.tree.GetItemText(item) <> obj.value.description:
                            self.tree.SetItemText(item, obj.value.description, 0)
                    except:
                        pass
                
#            elif bRefresh and self.tree and self.itemTree and self.tree.IsExpanded(self.itemTree):
#                self.tree.ReLoadItemData(self.itemTree)
    
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