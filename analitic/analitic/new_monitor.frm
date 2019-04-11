{'new_monitor': {'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (330, 150), 'style': 536877056, 'foregroundColor': None, 'span': (1, 1), 'title': u'\u0421\u043e\u0437\u0434\u0430\u043d\u0438\u0435 \u043c\u043e\u043d\u0438\u0442\u043e\u0440\u0430', 'proportion': 1, 'source': None, 'backgroundColor': None, 'type': u'Dialog', 'onClose': None, '_uuid': u'7f9a7357f49184d544e53cf01d84ba9b', 'moveAfterInTabOrder': u'', 'killFocus': None, 'flag': 0, 'child': [{'style': 0, 'activate': 1, 'prim': u'', 'name': u'default_1264', '_uuid': u'a6b4c442e922433167f340ed96ef7723', 'alias': None, 'init_expr': None, 'child': [{'activate': u'0', 'name': u'NsiList', '_uuid': u'd0887e0ac94a6314d329dc76ee389063', 'docstr': u'ic.db.icdataset-module.html', 'filter': None, 'alias': None, 'res_query': u'NsiList', 'init_expr': None, 'file': u'NsiList.tab', 'type': u'DataLink', 'link_expr': None}, {'activate': u'0', 'name': u'NsiStd', '_uuid': u'0aea348b160da3d8093bf5b7c8aaa9c1', 'docstr': u'ic.db.icdataset-module.html', 'filter': None, 'alias': None, 'res_query': u'NsiStd', 'init_expr': None, 'file': u'NsiStd.tab', 'type': u'DataLink', 'link_expr': None}], 'type': u'Group'}, {'hgap': 0, 'style': 0, 'activate': 1, 'span': (1, 1), 'name': u'DefaultName_1185_1499', 'flexRows': [], 'minCellWidth': 10, 'type': u'GridBagSizer', 'border': 0, '_uuid': u'f2460a63db8cfa47ff9ba97ceb4dfe5b', 'proportion': 0, 'alias': None, 'flag': 0, 'minCellHeight': 10, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'keyDown': None, 'border': 0, 'size': (200, 21), 'style': 33555520, 'foregroundColor': (0, 0, 0), 'span': (1, 2), 'proportion': 0, 'source': u'', 'backgroundColor': (255, 255, 255), 'type': u'Choice', 'loseFocus': None, '_uuid': u'f45e2ba9444f0b731ad7466306aa8675', 'moveAfterInTabOrder': u'', 'choice': u"from NSI import spravfunc\r\n\r\nsprav_type=self.GetValue()\r\nrepl_dict=spravfunc.getReplDict(sprav_type,'cod','name',\r\n    'type=\\'%s\\' AND LENGTH(cod)<5'%(sprav_type))\r\n_dict_obj['spravCodeChoice'].setDictRepl(repl_dict)", 'flag': 0, 'recount': [], 'field_name': u'', 'setFocus': None, 'name': u'spravTypeChoice', 'items': u"{'Product':'\u0412\u0438\u0434\u044b \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438',\r\n    'Region':'\u0420\u0435\u0433\u0438\u043e\u043d\u044b',\r\n    'Menager':'\u041c\u0435\u043d\u0435\u0434\u0436\u0435\u0440\u044b'}", 'refresh': [], 'alias': None, 'init_expr': None, 'position': (2, 1), 'onInit': u'None'}, {'activate': 1, 'show': 1, 'refresh': [], 'border': 0, 'size': (200, 21), 'style': 33555520, 'foregroundColor': (0, 0, 0), 'span': (1, 2), 'proportion': 0, 'source': u'', 'backgroundColor': (255, 255, 255), 'type': u'Choice', 'loseFocus': None, '_uuid': u'55e681db0b9c21d27130002c1a674f75', 'moveAfterInTabOrder': u'', 'choice': None, 'flag': 0, 'recount': [], 'field_name': u'', 'setFocus': u'None', 'name': u'spravCodeChoice', 'items': u'', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (3, 1), 'onInit': None}, {'activate': 1, 'show': 1, 'mouseClick': u"_dict_obj['new_monitor_dlg'].Close()", 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'label': u'\u041e\u0442\u043c\u0435\u043d\u0430', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'13424319f6a6b5bcd9ab4382d31ee043', 'moveAfterInTabOrder': u'', 'flag': 2560, 'recount': None, 'name': u'cancel_button', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (5, 1), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'show': 1, 'mouseClick': u"import genMonitor\r\n\r\nnam=_dict_obj['monitorNameTxt'].GetValue()\ntyp=_dict_obj['spravTypeChoice'].GetValue()\ncod=_dict_obj['spravCodeChoice'].GetValue()\nif nam and typ and cod:\n    genMonitor.createMonitor(nam,typ,cod)\r\n    print 'NewMonitor  OK',nam,typ,cod\r\n    _dict_obj['new_monitor_dlg'].Close()", 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'label': u'\u041e\u041a', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'c0a504ada73a4e2ee230da7681e6a009', 'moveAfterInTabOrder': u'', 'flag': 2560, 'recount': None, 'name': u'ok_button', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (5, 2), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'value': u'', 'font': {}, 'border': 0, 'size': (200, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 2), 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', '_uuid': u'078d7bbae42d4a05caff58ff5e014d80', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'monitorNameTxt', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (1, 1), 'onInit': None, 'refresh': []}, {'activate': 1, 'show': 1, 'text': u'\u0418\u043c\u044f \u043c\u043e\u043d\u0438\u0442\u043e\u0440\u0430:', 'keyDown': None, 'font': {}, 'border': 0, 'size': (80, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'8538ea820ddd5f1f6e6103c37403ac73', 'moveAfterInTabOrder': u'', 'flag': 2560, 'recount': None, 'name': u'default_1230', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (1, 0), 'onInit': None}], 'position': (-1, -1), 'flexCols': [], 'vgap': 0, 'size': (-1, -1)}], 'setFocus': None, 'name': u'new_monitor_dlg', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(0, 0), 'onInit': None}}