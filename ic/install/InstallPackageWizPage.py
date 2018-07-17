#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'onClose': None, '_uuid': u'ec873f1347ce847ff93ea3562d8efbca', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'hgap': 2, 'style': 0, 'activate': 1, 'span': (1, 1), 'name': u'DefaultName_1588_1449', 'flexRows': [], 'minCellWidth': 5, 'border': 0, '_uuid': u'483609b4008e96b22285ecbbe2e80215', 'proportion': 0, 'flexCols': [], 'alias': None, 'flag': 0, 'minCellHeight': 5, 'init_expr': u"_dict_obj['AttrGrid'].ReconstructHeader()", 'child': [{'activate': 1, 'show': 1, 'borderRightColor': None, 'child': [], 'refresh': None, 'borderTopColor': None, 'font': {'style': 'boldItalic', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Arial', 'type': 'Font', 'underline': False, 'size': 12}, 'border': 2, 'alignment': u"('left', 'middle')", 'size': (450, 30), 'style': 0, 'foregroundColor': (0, 98, 196), 'span': (1, 3), 'proportion': 0, 'label': u'\u041d\u0435\u043e\u0431\u0445\u043e\u0434\u0438\u043c\u044b\u0435 \u043f\u0430\u043a\u0435\u0442\u044b', 'source': u'None', 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'borderWidth': 1, 'shortHelpString': u'', '_uuid': u'fececf250274bf2bcb44d00af2f2910c', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'cursorColor': (100, 100, 100), 'borderStyle': None, 'borderStep': 0, 'borderLeftColor': None, 'name': u'HeadCell_Title', 'borderBottomColor': (0, 98, 196), 'keyDown': u'None', 'alias': u'None', 'init_expr': u'None', 'position': (0, 1), 'backgroundType': 0}, {'activate': 1, 'show': 1, 'borderRightColor': None, 'recount': None, 'keyDown': u'None', 'borderTopColor': None, 'font': {'style': 'bold', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Arial', 'type': 'Font', 'underline': False, 'size': 8}, 'border': 0, 'alignment': u"('left', 'middle')", 'size': (450, 40), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 3), 'proportion': 0, 'label': u'\u041d\u0430 \u0434\u0430\u043d\u043d\u043e\u0439 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0435 \u043e\u043f\u0440\u0435\u0434\u0435\u043b\u044f\u044e\u0442\u0441\u044f \u043e\u0441\u043d\u043e\u0432\u043d\u044b\u0435 \u043f\u0430\u043a\u0435\u0442\u044b, \\n\u043a\u043e\u0442\u043e\u0440\u044b\u0435 \u043d\u0435\u043e\u0431\u0445\u043e\u0434\u0438\u043c\u044b \u0434\u043b\u044f  \u0440\u0430\u0431\u043e\u0442\u044b \u0441\u0438\u0441\u0442\u0435\u043c\u044b.', 'source': u'None', 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'borderWidth': 1, 'shortHelpString': u'', '_uuid': u'03a005f2a6752cf90ca72cfff1d87b4e', 'moveAfterInTabOrder': u'', 'flag': 0, 'child': [], 'cursorColor': (100, 100, 100), 'borderStyle': None, 'borderStep': 0, 'borderLeftColor': None, 'name': u'HeadCell_Discr', 'borderBottomColor': (0, 98, 196), 'refresh': None, 'alias': u'None', 'init_expr': u'None', 'position': (2, 1), 'backgroundType': 0}, {'activate': 1, 'show': 1, 'text': u'(*) \u043e\u0442\u043c\u0435\u0447\u0435\u043d\u044b \u043f\u043e\u043b\u044f, \u043a\u043e\u0442\u043e\u0440\u044b\u0435 \u043e\u0431\u044f\u0437\u0430\u0442\u0435\u043b\u044c\u043d\u043e \u043d\u0435\u043e\u0431\u0445\u043e\u0434\u0438\u043c\u043e \u0437\u0430\u043f\u043e\u043b\u043d\u0438\u0442\u044c ', 'refresh': None, 'font': {'style': 'bold', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Arial', 'type': 'Font', 'underline': False, 'size': 8}, 'border': 0, 'size': (-1, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 3), 'proportion': 0, 'source': u'None', 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'fb2df569844a2c561d09b176e6bf0894', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_15381', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (13, 1)}, {'style': 0, 'activate': u'1', 'span': (1, 1), 'name': u'DefaultName_23201', 'border': 0, '_uuid': u'b5463ddc88723b47130a88adf3b1fa47', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': (12, 1), 'type': u'SizerSpace', 'size': wx.Size(15, 89)}, {'activate': 1, 'show': 1, 'activated': None, 'refresh': None, 'font': {}, 'border': 0, 'size': (300, 250), 'style': 3, 'foregroundColor': (0, 0, 0), 'span': (2, 2), 'component_module': None, 'selected': None, 'proportion': 0, 'source': None, 'backgroundColor': (255, 255, 255), 'type': u'MultiColumnList', 'col_width': [295], '_uuid': u'01fb91f7e5888a8783064f18e6f992a1', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'packageList', 'fields': u'[]', 'keyDown': None, 'alias': None, 'init_expr': None, 'items': [u'\u041f\u0430\u043a\u0435\u0442\u044b'], 'position': (5, 1), 'onInit': None}, {'activate': 1, 'show': 1, 'mouseClick': u"import ic.dlg.ic_dlg as ic_dlg\nfile_name=ic_dlg.icFileDlg(_dict_obj['addButton'].GetParent(),\n    '\u041d\u0435\u043e\u0431\u0445\u043e\u0434\u0438\u043c\u044b\u0435 \u043f\u0430\u043a\u0435\u0442\u044b',\n    'EXE Files(*.exe)|*.exe|Microsoft Install Files(*.msi)|*.msi|DLL Files(*.dll)|*.dll')\nif file_name:\r\n    packages=_dict_obj['packageList'].getStringsByCol(0)\r\n    if not(file_name in packages):\n        _dict_obj['packageList'].appendStringRec(file_name)\r\n", 'font': {'style': 'bold', 'size': 12, 'underline': False, 'faceName': 'MS Sans Serif', 'family': 'sansSerif'}, 'border': 0, 'size': (24, 24), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'+', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'2ee3e8b6dd9611ab6389fb1291e6557f', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'addButton', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (4, 1), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'show': 1, 'mouseClick': u"_dict_obj['packageList'].DeleteItem(_dict_obj['packageList'].currentItem)", 'font': {'style': 'bold', 'size': 12, 'underline': False, 'faceName': 'MS Sans Serif', 'family': 'sansSerif'}, 'border': 0, 'size': (24, 24), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'-', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'1bab6cd21bf032f1f073698f7be877dd', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'delButton', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (4, 2), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'show': 1, 'mouseClick': u"_dict_obj['packageList'].moveStringRec(-1,-1)", 'font': {'family': 'sansSerif', 'style': 'bold', 'underline': False, 'faceName': 'MS Sans Serif', 'size': 12}, 'border': 0, 'size': (24, 24), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'<', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'90702a8ad7669f17332ef9e5451d42b7', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'upButton', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (5, 3), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'show': 1, 'mouseClick': u"_dict_obj['packageList'].moveStringRec(-1,1)\r\n", 'font': {'style': 'bold', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'MS Sans Serif', 'type': 'Font', 'underline': False, 'size': 12}, 'border': 0, 'size': (24, 24), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'>', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'66f175fb77087ce6cff0d44e9944918e', 'moveAfterInTabOrder': u'', 'flag': 1024, 'recount': None, 'name': u'downButton', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (6, 3), 'onInit': None, 'refresh': None, 'mouseContextDown': None}], 'position': wx.Point(158, 63), 'type': u'GridBagSizer', 'vgap': 2, 'size': (-1, -1)}], 'name': u'pagePanel', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(0, 0), 'onInit': None}

#   Версия объекта
__version__ = (1, 0, 2, 0)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'icInstallPackageWizPage'

class icInstallPackageWizPage:
    def __init__(self, parent):
        self.evalSpace = util.InitEvalSpace()
        res = resource['child'][0]
        self.__obj = prs.icBuildObject(parent, res, evalSpace=self.evalSpace, bIndicator=False)
        self.object = self.evalSpace['_root_obj']
        
    def getObject(self):
        """
        """
        return self.object
        
def test(par=0):
    """
    Тестируем класс icInstallPackageWizPage.
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
