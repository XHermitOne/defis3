{'GenMonthPlanDlg': {'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (500, 400), 'style': 536877120, 'foregroundColor': None, 'span': (1, 1), 'title': u'\u0421\u043e\u0437\u0434\u0430\u043d\u0438\u0435 \u043f\u043b\u0430\u043d\u043e\u0432', 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'Dialog', 'onClose': None, '_uuid': u'a91d377c8e8027a00dc73b6b0958689e', 'moveAfterInTabOrder': u'', 'killFocus': None, 'flag': 0, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'name': u'DefaultName_1386', 'position': (0, 0), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'70f15ce7dc190acbe028991ee90d3f60', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'horizontal', 'name': u'templBSZR', 'component_module': None, 'border': 0, 'span': (1, 1), '_uuid': u'9d32a48800f60efc9f231c7f12cf7899', 'proportion': 0, 'label': u'\u0413\u043e\u0434 \u0438 \u043c\u0435\u0441\u044f\u0446 \u0448\u0430\u0431\u043b\u043e\u043d\u0430 \u043f\u043b\u0430\u043d\u0430', 'alias': None, 'flag': 8192, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'refresh': [], 'border': 0, 'size': (120, -1), 'style': 33555520, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': (255, 255, 255), 'type': u'Choice', 'loseFocus': None, '_uuid': u'f63707be0c2f0156d372e105a21f9cdf', 'moveAfterInTabOrder': u'', 'choice': None, 'flag': 0, 'recount': [], 'field_name': None, 'setFocus': None, 'name': u'monthTemplChoice', 'items': u"['\u042f\u043d\u0432\u0430\u0440\u044c',\r\n'\u0424\u0435\u0432\u0440\u0430\u043b\u044c',\r\n'\u041c\u0430\u0440\u0442',\r\n'\u0410\u043f\u0440\u0435\u043b\u044c',\r\n'\u041c\u0430\u0439',\r\n'\u0418\u044e\u043d\u044c',\r\n'\u0418\u044e\u043b\u044c',\r\n'\u0410\u0432\u0433\u0443\u0441\u0442',\r\n'\u0421\u0435\u043d\u0442\u044f\u0431\u0440\u044c',\r\n'\u041e\u043a\u0442\u044f\u0431\u0440\u044c',\r\n'\u041d\u043e\u044f\u0431\u0440\u044c',\r\n'\u0414\u0435\u043a\u0430\u0431\u0440\u044c']", 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': u'self.setSelection(0)'}, {'style': 0, 'activate': 1, 'span': (1, 1), 'name': u'DefaultName_1663', 'component_module': None, 'border': 0, '_uuid': u'8beaf9c3fb16a98c29946b8ed88b21d9', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': wx.Point(135, 9), 'type': u'SizerSpace', 'size': wx.Size(10, 10)}, {'activate': 1, 'show': 1, 'keyDown': None, 'font': {}, 'border': 0, 'size': (80, -1), 'style': 33562624, 'foregroundColor': None, 'span': (1, 1), 'min': 2000, 'component_module': None, 'proportion': 0, 'source': None, 'init': None, 'backgroundColor': None, 'type': u'Spinner', 'loseFocus': None, 'max': 2050, '_uuid': u'185022eab594eec5dd09ed3c10b99697', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'field_name': None, 'setFocus': None, 'name': u'yearTemplSpinner', 'value': 2005, 'alias': None, 'onSpin': None, 'init_expr': None, 'position': (-1, -1), 'onInit': u'', 'refresh': []}], 'position': (-1, -1), 'type': u'StaticBoxSizer', 'vgap': 0, 'size': (-1, -1)}, {'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'horizontal', 'name': u'planBSZR', 'component_module': None, 'border': 0, 'span': (1, 1), '_uuid': u'1b11e7de577af3a7be7ebc7d24acdb43', 'proportion': 0, 'label': u'\u0413\u043e\u0434 \u0438 \u043c\u0435\u0441\u044f\u0446 \u043d\u043e\u0432\u043e\u0433\u043e \u043f\u043b\u0430\u043d\u0430', 'alias': None, 'flag': 8192, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'keyDown': None, 'border': 0, 'size': (120, -1), 'style': 33555520, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': (255, 255, 255), 'type': u'Choice', 'loseFocus': None, '_uuid': u'741175a094a38c3754174cf6db15bf9c', 'moveAfterInTabOrder': u'', 'choice': None, 'flag': 0, 'recount': [], 'field_name': None, 'setFocus': None, 'name': u'monthChoice', 'items': u"['\u042f\u043d\u0432\u0430\u0440\u044c',\r\n'\u0424\u0435\u0432\u0440\u0430\u043b\u044c',\r\n'\u041c\u0430\u0440\u0442',\r\n'\u0410\u043f\u0440\u0435\u043b\u044c',\r\n'\u041c\u0430\u0439',\r\n'\u0418\u044e\u043d\u044c',\r\n'\u0418\u044e\u043b\u044c',\r\n'\u0410\u0432\u0433\u0443\u0441\u0442',\r\n'\u0421\u0435\u043d\u0442\u044f\u0431\u0440\u044c',\r\n'\u041e\u043a\u0442\u044f\u0431\u0440\u044c',\r\n'\u041d\u043e\u044f\u0431\u0440\u044c',\r\n'\u0414\u0435\u043a\u0430\u0431\u0440\u044c']", 'refresh': [], 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': u'self.setSelection(0)'}, {'style': 0, 'activate': 1, 'span': (1, 1), 'name': u'DefaultName_1663', 'component_module': None, 'border': 0, '_uuid': u'8beaf9c3fb16a98c29946b8ed88b21d9', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': wx.Point(135, 9), 'type': u'SizerSpace', 'size': wx.Size(10, 10)}, {'activate': 1, 'show': 1, 'value': 2005, 'font': {}, 'border': 0, 'size': (80, -1), 'style': 33562624, 'foregroundColor': None, 'span': (1, 1), 'min': 2000, 'component_module': None, 'proportion': 0, 'source': None, 'init': None, 'backgroundColor': None, 'type': u'Spinner', 'loseFocus': None, 'max': 2050, '_uuid': u'45b689e22132d52dcc4d2056c322e125', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'field_name': None, 'setFocus': None, 'name': u'yearSpinner', 'keyDown': None, 'alias': None, 'onSpin': None, 'init_expr': None, 'position': (-1, -1), 'onInit': u'', 'refresh': []}], 'position': (-1, -1), 'type': u'StaticBoxSizer', 'vgap': 0, 'size': (-1, -1)}, {'style': 0, 'activate': 1, 'span': (1, 1), 'name': u'DefaultName_2028', 'component_module': None, 'border': 0, '_uuid': u'4932e0ea3cb35accf45dbcc4d7483f0f', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': wx.Point(31, 95), 'type': u'SizerSpace', 'size': (10, 10)}, {'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'horizontal', 'name': u'buttonBSZR', 'position': wx.Point(88, 101), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'1cd9267e575af7ffc9a523bcb8ac71ff', 'proportion': 0, 'alias': None, 'flag': 256, 'init_expr': None, 'child': [{'style': 0, 'activate': 1, 'span': (1, 1), 'name': u'DefaultName_2136', 'component_module': None, 'border': 0, '_uuid': u'34fe32ef0ca58b3f3a2ad2088fc0a937', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': wx.Point(6, 99), 'type': u'SizerSpace', 'size': (10, 10)}, {'activate': 1, 'show': 1, 'mouseClick': u"import analitic.planUtils as planUtils\r\nimport analitic.metadatainterfaces.IMetaplan as IMetaplan\r\nfrom ic.dlg import progress\r\n\r\ncls = IMetaplan.IMetaplan()\r\nmetaObj = cls.getObject()\r\n\r\nmonth = _dict_obj['monthChoice'].GetSelection()+1\r\ntemplMonth = _dict_obj['monthTemplChoice'].GetSelection()+1\r\nyear = int(_dict_obj['yearSpinner'].GetValue())\r\ntemplYear = int(_dict_obj['yearTemplSpinner'].GetValue())\r\nprint ' Create :', templMonth, templYear, month, year\r\n\r\nplanUtils.genPlanTemplate(metaObj, 'analitic', templYear, templMonth, year, month)", 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u0421\u043e\u0437\u0434\u0430\u0442\u044c', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'2d187f18a4beac6928a2c86490b56f41', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'genBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(66, 96), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'style': 0, 'activate': 1, 'span': (1, 1), 'name': u'DefaultName_2157', 'component_module': None, 'border': 0, '_uuid': u'4ac68ecdbc93cb3c420e7cbfd293a8eb', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': wx.Point(31, 13), 'type': u'SizerSpace', 'size': (10, 10)}, {'activate': 1, 'show': 1, 'mouseClick': u"_dict_obj['GenMonthPlanDlg'].EndModal(wx.ID_CANCEL)\r\nresult=None", 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041e\u0442\u043c\u0435\u043d\u0430', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'a1492fca482f739a2979bd194630a7fa', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'closeBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(151, 96), 'onInit': None, 'refresh': None, 'mouseContextDown': None}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'setFocus': None, 'name': u'GenMonthPlanDlg', 'keyDown': u"keycod = event.GetKeyCode()\r\nprint ' Key=', keycod\r\nif keycod == wx.WXK_ESCAPE:\r\n    self.EndModal(wx.ID_OK)", 'alias': None, 'init_expr': None, 'position': wx.Point(0, 0), 'onInit': None}}