#!/usr/bin/env python
# -*- coding: utf-8 -*-


import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK

#   Ресурсное описание класса
resource = {'activate': 1, 'show': 1, 'selPageColor': (227, 226, 223), 'recount': None, 'onSelectTitle': u'None', 'titles': [u'\u0411\u0430\u0437\u043e\u0432\u044b\u0435', u'\u0421\u043f\u0435\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u0435', u'\u0412\u0441\u0435'], 'refresh': None, 'images': [u'Event.png', u'Item.png', u'list.png'], 'font': {'family': 'sansSerif', 'style': 'regular', 'underline': False, 'faceName': 'Arial', 'size': 8}, 'border': 0, 'size': wx.Size(393, 27), 'moveAfterInTabOrder': u'', 'foregroundColor': (128, 128, 128), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': (248, 248, 248), 'type': u'TitlesNotebook', '_uuid': u'c404bc99f6e8d4763433edc049468614', 'style': 0, 'flag': 8192, 'child': [], 'path': u"@# \u041e\u043f\u0440\u0435\u0434\u0435\u043b\u044f\u0435\u043c \u043f\u0443\u0442\u044c \u0434\u043e \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0438 \u043a\u0430\u0440\u0442\u0438\u043d\u043e\u043a\r\nimport ic.utils.resource as resource\r\n_resultEval = resource.icGetICPath()+'/imglib/common'\r\n", 'name': u'NB', 'icDelButton': 1, 'keyDown': u'None', 'alias': None, 'init_expr': u'None', 'position': (2, 3)}

#   Версия объекта
__version__ = (1, 0, 1, 2)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'icResPropNotebook'


class icResPropNotebook:
    def __init__(self, parent):
        self.evalSpace = util.InitEvalSpace()
        self.__obj = prs.icBuildObject(parent, resource, evalSpace=self.evalSpace, bIndicator=False)
        self.object = self.evalSpace['_root_obj']
        self.object.SelectTitle(0)
        
    def getObject(self):
        """
        """
        return self.object


def test(par=0):
    """
    Тестируем класс icResPropNotebook.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)

    ################
    # Тестовый код #
    ################
    nb = icResPropNotebook(win)    
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
