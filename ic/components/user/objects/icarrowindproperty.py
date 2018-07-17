#!/usr/bin/env python
# -*- coding: utf-8 -*-


import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.utils.coderror as coderror
import ic.dlg.msgbox as msgbox

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource = {'activate': 1, 'show': 1, 'child': [{'activate': 1, 'show': 1, 'borderRightColor': (0, 0, 160), 'child': [{'activate': 1, 'show': 1, 'borderRightColor': (100, 100, 100), 'recount': None, 'keyDown': None, 'borderTopColor': (250, 250, 250), 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': wx.Size(34, 16), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'label': u'', 'source': None, 'backgroundColor': (30, 183, 102), 'isSort': False, 'type': u'HeadCell', 'init_expr': None, 'shortHelpString': u'', '_uuid': u'abb7d3ce2f38dcf6f97d76bace13f972', 'style': 0, 'flag': 0, 'child': [], 'cursorColor': (100, 100, 100), 'borderStyle': None, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'GreenZone', 'borderBottomColor': (100, 100, 100), 'refresh': None, 'alias': None, 'borderWidth': 1, 'position': wx.Point(15, 70), 'backgroundType': 1}, {'activate': 1, 'show': 1, 'borderRightColor': (100, 100, 100), 'child': [], 'refresh': None, 'borderTopColor': (250, 250, 250), 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': wx.Size(34, 16), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'label': u'', 'source': None, 'backgroundColor': (244, 181, 11), 'isSort': False, 'type': u'HeadCell', 'borderWidth': 1, 'shortHelpString': u'', '_uuid': u'bffc7413daf0770f0db4d8b3cc59650a', 'style': 0, 'flag': 0, 'recount': None, 'cursorColor': (100, 100, 100), 'backgroundType': 1, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'YellowZone', 'borderBottomColor': (100, 100, 100), 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(15, 50), 'borderStyle': None}, {'activate': 1, 'show': 1, 'borderRightColor': (100, 100, 100), 'child': [], 'refresh': None, 'borderTopColor': (250, 250, 250), 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': wx.Size(34, 16), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'label': u'', 'source': None, 'backgroundColor': (174, 0, 87), 'isSort': False, 'type': u'HeadCell', 'borderWidth': 1, 'shortHelpString': u'', '_uuid': u'f19ba244b9c33a4596c3146f20b2a27f', 'style': 0, 'flag': 0, 'recount': None, 'cursorColor': (100, 100, 100), 'backgroundType': 1, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'RedZone', 'borderBottomColor': (100, 100, 100), 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(15, 30), 'borderStyle': None}, {'activate': 1, 'show': 1, 'borderRightColor': (100, 100, 100), 'recount': None, 'keyDown': None, 'borderTopColor': (250, 250, 250), 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': wx.Size(34, 16), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'label': u'', 'source': None, 'backgroundColor': (244, 181, 11), 'isSort': False, 'type': u'HeadCell', 'init_expr': None, 'shortHelpString': u'', '_uuid': u'f9169b0a86773929448d54ca474026df', 'style': 0, 'flag': 0, 'child': [], 'cursorColor': (100, 100, 100), 'borderStyle': None, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'YellowZone2', 'borderBottomColor': (100, 100, 100), 'refresh': None, 'alias': None, 'borderWidth': 1, 'position': (15, 90), 'backgroundType': 1}, {'activate': 1, 'show': 1, 'borderRightColor': (100, 100, 100), 'recount': None, 'keyDown': None, 'borderTopColor': (250, 250, 250), 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': wx.Size(34, 16), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'label': u'', 'source': None, 'backgroundColor': (174, 0, 87), 'isSort': False, 'type': u'HeadCell', 'init_expr': None, 'shortHelpString': u'', '_uuid': u'435647ff7459770830ecfe2625fb07db', 'style': 0, 'flag': 0, 'child': [], 'cursorColor': (100, 100, 100), 'borderStyle': None, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'RedZone2', 'borderBottomColor': (100, 100, 100), 'refresh': None, 'alias': None, 'borderWidth': 1, 'position': wx.Point(15, 110), 'backgroundType': 1}, {'activate': 1, 'show': 1, 'text': u'\u041d\u0438\u0436\u043d\u044f\u044f \u043e\u043f\u0430\u0441\u043d\u0430\u044f \u0437\u043e\u043d\u0430 (%)', 'refresh': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (0, 0, 160), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'8c57d8188cd448de2b88ebe97e5125f5', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'redText', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(70, 30)}, {'activate': 1, 'show': 1, 'text': u'\u041d\u0438\u0436\u043d\u044f\u044f \u043f\u0435\u0440\u0435\u0445\u043e\u0434\u043d\u0430\u044f \u0437\u043e\u043d\u0430 (%)', 'refresh': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (0, 0, 160), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'b1e60d7d6942e9d45e3f24345f86ad5f', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'yellowText', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (70, 50)}, {'activate': 1, 'show': 1, 'text': u'\u041f\u043b\u0430\u043d\u043e\u0432\u0430\u044f \u0437\u043e\u043d\u0430 (%)', 'refresh': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (0, 0, 160), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'a1d1510fd3f146572e94d19bf9edbb45', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'greenText', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(70, 70)}, {'activate': 1, 'show': 1, 'text': u'\u0412\u0435\u0440\u0445\u043d\u044f\u044f \u043f\u0435\u0440\u0435\u0445\u043e\u0434\u043d\u0430\u044f \u0437\u043e\u043d\u0430 (%)', 'refresh': None, 'font': {}, 'border': 0, 'size': wx.Size(148, 13), 'style': 0, 'foregroundColor': (0, 0, 160), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'9451e8641b29c24fb9842dca895bb507', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'yellowText2', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(70, 90)}, {'activate': 1, 'show': 1, 'text': u'\u0412\u0435\u0440\u0445\u043d\u044f\u044f \u043e\u043f\u0430\u0441\u043d\u0430\u044f \u0437\u043e\u043d\u0430 (%)', 'refresh': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (0, 0, 160), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'0e53a7e96c588e0cfba33c775b00ec00', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'redText2', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(70, 110)}, {'activate': 1, 'show': 1, 'keyDown': None, 'font': {}, 'border': 0, 'size': (50, 18), 'style': 33562624, 'foregroundColor': None, 'span': (1, 1), 'min': 0, 'proportion': 0, 'source': None, 'init': None, 'backgroundColor': None, 'type': u'Spinner', 'loseFocus': None, 'max': 100, '_uuid': u'9bf2cee3642071aae6ba6caaa7736dd9', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'field_name': None, 'setFocus': None, 'name': u'redSpinner', 'value': 30, 'alias': None, 'onSpin': None, 'init_expr': None, 'position': (225, 30), 'refresh': []}, {'activate': 1, 'show': 1, 'value': 40, 'font': {}, 'border': 0, 'size': (50, 18), 'style': 33562624, 'foregroundColor': None, 'span': (1, 1), 'min': 0, 'proportion': 0, 'source': None, 'init': None, 'backgroundColor': None, 'type': u'Spinner', 'loseFocus': None, 'max': 100, '_uuid': u'1abc26b127ff12ae92c08ee8783f9b79', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'field_name': None, 'setFocus': None, 'name': u'yellowSpinner', 'keyDown': None, 'alias': None, 'onSpin': None, 'init_expr': None, 'position': (225, 50), 'refresh': []}, {'activate': 1, 'show': 1, 'keyDown': None, 'font': {}, 'border': 0, 'size': (50, 18), 'style': 33562624, 'foregroundColor': None, 'span': (1, 1), 'min': 0, 'proportion': 0, 'source': None, 'init': None, 'backgroundColor': None, 'type': u'Spinner', 'loseFocus': None, 'max': 100, '_uuid': u'48eb3d7be5c62a333c8e1b21d79e053a', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'field_name': None, 'setFocus': None, 'name': u'greenSpinner', 'value': 60, 'alias': None, 'onSpin': None, 'init_expr': None, 'position': (225, 70), 'refresh': []}, {'activate': 1, 'show': 1, 'value': 70, 'font': {}, 'border': 0, 'size': (50, 18), 'style': 33562624, 'foregroundColor': None, 'span': (1, 1), 'min': 0, 'proportion': 0, 'source': None, 'init': None, 'backgroundColor': None, 'type': u'Spinner', 'loseFocus': None, 'max': 100, '_uuid': u'8cf4efdc6e723b580fea6bbd10772d3e', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'field_name': None, 'setFocus': None, 'name': u'yellowSpinner2', 'keyDown': None, 'alias': None, 'onSpin': None, 'init_expr': None, 'position': (225, 90), 'refresh': []}, {'activate': 1, 'show': 1, 'keyDown': None, 'font': {}, 'border': 0, 'size': (50, 18), 'style': 33562624, 'foregroundColor': None, 'span': (1, 1), 'min': 0, 'proportion': 0, 'source': None, 'init': None, 'backgroundColor': None, 'type': u'Spinner', 'loseFocus': None, 'max': 100, '_uuid': u'32d95fc856a4c837c3195bfd93658f3d', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'field_name': None, 'setFocus': None, 'name': u'redSpinner2', 'value': 100, 'alias': None, 'onSpin': None, 'init_expr': u'self.Enable(False)', 'position': (225, 110), 'refresh': []}, {'activate': 1, 'show': 1, 'mouseClick': u'WrapperObj.OnRefresh(evt)', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'label': u'\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'08f91f69e6ad14121687b81b013176fc', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'refreshBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(330, 113), 'refresh': None, 'mouseContextDown': None}], 'refresh': None, 'borderTopColor': (0, 0, 160), 'font': {}, 'border': 0, 'alignment': u"('left', 'top')", 'size': wx.Size(412, 141), 'moveAfterInTabOrder': u'', 'foregroundColor': (0, 0, 160), 'span': (1, 1), 'proportion': 0, 'label': u' \u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0430 \u0446\u0432\u0435\u0442\u043e\u0432\u044b\u0445 \u0437\u043e\u043d \u0438\u043d\u0434\u0438\u043a\u0430\u0442\u043e\u0440\u0430', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'borderWidth': 1, 'shortHelpString': u'', '_uuid': u'7d23ffd61c2eeceed71a59f928a2dcc3', 'style': 0, 'flag': 0, 'recount': None, 'cursorColor': (100, 100, 100), 'borderStyle': u'wx.DOT', 'borderStep': 0, 'borderLeftColor': (0, 0, 160), 'name': u'HeadCell_4864_1548', 'borderBottomColor': (0, 0, 160), 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(4, 305), 'backgroundType': 0}, {'majorValues': u'range(101)[0::10]', 'activate': 1, 'ei': u'', 'show': 1, 'onSaveProperty': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': wx.Size(411, 65), 'moveAfterInTabOrder': u'', 'onColor': None, 'layout': u'horizontal', 'proportion': 0, 'dateIzm': u'', 'onGraph': None, 'label': u'\u041f\u043e\u0434\u043f\u0438\u0441\u044c', 'colorRegions': u"[('100%', 'BLUE')]", 'source': None, 'backgroundColor': None, 'factor': 1, 'type': u'ArrowIndicator', 'majorLabels': u"r = range(101)[0::10]\r\nr[5] = '\u041f\u043b\u0430\u043d'\r\n_resultEval = r", 'minorValues': u'range(101)[0::5]', 'shortHelpString': u'\u0418\u043d\u0434\u0438\u043a\u0430\u0442\u043e\u0440', '_uuid': u'74a4c6b9e6882615aaa0bb2c98a3b3b1', 'style': 0, 'aggregationType': u'USUAL', 'attrVal': None, 'flag': 0, 'foregroundColor': None, 'recount': None, 'span': (1, 1), 'attrPlan': None, 'name': u'indicator', 'value': None, 'alias': None, 'aggregationFunc': u'SUM', 'init_expr': u'self.SetTypePredst(0)', 'position': wx.Point(5, 450), 'refresh': None}, {'activate': 1, 'show': 1, 'text': u'\u041c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u043e\u0435 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435', 'refresh': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'794a0373c996178332d70d53b2c8b4f2', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_2472', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(15, 15)}, {'activate': 1, 'ctrl': None, 'pic': u'N', 'hlp': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': wx.Size(60, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', '_uuid': u'4caa4f39f9c354ccb46064b89a655f76', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'minVal', 'changed': None, 'value': u'0', 'alias': None, 'init_expr': None, 'position': wx.Point(145, 15), 'refresh': []}, {'activate': 1, 'show': 1, 'text': u'\u041c\u0430\u043a\u0441\u0438\u043c\u0430\u043b\u044c\u043d\u043e\u0435 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435', 'refresh': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'c618e979d831a34f7cbf4fd853c2ba9e', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_2513', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(220, 15)}, {'activate': 1, 'ctrl': None, 'pic': u'9999', 'getvalue': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': wx.Size(60, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', '_uuid': u'3ffc337cd5ff837b4c6e7e5c5a75131b', 'moveAfterInTabOrder': u'minVal', 'flag': 0, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'maxVal', 'changed': None, 'value': u'100', 'alias': None, 'init_expr': None, 'position': wx.Point(355, 15), 'refresh': []}, {'activate': 1, 'show': 1, 'text': u'\u041f\u043e\u0434\u043f\u0438\u0441\u044c \u0433\u0440\u0430\u0444\u0438\u043a\u0430', 'refresh': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'3dbbe4002b35bbba7bcd21cde47d8c89', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_1190', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(15, 83)}, {'activate': 1, 'show': 1, 'text': u'\u0428\u0430\u0433 \u043c\u0430\u0436\u043e\u0440\u043d\u043e\u0439 \u0441\u0435\u0442\u043a\u0438', 'refresh': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'c39c0aa7c0169f9ea7b4d1f6851fd98f', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_1239', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(15, 37)}, {'activate': 1, 'show': 1, 'text': u'\u0428\u0430\u0433 \u043c\u0438\u043d\u043e\u0440\u043d\u043e\u0439 \u0441\u0435\u0442\u043a\u0438', 'refresh': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'598034cfd64e6ea6812a0d37eeb7ccc3', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_1265', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(220, 37)}, {'activate': 1, 'ctrl': None, 'pic': u'99999.99', 'getvalue': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': wx.Size(60, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', '_uuid': u'c2e95951051a2bc73e69bd61e85f79eb', 'moveAfterInTabOrder': u'maxVal', 'flag': 0, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'majorStep', 'changed': None, 'value': u'10', 'alias': None, 'init_expr': None, 'position': wx.Point(145, 37), 'refresh': []}, {'activate': 1, 'ctrl': None, 'pic': u'99999.99', 'getvalue': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': wx.Size(60, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', '_uuid': u'85bf0a6dc2f711725d2fa3c1b5c038d9', 'moveAfterInTabOrder': u'majorStep', 'flag': 0, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'minorStep', 'changed': None, 'value': u'5', 'alias': None, 'init_expr': None, 'position': wx.Point(355, 37), 'refresh': []}, {'activate': 1, 'show': 1, 'text': u'\u0415\u0434\u0438\u043d\u0438\u0446\u044b \u0438\u0437\u043c\u0435\u0440\u0435\u043d\u0438\u044f', 'refresh': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'c39d5e142d6fa9ffde4b01ebb6290631', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_2840', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(15, 60)}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': wx.Size(60, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', '_uuid': u'6f6ee24097a69b7db6931bd0100636a4', 'moveAfterInTabOrder': u'minorStep', 'flag': 0, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'eiEdt', 'changed': None, 'value': u'', 'alias': None, 'init_expr': None, 'position': wx.Point(145, 60), 'refresh': []}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': None, 'value': u'\u041f\u043e\u0434\u043f\u0438\u0441\u044c \u0433\u0440\u0430\u0444\u0438\u043a\u0430', 'font': {}, 'border': 0, 'size': wx.Size(270, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', '_uuid': u'30202ae735be480cd1f685eeadc15c98', 'moveAfterInTabOrder': u'factor', 'flag': 0, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'labelGraph', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(145, 83), 'refresh': []}, {'activate': 1, 'ctrl': None, 'pic': u'9999999999', 'getvalue': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': wx.Size(60, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', '_uuid': u'289d7a2cfda63b638d97d90208577d27', 'moveAfterInTabOrder': u'eiEdt', 'flag': 0, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': u'', 'name': u'factor', 'changed': None, 'value': u'1', 'alias': None, 'init_expr': None, 'position': wx.Point(355, 60), 'refresh': []}, {'activate': 1, 'show': 1, 'text': u'\u0422\u0430\u0431\u043b\u0438\u0446\u0430', 'refresh': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'ef7a36a36eae152d4cb6f0283b18bd4c', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_1399', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(15, 115)}, {'activate': 1, 'show': 1, 'value': u'', 'font': {}, 'border': 0, 'size': (110, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': (255, 255, 255), 'type': u'ComboBox', '_uuid': u'2ff036726913f53ef4027649ff43a48d', 'moveAfterInTabOrder': u'labelGraph', 'flag': 0, 'recount': None, 'name': u'tableNameEdt', 'items': [], 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(115, 115), 'refresh': None}, {'activate': 1, 'show': 1, 'keyDown': None, 'font': {}, 'border': 0, 'size': (110, 20), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': (255, 255, 255), 'type': u'ComboBox', '_uuid': u'7899765cbff6f792f895cd784b18c5cd', 'moveAfterInTabOrder': u'tableNameEdt', 'flag': 0, 'recount': None, 'name': u'valAttrNameEdt', 'items': u"['summa', 'kolf']", 'value': u'', 'alias': None, 'init_expr': None, 'position': wx.Point(115, 145), 'refresh': None}, {'activate': 1, 'show': 1, 'value': u'', 'font': {}, 'border': 0, 'size': wx.Size(90, 21), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': (255, 255, 255), 'type': u'ComboBox', '_uuid': u'47af5be314ba51b344b79bca1cd340e8', 'moveAfterInTabOrder': u'valAttrNameEdt', 'flag': 0, 'recount': None, 'name': u'planAttrNameEdt', 'items': [u'plan_sum', u'plan_kol'], 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(324, 143), 'refresh': None}, {'activate': 1, 'show': 1, 'text': u'\u0410\u0442\u0440\u0438\u0431\u0443\u0442 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f', 'refresh': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'7eca83807488b9f664108a317117aa73', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_1865', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(15, 145)}, {'activate': 1, 'show': 1, 'text': u'\u0410\u0442\u0440\u0438\u0431\u0443\u0442 \u043f\u043b\u0430\u043d\u0430', 'refresh': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'9f8ed794c12bfae7425b1d8682a7523c', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_1904', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(240, 146)}, {'activate': 1, 'show': 1, 'text': u'\u041c\u043d\u043e\u0436\u0438\u0442\u0435\u043b\u044c', 'refresh': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'2640256c9c59b0c577bd8c619fb4fc68', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_1249', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(223, 60)}, {'activate': 1, 'show': 1, 'mouseClick': u'WrapperObj.OnSave(evt)', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'label': u'\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'72259d26ba1724e8580343ccaedeba1f', 'moveAfterInTabOrder': u'aggregFuncChoice', 'flag': 0, 'recount': None, 'name': u'btnSave', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(142, 521), 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'show': 1, 'mouseClick': u'WrapperObj.OnCancel(evt)', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'label': u'\u041e\u0442\u043c\u0435\u043d\u0430', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'c07fa73f511a79cab2e835d396fac47c', 'moveAfterInTabOrder': u'btnSave', 'flag': 0, 'recount': None, 'name': u'btnCancel', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(227, 521), 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'show': 1, 'text': u'\u0422\u0438\u043f \u043d\u0430\u043a\u043e\u043f\u043b\u0435\u043d\u0438\u044f', 'refresh': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'99b4976b69e912eb67a98018e3969077', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_2698', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(15, 175)}, {'activate': 1, 'show': 1, 'keyDown': None, 'border': 0, 'size': (110, -1), 'style': 33555520, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': (255, 255, 255), 'type': u'Choice', 'loseFocus': None, '_uuid': u'33aed8ee7ad002350df9d36a2047571d', 'moveAfterInTabOrder': u'planAttrNameEdt', 'choice': None, 'flag': 0, 'recount': [], 'field_name': None, 'setFocus': None, 'name': u'aggregTypeChoice', 'items': None, 'refresh': [], 'alias': None, 'init_expr': u"dct = _dict_obj['indicator'].GetAggregationTypeDict()\r\nlst = dct.keys()\r\nlst.sort()\r\nself.setChoiceList(lst)\r\n", 'position': (115, 175)}, {'activate': 1, 'show': 1, 'text': u'\u0424\u0443\u043d\u043a. \u043d\u0430\u043a\u043e\u043f\u043b.', 'refresh': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'ab3910ad25d23e2a2eff20d21a49ccd4', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_1165', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(240, 175)}, {'activate': 1, 'show': 1, 'refresh': [], 'border': 0, 'size': wx.Size(90, 21), 'style': 33555520, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': (255, 255, 255), 'type': u'Choice', 'loseFocus': None, '_uuid': u'59c0fdd3aae45a05e86d1bfaaaadfc32', 'moveAfterInTabOrder': u'aggregTypeChoice', 'choice': None, 'flag': 0, 'recount': [], 'field_name': None, 'setFocus': None, 'name': u'aggregFuncChoice', 'items': None, 'keyDown': None, 'alias': None, 'init_expr': u"dct = _dict_obj['indicator'].GetAggregationFuncDict()\r\nlst = dct.keys()\r\nlst.sort()\r\nself.setChoiceList(lst)\r\n", 'position': wx.Point(325, 175)}, {'activate': 1, 'show': 1, 'text': u'\u0423\u0441\u043b\u043e\u0432\u0438\u0435 \u0433\u0440\u0443\u043f\u043f\u0438\u0440\u043e\u0432\u043a\u0438', 'refresh': None, 'font': {}, 'border': 0, 'size': wx.Size(82, 34), 'style': 1, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'5c516b92a0f47f1fdc1dc2f271a8c113', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_1241', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(15, 205)}, {'activate': 1, 'ctrl': u'WrapperObj.OnGroupConditionCtrl(value)', 'pic': u'S', 'hlp': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': wx.Size(300, 72), 'style': 32, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', '_uuid': u'75d2525da9b7c12578d066eba8f2f429', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'groupCondition', 'changed': None, 'value': u'', 'alias': None, 'init_expr': None, 'position': wx.Point(115, 205), 'refresh': []}, {'activate': 1, 'show': 1, 'borderRightColor': (100, 100, 100), 'recount': None, 'keyDown': None, 'borderTopColor': (100, 100, 100), 'font': {'style': 'italic', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Tahoma', 'type': 'Font', 'underline': False, 'size': 8}, 'border': 0, 'alignment': u"('left', 'middle')", 'size': wx.Size(225, 22), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'label': u"  \u041f\u0440\u0438\u043c\u0435\u0440:  'field1'='\u041f\u0435\u0442\u0440\u043e\u0432', 'field2'=20, ...", 'source': None, 'backgroundColor': (255, 249, 223), 'isSort': False, 'type': u'HeadCell', 'init_expr': None, 'shortHelpString': u'', '_uuid': u'dadfa5ab8e329065e9841befe332afee', 'style': 0, 'flag': 0, 'child': [], 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': (100, 100, 100), 'name': u'HeadCell_1130', 'borderBottomColor': (100, 100, 100), 'refresh': None, 'alias': None, 'borderWidth': 1, 'position': wx.Point(115, 276), 'borderStyle': None}], 'refresh': None, 'border': 0, 'size': (430, 600), 'style': 536877056, 'foregroundColor': None, 'span': (1, 1), 'title': u'\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0430 \u0441\u0432\u043e\u0439\u0441\u0442\u0432 \u0438\u043d\u0434\u0438\u043a\u0430\u0442\u043e\u0440\u0430', 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'Dialog', 'onClose': None, '_uuid': u'abc1cb918eabb3bb0858836d52fbbe27', 'moveAfterInTabOrder': u'', 'killFocus': None, 'flag': 0, 'recount': None, 'setFocus': None, 'name': u'DialogArrowIndProperty', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1)}

#   Версия объекта
__version__ = (1, 0, 2, 2)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'ArrowIndProperty'


class ArrowIndProperty:
    def __init__(self, parent, indicator=None):
        """
        Конструктор интерфейса.
        
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type indicator: C{ic.components.user.icarrowindicator.icArrowIndicator}
        @param indicator: Указатель на индикатор свойства, которого настраиваем.
        """
        self.evalSpace = util.InitEvalSpace()
        self.evalSpace['WrapperObj'] = self
        
        #   Указатель на индикатор
        self._indicator = indicator
        
        self.__obj = prs.icBuildObject(parent, resource, evalSpace=self.evalSpace, bIndicator=False)
        self.object = self.evalSpace['_root_obj']
        self.Init()
        self.OnRefresh(None)
        
    def getObject(self):
        """
        """
        return self.object
        
    def GetIndicator(self):
        """
        Возвращает указатель на индикатор.
        """
        return self._indicator
        
    def GetNameObj(self, name):
        """
        Возвращает указатель на объект с указанным именем.
        """
        if name in self.evalSpace['_dict_obj']:
            return self.evalSpace['_dict_obj'][name]
        else:
            return None
           
    def Init(self):
        """
        Инициализируем контролы значениями текщего индикатора.
        """
        ind = self.GetIndicator()
        
        if ind:
            # --- Заполняем основные свойства индикатора
            if ind.majorValues:
                min = ind.majorValues[0]
                max = ind.majorValues[-1]
                self.GetNameObj('minVal').SetValue(min)
                self.GetNameObj('maxVal').SetValue(max)
                minorStep = majorStep = (max - min)/(len(ind.majorValues)-1)
                self.GetNameObj('majorStep').SetValue(majorStep)
                
                if ind.minorValues:
                    minorStep = (max - min)/(len(ind.minorValues)-1)
                    
                self.GetNameObj('minorStep').SetValue(minorStep)
                
            self.GetNameObj('labelGraph').SetValue(ind.GetLabel())
            self.GetNameObj('eiEdt').SetValue(ind.ei)
            self.GetNameObj('factor').SetValue(str(ind.factor))
            
            if ind.source:
                ctrl = self.GetNameObj('tableNameEdt')
                ctrl.SetValue(ind.source)
                
                #   Список возможных источников данных берем из пространства
                # имен формы
                if len(ind.evalSpace['_sources'].keys()) > 0:
                    ctrl.Clear()
                    for key in ind.evalSpace['_sources']:
                        ctrl.Append(key)
                
            if ind.attrVal:
                self.GetNameObj('valAttrNameEdt').SetValue(ind.attrVal)
                
            if ind.attrPlan:
                self.GetNameObj('planAttrNameEdt').SetValue(ind.attrPlan)
            
            self.GetNameObj('aggregTypeChoice').SetValue(ind.aggregationType)

            self.GetNameObj('aggregFuncChoice').SetValue(ind.aggregationFunc)
            
            #   Устанавливаем списки полей
            self.SetFieldListComboCtrl()
            
            clr = ind.colorRegions
            
            if clr:
                lst = ('redSpinner', 'yellowSpinner', 'greenSpinner', 'yellowSpinner2')
                for indx, nm in enumerate(lst):
                    if indx < len(clr):
                        val = clr[indx][0]
                        if type(val) in (str, unicode):
                            self.GetNameObj(nm).SetValue(int(val.replace('%', '')))
                        
            # --- Заполняем структуру классов данных
            src_name = ind.source
            
            if src_name:
                pass
            
    def OnCancel(self, evt):
        """
        Выход из диалога.
        """
        self.getObject().EndModal(wx.ID_CANCEL)
        
        if evt:
            evt.Skip()
            
    def OnGroupConditionCtrl(self, value):
        """
        Функция контроля условия группировки.
        """
        cdt = self.ParseUserQuery(value)
        
        if cdt:
            return coderror.IC_CTRL_OK
        else:
            prnt = self.GetNameObj('DialogArrowIndProperty')
            msgbox.MsgBox(prnt, u'Не верное условие группировки')
            return coderror.IC_CTRL_FAILED_IGNORE
            
    def OnRefresh(self, evt):
        """
        Обрабатываем шажатие кнопки обновить представление.
        """
        min = int(self.GetNameObj('minVal').GetValue())
        max = int(self.GetNameObj('maxVal').GetValue())
        label = self.GetNameObj('labelGraph').GetValue()
        factor = int(self.GetNameObj('factor').GetValue())
        ei = self.GetNameObj('eiEdt').GetValue()
        majorStep = int(float(self.GetNameObj('majorStep').GetValue()))
        minorStep = int(float(self.GetNameObj('minorStep').GetValue()))
        ind = self.GetNameObj('indicator')
        
        red1 = self.GetNameObj('redSpinner').GetValue()
        yellow1 = self.GetNameObj('yellowSpinner').GetValue()
        green = self.GetNameObj('greenSpinner').GetValue()
        yellow2 = self.GetNameObj('yellowSpinner2').GetValue()
        
        ind.SetAggregationType(self.GetNameObj('aggregTypeChoice').GetValue())
        ind.SetAggregationFunc(self.GetNameObj('aggregFuncChoice').GetValue())

        ind.RecountScalePar(min, max, majorStep, minorStep, factor)
        
        ind.ei = ei
        ind.colorRegions = [('%d' % red1, 'RED'),
                            ('%d' % yellow1, (255, 150, 0)),
                            ('%d' % green, 'GREEN'),
                            ('%d' % yellow2, (255, 150, 0)),
                            ('100%', 'RED')]
                    
        ind.SetLabel(label)
        ind.Refresh()

    def OnSave(self, evt):
        """
        Сохранить настройки.
        """
        self.RefreshIndProp()
        self.getObject().EndModal(wx.ID_OK)
        
        if evt:
            evt.Skip()

    def ParseUserQuery(self, user_query):
        """
        Формирует по пользовательскому условию группировки структурный словарный
        запрос. <'f1'='Петров', 'f2'=10> -> {'f1':'Петров', 'f2':10}.
        
        @type user_query: C{string}
        @param user_query: Строка пользовательского запроса.
        @rtype: C{dictionary}
        @return: Структурный запрос.
        """
        user_query = user_query.strip()
        
        #   Если строка начинается на '{', считаем, что условие записано в
        #   виде структурного запроса
        if not user_query.startswith('{'):
            user_query = '{%s}' % (user_query.replace('=', ':').replace(';', ',').
                                   replace('\r\n', '\n').replace('\n', ','))
                                    
        #   Преобразуем к словарю
        try:
            return eval(user_query)
        except:
            return None
            
    def RefreshIndProp(self):
        """
        Изменяет свойства настраиваемого индикатора.
        """
        min = int(self.GetNameObj('minVal').GetValue())
        max = int(self.GetNameObj('maxVal').GetValue())
        label = self.GetNameObj('labelGraph').GetValue()
        majorStep = int(float(self.GetNameObj('majorStep').GetValue()))
        minorStep = int(float(self.GetNameObj('minorStep').GetValue()))
        factor = int(float(self.GetNameObj('factor').GetValue()))
        ind = self.GetIndicator()
        
        if ind:
            red1 = self.GetNameObj('redSpinner').GetValue()
            yellow1 = self.GetNameObj('yellowSpinner').GetValue()
            green = self.GetNameObj('greenSpinner').GetValue()
            yellow2 = self.GetNameObj('yellowSpinner2').GetValue()
            ei = self.GetNameObj('eiEdt').GetValue()
            
            _table = self.GetNameObj('tableNameEdt').GetValue()
            _val = self.GetNameObj('valAttrNameEdt').GetValue()
            _plan = self.GetNameObj('planAttrNameEdt').GetValue()
                        
            ind.source = _table
            ind.attrVal = _val
            ind.attrPlan = _plan
            ind.SetAggregationType(self.GetNameObj('aggregTypeChoice').GetValue())
            ind.SetAggregationFunc(self.GetNameObj('aggregFuncChoice').GetValue())
            
            ind.RecountScalePar(min, max, majorStep, minorStep, factor)
            ind.colorRegions = [('%d' % red1, 'RED'),
                                ('%d' % yellow1, (255, 150, 0)),
                                ('%d' % green, 'GREEN'),
                                ('%d' % yellow2, (255, 150, 0)),
                                ('100%', 'RED')]
                        
            ind.SetLabel(label)
            ind.ei = ei
            ind.Refresh()

    def SetFieldListComboCtrl(self):
        """
        Устанавливает списоки возможных значений для выбора полей.
        """
        ind = self.GetIndicator()

        valCtrl = self.GetNameObj('valAttrNameEdt').GetValue()
        planCtrl = self.GetNameObj('planAttrNameEdt').GetValue()
        src = self.GetNameObj('tableNameEdt').GetValue()
            
        if src in ind.evalSpace['_sources']:
            res = ind.evalSpace['_sources'][src].resource
            valCtrl.Clear()
            planCtrl.Clear()
            
            for el in res['child']:
                valCtrl.Appen(el['name'])
                planCtrl.Appen(el['name'])


def test(par=0):
    """
    Тестируем класс ArrowIndProperty.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    frame.Show(True)

    ################
    # Тестовый код #
    ################
    cls = ArrowIndProperty(None)
    dlg = cls.getObject()
    dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop()


if __name__ == '__main__':
    test()
