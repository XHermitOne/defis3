{u'std_refbook_brws_dlg': {'activate': 1, 'obj_module': None, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (700, 400), 'style': 536877056, 'foregroundColor': None, 'span': (1, 1), 'fit': False, 'title': u'@GetResModule().onDialogTitle(GetContext())', 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': 'Dialog', 'res_module': u'std_refbook_brws_dlg_frm.py', 'enable': True, 'description': None, 'onClose': None, '_uuid': '63ee80d1b4033ad844e8d05972ed0632', 'moveAfterInTabOrder': '', 'killFocus': None, 'flag': 0, 'alias': None, 'child': [{'activate': 1, 'obj_module': None, 'data_name': None, 'border': 0, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'type': 'BoxSizer', 'res_module': None, 'hgap': 0, 'description': None, '_uuid': 'b477b692485a6cc87ce244a4c9ced1ae', 'flag': 0, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'recount': None, 'keyDown': None, 'border': 0, 'size': (-1, -1), 'style': 2097668, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': 'ToolBar', 'res_module': None, 'description': None, '_uuid': '4a615c845eecc0fdc05ef11001b52620', 'moveAfterInTabOrder': '', 'flag': 8192, 'child': [{'activate': 1, 'name': 'add_tool', 'toolType': 0, 'shortHelpString': u'\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435', 'longHelpString': '', '_uuid': 'd8aa7b08ee0b5f69b5625784674f9425', 'pushedBitmap': None, 'label': '', 'isToggle': 0, 'init_expr': None, 'bitmap': '@common.imgPlus', 'type': 'ToolBarTool', 'onTool': None}, {'activate': 1, 'name': 'del_tool', 'toolType': 0, 'shortHelpString': u'\u0423\u0434\u0430\u043b\u0435\u043d\u0438\u0435', 'longHelpString': '', '_uuid': '1581287d81176ad9054765e277f02a51', 'pushedBitmap': None, 'label': '', 'isToggle': 0, 'init_expr': None, 'bitmap': '@common.imgMinus', 'type': 'ToolBarTool', 'onTool': u'GetResModule().onDelObjTool(GetContext())'}, {'activate': 1, 'name': 'edit_tool', 'toolType': 0, 'shortHelpString': u'\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435', 'longHelpString': '', '_uuid': '3f559e1132455fd994def47267e24f21', 'pushedBitmap': None, 'label': '', 'isToggle': 0, 'init_expr': None, 'bitmap': '@common.imgEdit', 'type': 'ToolBarTool', 'onTool': None}, {'activate': 1, 'name': u'save_tool', 'toolType': 0, 'shortHelpString': u'\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f', 'longHelpString': '', '_uuid': 'f3e70551fb5286ebe6de89405c8fe44b', 'pushedBitmap': None, 'label': '', 'isToggle': 0, 'init_expr': None, 'bitmap': u'@common.imgCheck', 'type': 'ToolBarTool', 'onTool': u'GetResModule().onSaveToolMouseClick(GetContext())'}, {'activate': 1, 'name': 'separator1', '_uuid': None, 'init_expr': None, 'type': 'Separator', 'size': 5}, {'activate': u'0', 'name': 'mode_tool', 'toolType': 0, 'shortHelpString': 'icButton', 'longHelpString': '', '_uuid': 'bb53d9817229a7b83e67d0de175bafee', 'pushedBitmap': None, 'label': '', 'isToggle': 0, 'init_expr': None, 'bitmap': '@common.imgProperties', 'type': 'ToolBarTool', 'onTool': u'GetResModule().onBrwsModeTool(GetContext())'}, {'activate': u'0', 'name': 'separator2', '_uuid': '7b3275e0bac4871d98481ac57931e96c', 'init_expr': None, 'type': 'Separator', 'size': 5}, {'style': 0, 'activate': 1, 'name': 'find_label', 'text': u'\u041d\u0430\u0439\u0442\u0438:', 'foregroundColor': (50, 50, 50), 'backgroundColor': None, 'position': (-1, -1), 'font': {}, 'type': 'StaticText', 'size': (70, 18)}, {'activate': 1, 'ctrl': None, 'pic': 'S', 'hlp': None, 'keyDown': None, 'font': {}, 'size': (-1, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': 'TextField', 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': 'find_edit', 'changed': None, 'value': '', 'position': (-1, -1), 'refresh': []}, {'activate': 1, 'name': 'find_tool', 'toolType': 0, 'shortHelpString': u'\u041d\u0430\u0439\u0442\u0438', 'longHelpString': '', '_uuid': '5aaaafcb717173b48fa3a207d9b604a7', 'pushedBitmap': None, 'label': '', 'isToggle': 0, 'init_expr': None, 'bitmap': '@common.imgSearchData', 'type': 'ToolBarTool', 'onTool': None}], 'name': u'refbook_test_brws_toolbar', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None, 'bitmap_size': (16, 15)}, {'activate': 1, 'obj_module': None, 'show': 1, 'data_name': None, 'keyDown': None, 'border': 0, 'size': (-1, -1), 'moveAfterInTabOrder': '', 'foregroundColor': None, 'layout': u'vertical', 'alias': None, 'component_module': None, 'win1': {'activate': 1, 'obj_module': None, 'show': 1, 'child': [{'activate': 1, 'obj_module': None, 'data_name': None, 'border': 0, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'type': 'BoxSizer', 'res_module': None, 'hgap': 0, 'description': None, '_uuid': 'e8f2ebe3b82ebc8c3bb1d7d64457a288', 'flag': 8192, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'labels': [u'\u041a\u043e\u0434', u'\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435'], 'refresh': None, 'selectChanged': u'GetResModule().onObjCodeChanged(GetContext())', 'border': 0, 'size': (-1, -1), 'treeDict': {}, 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'itemCollapsed': None, 'source': None, 'itemActivated': None, 'itemExpanded': None, 'titleRoot': u'@GetResModule().onTreeRootTitle(GetContext())', 'type': 'SimpleTreeListCtrl', 'res_module': None, 'enable': True, 'description': None, '_uuid': '3a25c1fd1db7b6ffcd6a8b0d4f3d45bc', 'style': 0, 'flag': 8192, 'recount': None, 'hideHeader': False, 'backgroundColor': None, 'child': [], 'name': u'tree_object_ctrl', 'wcols': [200, 300], 'data_name': None, 'keyDown': None, 'alias': None, 'itemChecked': None, 'init_expr': None, 'position': (-1, -1), 'onInit': u'GetResModule().onTreeBrwsInit(GetContext())'}], 'layout': 'vertical', 'name': u'tree_obj_sizer', 'alias': None, 'init_expr': None, 'position': (0, 0), 'vgap': 0}], 'keyDown': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': 'Panel', 'res_module': None, 'enable': True, 'description': None, 'onClose': None, '_uuid': '162d5332c05908d1d42302ab82edfd0c', 'style': 524288, 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 8192, 'recount': None, 'name': u'tree_obj_panel', 'data_name': None, 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}, 'proportion': 1, 'sash_size': -1, 'source': None, 'backgroundColor': None, 'type': 'SplitterWindow', 'res_module': None, 'enable': True, 'description': None, '_uuid': '0b015b12be5c4b713d1dfd80e47c944e', 'style': 768, 'docstr': 'ic.components.icsplitter-module.html', 'flag': 8192, 'recount': None, 'span': (1, 1), 'name': u'splitter_win', 'min_panelsize': 20, 'refresh': None, 'win2': {'activate': 1, 'obj_module': None, 'show': 1, 'child': [{'activate': 1, 'obj_module': None, 'data_name': None, 'border': 0, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'type': 'BoxSizer', 'res_module': None, 'hgap': 0, 'description': None, '_uuid': '421609e1af3e3d2a3ba647dd2f226904', 'flag': 8192, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'buttonAdd': 1, 'buttonDel': 1, 'data_name': None, 'keyDown': None, 'border': 0, 'size': (200, -1), 'style': 2097188, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'onPrint': None, 'proportion': 0, 'source': None, 'onAdd': None, 'backgroundColor': None, 'type': 'DatasetNavigator', 'res_module': None, 'enable': True, 'description': None, 'buttonPrint': 0, '_uuid': '4955c6086f9fd7fc55ce4094643f302f', 'onHelp': None, 'moveAfterInTabOrder': '', 'onUpdate': None, 'flag': 8192, 'object_link': None, 'recount': None, 'onDelete': None, 'onInit': None, 'name': u'grid_obj_navigator', 'refresh': None, 'alias': None, 'init_expr': None, 'buttonHelp': 0, 'position': (-1, -1), 'buttonUpdate': 0}, {'line_color': (200, 200, 200), 'activate': 1, 'obj_module': None, 'enable_freq_dict': False, 'show': 1, 'data_name': None, 'cols': [{'activate': 1, 'obj_module': None, 'ctrl': u'return GetResModule().onCodeObjControl(GetContext())', 'pic': 'S', 'getvalue': '', 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u0434', 'width': 100, 'init': None, 'valid': None, 'type': 'GridCell', 'res_module': None, 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'description': None, 'shortHelpString': '', '_uuid': '572b4e8a3111d8f67daddaf29109fb4c', 'recount': None, 'hlp': None, 'name': u'code', 'setvalue': '', 'attr': 'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'obj_module': None, 'ctrl': None, 'pic': 'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', 'width': 300, 'init': None, 'valid': None, 'type': 'GridCell', 'res_module': None, 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'description': None, 'shortHelpString': '', '_uuid': '41ce53e1319b59c91418aa02081ba4ce', 'recount': None, 'getvalue': '', 'name': u'description', 'setvalue': '', 'attr': 'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'obj_module': None, 'ctrl': None, 'pic': 'S', 'getvalue': '', 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u0434 \u0432\u0435\u0440\u0445\u043d\u0435\u0433\u043e \u0443\u0440\u043e\u0432\u043d\u044f', 'width': 100, 'init': None, 'valid': None, 'type': 'GridCell', 'res_module': None, 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'description': None, 'shortHelpString': '', '_uuid': '79730d5cf9eb97e2d123fe950edaac84', 'recount': None, 'hlp': None, 'name': u'parent', 'setvalue': '', 'attr': 'W', 'keyDown': None, 'alias': None, 'init_expr': None}], 'onSize': None, 'border': 0, 'post_select': None, 'size': (-1, -1), 'moveAfterInTabOrder': '', 'dclickEditor': None, 'span': (1, 1), 'delRec': None, 'component_module': None, 'row_height': 20, 'selected': None, 'proportion': 1, 'getattr': None, 'label': 'Grid', 'source': None, 'init': None, 'backgroundColor': None, 'fixRowSize': 0, 'type': 'GridDataset', 'post_init': None, 'res_module': None, 'enable': True, 'fixColSize': 0, 'description': None, 'post_del': None, 'selection_mode': 'cells', '_uuid': '1f6dec0273b21b43d2d7104cb919ab1d', 'style': 0, 'docstr': 'ic.components.icgrid.html', 'flag': 8192, 'foregroundColor': None, 'recount': None, 'label_attr': {'foregroundColor': (0, 0, 0), 'name': '', '_uuid': None, 'backgroundColor': None, 'font': {'style': None, 'name': 'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'label_attr', 'alignment': ('left', 'middle')}, 'name': u'grid_obj', 'label_height': 20, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None, 'refresh': None}], 'layout': 'vertical', 'name': u'grid_obj_sizer', 'alias': None, 'init_expr': None, 'position': (0, 0), 'vgap': 0}], 'keyDown': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': 'Panel', 'res_module': None, 'enable': True, 'description': None, 'onClose': None, '_uuid': '161952b9e5c8215cebddeee16702239f', 'style': 524288, 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 8192, 'recount': None, 'name': u'grid_obj_panel', 'data_name': None, 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}, 'init_expr': None, 'position': (-1, -1), 'sash_pos': 300, 'onInit': None}, {'activate': 1, 'obj_module': None, 'border': 5, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'type': 'BoxSizer', 'res_module': None, 'hgap': 0, 'description': None, '_uuid': '20741934a55de2a91bbc85b77a95cea7', 'flag': 2560, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'attach_focus': False, 'mouseClick': u'GetResModule().onCancelButtonMouseClick(GetContext())', 'font': {}, 'border': 5, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041e\u0442\u043c\u0435\u043d\u0430', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': 'Button', 'res_module': None, 'description': None, '_uuid': 'd2e4aac38ca2e0b3e0838a40d1b67e68', 'userAttr': None, 'moveAfterInTabOrder': '', 'flag': 240, 'recount': None, 'name': 'cancel_button', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'obj_module': None, 'show': 1, 'attach_focus': False, 'mouseClick': u'GetResModule().onOkButtonMouseClick(GetContext())', 'font': {}, 'border': 5, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'OK', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': 'Button', 'res_module': None, 'description': None, '_uuid': '28e409a8dfa32c5f4217bc70a4d9aa94', 'userAttr': None, 'moveAfterInTabOrder': '', 'flag': 240, 'recount': None, 'name': 'ok_button', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None, 'refresh': None, 'mouseContextDown': None}], 'layout': 'horizontal', 'name': u'refbook_test_brws_sizer_btn', 'alias': None, 'init_expr': None, 'position': (0, 0), 'vgap': 0}], 'layout': 'vertical', 'name': u'refbook_test_brws_sizer_v', 'alias': None, 'init_expr': None, 'position': (0, 0), 'vgap': 0}], 'icon': None, 'setFocus': None, 'name': u'std_refbook_brws_dlg', 'data_name': None, 'keyDown': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}}