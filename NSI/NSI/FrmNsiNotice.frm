{'FrmNsiNotice': {'activate': u'1', 'prim': u'', 'name': u'FrmNsiNotice', '_uuid': u'd3b47b3aa422004cc4d2437576182470', 'init_expr': None, 'child': [{'activate': u'1', 'show': u'1', 'recount': None, 'keyDown': None, 'border': 0, 'size': (650, 400), 'style': 536877120, 'foregroundColor': None, 'span': (1, 1), 'title': u'\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0434\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0445 \u043f\u043e\u043b\u0435\u0439', 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'Dialog', 'onClose': None, '_uuid': u'b171872e4bc8e56c52d50ad14a84abbe', 'moveAfterInTabOrder': u'', 'killFocus': None, 'flag': 0, 'child': [{'activate': u'1', 'prim': u'', 'name': u'\u0414\u0430\u043d\u043d\u044b\u0435_1028', '_uuid': u'b171872e4bc8e56c52d50ad14a84abbe', 'init_expr': None, 'child': [{'style': 0, 'activate': u'1', 'span': (1, 1), 'name': u'imp_277', 'proportion': 0, '_uuid': u'6d58eaf61bb9fd1dc1ac6f5383832635', 'modules': {'ic.db.icsqlobjdataset': [u'icSQLObjDataSet'], 'NSI.spravfunc': [u'*']}, 'object': None, 'alias': None, 'flag': 0, 'init_expr': u'', 'type': u'Import', 'position': (-1, -1), 'border': 0, 'size': (-1, -1)}, {'activate': u'1', 'name': u'NsiNotice', '_uuid': u'b71d20130c75663ca0b2faeafcf617a6', 'docstr': u'ic.db.icdataset-module.html', 'filter': u'', 'alias': None, 'res_query': u'NsiNotice', 'init_expr': None, 'file': u'NsiNotice.tab', 'type': u'DataLink', 'link_expr': u''}, {'activate': u'1', 'name': u'NsiList', '_uuid': u'26e55379e37231b081ca0ba9f17d5889', 'docstr': u'ic.db.icdataset-module.html', 'filter': u'', 'alias': None, 'res_query': u'NsiList', 'init_expr': None, 'file': u'NsiList.tab', 'type': u'DataLink', 'link_expr': u''}, {'activate': u'1', 'name': u'NsiLevel', '_uuid': u'b57e8fa03db5e63639fb8994e43c6d0c', 'docstr': u'ic.db.icdataset-module.html', 'filter': u'', 'alias': None, 'res_query': u'NsiLevel', 'init_expr': None, 'file': u'NsiLevel.tab', 'type': u'DataLink', 'link_expr': u''}], 'type': u'Group'}, {'hgap': 0, 'style': 0, 'activate': u'1', 'layout': u'vertical', 'description': None, 'position': (-1, -1), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'12504c9bab19d2a025108930b44d225d', 'proportion': 0, 'name': u'DefaultName_946_1503_1754', 'alias': None, 'flag': 0, 'init_expr': u'', 'child': [{'activate': 1, 'show': 1, 'borderRightColor': (167, 160, 150), 'child': [{'activate': u'1', 'show': u'1', 'text': u"_NsiList.get(_NsiLevel.get(NsiNotice.filter['id_nsi_level']).id_nsi_listID).name", 'refresh': None, 'font': {'style': u'italic', 'name': u'defaultFont', 'family': u'sansSerif', 'faceName': u'Times New Roman', 'type': u'Font', 'underline': 0, 'size': 11}, 'border': 0, 'size': (-1, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'a14bb33f927f1cfecaccb21e52e45075', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'titleNotice_2704', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (30, 4)}, {'activate': 1, 'show': 1, 'hlp': None, 'keyDown': None, 'file': u'@common.imgHelp', 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'Image', '_uuid': u'd23704e71ef14b8f813e84621737b115', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': [], 'field_name': None, 'name': u'DefaultName_4148', 'refresh': [], 'alias': None, 'init_expr': None, 'position': (5, 5)}], 'refresh': None, 'borderTopColor': (167, 160, 150), 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': wx.Size(643, 27), 'moveAfterInTabOrder': u'', 'foregroundColor': (0, 64, 128), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'init_expr': None, 'description': None, 'shortHelpString': u'', 'backgroundColor2': None, '_uuid': u'5cda9a5562836ef27fb7f494ea76dfa0', 'style': 0, 'bgrImage': None, 'flag': 8192, 'recount': None, 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 1, 'borderLeftColor': (167, 160, 150), 'name': u'HeadCellTitle', 'borderBottomColor': (167, 160, 150), 'keyDown': None, 'alias': None, 'borderWidth': 1, 'position': wx.Point(0, 0), 'borderStyle': None, 'onInit': u'self.setRoundCorners((1,1,1,1))'}, {'style': 0, 'activate': u'1', 'span': (1, 1), 'description': None, 'component_module': None, 'type': u'SizerSpace', '_uuid': u'30c2a238d0f77276eb070caa16639e73', 'proportion': 0, 'name': u'sp1', 'alias': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'border': 0, 'size': (0, 2)}, {'activate': u'1', 'show': u'1', 'proportion': 0, 'buttonDel': 1, 'refresh': None, 'border': 0, 'size': (200, 20), 'style': 512, 'foregroundColor': None, 'span': (1, 1), 'onPrint': None, 'buttonAdd': 1, 'source': u'NsiNotice', 'onAdd': None, 'backgroundColor': None, 'type': u'DatasetNavigator', 'buttonPrint': 0, '_uuid': u'26c264541da6df9028d6bef9155065c9', 'onHelp': None, 'moveAfterInTabOrder': u'', 'onUpdate': None, 'flag': 8192, 'object_link': None, 'recount': None, 'onDelete': None, 'name': u'default_1014', 'keyDown': None, 'alias': None, 'init_expr': None, 'buttonHelp': 0, 'position': (-1, -1), 'buttonUpdate': 0}, {'style': 0, 'activate': u'1', 'span': (1, 1), 'description': None, 'component_module': None, 'type': u'SizerSpace', '_uuid': u'9c52d20b944d64b360e2135156fb2ac6', 'proportion': 0, 'name': u'sp1_601', 'alias': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'border': 0, 'size': (0, 5)}, {'activate': 1, 'show': 1, 'recount': None, 'keyDown': None, 'font': {}, 'border': 0, 'alignment': u"('left', 'middle')", 'size': (-1, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': (235, 235, 235), 'type': u'Head', 'description': None, '_uuid': u'bd041a6d02b6f2d6fc4dd21830154a63', 'style': 0, 'flag': 8192, 'child': [{'activate': u'0', 'show': 1, 'borderRightColor': (100, 100, 100), 'recount': None, 'keyDown': None, 'borderTopColor': (182, 182, 182), 'font': {'family': u'sansSerif', 'style': u'bold', 'underline': False, 'faceName': u'Arial', 'size': 8}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (50, 22), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u0422\u0438\u043f', 'source': None, 'backgroundColor': (255, 255, 255), 'isSort': False, 'type': u'HeadCell', 'init_expr': None, 'description': None, 'shortHelpString': u'\u0422\u0438\u043f \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0430', 'backgroundColor2': None, '_uuid': u'b4cbe0fe54f0c896ca29082985c8d919', 'style': 0, 'bgrImage': None, 'flag': 0, 'child': [], 'cursorColor': (100, 100, 100), 'backgroundType': 1, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'type', 'borderBottomColor': (100, 100, 100), 'refresh': None, 'alias': None, 'borderWidth': 1, 'position': (0, 0), 'borderStyle': None, 'onInit': None}, {'activate': u'0', 'show': 1, 'borderRightColor': (100, 100, 100), 'recount': None, 'keyDown': None, 'borderTopColor': (182, 182, 182), 'font': {'style': u'bold', 'size': 8, 'underline': False, 'faceName': u'Arial', 'family': u'sansSerif'}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (50, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u0423\u0440\u043e\u0432\u0435\u043d\u044c', 'source': None, 'backgroundColor': (255, 255, 255), 'isSort': False, 'type': u'HeadCell', 'init_expr': None, 'description': None, 'shortHelpString': u'\u041d\u043e\u043c\u0435\u0440 \u0443\u0440\u043e\u0432\u0435\u043d\u044f \u043a\u043e\u0434\u0430', 'backgroundColor2': None, '_uuid': u'041431047fc498893ef67159b6e189c5', 'style': 0, 'bgrImage': None, 'flag': 0, 'child': [], 'cursorColor': (100, 100, 100), 'backgroundType': 1, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'level', 'borderBottomColor': (100, 100, 100), 'refresh': None, 'alias': None, 'borderWidth': 1, 'position': (0, 1), 'borderStyle': None, 'onInit': None}, {'activate': u'0', 'show': 1, 'borderRightColor': (100, 100, 100), 'recount': None, 'keyDown': None, 'borderTopColor': (182, 182, 182), 'font': {'family': u'sansSerif', 'style': u'bold', 'underline': False, 'faceName': u'Arial', 'size': 8}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (50, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u0418\u043c\u044f \u043f\u043e\u043b\u044f', 'source': None, 'backgroundColor': (255, 255, 255), 'isSort': False, 'type': u'HeadCell', 'init_expr': None, 'description': None, 'shortHelpString': u'', 'backgroundColor2': None, '_uuid': u'54c71853dede79d189a4763980360fdb', 'style': 0, 'bgrImage': None, 'flag': 0, 'child': [], 'cursorColor': (100, 100, 100), 'backgroundType': 1, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'fld_name', 'borderBottomColor': (100, 100, 100), 'refresh': None, 'alias': None, 'borderWidth': 1, 'position': (0, 2), 'borderStyle': None, 'onInit': None}, {'activate': u'0', 'show': 1, 'borderRightColor': (100, 100, 100), 'recount': None, 'keyDown': None, 'borderTopColor': (182, 182, 182), 'font': {'family': u'sansSerif', 'style': u'bold', 'underline': False, 'faceName': u'Arial', 'size': 8}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (50, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043f\u043e\u043b\u044f', 'source': None, 'backgroundColor': (255, 255, 255), 'isSort': False, 'type': u'HeadCell', 'init_expr': None, 'description': None, 'shortHelpString': u'', 'backgroundColor2': None, '_uuid': u'2bfca6f592762080e9c2f73f81a4d6c9', 'style': 0, 'bgrImage': None, 'flag': 0, 'child': [], 'cursorColor': (100, 100, 100), 'backgroundType': 1, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'descr', 'borderBottomColor': (100, 100, 100), 'refresh': None, 'alias': None, 'borderWidth': 1, 'position': (0, 3), 'borderStyle': None, 'onInit': None}, {'activate': u'1', 'proportion': 0, 'border': 0, 'size': (50, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'przn_border': [1, 1, 0, 1], 'label': u'\u0422\u0438\u043f', 'isSort': 0, 'scheme': u'GOLD', 'type': u'NsiLabelCell', 'description': None, 'shortHelpString': u'', 'nest': None, '_uuid': u'7f6950e85b377a694d4bd0e6f873a6ae', 'flag': 0, 'child': [], 'name': u'LType', 'round_corner': [1, 0, 0, 0], 'alias': None, 'init_expr': None, 'position': (0, 0)}, {'activate': u'1', 'proportion': 0, 'border': 0, 'size': (50, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'przn_border': [1, 1, 0, 1], 'label': u'\u0423\u0440\u043e\u0432.', 'isSort': 0, 'scheme': u'GOLD', 'type': u'NsiLabelCell', 'description': None, 'shortHelpString': u'', 'nest': None, '_uuid': u'f1dfcb0529c77a5c775971b16efa863b', 'flag': 0, 'child': [], 'name': u'LLevel', 'round_corner': [0, 0, 0, 0], 'alias': None, 'init_expr': None, 'position': (0, 1)}, {'activate': u'1', 'proportion': 0, 'border': 0, 'size': (50, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'przn_border': [1, 1, 0, 1], 'label': u'\u0418\u043c\u044f \u043f\u043e\u043b\u044f', 'isSort': 0, 'scheme': u'GOLD', 'type': u'NsiLabelCell', 'description': None, 'shortHelpString': u'', 'nest': None, '_uuid': u'b6794b12bb5551bee4bda9c3ebd1f14d', 'flag': 0, 'child': [], 'name': u'LFld_name', 'round_corner': [0, 0, 0, 0], 'alias': None, 'init_expr': None, 'position': (0, 2)}, {'activate': 1, 'proportion': 0, 'border': 0, 'size': (50, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'przn_border': [1, 1, 1, 1], 'label': u'\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043f\u043e\u043b\u044f', 'isSort': 0, 'scheme': u'GOLD', 'type': u'NsiLabelCell', 'description': None, 'shortHelpString': u' \u041a\u0440\u0430\u0442\u043a\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043f\u043e\u043b\u0435, \u043a\u043e\u0442\u043e\u0440\u043e\u0435 \r\n \u0431\u0443\u0434\u0435\u0442 \u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0430\u0442\u044c\u0441\u044f \u0432 \u0448\u0430\u043f\u043a\u0435 \u043f\u0440\u0438 \r\n \u0440\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0438 \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u043e\u0432', 'nest': None, '_uuid': u'c27a9ae5bfdbaaba5f28dc5881515033', 'flag': 0, 'child': [], 'name': u'LDescr', 'round_corner': [0, 1, 0, 0], 'alias': None, 'init_expr': None, 'position': (0, 3)}], 'name': u'HeadNotice', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}, {'line_color': (210, 214, 223), 'activate': u'1', 'show': u'1', 'cols': [{'sort': u'1', 'setvalue': u'', 'attr': None, 'ctrl': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', 'activate': u'1', 'backgroundColor': (255, 255, 255), 'font': {'style': u'bold', 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'pic': u'N', 'keyDown': None, 'hlp': None, 'width': 70, 'init': u'None', 'activate': u'0', 'recount': None, 'label': u'id\\n\u0443\u0440\u043e\u0432\u043d\u044f\\n\u043a\u043e\u0434\u0430', 'type': u'GridCell', 'valid': u'None', 'getvalue': u'', 'name': u'id_nsi_level'}, {'activate': u'1', 'ctrl': None, 'pic': u'S', 'getvalue': u'', 'style': 0, 'show': u'1', 'label': u'\u0422\u0438\u043f', 'width': 70, 'init': u"@_NsiLevel.get(NsiNotice.filter['id_nsi_level']).type", 'valid': u'None', 'type': u'GridCell', 'sort': u'1', 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'activate': u'1', 'backgroundColor': (255, 255, 255), 'font': {'style': u'bold', 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'9c52d20b944d64b360e2135156fb2ac6', 'recount': None, 'hlp': None, 'name': u'type', 'setvalue': u'', 'attr': u'R', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': u'1', 'ctrl': None, 'pic': u'S', 'getvalue': u'', 'style': 0, 'show': u'1', 'label': u'\u0423\u0440\u043e\u0432\u0435\u043d\u044c', 'width': 70, 'init': u"@_NsiLevel.get(NsiNotice.filter['id_nsi_level']).level", 'valid': u'None', 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'activate': u'1', 'backgroundColor': (255, 255, 255), 'font': {'style': u'italic', 'name': u'defaultFont', 'family': u'sansSerif', 'faceName': u'Times New Roman', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'61a60cbfb38b2960bd4a9683040e9880', 'recount': None, 'hlp': None, 'name': u'level', 'setvalue': u'', 'attr': u'R', 'keyDown': u'None', 'alias': None, 'init_expr': None}, {'activate': u'1', 'ctrl': u'None', 'pic': u'CH', 'hlp': None, 'style': 0, 'show': u'1', 'label': u'\u0418\u043c\u044f\\n\u043f\u043e\u043b\u044f', 'width': 117, 'init': None, 'valid': u's1,s2,s3,s4,s5,n1,n2,n3,n4,n5,f1,f2,f3,f4,f5,d1,d2,d3,d4,d5', 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'5c5e5302bed5fd100ae2ebd05a9bf8c9', 'recount': u'None', 'getvalue': u'', 'name': u'fld_name', 'setvalue': u'', 'attr': None, 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': u'1', 'ctrl': u'None', 'pic': u'S', 'getvalue': u'', 'style': 0, 'component_module': None, 'show': u'1', 'label': u'\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043f\u043e\u043b\u044f', 'width': 242, 'init': None, 'valid': u'None', 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'5c5e5302bed5fd100ae2ebd05a9bf8c9', 'recount': None, 'hlp': None, 'name': u'descr', 'setvalue': u'', 'attr': None, 'keyDown': None, 'alias': None, 'init_expr': None}], 'row_height': 18, 'onSize': None, 'border': 0, 'post_select': None, 'size': (200, 200), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'delRec': None, 'component_module': None, 'selected': None, 'proportion': 1, 'getattr': u'#iter_rowcol(self, [(234,234,234), None])', 'label': u'Grid', 'source': u'NsiNotice', 'init': None, 'backgroundColor': None, 'fixRowSize': 0, 'type': u'GridDataset', '_uuid': u'6b854bcc0c221122016b868d59998efd', 'fixColSize': 0, 'description': None, 'post_del': None, 'post_init': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'fb7f05b2e2adb371dd44105432a1af5a', 'activate': u'1', 'backgroundColor': (247, 247, 247), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'style': 0, 'docstr': u'ic.components.icgrid.html', 'flag': 8192, 'dclickEditor': None, 'recount': None, 'label_attr': {'foregroundColor': (255, 255, 255), 'name': u'', '_uuid': None, 'activate': u'1', 'init_expr': None, 'backgroundColor': (115, 115, 185), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'label_attr', 'alignment': u"('left', 'middle')"}, 'name': u'gridNotice', 'label_height': 35, 'changed': None, 'keyDown': u'# \u041e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430 \u043d\u0430\u0436\u0430\u0442\u0438\u044f \u043a\u043b\u0430\u0432\u0438\u0448\u044c \u0413\u0440\u0438\u0434\u0430\r\nkey=event.GetKeyCode()\r\n\r\nif key==wx.WXK_ESCAPE and not event.ShiftDown() and not event.AltDown():\r\n\t_dict_obj["DlgNsiNotice"].EndModal(wx.ID_CANCEL)\r\n\r\n\r\n', 'alias': None, 'init_expr': u"header = _dict_obj['HeadNotice']\r\nself.setHeader(header, False, True)\r\nself.doReconstructHeader()", 'position': (-1, -1), 'onInit': None, 'refresh': u'None'}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'setFocus': None, 'name': u'DlgNsiNotice', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1)}, {'style': 0, 'activate': u'1', 'span': (1, 1), 'name': u'imp_3102', 'modules': {}, 'border': 0, '_uuid': u'cd1e03023afc86e2e9bc97f709e2ae37', 'proportion': 0, 'object': None, 'alias': None, 'flag': 0, 'init_expr': u"method('SetLastRow', 'NSI', locals(), grid=_dict_obj['gridNotice'])", 'position': (-1, -1), 'type': u'Import', 'size': (-1, -1)}], 'type': u'Group'}}