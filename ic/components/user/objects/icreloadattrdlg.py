#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.dlg.msgbox as msgbox

### !!!!  !!!!
###BEGIN SPECIAL BLOCK
#
resource = {'activate': u'1', 'show': u'1', 'recount': u'None', 'refresh': u'None', 'border': 0, 'size': (300, 300), 'style': 536877056, 'foregroundColor': None, 'span': (1, 1), 'title': u'\u0423\u043a\u0430\u0436\u0438 \u043f\u0435\u0440\u0435\u043e\u043f\u0440\u0435\u0434\u0435\u043b\u044f\u0435\u043c\u044b\u0439 \u0430\u0442\u0440\u0438\u0431\u0443\u0442', 'proportion': 0, 'source': u'None', 'backgroundColor': None, 'type': u'Dialog', 'onClose': u'None', '_uuid': u'036d443ffbb0e58406110da0fa77aa5d', 'moveAfterInTabOrder': u'', 'killFocus': u'None', 'flag': 0, 'child': [{'hgap': 0, 'style': 0, 'activate': u'1', 'span': (1, 1), 'name': u'DefaultName_1156', 'flexRows': [], 'minCellWidth': 10, 'flexCols': [], 'border': 0, '_uuid': u'434a3481cbb5339e46c8d13e593c53bb', 'proportion': 0, 'alias': u'None', 'flag': 0, 'minCellHeight': 10, 'init_expr': u'None', 'child': [{'activate': u'1', 'show': u'1', 'text': u'\u0422\u0438\u043f \u043a\u043e\u043c\u043f\u043e\u043d\u0435\u043d\u0442\u0430', 'keyDown': None, 'font': {'style': 'bold', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Arial', 'type': 'Font', 'underline': False, 'size': 8}, 'border': 0, 'size': wx.Size(103, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': u'None', 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'4e90001934e515b6f221fd67a7fa2a5b', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': u'None', 'name': u'default_1163', 'refresh': u'None', 'alias': u'None', 'init_expr': u'None', 'position': (1, 1)}, {'activate': u'1', 'show': u'1', 'keyDown': u'None', 'border': 0, 'size': wx.Size(130, 21), 'style': 33555520, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'proportion': 0, 'source': u'None', 'backgroundColor': (255, 255, 255), 'type': u'Choice', 'loseFocus': u'None', '_uuid': u'9f2d83c0a99c6d231b9e415e59614bca', 'moveAfterInTabOrder': u'', 'choice': u'WrapperObj.OnSelectType(evt)', 'flag': 8192, 'recount': u'[]', 'field_name': u'None', 'setFocus': u'None', 'name': u'typeChoice', 'items': u'None', 'refresh': u'[]', 'alias': u'None', 'init_expr': u'None', 'position': (1, 2)}, {'activate': u'1', 'show': u'1', 'text': u'\u0418\u043c\u044f \u043a\u043e\u043c\u043f\u043e\u043d\u0435\u043d\u0442\u0430', 'keyDown': None, 'font': {'style': 'bold', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Arial', 'type': 'Font', 'underline': False, 'size': 8}, 'border': 0, 'size': wx.Size(104, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': u'None', 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'3b9e601984d4872726425ed8cc3ec47b', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': u'None', 'name': u'default_1176', 'refresh': u'None', 'alias': u'None', 'init_expr': u'None', 'position': (3, 1)}, {'activate': u'1', 'ctrl': None, 'pic': u'S', 'hlp': None, 'keyDown': None, 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'border': 0, 'size': wx.Size(130, 20), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', '_uuid': u'03219ec2e23ca30eb78388b7cfdb5b48', 'moveAfterInTabOrder': u'', 'flag': 8192, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'nameText', 'changed': None, 'value': u'', 'alias': u'None', 'init_expr': u'None', 'position': (3, 2), 'refresh': []}, {'activate': u'1', 'show': 1, 'text': u'\u0418\u043c\u044f \u0430\u0442\u0440\u0438\u0431\u0443\u0442\u0430', 'keyDown': None, 'font': {'style': 'bold', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Arial', 'type': 'Font', 'underline': False, 'size': 8}, 'border': 0, 'size': wx.Size(109, 19), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': u'None', 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'aee9ed601be3065f0adda3241294efc4', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_1444', 'refresh': None, 'alias': u'None', 'init_expr': u'None', 'position': (5, 1)}, {'activate': u'1', 'show': 1, 'refresh': [], 'border': 0, 'size': (-1, -1), 'style': 33555520, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': (255, 255, 255), 'type': u'Choice', 'loseFocus': None, '_uuid': u'642514555e3f7c409177f03ed943f5c1', 'moveAfterInTabOrder': u'', 'choice': None, 'flag': 8192, 'recount': [], 'field_name': None, 'setFocus': None, 'name': u'attrChoice', 'items': None, 'keyDown': None, 'alias': u'None', 'init_expr': u'None', 'position': (5, 2)}, {'activate': u'1', 'show': u'1', 'borderRightColor': None, 'child': [], 'refresh': u'None', 'borderTopColor': (2, 78, 162), 'font': {'style': 'boldItalic', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Arial', 'type': 'Font', 'underline': False, 'size': 8}, 'border': 0, 'alignment': u"('centred', 'middle')", 'size': (280, 73), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 3), 'proportion': 0, 'label': u"!!! \u041f\u0435\u0440\u0435\u043e\u043f\u0440\u0435\u0434\u0435\u043b\u043d\u0438\u0435 \u0430\u0442\u0440\u0438\u0431\u0443\u0442\u0430 \u043f\u0440\u043e\u0438\u0441\u0445\u043e\u0434\u0438\u0442 \r\n\u0432 \u043c\u043e\u043c\u0435\u043d\u0442 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f \u043a\u043e\u043c\u043f\u043e\u043d\u0435\u043d\u0442\u0430. \u0410\u0442\u0440\u0438\u0431\u0443\u0442,\r\n\u043d\u0430\u0447\u0438\u043d\u0430\u044e\u0449\u0438\u0439\u0441\u044f \u0441 '@' \u0441\u0447\u0438\u0442\u0430\u0435\u0442\u0441\u044f \u0432\u044b\u0447\u0438\u0441\u043b\u044f\u0435\u043c\u044b\u043c,\r\n\u0432\u044b\u0447\u0438\u0441\u043b\u0435\u043d\u043d\u043e\u0435 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435 \u0431\u0443\u0434\u0435\u0442 \u0437\u0430\u043d\u0435\u0441\u0435\u043d\u043e \u0432 \r\n\u043f\u0435\u0440\u0435\u043e\u043f\u0440\u0435\u0434\u0435\u043b\u044f\u0435\u043c\u044b\u0439 \u0430\u0442\u0440\u0438\u0431\u0443\u0442. ", 'source': u'None', 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'borderWidth': 1, 'shortHelpString': u'', '_uuid': u'8e0d65b7eee7a27e31e9f1b88749f0a7', 'style': 0, 'flag': 0, 'recount': u'None', 'cursorColor': (100, 100, 100), 'borderStyle': u'None', 'borderStep': 0, 'borderLeftColor': None, 'name': u'HeadCell_1477', 'borderBottomColor': (2, 78, 162), 'keyDown': u'None', 'alias': u'None', 'init_expr': u'None', 'position': (7, 1), 'backgroundType': 0}, {'activate': u'1', 'show': 1, 'text': u'\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435', 'refresh': None, 'font': {'style': 'bold', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Arial', 'type': 'Font', 'underline': False, 'size': 8}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': u'None', 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'9bfcc6c1b6a968a8f8e6ffa1db4866e6', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_1031', 'keyDown': None, 'alias': u'None', 'init_expr': u'None', 'position': (9, 1)}, {'activate': u'1', 'ctrl': None, 'pic': u'S', 'hlp': None, 'value': u'', 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'border': 0, 'size': wx.Size(140, 20), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'show': u'1', 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', '_uuid': u'd758bdd52e2c46a6707136e4889f46ef', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': u'[]', 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'valText', 'changed': None, 'keyDown': None, 'alias': u'None', 'init_expr': u'None', 'position': (9, 2), 'refresh': u'[]'}, {'activate': u'1', 'show': 1, 'mouseClick': None, 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'border': 0, 'size': wx.Size(28, 20), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'label': u'...', 'source': u'None', 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'e8324b6dd50f25c525e70f42ff8a0075', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'editorBtn', 'mouseUp': None, 'keyDown': None, 'alias': u'None', 'init_expr': u'None', 'position': (9, 3), 'refresh': None, 'mouseContextDown': None}, {'hgap': u'0', 'style': 0, 'activate': u'1', 'layout': u'horizontal', 'name': u'DefaultName_1282', 'border': 0, 'span': (1, 3), '_uuid': u'15a13423ccd0ce6cb51833c8ef088f40', 'proportion': 0, 'alias': u'None', 'flag': 0, 'init_expr': u'None', 'child': [{'style': 0, 'activate': u'1', 'span': (1, 1), 'name': u'DefaultName_1460_1611', 'border': 0, '_uuid': u'03285e792d2dab0ba608e3c5d6eb3bcb', 'proportion': 0, 'alias': u'None', 'flag': 0, 'init_expr': u'None', 'position': wx.Point(10, 214), 'type': u'SizerSpace', 'size': (56, 12)}, {'activate': u'1', 'show': u'1', 'mouseClick': u'WrapperObj.OnOK(evt)', 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'label': u'OK', 'source': u'None', 'mouseDown': u'None', 'backgroundColor': None, 'type': u'Button', '_uuid': u'70e00fd23cce6f2aef4783abab797584', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': u'None', 'name': u'btnOk', 'mouseUp': u'None', 'keyDown': u'None', 'alias': u'None', 'init_expr': u'None', 'position': (13, 219), 'refresh': u'None', 'mouseContextDown': u'None'}, {'activate': u'1', 'show': 1, 'mouseClick': u'WrapperObj.OnCancel(evt)', 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'label': u'Cancel', 'source': u'None', 'mouseDown': u'None', 'backgroundColor': None, 'type': u'Button', '_uuid': u'34945c3f9aa0d57521ab1aec6e041fb5', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'btnCancel', 'mouseUp': u'None', 'keyDown': u'None', 'alias': u'None', 'init_expr': u'None', 'position': wx.Point(107, 226), 'refresh': None, 'mouseContextDown': u'None'}], 'position': (12, 1), 'type': u'BoxSizer', 'vgap': u'0', 'size': (-1, -1)}, {'activate': u'1', 'show': u'1', 'borderRightColor': None, 'child': [], 'refresh': u'None', 'borderTopColor': None, 'font': {}, 'border': 0, 'alignment': u"('centred', 'middle')", 'size': (280, 11), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 3), 'proportion': 0, 'label': u'', 'source': u'None', 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'borderWidth': 1, 'shortHelpString': u'', '_uuid': u'f42d438bc188a58832d04024bbdfeb5f', 'style': 0, 'flag': 0, 'recount': u'None', 'cursorColor': (100, 100, 100), 'borderStyle': u'None', 'borderStep': 0, 'borderLeftColor': None, 'name': u'HeadCell_1764', 'borderBottomColor': (2, 78, 162), 'keyDown': None, 'alias': u'None', 'init_expr': u'None', 'position': (10, 1), 'backgroundType': 0}], 'position': wx.Point(102, 35), 'type': u'GridBagSizer', 'vgap': 0, 'size': (-1, -1)}], 'setFocus': u'None', 'name': u'Dialog_1143', 'keyDown': u'None', 'alias': u'None', 'init_expr': u'None', 'position': (-1, -1)}

__version__ = (1, 0, 1, 2)

###END SPECIAL BLOCK


ic_class_name = 'ReloadAttrDlg'


class ReloadAttrDlg:

    def __init__(self, parent, typeInfo=None):
        """
        """
        self._info = typeInfo
        self.evalSpace = util.InitEvalSpace()
        self.evalSpace['WrapperObj'] = self
        self.__obj = prs.icBuildObject(parent, resource, evalSpace=self.evalSpace, bIndicator=False)
        self.object = self.evalSpace['_root_obj']
        self.typeList = None

        if typeInfo:
            choice = self.evalSpace['_dict_obj']['typeChoice']
            choice.Clear()
            typeList = typeInfo.keys()
            typeList.sort()
            self.typeList = typeList

            for item in typeList:
                choice.Append(str(item))

    def getObject(self):
        """
        """
        return self.object

    def getTypeInfo(self):
        """
        """
        return self._info

    def OnOK(self, evt):
        """
        """
        dlg = self.getObject()

        if dlg:
            typeObj = self.evalSpace['_dict_obj']['typeChoice'].GetStringSelection()
            if not typeObj:
                msgbox.MsgBox(self.getObject(), u'-')

            name = self.evalSpace['_dict_obj']['nameText'].GetValue()
            if typeObj and not name:
                msgbox.MsgBox(self.getObject(), u'-')

            attr = self.evalSpace['_dict_obj']['attrChoice'].GetStringSelection()
            if typeObj and name and not attr:
                msgbox.MsgBox(self.getObject(), u'-')

            if typeObj and name and attr:
                dlg.EndModal(wx.ID_OK)
        evt.Skip()

    def OnCancel(self, evt):
        """
        """
        dlg = self.getObject()

        if dlg:
            dlg.EndModal(wx.ID_CANCEL)

        evt.Skip()

    def OnSelectType(self, evt):
        """
        """
        if not self.typeList:
            return

        indx = evt.GetSelection()
        objType = self.typeList[indx]
        choice = self.evalSpace['_dict_obj']['attrChoice']
        choice.Clear()
        spc = self.getTypeInfo()[objType][3]
        spc = util.icSpcDefStruct(spc, spc, True)
        lst = spc.keys()
        lst.sort()

        for attr in lst:
            if not attr.startswith('_') and attr not in ['name', 'type']:
                choice.Append(str(attr))
        

def test(par=0):
    """
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)

    cls = ReloadAttrDlg(win, {'dataset': '1', 'button': '2'})
    dlg = cls.getObject()
    dlg.ShowModal()
    dlg.Destroy()

    frame.Show(True)
    app.MainLoop()
    

if __name__ == '__main__':
    test()
