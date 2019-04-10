#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.interfaces.icobjectinterface as icobjectinterface
import ic.components.user.icarrowindicator as icarrowindicator
import plan.calc_plan as calc_plan
### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'onClose': None, '_uuid': u'1d7a8a88c8f420230d24b1175baa93a4', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'style': 0, 'activate': 1, 'prim': u'', 'name': u'Data', 'component_module': None, '_uuid': u'6ab610a7aa1e4950a272b3bf36a96c39', 'alias': None, 'init_expr': None, 'child': [], 'type': u'Group'}, {'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'name': u'DefaultName_1297', 'position': (0, 0), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'2f5c953a576c24f903676c9d7c9cd4e5', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'borderRightColor': (100, 100, 100), 'recount': None, 'keyDown': None, 'borderTopColor': (250, 250, 250), 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (50, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u0417\u0430\u044f\u0432\u043a\u0438', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'init_expr': None, 'shortHelpString': u'', '_uuid': u'67f906dbf831d419fbd41cbde01eeddb', 'style': 0, 'flag': 8192, 'child': [], 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'zayavkiLabel', 'borderBottomColor': (100, 100, 100), 'refresh': None, 'alias': None, 'borderWidth': 1, 'position': wx.Point(0, 0), 'borderStyle': None, 'onInit': None}, {'line_color': (200, 200, 200), 'activate': 1, 'show': 1, 'cols': [{'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u0414\u0430\u0442\u0430', 'width': 98, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'cf95b61e0d99a23d9b0c06fe7f59f11b', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'date', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e (\u043a\u0433.)', 'width': 138, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'a7bb6865af90b124337d04bafa63cff2', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'kol', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'999,999,999,999.99', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u0421\u0443\u043c\u043c\u0430 (\u0440\u0443\u0431.)', 'width': 164, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'dba09c07f7524757cf30ab5717eb3442', 'recount': None, 'hlp': None, 'attr': u'W', 'setvalue': u'', 'name': u'summa', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u041f\u043b\u0430\u043d\u043e\u0432\u043e\u0435 \u043a\u043e\u043b. (\u043a\u0433.)', 'width': 124, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'4aedb6d487b6d0767c916e4d848a2292', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'kol_plan', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'999,999,999,999.99', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u041f\u043b\u0430\u043d (\u0440\u0443\u0431.)', 'width': 161, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'4aedb6d487b6d0767c916e4d848a2292', 'recount': None, 'hlp': None, 'name': u'plan', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}], 'onSize': None, 'border': 0, 'post_select': None, 'size': (-1, -1), 'moveAfterInTabOrder': u'', 'dclickEditor': None, 'span': (1, 1), 'delRec': None, 'alias': None, 'component_module': None, 'selected': None, 'proportion': 1, 'getattr': u'WrapperObj.getattrFunczayavki(self.GetView(), row, col, evt)', 'label': u'Grid', 'source': None, 'init': None, 'backgroundColor': None, 'fixRowSize': 0, 'type': u'GridDataset', '_uuid': u'7165e1c4f6b0d8ea6079e7e8f2927555', 'fixColSize': 0, 'post_del': None, 'post_init': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'style': 0, 'docstr': u'ic.components.icgrid.html', 'flag': 8192, 'foregroundColor': None, 'recount': None, 'label_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': None, 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'label_attr', 'alignment': (u'left', u'middle')}, 'name': u'zayavki', 'label_height': 20, 'changed': None, 'keyDown': None, 'row_height': 20, 'init_expr': None, 'position': wx.Point(103, 58), 'onInit': None, 'refresh': None}, {'activate': 1, 'show': 1, 'borderRightColor': (100, 100, 100), 'recount': None, 'refresh': None, 'borderTopColor': (250, 250, 250), 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (50, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u0418\u0441\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435 \u0437\u0430\u044f\u0432\u043e\u043a', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'init_expr': None, 'shortHelpString': u'', '_uuid': u'd265a2d6791a96704589652bb3e246de', 'style': 0, 'flag': 8192, 'child': [], 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'ispZayavkiLabel', 'borderBottomColor': (100, 100, 100), 'keyDown': None, 'alias': None, 'borderWidth': 1, 'position': wx.Point(0, 146), 'borderStyle': None, 'onInit': None}, {'line_color': (200, 200, 200), 'activate': 1, 'show': 1, 'cols': [{'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u0414\u0430\u0442\u0430', 'width': 100, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'b5eb4c365fbdc273bc525d5279412c89', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'date', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e (\u043a\u0433.)', 'width': 108, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'7d758682d798903d0865def01eae037e', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'kol', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'999,999,999,999.99', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u0421\u0443\u043c\u043c\u0430 (\u0440\u0443\u0431.)', 'width': 132, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'5e655846052721ba7f8e9913b568b12e', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'summa', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u0417\u0430\u044f\u0432\u043b\u0435\u043d\u043d\u043e\u0435 \u043a\u043e\u043b. (\u043a\u0433)', 'width': 50, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'4aedb6d487b6d0767c916e4d848a2292', 'recount': None, 'hlp': None, 'name': u'kol_plan', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'999,999,999,999.99', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u0417\u0430\u044f\u0432\u043b\u0435\u043d\u043d\u0430\u044f \u0441\u0443\u043c\u043c\u0430 (\u0440\u0443\u0431.)', 'width': 50, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'4aedb6d487b6d0767c916e4d848a2292', 'recount': None, 'hlp': None, 'attr': u'W', 'setvalue': u'', 'name': u'plan', 'keyDown': None, 'alias': None, 'init_expr': None}], 'onSize': None, 'border': 0, 'post_select': None, 'size': (-1, -1), 'moveAfterInTabOrder': u'', 'dclickEditor': None, 'span': (1, 1), 'delRec': None, 'alias': None, 'component_module': None, 'selected': None, 'proportion': 1, 'getattr': u'WrapperObj.getattrFuncispZayavki(self.GetView(), row, col, evt)', 'label': u'Grid', 'source': None, 'init': None, 'backgroundColor': None, 'fixRowSize': 0, 'type': u'GridDataset', '_uuid': u'2041b511c43382965280ade03a4be3e3', 'fixColSize': 0, 'post_del': None, 'post_init': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'style': 0, 'docstr': u'ic.components.icgrid.html', 'flag': 8192, 'foregroundColor': None, 'recount': None, 'label_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': None, 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'label_attr', 'alignment': (u'left', u'middle')}, 'name': u'ispZayavki', 'label_height': 20, 'changed': None, 'keyDown': None, 'row_height': 20, 'init_expr': None, 'position': wx.Point(98, 432), 'onInit': None, 'refresh': None}, {'activate': 1, 'show': 1, 'borderRightColor': (100, 100, 100), 'recount': None, 'refresh': None, 'borderTopColor': (250, 250, 250), 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (50, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u0420\u0435\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u044f', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'init_expr': None, 'shortHelpString': u'', '_uuid': u'81d87dcd118ebadd7c79744aed6545ac', 'style': 0, 'flag': 8192, 'child': [], 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': u'realizeLabel', 'borderBottomColor': (100, 100, 100), 'keyDown': None, 'alias': None, 'borderWidth': 1, 'position': wx.Point(0, 292), 'borderStyle': None, 'onInit': None}, {'line_color': (200, 200, 200), 'activate': 1, 'show': 1, 'cols': [{'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u0414\u0430\u0442\u0430', 'width': 102, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'0a85e87d8bcf787559f1e31a7cdcc4b4', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'date', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e (\u043a\u0433.)', 'width': 132, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'a2bbbfffc67a5b6e54379b9965086ef7', 'recount': None, 'hlp': None, 'attr': u'W', 'setvalue': u'', 'name': u'kol', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'999,999,999,999.99', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u0421\u0443\u043c\u043c\u0430 (\u0440\u0443\u0431.)', 'width': 167, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'955f8f1d955caa2d31c82e8997d64264', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'summa', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u041f\u043b\u0430\u043d\u043e\u0432\u043e\u0435 \u043a\u043e\u043b. (\u043a\u0433.)', 'width': 125, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'4aedb6d487b6d0767c916e4d848a2292', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'kol_plan', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'999,999,999,999.99', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u041f\u043b\u0430\u043d (\u0440\u0443\u0431.)', 'width': 161, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'4aedb6d487b6d0767c916e4d848a2292', 'recount': None, 'hlp': None, 'attr': u'W', 'setvalue': u'', 'name': u'plan', 'keyDown': None, 'alias': None, 'init_expr': None}], 'onSize': None, 'border': 0, 'post_select': None, 'size': (-1, -1), 'moveAfterInTabOrder': u'', 'dclickEditor': None, 'span': (1, 1), 'delRec': None, 'alias': None, 'component_module': None, 'selected': None, 'proportion': 1, 'getattr': u'WrapperObj.getattrFuncRealize(self.GetView(), row, col, evt)', 'label': u'Grid', 'source': None, 'init': None, 'backgroundColor': None, 'fixRowSize': 0, 'type': u'GridDataset', '_uuid': u'75353204114f94f2b6d7ff5dd8391916', 'fixColSize': 0, 'post_del': None, 'post_init': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'fb9a1ac28f6817dc82282c05d2d2e910', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'style': 0, 'docstr': u'ic.components.icgrid.html', 'flag': 8192, 'foregroundColor': None, 'recount': None, 'label_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': None, 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'label_attr', 'alignment': (u'left', u'middle')}, 'name': u'realize', 'label_height': 20, 'changed': None, 'keyDown': None, 'row_height': 20, 'init_expr': None, 'position': wx.Point(264, 430), 'onInit': None, 'refresh': None}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'name': u'browsPanel', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}

#   Версия объекта
__version__ = (1, 0, 1, 9)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'IAnaliticBrows'

class IAnaliticBrows(icobjectinterface.icObjectInterface):
    def __init__(self, parent, metaObj=None):
        """
        Конструктор интерфейса.
        
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type metaObj: C{icMetaItem}
        @param metaObj: Указатель на метаобъект классификатора мониторов.
        """
        #
        self.metaObj = metaObj
        
        #   Вызываем конструктор базового класса
        icobjectinterface.icObjectInterface.__init__(self, parent, resource)

    def GetValColor(self, value, min, max, clrReg):
        """
        Возвращает цвет зоны значения индикатора.

        @type value: C{float}
        @param value: Значение индикатора.
        @type min: C{float}
        @param min: Минимальное значение шкалы индикатора.
        @type max: C{float}
        @param max: Максимальное значение шкалы индикатора.
        @type clrReg: C{list}
        @param clrReg: Описание цветовых зон. Первый элемент списка - значение
            правой границы зоны, второй элемент описание цвета зоны. Описание
            зоны должно быть в виде кортежа (rr, gg, bb) название цвета, принятое
            в библиотеке wx.
            Пример:[('40%', 'RED'), ('50%', (255, 200, 0)),('100%', 'GREEN')]
        """
        return icarrowindicator.GetValColor(value, min, max, clrReg)
                        
    ###BEGIN EVENT BLOCK
    
    def getattrFuncispZayavki(self, grid, row, col, evt):
        """
        Функция обрабатывает событие <getattr>.
        """
        if col in (1,2):
            val = grid.dataset.data[row][col]
            
            if val in (0,'0'):
                print('getattrFuncispZayavki ZERO', row, col)
                attr = {'backgroundColor':(255,0,0), 'foregroundColor':(255,255,255)}
                return attr
            else:
                val = grid.dataset.data[row][col]
                plan = grid.dataset.data[row][col+2]
                
                if plan > 0:
                    clr = self.GetValColor(val, 0, plan*2, self.metaObj.value.color_zones)
                    #print '>>>> val=%d, row=%d, col=%d, plan*2=%d, clr=%s' % (val, row, col, plan*2, str(clr))
                    print('>>> type clr =', type(clr))
                    if clr:
                        return {'foregroundColor':clr}
    
    def getattrFunczayavki(self, grid, row, col, evt):
        """
        Функция обрабатывает событие <getattr>..
        """
        #   Определяем атрибут ячейки суммы заявок
        if self.metaObj:
            if col in (1,2):
                val = grid.dataset.data[row][col]
                plan = grid.dataset.data[row][col+2]
                
                if plan > 0:
                    clr = self.GetValColor(val, 0, plan*2, self.metaObj.value.color_zones)
                    #print '>>>> val=%d, row=%d, col=%d, plan*2=%d, clr=%s' % (val, row, col, plan*2, str(clr))
                    print('>>> type clr =', type(clr))
                    if clr:
                        return {'foregroundColor':clr}
    
    def getattrFuncRealize(self, grid, row, col, evt):
        """
        Функция обрабатывает событие <?>.
        """
        #   Определяем атрибут ячейки суммы заявок
        if self.metaObj:
            if col in (1,2):
                val = grid.dataset.data[row][col]
                plan = grid.dataset.data[row][col+2]
                
                if plan > 0:
                    clr = self.GetValColor(val, 0, plan*2, self.metaObj.value.color_zones)
                    #print '>>>> val=%d, row=%d, col=%d, plan*2=%d, clr=%s' % (val, row, col, plan*2, str(clr))
                    print('>>> type clr =', type(clr))
                    if clr:
                        return {'foregroundColor':clr}
                        
    ###END EVENT BLOCK
    def LoadData(self):
        """
        Функция обновления данных на мониторе.
        """
        if self.metaObj:
            #--- Загружаем данные по заявкам
            lst = self.metaObj.value.zayavki.keys()
            lst.sort()
            data = []
            
            for key in lst:
                summa,kol = self.metaObj.value.zayavki[key]
                
                if key == 'summa':
                    nm = 'Итоговая сумма'
                    plan_summa = self.metaObj.value.summa
                    plan_kol = self.metaObj.value.kol
                else:
                    nm = key
                    plan_summa = calc_plan.getDayPlanValue(key, self.metaObj)
                    plan_kol = calc_plan.getDayPlanKol(key, self.metaObj)
#                try:
#                    plan_kol = plan_summa/(summa/kol)
#                except:
#                    plan_kol = 0
                    
                data.append((nm, kol, summa, plan_kol, plan_summa))
            
            self.GetNameObj('zayavki').dataset.SetDataBuff(data)
            self.GetNameObj('zayavki').RefreshGrid()

            #--- Загружаем данные по исполнению заявок
            lst = list(set(self.metaObj.value.analitic.keys()) |
                       set(self.metaObj.value.zayavki.keys()))
            lst.sort()
            data = []
            
            for key in lst:
                if self.metaObj.value.analitic.has_key(key):
                    summa,kol = self.metaObj.value.analitic[key]
                else:
                    summa, kol = 0,0
                    
                if key == 'summa':
                    nm = 'Итоговая сумма'
                    plan_summa, plan_kol = self.metaObj.value.zayavki['summa']
                else:
                    nm = key
                    if self.metaObj.value.zayavki.has_key(key):
                        plan_summa, plan_kol = self.metaObj.value.zayavki[key]
                    else:
                        plan_summa = 0
                        plan_kol = 0
                
                data.append((nm, kol, summa, plan_kol, plan_summa))
            
            self.GetNameObj('ispZayavki').dataset.SetDataBuff(data)
            self.GetNameObj('ispZayavki').RefreshGrid()

            #--- Загружаем данные по реализация
            lst = self.metaObj.value.analitic.keys()
            lst.sort()
            data = []
            
            for key in lst:
                summa,kol = self.metaObj.value.analitic[key]
                if key == 'summa':
                    nm = 'Итоговая сумма'
                    plan_summa = self.metaObj.value.summa
                    plan_kol = self.metaObj.value.kol
                else:
                    nm = key
                    plan_summa = calc_plan.getDayPlanValue(key, self.metaObj)
                    plan_kol = calc_plan.getDayPlanKol(key, self.metaObj)
#                try:
#                    plan_kol = plan_summa/(summa/kol)
#                except:
#                    plan_kol = 0

                data.append((nm, kol, summa, plan_kol, plan_summa))
            
            self.GetNameObj('realize').dataset.SetDataBuff(data)
            self.GetNameObj('realize').RefreshGrid()
        
    def SaveData(self):
        """
        """
        pass
    
def test(par=0):
    """
    Тестируем класс new_form.
    """
    
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)

    ################
    # Тестовый код #
    ################
        
    frame.Show(True)
    app.MainLoop()
    
if __name__ == '__main__':
    test()