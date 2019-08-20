#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import wx
import ic.components.icResourceParser as prs
from ic.utils import util

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource = {'activate': 1, 'show': 1, 'keyDown': u'None', 'border': 0, 'size': (-1, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'layout': u'vertical', 'win2': {'activate': 1, 'show': 1, '__attr_types__': {0: ['alias', 'moveAfterInTabOrder', 'name', 'type'], 7: ['flag', 'style'], 8: ['foregroundColor', 'backgroundColor'], 10: ['position', 'span'], 11: ['size'], 12: ['source', 'activate', 'keyDown', 'show', 'recount', 'refresh', 'init_expr'], 40: ['border', 'proportion']}, 'recount': None, 'keyDown': None, 'border': 0, '__parent__': {'__events__': None, 'moveAfterInTabOrder': '', 'foregroundColor': None, 'name': 'widget', 'show': 1, '__attr_types__': {0: ['alias', 'moveAfterInTabOrder', 'name', 'type'], 7: ['flag', 'style'], 8: ['foregroundColor', 'backgroundColor'], 10: ['position', 'span'], 11: ['size'], 12: ['source', 'activate', 'keyDown', 'show', 'recount', 'refresh', 'init_expr'], 40: ['border', 'proportion']}, 'refresh': None, '__version__icwidget': '0.0.0.0', 'source': None, 'keyDown': None, 'backgroundColor': None, 'recount': None, 'type': 'Widget', '__parent__': {'__styles__': None, 'style': 0, 'activate': 1, 'span': (1, 1), 'name': 'base', 'alias': None, '__version__base': '0.0.0.0', '__attr_types__': {0: ['alias', 'name', 'type'], 7: ['flag', 'style'], 40: ['border', 'proportion'], 10: ['position', 'span'], 11: ['size'], 12: ['activate', 'init_expr']}, '_uuid': None, 'proportion': 0, '__item_id': None, 'flag': 0, 'init_expr': None, 'type': 'Base', 'position': (-1, -1), '__version__': '0.0.0.0', 'border': 0, '__doc__': None, 'size': (-1, -1)}}, 'size': (-1, -1), 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), '__version__base': '0.0.0.0', 'proportion': 0, 'source': None, 'backgroundColor': None, '__version__': '0.0.0.0', 'type': 'Panel', '__doc__': None, '__styles__': None, '__events__': None, '__item_id': 38, 'onClose': None, '_uuid': 'd5546fd11473ff7187d1b83f8be2c1fb', 'style': 524288, 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'__styles__': None, 'activate': 1, '__attr_types__': {0: ['alias', 'name', 'type'], 7: ['flag', 'style'], 40: ['border', 'vgap, hgap', 'proportion'], 10: ['position', 'span'], 11: ['size'], 12: ['activate', 'init_expr']}, 'border': 0, '__parent__': {'hgap': 0, 'span': (1, 1), 'name': 'DefaultName', '__attr_types__': {0: ['alias', 'name', 'type'], 7: ['flag', 'style'], 40: ['border', 'vgap, hgap', 'proportion'], 10: ['position', 'span'], 11: ['size'], 12: ['activate', 'init_expr']}, 'vgap': 0, 'child': [], 'position': (0, 0), 'type': 'Sizer', '__parent__': {'__styles__': None, 'style': 0, 'activate': 1, 'span': (1, 1), 'name': 'base', 'alias': None, '__version__base': '0.0.0.0', '__attr_types__': {0: ['alias', 'name', 'type'], 7: ['flag', 'style'], 40: ['border', 'proportion'], 10: ['position', 'span'], 11: ['size'], 12: ['activate', 'init_expr']}, '_uuid': None, 'proportion': 0, '__item_id': None, 'flag': 0, 'init_expr': None, 'type': 'Base', 'position': (-1, -1), '__version__': '0.0.0.0', 'border': 0, '__doc__': None, 'size': (-1, -1)}}, 'size': (-1, -1), 'style': 0, 'layout': 'vertical', '__version__base': '0.0.0.0', 'proportion': 0, '__version__': '0.0.0.0', 'type': 'BoxSizer', '__doc__': None, 'hgap': 0, '__item_id': 39, '_uuid': '059236b3146ec17c046180e09de84d6e', 'flag': 0, 'child': [{'activate': 1, 'show': 1, '__attr_types__': {0: ['alias', 'moveAfterInTabOrder', 'name', 'type'], 7: ['flag', 'style'], 8: ['foregroundColor', 'backgroundColor'], 10: ['position', 'span'], 11: ['size'], 12: ['source', 'activate', 'keyDown', 'show', 'recount', 'refresh', 'init_expr'], 40: ['border', 'proportion']}, 'recount': None, 'refresh': None, 'border': 0, '__parent__': {'__events__': None, 'moveAfterInTabOrder': '', 'foregroundColor': None, 'name': 'widget', 'show': 1, '__attr_types__': {0: ['alias', 'moveAfterInTabOrder', 'name', 'type'], 7: ['flag', 'style'], 8: ['foregroundColor', 'backgroundColor'], 10: ['position', 'span'], 11: ['size'], 12: ['source', 'activate', 'keyDown', 'show', 'recount', 'refresh', 'init_expr'], 40: ['border', 'proportion']}, 'refresh': None, '__version__icwidget': '0.0.0.0', 'source': None, 'keyDown': None, 'backgroundColor': None, 'recount': None, 'type': 'Widget', '__parent__': {'__styles__': None, 'style': 0, 'activate': 1, 'span': (1, 1), 'name': 'base', 'alias': None, '__version__base': '0.0.0.0', '__attr_types__': {0: ['alias', 'name', 'type'], 7: ['flag', 'style'], 40: ['border', 'proportion'], 10: ['position', 'span'], 11: ['size'], 12: ['activate', 'init_expr']}, '_uuid': None, 'proportion': 0, '__item_id': None, 'flag': 0, 'init_expr': None, 'type': 'Base', 'position': (-1, -1), '__version__': '0.0.0.0', 'border': 0, '__doc__': None, 'size': (-1, -1)}}, 'size': (-1, -1), 'style': 516, 'foregroundColor': None, 'span': (1, 1), '__version__base': '0.0.0.0', 'proportion': 0, 'source': None, 'backgroundColor': None, '__version__': '0.0.0.0', 'type': 'ToolBar', '__doc__': None, '__styles__': {'TB_DOCKABLE': 64, 'TB_HORIZONTAL': 4, 'TB_3DBUTTONS': 16, 'TB_NOICONS': 128, 'TB_VERTICAL': 8, 'TB_NOALIGN': 1024, 'TB_NODIVIDER': 512, 'TB_TEXT': 256, 'TB_FLAT': 32}, '__events__': None, '__item_id': 40, '_uuid': 'ab3eaf79939327b7da2d47ce1863b67a', 'moveAfterInTabOrder': '', 'flag': 0, 'child': [{'activate': '1', 'name': 'default_3635', 'toolType': 0, 'shortHelpString': 'icButton', '__item_id': 54, 'longHelpString': '', '_uuid': '718723df7a4ea2e37bd0609ee8a40e19', 'proportion': 0, 'pushedBitmap': None, 'bitmap': '', 'flag': 0, 'isToggle': 0, 'init_expr': None, 'label': '', 'type': 'ToolBarTool', 'OnTool': None}], 'name': 'DefaultName_3281', 'keyDown': None, '__version__icwidget': '0.0.0.0', 'alias': None, 'init_expr': None, 'position': wx.Point(139, 13), 'bitmap_size': (16, 15)}, {'activate': 1, 'show': 1, '__attr_types__': {0: ['alias', 'moveAfterInTabOrder', 'name', 'type'], 7: ['flag', 'style'], 8: ['foregroundColor', 'backgroundColor'], 10: ['position', 'span'], 11: ['size'], 12: ['source', 'activate', 'keyDown', 'show', 'recount', 'refresh', 'init_expr'], 40: ['border', 'proportion']}, 'refresh': None, 'border': 0, '__parent__': {'__events__': None, 'moveAfterInTabOrder': '', 'foregroundColor': None, 'name': 'widget', 'show': 1, '__attr_types__': {0: ['alias', 'moveAfterInTabOrder', 'name', 'type'], 7: ['flag', 'style'], 8: ['foregroundColor', 'backgroundColor'], 10: ['position', 'span'], 11: ['size'], 12: ['source', 'activate', 'keyDown', 'show', 'recount', 'refresh', 'init_expr'], 40: ['border', 'proportion']}, 'refresh': None, '__version__icwidget': '0.0.0.0', 'source': None, 'keyDown': None, 'backgroundColor': None, 'recount': None, 'type': 'Widget', '__parent__': {'__styles__': None, 'style': 0, 'activate': 1, 'span': (1, 1), 'name': 'base', '__version__base': '0.0.0.0', '__attr_types__': {0: ['name', 'type', 'alias'], 7: ['flag', 'style'], 40: ['border', 'proportion'], 10: ['position', 'span'], 11: ['size'], 12: ['activate', 'init_expr']}, 'border': 0, '_uuid': None, 'proportion': 0, '__item_id': None, 'alias': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), '__version__': '0.0.0.0', 'type': 'Base', '__doc__': None, 'size': (-1, -1)}}, 'size': (-1, -1), 'moveAfterInTabOrder': '', 'foregroundColor': None, 'layout': 'horizontal', 'alias': None, 'win2': {'activate': 1, 'show': 1, '__attr_types__': {0: ['alias', 'moveAfterInTabOrder', 'name', 'type'], 7: ['flag', 'style'], 8: ['foregroundColor', 'backgroundColor'], 10: ['position', 'span'], 11: ['size'], 12: ['source', 'activate', 'keyDown', 'show', 'recount', 'refresh', 'init_expr'], 40: ['border', 'proportion']}, 'recount': None, 'keyDown': None, 'border': 0, '__parent__': {'__events__': None, 'moveAfterInTabOrder': '', 'foregroundColor': None, 'name': 'widget', 'show': 1, '__attr_types__': {0: ['alias', 'moveAfterInTabOrder', 'name', 'type'], 7: ['flag', 'style'], 8: ['foregroundColor', 'backgroundColor'], 10: ['position', 'span'], 11: ['size'], 12: ['source', 'activate', 'keyDown', 'show', 'recount', 'refresh', 'init_expr'], 40: ['border', 'proportion']}, 'refresh': None, '__version__icwidget': '0.0.0.0', 'source': None, 'keyDown': None, 'backgroundColor': None, 'recount': None, 'type': 'Widget', '__parent__': {'__styles__': None, 'style': 0, 'activate': 1, 'span': (1, 1), 'name': 'base', 'alias': None, '__version__base': '0.0.0.0', '__attr_types__': {0: ['name', 'type', 'alias'], 7: ['flag', 'style'], 40: ['border', 'proportion'], 10: ['position', 'span'], 11: ['size'], 12: ['activate', 'init_expr']}, '_uuid': None, 'proportion': 0, '__item_id': None, 'flag': 0, 'init_expr': None, 'type': 'Base', 'position': (-1, -1), '__version__': '0.0.0.0', 'border': 0, '__doc__': None, 'size': (-1, -1)}}, 'size': (-1, -1), 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), '__version__base': '0.0.0.0', 'proportion': 0, 'source': None, 'backgroundColor': (255, 255, 255), '__version__': '0.0.0.0', 'type': 'Panel', '__doc__': None, '__styles__': None, '__events__': None, '__item_id': 53, 'onClose': None, '_uuid': '4da8375e416b1536096202cdf3c433d5', 'style': 524288, 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [], 'name': 'defaultWindow_2018', 'refresh': None, '__version__icwidget': '0.0.0.0', 'alias': None, 'init_expr': None, 'position': (-1, -1)}, 'win1': {'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (300, -1), 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), '__version__base': '0.0.0.0', 'proportion': 0, 'source': None, 'backgroundColor': None, '__version__': '0.0.0.0', 'type': 'Panel', '__doc__': None, '__item_id': 42, 'onClose': None, '_uuid': '0129fbee95dca81e705c5ced1e93ed5c', 'style': 524288, 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'style': 0, 'activate': 1, 'span': (1, 1), 'name': 'resource', '__item_id': 43, 'proportion': 0, '_uuid': '60d4d4bb5fe3e4aaa6fe07b8bcdf75dd', 'modules': {}, 'object': 'None', 'alias': 'None', 'flag': 0, 'init_expr': "from ic.components import icwidget\r\nfrom ic.utils import util\r\nfrom ic.PropertyEditor import icDefInf\r\n\r\n#   \xd0\xe5\xf1\xf3\xf0\xf1 \xf0\xee\xe4\xe8\xf2\xe5\xeb\xfc\xf1\xea\xee\xe3\xee \xea\xee\xec\xef\xee\xed\xe5\xed\xf2\xe0\r\nif not _dict_obj.has_key('parent_resource'):\r\n    _dict_obj['parent_resource'] = None\r\n\r\n#   \xc5\xf1\xeb\xe8 \xed\xe5 \xee\xef\xf0\xe5\xe4\xe5\xeb\xe5\xed \xf0\xe5\xe6\xe8\xec \xf0\xe0\xe1\xee\xf2\xfb (\xef\xf0\xee\xf1\xec\xee\xf2\xf0, \xf0\xe5\xe4\xe0\xea\xf2\xe8\xf0\xee\xe2\xe0\xed\xe8\xe5),\r\n#   \xf2\xee \xf3\xf1\xf2\xe0\xed\xe0\xe2\xeb\xe8\xe2\xe0\xe5\xec \xf0\xe5\xe6\xe8\xec \xf0\xe5\xe4\xe0\xea\xf2\xe8\xf0\xee\xe2\xed\xe8\xff.\r\nif not _dict_obj.has_key('bEditMode'):\r\n    _dict_obj['bEditMode'] = True\r\n\r\n#   \xd1\xe5\xf0\xe2\xe8\xf1\xed\xfb\xe5 \xef\xe5\xf0\xe5\xec\xe5\xed\xed\xfb\xe5\r\n_dict_obj['_last_select'] = (-1,-1)\r\n#WrapperObj.SetResource(None)\r\nprint '###SPC:', WrapperObj.getResource()\r\n", 'type': 'Import', 'position': (-1, -1), 'border': 0, 'size': (-1, -1)}, {'hgap': 0, 'style': 0, 'activate': 1, 'layout': 'vertical', 'name': 'DefaultName_1121', 'position': wx.Point(191, 25), '__item_id': 44, 'type': 'BoxSizer', '_uuid': '4a4ca30ae69f315d5afcac400a4ee0f4', 'proportion': 0, 'alias': '', 'flag': 0, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'selPageColor': (208, 207, 202), 'recount': None, 'onSelectTitle': '#   \xd4\xe8\xeb\xfc\xf2\xf0\xf3\xe5\xec \xf1\xef\xe8\xf1\xee\xea \xf1\xe2\xee\xe9\xf1\xf2\xe2 \xe2 \xe7\xe0\xe2\xe8\xf1\xe8\xec\xee\xf1\xf2\xe8 \xee\xf2 \xe7\xe0\xea\xeb\xe0\xe4\xea\xe8\r\n#   \xce\xe1\xfa\xe5\xea\xf2 resource \xff\xe2\xeb\xff\xe5\xf2\xf1\xff \xef\xe0\xf0\xe0\xec\xe5\xf2\xf0\xee\xec \xea\xeb\xe0\xf1\xf1\xe0\r\nfrom ic.components import icwidget\r\nfrom ic.utils import util\r\n\r\nindx = self.GetSelected()\r\n#resource = _dict_obj[\'resource\']\r\nresource = WrapperObj.getResource()\r\n\r\nif _dict_obj.has_key(\'PropertyGrid\'):\r\n    \r\n    grid = _dict_obj[\'PropertyGrid\']\r\n    #lst = _dict_obj[\'_pages_list_filter\'][indx]\r\n    lst = WrapperObj.GetPageAttrLst(indx)\r\n\r\n    grid.BeginBatch()\r\n    grid.resource[\'init\'] = None\r\n\r\n    #   \xd7\xe8\xf1\xf2\xe8\xec \xf1\xef\xe8\xf1\xee\xea \xe0\xf2\xf0\xe8\xe1\xf3\xf2\xee\xe2\r\n    dn = len(lst) - (grid.GetTable().GetNumberRows()-1)\r\n    num = (grid.GetTable().GetNumberRows()-1)\r\n    """\r\n    for idx in range(num):\r\n        grid.GetTable().DeleteRows(0, bAsk=False)\r\n\r\n    #   \xc4\xee\xe1\xe0\xe2\xeb\xff\xe5\xec \xed\xf3\xe6\xed\xee\xe5 \xea\xee\xeb\xe8\xf7\xe5\xf1\xf2\xe2\xee \xf1\xf2\xf0\xee\xea \xe2 \xe3\xf0\xe8\xe4\r\n    if len(lst) > 0:\r\n        grid.AddRows(len(lst))\r\n    """\r\n    if dn < 0:\r\n        for idx in range(-dn):\r\n            grid.GetTable().DeleteRows(0, bAsk=False)\r\n    elif dn > 0:\r\n        grid.AddRows(dn)\r\n    \r\n    grid = _dict_obj[\'PropertyGrid\']\r\n\r\n    #   \xc7\xe0\xef\xee\xeb\xed\xff\xe5\xec \xed\xf3\xe6\xed\xfb\xec\xe8 \xf1\xe2\xee\xe9\xf1\xf2\xe2\xe0\r\n    for indx, key in enumerate(lst):\r\n        grid.setNameValue(\'attributes\', \'  \'+key, indx)\r\n        grid.setNameValue(\'values\', str(resource[key]), indx)\r\n        grid.Update(indx)\r\n\r\n    grid.EndBatch()\r\n    grid.resource[\'init\'] = \'@False\'\r\n    ', 'titles': ['\xc1\xe0\xe7\xee\xe2\xfb\xe5', '\xc2\xe8\xe7\xf3\xe0\xeb\xfc\xed\xfb\xe5', '\xd1\xef\xe5\xf6\xe8\xe0\xeb\xfc\xed\xfb\xe5', '\xd1\xee\xe1\xfb\xf2\xe8\xff', '\xc2\xf1\xe5'], 'refresh': 'None', 'images': ['Event.png', 'Item.png', '', '', 'list.png'], 'font': {'family': 'sansSerif', 'style': 'regular', 'underline': False, 'faceName': 'Arial', 'size': 8}, 'border': 0, 'size': wx.Size(393, 27), 'moveAfterInTabOrder': '', 'foregroundColor': (128, 128, 128), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': (248, 248, 248), 'type': 'TitlesNotebook', '__item_id': 45, '_uuid': '13afb89c6e9eb040f145e8e6ddac2f80', 'style': 0, 'flag': 8192, 'child': [], 'path': "@# \xce\xef\xf0\xe5\xe4\xe5\xeb\xff\xe5\xec \xef\xf3\xf2\xfc \xe4\xee \xe1\xe8\xe1\xeb\xe8\xee\xf2\xe5\xea\xe8 \xea\xe0\xf0\xf2\xe8\xed\xee\xea\r\nimport ic.utils.resource as resource\r\n_resultEval = resource.icGetICPath()+'/imglib/common'\r\n", 'name': 'NB', 'icDelButton': 1, 'keyDown': 'None', 'alias': None, 'init_expr': 'None', 'position': wx.Point(0, 0)}, {'line_color': (192, 192, 192), 'activate': 1, 'show': 1, 'cols': [{'activate': '1', 'ctrl': '', 'pic': 'S', 'getvalue': '', 'show': '1', 'label': '', 'width': 120, 'init': None, 'valid': None, 'type': 'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '__item_id': 48, '_uuid': '23fd87416a6b09f3ca925a9314584fc5', 'activate': '1', 'init_expr': None, 'backgroundColor': (234, 234, 234), 'font': {'style': 'regular', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Arial', 'type': 'Font', 'underline': False, 'size': 8}, 'type': 'cell_attr', 'alignment': "('left', 'middle')"}, 'shortHelpString': '', '__item_id': 47, '_uuid': '7ed8b82e86d35d9e1e0dee428a03f15b', 'recount': None, 'hlp': None, 'name': 'attributes', 'setvalue': '', 'attr': 'R', 'keyDown': None, 'init_expr': None}, {'sort': None, 'activate': '1', 'attr': 'W', '_uuid': '30f54add9409a3782465da2228ca7635', 'show': '1', '__item_id': 49, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '__item_id': 50, '_uuid': '23fd87416a6b09f3ca925a9314584fc5', 'activate': '1', 'init_expr': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'ctrl': 'import ic.utils.coderror as coderror\r\nfrom ic.PropertyEditor import icDefInf\r\nimport ic.dlg.msgbox as msgbox\r\n\r\nif row >= self.GetTable().GetNumberRows()-1:\r\n    _resultEval = coderror.IC_CTRL_FAILED_IGNORE\r\nelse:\r\n    _resultEval = coderror.IC_CTRL_OK\r\n    \r\n    #   \xca\xee\xed\xf2\xf0\xee\xeb\xfc \xe2 \xf1\xee\xee\xf2\xe2\xe5\xf2\xf1\xf2\xe2\xe8\xe8 \xf1 \xf2\xe8\xef\xee\xec \xe0\xf2\xf0\xe8\xe1\xf3\xf2\xe0\r\n    _val = value\r\n    attr = self.GetTable().GetValue(row, 0)\r\n    attr = attr.strip()\r\n    typ = WrapperObj.GetPropertyType(attr)\r\n    cls = icDefInf.GetEditorClass(typ)\r\n\r\n    #print \'>>> CTRL-00 typ, attr:\', typ, attr, _val\r\n    \r\n    ret = cls.Ctrl(_val)\r\n    print \'CLASS:\', cls, typ, ret\r\n    #ret = icDefInf.ctrlVal(typ, _val)\r\n    #print \'>>> CTRL typ,ret:\', typ, ret\r\n\r\n    if typ == None:\r\n        msgbox.MsgBox(self.GetView(), \'\xc2 \xf1\xef\xe5\xf6\xe8\xf4\xe8\xea\xe0\xf6\xe8\xe8 \xed\xe5 \xee\xef\xf0\xe5\xe4\xe5\xeb\xe5\xed \xf2\xe8\xef \xe0\xf2\xf0\xe8\xe1\xf3\xf2\xe0:%s\' % _val)\r\n        _resultEval = coderror.IC_CTRL_FAILED_IGNORE\r\n    elif ret == coderror.IC_CTRL_FAILED:\r\n        msgbox.MsgBox(self.GetView(), \'\xce\xf8\xe8\xe1\xee\xf7\xed\xfb\xe9 \xf2\xe8\xef \xe7\xed\xe0\xf7\xe5\xed\xe8\xff:%s\' % _val)\r\n        _resultEval = coderror.IC_CTRL_FAILED_IGNORE\r\n    elif ret == None:\r\n        msgbox.MsgBox(self.GetView(), \'\xce\xf8\xe8\xe1\xea\xe0 \xe7\xe0\xef\xe8\xf1\xe8 \xe7\xed\xe0\xf7\xe5\xed\xe8\xff:%s\' % _val)\r\n        _resultEval = coderror.IC_CTRL_FAILED_IGNORE\r\n    #   \xc5\xf1\xeb\xe8 \xea\xee\xed\xf2\xf0\xee\xeb\xfc \xef\xf0\xee\xf8\xe5\xeb \xf3\xf1\xef\xe5\xf8\xed\xee, \xf2\xee \xf1\xee\xf5\xf0\xe0\xed\xff\xe5\xec \xe7\xed\xe0\xf7\xe5\xed\xe8\xe5 \xe2 \xf0\xe5\xf1\xf3\xf0\xf1\xed\xee\xec\r\n    #   \xee\xef\xe8\xf1\xe0\xed\xe8\xe8\r\n    else:\r\n        WrapperObj.SetProperty(attr, _val)\r\n        #print \'!!! SetProperty prop, val:\', attr, _val\r\n\', \'pic\': \'S\', \'hlp\': \'import ic.PropertyEditor.icExternalEditors as edt\r\nfrom ic.PropertyEditor import icDefInf\r\nimport ic.utils import ic_uuid\r\nimport ic.utils.resource as resource\r\n\r\nattr = self.GetTable().GetValue(row, 0)\r\nattr = attr.strip()\r\n\r\ngrid = _dict_obj[\'PropertyGrid\']\r\ntype = grid.render.GetColAttrType(attr)\r\n_val = self.GetTable().GetValue(row, 1)\r\ncls = icDefInf.GetEditorClass(type)\r\n\r\n##############################################\r\n#   \xce\xef\xf0\xe5\xe4\xe5\xeb\xff\xe5\xec \xef\xee\xe7\xe8\xf6\xe8\xfe \xe8 \xf0\xe0\xe7\xec\xe5\xf0\r\nr = grid.CellToRect(row, col)\r\ndx, dy = grid.GetScrollPixelsPerUnit()\r\nvx, vy = grid.GetViewStart()\r\nscr_x = dx*vx\r\nscr_y = dy*vy\r\nscreen_x, screen_y = wx.GetDisplaySize()\r\nsx, sy = (-1, 150)\r\npx, py = grid.ClientToScreenXY(0, r.y+20-scr_y)\r\n\r\nif py + sy > screen_y:\r\n    pos = (r.x-scr_x, r.y-scr_y-sy)\r\nelse:\r\n    pos = (r.x-scr_x, r.y+20-scr_y)\r\n##############################################\r\n"""\r\nif type == icDefInf.EDT_COLOR:\r\n    #_resultEval = edt.ColorEdtDlg(self.GetView(), _val)\r\n    _resultEval = cls.HlpDlg(self.GetView(), attr, _val, pos, (sx, sy))\r\n\r\nelif type == icDefInf.EDT_FONT:\r\n    #_resultEval = edt.FontEdtDlg(self.GetView(), _val)\r\n    _resultEval = cls.HlpDlg(self.GetView(), attr, _val, pos, (sx, sy))\r\n"""\r\nif type == icDefInf.EDT_COMBINE and grid._styles_attr.has_key(attr):\r\n    styles = grid._styles_attr[attr]\r\n    cls.SetAttrCombDict(attr, styles)\r\n    _resultEval = cls.HlpDlg(self.GetView(), attr, _val, pos=pos, size=(sx,sy))\r\n\r\nelif type == icDefInf.EDT_CHOICE and grid._lists_attr.has_key(attr):\r\n    lst = grid._lists_attr[attr]\r\n    cls.SetAttrListDict(attr, lst)\r\n    _resultEval = cls.HlpDlg(self.GetView(), attr, _val, pos=pos, size=(sx,sy), style=wx.CANCEL)\r\n\r\nelif type == icDefInf.EDT_PY_SCRIPT:\r\n    r = grid.CellToRect(row, col)\r\n    sx, sy = grid.GetSize()\r\n    #res = _dict_obj[\'resource\']\r\n    res = WrapperObj.getResource()\r\n    \r\n    if res.has_key(\'_uuid\'):\r\n        _uuid = res[\'_uuid\']\r\n    else:\r\n        _uuid = ic_uuid.get_uuid()\r\n\r\n    #prz, val, _uuid = edt.PyScriptEdtDlg(self.GetView(), attr, _val, (r.x+70, 0), (sx-r.x-70, sy), _uuid)\r\n    prz, val, _uuid = cls.HlpDlg(self.GetView(), attr, _val, pos=(r.x+70, 0), size=(sx-r.x-70, sy), uuid_attr=_uuid, bEnable=True)\r\n\r\n    #   \xce\xe1\xed\xee\xe2\xeb\xff\xe5\xec uuid\r\n    if prz:\r\n        prnt_res = WrapperObj.GetPrntResource()\r\n        resource.RefreshResUUID(res, prnt_res, _uuid)\r\n        _resultEval = val\r\n    else:\r\n        _resultEval = None\r\nelse:\r\n    _resultEval = cls.HlpDlg(self.GetView(), attr, _val, pos, (sx, sy))', 'keyDown': '', 'label': 'col', 'width': 200, 'init': 'None', 'valid': None, 'init_expr': 'None', 'shortHelpString': '', 'recount': None, 'setvalue': '', 'getvalue': '', 'type': 'GridCell', 'name': 'values'}], 'keyDown': 'if evt.GetKeyCode() == wx.WXK_DELETE:\r\n    _resultEval = False', 'border': 0, 'post_select': 'import wx.grid as grid\r\nfrom ic.PropertyEditor import icDefInf\r\nimport ic.PropertyEditor.icExternalEditors as edt\r\nimport ic.utils.resource as resource\r\n\r\n_grid = self.GetView()\r\n\r\n_row, _col = evt.GetData()\r\n#row = _grid.GetGridCursorRow()\r\n#col = _grid.GetGridCursorCol()\r\n\r\ntry:\r\n    attr = self.GetTable().GetValue(_row, 0)\r\n    attr = attr.strip()\r\n    \r\n    type = _grid.render.GetColAttrType(attr)\r\n    _val = self.GetTable().GetValue(_row, 1)\r\n    \r\n    if _col==1 and type == icDefInf.EDT_PY_SCRIPT and _dict_obj[\'_last_select\'] <> (_row, _col):\r\n        print \' COL=\', _col\r\n        r = _grid.CellToRect(_row, _col)\r\n        _dict_obj[\'_last_select\'] = (_row, _col)\r\n        sx, sy = _grid.GetSize()\r\n        res = WrapperObj.getResource()\r\n    \r\n        if res.has_key(\'_uuid\'):\r\n            _uuid = res[\'_uuid\']\r\n        else:\r\n            _uuid = ic_uuid.get_uuid()\r\n    \r\n        if _val.find(\'\\n\') >= 0:\r\n            print \'>>> Python Editor \'\r\n            prz, val, _uuid = edt.PyScriptEdtDlg(_grid, attr, _val, (r.x+70, 0), (sx-r.x-70, sy), _uuid)\r\n        \r\n            #   \xce\xe1\xed\xee\xe2\xeb\xff\xe5\xec uuid\r\n            if prz:\r\n                resource.RefreshResUUID(res, WrapperObj.GetPrntResource(), _uuid)\r\n                ret = _grid.setNameValue(\'values\', val)\r\n        else:\r\n            resource.RefreshResUUID(res, WrapperObj.GetPrntResource(), ic_uuid.get_uuid())\r\n            print \'>>> EnableCellEditControl()\'\r\n            _grid.EnableCellEditControl()\r\n            """\r\n            select_evt = grid.GridEvent(wx.NewId(), grid.wxEVT_GRID_CELL_LEFT_DCLICK, self, _row, _col)\r\n            self.GetEventHandler().AddPendingEvent(select_evt)\r\n            """\r\n    _dict_obj[\'_last_select\'] = (_row, _col)\r\n    \r\n    #\r\n    #print \'###?: POST_SELECT\', _row, _col\r\nexcept:\r\n    pass', 'size': wx.Size(220, 207), 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), 'delRec': '', 'row_height': 20, 'selected': 'import wx.grid as grid\r\nfrom ic.PropertyEditor import icDefInf\r\nimport ic.PropertyEditor.icExternalEditors as edt\r\n\r\nattr = self.GetTable().GetValue(row, 0)\r\nattr = attr.strip()\r\n\r\n_grid = self.GetView()\r\ntype = _grid.render.GetColAttrType(attr)\r\n_val = self.GetTable().GetValue(row, 1)\r\n\r\nif col == 0:\r\n    pass\r\nelif type <> icDefInf.EDT_PY_SCRIPT:\r\n    select_evt = grid.GridEvent(wx.NewId(), grid.wxEVT_GRID_CELL_LEFT_DCLICK, self, row, col)\r\n    self.GetEventHandler().AddPendingEvent(select_evt)\r\n', 'proportion': 1, 'getattr': '#import ic.PropertyEditor.icEditorGridRender as icrender\r\nimport  wx\r\nimport  wx.grid as  Grid\r\n\r\nif col == 1:\r\n    attr = self.GetView().val_col_attr\r\n    attr.IncRef()\r\n    #attr.SetReadOnly(False)\r\n    _resultEval = attr\r\nelse:\r\n    _resultEval = None\r\n\r\n', 'label': 'Grid', 'source': None, 'init': '', 'backgroundColor': None, 'fixRowSize': 0, 'type': 'GridDataset', '_uuid': '3d5cdf26440697de2c68eab04fd1ae3e', 'fixColSize': 0, 'post_del': 'None', 'post_init': 'None', 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '__item_id': 51, '_uuid': '6c62e5d9286f17d110c8db3613ae518b', 'activate': '1', 'init_expr': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': "('left', 'middle')"}, 'style': 0, 'docstr': 'ic.components.icgrid.html', 'flag': 8192, 'recount': None, 'label_attr': {'foregroundColor': (255, 255, 255), 'name': '', '__item_id': 52, '_uuid': '6c62e5d9286f17d110c8db3613ae518b', 'activate': '1', 'init_expr': None, 'backgroundColor': (100, 100, 100), 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'label_attr', 'alignment': ('left', 'middle')}, '__item_id': 46, 'name': 'PropertyGrid', 'label_height': 0, 'changed': 'None', 'refresh': 'None', 'alias': None, 'init_expr': "import ic.PropertyEditor.icEditorGridRender as icrender\r\nimport  wx\r\nimport  wx.grid as  Grid\r\nfrom ic.PropertyEditor import icDefInf\r\n\r\ngrid = self\r\nnb = _dict_obj['NB']\r\n#res = _dict_obj['resource']\r\nWrapperObj.SetResource(None)\r\nres = WrapperObj.getResource()\r\n\r\ngrid.render = icrender.PropValueRenderer(grid.GetTable(), color=wx.Colour(0,85,170))\r\ngrid.render.SetColAttrTypes(res['__attr_types__'])\r\n\r\n#   \xd1\xee\xe7\xe4\xe0\xe5\xec \xe2\xe8\xe7\xf3\xe0\xeb\xfc\xed\xfb\xe5 \xe0\xf2\xf0\xe8\xe1\xf3\xf2\xfb \xea\xee\xeb\xee\xed\xea\xe8 \xe7\xed\xe0\xf7\xe5\xed\xe8\xe9\r\ngrid.val_col_attr = Grid.GridCellAttr()\r\ngrid.val_col_attr.SetRenderer(grid.render)\r\n\r\n#   \xc7\xe0\xe4\xe0\xe5\xec \xe1\xe0\xe7\xe8\xf1 \xf0\xe0\xe7\xeb\xee\xe6\xe5\xed\xe8\xff \xea\xee\xec\xe1\xe8\xed\xe8\xf0\xee\xe2\xe0\xed\xed\xfb\xf5 \xf1\xf2\xe8\xeb\xe5\xe9\r\ngrid._styles_attr = {'style':res['__styles__']}\r\ngrid._styles_attr['flag'] = icDefInf.ICSizerFlag\r\n\r\n#   \xc7\xe0\xe4\xe0\xe5\xec \xf1\xef\xe8\xf1\xea\xe8 \xe2\xfb\xe1\xee\xf0\xe0 \xe4\xeb\xff \xf1\xef\xe8\xf1\xea\xee\xe2\xfb\xf5 \xe0\xf2\xf0\xe8\xe1\xf3\xf2\xee\xe2\r\ngrid._lists_attr = {'layout':['vertical','horizontal'],\r\n                    'alignment':['('left', 'middle')',\r\n                                '('left', 'top')',\r\n                                '('left', 'bottom')', \r\n                                '('centred', 'middle')', \r\n                                '('centred', 'top')', \r\n                                '('centred', 'bottom')',\r\n                                '('right', 'middle')', \r\n                                '('right', 'top')', \r\n                                '('right', 'bottom')']}\r\n\r\ngrid.resource['init'] = '@False'\r\n\r\n#   \xce\xf2\xea\xeb\xfe\xf7\xe0\xe5\xec \xf7\xe0\xf1\xf2\xee\xf2\xed\xfb\xe9 \xf1\xeb\xee\xe2\xe0\xf0\xfc\r\ngrid.EnableFreqDict(False)\r\nnb.SelectTitle(0)", 'position': (2, 2)}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'name': 'PropertyPanel_2162', 'keyDown': None, '__version__icwidget': '0.0.0.0', 'alias': None, 'init_expr': None, 'position': wx.Point(0, 0)}, 'proportion': 1, 'source': None, 'backgroundColor': None, '__version__': '0.0.0.0', 'type': 'SplitterWindow', '__doc__': None, '__styles__': {'SP_LIVE_UPDATE': 128, 'SP_NOBORDER': 0, 'SP_BORDER': 512, 'SP_3DBORDER': 512, 'SP_3DSASH': 256, 'SP_PERMIT_UNSPLIT': 64, 'SP_3D': 768}, '__events__': None, 'min_panelsize': 20, '__item_id': 41, '_uuid': '3d5bb99ab5369674cbeabeeffcf3e6c3', 'style': 768, 'docstr': 'ic.components.icsplitter-module.html', 'flag': 8192, 'recount': 'None', 'span': (1, 1), 'name': 'defaultName_1914_3387', 'keyDown': None, '__version__icwidget': '0.0.0.0', '__version__base': '0.0.0.0', 'init_expr': None, 'position': wx.Point(0, 84), 'sash_pos': 100}], 'span': (1, 1), 'name': 'DefaultName_3247', 'alias': None, 'init_expr': None, 'position': wx.Point(84, 22), 'vgap': 0}], 'name': 'defaultWindow_3143', 'refresh': None, '__version__icwidget': '0.0.0.0', 'alias': None, 'init_expr': None, 'position': (-1, -1)}, 'win1': {'activate': 1, 'show': 1, '__attr_types__': {0: ['alias', 'moveAfterInTabOrder', 'name', 'type'], 7: ['flag', 'style'], 8: ['foregroundColor', 'backgroundColor'], 10: ['position', 'span'], 11: ['size'], 12: ['source', 'activate', 'keyDown', 'show', 'recount', 'refresh', 'init_expr'], 40: ['border', 'proportion']}, 'recount': None, 'keyDown': None, 'border': 0, '__parent__': {'__events__': None, 'moveAfterInTabOrder': '', 'foregroundColor': None, 'name': 'widget', 'show': 1, '__attr_types__': {0: ['alias', 'moveAfterInTabOrder', 'name', 'type'], 7: ['flag', 'style'], 8: ['foregroundColor', 'backgroundColor'], 10: ['position', 'span'], 11: ['size'], 12: ['source', 'activate', 'keyDown', 'show', 'recount', 'refresh', 'init_expr'], 40: ['border', 'proportion']}, 'refresh': None, '__version__icwidget': '0.0.0.0', 'source': None, 'keyDown': None, 'backgroundColor': None, 'recount': None, 'type': 'Widget', '__parent__': {'__styles__': None, 'style': 0, 'activate': 1, 'span': (1, 1), 'name': 'base', 'alias': None, '__version__base': '0.0.0.0', '__attr_types__': {0: ['name', 'type', 'alias'], 7: ['flag', 'style'], 40: ['border', 'proportion'], 10: ['position', 'span'], 11: ['size'], 12: ['activate', 'init_expr']}, '_uuid': None, 'proportion': 0, '__item_id': None, 'flag': 0, 'init_expr': None, 'type': 'Base', 'position': (-1, -1), '__version__': '0.0.0.0', 'border': 0, '__doc__': None, 'size': (-1, -1)}}, 'size': (-1, -1), 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), '__version__base': '0.0.0.0', 'proportion': 0, 'source': None, 'backgroundColor': (192, 192, 192), '__version__': '0.0.0.0', 'type': 'Panel', '__doc__': None, '__styles__': None, '__events__': None, '__item_id': 12, 'onClose': None, '_uuid': '99201af50e1e8a1ae20b455260581c85', 'style': 524288, 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [], 'name': 'defaultWindow_1381', 'refresh': None, '__version__icwidget': '0.0.0.0', 'alias': None, 'init_expr': None, 'position': (-1, -1)}, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'SplitterWindow', 'min_panelsize': 0, '_uuid': u'7e8a29413e873d142a0c052033805fdd', 'style': 768, 'docstr': u'ic.components.icsplitter-module.html', 'flag': 0, 'recount': None, 'span': (1, 1), 'name': u'defaultName_1225', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'sash_pos': 100}

#   Версия объекта
__version__ = (1, 0, 1, 2)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'icResourceEdt'


class icResourceEdt:
    def __init__(self, parent):
        self.evalSpace = util.InitEvalSpace()
        self.__obj = prs.icBuildObject(parent, resource, evalSpace=self.evalSpace, bIndicator=False)
        self.object = self.evalSpace['_root_obj']
        
    def getObject(self):
        """
        """
        return self.object


def test(par=0):
    """
    Тестируем класс icResourceEdt.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)

    #
    # Тестовый код
    #
        
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
