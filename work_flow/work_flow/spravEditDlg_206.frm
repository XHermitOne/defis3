{'spravEditDlg_206': {'style': 0, 'activate': 1, 'prim': u'', 'name': u'default_1120', 'component_module': None, '_uuid': u'8b4c69ef3148065c63fc7c4ebb18acf6', 'alias': None, 'init_expr': None, 'child': [{'style': 0, 'activate': 1, 'span': (1, 1), 'description': None, 'component_module': None, 'modules': {'ic.dlg': [u'ic_dlg']}, 'border': 0, '_uuid': u'617c79d7c63a8abeaa271276fd636741', 'proportion': 0, 'object': None, 'alias': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'size': (-1, -1), 'type': u'Import', 'name': u'all_imports'}, {'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (700, 400), 'style': 536877120, 'foregroundColor': None, 'span': (1, 1), 'title': u'\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0430:', 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'Dialog', 'description': None, 'onClose': None, '_uuid': u'0ddd201bba98b0714b1b398fc9b899d3', 'moveAfterInTabOrder': u'', 'killFocus': None, 'flag': 0, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'description': None, 'component_module': None, 'border': 0, 'span': (1, 1), '_uuid': u'fafd3cf5efc4d6ec1b31caa2b4d5caa2', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'keyDown': None, 'border': 0, 'size': (-1, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'layout': u'vertical', 'component_module': None, 'win1': {'activate': 1, 'show': 1, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'description': None, 'component_module': None, 'border': 0, 'span': (1, 1), '_uuid': u'4dbdc4d53aea40dcb6258e8c7bc46ded', 'proportion': 0, 'alias': None, 'flag': 8192, 'init_expr': None, 'child': [{'activate': u'0', 'show': 1, 'recount': None, 'keyDown': None, 'border': 0, 'size': (-1, -1), 'style': 2097668, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'ToolBar', 'description': None, '_uuid': u'70d8c707ded4671376096e004428de92', 'moveAfterInTabOrder': u'', 'flag': 0, 'child': [{'activate': 1, 'show': 1, 'text': u' \u041d\u0430\u0439\u0442\u0438: ', 'refresh': None, 'font': {'family': u'sansSerif', 'style': u'bold', 'underline': False, 'faceName': u'Tahoma', 'size': 8}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', 'description': None, '_uuid': u'11bd9daf66717742b935052771b04a76', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'findTxt1', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (0, 0), 'onInit': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'value': u'', 'font': {}, 'border': 0, 'size': (-1, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'5c5ea5c83bdfd647b67a949902ab219a', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'findEdit1', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None, 'refresh': []}, {'activate': 1, 'name': u'findTool1', 'toolType': 0, 'shortHelpString': u'\u041f\u043e\u0438\u0441\u043a', 'longHelpString': u'', '_uuid': u'107a7ff6f6baf06edec23a0d329db013', 'pushedBitmap': None, 'label': u'', 'isToggle': 0, 'init_expr': None, 'bitmap': u'@common.imgSearchData', 'type': u'ToolBarTool', 'onTool': u"find_str=_dict_obj['findEdit1'].GetValue()\ncur_item=_dict_obj['spravTree'].GetSelection()\r\n_dict_obj['spravTree'].ExpandAll(cur_item)\r\n\r\nif not cur_item.IsOk():\n    cur_item=None\r\nitem=_dict_obj['spravTree'].findItemString(find_str,\n    curItem=cur_item,columns=[1])\r\n\r\nif item is not None:\n    _dict_obj['spravTree'].SelectItem(item)"}], 'name': u'treeToolBar', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (0, 0), 'onInit': None, 'bitmap_size': (16, 15)}, {'activate': u'0', 'show': 1, 'labels': [u'\u041a\u043e\u0434', u'\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435', u's1', u's2', u's3', u'n1', u'n2', u'n3', u'f1', u'f2', u'f3', u'\u0414\u043e\u0441\u0442\u0443\u043f'], 'keyDown': None, 'selectChanged': u"#\u0412\u044b\u0431\u0440\u0430\u043d\u043d\u044b\u0439 \u043a\u043e\u0434\ntry:\n    cod=self.getSelectionRecord()[0]\nexcept:\n    cod=None\n\n#\u0421\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u0438\u0435 \u0432\u043d\u0435\u0441\u0435\u043d\u043d\u044b\u0445 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0439\n#print '!!!1',old_cod,cod,sprav.getLevelByCod(cod)\n#if old_cod<>cod:\n#    tab=_dict_obj['spravGrid'].GetTable().GetDataset().data\n#    print '!!!',old_cod,tab\n#    sprav.getStorage().setLevelTable(old_cod,tab)\n#    #\u041f\u0435\u0440\u0435\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0434\u0435\u0440\u0435\u0432\u043e \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0430\n#    sprav_tree=sprav.getStorage().getLevelTree()\n#    _dict_obj['spravTree'].loadTree(sprav_tree)\n\n    #sprav.getStorage().setLevelTable(old_cod,\n    #    _dict_obj['spravGrid'].GetTable().GetDataset().data)\nold_cod=cod\nlevel=sprav.getLevelByCod(cod)\n\n#\u041f\u043e\u043b\u0443\u0447\u0438\u0442\u044c \u0442\u0430\u0431\u043b\u0438\u0446\u0443\nlevel_tab=map(lambda rec: list(rec),\n    sprav.getStorage().getLevelTable(cod))\nif level_tab is not None:\n    _dict_obj['spravGrid'].GetDataset().SetDataBuff(level_tab)\n    #\u041e\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u0438\u0435 \u0434\u043b\u0438\u043d\u044b \u043a\u043e\u0434\u0430\n    if level:\n        len_cod=level.getCodLen()\n    else:\n        len_cod=sprav.getLevelByIdx(0).getCodLen()\n    _dict_obj['spravGrid'].GetDataset().SetStructFilter({'cod':[cod,len_cod]})\n    _dict_obj['spravGrid'].RefreshGrid()\n\n#\u041f\u043e\u043c\u0435\u043d\u044f\u0442\u044c \u043d\u0430\u0434\u043f\u0438\u0441\u0438 \u043a\u043e\u043b\u043e\u043d\u043e\u043a\nif level:\n    _dict_obj['spravTree'].setLabelCols(level.labelsNotice())\n    _dict_obj['spravGrid'].setColLabels(level.getNoticeDict())\n    is_next_level=level.isNext()\n    _dict_obj['spravToolBar'].enableTool('addTool',is_next_level)\n    _dict_obj['spravToolBar'].enableTool('delTool',is_next_level)\n    _dict_obj['spravToolBar'].enableTool('saveTool',is_next_level)", 'border': 0, 'titleRoot': u'@sprav.description', 'treeDict': {}, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'source': None, 'backgroundColor': None, 'size': (-1, -1), 'type': u'TreeListCtrlSimple', 'description': None, '_uuid': u'a9e90dcfb8d56fffb5b9eadaa675ecc0', 'style': 8193, 'flag': 8192, 'recount': None, 'itemCollapsed': None, 'itemExpanded': None, 'name': u'spravTree1', 'wcols': [200, 250, 50, 50, 50, 50, 50, 50, 50, 50, 50, 70], 'refresh': None, 'alias': None, 'itemActivated': None, 'init_expr': None, 'position': (-1, -1), 'onInit': u"sprav_tree=sprav.getStorage().getLevelTree()\n_dict_obj['spravTree'].loadTree(sprav_tree)\n\n#\u041f\u043e\u043b\u0443\u0447\u0438\u0442\u044c \u0442\u0430\u0431\u043b\u0438\u0446\u0443\r\nlevel_tab_tuple=sprav.getStorage().getLevelTable(None)\r\n#print '!!!',level_tab_tuple\r\nlevel_tab=map(lambda rec: list(rec),level_tab_tuple)\r\nif level_tab is not None:\r\n    _dict_obj['spravGrid'].GetDataset().SetDataBuff(level_tab)\r\n    #\r\n    len_cod=sprav.getLevelByIdx(0).getCodLen()\r\n    \r\n    _dict_obj['spravGrid'].GetDataset().SetStructFilter({'cod':[len_cod]})\r\n    _dict_obj['spravGrid'].RefreshGrid()\r\n"}, {'activate': 1, 'show': 1, 'labels': [u'\u041a\u043e\u0434', u'\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435', u's1', u's2', u's3', u'n1', u'n2', u'n3', u'f1', u'f2', u'f3', u'\u0414\u043e\u0441\u0442\u0443\u043f'], 'refresh': None, 'selectChanged': u"#\u0412\u044b\u0431\u0440\u0430\u043d\u043d\u044b\u0439 \u043a\u043e\u0434\r\ntry:\r\n    cod=_dict_obj['spravTree'].getSelectionRecord()[0]\r\nexcept:\r\n    cod=None\r\n\r\n#\u0421\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u0438\u0435 \u0432\u043d\u0435\u0441\u0435\u043d\u043d\u044b\u0445 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0439\r\n#print '!!!1',old_cod,cod,sprav.getLevelByCod(cod)\r\n#if old_cod<>cod:\r\n#    tab=_dict_obj['spravGrid'].GetTable().GetDataset().data\r\n#    print '!!!',old_cod,tab\r\n#    sprav.getStorage().setLevelTable(old_cod,tab)\r\n#    #\u041f\u0435\u0440\u0435\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0434\u0435\u0440\u0435\u0432\u043e \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0430\r\n#    sprav_tree=sprav.getStorage().getLevelTree()\r\n#    _dict_obj['spravTree'].loadTree(sprav_tree)\r\n\r\n    #sprav.getStorage().setLevelTable(old_cod,\r\n    #    _dict_obj['spravGrid'].GetTable().GetDataset().data)\r\nold_cod=cod\r\nlevel=sprav.getLevelByCod(cod)\r\n\r\n#\u041f\u043e\u043b\u0443\u0447\u0438\u0442\u044c \u0442\u0430\u0431\u043b\u0438\u0446\u0443\r\nlevel_tab=map(lambda rec: list(rec),\r\n    sprav.getStorage().getLevelTable(cod))\r\nif level_tab is not None:\r\n    _dict_obj['spravGrid'].GetDataset().SetDataBuff(level_tab)\r\n    #\u041e\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u0438\u0435 \u0434\u043b\u0438\u043d\u044b \u043a\u043e\u0434\u0430\r\n    if level:\r\n        len_cod=level.getCodLen()\r\n    else:\r\n        len_cod=sprav.getLevelByIdx(0).getCodLen()\r\n    _dict_obj['spravGrid'].GetDataset().SetStructFilter({'cod':[cod,len_cod]})\r\n    _dict_obj['spravGrid'].RefreshGrid()\r\n\r\n#\u041f\u043e\u043c\u0435\u043d\u044f\u0442\u044c \u043d\u0430\u0434\u043f\u0438\u0441\u0438 \u043a\u043e\u043b\u043e\u043d\u043e\u043a\r\nif level:\r\n    _dict_obj['spravTree'].setLabelCols(level.labelsNotice())\r\n    _dict_obj['spravGrid'].setColLabels(level.getNoticeDict())\r\n    is_next_level=level.isNext()\r\n    _dict_obj['spravToolBar'].enableTool('addTool',is_next_level)\r\n    _dict_obj['spravToolBar'].enableTool('delTool',is_next_level)\r\n    _dict_obj['spravToolBar'].enableTool('saveTool',is_next_level)", 'border': 0, 'size': (-1, -1), 'treeDict': {}, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'source': None, 'itemExpanded': None, 'titleRoot': u'@sprav.description', 'type': u'SimpleTreeListCtrl', 'description': None, '_uuid': u'95296977dde9682ac9c78cb739419286', 'style': 8193, 'flag': 8192, 'recount': None, 'itemCollapsed': None, 'backgroundColor': None, 'name': u'spravTree', 'wcols': [200, 250, 50, 50, 50, 50, 50, 50, 50, 50, 50, 70], 'keyDown': None, 'alias': None, 'itemActivated': None, 'init_expr': None, 'position': (-1, -1), 'onInit': u"sprav_tree=sprav.getStorage().getLevelTree()\r\n_dict_obj['spravTree'].loadTree(sprav_tree)\r\n\r\n#\u041f\u043e\u043b\u0443\u0447\u0438\u0442\u044c \u0442\u0430\u0431\u043b\u0438\u0446\u0443\r\nlevel_tab_tuple=sprav.getStorage().getLevelTable(None)\r\n#print '!!!',level_tab_tuple\r\nlevel_tab=map(lambda rec: list(rec),level_tab_tuple)\r\nif level_tab is not None:\r\n    _dict_obj['spravGrid'].GetDataset().SetDataBuff(level_tab)\r\n    #\r\n    len_cod=sprav.getLevelByIdx(0).getCodLen()\r\n    \r\n    _dict_obj['spravGrid'].GetDataset().SetStructFilter({'cod':[len_cod]})\r\n    _dict_obj['spravGrid'].RefreshGrid()\r\n"}], 'position': (0, 0), 'size': (-1, -1), 'type': u'BoxSizer', 'vgap': 0, 'name': u'DefaultName_1770'}], 'keyDown': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'46bdf4a4f1cfe7b7c988ab37625a9f52', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'recount': None, 'name': u'defaultWindow_1584', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}, 'proportion': 1, 'source': None, 'backgroundColor': None, 'type': u'SplitterWindow', 'win2': {'activate': 1, 'show': 1, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'description': None, 'component_module': None, 'border': 0, 'span': (1, 1), '_uuid': u'6c0bef3d0303e8cb6abe3f8a89aaa789', 'proportion': 0, 'alias': None, 'flag': 8192, 'init_expr': u'self.SetMinSize((10,10))', 'child': [{'style': 0, 'activate': u'1', 'span': (1, 1), 'description': None, 'component_module': None, 'border': 0, '_uuid': u'9dc22fdb39c6dbd8ac7759640ae2eb70', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'size': (0, 5), 'type': u'SizerSpace', 'name': u'SzrSp'}, {'activate': u'1', 'show': 1, 'recount': None, 'keyDown': None, 'border': 0, 'size': (300, -1), 'style': 2097668, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'ToolBar', 'description': None, '_uuid': u'69418939e02acea410757f2b696636fb', 'moveAfterInTabOrder': u'', 'flag': 8192, 'child': [{'activate': 1, 'name': u'addTool', 'toolType': 0, 'shortHelpString': u'\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c', 'longHelpString': u'', '_uuid': u'ae43bef6b364ba28e120a9a6b69978ee', 'pushedBitmap': None, 'label': u'', 'isToggle': 0, 'init_expr': None, 'bitmap': u'@common.imgPlus', 'type': u'ToolBarTool', 'onTool': u"if old_cod is None:\n    old_cod=''\nif old_cod:\n    level=sprav.getLevelByCod(old_cod).getNext()\nelse:\n    level=sprav.getLevelByCod(old_cod)\nnew_cod=old_cod\nif level:\n    cod_len=level.getCodLen()\n    new_cod+='*'*cod_len\n_dict_obj['spravGrid'].AddRows()\n_dict_obj['spravGrid'].setNameValue('cod',new_cod)\n"}, {'activate': 1, 'name': u'delTool', 'toolType': 0, 'shortHelpString': u'\u0423\u0434\u0430\u043b\u0438\u0442\u044c', 'longHelpString': u'', '_uuid': u'7db0e3ecf9876f61f3821f0f7c0addba', 'pushedBitmap': None, 'label': u'', 'isToggle': 0, 'init_expr': None, 'bitmap': u'@common.imgMinus', 'type': u'ToolBarTool', 'onTool': u"i_row=_dict_obj['spravGrid'].GetGridCursorRow()\r\n#tab=[_dict_obj['spravGrid'].GetDataset().data[i_row]]\r\n_dict_obj['spravGrid'].DelRows(i_row)\r\n#sprav.getStorage().delLevelTable(tab)"}, {'activate': 1, 'name': u'separator1_2034', '_uuid': u'5d4bfe7b0be6cc044908cf88ddc0c416', 'init_expr': None, 'type': u'Separator', 'size': 5}, {'activate': 1, 'name': u'saveTool', 'toolType': 0, 'shortHelpString': u'\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f', 'longHelpString': u'', '_uuid': u'29a6cba5d62b677123c3eb365cd30359', 'pushedBitmap': None, 'label': u'', 'isToggle': 0, 'init_expr': None, 'bitmap': u'@common.imgCheck', 'type': u'ToolBarTool', 'onTool': u"#\u0421\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u0438\u0435 \u0432\u043d\u0435\u0441\u0435\u043d\u043d\u044b\u0445 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0439\ntab=_dict_obj['spravGrid'].GetTable().GetDataset().data\ntab=sprav.getStorage().setTypeLevelTable(tab)\nsprav.getStorage().setLevelTable(old_cod,tab)\n#\u041f\u0435\u0440\u0435\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0434\u0435\u0440\u0435\u0432\u043e \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0430\nsprav_tree=sprav.getStorage().getLevelTree()\n_dict_obj['spravTree'].loadTree(sprav_tree)\n "}, {'activate': 1, 'name': u'separator1_2126', '_uuid': u'5d4bfe7b0be6cc044908cf88ddc0c416', 'init_expr': None, 'type': u'Separator', 'size': 5}, {'activate': 1, 'show': 1, 'text': u'\u041d\u0430\u0439\u0442\u0438: ', 'keyDown': None, 'font': {'family': u'sansSerif', 'style': u'bold', 'underline': False, 'faceName': u'Tahoma', 'size': 8}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', 'description': None, '_uuid': u'4bafe37230047a9467444e2719dedfb4', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'findTxt', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': (-1, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'8c7ec33d158cd46288d8da4abedcd2d4', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'findEdit', 'changed': None, 'value': u'', 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None, 'refresh': []}, {'activate': 1, 'name': u'findTool', 'toolType': 0, 'shortHelpString': u'\u041f\u043e\u0438\u0441\u043a', 'longHelpString': u'', '_uuid': u'd77479fe788e46bf29fcd04520cb8e6b', 'pushedBitmap': None, 'label': u'', 'isToggle': 0, 'init_expr': None, 'bitmap': u'@common.imgSearchData', 'type': u'ToolBarTool', 'onTool': u"find_str=_dict_obj['findEdit'].GetValue()\r\ncur_cursor=_dict_obj['spravGrid'].GetGridCursorRow()\r\ni_row,field=_dict_obj['spravGrid'].GetDataset().FindRowString(find_str,\r\n    cursor=cur_cursor,fields=['name'])\r\nif i_row>=0:\r\n    _dict_obj['spravGrid'].SetCursor(i_row,1)"}], 'name': u'spravToolBar', 'refresh': None, 'alias': None, 'init_expr': u'self.SetPosition((3,2))\r\nbgr = self.GetParent().GetBackgroundColour()\r\nself.SetBackgroundColour(clr)', 'position': (3, 2), 'onInit': None, 'bitmap_size': (16, 15)}, {'style': 0, 'activate': u'1', 'span': (1, 1), 'description': None, 'component_module': None, 'border': 0, '_uuid': u'940c3c8cb13aac8ad31fe711e8dd0cc6', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'size': (0, 5), 'type': u'SizerSpace', 'name': u'SzrSp_2829'}, {'activate': u'0', 'col_labels': [u'\u041a\u043e\u0434', u'\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435', u'\u0414\u043e\u0441\u0442\u0443\u043f', u's1', u's2', u's3', u'n1', u'n2', u'n3', u'f1', u'f2', u'f3'], 'show': 1, 'col_count': 12, 'refresh': None, 'hrows': [], 'border': 0, 'size': (-1, -1), 'row_labels': [], 'col_label_height': -1, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'row_label_width': 0, 'cellSelect': None, 'row_count': 1, 'component_module': None, 'proportion': 1, 'source': None, 'backgroundColor': None, 'type': u'SimpleGrid', 'description': None, '_uuid': u'22ec21085be3a8f55bee30347103a933', 'style': 0, 'flag': 8192, 'recount': None, 'child': [], 'name': u'spravGrid1', 'wcols': [100, 250, 70, 50, 50, 50, 50, 50, 50, 50, 50, 50], 'keyDown': u"key=event.GetKeyCode()\r\nif key==wx.WXK_INSERT:\r\n    if old_cod is None:\r\n        old_cod=''\r\n    cod_len=sprav.getLevelByCod(old_cod).getCodLen()\r\n    new_cod=old_cod+'*'*cod_len\r\n    _dict_obj['spravGrid'].appendRow(new_cod,'','',\r\n    '','','',\r\n    '0','0','0',\r\n    '0.0','0.0','0.0')", 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None, 'cellChange': None}, {'line_color': (200, 200, 200), 'activate': u'1', 'show': 1, 'cols': [{'activate': 1, 'ctrl': u"#\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0443\u043d\u0438\u043a\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u0438 \u043a\u043e\u0434\u0430\ntry:\r\n    new_cod=_dict_obj['spravTree'].getSelectionRecord()[0]\r\nexcept:\r\n    new_cod=None\r\n\r\n#ctrl_ret,val=sprav.Ctrl(value,None,'cod',cod=new_cod)\r\nbuff_codes=map(lambda rec: rec[0],\r\n    _dict_obj['spravGrid'].GetDataset().data)[:-1]\r\n#print '!',buff_codes,new_cod,value\r\nctrl_ret=2\r\nif value in buff_codes:\r\n    ctrl_ret=0\r\n\nif not ctrl_ret in [0,1]:\r\n    _resultEval=(0,None)\nelse:\n    ic_dlg.openMsgBox('\u0412\u041d\u0418\u041c\u0410\u041d\u0418\u0415!','\u0422\u0430\u043a\u043e\u0439 \u043a\u043e\u0434 \u0435\u0441\u0442\u044c \u0443\u0436\u0435 \u0432 \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0435!')\n    _resultEval=(3,None)", 'pic': u'S', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u0434', 'width': 100, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'f46aa54eb5a9e9a59dfcd8d12ef93977', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'2b82d744c4512e2f8cc8e624de3adefc', 'recount': None, 'hlp': None, 'attr': u'W', 'setvalue': u'', 'name': u'cod', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435', 'width': 250, 'init': u"@''", 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'f82af77ddf06306b3d40edff8b33a3c4', 'recount': None, 'hlp': None, 'attr': u'W', 'setvalue': u'', 'name': u'name', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u's1', 'width': 50, 'init': u"@''", 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'b16c5a659385c89e5f89a73e70c94a62', 'recount': None, 'getvalue': u'', 'name': u's1', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u's2', 'width': 50, 'init': u"@''", 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'b16c5a659385c89e5f89a73e70c94a62', 'recount': None, 'hlp': None, 'name': u's2', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u's3', 'width': 50, 'init': u"@''", 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'b16c5a659385c89e5f89a73e70c94a62', 'recount': None, 'hlp': None, 'name': u's3', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'N', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'n1', 'width': 50, 'init': u'0', 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'b16c5a659385c89e5f89a73e70c94a62', 'recount': None, 'hlp': None, 'name': u'n1', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'N', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'n2', 'width': 50, 'init': u'0', 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'b16c5a659385c89e5f89a73e70c94a62', 'recount': None, 'hlp': None, 'name': u'n2', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'N', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'n3', 'width': 50, 'init': u'0', 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'b16c5a659385c89e5f89a73e70c94a62', 'recount': None, 'hlp': None, 'name': u'n3', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'F', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'f1', 'width': 50, 'init': u'0.0', 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'b16c5a659385c89e5f89a73e70c94a62', 'recount': None, 'hlp': None, 'name': u'f1', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'F', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'f2', 'width': 50, 'init': u'0.0', 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'b16c5a659385c89e5f89a73e70c94a62', 'recount': None, 'hlp': None, 'name': u'f2', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'F', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'f3', 'width': 50, 'init': u'0.0', 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'47ef57b717e70c7b171945765fe28ced', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'b16c5a659385c89e5f89a73e70c94a62', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'f3', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u0414\u043e\u0441\u0442\u0443\u043f', 'width': 70, 'init': u"@''", 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'description': None, 'shortHelpString': u'', '_uuid': u'e3679c864c3223113e42d69c70086818', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'access', 'keyDown': None, 'alias': None, 'init_expr': None}], 'keyDown': None, 'border': 0, 'post_select': None, 'size': (-1, -1), 'moveAfterInTabOrder': u'', 'dclickEditor': None, 'span': (1, 1), 'delRec': None, 'component_module': None, 'row_height': 20, 'selected': None, 'proportion': 1, 'init': None, 'label': u'Grid', 'source': None, 'getattr': None, 'backgroundColor': None, 'fixRowSize': 0, 'type': u'GridDataset', 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'fixColSize': 0, 'description': None, 'post_del': None, 'post_init': None, '_uuid': u'95a0ec8bb60e98ca736bed065e7d8d69', 'style': 0, 'docstr': u'ic.components.icgrid.html', 'flag': 8192, 'foregroundColor': None, 'recount': None, 'label_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': None, 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'label_attr', 'alignment': (u'left', u'middle')}, 'name': u'spravGrid', 'label_height': 20, 'changed': None, 'onSize': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None, 'refresh': None}, {'activate': u'0', 'show': 1, 'child': [], 'keyDown': None, 'border': 0, 'size': (300, 20), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'a9a2847c2c80d652692f99fdbacf44aa', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'recount': None, 'name': u'defaultWindow_1226_1415_2189', 'refresh': None, 'alias': None, 'init_expr': u"import ic.utils.graphicUtils as graph\r\nimport wx\r\nbgr = self.GetParent().GetBackgroundColour()\r\nclr = graph.getMidColour(bgr, wx.Color(255,255,255), 0.5)\r\nprint '-------------', clr\r\nself.setRoundBoundMode((150,150,130), 1)\r\nself.SetBackgroundColour(clr)\r\n_dict_obj['spravToolBar'].SetBackgroundColour(clr)\r\nself.SetSize((300,20))", 'position': (-1, -1), 'onInit': None}], 'position': (0, 0), 'size': (-1, 30), 'type': u'BoxSizer', 'vgap': 0, 'name': u'leftPanelSZR'}], 'keyDown': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'd22792960188e4b0d117c9d56d113162', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'recount': None, 'name': u'defaultWindow_1677', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}, 'description': None, '_uuid': u'fa55c7c4ffcfb8cc7464c1b5a3f8ee81', 'style': 768, 'docstr': u'ic.components.icsplitter-module.html', 'flag': 8192, 'recount': None, 'span': (1, 4), 'name': u'panelSplitter', 'min_panelsize': 20, 'refresh': None, 'alias': None, 'init_expr': None, 'position': (0, 0), 'sash_pos': 300, 'onInit': None}, {'style': 0, 'activate': 1, 'span': (1, 1), 'description': None, 'component_module': None, 'border': 0, '_uuid': u'0679d55d1db7d4689775fc6837eb0cbf', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'size': (0, 5), 'type': u'SizerSpace', 'name': u'DefaultName_1408_2140'}, {'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'horizontal', 'description': None, 'component_module': None, 'border': 0, 'span': (1, 4), '_uuid': u'85c15370c34e6276419e502516faa254', 'proportion': 0, 'alias': None, 'flag': 2304, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'mouseClick': u"result=None\r\n_dict_obj['SpravEditDlg'].EndModal(wx.ID_CANCEL)\r\n_resultEval=True", 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u0412\u044b\u0445\u043e\u0434', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'description': None, '_uuid': u'c23c4093058559049a21ae776a7f532d', 'moveAfterInTabOrder': u'', 'flag': 2560, 'recount': None, 'name': u'cancel_button', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (1, 2), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'show': 1, 'mouseClick': u"result=True\r\n_dict_obj['SpravEditDlg'].EndModal(wx.ID_OK)\r\n_resultEval=True", 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'OK', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'description': None, '_uuid': u'f14ba7beeed504cb9fb7dcf6c36b3c44', 'moveAfterInTabOrder': u'', 'flag': 2560, 'recount': None, 'name': u'ok_button', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (1, 3), 'onInit': None, 'refresh': None, 'mouseContextDown': None}], 'position': (1, 0), 'size': (-1, -1), 'type': u'BoxSizer', 'vgap': 0, 'name': u'DefaultName_1308_1782'}, {'style': 0, 'activate': 1, 'span': (1, 1), 'description': None, 'component_module': None, 'border': 0, '_uuid': u'0679d55d1db7d4689775fc6837eb0cbf', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'size': (0, 5), 'type': u'SizerSpace', 'name': u'DefaultName_1408'}], 'position': (0, 0), 'size': (-1, -1), 'type': u'BoxSizer', 'vgap': 0, 'name': u'DefaultName_1314'}], 'setFocus': None, 'name': u'SpravEditDlg', 'keyDown': u"key=event.GetKeyCode()\r\nif key==wx.WXK_ESCAPE:\r\n    result=None\r\n    _dict_obj['SpravEditDlg'].EndModal(wx.ID_CANCEL)\r\n    _resultEval=True    ", 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': u"old_cod=''"}], 'type': u'Group', 'description': None}}