{'FrmHlpStructSpravFloat': {'activate': u'1', 'prim': u'\u0414\u0430\u043d\u043d\u0430\u044f \u0444\u043e\u0440\u043c\u0430 \u0443\u043d\u0430\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u043d\u0430 \u043e\u0442 FrmHlpStructSprav\r\n\u0441 \u043f\u0435\u0440\u0435\u043e\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u0438\u0435\u043c \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f \u043f\u043e \u043a\u043d\u043e\u043f\u043a\u0435 \u0432\u044b\u0431\u043e\u0440\u0430\r\n\u0441 \u0443\u0447\u0435\u0442\u043e\u043c \u0442\u043e\u0433\u043e, \u0441\u043e\u0434\u0435\u0440\u0436\u0438\u0442 \u043b\u0438 \u0442\u0435\u043a\u0443\u0449\u0438\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442 \u0434\u0430\u043d\u043d\u044b\u0435 \u043d\u0430 \r\n\u0441\u043b\u0435\u0434\u0443\u044e\u0449\u0435\u043c \u0443\u0440\u043e\u0432\u043d\u0435', 'name': u'FrmHlpStructSpravFloat', '_uuid': u'7e40193dff0f0eb7141179842e2d9a47', 'init_expr': None, 'child': [{'style': 0, 'activate': u'1', 'span': (1, 1), 'name': u'imp_580_1067', 'proportion': 0, '_uuid': u'7e40193dff0f0eb7141179842e2d9a47', 'modules': {}, 'object': None, 'alias': None, 'flag': 0, 'init_expr': u"_dict_obj['ListDS'].SetCursor(0)\r\n#_dict_obj['ListDS'].Focus(0)", 'type': u'Import', 'position': (-1, -1), 'border': 0, 'size': (-1, -1)}, {'activate': u'1', 'name': u'Link_FrmHlpStructSprav', '_uuid': u'017fecdc0a81a457225aee3a224410e3', 'docstr': u'ic.db.icdataset-module.html', 'filter': u'None', 'ListDataset:ListDS.activated': u"#\u041f\u0435\u0440\u0435\u043e\u043f\u0440\u0435\u0434\u0435\u043b\u0438\u0442\u044c \u0441\u043e\u0431\u044b\u0442\u0438\u0435\r\ncur_row=row\r\n#\u0417\u0430\u043f\u043e\u043c\u043d\u0438\u0442\u044c \u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u0435 \u043a\u0443\u0440\u0441\u043e\u0440\u0430\r\n#cur_row=_dict_obj['ListDS'].currentItem\r\ncod_struct=get_hlp_code(sprav_type,sprav_code,NsiStd.rec.cod)\r\nprint '%%%%%%%%cod_struct:',cod_struct\r\n#\u043f\u0440\u043e\u0432\u0435\u0440\u0438\u0442\u044c \u0435\u0441\u0442\u044c \u043b\u0438 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f \u043d\u0430 \u0441\u043b\u0435\u0434\u0443\u044e\u0449\u0435\u043c \u0443\u0440\u043e\u0432\u043d\u0435\r\ncs=''\r\nfor s in cod_struct:\r\n\tcs=cs+s\r\nprint 'c%%%%%%%%%%s:',cs\r\nrs=_NsiStd.select(AND(_NsiStd.q.type==sprav_type,_NsiStd.q.cod.startswith(cs)))\r\nfor i in range(getRecordCount(rs)):\r\n\tprint '%%%%%%%%% rs:',rs[i]\r\nif getRecordCount(rs) > 1:\r\n\tprint '%%%%%%%%This is a group'\r\n\tcod_struct=list(cod_struct)\r\n\tcod_struct.append(None)\r\n\tcod_struct=tuple(cod_struct)\r\n\tresult=HlpSprav(sprav_type,ParentCode=cod_struct,field=sprav_field,rec=NsiStd.rec,parentForm=self)\r\n\tif result:\r\n\t\t_esp['_dict_obj']['DlgHlpSprav'].EndModal(wx.ID_OK)\r\n\telse:\r\n\t\t_dict_obj['ListDS'].SetCursor(cur_row)\r\nelse:\r\n\tprint '%%%%%%%%This is an item'\r\n\tresult=HlpSprav(sprav_type,ParentCode=cod_struct,field=sprav_field,rec=NsiStd.rec,parentForm=self)\r\n\tif result:\r\n\t\t_esp['_dict_obj']['DlgHlpSprav'].EndModal(wx.ID_OK)\r\n\telse:\r\n\t\t_dict_obj['ListDS'].SetCursor(cur_row)\r\n\r\n", 'init_expr': None, 'file': u'NSI/resource.frm', 'res_query': u'FrmHlpStructSprav', 'Button:btn_choose.mouseClick': u"#\u041f\u0435\u0440\u0435\u043e\u043f\u0440\u0435\u0434\u0435\u043b\u0438\u0442\u044c \u0441\u043e\u0431\u044b\u0442\u0438\u0435\r\n#\u0417\u0430\u043f\u043e\u043c\u043d\u0438\u0442\u044c \u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u0435 \u043a\u0443\u0440\u0441\u043e\u0440\u0430\r\ncur_row=_dict_obj['ListDS'].currentItem\r\ncod_struct=get_hlp_code(sprav_type,sprav_code,NsiStd.rec.cod)\r\nprint '%%%%%%%%cod_struct:',cod_struct\r\n#\u043f\u0440\u043e\u0432\u0435\u0440\u0438\u0442\u044c \u0435\u0441\u0442\u044c \u043b\u0438 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f \u043d\u0430 \u0441\u043b\u0435\u0434\u0443\u044e\u0449\u0435\u043c \u0443\u0440\u043e\u0432\u043d\u0435\r\ncs=''\r\nfor s in cod_struct:\r\n\tcs=cs+s\r\nprint 'c%%%%%%%%%%s:',cs\r\nrs=_NsiStd.select(AND(_NsiStd.q.type==sprav_type,_NsiStd.q.cod.startswith(cs)))\r\nfor i in range(getRecordCount(rs)):\r\n\tprint '%%%%%%%%% rs:',rs[i]\r\nif getRecordCount(rs) > 1:\r\n\tprint '%%%%%%%%This is a group'\r\n\tcod_struct=list(cod_struct)\r\n\tcod_struct.append(None)\r\n\tcod_struct=tuple(cod_struct)\r\n\tresult=HlpSprav(sprav_type,ParentCode=cod_struct,field=sprav_field,rec=NsiStd.rec,parentForm=self)\r\n\tif result:\r\n\t\t_esp['_dict_obj']['DlgHlpSprav'].EndModal(wx.ID_OK)\r\n\telse:\r\n\t\t_dict_obj['ListDS'].SetCursor(cur_row)\r\nelse:\r\n\tprint '%%%%%%%%This is an item'\r\n\tresult=HlpSprav(sprav_type,ParentCode=cod_struct,field=sprav_field,rec=NsiStd.rec,parentForm=self)\r\n\tif result:\r\n\t\t_esp['_dict_obj']['DlgHlpSprav'].EndModal(wx.ID_OK)\r\n\telse:\r\n\t\t_dict_obj['ListDS'].SetCursor(cur_row)\r\n\r\n", 'type': u'DataLink', 'link_expr': None}], 'type': u'Group'}}