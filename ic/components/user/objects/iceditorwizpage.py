#!/usr/bin/env python
# -*- coding: utf-8 -*-


import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource = {'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (-1, -1), 'style': 524288, 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'Panel', 'onClose': None, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'hgap': 2, 'style': 0, 'activate': 1, 'span': (1, 1), 'name': u'Sizer_Editor', 'flexRows': [], 'minCellWidth': 5, 'type': u'GridBagSizer', 'border': 0, 'proportion': 0, 'alias': None, 'flag': 0, 'minCellHeight': 5, 'init_expr': u'', 'child': [{'activate': 1, 'show': 1, 'borderRightColor': None, 'recount': None, 'keyDown': u'None', 'borderTopColor': None, 'font': {'style': 'boldItalic', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Arial', 'type': 'Font', 'underline': False, 'size': 12}, 'border': 2, 'alignment': u"('left', 'middle')", 'size': (500, 30), 'style': 0, 'foregroundColor': (0, 98, 196), 'span': (1, 1), 'proportion': 0, 'label': u' \u0421\u0433\u0435\u043d\u0435\u0440\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0439 \u0442\u0435\u043a\u0441\u0442 \u043c\u043e\u0434\u0443\u043b\u044f', 'source': u'None', 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'shortHelpString': u'', 'flag': 0, 'child': [], 'borderStep': 0, 'borderLeftColor': None, 'name': u'HeadCellTitle', 'borderBottomColor': (0, 98, 196), 'refresh': None, 'alias': u'None', 'init_expr': u'None', 'position': (0, 1), 'backgroundType': 0}, {'activate': 1, 'show': 1, 'borderRightColor': None, 'child': [], 'refresh': None, 'borderTopColor': None, 'font': {'style': 'bold', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Arial', 'type': 'Font', 'underline': False, 'size': 8}, 'border': 2, 'alignment': u"('left', 'middle')", 'size': wx.Size(392, 105), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'proportion': 0, 'label': u'\u041d\u0430 \u0434\u0430\u043d\u043d\u043e\u0439 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0435 \u0432\u0430\u043c \u043d\u0435\u043e\u0431\u0445\u043e\u0434\u0438\u043c\u043e \u043f\u043e\u043f\u0440\u0430\u0432\u0438\u0442\u044c \u0441\u0433\u0435\u043d\u0435\u0440\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0439\r\n\u0442\u0435\u0441\u043a\u0441 \u043c\u043e\u0434\u0443\u043b\u044f:\r\n     - \u0434\u043e\u043f\u0438\u0441\u0430\u0442\u044c \u043d\u0435\u043e\u0431\u0445\u043e\u0434\u0438\u043c\u044b\u0435 \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b \u043f\u0440\u0438 \u0432\u044b\u0437\u043e\u0432\u0435 \u043a\u043e\u043d\u0441\u0442\u0440\u0443\u043a\u0442\u043e\u0440\u0430 \r\n       \u0431\u0430\u0437\u043e\u0432\u043e\u0433\u043e \u043a\u043b\u0430\u0441\u0441\u0430;\r\n     - \u043f\u043e\u043f\u0440\u0430\u0432\u0438\u0442\u044c \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a\u0438 \u0441\u043e\u0431\u044b\u0442\u0438\u0439;\r\n     - \u0434\u043e\u043f\u0438\u0441\u0430\u0442\u044c \u043d\u0435\u043e\u0431\u0445\u043e\u0434\u0438\u043c\u0443\u044e \u0444\u0443\u043d\u043a\u0446\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u044c;\r\n     - \u0434\u043e\u043f\u0438\u0441\u0442\u044c \u043a\u043e\u0434 \u0434\u043b\u044f \u0442\u0435\u0441\u0442\u043e\u0432\u043e\u0439 \u0444\u0443\u043d\u043a\u0446\u0438\u0438.\r\n\r\n  ', 'source': u'None', 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'shortHelpString': u'', 'flag': 8192, 'recount': None, 'borderStep': 0, 'borderLeftColor': None, 'name': u'HeadCell_1250_15802', 'borderBottomColor': (0, 98, 196), 'keyDown': u'None', 'alias': u'None', 'init_expr': u'None', 'position': (1, 1), 'backgroundType': 0}, {'style': 0, 'activate': u'1', 'span': (1, 1), 'name': u'Editor', 'modules': {}, 'border': 0, 'object': u"import ic.PropertyEditor.ic_pyed as editor\r\nimport wx\r\ntext = '#Example'\r\n\r\nwin = editor.icPyEditor(self.parent, -1,\r\n         text, pos=self.position, size=self.size)\r\n#_dict_obj['Sizer'].Add(win, (2,1), (1,1), flag=wx.EXPAND)\r\n_resultEval = win", 'proportion': 0, 'alias': None, 'flag': 8192, 'init_expr': None, 'position': (3, 1), 'type': u'Import', 'size': (500, 220)}, {'alias': None, 'style': 0, 'activate': 1, 'span': (1, 1), 'name': u'ModulName', 'show': 1, 'init_expr': u'None', 'text': u"@#  \u041e\u043f\u0440\u0435\u0434\u0435\u043b\u044f\u0435\u043c \u0438\u043c\u044f \u043c\u043e\u0434\u0443\u043b\u044f\r\ntry: \r\n    _resultEval = 'Module:'+self.modulName\r\nexcept:\r\n    _resultEval = 'Module: .ic/components/user/userClass.py'\r\n\r\n", 'recount': None, 'proportion': 0, 'refresh': None, 'source': None, 'flag': 0, 'foregroundColor': (0, 98, 196), 'keyDown': None, 'backgroundColor': None, 'type': u'StaticText', 'position': (2, 1), 'font': {'style': 'bold', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Arial', 'type': 'Font', 'underline': False, 'size': 8}, 'border': 0, 'size': (-1, 18)}], 'position': wx.Point(158, 63), 'flexCols': [], 'vgap': 2, 'size': (-1, -1)}], 'name': u'Panel_1804', 'keyDown': u'None', 'alias': None, 'init_expr': u'', 'position': wx.Point(0, 0)}

#   Версия объекта
__version__ = (1, 0, 1, 2)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'icEditModulClass'


class icEditModulClass:
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
    Тестируем класс icEditModulClass.
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
