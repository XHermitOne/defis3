#!/usr/bin/env python
# -*- coding: utf-8 -*-


import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util

#   Ресурсное описание класса
resource = {'activate': 1, 'show': 1, 'child': [], 'refresh': None, 'border': 0, 'size': (-1, -1), 'style': 524288, 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': (128, 128, 192), 'type': 'Panel', 'onClose': None, 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 0, 'recount': None, 'name': 'defaultWindow_1075', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1)}

__version__ = (1, 0, 1, 2)


class examplePanel:
    def __init__(self, parent):
        self.evalSpace = util.InitEvalSpace()
        self.__obj = prs.icBuildObject(parent, resource, evalSpace=self.evalSpace, bIndicator=False)
        self.object = self.evalSpace['_root_obj']
        
    def getObject(self):
        """
        """
        return self.object


def test(par=0):
    """
    Тестируем класс examplePanel.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    win = examplePanel(None)

    ################
    # Тестовый код #
    ################
        
    win.getObject().Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
