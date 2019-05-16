#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wx

import ic.components.icResourceParser as prs
import ic.utils.util as util

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'show': 1, 'recount': None, 'keyDown': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'onClose': None, '_uuid': u'c7cecad2d4756d0dc2a3f2e351e8b9cd', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [], 'name': u'edtPanel', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}

#   Версия объекта
__version__ = (1, 1, 1, 1)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'IVidProdEdtPanel'


class IVidProdEdtPanel:
    def __init__(self, parent):
        self.evalSpace = util.InitEvalSpace()
        self.evalSpace['WrapperObj'] = self
        self.__obj = prs.icBuildObject(parent, resource, evalSpace=self.evalSpace, bIndicator=False)
        self.object = self.evalSpace['_root_obj']
        
    def getObject(self):
        """
        """
        return self.object

    def GetNameObj(self, name):
        """
        Возвращает указатель на объект с указанным именем.
        """
        if self.evalSpace['_dict_obj'].has_key(name):
            return self.evalSpace['_dict_obj'][name]
        else:
            return None
            
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK


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
