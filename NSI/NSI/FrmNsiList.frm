{'FrmNsiList': {'style': 0, 'activate': u'1', 'prim': u'', 'name': u'FrmNsiList', 'alias': None, 'description': None, '_uuid': u'704b5094e837483991dc33b605a7b569', 'component_module': None, 'init_expr': u'None', 'child': [{'activate': u'1', 'obj_module': None, 'show': u'1', 'child': [{'style': 0, 'activate': u'1', 'prim': u'', 'name': u'\u0414\u0430\u043d\u043d\u044b\u0435_1028', 'alias': None, '_uuid': u'84695d012c7860ebd020e088b45dc87d', 'component_module': None, 'init_expr': u'None', 'child': [{'style': 0, 'activate': u'1', 'span': (1, 1), 'description': None, 'alias': None, 'proportion': 0, '_uuid': u'fe48edafc4971039a631a7c52cc3e72c', 'modules': {}, 'object': None, 'name': u'imp_277', 'component_module': None, 'flag': 0, 'init_expr': u"#MsgBox(None,NsiEdtFormName('City'))\r\nfrom ic.dlg.msgbox import *\r\nfrom NSI.spravfunc import *", 'type': u'Import', 'position': (-1, -1), 'border': 0, 'size': (-1, -1)}, {'file': u'NsiList.tab', 'activate': u'1', 'name': u'NsiList', '_uuid': u'b62956aecd014e32bcae9c8807f0bb5d', 'docstr': 'ic.db.icdataset-module.html', 'filter': u'', 'alias': None, 'res_query': u'@getNsiListClassName()', 'init_expr': u'None', 'icField:type.ctrl': u"# \u041f\u0435\u0440\u0435\u043e\u043f\u0440\u0435\u0434\u0435\u043b\u044f\u0435\u043c \u043a\u043e\u043d\u0442\u0440\u043e\u043b\u044c \u043d\u0430 \u043f\u043e\u043b\u0435 <type>. \u041f\u0440\u043e\u0432\u0435\u0440\u044f\u0435\u043c \u0443\u043d\u0438\u043a\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u044c \u0442\u0438\u043f\u0430 \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0430\r\nprint 'SCRIPT CTRL FIELD <TYPE>, value=', value\r\nrs = _NsiList.select(_NsiList.q.type==value)\r\n\r\nif getRecordCount(rs) > 0:\r\n\tMsgBox(None, 'C\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a <%s> \u0443\u0436\u0435 \u043e\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d. \u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0434\u0440\u0443\u0433\u043e\u0439 \u0442\u0438\u043f \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0430.' % value)\r\n\t_resultEval = (3, None)\r\nelse:\r\n\t_resultEval = (0, None)", 'icField:type.init': u'<typ>', 'type': u'DataLink', 'link_expr': u"#MsgBox(None,NsiEdtFormName('Street', '2'))"}, {'activate': u'1', 'name': u'NsiLevel', '_uuid': u'b3fead4c7590c35af1cc0ba54b17ad42', 'docstr': 'ic.db.icdataset-module.html', 'filter': u'', 'alias': None, 'res_query': u'@getNsiLevelClassName()', 'init_expr': None, 'file': u'NsiLevel.tab', 'type': u'DataLink', 'link_expr': u''}], 'type': u'Group', 'description': None}, {'activate': u'1', 'obj_module': None, 'border': 0, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'type': u'BoxSizer', 'res_module': None, 'hgap': 0, 'description': None, '_uuid': u'eb86b2308aade7a9292a1cbcf8ccdbc5', 'flag': 0, 'child': [{'activate': u'1', 'span': (1, 1), 'name': u'sp1', 'type': u'SizerSpace', '_uuid': u'eb86b2308aade7a9292a1cbcf8ccdbc5', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'border': 0, 'size': (0, 3)}, {'activate': u'1', 'show': u'1', 'buttonAdd': 1, 'buttonDel': 1, 'refresh': None, 'border': 0, 'size': (200, 20), 'style': 512, 'object_link': None, 'span': (1, 1), 'onPrint': None, 'proportion': 0, 'source': u'NsiList', 'onAdd': u'None', 'backgroundColor': None, 'type': u'DatasetNavigator', 'buttonPrint': 0, '_uuid': u'649219af8b91e075e19ce3833580db33', 'onHelp': None, 'moveAfterInTabOrder': u'', 'onUpdate': None, 'flag': 8192, 'foregroundColor': None, 'recount': None, 'onDelete': None, 'name': u'default_1014', 'keyDown': None, 'alias': None, 'init_expr': None, 'buttonHelp': 0, 'position': (-1, -1), 'buttonUpdate': 0}, {'activate': u'1', 'span': (1, 1), 'name': u'sp1_1035', 'border': 0, '_uuid': u'aa01bbf7c03919d08287290604c13480', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'type': u'SizerSpace', 'size': (0, 5)}, {'activate': 1, 'show': 1, 'recount': None, 'keyDown': None, 'font': {}, 'border': 0, 'alignment': (u'left', u'middle'), 'size': (240, 31), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': (235, 235, 235), 'type': u'Head', 'description': None, '_uuid': u'0f0a9b5b3dd35e28296ae61e6501588b', 'style': 0, 'flag': 8192, 'child': [{'activate': u'0', 'show': 1, 'borderRightColor': (100, 100, 100), 'recount': None, 'keyDown': None, 'borderTopColor': (182, 182, 182), 'font': {'family': u'sansSerif', 'style': u'bold', 'underline': False, 'faceName': u'Arial', 'size': 8}, 'border': 0, 'alignment': u"('centred', 'middle')", 'size': (50, 22), 'moveAfterInTabOrder': u'', 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u0422\u0438\u043f', 'source': None, 'backgroundColor': (255, 255, 255), 'isSort': u'True', 'type': u'HeadCell', 'borderWidth': 1, 'description': None, 'shortHelpString': u'\u0422\u0438\u043f \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0430', 'backgroundColor2': None, '_uuid': u'f422647427f7178ad395a0f3f17989f8', 'style': 0, 'bgrImage': None, 'flag': 0, 'child': [], 'cursorColor': (100, 100, 100), 'borderStyle': None, 'borderStep': 0, 'borderLeftColor': (100, 100, 100), 'name': u'type', 'borderBottomColor': (100, 100, 100), 'refresh': None, 'alias': None, 'init_expr': u'', 'position': (0, 0), 'backgroundType': 1, 'onInit': None}, {'activate': u'0', 'show': 1, 'borderRightColor': (100, 100, 100), 'recount': None, 'keyDown': None, 'borderTopColor': (182, 182, 182), 'font': {'family': u'sansSerif', 'style': u'bold', 'underline': False, 'faceName': u'Arial', 'size': 8}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (50, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435', 'source': None, 'backgroundColor': (255, 255, 255), 'isSort': u'True', 'type': u'HeadCell', 'borderWidth': 1, 'description': None, 'shortHelpString': u'\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0430', 'backgroundColor2': None, '_uuid': u'cc954504cb2ac58751bc2101078fa1b4', 'style': 0, 'bgrImage': None, 'flag': 0, 'child': [], 'cursorColor': (100, 100, 100), 'borderStyle': None, 'borderStep': 0, 'borderLeftColor': (240, 240, 240), 'name': u'name', 'borderBottomColor': (100, 100, 100), 'refresh': None, 'alias': None, 'init_expr': None, 'position': (0, 1), 'backgroundType': 1, 'onInit': None}, {'activate': u'0', 'show': 1, 'borderRightColor': (100, 100, 100), 'recount': None, 'keyDown': None, 'borderTopColor': (182, 182, 182), 'font': {'family': u'sansSerif', 'style': u'bold', 'underline': False, 'faceName': u'Arial', 'size': 8}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (50, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041a\u043b\u0430\u0441\u0441', 'source': None, 'backgroundColor': (255, 255, 255), 'isSort': u'True', 'type': u'HeadCell', 'borderWidth': 1, 'description': None, 'shortHelpString': u'\u041a\u043b\u0430\u0441\u0441 \u0434\u0430\u043d\u043d\u044b\u0445, \u0433\u0434\u0435\r\n\u0445\u0440\u0430\u043d\u0438\u0442\u0441\u044f \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a', 'backgroundColor2': None, '_uuid': u'cd55176b8647320f09f722f5ff453ffc', 'style': 0, 'bgrImage': None, 'flag': 0, 'child': [], 'cursorColor': (100, 100, 100), 'borderStyle': None, 'borderStep': 0, 'borderLeftColor': (240, 240, 240), 'name': u'tab', 'borderBottomColor': (100, 100, 100), 'refresh': None, 'alias': None, 'init_expr': None, 'position': (0, 2), 'backgroundType': 1, 'onInit': None}, {'activate': u'0', 'show': 1, 'borderRightColor': (100, 100, 100), 'recount': None, 'keyDown': None, 'borderTopColor': (182, 182, 182), 'font': {'family': u'sansSerif', 'style': u'bold', 'underline': False, 'faceName': u'Arial', 'size': 8}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (50, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041a\u043e\u043b-\u0432\u043e \u0443\u0440\u043e\u0432\u043d\u0435\u0439 ', 'source': None, 'backgroundColor': (255, 255, 255), 'isSort': u'True', 'type': u'HeadCell', 'borderWidth': 1, 'description': None, 'shortHelpString': u'\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0443\u0440\u043e\u0432\u043d\u0435\u0439 \u043a\u043e\u0434\u0430\r\n\u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0430', 'backgroundColor2': None, '_uuid': u'd059d9ca625346930423cef17a738a1b', 'style': 0, 'bgrImage': None, 'flag': 0, 'child': [], 'cursorColor': (100, 100, 100), 'borderStyle': None, 'borderStep': 0, 'borderLeftColor': (240, 240, 240), 'name': u'level_num', 'borderBottomColor': (100, 100, 100), 'refresh': u'None', 'alias': None, 'init_expr': None, 'position': (0, 3), 'backgroundType': 1, 'onInit': None}, {'activate': 1, 'proportion': 0, 'border': 0, 'size': (50, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'przn_border': [1, 1, 0, 1], 'label': u'\u0422\u0438\u043f', 'isSort': 1, 'scheme': u'GOLD', 'type': u'NsiLabelCell', 'description': None, 'shortHelpString': u'', 'nest': None, '_uuid': u'3a10fd200add81711bf684bb6ba1ac5a', 'flag': 0, 'child': [], 'name': u'LType', 'round_corner': [1, 0, 0, 0], 'alias': None, 'init_expr': None, 'position': (0, 0)}, {'activate': 1, 'proportion': 0, 'border': 0, 'size': (50, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'przn_border': [1, 1, 0, 1], 'label': u'\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435', 'isSort': 1, 'scheme': u'GOLD', 'type': u'NsiLabelCell', 'description': None, 'shortHelpString': u'', 'nest': None, '_uuid': u'80afab95037c4817a9440d2156bc638c', 'flag': 0, 'child': [], 'name': u'LName', 'round_corner': [0, 0, 0, 0], 'alias': None, 'init_expr': None, 'position': (0, 1)}, {'activate': 1, 'proportion': 0, 'border': 0, 'size': (50, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'przn_border': [1, 1, 0, 1], 'label': u'\u041a\u043b\u0430\u0441\u0441', 'isSort': False, 'scheme': u'GOLD', 'type': u'NsiLabelCell', 'description': None, 'shortHelpString': u'', 'nest': None, '_uuid': u'c9872ad90fbacb588a3b6ded9fbb34f2', 'flag': 0, 'child': [], 'name': u'LTab', 'round_corner': [0, 0, 0, 0], 'alias': None, 'init_expr': None, 'position': (0, 2)}, {'activate': 1, 'proportion': 0, 'border': 0, 'size': (50, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'przn_border': [1, 1, 1, 1], 'label': u'\u041a\u043e\u043b-\u0432\u043e \u0443\u0440\u043e\u0432\u043d\u0435\u0439 ', 'isSort': False, 'scheme': u'GOLD', 'type': u'NsiLabelCell', 'description': None, 'shortHelpString': u'', 'nest': None, '_uuid': u'5f66e65b130347f87d93a7e70202e52e', 'flag': 0, 'child': [], 'name': u'LLevel_num', 'round_corner': [0, 1, 0, 0], 'alias': None, 'init_expr': None, 'position': (0, 3)}], 'name': u'HeadNsiList', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(162, 324), 'onInit': None}, {'line_color': (210, 214, 223), 'activate': u'True', 'show': u'1', 'cols': [{'activate': u'1', 'ctrl': u'', 'pic': u'S', 'hlp': u'None', 'style': 0, 'component_module': None, 'show': u'1', 'label': u'\u0422\u0438\u043f', 'width': 70, 'init': u'', 'valid': u'None', 'type': u'GridCell', 'sort': u'1', 'cell_attr': {'foregroundColor': (40, 40, 55), 'name': '', '_uuid': u'066a9054f8acac425512040e7eae22c5', 'activate': u'1', 'init_expr': None, 'backgroundColor': (255, 255, 255), 'font': {'style': u'bold', 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'\u0422\u0438\u043f \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0430', '_uuid': u'066a9054f8acac425512040e7eae22c5', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'type', 'keyDown': None, 'alias': None, 'init_expr': u'None'}, {'activate': u'1', 'ctrl': None, 'pic': u'S', 'getvalue': u'', 'show': u'1', 'label': u'\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435', 'width': 308, 'init': u'None', 'valid': u'None', 'type': u'GridCell', 'sort': u'1', 'cell_attr': {'foregroundColor': (40, 40, 55), 'name': '', '_uuid': u'066a9054f8acac425512040e7eae22c5', 'activate': u'1', 'init_expr': None, 'backgroundColor': (255, 255, 255), 'font': {'style': u'italic', 'name': u'defaultFont', 'family': u'sansSerif', 'faceName': u'Times New Roman', 'type': u'Font', 'underline': 0, 'size': 10}, 'type': 'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0430', '_uuid': u'066a9054f8acac425512040e7eae22c5', 'recount': None, 'hlp': None, 'attr': None, 'setvalue': u'', 'name': u'name', 'keyDown': u'None', 'init_expr': None}, {'activate': u'1', 'ctrl': None, 'pic': u'S', 'getvalue': u'', 'show': u'1', 'label': u'\u041a\u043b\u0430\u0441\u0441', 'width': 140, 'init': u'NsiStd', 'valid': u'None', 'type': u'GridCell', 'sort': u'1', 'cell_attr': {'foregroundColor': (40, 40, 55), 'name': '', '_uuid': u'066a9054f8acac425512040e7eae22c5', 'activate': u'1', 'init_expr': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': u"('centred', 'top')"}, 'shortHelpString': u'\u041a\u043b\u0430\u0441\u0441 \u0434\u0430\u043d\u043d\u044b\u0445, \u0433\u0434\u0435\r\n\u0445\u0440\u0430\u043d\u0438\u0442\u0441\u044f \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a', '_uuid': u'4987812fdfb4c4ad9bf73856e166f1b7', 'recount': None, 'hlp': None, 'attr': None, 'setvalue': u'', 'name': u'tab', 'keyDown': None, 'init_expr': None}, {'activate': u'1', 'ctrl': None, 'pic': u'99', 'getvalue': u'', 'show': u'1', 'label': u'\u041a\u043e\u043b-\u0432\u043e \u0443\u0440\u043e\u0432\u043d\u0435\u0439 ', 'width': 123, 'init': None, 'valid': u'1,20', 'type': u'GridCell', 'sort': u'1', 'cell_attr': {'foregroundColor': (40, 40, 55), 'name': '', '_uuid': u'066a9054f8acac425512040e7eae22c5', 'activate': u'1', 'init_expr': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0443\u0440\u043e\u0432\u043d\u0435\u0439 \u043a\u043e\u0434\u0430\r\n\u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0430', '_uuid': u'a08f2ee5a1ae17904b7f1eb6457bbcf0', 'recount': None, 'hlp': u'None', 'attr': u'R', 'setvalue': u'', 'name': u'level_num', 'keyDown': u'None', 'init_expr': None}], 'row_height': 18, 'keyDown': u'#   \u041e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430 \u043d\u0430\u0436\u0430\u0442\u0438\u044f \u043a\u043b\u0430\u0432\u0438\u0448\u044c\r\nimport NSI.spravfunc as spravfunc\r\nkey=event.GetKeyCode()\r\nprnt = _dict_obj[\'DlgNsiList\']\r\nprint \'KeyDown in GRID key:\', prnt\r\n\r\nif key==wx.WXK_F3:\r\n    print \'============================= F3 -\', key\r\n    #ResultForm(NsiEdtFormName(NsiList.rec.type), filter={"Sprav":{"id_nsi_list":NsiList.rec.id}}, parent=self)\r\n\r\n    #   1. \u041e\u043f\u0440\u0435\u0434\u0435\u043b\u044f\u0435\u043c \u0440\u0430\u0437\u043c\u0435\u0440 \u043f\u0435\u0440\u0432\u043e\u0433\u043e \u0443\u0440\u043e\u0432\u043d\u044f \u0438 \u0441\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u043d\u044b\u0439 \u0444\u0438\u043b\u044c\u0442\u0440 \u0434\u043b\u044f \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0430\r\n    try:\r\n        levelLen = _NsiLevel.select(AND(_NsiLevel.q.id_nsi_listID==NsiList.rec.id,\r\n                                                    _NsiLevel.q.level==1))[0].level_len\r\n        flt = {"NsiStd":{"id_nsi_list":NsiList.rec.id, \'cod\':[levelLen]}}\r\n    except:\r\n        flt = {"NsiStd":{"id_nsi_list":NsiList.rec.id}}\r\n        print \'------------------------------------------------------------------------------------------------------\'\r\n        print \'SCRIPT ATTRIBUTE WARNING: Do not find level(1) len for structual filter\', flt\r\n    \r\n    #   2. \u0412\u044b\u0437\u044b\u0432\u0430\u0435\u043c \u0444\u043e\u0440\u043c\u0443 \u0434\u043b\u044f \u0440\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f\r\n    formName = spravfunc.NsiEdtFormName(NsiList.rec.type)\r\n    print \'SCRIPT ATTRIBUTE: filter=\', flt, formName\r\n    \r\n    ResultForm(formName, filter=flt, parent=prnt)\r\n    #_dict_obj[\'gridList\'].SetFocus()\r\n    self.GetView().SetFocus()\r\n\r\nelif key==wx.WXK_F4:\r\n    print \'============================= F4 -\', key\r\n    ResultForm("FrmNsiLevel", filter={"NsiLevel":{"id_nsi_list":NsiList.rec.id}}, parent=prnt)\r\n    #lev_num = len(_NsiLevel.select(_NsiLevel.q.id_nsi_listID==NsiList.rec.id))\r\n\r\n    lev_num = spravfunc.getRecordCount(_NsiLevel.select(_NsiLevel.q.id_nsi_listID==NsiList.rec.id))\r\n    NsiList.setNameValue(\'level_num\', lev_num)\r\n    NsiList.update()\r\n    self.GetView().SetFocus()\r\n\r\nelif key==wx.WXK_ESCAPE and not event.ShiftDown() and not event.AltDown():\r\n    print \'ESCAPE shift, alt:\', event.ShiftDown(), event.AltDown()\r\n    _dict_obj["DlgNsiList"].EndModal(wx.ID_CANCEL)\r\n\r\n# \u0423\u0441\u0442\u0430\u043d\u0430\u0432\u043b\u0438\u0432\u0430\u0435\u043c \u043a\u043e\u0434 \u0432\u043e\u0437\u0432\u0440\u0430\u0442\u0430 IC_CTRLKEY_OK. \r\n#_resultEval = 0', 'border': 0, 'post_select': None, 'size': (200, 200), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'delRec': u'None', 'component_module': None, 'selected': u'None', 'proportion': 1, 'getattr': u'#iter_rowcol(self, [(234, 234, 234), (255, 255, 255)])', 'label': u'Grid', 'source': u'NsiList', 'init': u'None', 'backgroundColor': (255, 255, 255), 'fixRowSize': 0, 'type': u'GridDataset', '_uuid': u'69b35ab083bee4e2fe27b316b637a8ed', 'fixColSize': 0, 'description': None, 'post_del': None, 'post_init': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '_uuid': u'fc85459788dc405bf6a693b37427bc21', 'activate': u'1', 'init_expr': None, 'backgroundColor': (247, 247, 247), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': (u'left', u'middle')}, 'style': 0, 'docstr': u'ic.components.icgrid.html', 'flag': 8192, 'dclickEditor': None, 'recount': None, 'label_attr': {'foregroundColor': (255, 255, 255), 'name': '', '_uuid': u'73c9d13616eff4663ca72e71489404f2', 'activate': u'1', 'init_expr': None, 'backgroundColor': None, 'font': {'style': u'regular', 'name': u'defaultFont', 'family': u'sansSerif', 'faceName': u'Tahoma', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': 'label_attr', 'alignment': u"('left', 'middle')"}, 'name': u'gridList', 'label_height': 20, 'changed': u'None', 'onSize': None, 'alias': u'None', 'init_expr': u"header = _dict_obj['HeadNsiList']\r\nself.setHeader(header, False, True)\r\nself.doReconstructHeader()", 'position': (-1, -1), 'onInit': None, 'refresh': u'None'}, {'activate': u'1', 'name': u'sp1_2642', '_uuid': u'3e8fc3107483e84826776942eae16bcc', 'proportion': 0, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'type': u'SizerSpace', 'size': (0, 5)}, {'hgap': 0, 'style': 0, 'activate': u'1', 'layout': u'horizontal', 'description': None, 'alias': None, 'component_module': None, 'type': u'BoxSizer', '_uuid': u'e9bc2e98fd81e9a2814122375245193c', 'proportion': 0, 'name': u'DefaultName_382', 'flag': 256, 'position': (0, 0), 'init_expr': None, 'child': [{'activate': u'1', 'show': u'1', 'refresh': None, 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'F3 - \u0440\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a', 'source': None, 'mouseDown': u'None', 'backgroundColor': None, 'type': u'Button', 'description': None, '_uuid': u'c12fe1b6c73ecda818ee39ac384b6b2e', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'F3', 'mouseUp': u'None', 'keyDown': None, 'alias': None, 'init_expr': u'None', 'position': (-1, -1), 'onInit': None, 'keyCode': None, 'mouseContextDown': u'', 'mouseClick': u'import NSI.spravfunc as spravfunc\r\n#\t\u0412\u044b\u0437\u044b\u0432\u0430\u0435\u043c \u0440\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0430\r\n\r\n#\t1. \u041e\u043f\u0440\u0435\u0434\u0435\u043b\u044f\u0435\u043c \u0440\u0430\u0437\u043c\u0435\u0440 \u043f\u0435\u0440\u0432\u043e\u0433\u043e \u0443\u0440\u043e\u0432\u043d\u044f \u0438 \u0441\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u043d\u044b\u0439 \u0444\u0438\u043b\u044c\u0442\u0440 \u0434\u043b\u044f \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0430\r\ntry:\r\n\tlevelLen = _NsiLevel.select(AND(_NsiLevel.q.id_nsi_listID==NsiList.rec.id,\r\n\t\t\t\t\t\t\t\t\t\t\t\t_NsiLevel.q.level==1))[0].level_len\r\n\tflt = {"NsiStd":{"id_nsi_list":NsiList.rec.id, \'cod\':[levelLen]}}\r\nexcept:\r\n\tflt = {"NsiStd":{"id_nsi_list":NsiList.rec.id}}\r\n\tprint \'------------------------------------------------------------------------------------------------------\'\r\n\tprint \'SCRIPT ATTRIBUTE WARNING: Do not find level(1) len for structual filter\', flt\r\n\t\r\n#\t2. \u0412\u044b\u0437\u044b\u0432\u0430\u0435\u043c \u0444\u043e\u0440\u043c\u0443 \u0434\u043b\u044f \u0440\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f\r\nprint \'SCRIPT ATTRIBUTE: filter=\', flt\r\nResultForm(spravfunc.NsiEdtFormName(NsiList.rec.type), filter=flt, parent=self)\r\n#ResultForm(NsiEdtFormName(NsiList.rec.type), filter=flt, parent=self)\r\n_dict_obj[\'gridList\'].SetFocus()'}, {'activate': u'1', 'show': u'1', 'mouseClick': u'import NSI.spravfunc as spravfunc\r\nResultForm("FrmNsiLevel", filter={"NsiLevel":{"id_nsi_list":NsiList.rec.id}}, parent=self)\r\nrow = spravfunc.getRecordCount(_NsiLevel.select(_NsiLevel.q.id_nsi_listID==NsiList.rec.id))\r\nNsiList.setNameValue(\'level_num\', row)\r\nNsiList.update()\r\n_dict_obj[\'gridList\'].SetFocus()', 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'label': u'F4 - \u0441\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u0430 \u043a\u043e\u0434\u0430', 'source': None, 'mouseDown': u'None', 'backgroundColor': None, 'type': u'Button', '_uuid': u'7f108086b53b3fd859b2e6ebc68de601', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'F4_339', 'mouseUp': None, 'keyDown': None, 'keyCode': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'refresh': None, 'mouseContextDown': u'None'}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}, {'activate': u'1', 'name': u'sp1_2716', '_uuid': u'e9bc2e98fd81e9a2814122375245193c', 'proportion': 0, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'type': u'SizerSpace', 'size': (0, 5)}], 'layout': u'vertical', 'name': u'DefaultName_946_1503_1754', 'alias': None, 'init_expr': u"method('SetLastRow', 'NSI', locals(), grid=_dict_obj['gridList'])", 'position': (-1, -1), 'vgap': 0}], 'keyDown': None, 'border': 0, 'size': (650, 400), 'style': 536877120, 'foregroundColor': None, 'span': (1, 1), 'title': u'\u0422\u0438\u043f\u044b \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u043e\u0432', 'component_module': None, 'proportion': 0, 'source': u'None', 'backgroundColor': (91, 144, 137), 'type': u'Dialog', 'res_module': None, 'description': None, 'onClose': None, '_uuid': '370d61172fa2a110bc57f31403f14555', 'moveAfterInTabOrder': u'', 'killFocus': None, 'flag': 0, 'recount': None, 'setFocus': None, 'name': u'DlgNsiList', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(0, 0), 'onInit': None}], 'obj_module': None, 'type': u'Group', 'res_module': None}}