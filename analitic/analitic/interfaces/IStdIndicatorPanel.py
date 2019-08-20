#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import copy
import wx

from pytz import timezone
from matplotlib.dates import drange
import matplotlib.dates as dates

import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.db.icdataset as icdataset
import ic.interfaces.icobjectinterface as icobjectinterface

try:
    import analitic.genMonitor as genMonitor
except:
    print('Import Error analitic.genMonitor')

try:
    import analitic.indicatorUtils as indicatorUtils
except:
    print('Import Error analitic.indicatorUtils')

try:
    import plan.calc_plan as calc_plan
except:
    print('Import Error plan.calc_plan')
    
from ic.log import log
from analitic.usercomponents import icarrowindicator
from ic.dlg import ic_proccess_dlg

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'show': u'1', 'recount': None, 'keyDown': None, 'border': 0, 'size': (700, 600), 'onRightMouseClick': u"print 'onRightMouseClick'", 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': u"print 'onLeftMouseClick'", 'backgroundColor': (245, 245, 245), 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'bf5b0d8a9fc1353d01f977a8709e7615', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'style': 0, 'activate': 1, 'prim': u'', 'name': u'Data', 'component_module': None, '_uuid': u'b01e2342064bbaf506d57543e6455c7b', 'alias': None, 'init_expr': u'', 'child': [], 'type': u'Group'}, {'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'description': None, 'position': (0, 0), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'508b1bf8a594506b81b211d43874f382', 'proportion': 0, 'name': u'MainSZR', 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'style': 0, 'activate': 1, 'span': (1, 1), 'description': None, 'component_module': None, 'type': u'SizerSpace', '_uuid': u'0931986146d7bdeb83879524030c47ea', 'proportion': 0, 'name': u'DefaultName_1199_1358', 'alias': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'border': 0, 'size': (0, 0)}, {'activate': 1, 'show': 1, 'borderRightColor': None, 'child': [{'activate': 1, 'show': 1, 'value': u'', 'border': 0, 'size': (-1, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'DatePickerCtrl', 'description': None, '_uuid': u'e6485b9cc5d3c1c9da6a6478802f494e', 'style': 2, 'flag': 0, 'recount': None, 'name': u'currentDate', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (180, 9), 'onInit': None, 'refresh': None}], 'refresh': None, 'borderTopColor': None, 'font': {'style': u'regular', 'size': 8, 'underline': False, 'faceName': u'Tahoma', 'family': u'sansSerif'}, 'border': 0, 'alignment': u"('left', 'middle')", 'size': wx.Size(286, 44), 'moveAfterInTabOrder': u'', 'foregroundColor': (10, 83, 220), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'  \u041c\u043e\u043d\u0438\u0442\u043e\u0440\u0438\u043d\u0433 \u043f\u043e\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u0435\u0439 \u043d\u0430', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'borderWidth': 1, 'description': None, 'shortHelpString': u'', '_uuid': u'259dd5dcf4fc2ed09b12874f5e4f4fc9', 'style': 0, 'flag': 8192, 'recount': None, 'cursorColor': (100, 100, 100), 'borderStyle': None, 'borderStep': 0, 'borderLeftColor': None, 'name': u'HeadCell_1975_2134', 'borderBottomColor': (10, 83, 220), 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(0, 0), 'backgroundType': 0, 'onInit': u''}, {'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (-1, -1), 'style': 2097668, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': (245, 245, 245), 'type': u'ToolBar', 'description': None, '_uuid': u'1846b52e8739a40a48b8eaeea4250df6', 'moveAfterInTabOrder': u'', 'flag': 8192, 'child': [{'activate': 1, 'name': u'default_1107', 'toolType': 0, 'shortHelpString': u'\u041e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u0435 \u0438\u043d\u0434\u0438\u043a\u0430\u0442\u043e\u0440\u043e\u0432', 'longHelpString': u'', '_uuid': u'ee11ec5efa2d531fdc31ca409c689eb2', 'pushedBitmap': None, 'label': u'', 'isToggle': 0, 'init_expr': None, 'bitmap': u'@import ic.imglib.common as common\r\n_resultEval = common.imgRefreshPage', 'type': u'ToolBarTool', 'onTool': u'WrapperObj.OnToolRefresh(evt)'}], 'name': u'ToolBar', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(0, 42), 'onInit': None, 'bitmap_size': (16, 15)}, {'style': 0, 'activate': 1, 'span': (1, 1), 'description': None, 'component_module': None, 'type': u'SizerSpace', '_uuid': u'89999d336a54fded1afa8abd13d38690', 'proportion': 0, 'name': u'DefaultName_1482_2106', 'alias': None, 'flag': 0, 'init_expr': None, 'position': wx.Point(0, 69), 'border': 0, 'size': (27, 3)}, {'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'horizontal', 'description': None, 'position': (0, 0), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'075bdae02037d54454edc9afc74d819b', 'proportion': 0, 'name': u'SZR', 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'hgap': 0, 'style': 0, 'activate': u'1', 'layout': u'vertical', 'name': u'ZajavSZR', 'position': (-1, -1), 'component_module': None, 'type': u'StaticBoxSizer', '_uuid': u'62a931c3edd085758b1428e43ceb092b', 'proportion': 0, 'label': u'\u0417\u0430\u044f\u0432\u043a\u0438', 'alias': u'', 'flag': 0, 'init_expr': None, 'child': [{'majorValues': u'[0, 20, 40, 60, 80, 100]', 'activate': 1, 'ei': u'\u0440\u0443\u0431\u043b\u0435\u0439', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\r\nindicatorUtils.SaveIndicatorProperty(self, 'IZSD')\r\n", 'onLeftDblClick': u'', 'keyDown': None, 'font': {'family': u'sansSerif', 'style': u'bold', 'underline': False, 'faceName': u'Tahoma', 'size': 8}, 'border': 0, 'structQuery': {}, 'size': (200, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'component_module': None, 'proportion': 0, 'onGraph': None, 'label': u'\u041d\u0430 \u0442\u0435\u043a. \u0434\u0430\u0442\u0443 (\u0440\u0443\u0431.)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': None, 'backgroundColor': (235, 235, 235), 'factor': 1, 'type': u'ArrowIndicator', 'init_expr': None, 'description': None, 'minorValues': u'[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]', 'shortHelpString': u'', '_uuid': u'95fcc13b6a3b610f0be16fae9ec772ce', 'moveAfterInTabOrder': u'', 'aggregationType': u'USUAL', 'attrVal': None, 'majorLabels': u'', 'onColor': u'WrapperObj.OnColorFunc(evt)', 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': None, 'name': u'dayZajav', 'typPar': u'', 'flag': 8192, 'value': u'0', 'alias': None, 'aggregationFunc': u'SUM', 'cod': u'000', 'attrTime': u'dtoper', 'position': wx.Point(5, 89), 'onInit': None, 'refresh': None}, {'majorValues': u'[0, 20, 40, 60, 80, 100]', 'activate': 1, 'ei': u'\u0440\u0443\u0431\u043b\u0435\u0439', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\r\nindicatorUtils.SaveIndicatorProperty(self, 'IZSM')\r\n", 'onLeftDblClick': u'', 'value': u'0', 'font': {'style': u'bold', 'size': 8, 'underline': False, 'family': u'sansSerif', 'faceName': u'Tahoma'}, 'border': 0, 'structQuery': {}, 'size': (200, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'component_module': None, 'proportion': 0, 'onGraph': None, 'label': u'\u0421 \u043d\u0430\u0447.  \u043c\u0435\u0441\u044f\u0446\u0430 (\u0440\u0443\u0431.)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': None, 'backgroundColor': (247, 247, 247), 'factor': 1, 'type': u'ArrowIndicator', 'init_expr': None, 'description': None, 'minorValues': u'[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]', 'shortHelpString': u'', '_uuid': u'5304c659b0b3ddc031d7085ca3a1ff3c', 'moveAfterInTabOrder': u'', 'aggregationType': u'USUAL', 'attrVal': None, 'majorLabels': None, 'onColor': u'WrapperObj.OnColorFunc(evt)', 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': None, 'name': u'monthZajav', 'typPar': u'', 'flag': 8192, 'keyDown': None, 'alias': None, 'aggregationFunc': u'SUM', 'cod': u'000', 'attrTime': u'dtoper', 'position': wx.Point(0, 60), 'onInit': None, 'refresh': None}, {'majorValues': u'[0, 20, 40, 60, 80, 100]', 'activate': u'0', 'ei': u'\u0440\u0443\u0431\u043b\u0435\u0439', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\r\nindicatorUtils.SaveIndicatorProperty(self, 'IZSQ')\r\n", 'onLeftDblClick': u'', 'keyDown': None, 'font': {'style': u'bold', 'size': 8, 'underline': False, 'family': u'sansSerif', 'faceName': u'Tahoma'}, 'border': 0, 'structQuery': {}, 'size': (200, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'component_module': None, 'proportion': 0, 'onGraph': None, 'label': u'\u0417\u0430\u044f\u0432\u043b\u0435\u043d\u043d\u043e \u043d\u0430 \u043a\u0432\u0430\u0440\u0442\u0430\u043b (\u0440\u0443\u0431.)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': None, 'backgroundColor': (235, 235, 235), 'factor': 1, 'type': u'ArrowIndicator', 'init_expr': None, 'majorLabels': None, 'minorValues': u'[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]', 'shortHelpString': u'', '_uuid': u'18cb8ed45a487c15c72a137a5c37c143', 'moveAfterInTabOrder': u'', 'aggregationType': u'USUAL', 'attrVal': None, 'flag': 8192, 'onColor': u"_dict_obj['SZR'].Layout()\r\n_dict_obj['MainIndicatorPanel'].Refresh()", 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': None, 'name': u'qwartZajav', 'typPar': u'', 'value': u'0', 'alias': None, 'aggregationFunc': u'SUM', 'cod': u'000', 'attrTime': u'dtoper', 'position': wx.Point(0, 161), 'onInit': None, 'refresh': None}, {'majorValues': u'[0, 20, 40, 60, 80, 100]', 'activate': 1, 'ei': u'\u0440\u0443\u0431\u043b\u0435\u0439', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\r\nindicatorUtils.SaveIndicatorProperty(self, 'IZSY')\r\n", 'onLeftDblClick': u'', 'value': u'0', 'font': {'style': u'bold', 'size': 8, 'underline': False, 'family': u'sansSerif', 'faceName': u'Tahoma'}, 'border': 0, 'structQuery': {}, 'size': (220, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'component_module': None, 'proportion': 0, 'onGraph': None, 'label': u'\u0421 \u043d\u0430\u0447. \u0433\u043e\u0434\u0430 (\u0440\u0443\u0431.)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': None, 'backgroundColor': (247, 247, 247), 'factor': 1, 'type': u'ArrowIndicator', 'init_expr': None, 'description': None, 'minorValues': u'[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]', 'shortHelpString': u'', '_uuid': u'74d432cabfdbe93e822e60b79f410e1e', 'moveAfterInTabOrder': u'', 'aggregationType': u'USUAL', 'attrVal': None, 'majorLabels': None, 'onColor': u'WrapperObj.OnColorFunc(evt)', 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': None, 'name': u'yearZajav', 'typPar': u'', 'flag': 8192, 'keyDown': None, 'alias': None, 'aggregationFunc': u'SUM', 'cod': u'000', 'attrTime': u'dtoper', 'position': wx.Point(0, 240), 'onInit': None, 'refresh': None}, {'style': 0, 'activate': 1, 'span': (1, 1), 'name': u'DefaultName_2892', 'type': u'SizerSpace', '_uuid': u'c55cb2e4047feeab38312c6480cda386', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': wx.Point(166, 98), 'border': 0, 'size': (10, 10)}, {'majorValues': u'[0, 20,40, 60, 80, 100]', 'activate': u'1', 'ei': u'\u043a\u0433.', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\r\nindicatorUtils.SaveIndicatorProperty(self, 'IZVD')\r\n", 'onLeftDblClick': u'', 'value': u'0', 'font': {'style': u'bold', 'size': 8, 'underline': False, 'family': u'sansSerif', 'faceName': u'Tahoma'}, 'border': 0, 'structQuery': {}, 'size': (200, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'component_module': None, 'proportion': 0, 'dateIzm': u'', 'onGraph': None, 'label': u'\u041d\u0430 \u0442\u0435\u043a. \u0434\u0430\u0442\u0443 (\u043a\u0433.)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': None, 'backgroundColor': (247, 247, 247), 'factor': 1, 'type': u'ArrowIndicator', 'init_expr': None, 'description': None, 'minorValues': u'[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]', 'shortHelpString': u'', '_uuid': u'1d29791d8a501aacb0c6d10bb2debe9b', 'moveAfterInTabOrder': u'', 'aggregationType': u'USUAL', 'attrVal': None, 'majorLabels': u'', 'onColor': u'WrapperObj.OnColorFunc(evt)', 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': None, 'name': u'dayZajavMass', 'typPar': u'', 'flag': 8192, 'keyDown': None, 'alias': None, 'aggregationFunc': u'SUM', 'cod': u'000', 'attrTime': u'dtoper', 'position': wx.Point(0, 0), 'onInit': None, 'refresh': None}, {'majorValues': u'[0, 20, 40, 60, 80, 100]', 'activate': u'1', 'ei': u'\u043a\u0433.', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\r\nindicatorUtils.SaveIndicatorProperty(self, 'IZVM')\r\n", 'onLeftDblClick': u'', 'keyDown': None, 'font': {'faceName': u'Tahoma', 'style': u'bold', 'underline': False, 'family': u'sansSerif', 'size': 8}, 'border': 0, 'structQuery': {}, 'size': (200, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'component_module': None, 'proportion': 0, 'dateIzm': u'', 'onGraph': None, 'label': u'\u0421 \u043d\u0430\u0447. \u043c\u0435\u0441\u044f\u0446\u0430 (\u043a\u0433.)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': None, 'backgroundColor': (235, 235, 235), 'factor': 1, 'type': u'ArrowIndicator', 'init_expr': None, 'description': None, 'minorValues': u'[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]', 'shortHelpString': u'', '_uuid': u'7a85e35a3268dc717ac39e630f6814a0', 'moveAfterInTabOrder': u'', 'aggregationType': u'USUAL', 'attrVal': None, 'majorLabels': None, 'onColor': u'WrapperObj.OnColorFunc(evt)', 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': None, 'name': u'monthZajavMass', 'typPar': u'', 'flag': 8192, 'value': u'0', 'alias': None, 'aggregationFunc': u'SUM', 'cod': u'000', 'attrTime': u'dtoper', 'position': wx.Point(0, 60), 'onInit': None, 'refresh': None}, {'majorValues': u'[0, 20, 40, 60, 80, 100]', 'activate': u'0', 'ei': u'\u043a\u0433.', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\r\nindicatorUtils.SaveIndicatorProperty(self, 'IZVQ')\r\n", 'onLeftDblClick': u'', 'value': u'0', 'font': {'faceName': u'Tahoma', 'style': u'bold', 'underline': False, 'family': u'sansSerif', 'size': 8}, 'border': 0, 'structQuery': {}, 'size': (200, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'component_module': None, 'proportion': 0, 'dateIzm': u'', 'onGraph': None, 'label': u'\u0417\u0430\u044f\u0432\u043b\u0435\u043d\u043d\u043e \u043d\u0430 \u043a\u0432\u0430\u0440\u0442\u0430\u043b (\u043a\u0433)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': None, 'backgroundColor': (247, 247, 247), 'factor': 1, 'type': u'ArrowIndicator', 'init_expr': None, 'majorLabels': None, 'minorValues': u'[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]', 'shortHelpString': u'', '_uuid': u'527021af7158f8f5cb35a2e88f73d24f', 'moveAfterInTabOrder': u'', 'aggregationType': u'USUAL', 'attrVal': None, 'flag': 8192, 'onColor': u"_dict_obj['SZR'].Layout()\r\n_dict_obj['MainIndicatorPanel'].Refresh()", 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': None, 'name': u'qwartZajavMass', 'typPar': u'', 'keyDown': None, 'alias': None, 'aggregationFunc': u'SUM', 'cod': u'000', 'attrTime': u'dtoper', 'position': wx.Point(0, 161), 'onInit': None, 'refresh': None}, {'majorValues': u'[0, 20, 40, 60, 80, 100]', 'activate': u'1', 'ei': u'\u043a\u0433.', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\r\nindicatorUtils.SaveIndicatorProperty(self, 'IZVY')\r\n", 'onLeftDblClick': u'', 'keyDown': None, 'font': {'faceName': u'Tahoma', 'style': u'bold', 'underline': False, 'family': u'sansSerif', 'size': 8}, 'border': 0, 'structQuery': {}, 'size': (220, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'component_module': None, 'proportion': 0, 'dateIzm': u'', 'onGraph': None, 'label': u'\u0421 \u043d\u0430\u0447. \u0433\u043e\u0434\u0430 (\u043a\u0433.)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': None, 'backgroundColor': (235, 235, 235), 'factor': 1, 'type': u'ArrowIndicator', 'init_expr': None, 'description': None, 'minorValues': u'[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]', 'shortHelpString': u'', '_uuid': u'aa5af2c5a5bfa2b026dbc189c9ea4667', 'moveAfterInTabOrder': u'', 'aggregationType': u'USUAL', 'attrVal': None, 'majorLabels': None, 'onColor': u'WrapperObj.OnColorFunc(evt)', 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': None, 'name': u'yearZajavMass', 'typPar': u'', 'flag': 8192, 'value': u'0', 'alias': None, 'aggregationFunc': u'SUM', 'cod': u'000', 'attrTime': u'dtoper', 'position': wx.Point(235, 167), 'onInit': None, 'refresh': None}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}, {'style': 0, 'activate': 1, 'span': (1, 1), 'name': u'DefaultName_1199_1592_1903', 'border': 0, '_uuid': u'0931986146d7bdeb83879524030c47ea', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'type': u'SizerSpace', 'size': (2, 0)}, {'hgap': 0, 'style': 0, 'activate': u'1', 'layout': u'vertical', 'name': u'IspZajavSZR', 'position': (-1, -1), 'component_module': None, 'type': u'StaticBoxSizer', '_uuid': u'0bd9aba8bd4f0049a64abfbd8e4dab40', 'proportion': 0, 'label': u'\u0418\u0441\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435 \u0437\u0430\u044f\u0432\u043e\u043a', 'alias': u'', 'flag': 0, 'init_expr': None, 'child': [{'majorValues': u'[0, 20, 40, 60, 80, 100]', 'activate': 1, 'ei': u'\u0440\u0443\u0431\u043b\u0435\u0439', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\r\nindicatorUtils.SaveIndicatorProperty(self, 'IZSD')\r\n", 'onLeftDblClick': u'', 'value': u'0', 'font': {'style': u'bold', 'size': 8, 'underline': False, 'family': u'sansSerif', 'faceName': u'Tahoma'}, 'border': 0, 'structQuery': {}, 'size': (200, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'position': wx.Point(0, 0), 'component_module': None, 'proportion': 0, 'onGraph': None, 'label': u'\u041d\u0430 \u0442\u0435\u043a. \u0434\u0430\u0442\u0443 (\u0440\u0443\u0431.)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': None, 'backgroundColor': (235, 235, 235), 'factor': 1, 'type': u'ArrowIndicator', 'cod': u'000', 'description': None, 'minorValues': u'[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]', 'shortHelpString': u'', '_uuid': u'bffb86f6b83076bd325c3a14f23694cf', 'moveAfterInTabOrder': u'', 'attrVal': None, 'majorLabels': u'', 'onColor': u'WrapperObj.OnColorFunc(evt)', 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': None, 'name': u'dayIspZajav', 'typPar': u'', 'flag': 8192, 'keyDown': None, 'alias': None, 'aggregationFunc': u'SUM', 'init_expr': None, 'attrTime': u'dtoper', 'aggregationType': u'USUAL', 'onInit': None, 'refresh': None}, {'majorValues': u'[0, 20, 40, 60, 80, 100]', 'activate': 1, 'ei': u'\u0440\u0443\u0431\u043b\u0435\u0439', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\r\nindicatorUtils.SaveIndicatorProperty(self, 'IZSM')\r\n", 'onLeftDblClick': u'', 'keyDown': None, 'font': {'faceName': u'Tahoma', 'style': u'bold', 'underline': False, 'family': u'sansSerif', 'size': 8}, 'border': 0, 'structQuery': {}, 'size': (200, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'position': wx.Point(0, 60), 'component_module': None, 'proportion': 0, 'onGraph': None, 'label': u'\u0421 \u043d\u0430\u0447. \u043c\u0435\u0441\u044f\u0446\u0430 (\u0440\u0443\u0431.)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': None, 'backgroundColor': (247, 247, 247), 'factor': 1, 'type': u'ArrowIndicator', 'cod': u'000', 'description': None, 'minorValues': u'[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]', 'shortHelpString': u'', '_uuid': u'1bdc5643a445218947d0aa42f5b99f6d', 'moveAfterInTabOrder': u'', 'attrVal': None, 'majorLabels': None, 'onColor': u'WrapperObj.OnColorFunc(evt)', 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': None, 'name': u'monthIspZajav', 'typPar': u'', 'flag': 8192, 'value': u'0', 'alias': None, 'aggregationFunc': u'SUM', 'init_expr': None, 'attrTime': u'dtoper', 'aggregationType': u'USUAL', 'onInit': None, 'refresh': None}, {'majorValues': u'[0, 20, 40, 60, 80, 100]', 'activate': u'0', 'ei': u'\u0440\u0443\u0431\u043b\u0435\u0439', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\r\nindicatorUtils.SaveIndicatorProperty(self, 'IZSQ')\r\n", 'onLeftDblClick': u'', 'value': u'0', 'font': {'faceName': u'Tahoma', 'style': u'bold', 'underline': False, 'family': u'sansSerif', 'size': 8}, 'border': 0, 'structQuery': {}, 'size': (200, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'position': wx.Point(0, 161), 'component_module': None, 'proportion': 0, 'onGraph': None, 'label': u'\u0418\u0441\u043f\u043e\u043b\u043d\u0435\u043d\u043d\u043e \u0437\u0430 \u043a\u0432\u0430\u0440\u0442\u0430\u043b (\u0440\u0443\u0431.)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': None, 'backgroundColor': (235, 235, 235), 'factor': 1, 'type': u'ArrowIndicator', 'cod': u'000', 'majorLabels': None, 'minorValues': u'[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]', 'shortHelpString': u'', '_uuid': u'befb5be84bbd957199d193fbe7d5733f', 'moveAfterInTabOrder': u'', 'attrVal': None, 'flag': 8192, 'onColor': u"_dict_obj['SZR'].Layout()\r\n_dict_obj['MainIndicatorPanel'].Refresh()", 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': None, 'name': u'qwartIspZajav', 'typPar': u'', 'keyDown': None, 'alias': None, 'aggregationFunc': u'SUM', 'init_expr': None, 'attrTime': u'dtoper', 'aggregationType': u'USUAL', 'onInit': None, 'refresh': None}, {'majorValues': u'[0, 20, 40, 60, 80, 100]', 'activate': 1, 'ei': u'\u0440\u0443\u0431\u043b\u0435\u0439', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\r\nindicatorUtils.SaveIndicatorProperty(self, 'IZSY')\r\n", 'onLeftDblClick': u'', 'keyDown': None, 'font': {'faceName': u'Tahoma', 'style': u'bold', 'underline': False, 'family': u'sansSerif', 'size': 8}, 'border': 0, 'structQuery': {}, 'size': (220, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'position': wx.Point(0, 240), 'component_module': None, 'proportion': 0, 'onGraph': None, 'label': u'\u0421 \u043d\u0430\u0447. \u0433\u043e\u0434\u0430 (\u0440\u0443\u0431.)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': None, 'backgroundColor': (247, 247, 247), 'factor': 1, 'type': u'ArrowIndicator', 'cod': u'000', 'description': None, 'minorValues': u'[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]', 'shortHelpString': u'', '_uuid': u'2f6ef600b8cf87698b297b4f16759af7', 'moveAfterInTabOrder': u'', 'attrVal': None, 'majorLabels': None, 'onColor': u'WrapperObj.OnColorFunc(evt)', 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': None, 'name': u'yearIspZajav', 'typPar': u'', 'flag': 8192, 'value': u'0', 'alias': None, 'aggregationFunc': u'SUM', 'init_expr': None, 'attrTime': u'dtoper', 'aggregationType': u'USUAL', 'onInit': None, 'refresh': None}, {'style': 0, 'activate': 1, 'span': (1, 1), 'name': u'DefaultName_2892', 'border': 0, '_uuid': u'c55cb2e4047feeab38312c6480cda386', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': wx.Point(166, 98), 'type': u'SizerSpace', 'size': (10, 10)}, {'majorValues': u'[0, 20,40, 60, 80, 100]', 'activate': u'1', 'ei': u'\u043a\u0433.', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\r\nindicatorUtils.SaveIndicatorProperty(self, 'IZVD')\r\n", 'onLeftDblClick': u'', 'keyDown': None, 'font': {'faceName': u'Tahoma', 'style': u'bold', 'underline': False, 'family': u'sansSerif', 'size': 8}, 'border': 0, 'structQuery': {}, 'size': (200, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'position': wx.Point(0, 0), 'component_module': None, 'proportion': 0, 'dateIzm': u'', 'onGraph': None, 'label': u'\u041d\u0430 \u0442\u0435\u043a. \u0434\u0430\u0442\u0443 (\u043a\u0433)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': None, 'backgroundColor': (247, 247, 247), 'factor': 1, 'type': u'ArrowIndicator', 'cod': u'000', 'description': None, 'minorValues': u'[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]', 'shortHelpString': u'', '_uuid': u'adb30fc0d183e31c20026f387701a8e6', 'moveAfterInTabOrder': u'', 'attrVal': None, 'majorLabels': u'', 'onColor': u'WrapperObj.OnColorFunc(evt)', 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': None, 'name': u'dayIspZajavMass', 'typPar': u'', 'flag': 8192, 'value': u'0', 'alias': None, 'aggregationFunc': u'SUM', 'init_expr': None, 'attrTime': u'dtoper', 'aggregationType': u'USUAL', 'onInit': None, 'refresh': None}, {'majorValues': u'[0, 20, 40, 60, 80, 100]', 'activate': u'1', 'ei': u'\u043a\u0433.', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\r\nindicatorUtils.SaveIndicatorProperty(self, 'IZVM')\r\n", 'onLeftDblClick': u'', 'value': u'0', 'font': {'style': u'bold', 'size': 8, 'underline': False, 'faceName': u'Tahoma', 'family': u'sansSerif'}, 'border': 0, 'structQuery': {}, 'size': (200, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'position': wx.Point(0, 60), 'component_module': None, 'proportion': 0, 'dateIzm': u'', 'onGraph': None, 'label': u'\u0421 \u043d\u0430\u0447. \u043c\u0435\u0441\u044f\u0446\u0430 (\u043a\u0433.)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': None, 'backgroundColor': (235, 235, 235), 'factor': 1, 'type': u'ArrowIndicator', 'cod': u'000', 'description': None, 'minorValues': u'[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]', 'shortHelpString': u'', '_uuid': u'3fdf00eec62755e7dc073572277e3943', 'moveAfterInTabOrder': u'', 'attrVal': None, 'majorLabels': None, 'onColor': u'WrapperObj.OnColorFunc(evt)', 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': None, 'name': u'monthIspZajavMass', 'typPar': u'', 'flag': 8192, 'keyDown': None, 'alias': None, 'aggregationFunc': u'SUM', 'init_expr': None, 'attrTime': u'dtoper', 'aggregationType': u'USUAL', 'onInit': None, 'refresh': None}, {'majorValues': u'[0, 20, 40, 60, 80, 100]', 'activate': u'0', 'ei': u'\u043a\u0433.', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\r\nindicatorUtils.SaveIndicatorProperty(self, 'IZVQ')\r\n", 'onLeftDblClick': u'', 'keyDown': None, 'font': {'style': u'bold', 'size': 8, 'underline': False, 'faceName': u'Tahoma', 'family': u'sansSerif'}, 'border': 0, 'structQuery': {}, 'size': (200, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'position': wx.Point(0, 161), 'component_module': None, 'proportion': 0, 'dateIzm': u'', 'onGraph': None, 'label': u'\u0418\u0441\u043f\u043e\u043b\u043d\u0435\u043d\u043d\u043e \u0437\u0430 \u043a\u0432\u0430\u0440\u0442\u0430\u043b (\u043a\u0433.)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': None, 'backgroundColor': (247, 247, 247), 'factor': 1, 'type': u'ArrowIndicator', 'cod': u'000', 'majorLabels': None, 'minorValues': u'[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]', 'shortHelpString': u'', '_uuid': u'e7f6eb1b3e2b3a50ceec29d6da13ea16', 'moveAfterInTabOrder': u'', 'attrVal': None, 'flag': 8192, 'onColor': u"_dict_obj['SZR'].Layout()\r\n_dict_obj['MainIndicatorPanel'].Refresh()", 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': None, 'name': u'qwartIspZajavMass', 'typPar': u'', 'value': u'50', 'alias': None, 'aggregationFunc': u'SUM', 'init_expr': None, 'attrTime': u'dtoper', 'aggregationType': u'USUAL', 'onInit': None, 'refresh': None}, {'majorValues': u'[0, 20, 40, 60, 80, 100]', 'activate': u'1', 'ei': u'\u043a\u0433.', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\r\nindicatorUtils.SaveIndicatorProperty(self, 'IZVY')\r\n", 'onLeftDblClick': u'', 'value': u'0', 'font': {'style': u'bold', 'size': 8, 'underline': False, 'faceName': u'Tahoma', 'family': u'sansSerif'}, 'border': 0, 'structQuery': {}, 'size': (220, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'position': wx.Point(235, 167), 'component_module': None, 'proportion': 0, 'dateIzm': u'', 'onGraph': None, 'label': u'\u0421 \u043d\u0430\u0447. \u0433\u043e\u0434\u0430 (\u043a\u0433)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': None, 'backgroundColor': (235, 235, 235), 'factor': 1, 'type': u'ArrowIndicator', 'cod': u'000', 'description': None, 'minorValues': u'[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]', 'shortHelpString': u'', '_uuid': u'325bf9448aa944133a0e28f14ee602e0', 'moveAfterInTabOrder': u'', 'attrVal': None, 'majorLabels': None, 'onColor': u'WrapperObj.OnColorFunc(evt)', 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': None, 'name': u'yearIspZajavMass', 'typPar': u'', 'flag': 8192, 'keyDown': None, 'alias': None, 'aggregationFunc': u'SUM', 'init_expr': None, 'attrTime': u'dtoper', 'aggregationType': u'USUAL', 'onInit': None, 'refresh': None}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}, {'style': 0, 'activate': 1, 'span': (1, 1), 'name': u'DefaultName_1199_1592_2016', 'type': u'SizerSpace', '_uuid': u'0931986146d7bdeb83879524030c47ea', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'border': 0, 'size': (2, 0)}, {'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'name': u'RealizSZR', 'position': (-1, -1), 'component_module': None, 'type': u'StaticBoxSizer', '_uuid': u'36f840faccea9a2c6fb977091c4837e0', 'proportion': 0, 'label': u'\u0420\u0435\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u044f', 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'majorValues': u'[0, 20, 40, 60, 80, 100]', 'activate': 1, 'ei': u'\u0440\u0443\u0431\u043b\u0435\u0439', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\r\nindicatorUtils.SaveIndicatorProperty(self, 'IRSD')\r\n", 'onLeftDblClick': u'', 'value': u'0', 'font': {'style': u'bold', 'size': 8, 'underline': False, 'family': u'sansSerif', 'faceName': u'Tahoma'}, 'border': 0, 'structQuery': {}, 'size': (200, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'position': wx.Point(5, 22), 'component_module': None, 'proportion': 0, 'dateIzm': u'', 'onGraph': None, 'label': u'\u041d\u0430 \u0442\u0435\u043a. \u0434\u0430\u0442\u0443 (\u0440\u0443\u0431.)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': u'realize_sum', 'backgroundColor': (235, 235, 235), 'factor': 1, 'type': u'ArrowIndicator', 'init_expr': u'', 'description': None, 'minorValues': u'[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]', 'shortHelpString': u'', '_uuid': u'7637050a6488e3651a4dcf2c7b478cd4', 'moveAfterInTabOrder': u'', 'attrVal': None, 'majorLabels': u'', 'onColor': u'WrapperObj.OnColorFunc(evt)', 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': [], 'name': u'dayRealiz', 'typPar': u'', 'flag': 8192, 'keyDown': None, 'alias': None, 'aggregationFunc': u'SUM', 'cod': u'000', 'attrTime': u'dtoper', 'aggregationType': u'USUAL', 'onInit': u'', 'refresh': None}, {'majorValues': u'[0, 20, 40, 60, 80, 100]', 'activate': 1, 'ei': u'\u0440\u0443\u0431\u043b\u0435\u0439', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\r\nindicatorUtils.SaveIndicatorProperty(self, 'IRSM')\r\nprint 'SaveIndicatorProperty'", 'onLeftDblClick': u'', 'keyDown': None, 'font': {'faceName': u'Tahoma', 'style': u'bold', 'underline': False, 'family': u'sansSerif', 'size': 8}, 'border': 0, 'structQuery': {}, 'size': (200, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'position': wx.Point(0, 60), 'component_module': None, 'proportion': 0, 'dateIzm': u'', 'onGraph': None, 'label': u'\u0421 \u043d\u0430\u0447. \u043c\u0435\u0441\u044f\u0446\u0430 (\u0440\u0443\u0431.)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': None, 'backgroundColor': (247, 247, 247), 'factor': 1, 'type': u'ArrowIndicator', 'cod': u'000', 'description': None, 'minorValues': u'[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]', 'shortHelpString': u'', '_uuid': u'0eaadb1736afa1ad8ca22e7e094d2f96', 'moveAfterInTabOrder': u'', 'attrVal': None, 'majorLabels': None, 'onColor': u'WrapperObj.OnColorFunc(evt)', 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': [], 'name': u'monthRealiz', 'typPar': u'', 'flag': 8192, 'value': u'0', 'alias': None, 'aggregationFunc': u'SUM', 'init_expr': u"#import analitic.indicatorUtils as indicatorUtils\r\n#indicatorUtils.LoadIndicatorProperty(self, 'IRSM')\r\n#self.Refresh()\r\n#print 'LoadIndicatorProperty'", 'attrTime': u'dtoper', 'aggregationType': u'USUAL', 'onInit': u'', 'refresh': None}, {'majorValues': u'[0, 20, 40, 60, 80, 100]', 'activate': u'0', 'ei': u'\u0440\u0443\u0431\u043b\u0435\u0439', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\r\nindicatorUtils.SaveIndicatorProperty(self, 'IRSQ')\r\n", 'onLeftDblClick': u'', 'value': u'50', 'font': {'faceName': u'Tahoma', 'style': u'bold', 'underline': False, 'family': u'sansSerif', 'size': 8}, 'border': 0, 'structQuery': {}, 'size': (200, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'position': wx.Point(0, 161), 'component_module': None, 'proportion': 0, 'dateIzm': u'', 'onGraph': None, 'label': u'\u041e\u0442\u0433\u0440\u0443\u0436\u0435\u043d\u043e \u0437\u0430 \u043a\u0432\u0430\u0440\u0442\u0430\u043b (\u0440\u0443\u0431.)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': None, 'backgroundColor': (235, 235, 235), 'factor': 1, 'type': u'ArrowIndicator', 'cod': u'000', 'majorLabels': None, 'minorValues': u'[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]', 'shortHelpString': u'', '_uuid': u'0f5a2be67ea17932765abc9035f419a9', 'moveAfterInTabOrder': u'', 'attrVal': None, 'flag': 8192, 'onColor': u"_dict_obj['SZR'].Layout()\r\n_dict_obj['MainIndicatorPanel'].Refresh()", 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': None, 'name': u'qwartRealiz', 'typPar': u'', 'keyDown': None, 'alias': None, 'aggregationFunc': u'SUM', 'init_expr': u"#import analitic.indicatorUtils as indicatorUtils\r\n#indicatorUtils.LoadIndicatorProperty(self, 'IRSQ')\r\n", 'attrTime': u'dtoper', 'aggregationType': u'USUAL', 'onInit': u'', 'refresh': None}, {'majorValues': u'[0, 20, 40, 60, 80, 100]', 'activate': 1, 'ei': u'\u0440\u0443\u0431\u043b\u0435\u0439', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\nindicatorUtils.SaveIndicatorProperty(self, 'IRSY')\n", 'onLeftDblClick': u'', 'keyDown': None, 'font': {'faceName': u'Tahoma', 'style': u'bold', 'underline': False, 'family': u'sansSerif', 'size': 8}, 'border': 0, 'structQuery': {}, 'size': (220, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'position': wx.Point(5, 78), 'component_module': None, 'proportion': 0, 'dateIzm': u'', 'onGraph': None, 'label': u'\u0421 \u043d\u0430\u0447. \u0433\u043e\u0434\u0430 (\u0440\u0443\u0431.)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': None, 'backgroundColor': (247, 247, 247), 'factor': 1, 'type': u'ArrowIndicator', 'cod': u'000', 'description': None, 'minorValues': u'[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]', 'shortHelpString': u'', '_uuid': u'b3142b061b5f177145d0c8bc47063cdc', 'moveAfterInTabOrder': u'', 'attrVal': None, 'majorLabels': None, 'onColor': u'WrapperObj.OnColorFunc(evt)', 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': None, 'name': u'yearRealiz', 'typPar': u'', 'flag': 8192, 'value': u'0', 'alias': None, 'aggregationFunc': u'SUM', 'init_expr': u'', 'attrTime': u'dtoper', 'aggregationType': u'USUAL', 'onInit': u'', 'refresh': None}, {'style': 0, 'activate': 1, 'span': (1, 1), 'name': u'DefaultName_2892', 'border': 0, '_uuid': u'c55cb2e4047feeab38312c6480cda386', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': wx.Point(166, 98), 'type': u'SizerSpace', 'size': (10, 10)}, {'majorValues': u'[0, 10, 20, 30, 40, 50]', 'activate': u'1', 'ei': u'\u043a\u0433.', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\r\nindicatorUtils.SaveIndicatorProperty(self, 'IRVD')\r\n", 'onLeftDblClick': u'', 'keyDown': None, 'font': {'faceName': u'Tahoma', 'style': u'bold', 'underline': False, 'family': u'sansSerif', 'size': 8}, 'border': 0, 'structQuery': {}, 'size': (200, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'position': wx.Point(0, 0), 'component_module': None, 'proportion': 0, 'dateIzm': u'', 'onGraph': None, 'label': u'\u041d\u0430 \u0442\u0435\u043a. \u0434\u0430\u0442\u0443 (\u043a\u0433.)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': None, 'backgroundColor': (247, 247, 247), 'factor': u'1000', 'type': u'ArrowIndicator', 'cod': u'000', 'description': None, 'minorValues': u'[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]', 'shortHelpString': u'', '_uuid': u'7c4105ab0dd524d6b757ed6b419a3406', 'moveAfterInTabOrder': u'', 'attrVal': None, 'majorLabels': u'', 'onColor': u'WrapperObj.OnColorFunc(evt)', 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': None, 'name': u'dayRealizMass', 'typPar': u'', 'flag': 8192, 'value': u'0', 'alias': None, 'aggregationFunc': u'SUM', 'init_expr': None, 'attrTime': u'dtoper', 'aggregationType': u'USUAL', 'onInit': u'', 'refresh': None}, {'majorValues': u'[0, 20, 40, 60, 80, 100]', 'activate': u'1', 'ei': u'\u043a\u0433.', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\r\nindicatorUtils.SaveIndicatorProperty(self, 'IRVM')\r\n", 'onLeftDblClick': u'', 'value': u'0', 'font': {'style': u'bold', 'size': 8, 'underline': False, 'faceName': u'Tahoma', 'family': u'sansSerif'}, 'border': 0, 'structQuery': {}, 'size': (200, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'position': wx.Point(0, 60), 'component_module': None, 'proportion': 0, 'dateIzm': u'', 'onGraph': None, 'label': u'\u0421 \u043d\u0430\u0447. \u043c\u0435\u0441\u044f\u0446\u0430 (\u043a\u0433.)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': None, 'backgroundColor': (235, 235, 235), 'factor': 1, 'type': u'ArrowIndicator', 'cod': u'000', 'description': None, 'minorValues': u'[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]', 'shortHelpString': u'', '_uuid': u'1bcc1589a22596fb90b3dd0730040407', 'moveAfterInTabOrder': u'', 'attrVal': None, 'majorLabels': None, 'onColor': u'WrapperObj.OnColorFunc(evt)', 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': None, 'name': u'monthRealizMass', 'typPar': u'', 'flag': 8192, 'keyDown': None, 'alias': None, 'aggregationFunc': u'SUM', 'init_expr': None, 'attrTime': u'dtoper', 'aggregationType': u'USUAL', 'onInit': u'', 'refresh': None}, {'majorValues': u'[0, 20, 40, 60, 80, 100]', 'activate': u'0', 'ei': u'\u043a\u0433.', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\r\nindicatorUtils.SaveIndicatorProperty(self, 'IRVQ')\r\n", 'onLeftDblClick': u'', 'keyDown': None, 'font': {'style': u'bold', 'size': 8, 'underline': False, 'faceName': u'Tahoma', 'family': u'sansSerif'}, 'border': 0, 'structQuery': {}, 'size': (200, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'position': wx.Point(0, 161), 'component_module': None, 'proportion': 0, 'dateIzm': u'', 'onGraph': None, 'label': u'\u041e\u0442\u0433\u0440\u0443\u0436\u0435\u043d\u043e \u0437\u0430 \u043a\u0432\u0430\u0440\u0442\u0430\u043b (\u043a\u0433.)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': None, 'backgroundColor': (247, 247, 247), 'factor': 1, 'type': u'ArrowIndicator', 'cod': u'000', 'majorLabels': None, 'minorValues': u'[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]', 'shortHelpString': u'', '_uuid': u'be8a748d44456a9f7be0b73d136ef5bb', 'moveAfterInTabOrder': u'', 'attrVal': None, 'flag': 8192, 'onColor': u"_dict_obj['SZR'].Layout()\r\n_dict_obj['MainIndicatorPanel'].Refresh()", 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': None, 'name': u'qwartRealizMass', 'typPar': u'', 'value': u'50', 'alias': None, 'aggregationFunc': u'SUM', 'init_expr': None, 'attrTime': u'dtoper', 'aggregationType': u'USUAL', 'onInit': u'', 'refresh': None}, {'majorValues': u'[0, 20, 40, 60, 80, 100]', 'activate': u'1', 'ei': u'\u043a\u0433.', 'show': 1, 'onSaveProperty': u"import analitic.indicatorUtils as indicatorUtils\r\nindicatorUtils.SaveIndicatorProperty(self, 'IRVY')\r\n", 'onLeftDblClick': u'', 'value': u'0', 'font': {'style': u'bold', 'size': 8, 'underline': False, 'faceName': u'Tahoma', 'family': u'sansSerif'}, 'border': 0, 'structQuery': {}, 'size': (220, 60), 'style': 0, 'foregroundColor': None, 'layout': u'horizontal', 'position': wx.Point(0, 240), 'component_module': None, 'proportion': 0, 'dateIzm': u'', 'onGraph': None, 'label': u'\u0421 \u043d\u0430\u0447. \u0433\u043e\u0434\u0430 (\u043a\u0433.)', 'colorRegions': u"[('25%', 'RED'), ('75%', (255, 200, 0)), ('100%', 'GREEN')]", 'source': None, 'backgroundColor': (235, 235, 235), 'factor': 1, 'type': u'ArrowIndicator', 'cod': u'000', 'description': None, 'minorValues': u'[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]', 'shortHelpString': u'', '_uuid': u'97f5207978e6c91cfadc8baf1f4f6fe2', 'moveAfterInTabOrder': u'', 'attrVal': None, 'majorLabels': None, 'onColor': u'WrapperObj.OnColorFunc(evt)', 'recount': None, 'span': (1, 1), 'attrPlan': None, 'periodIzm': None, 'name': u'yearRealizMass', 'typPar': u'', 'flag': 8192, 'keyDown': None, 'alias': None, 'aggregationFunc': u'SUM', 'init_expr': None, 'attrTime': u'dtoper', 'aggregationType': u'USUAL', 'onInit': u'', 'refresh': None}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}, {'style': 0, 'activate': 1, 'span': (1, 1), 'description': None, 'component_module': None, 'type': u'SizerSpace', '_uuid': u'0931986146d7bdeb83879524030c47ea', 'proportion': 0, 'name': u'DefaultName_1199_1512', 'alias': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'border': 0, 'size': (2, 0)}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}, {'activate': 1, 'show': 1, 'borderRightColor': None, 'recount': None, 'keyDown': None, 'borderTopColor': None, 'font': {'family': u'sansSerif', 'style': u'regular', 'underline': False, 'faceName': u'Tahoma', 'size': 8}, 'border': 0, 'alignment': u"('left', 'middle')", 'size': (286, 10), 'moveAfterInTabOrder': u'', 'foregroundColor': (10, 83, 220), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'init_expr': None, 'description': None, 'shortHelpString': u'', '_uuid': u'8e82cd43b7116f456f346a30ceb5f6b3', 'style': 0, 'flag': 8192, 'child': [], 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': None, 'name': u'HeadCell_Bottom', 'borderBottomColor': (10, 83, 220), 'refresh': None, 'alias': None, 'borderWidth': 1, 'position': wx.Point(0, 0), 'borderStyle': u'import wx\r\n_resultEval = wx.DOT', 'onInit': u''}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'name': u'MainIndicatorPanel', 'refresh': None, 'alias': None, 'init_expr': u'', 'position': wx.Point(0, 0), 'onInit': u'import analitic.indicatorUtils as Utils\r\n#   \u0417\u0430\u0433\u0440\u0443\u0436\u0430\u0435\u043c \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u0438\u043d\u0434\u0438\u043a\u0430\u0442\u043e\u0440\u043e\u0432 \u0438\u0437 \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u043e\u0432\r\nUtils.LoadMonitorProperties(_dict_obj)\r\n#   \u041e\u0431\u043d\u043e\u0432\u043b\u044f\u0435\u043c \u0441\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u044f \u0438\u043d\u0434\u0438\u043a\u0430\u0442\u043e\u0440\u043e\u0432\r\nUtils.RefreshFormRealizMonitor(_dict_obj)\r\n'}

#   Версия объекта
__version__ = (1, 1, 1, 1)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'IStdIndicatorPanel'


def _getMonthSumma(date, metaObj, tableName):
    """
    Вычисляет накопленную сумму на определенную дату.

    @type date: C{string}
    @param date: Дата в виде 'yyyy.mm.dd'
    @type metaObj: C{icMetaItem}
    @param metaObj: Текущий узел дерева данных.
    @type tableName: C{string}
    @param tableName: Имя таблицы агрегации.
    @rtype: C{float}
    @return: Возвращает накопленную сумму к определенной дате по месяцу.
    """
    try:
        metadict = getattr(metaObj.value, tableName)
    except AttributeError:
        print('### AttributeError in :_getMonthSumma date=%s, tableName=%s, metaObj=%s' % (date, tableName, metaObj))
        return 0, 0
        
    lst = metadict.keys()
    lst.sort()
    summa, kol = 0, 0
    
    for key in lst:
        if key > date:
            return summa, kol
#            if key <> 'summa':
        s, k = metadict[key]
        summa += s
        kol += k

        if key == date:
            return summa, kol
            
    return 0, 0


def _getMonthPlan(date, metaObj):
    """
    Вычисляет накопленную плановую сумму на определенную дату.

    @type date: C{string}
    @param date: Дата в виде 'yyyy.mm.dd'
    @type metaObj: C{icMetaItem}
    @param metaObj: Текущий узел дерева данных.
    @rtype: C{float}
    @return: Плановую накопленную сумму.
    """
    year, month, day = map(lambda x: int(x), date.split('.'))
    nday = wx.DateTime.GetNumberOfDaysInMonth(month-1, year)
    
    #   Находим декадные параметры
    cod_mnth = 'm%02d' % month
    
    root = metaObj.getRoot()
    decadWeight = root[str(year)][cod_mnth].value.decadWeight
    path = metaObj.getPath()
    
    if len(path) > 2:
        obj = root[str(year)][cod_mnth].findObject(path[2:])
    else:
        obj = root[str(year)][cod_mnth]
    
    #   Определяем количество дней в декаде
    dec_nday = {0: 10, 1: 10, 2: nday-20}
    summa = 0
    
    #   Сумма весовых коэфициентов
    sk = reduce(lambda x, y: x+y, decadWeight)
        
    for d in range(day):
        #   Определяем декаду
        if d <= 10:
            idec = 0
        elif d <=20:
            idec = 1
        else:
            idec = 2
        # декадный коэфициент
        k = decadWeight[idec]
        # накапливаем дневные планы
        # summa += k*metaObj.value.summa/(sk*dec_nday[idec])
        summa += k*obj.value.summa/(sk*dec_nday[idec])
    return summa


def _getMonthKolPlan(date, metaObj):
    """
    Вычисляет накопленную плановую сумму на определенную дату.

    @type date: C{string}
    @param date: Дата в виде 'yyyy.mm.dd'
    @type metaObj: C{icMetaItem}
    @param metaObj: Текущий узел дерева данных.
    @rtype: C{float}
    @return: Плановую накопленную сумму.
    """
    year, month, day = map(lambda x: int(x), date.split('.'))
    nday = wx.DateTime.GetNumberOfDaysInMonth(month-1, year)
    
    #   Находим декадные параметры
    root = metaObj.getRoot()
    decadWeight = root[str(year)]['m'+('0'+str(month))[-2:]].value.decadWeightKol
    
    #   Определяем количество дней в декаде
    dec_nday = {0: 10, 1: 10, 2: nday-20}
    summa = 0
    
    #   Сумма весовых коэфициентов
    sk = reduce(lambda x, y: x+y, decadWeight)
        
    for d in range(day):
        #   Определяем декаду
        if d <= 10:
            idec = 0
        elif d <= 20:
            idec = 1
        else:
            idec = 2
        # декадный коэфициент
        k = decadWeight[idec]
        # накапливаем дневные планы
        summa += k * metaObj.value.kol / (sk * dec_nday[idec])
    return summa


def _getYearSumma(date, metaObj, tableName):
    """
    Вычисляет накопленную годовую сумму к определенной дате.
    
    @type date: C{string}
    @param date: Дата в виде 'yyyy.mm.dd'
    @type metaObj: C{icMetaItem}
    @param metaObj: Текущий узел дерева данных.
    @type tableName: C{string}
    @param tableName: Имя таблицы агрегации.
    @rtype: C{float}
    @return: Возвращает накопленную сумму к определенной дате по году.
    """
    year, month, day = map(lambda x: int(x), date.split('.'))
    root = metaObj.getRoot()
    summa, kol = 0, 0
    yearObj = root[str(year)]
    path = metaObj.getPath()
    
    #   Вычисляем сумму по полным месяцам
    for mnth in range(month-1):
        cod_month = 'm'+('0'+str(mnth+1))[-2:]
        if cod_month in yearObj:
            obj = yearObj[cod_month].findObject(path[2:])
            
            # s, k = getattr(yearObj[cod_mnth].value, tableName)['summa']
            if obj:
                s, k = getattr(obj.value, tableName)['summa']
                summa += s
                kol += k
            
    #   Вычисляем сумму по неполному месяцу
    cod_month = 'm'+('0'+str(month))[-2:]
    if cod_month in yearObj:
        obj = yearObj[cod_month].findObject(path[2:])
        s, k = _getMonthSumma(date, obj, tableName)
        # s, k = _getMonthSumma(date, metaObj, tableName)
        summa += s
        kol += k
    return summa, kol


def _getYearPlan(date, metaObj):
    """
    Вычисляет накопленный годовой план к определенной дате.
    
    @type date: C{string}
    @param date: Дата в виде 'yyyy.mm.dd'
    @type metaObj: C{icMetaItem}
    @param metaObj: Текущий узел дерева данных.
    @rtype: C{float}
    @return: Плановую накопленную сумму.
    """
    year, month, day = map(lambda x: int(x), date.split('.'))
    path = metaObj.getPath()
    root = metaObj.getRoot()
    summa = 0
    yearObj = root[str(year)]
    
    #   Вычисляем план по полным месяцам
    for mnth in range(month-1):
        cod_month = 'm%02d' % (mnth+1)  # 'm'+('0'+str(mnth+1))[-2:]
        if cod_month in yearObj:
            obj = yearObj[cod_month].findObject(path[2:])
            if obj:
                s = obj.value.summa
                summa += s
            
    #   Вычисляем сумму по неполному месяцу
    cod_month = 'm%02d' % month     # 'm'+('0'+str(month))[-2:]
    if cod_month in yearObj:
        s = _getMonthPlan(date, metaObj)
        summa += s
    return summa


def _getYearKolPlan(date, metaObj):
    """
    Вычисляет накопленный годовой план к определенной дате.
    
    @type date: C{string}
    @param date: Дата в виде 'yyyy.mm.dd'
    @type metaObj: C{icMetaItem}
    @param metaObj: Текущий узел дерева данных.
    @rtype: C{float}
    @return: Плановую накопленную сумму.
    """
    year, month, day = map(lambda x: int(x), date.split('.'))
    path = metaObj.getPath()
    root = metaObj.getRoot()
    summa = 0
    yearObj = root[str(year)]
    
    #   Вычисляем план по полным месяцам
    for mnth in range(month-1):
        cod_month = 'm'+('0'+str(mnth+1))[-2:]
        if cod_month in yearObj:
            obj = yearObj[cod_month].findObject(path[2:])
            if obj:
                s = obj.value.kol
                summa += s
            
    #   Вычисляем сумму по неполному месяцу
    cod_month = 'm'+('0'+str(month))[-2:]
    if cod_month in yearObj:
        s = _getMonthKolPlan(date, metaObj)
        summa += s
    return summa


def _getStatisticYear(metaObj, tableName, dateLst=None):
    """
    Подготавливаем статистику за год.
    
    @type metaObj: C{icMetaItem}
    @param metaObj: Текущий узел дерева данных.
    @type tableName: C{string}
    @param tableName: Имя таблицы агрегации.
    @type dateLst: C{list}
    @param dateLst: Список дат, по которым собирается статистика.
    """
    if dateLst:
        lst = dateLst
        lst.sort()
    else:
        obj = getattr(metaObj.value, tableName)
        lst = obj.keys()
        lst.sort()
        lst = lst[:-1]
        
    data = range(len(lst))
    kol_data = range(len(lst))
    
    for i, tdate in enumerate(lst):
        summa, kol = _getYearSumma(tdate, metaObj, tableName)
        plan = _getYearPlan(tdate, metaObj)
        kol_plan = _getYearKolPlan(tdate, metaObj)
        data[i] = (tdate, summa, plan)
        kol_data[i] = (tdate, kol, kol_plan)
    return data, kol_data


# @ic_proccess_dlg.proccess_noparent_deco_auto
def _getStatisticYearSumma(metaObj, tableName, dateLst=None):
    """
    Подготавливаем статистику за год по суммам.
    
    @type metaObj: C{icMetaItem}
    @param metaObj: Текущий узел дерева данных.
    @type tableName: C{string}
    @param tableName: Имя таблицы агрегации.
    @type dateLst: C{list}
    @param dateLst: Список дат, по которым собирается статистика.
    """
    if dateLst:
        lst = dateLst
        lst.sort()
    else:
        obj = getattr(metaObj.value, tableName)
        lst = obj.keys()
        lst.sort()
        lst = lst[:-1]
        
    data = range(len(lst))
    # kol_data = range(len(lst))
    
    for i, tdate in enumerate(lst):
        summa, kol = _getYearSumma(tdate, metaObj, tableName)
        plan = _getYearPlan(tdate, metaObj)
        # kol_plan = _getYearKolPlan(tdate, metaObj)
        data[i] = (tdate, summa, plan)
        # kol_data[idx] = (tdate, kol, kol_plan)
    return data


# @ic_proccess_dlg.proccess_noparent_deco_auto
def _getStatisticYearKol(metaObj, tableName, dateLst=None):
    """
    Подготавливаем статистику за год по количеству.
    
    @type metaObj: C{icMetaItem}
    @param metaObj: Текущий узел дерева данных.
    @type tableName: C{string}
    @param tableName: Имя таблицы агрегации.
    @type dateLst: C{list}
    @param dateLst: Список дат, по которым собирается статистика.
    """
    if dateLst:
        lst = dateLst
        lst.sort()
    else:
        obj = getattr(metaObj.value, tableName)
        lst = obj.keys()
        lst.sort()
        lst = lst[:-1]
        
    # data = range(len(lst))
    kol_data = range(len(lst))
    
    for i, tdate in enumerate(lst):
        summa, kol = _getYearSumma(tdate, metaObj, tableName)
        # plan = _getYearPlan(tdate, metaObj)
        kol_plan = _getYearKolPlan(tdate, metaObj)
        # data[idx] = (tdate, summa, plan)
        kol_data[i] = (tdate, kol, kol_plan)
    
    return kol_data


# @ic_proccess_dlg.proccess_noparent_deco_auto
def _getStatisticIspYearSumma(metaObj, dateLst=None):
    """
    """
    rlz_year_data = _getStatisticYearSumma(metaObj, 'zayavki', dateLst)
    year_data = _getStatisticYearSumma(metaObj, 'analitic', dateLst)
    return _unionStatistic(rlz_year_data, year_data)


# @ic_proccess_dlg.proccess_noparent_deco_auto
def _getStatisticIspYearKol(metaObj, dateLst=None):
    """
    """
    rlz_year_data = _getStatisticYearKol(metaObj, 'zayavki', dateLst)
    year_data = _getStatisticYearKol(metaObj, 'analitic', dateLst)
    return _unionStatistic(rlz_year_data, year_data)


def _getTypeFactor(metaObj, plan):
    """
    Возвращает типовой множетель индикатора.
    """
    if metaObj:
        if 10000 < plan <= 10000000:
            return 1000
        elif plan > 10000000:
            return 1000000
        else:
            return 1


def _getDaysLst(date1, date2):
    """
    Возвращает список дат между двумя датами.
    """
    
    tz = timezone('US/Pacific')
    frmt = dates.DateFormatter('%Y.%m.%d', tz)
    delta = datetime.timedelta(days=1)

    y2, m2, d2 = [int(x) for x in date2.split('.')]
    if not date1:
        y1, m1, d1 = (y2, 1, 1)
    else:
        y1, m1, d1 = [int(x) for x in date1.split('.')]
    
    t1 = datetime.datetime(y1, m1, d1, tzinfo=tz)
    t2 = datetime.datetime(y2, m2, d2, tzinfo=tz)
    dts = dates.drange(t1, t2, delta)
    dLst = [frmt(t) for t in dts]
    return dLst


def _unionStatistic(valLst, planLst):
    """
    """
    keyValLst = [r[0] for r in valLst]
    keyPlanLst = [r[0] for r in planLst]
    valDict = dict([(r[0], (r[1], r[2])) for r in valLst])
    planDict = dict([(r[0], (r[1], r[2])) for r in planLst])
    
    keyLst = list(set(keyValLst) | set(keyPlanLst))
    keyLst.sort()
    data = range(len(keyLst))
    
    for i, key in enumerate(keyLst):
        if key in valDict:
            val = valDict[key][0]
        else:
            val = 0
        
        if key in planDict:
            plan = planDict[key][0]
        else:
            plan = 0
        
        data[i] = (key, val, plan)
    
    return data


def getIndexState(value, color_zones):
    """
    """


def getMonitorState(metaObj):
    """
    Возвращает оценку состояния группы индикаторов. Оцениваем реализацию и
    исполнение заявок.

    @type metaObj: C{icMetaItem}
    @param metaObj: Указатель на узел дерева данных.
    """
    # --- Устанавливаем текущую дату
    pathLst = metaObj.getPath()
    year = int(pathLst[0])

    if len(pathLst) > 1:
        month = int(pathLst[1][1:])
        
    day = wx.DateTime.GetNumberOfDaysInMonth(month-1, year)
    # year, month, day = self.SetPanelDate(int(year), month, day)
    tdate = '%s.%s.%s' % (year, ('0'+str(month))[-2:], ('0'+str(day))[-2:])
    # print ' ... tdate:', tdate
    st = [0, 0, 0]
    # --- Реализация
    # Реализация за день
#    if tdate in metaObj.value.analitic.keys():
#        summa, kol = metaObj.value.analitic[tdate]
#        plan = calc_plan.getDayPlanValue(tdate, metaObj)
#        st[0] = icarrowindicator.GetStateIndx(summa, 0, 2*plan, metaObj.value.color_zones)+1
        
    # Устанавливаем индикаторы по реализации на месяц
    summa, kol = _getMonthSumma(tdate, metaObj, 'analitic')
    plan = _getMonthPlan(tdate, metaObj)
    
    if summa:
        st[1] = icarrowindicator.GetStateIndx(summa, 0, 2*plan, metaObj.value.color_zones)+1
    
    # Устанавливаем индикаторы по реализации на год
    summa, kol = _getYearSumma(tdate, metaObj, 'analitic')
    plan = _getYearPlan(tdate, metaObj)
    if summa:
        st[2] = icarrowindicator.GetStateIndx(summa, 0, 2*plan, metaObj.value.color_zones)+1
    
    return st[1:]


class IStdIndicatorPanel(icobjectinterface.icObjectInterface):
    """
    Интерфейс к панели мониторинга реализации и исполнения заявок по видам продукции.
    """
    def __init__(self, parent, metaObj=None):
        """
        Конструктор интерфейса.
        
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type metaObj: C{icMetaItem}
        @param metaObj: Указатель на метаобъект классификатора мониторов.
        """
        self._res = copy.deepcopy(resource)
        self.metaObj = metaObj
        #   Вызываем конструктор базового класса
        icobjectinterface.icObjectInterface.__init__(self, parent, self._res)

    def ChangeTypCod(self):
        """
        Изменяет типы и коды наблюдаемых параметров у всех индикаторов.
        """
        lst = self.GetIndicatorResList()
        for res in lst:
            res['cod'] = self.cod
            res['typPar'] = self.typ
        
    def ChangeViewName(self):
        """
        Изменяет имена представлений у индикаторов.
        """
        lst = self.GetIndicatorResList()
        for res in lst:
            if 'IspZajav' in res['name']:
                vn = genMonitor.genViewRealizeName(self.typ, self.cod)
            elif 'Zajav' in res['name']:
                vn = genMonitor.genViewZayavkiName(self.typ, self.cod)
            elif 'Realiz' in res['name']:
                vn = genMonitor.genViewRealizeName(self.typ, self.cod)
            
            res['source'] = vn
           
    def GetEI(self, metaObj=None):
        """
        Определяет единицы измерения количества. Если на узле они не определены,
        то рекурсивно ищем в родительских узлах.
        
        @type metaObj: C{icMetaItem}
        @param metaObj: Текущий узел дерева данных.
        @retrun: Единицы измерения количества.
        """
        if not metaObj:
            metaObj = self.metaObj
            
        prnt = metaObj.getItemParent()
        
        if metaObj.isRoot():
            return ''
        elif metaObj.value.ei:
            return metaObj.value.ei
        elif prnt:
            return self.GetEI(prnt)
        else:
            return metaObj.value.ei
        
    def GetTypeFactor(self, plan):
        """
        Возвращает типовой множетель индикатора.
        """
        return _getTypeFactor(self.metaObj, plan)
#        if self.metaObj:
#            if plan > 10000 and plan <= 10000000:
#                return 1000
#            elif plan > 10000000:
#                return 1000000
#            else:
#                return 1
                
    def GetIndicatorResList(self):
        """
        Возвращет список всех ресурсов индикаторов.
        """
        lst = icdataset.findResTypeLst(self._res, 'ArrowIndicator')
        # print '@@@@@>>> Indicator Names:', map(lambda x: x['name'], lst)
        return lst
    
    def GetNameRes(self, name):
        """
        Возвращает ресурс по имени компонента.
        """
        return icdataset.findResName(self._res, name)
    
    def GetObjCod(self):
        """
        Возвращает код наблюдаемого объекта.
        """
        return self.cod

    def GetObjTyp(self):
        """
        Возвращает тип наблюдаемого объекта.
        """
        return self.typ
        
    def GetStatisticDay(self, metaObj, tableName):
        """
        """
        obj = getattr(metaObj.value, tableName)
        lst = obj.keys()
        lst.sort()
        lst = lst[:-1]
        data = range(len(lst))
        kol_data = range(len(lst))
        
        for i, tdate in enumerate(lst):
            summa, kol = obj[tdate]
            plan = calc_plan.getDayPlanValue(tdate, metaObj)
            kol_plan = calc_plan.getDayPlanKol(tdate, metaObj)
            
#            if summa==0 or kol==0:
#                kol, kol_plan = 0,0
#            else:
#                kol_plan = plan/(summa/kol)
                
            data[i] = (tdate, summa, plan)
            kol_data[i] = (tdate, kol, kol_plan)
        
        return data, kol_data

    def GetStatisticMonth(self, metaObj, tableName):
        """
        """
        obj = getattr(metaObj.value, tableName)
        lst = obj.keys()
        lst.sort()
        lst = lst[:-1]
        data = range(len(lst))
        kol_data = range(len(lst))
        
        for i, tdate in enumerate(lst):
            summa, kol = self.GetMonthSumma(tdate, metaObj, tableName)
            plan = self.GetMonthPlan(tdate, metaObj)
            kol_plan = self.GetMonthKolPlan(tdate, metaObj)
#            if summa==0 or kol==0:
#                kol, kol_plan = 0,0
#            else:
#                kol_plan = plan/(summa/kol)
                
            data[i] = (tdate, summa, plan)
            kol_data[i] = (tdate, kol, kol_plan)
        
        return data, kol_data

    def GetStatisticYear(self, metaObj, tableName, dateLst=None):
        """
        Подготавливаем статистику за год.
        
        @type metaObj: C{icMetaItem}
        @param metaObj: Текущий узел дерева данных.
        @type tableName: C{string}
        @param tableName: Имя таблицы агрегации.
        @type dateLst: C{list}
        @param dateLst: Список дат, по которым собирается статистика.
        """
        return _getStatisticYear(metaObj, tableName, dateLst=None)
#        if dateLst:
#            lst = dateLst
#            lst.sort()
#        else:
#            obj = getattr(metaObj.value, tableName)
#            lst = obj.keys()
#            lst.sort()
#            lst = lst[:-1]
#
#        data = range(len(lst))
#        kol_data = range(len(lst))
#
#        for idx, tdate in enumerate(lst):
#            summa, kol = self.GetYearSumma(tdate, metaObj, tableName)
#            plan = self.GetYearPlan(tdate, metaObj)
#            kol_plan = self.GetYearKolPlan(tdate, metaObj)
#            data[idx] = (tdate, summa, plan)
#            kol_data[idx] = (tdate, kol, kol_plan)
#
#        return (data, kol_data)

    def UnionStatistic(self, valLst, planLst):
        """
        """
        keyValLst = [r[0] for r in valLst]
        keyPlanLst = [r[0] for r in planLst]
        valDict = dict([(r[0], (r[1], r[2])) for r in valLst])
        planDict = dict([(r[0], (r[1], r[2])) for r in planLst])
        
        keyLst = list(set(keyValLst) | set(keyPlanLst))
        keyLst.sort()
        data = range(len(keyLst))
        
        for i, key in enumerate(keyLst):
            if key in valDict:
                val = valDict[key][0]
            else:
                val = 0
            
            if key in planDict:
                plan = planDict[key][0]
            else:
                plan = 0
            
            data[i] = (key, val, plan)
        
        return data
        
    def GetMonthSumma(self, date, metaObj, tableName):
        """
        Вычисляет накопленную сумму на определенную дату.

        @type date: C{string}
        @param date: Дата в виде 'yyyy.mm.dd'
        @type metaObj: C{icMetaItem}
        @param metaObj: Текущий узел дерева данных.
        @type tableName: C{string}
        @param tableName: Имя таблицы агрегации.
        @rtype: C{float}
        @return: Возвращает накопленную сумму к определенной дате по месяцу.
        """
        return _getMonthSumma(date, metaObj, tableName)
        
    def GetMonthPlan(self, date, metaObj):
        """
        Вычисляет накопленную плановую сумму на определенную дату.

        @type date: C{string}
        @param date: Дата в виде 'yyyy.mm.dd'
        @type metaObj: C{icMetaItem}
        @param metaObj: Текущий узел дерева данных.
        @rtype: C{float}
        @return: Плановую накопленную сумму.
        """
        return _getMonthPlan(date, metaObj)

    def GetMonthKolPlan(self, date, metaObj):
        """
        Вычисляет накопленную плановую сумму на определенную дату.

        @type date: C{string}
        @param date: Дата в виде 'yyyy.mm.dd'
        @type metaObj: C{icMetaItem}
        @param metaObj: Текущий узел дерева данных.
        @rtype: C{float}
        @return: Плановую накопленную сумму.
        """
        return _getMonthKolPlan(date, metaObj)
        
    def GetYearSumma(self, date, metaObj, tableName):
        """
        Вычисляет накопленную годовую сумму к определенной дате.
        
        @type date: C{string}
        @param date: Дата в виде 'yyyy.mm.dd'
        @type metaObj: C{icMetaItem}
        @param metaObj: Текущий узел дерева данных.
        @type tableName: C{string}
        @param tableName: Имя таблицы агрегации.
        @rtype: C{float}
        @return: Возвращает накопленную сумму к определенной дате по году.
        """
        return _getYearSumma(date, metaObj, tableName)
        
    def GetYearPlan(self, date, metaObj):
        """
        Вычисляет накопленный годовой план к определенной дате.
        
        @type date: C{string}
        @param date: Дата в виде 'yyyy.mm.dd'
        @type metaObj: C{icMetaItem}
        @param metaObj: Текущий узел дерева данных.
        @rtype: C{float}
        @return: Плановую накопленную сумму.
        """
        return _getYearPlan(date, metaObj)

    def GetYearKolPlan(self, date, metaObj):
        """
        Вычисляет накопленный годовой план к определенной дате.
        
        @type date: C{string}
        @param date: Дата в виде 'yyyy.mm.dd'
        @type metaObj: C{icMetaItem}
        @param metaObj: Текущий узел дерева данных.
        @rtype: C{float}
        @return: Плановую накопленную сумму.
        """
        return _getYearKolPlan(date, metaObj)

    ###BEGIN EVENT BLOCK
    
    def OnToolRefresh(self, evt):
        """
        Функция обрабатывает нажатие кнопки <Refresh> в панели инструментов.
        """
        if self.metaObj and not self.metaObj.isRoot():
            month = self.GetNameObj('currentDate').GetValue().GetMonth()
            day = self.GetNameObj('currentDate').GetValue().GetDay()
            
            if self.metaObj.value.metatype == 'mYear':
                self.LoadData(month=month+1, day=day)
            else:
                self.LoadData(day=day)

        return None
    
    def OnColorFunc(self, evt):
        """
        Функция обрабатывает событие <?>.
        """
        self.GetNameObj('MainSZR').Layout()
        self.GetNameObj('MainIndicatorPanel').Refresh()
        
    ###END EVENT BLOCK

    def LoadIndicator(self, name, summa, plan, label='', ei=None):
        """
        Функция загружает заданый индикатор.
        """
        obj = self.GetNameObj(name)
        if obj and self.metaObj:
            
            # По необходимости устанавливаем заголовок индикатора
            if ei:
                obj.SetLabel('%s (%s)' % (label, ei))
                obj.ei = ei
            else:
                obj.SetLabel('%s (%s)' % (label, obj.ei))

            factor = self.GetTypeFactor(2*plan)
            obj.colorRegions = self.metaObj.value.color_zones
            obj.SetState(summa, plan, factor=factor)
            return True

        return False
        
    def LoadData(self, month=None, day=None):
        """
        Функция обновления данных на мониторе.
        """
        if self.metaObj and not self.metaObj.isRoot():
            # --- Устанавливаем текущую дату
            pathLst = self.metaObj.getPath()
            year = int(pathLst[0])
            # month = None
            if len(pathLst) > 1:
                month = int(pathLst[1][1:])
            
            print(' :::: date:', year, month, day)
            year, month, day = self.SetPanelDate(int(year), month, day)
            tdate = '%s.%s.%s' % (year, ('0'+str(month))[-2:], ('0'+str(day))[-2:])
            # print ' :::: date:', tdate
            _ei = self.GetEI()
            # --- Устанавливаем индикаторы по заявкам
            # Устанавливаем индикаторы по заявкам на день
            if tdate in self.metaObj.value.zayavki.keys():
                summa, kol = self.metaObj.value.zayavki[tdate]
                plan = calc_plan.getDayPlanValue(tdate, self.metaObj)
                plan_kol = calc_plan.getDayPlanKol(tdate, self.metaObj)

                self.LoadIndicator('dayZajav', summa, plan, 'На тек. дату')
                self.LoadIndicator('dayZajavMass', kol, plan_kol, 'На тек. дату', _ei)
            else:
                self.GetNameObj('dayZajav').SetValue(0)
                self.GetNameObj('dayZajavMass').SetValue(0)

            #   Подготавливаем данные для графика
            data, kol_data = self.GetStatisticDay(self.metaObj, 'zayavki')
            self.GetNameObj('dayZajav').SetStatisticBuff(data)
            self.GetNameObj('dayZajavMass').SetStatisticBuff(kol_data)
            
            # Устанавливаем индикаторы по заявкам на месяц
            summa, kol = self.GetMonthSumma(tdate, self.metaObj, 'zayavki')
            plan = self.GetMonthPlan(tdate, self.metaObj)
            plan_kol = self.GetMonthKolPlan(tdate, self.metaObj)

            self.LoadIndicator('monthZajav', summa, plan, 'С нач. месяца')
            if plan_kol == 0 and kol == 0:
                self.GetNameObj('monthZajavMass').SetValue(0)
            else:
                self.LoadIndicator('monthZajavMass', kol, plan_kol, 'С нач. месяца', _ei)
            
            #   Подготавливаем данные для графика
            mnth_data, mnth_kol_data = self.GetStatisticMonth(self.metaObj, 'zayavki')
            self.GetNameObj('monthZajav').SetStatisticBuff(mnth_data)
            self.GetNameObj('monthZajavMass').SetStatisticBuff(mnth_kol_data)

            # Устанавливаем индикаторы по заявкам на год
            summa, kol = self.GetYearSumma(tdate, self.metaObj, 'zayavki')
            plan = self.GetYearPlan(tdate, self.metaObj)
            plan_kol = self.GetYearKolPlan(tdate, self.metaObj)

            self.LoadIndicator('yearZajav', summa, plan, 'С нач. года')
            if plan_kol == 0 and kol == 0:
                self.GetNameObj('yearZajavMass').SetValue(0)
            else:
                self.LoadIndicator('yearZajavMass', kol, plan_kol, 'С нач. года', _ei)

            #   Подготавливаем данные для графика
            lstDays = _getDaysLst(None, tdate)
            self.GetNameObj('yearZajav').SetStatisticFuncPar(_getStatisticYearSumma,
                                            self.metaObj, 'zayavki', lstDays)
            self.GetNameObj('yearZajavMass').SetStatisticFuncPar(_getStatisticYearKol,
                                            self.metaObj, 'zayavki', lstDays)

            # --- Устанавливаем индикаторы по реализации
            # Устанавливаем индикаторы по реализации на день
            if tdate in self.metaObj.value.analitic.keys():
                summa, kol = self.metaObj.value.analitic[tdate]
                plan = calc_plan.getDayPlanValue(tdate, self.metaObj)
                plan_kol = calc_plan.getDayPlanKol(tdate, self.metaObj)

                self.LoadIndicator('dayRealiz', summa, plan, 'На тек. дату')
                self.LoadIndicator('dayRealizMass', kol, plan_kol, 'На тек. дату', _ei)
            else:
                self.GetNameObj('dayRealiz').SetValue(0)
                self.GetNameObj('dayRealizMass').SetValue(0)

            #   Подготавливаем данные для графика
            rlz_data, rlz_kol_data = self.GetStatisticDay(self.metaObj, 'analitic')
            self.GetNameObj('dayRealiz').SetStatisticBuff(rlz_data)
            self.GetNameObj('dayRealizMass').SetStatisticBuff(rlz_kol_data)
            
            # Устанавливаем индикаторы по реализации на месяц
            summa, kol = self.GetMonthSumma(tdate, self.metaObj, 'analitic')
            plan = self.GetMonthPlan(tdate, self.metaObj)
            plan_kol = self.GetMonthKolPlan(tdate, self.metaObj)
            
            self.LoadIndicator('monthRealiz', summa, plan, 'С нач. месяца')
            if plan_kol == 0 and kol == 0:
                self.GetNameObj('monthRealizMass').SetValue(0)
            else:
                self.LoadIndicator('monthRealizMass', kol, plan_kol, 'С нач. месяца', _ei)

            #   Подготавливаем данные для графика
            rlz_mnth_data, rlz_mnth_kol_data = self.GetStatisticMonth(self.metaObj, 'analitic')
            self.GetNameObj('monthRealiz').SetStatisticBuff(rlz_mnth_data)
            self.GetNameObj('monthRealizMass').SetStatisticBuff(rlz_mnth_kol_data)
                
            # Устанавливаем индикаторы по реализации на год
            summa, kol = self.GetYearSumma(tdate, self.metaObj, 'analitic')
            plan = self.GetYearPlan(tdate, self.metaObj)
            plan_kol = self.GetYearKolPlan(tdate, self.metaObj)
            
            self.LoadIndicator('yearRealiz', summa, plan, 'С нач. года')
            if plan_kol == 0 and kol == 0:
                self.GetNameObj('yearRealizMass').SetValue(0)
            else:
                self.LoadIndicator('yearRealizMass', kol, plan_kol, 'С нач. года', _ei)

            #   Подготавливаем данные для графика
            self.GetNameObj('yearRealiz').SetStatisticFuncPar(_getStatisticYearSumma,
                                        self.metaObj, 'analitic', lstDays)
            self.GetNameObj('yearRealizMass').SetStatisticFuncPar(_getStatisticYearKol,
                                        self.metaObj, 'analitic', lstDays)

            # --- Устанавливаем индикаторы по исполнению заявок
            # Устанавливаем индикаторы по исполнению заявок за день
            if self.metaObj.value.zayavki.has_key(tdate):
                if self.metaObj.value.analitic.has_key(tdate):
                    summa, kol = self.metaObj.value.analitic[tdate]
                else:
                    summa, kol = 0, 0
                    
                plan, plan_kol = self.metaObj.value.zayavki[tdate]
                self.LoadIndicator('dayIspZajav', summa, plan, 'На тек. дату')
                self.LoadIndicator('dayIspZajavMass', kol, plan_kol, 'На тек. дату', _ei)
            else:
                self.GetNameObj('dayIspZajav').SetValue(0)
                self.GetNameObj('dayIspZajavMass').SetValue(0)

            #   Подготавливаем данные для графика
            isp_data = self.UnionStatistic(rlz_data, data)
            isp_kol_data = self.UnionStatistic(rlz_kol_data, kol_data)
            self.GetNameObj('dayIspZajav').SetStatisticBuff(isp_data)
            self.GetNameObj('dayIspZajavMass').SetStatisticBuff(isp_kol_data)
            
            # Устанавливаем индикаторы по исполнению заявок за месяц
            summa, kol = self.GetMonthSumma(tdate, self.metaObj, 'analitic')
            plan, plan_kol = self.GetMonthSumma(tdate, self.metaObj, 'zayavki')

            if plan == 0 or summa == 0:
                self.GetNameObj('monthIspZajav').SetValue(0)
            else:
                self.LoadIndicator('monthIspZajav', summa, plan, 'С нач. месяца')
                
            if kol == 0 or plan_kol==0:
                self.GetNameObj('monthIspZajavMass').SetValue(0)
            else:
                self.LoadIndicator('monthIspZajavMass', kol, plan_kol, 'С нач. месяца', _ei)

            #   Подготавливаем данные для графика
            isp_data = self.UnionStatistic(rlz_mnth_data, mnth_data)
            isp_kol_data = self.UnionStatistic(rlz_mnth_kol_data, mnth_kol_data)
            self.GetNameObj('monthIspZajav').SetStatisticBuff(isp_data)
            self.GetNameObj('monthIspZajavMass').SetStatisticBuff(isp_kol_data)
                
            # Устанавливаем индикаторы по исполнению заявок за год
            summa, kol = self.GetYearSumma(tdate, self.metaObj, 'analitic')
            plan, plan_kol = self.GetYearSumma(tdate, self.metaObj, 'zayavki')
            
            if plan == 0 or summa == 0:
                self.GetNameObj('yearIspZajav').SetValue(0)
            else:
                self.LoadIndicator('yearIspZajav', summa, plan, 'С нач. года')
                
            if kol == 0 or plan_kol == 0:
                self.GetNameObj('yearIspZajavMass').SetValue(0)
            else:
                self.LoadIndicator('yearIspZajavMass', kol, plan_kol, 'С нач. года', _ei)

            #   Подготавливаем данные для графика
            self.GetNameObj('yearIspZajav').SetStatisticFuncPar(_getStatisticIspYearSumma,
                                                                self.metaObj, lstDays)
            self.GetNameObj('yearIspZajavMass').SetStatisticFuncPar(_getStatisticIspYearKol,
                                                                    self.metaObj, lstDays)

    def SaveData(self):
        """
        """
        pass

    def SetPanelDate(self, year, month=None, day=None):
        """
        Устанавливает текущую дату на панели.
        """
        #   Определяем месяц
        omonth = month
        if month is None:
            if year != wx.DateTime.GetCurrentYear():
                month = 12
            else:
                month = wx.DateTime.GetCurrentMonth()+1
                
        #   Определяем год
        if day is None:
            # if month <> wx.DateTime.GetCurrentMonth() and year <> wx.DateTime.GetCurrentYear():
            if year != wx.DateTime.GetCurrentYear():
                # print 'typ month, year:', month-1, year
                day = wx.DateTime.GetNumberOfDaysInMonth(month-1, year)
            elif omonth is not None:
                day = wx.DateTime.GetNumberOfDaysInMonth(month-1, year)
            else:
                day = datetime.date.today().day
        
        # print 'Curretn Date', day, month-1, year
        dt = wx.DateTimeFromDMY(day, month-1, year)
        # print ' ::::: Set Curretn Panel Date:', dt
        self.GetNameObj('currentDate').SetValue(dt)
        return year, month, day


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


def test2():
    """
    """
    lst = _getDaysLst('2006.01.01', '2006.02.07')
    lst.sort()
    print(lst)
#    for t in lst:
#        print [int(x) for x in t.split('-')]


if __name__ == '__main__':
    test2()
