{'MonthYearDlg': {'activate': 1, 'show': 1, 'recount': None, 'keyDown': u"keycod = evt.GetKeyCode()\r\n#print ' Key=', keycod\r\nif keycod == wx.WXK_ESCAPE:\r\n    self.EndModal(wx.ID_CANCEL)", 'border': 0, 'size': (220, 85), 'style': 536877120, 'foregroundColor': None, 'span': (1, 1), 'title': u'\u041c\u0435\u0441\u044f\u0446 - \u0433\u043e\u0434', 'component_module': None, 'proportion': 1, 'source': None, 'backgroundColor': None, 'type': u'Dialog', 'onClose': None, '_uuid': u'5f0cf24c7cbabdf80a1b3b8fe09a036b', 'moveAfterInTabOrder': u'', 'killFocus': None, 'flag': 8192, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'span': (1, 1), 'name': u'DefaultName_1430', 'flexRows': [], 'minCellWidth': 10, 'type': u'GridBagSizer', 'border': 0, '_uuid': u'e3fac0568de29bf5f4f0af6e41e8f69d', 'proportion': 0, 'alias': None, 'flag': 0, 'minCellHeight': 5, 'init_expr': None, 'child': [{'activate': u'0', 'show': 1, 'keyDown': None, 'border': 0, 'size': (-1, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'DatePickerCtrl', '_uuid': u'9c0941eec90d4a68fa43335ba7f0de52', 'style': 2, 'flag': 0, 'recount': None, 'name': u'default_1520', 'value': u'', 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None, 'refresh': None}, {'activate': 1, 'show': 1, 'keyDown': None, 'border': 0, 'size': wx.Size(85, 21), 'style': 33555520, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': (255, 255, 255), 'type': u'Choice', 'loseFocus': None, '_uuid': u'1d6ea0bfba9e6ca6f953e19bf9383276', 'moveAfterInTabOrder': u'', 'choice': None, 'flag': 0, 'recount': [], 'field_name': None, 'setFocus': None, 'name': u'monthChoice', 'items': u"['\u042f\u043d\u0432\u0430\u0440\u044c',\r\n'\u0424\u0435\u0432\u0440\u0430\u043b\u044c',\r\n'\u041c\u0430\u0440\u0442',\r\n'\u0410\u043f\u0440\u0435\u043b\u044c',\r\n'\u041c\u0430\u0439',\r\n'\u0418\u044e\u043d\u044c',\r\n'\u0418\u044e\u043b\u044c',\r\n'\u0410\u0432\u0433\u0443\u0441\u0442',\r\n'\u0421\u0435\u043d\u0442\u044f\u0431\u0440\u044c',\r\n'\u041e\u043a\u0442\u044f\u0431\u0440\u044c',\r\n'\u041d\u043e\u044f\u0431\u0440\u044c',\r\n'\u0414\u0435\u043a\u0430\u0431\u0440\u044c']", 'refresh': [], 'alias': None, 'init_expr': None, 'position': (1, 1), 'onInit': None}, {'activate': 1, 'show': 1, 'value': 2005, 'font': {}, 'border': 0, 'size': wx.Size(84, 21), 'style': 33562624, 'foregroundColor': None, 'span': (1, 1), 'min': 0, 'component_module': None, 'proportion': 0, 'source': None, 'init': None, 'backgroundColor': None, 'type': u'Spinner', 'loseFocus': None, 'max': 2100, '_uuid': u'12c601c6533608346324c34147f0d7db', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'field_name': None, 'setFocus': None, 'name': u'yearSpinner', 'keyDown': None, 'alias': None, 'onSpin': None, 'init_expr': None, 'position': (1, 3), 'onInit': None, 'refresh': []}, {'activate': 1, 'show': 1, 'mouseClick': u"month='%02i'%(_dict_obj['monthChoice'].GetSelection()+1)\nyear=str(_dict_obj['yearSpinner'].GetValue())\n_root_obj.EndModal(wx.ID_OK)\nresult=(month,year)", 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041e\u041a', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'21159985c7ea42edc3357b2d999958fd', 'moveAfterInTabOrder': u'', 'flag': 10752, 'recount': None, 'name': u'okButton', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (3, 3), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'show': 1, 'mouseClick': u"_dict_obj['MonthYearDlg'].EndModal(wx.ID_CANCEL)\r\nresult=None", 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041e\u0442\u043c\u0435\u043d\u0438\u0442\u044c', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'92c376f80399b89f32e06a047fb9f39a', 'moveAfterInTabOrder': u'', 'flag': 10752, 'recount': None, 'name': u'cancelButton', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (3, 1), 'onInit': None, 'refresh': None, 'mouseContextDown': None}], 'component_module': None, 'position': (-1, -1), 'flexCols': [], 'vgap': 0, 'size': (-1, -1)}], 'setFocus': None, 'name': u'MonthYearDlg', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(0, 0), 'onInit': u"_dict_obj['monthChoice'].SetSelection(0)"}}