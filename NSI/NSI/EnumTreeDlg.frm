{'EnumTreeDlg': {'activate': 1, 'prim': u'', 'data_name': None, 'obj_module': None, 'style': 0, 'type': u'Group', 'res_module': None, 'description': None, '_uuid': u'00da78d9a7313c83ce68e2e9c1d0486d', 'component_module': None, 'child': [{'activate': 1, 'name': u'NsiStd', '_uuid': u'a3f3c5b9340891f38aa586c6db21773e', 'docstr': u'ic.db.icdataset-module.html', 'filter': None, 'alias': None, 'res_query': u'NsiStd', 'init_expr': None, 'file': u'NsiStd.tab', 'type': u'DataLink', 'link_expr': None}, {'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (400, 400), 'style': 536877056, 'foregroundColor': None, 'span': (1, 1), 'title': u'\u0421\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a:', 'component_module': None, 'proportion': 1, 'source': None, 'backgroundColor': None, 'type': u'Dialog', 'res_module': None, 'description': None, 'onClose': None, '_uuid': u'd0377934f6be5aca2151b86c6d3174d8', 'moveAfterInTabOrder': u'', 'killFocus': None, 'flag': 2304, 'child': [{'activate': 1, 'minCellWidth': 10, 'minCellHeight': 10, 'border': 0, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'flexRows': [1], 'component_module': None, 'flexCols': [1, 2, 3], 'proportion': 0, 'type': u'GridBagSizer', 'hgap': 0, '_uuid': u'f4a715083c345ea7eb100e2bc400844d', 'flag': 8192, 'child': [{'activate': 1, 'show': 1, 'labels': [u'\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435', u'\u041a\u043e\u0434', u'', u'', u'', u'', u'', u'', u'', u'', u''], 'activated': u"cod=_dict_obj['sprav_tree'].getSelectionCod()\r\nif cod:\r\n    struct_cod=sprav.getStructCod(sprav_code,cod)\r\n    result=struct_cod\r\n    if None not in result:\r\n        _dict_obj['SpravTreeDlg'].EndModal(wx.ID_OK)\r\n", 'keyDown': u'#\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430 \u043d\u0430\u0436\u0430\u0442\u0438\u044f \u043a\u043b\u0430\u0432\u0438\u0448\r\nkey=evt.GetKeyCode()\r\nif key==wx.WXK_ESCAPE and not evt.ShiftDown() and not evt.AltDown():\r\n    result=None\r\n    _root_obj.EndModal(wx.ID_CANCEL)\r\n_resultEval=True', 'border': 0, 'size': (400, 350), 'style': 9, 'foregroundColor': None, 'span': (1, 3), 'component_module': None, 'typeSprav': u'@sprav.name', 'selected': None, 'proportion': 1, 'source': u'NsiStd', 'backgroundColor': None, 'codfield': u'cod', 'titleRoot': u'@sprav.description', 'type': u'SpravTreeList', '_uuid': u'290878c8ac048496d85aa1e9cba31396', 'moveAfterInTabOrder': u'', 'flag': 8192, 'recount': None, 'name': u'sprav_tree', 'wcols': [150, 30, 70, 70, 70, 50, 50, 50, 50, 50, 50], 'fields': [u'name', u'cod', u's1', u's2', u's3', u'n1', u'n2', u'n3', u'f1', u'f2', u'f3'], 'mask': u'', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (1, 1), 'onInit': None}, {'activate': 1, 'show': 1, 'attach_focus': False, 'mouseClick': u"result=None\r\n_dict_obj['SpravTreeDlg'].EndModal(wx.ID_CANCEL)\r\n_resultEval=True", 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041e\u0442\u043c\u0435\u043d\u0430', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'res_module': None, 'description': None, '_uuid': u'e2268caf00f1bc972e22d8406debac63', 'userAttr': None, 'moveAfterInTabOrder': u'', 'flag': 2560, 'recount': None, 'name': u'cancel_button', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (2, 2), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'show': 1, 'attach_focus': False, 'mouseClick': u"cod=_dict_obj['sprav_tree'].getSelectionCod()\r\nif cod:\r\n    struct_cod=sprav.getStructCod(sprav_code,cod)\r\n    result=struct_cod\r\n    if None not in result:\r\n        _dict_obj['SpravTreeDlg'].EndModal(wx.ID_OK)\r\n#get_hlp_code(sprav_type,sprav_code,NsiStd.rec.cod)\r\n#result=sprav.Hlp(ParentCode=cod_struct,field=sprav_field,rec=NsiStd.rec,parentForm=_dict_obj['DlgHlpSprav'])\r\n#if result:\r\n#    _esp['_dict_obj']['DlgHlpSprav'].EndModal(wx.ID_OK)\r\n#else:\r\n#    _dict_obj['ListDS'].SetCursor(cur_row)\r\n#print _dict_obj['sprav_tree'].getSelectionCod()", 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041e\u041a', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'res_module': None, 'description': None, '_uuid': u'1734c3124479e2f00f9ea6b71ddd1804', 'userAttr': None, 'moveAfterInTabOrder': u'', 'flag': 2560, 'recount': None, 'name': u'ok_button', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (2, 3), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'show': 1, 'mouseClick': u"sprav.edit(sprav_code,_dict_obj['SpravTreeDlg'])", 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435...', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'18ebb02806b1b836f91439f29e6de716', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'edit_button', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (2, 1), 'onInit': None, 'refresh': None, 'mouseContextDown': None}], 'name': u'DefaultName_1415', 'alias': None, 'init_expr': None, 'position': (-1, -1), 'vgap': 0}], 'setFocus': None, 'name': u'SpravTreeDlg', 'keyDown': u'#\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430 \u043d\u0430\u0436\u0430\u0442\u0438\u044f \u043a\u043b\u0430\u0432\u0438\u0448\r\nkey=evt.GetKeyCode()\r\nif key==wx.WXK_ESCAPE and not evt.ShiftDown() and not evt.AltDown():\r\n    result=None\r\n    _root_obj.EndModal(wx.ID_CANCEL)\r\n_resultEval=True', 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}], 'name': u'EnumTreeDlg', 'alias': None, 'init_expr': None}}