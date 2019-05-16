#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wx

import ic.components.icResourceParser as prs
import ic.utils.util as util
import plan.plan_service as plan_service
import plan.interfaces.ieditpanel as ieditpanel
#import NSI.spravfunc as spravfunc
from NSI import spravctrl
import ic.utils.coderror as coderror
import ic.dlg.msgbox as msgbox

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'show': 1, 'recount': None, 'keyDown': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'e5048389b79c970db02074654fdc6610', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'description': None, 'position': wx.Point(29, 64), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'2b90d4c1a3aa604058421bde947e36c3', 'proportion': 1, 'name': u'DefaultName_1896', 'alias': None, 'flag': 8192, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'child': [{'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': None, 'value': u'2006', 'font': {}, 'border': 0, 'size': (-1, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'a7c993d2027897abb7bd9276c6080610', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'edtId', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(100, 10), 'onInit': None, 'refresh': []}, {'activate': 1, 'show': 1, 'text': u'\u0421\u0443\u043c\u043c\u0430 (\u0440\u0443\u0431.)', 'keyDown': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', 'description': None, '_uuid': u'5d6e782c886b4a955cb85755b3b7c4bb', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_2145', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(10, 40), 'onInit': None}, {'activate': 1, 'show': 1, 'text': u'\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e', 'keyDown': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', 'description': None, '_uuid': u'4ea0bdbaafd07fb29c4eb65bd6011dc5', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_2145_2141', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(10, 70), 'onInit': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': None, 'value': u'2006 (\u0433\u043e\u0434\u043e\u0432\u043e\u0439 \u043f\u043b\u0430\u043d)', 'font': {}, 'border': 0, 'size': wx.Size(300, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': u'', 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'ef64abe6b274caa0d385876dceea73c0', 'moveAfterInTabOrder': u'edtId', 'flag': 0, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'edtDescription', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(311, 10), 'onInit': None, 'refresh': []}, {'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncEdtSumma(evt)', 'pic': u'999,999,999,999.99', 'hlp': None, 'value': u'', 'font': {}, 'border': 0, 'size': (-1, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'3f513ee8a8421031b6cc1d3292537738', 'moveAfterInTabOrder': u'edtDescription', 'flag': 0, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': u'', 'name': u'edtSumma', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(100, 40), 'onInit': None, 'refresh': []}, {'activate': 1, 'ctrl': u"import ic.utils.coderror as coderror\r\nimport ic.dlg.msgbox as msg\r\n\r\nif float(value) > 1:\r\n   _resultEval = coderror.IC_CTRL_FAILED_IGNORE\r\n   msg.MsgBox(self, '\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435 \u043c\u0430\u0440\u0436\u0438\u043d\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u043a\u043e\u044d\u0444\u0438\u0446\u0438\u0435\u043d\u0442\u0430 \u043d\u0435 \u043c\u043e\u0436\u0435\u0442 \u0431\u044b\u0442\u044c \u0431\u043e\u043b\u044c\u0448\u0435 1')\r\nelse:\r\n   _resultEval = coderror.IC_CTRL_OK", 'pic': u'99.9999', 'getvalue': None, 'value': u'', 'font': {}, 'border': 0, 'size': wx.Size(98, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'res_module': None, 'description': None, '_uuid': u'7a87ab611e801f255dcec1969e3f9211', 'moveAfterInTabOrder': u'recountSumma', 'flag': 0, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'edtMarja', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(280, 40), 'onInit': None, 'refresh': []}, {'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncEdtKol(evt)', 'pic': u'999,999,999.99', 'hlp': None, 'value': u'', 'font': {}, 'border': 0, 'size': (-1, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'33a169512492375f82e5d492c67f92df', 'moveAfterInTabOrder': u'edtMarja', 'flag': 0, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': u'', 'name': u'edtKol', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(100, 70), 'onInit': None, 'refresh': []}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': None, 'value': u'', 'font': {}, 'border': 0, 'size': wx.Size(80, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'res_module': None, 'description': None, '_uuid': u'4c3f125aeb216e6b04caae4d885dbecf', 'moveAfterInTabOrder': u'edtKol', 'flag': 0, 'recount': [], 'hlp': u'WrapperObj.hlpFuncEi(self, evt)', 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'edtEI', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(280, 70), 'onInit': None, 'refresh': []}, {'activate': 1, 'show': 1, 'borderRightColor': (167, 166, 152), 'child': [], 'refresh': None, 'borderWidth': 1, 'borderTopColor': (167, 166, 152), 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (18, 18), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'...', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'description': None, 'shortHelpString': u'\u041f\u043e\u043c\u043e\u0449\u044c', 'backgroundColor2': None, '_uuid': u'42b4ba795f1e1a4be2774a06ba656652', 'style': 0, 'bgrImage': None, 'flag': 0, 'recount': None, 'onLeftDown': u"res = WrapperObj.hlpFuncEi(self, evt)\r\n## print '===== INTERFACE=', GetInterface()\r\nctrl = WrapperObj.GetNameObj('edtEI')\r\n# print '========== CTRL=', ctrl, self\r\nif res[1]:\r\n    ctrl.SetValue(res[1], 1, False)\r\n", 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': None, 'name': u'edtEIHlp', 'borderBottomColor': (167, 166, 152), 'keyDown': None, 'alias': None, 'init_expr': u'#self.SetRoundCorners((1,1,1,1))\r\nself.SetButtonStyle()', 'position': wx.Point(360, 70), 'borderStyle': None, 'onInit': None}, {'activate': 1, 'show': 1, 'mouseClick': u'WrapperObj.mouseClickRecountBtn(evt)', 'font': {}, 'border': 0, 'size': wx.Size(132, 19), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041f\u0435\u0440\u0435\u0441\u0447\u0435\u0442 \u0441\u0443\u043c\u043c', 'source': u'', 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'res_module': None, 'description': None, '_uuid': u'1b2fe424e155453d286da0dda8f3c651', 'moveAfterInTabOrder': u'edtEI', 'flag': 0, 'recount': None, 'name': u'recountBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(390, 40), 'onInit': None, 'refresh': None, 'mouseContextDown': u''}, {'activate': 1, 'show': 1, 'mouseClick': u'WrapperObj.mouseClickRecountKolBtn(evt)', 'font': {}, 'border': 0, 'size': wx.Size(132, 19), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041f\u0435\u0440\u0435\u0441\u0447\u0435\u0442 \u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u0430', 'source': u'', 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'res_module': None, 'description': None, '_uuid': u'd97ffb39124e21a75bb1981b3f91bef2', 'moveAfterInTabOrder': u'recountBtn', 'flag': 0, 'recount': None, 'name': u'recountKolBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(390, 70), 'onInit': None, 'refresh': None, 'mouseContextDown': u''}, {'activate': 1, 'show': 1, 'text': u'\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043f\u043b\u0430\u043d\u0430', 'refresh': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', 'description': None, '_uuid': u'd4c9a42cd75aa8f7e5881b3683328069', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_1221', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(220, 10), 'onInit': None}, {'activate': 1, 'show': 1, 'text': u'\u0418\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440', 'refresh': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', 'description': None, '_uuid': u'4d44b5ef17b0d89e6d89be42425f2c26', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_1107', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(10, 10), 'onInit': None}, {'activate': u'1', 'show': 1, 'borderRightColor': (167, 166, 152), 'child': [], 'refresh': None, 'borderTopColor': (167, 166, 152), 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': wx.Size(50, 18), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u0415\u0434. \u0438\u0437\u043c.', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'borderWidth': 1, 'description': None, 'shortHelpString': u'\u0415\u0434\u0438\u043d\u0438\u0446\u044b \u0438\u0437\u043c\u0435\u0440\u0435\u043d\u0438\u044f \r\n\u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u0430', 'backgroundColor2': None, '_uuid': u'87c4cb9614538d1e47012f7fe692bfa5', 'style': 0, 'bgrImage': None, 'flag': 0, 'recount': None, 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': (167, 166, 152), 'name': u'HeadCell_LabelEdIzm', 'borderBottomColor': (167, 166, 152), 'keyDown': None, 'alias': None, 'init_expr': u'self.SetRoundCorners((1,1,1,1))', 'position': wx.Point(220, 70), 'borderStyle': None, 'onInit': None}, {'activate': u'1', 'show': 1, 'borderRightColor': (167, 166, 152), 'child': [], 'refresh': None, 'borderTopColor': (167, 166, 152), 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': wx.Size(50, 18), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041c\u0430\u0440\u0436\u0430', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'borderWidth': 1, 'description': None, 'shortHelpString': u'\u0414\u043e\u043b\u044f \u043c\u0430\u0440\u0436\u0438\u043d\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u0434\u043e\u0445\u043e\u0434\u0430.\r\n\u041f\u0440\u0438\u043c\u0435\u0440: 0.1 \u0441\u043e\u043e\u0442\u0432\u0435\u0442\u0441\u0442\u0432\u0443\u0435\u0442 10%\r\n\u043e\u0442 \u043f\u043b\u0430\u043d\u0438\u0440\u0443\u0435\u043c\u043e\u0439 \u0441\u0443\u043c\u043c\u044b', 'backgroundColor2': None, '_uuid': u'62ec316112fe11de6366dac6ecbf5a54', 'style': 0, 'bgrImage': None, 'flag': 0, 'recount': None, 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': (167, 166, 152), 'name': u'HeadCell_Marja', 'borderBottomColor': (167, 166, 152), 'keyDown': None, 'alias': None, 'init_expr': u'self.SetRoundCorners((1,1,1,1))', 'position': wx.Point(220, 40), 'borderStyle': None, 'onInit': None}, {'activate': u'1', 'show': 1, 'child': [], 'keyDown': None, 'border': 0, 'size': wx.Size(0, 20), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': u'# \u0412\u0441\u0442\u0430\u0432\u043b\u044f\u0435\u043c \u043f\u0430\u043d\u0435\u043b\u044c, \u0447\u0442\u043e\u0431\u044b \u0441\u0430\u0439\u0437\u0435\u0440 \u043d\u0435 \u0441\u0445\u043b\u0430\u043f\u044b\u0432\u0430\u043b \u0440\u043e\u0434\u0438\u0442\u0435\u043b\u044c\u0441\u043a\u0443\u044e\r\n# \u043f\u0430\u043d\u0435\u043b\u044c \u043a\u0443\u0434\u0430-\u043f\u043e\u043f\u0430\u043b\u043e (\u043f\u0440\u0435\u0434\u043f\u043e\u043b\u043e\u0436\u0438\u0442\u0435\u043b\u044c\u043d\u043e \u0434\u0435\u043b\u0430\u0435\u0442 \u043e\u043a\u0443\u043d\u0443 Fit) ', 'onClose': None, '_uuid': u'f6bc66adef2ec0425b6f9f5b1dabb289', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'recount': None, 'name': u'defaultWindow_1100', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(543, 80), 'onInit': None}], 'keyDown': None, 'border': 0, 'size': (200, 200), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': (186, 187, 162), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': (248, 248, 239), 'type': u'Panel', 'res_module': None, 'description': None, 'onClose': None, '_uuid': u'38c02901ed0f63c5f0aa77d3dce4caeb', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'recount': None, 'name': u'defaultWindow_1305_1488', 'refresh': None, 'alias': None, 'init_expr': u'self.SetRoundBoundMode((208, 198, 153),1)', 'position': wx.Point(0, 0), 'onInit': None}, {'line_color': (200, 200, 200), 'activate': u'0', 'show': 1, 'cols': [{'activate': 1, 'ctrl': u'WrapperObj.ctrlFunccodPlan( self.GetView(), value, row, col, evt)', 'pic': u'S', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u0434', 'width': 113, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'182f0733526295aa0befd962bdc8a4f9', 'recount': None, 'hlp': u'WrapperObj.hlpFunccodPar(evt, self.GetView(), row, col)', 'name': u'codPlan', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u041c\u0435\u0441\u044f\u0446', 'width': 140, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'8927f85b2c125736e11d45cdb5c6e9a7', 'backgroundColor': (255, 255, 255), 'font': {'style': u'boldItalic', 'name': u'defaultFont', 'family': u'sansSerif', '__attr_types__': {}, 'faceName': u'Times New Roman', 'type': u'Font', 'underline': False, 'size': 8}, 'type': u'cell_attr', 'alignment': u"('centred', 'middle')"}, 'description': None, 'shortHelpString': u'', '_uuid': u'4515d88b0254b668f7a45b8b5fcf6312', 'recount': None, 'getvalue': u'', 'name': u'descrPlan', 'setvalue': u'', 'attr': u'R', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncParam(evt)', 'pic': u'999.9999', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u044d\u0444\u0438\u0446\u0438\u0435\u043d\u0442', 'width': 113, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'c69fac0a1df2528f5884a6764d5c2c46', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': u"('right', 'middle')"}, 'description': None, 'shortHelpString': u'', '_uuid': u'182f0733526295aa0befd962bdc8a4f9', 'recount': None, 'hlp': None, 'name': u'param', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncSumma(self.GetView(), value, row, evt)', 'pic': u'999,999,999.99', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u0421\u0443\u043c\u043c\u0430', 'width': 50, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'd61d93f225ece2387776daa8c264abb0', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': u"('right', 'middle')"}, 'description': None, 'shortHelpString': u'', '_uuid': u'438b60b6ddf4acbc0168fb1f1e69c2c0', 'recount': None, 'getvalue': u'', 'name': u'summa', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncParamKol(evt)', 'pic': u'999.9999', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u043b. \u043a\u043e\u044d\u0444\u0438\u0446\u0438\u0435\u043d\u0442', 'width': 113, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'2aa3d61b8ed74acbf466c6f9d27b8daf', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': u"('right', 'middle')"}, 'description': None, 'shortHelpString': u'', '_uuid': u'182f0733526295aa0befd962bdc8a4f9', 'recount': None, 'hlp': None, 'attr': u'W', 'setvalue': u'', 'name': u'paramKol', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncKol(self.GetView(), value, row, evt)', 'pic': u'999,999,999.99', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e', 'width': 50, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'68ae5f1268b8507361110812fa6d6666', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': u"('right', 'middle')"}, 'description': None, 'shortHelpString': u'', '_uuid': u'438b60b6ddf4acbc0168fb1f1e69c2c0', 'recount': None, 'hlp': None, 'attr': u'W', 'setvalue': u'', 'name': u'kol', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u'', 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u0415\u0434. \u0438\u0437\u043c.', 'width': 50, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'68ae5f1268b8507361110812fa6d6666', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': u"('right', 'middle')"}, 'description': None, 'shortHelpString': u'', '_uuid': u'438b60b6ddf4acbc0168fb1f1e69c2c0', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'ei', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u"import ic.utils.coderror as coderror\r\nimport ic.dlg.msgbox as msg\r\n\r\nif float(value) > 1:\r\n   _resultEval = coderror.IC_CTRL_FAILED_IGNORE\r\n   msg.MsgBox(self.GetView(), '\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435 \u043c\u0430\u0440\u0436\u0438\u043d\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u043a\u043e\u044d\u0444\u0438\u0446\u0438\u0435\u043d\u0442\u0430 \u043d\u0435 \u043c\u043e\u0436\u0435\u0442 \u0431\u044b\u0442\u044c \u0431\u043e\u043b\u044c\u0448\u0435 1')\r\nelse:\r\n   _resultEval = coderror.IC_CTRL_OK", 'pic': u'99.9999', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u041c\u0430\u0440\u0436\u0430', 'width': 50, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'4b3c2cd8510b9449e111def458ca84b4', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'marja', 'keyDown': None, 'alias': None, 'init_expr': None}], 'keyDown': None, 'border': 4, 'post_select': None, 'size': (-1, -1), 'moveAfterInTabOrder': u'recountKolBtn', 'foregroundColor': None, 'span': (1, 1), 'delRec': None, 'alias': None, 'row_height': 20, 'selected': None, 'proportion': 1, 'getattr': None, 'label': u'Grid', 'source': None, 'init': u'WrapperObj.initFuncplanGrid(evt)', 'backgroundColor': None, 'fixRowSize': 0, 'type': u'GridDataset', 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'19a1d5d8b29b338019a5744f9cff420c', 'backgroundColor': None, 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'fixColSize': 0, 'description': None, 'post_del': None, 'post_init': None, '_uuid': u'65882d01f926628244804d606283c123', 'style': 0, 'docstr': u'ic.components.icgrid.html', 'flag': 8432, 'dclickEditor': None, 'recount': u'', 'label_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'a1cbc9c321890de87ae2890fa2a2a51f', 'backgroundColor': None, 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'label_attr', 'alignment': (u'left', u'middle')}, 'name': u'planGrid', 'label_height': 20, 'changed': None, 'onSize': None, 'component_module': None, 'init_expr': u'', 'position': wx.Point(18, 18), 'onInit': u'', 'refresh': None}, {'LabelBgrColor': (247, 245, 234), 'activate': 1, 'LabelBorderColor': (208, 198, 153), 'border': 0, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'delRec': None, 'component_module': None, 'proportion': 1, 'init': u'WrapperObj.initFuncplanGrid(evt)', 'scheme': u'STD', 'type': u'StdDataGrid', 'LabelFgrColor': (0, 0, 0), 'description': None, 'nest': u'GridDataset:DataGrid', '_uuid': u'03bc0fcecabf6da5954f32e6a1500fe1', 'flag': 8192, 'child': [{'activate': 1, 'ctrl': u'WrapperObj.ctrlFunccodPlan( self.GetView(), value, row, col, evt)', 'pic': u'S', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u0434', 'width': 73, 'init': None, 'valid': None, 'type': u'GridCell', 'res_module': None, 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'182f0733526295aa0befd962bdc8a4f9', 'recount': None, 'hlp': u'WrapperObj.hlpFunccodPar(evt, self.GetView(), row, col)', 'attr': u'W', 'setvalue': u'', 'name': u'codPlan', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u041c\u0435\u0441\u044f\u0446', 'width': 86, 'init': None, 'valid': None, 'type': u'GridCell', 'res_module': None, 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'8927f85b2c125736e11d45cdb5c6e9a7', 'backgroundColor': (255, 255, 255), 'font': {'style': u'boldItalic', 'name': u'defaultFont', 'family': u'sansSerif', '__attr_types__': {}, 'faceName': u'Times New Roman', 'type': u'Font', 'underline': False, 'size': 8}, 'type': u'cell_attr', 'alignment': u"('centred', 'middle')"}, 'description': None, 'shortHelpString': u'', '_uuid': u'4515d88b0254b668f7a45b8b5fcf6312', 'recount': None, 'hlp': None, 'attr': u'R', 'setvalue': u'', 'name': u'descrPlan', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncParam(evt)', 'pic': u'999.9999', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u044d\u0444\u0438\u0446\u0438\u0435\u043d\u0442', 'width': 87, 'init': None, 'valid': None, 'type': u'GridCell', 'res_module': None, 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'c69fac0a1df2528f5884a6764d5c2c46', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': u"('right', 'middle')"}, 'description': None, 'shortHelpString': u'', '_uuid': u'182f0733526295aa0befd962bdc8a4f9', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'param', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncSumma(self.GetView(), value, row, evt)', 'pic': u'999,999,999.99', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u0421\u0443\u043c\u043c\u0430', 'width': 84, 'init': None, 'valid': None, 'type': u'GridCell', 'res_module': None, 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'd61d93f225ece2387776daa8c264abb0', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': u"('right', 'middle')"}, 'description': None, 'shortHelpString': u'', '_uuid': u'438b60b6ddf4acbc0168fb1f1e69c2c0', 'recount': None, 'hlp': None, 'attr': u'W', 'setvalue': u'', 'name': u'summa', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncParamKol(evt)', 'pic': u'999.9999', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u043b. \u043a\u043e\u044d\u0444\u0438\u0446\u0438\u0435\u043d\u0442', 'width': 104, 'init': None, 'valid': None, 'type': u'GridCell', 'res_module': None, 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'2aa3d61b8ed74acbf466c6f9d27b8daf', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': u"('right', 'middle')"}, 'description': None, 'shortHelpString': u'', '_uuid': u'182f0733526295aa0befd962bdc8a4f9', 'recount': None, 'getvalue': u'', 'name': u'paramKol', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncKol(self.GetView(), value, row, evt)', 'pic': u'999,999,999.99', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e', 'width': 77, 'init': None, 'valid': None, 'type': u'GridCell', 'res_module': None, 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'68ae5f1268b8507361110812fa6d6666', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': u"('right', 'middle')"}, 'description': None, 'shortHelpString': u'', '_uuid': u'438b60b6ddf4acbc0168fb1f1e69c2c0', 'recount': None, 'hlp': None, 'attr': u'W', 'setvalue': u'', 'name': u'kol', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u'', 'pic': u'S', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u0415\u0434. \u0438\u0437\u043c.', 'width': 103, 'init': None, 'valid': None, 'type': u'GridCell', 'res_module': None, 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'68ae5f1268b8507361110812fa6d6666', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': u"('right', 'middle')"}, 'description': None, 'shortHelpString': u'', '_uuid': u'438b60b6ddf4acbc0168fb1f1e69c2c0', 'recount': None, 'hlp': u'WrapperObj.hlpFuncEi(self.GetView(), evt)', 'name': u'ei', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u"import ic.utils.coderror as coderror\r\nimport ic.dlg.msgbox as msg\r\n\r\nif float(value) > 1:\r\n   _resultEval = coderror.IC_CTRL_FAILED_IGNORE\r\n   msg.MsgBox(self.GetView(), '\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435 \u043c\u0430\u0440\u0436\u0438\u043d\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u043a\u043e\u044d\u0444\u0438\u0446\u0438\u0435\u043d\u0442\u0430 \u043d\u0435 \u043c\u043e\u0436\u0435\u0442 \u0431\u044b\u0442\u044c \u0431\u043e\u043b\u044c\u0448\u0435 1')\r\nelse:\r\n   _resultEval = coderror.IC_CTRL_OK", 'pic': u'99.9999', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u041c\u0430\u0440\u0436\u0430', 'width': 99, 'init': None, 'valid': None, 'type': u'GridCell', 'res_module': None, 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'4b3c2cd8510b9449e111def458ca84b4', 'recount': None, 'hlp': None, 'name': u'marja', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}], 'name': u'planGridPanel', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1)}, {'style': 0, 'activate': u'1', 'span': (1, 1), 'description': None, 'component_module': None, 'border': 0, '_uuid': u'60880469bdcec6ddf80df4fd491896d4', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'size': (0, 0), 'type': u'SizerSpace', 'name': u'DefaultName_4366_4641_1523'}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'name': u'edtPanel', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(104, 0), 'onInit': u'WrapperObj.OnInitFuncedtPanel(evt)'}

#   Версия объекта
__version__ = (1, 1, 1, 1)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'IYearEdtPanel'

COL_GRID_KEY = ieditpanel.COL_GRID_KEY


class IYearEdtPanel(ieditpanel.IEdtPanel):
    def __init__(self, parent, metaYearObj=None, tree=None):
        """
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type metaYearObj: C{icMetaItem}
        @param metaYearObj: Указатель на метаобъект годового плана.
        @type tree: C{ic.components.user.ictreelistctrl.icTreeListCtrl}
        @param tree: Указатель на дерево планов.
        """
        self._data = None
        self.summa = None
        ieditpanel.IEdtPanel.__init__(self, parent, resource, metaYearObj, tree)

    def get_plan_grid(self):
        """
        Возвращает указатель на грид планирования.
        """
        return self.GetNameObj('edtPanel').GetContext().GetInterface('planGridPanel').get_grid()

    def LoadChildData(self):
        """
        Загружаем данные по дочерним планам.
        """
        if self.metaObj:
            grid = self.get_plan_grid()
            lst = self.metaObj.keys()
            lst.sort()
            
            # --- Коэфициенты элементов планов
            self._data = range(len(lst))
            for i, key in enumerate(lst):
                obj = self.metaObj[key]
                self._data[i] = [key, obj.value.description,
                                 obj.value.w, obj.value.summa,
                                 obj.value.w_kol, obj.value.kol,
                                 obj.value.ei, obj.value.marja, key]

            grid.dataset.SetDataBuff(self._data)
            grid.RefreshGrid()
                
            return self._data
        
    def LoadData(self):
        """
        Загружаем данные по планам.
        """
        if self.metaObj:
            descr = self.GetNameObj('edtDescription')
            edtId = self.GetNameObj('edtId')
            edtSumma = self.GetNameObj('edtSumma')
            edtKol = self.GetNameObj('edtKol')
            edtEI = self.GetNameObj('edtEI')
            
            self.summa = self.metaObj.value.summa
            self.kol = self.metaObj.value.kol
            self.ei = self.metaObj.value.ei
            descr.SetValue(self.metaObj.value.description)
            edtId.SetValue(self.metaObj.value.name)
            edtSumma.SetValue(self.summa)
            edtKol.SetValue(self.kol)
            edtEI.SetValue(self.ei)
            self.GetNameObj('edtMarja').SetValue(self.metaObj.value.marja)
            self.LoadChildData()
            return self._data
    
    ###BEGIN EVENT BLOCK
    
    def OnInitFuncedtPanel(self, evt):
        """
        Функция обрабатывает событие <?>.
        """
        grid = self.get_plan_grid()
        self.LoadData()
        
        if self._data:
            grid.dataset.SetDataBuff(self._data)

        # self.ReCount()
        return None
    
    def initFuncplanGrid(self, evt):
        """
        Функция обрабатывает событие <?>.
        """
        return False
    
    def mouseClickRecountBtn(self, evt):
        """
        Функция обрабатывает событие <mouseClick>.
        Производим пересчет сумм с учетом весовых коэфициентов.
        """
        self.ReCount()

    def mouseClickRecountKolBtn(self, evt):
        """
        Функция обрабатывает событие <mouseClick>.
        Производим пересчет сумм с учетом весовых коэфициентов.
        """
        self.ReCountKol()
    
    def ctrlFuncSumma(self, grid, value, row, evt):
        """
        Функция контроля на изменения поля <summa> грида.
        """
        key = grid.dataset.data[row][0]
        
        if self.metaObj and self.metaObj.isMyLock() and key and key in self.metaObj:
            edt = self.GetNameObj('edtSumma')
            data = grid.dataset.data
    
            #   Вычисляем сумму весов без текущей строки
            S = 0
            for i, r in enumerate(data):
                if i != row:
                    S += float(r[3])
            
            #   Определяем параметр в гриде
            if self.metaObj[key].value.summa != 0 and self.metaObj[key].value.w != 0:
                data[row][2] = value/(self.metaObj[key].value.summa/self.metaObj[key].value.w)
            else:
                data[row][2] = 1

            self.metaObj[key].value.summa = float(value)
            edt.SetValue(S+value)
            edt.Refresh()
            self.ReCount()

    def ctrlFuncKol(self, grid, value, row, evt):
        """
        Функция контроля на изменения поля <summa> грида.
        """
        key = grid.dataset.data[row][0]
        
        if self.metaObj and self.metaObj.isMyLock() and key and self.metaObj.has_key(key):
            edt = self.GetNameObj('edtKol')
            data = grid.dataset.data
    
            #   Вычисляем сумму весов без текущей строки
            S = 0
            for i, r in enumerate(data):
                if i != row:
                    S += float(r[5])
            
            #   Определяем параметр в гриде
            if self.metaObj[key].value.kol != 0 and self.metaObj[key].value.w_kol != 0:
                data[row][4] = value/(self.metaObj[key].value.kol/self.metaObj[key].value.w_kol)
            else:
                data[row][4] = 1

            self.metaObj[key].value.kol = float(value)
            edt.SetValue(S+value)
            edt.Refresh()
            self.ReCountKol()

    def ctrlFunccodPlan(self, grid, value, row, col, evt):
        """
        Контроль поля кода плана <codPlan>.
        """
        if value in [r[0] for r in grid.dataset.data]:
            prnt = self.GetNameObj('edtPanel')
            msgbox.MsgBox(prnt, u'Элемент плана уже введен')
            return coderror.IC_CTRL_FAILED_IGNORE
        try:
            key = grid.dataset.data[row][COL_GRID_KEY]
            obj = self.metaObj[key]
            return spravctrl.CtrlSprav(obj.value.sprav, value, field='cod', flds={'descrPlan': 'name'})
        except:
            return coderror.IC_CTRL_FAILED_IGNORE
    
    def ctrlFuncParam(self, evt):
        """
        Функция обрабатывает событие <Ctrl на поле коэфициента>.
        """
        grid = self.get_plan_grid()
        data = grid.dataset.data
        row = grid.GetGridCursorRow()
        val = float(grid.evalSpace['value'])
        data[row][2] = val
        self.ReCount()
        return None

    def ctrlFuncParamKol(self, evt):
        """
        Функция обрабатывает событие <Ctrl на поле коэфициента>.
        """
        grid = self.get_plan_grid()
        data = grid.dataset.data
        row = grid.GetGridCursorRow()
        val = float(grid.evalSpace['value'])
        data[row][4] = val
        self.ReCountKol()
        return None
    
    def ctrlFuncEdtSumma(self, evt):
        """
        Функция обрабатывает событие <?>.
        """
        self.ReCount()

    def ctrlFuncEdtKol(self, evt):
        """
        Функция обрабатывает событие <?>.
        """
        self.ReCountKol()
    
    def hlpFunccodPar(self, evt, grid, row, col):
        """
        Функция обрабатывает запрос на подсказку по <F1> на поле кода
        элемента плана грида.
        """
        key = grid.dataset.data[row][COL_GRID_KEY]
        
        if self.metaObj and self.metaObj.isMyLock() and key and self.metaObj.has_key(key):
            obj = self.metaObj[key]
            prnt = self.GetNameObj('edtPanel')
            ret = spravctrl.HlpSprav(obj.value.sprav,
                                     field={'descrPlan': 'name', 'cod': 'cod'}, parentForm=grid)
            return ret
        
        return None

    def hlpFuncEi(self, grid, evt):
        """
        Функция обрабатывает событие <hlp> на GridCell <ei>.
        """
        sprav = spravctrl.getSprav('Edizm')
        ret = sprav.Hlp(ParentCode=(None,),
                        field={'ei': 'name'}, parentForm=grid)
        
        try:
            if ret[2]:
                return ret[0], ret[2]['ei'], None
        except IndexError:
            # print '<ESCAPE>'
            return ret
        except TypeError:
            # print '<ESCAPE>'
            return ret

        return ret
        
    ###END EVENT BLOCK
    
    def SaveData(self, bRefresh=False):
        """
        Сохранение плана.
        """
        if self.metaObj and self.metaObj.isMyLock():
            edt = self.GetNameObj('edtSumma')
            descr = self.GetNameObj('edtDescription').GetValue()
            grid = self.get_plan_grid()
            data = grid.dataset.data
            oldS = self.metaObj.value.summa
            old_descr = self.metaObj.value.description
            
            #   Сохраняем параметры годового плана
            self.metaObj.value.summa = float(edt.GetValue())
            self.metaObj.value.kol = float(self.GetNameObj('edtKol').GetValue())
            self.metaObj.value.ei = self.GetNameObj('edtEI').GetValue()
            self.metaObj.value.marja = float(self.GetNameObj('edtMarja').GetValue())
            self.metaObj.value.description = descr.strip()
            #   По необходимости переименовываем объект
            self.metaObj.rename(self.GetNameObj('edtId').GetValue())
            bRefresh = self.SaveChildrenData(data, bRefresh)

            #   Обновляем Дерево
            if self.metaObj.value.description != old_descr and self.tree and self.itemTree:
                self.tree.SetItemText(self.itemTree, self.metaObj.value.description, 0)

            if self.tree and self.itemTree:
                for el in self.tree.getChildLst(self.itemTree):
                    item, obj = el
                    try:
                        if self.tree.GetItemText(item) != obj.value.description:
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
