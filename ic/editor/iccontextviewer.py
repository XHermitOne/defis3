#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Окно просмотра контекста.
"""

import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.interfaces.icobjectinterface as icobjectinterface

from ic.kernel import io_prnt
from ic.engine import ic_user

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Resource description of class
resource={'activate': 1, 'obj_module': None, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (500, 400), 'style': 536877056, 'foregroundColor': None, 'span': (1, 1), 'fit': False, 'title': u'\u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435 \u043a\u043e\u043d\u0442\u0435\u043a\u0441\u0442\u0430:', 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'Dialog', 'res_module': None, 'enable': True, 'description': None, 'onClose': None, '_uuid': u'f25c7f489b53cd5c49bcf84cf9f0a41f', 'moveAfterInTabOrder': u'', 'killFocus': None, 'flag': 0, 'alias': None, 'child': [{'activate': 1, 'obj_module': None, 'border': 0, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'type': u'BoxSizer', 'res_module': None, 'hgap': 0, 'description': None, '_uuid': u'1b8806cf6c2d638c25d3c59ff3c112d6', 'flag': 8192, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'labels': [u'\u0418\u043c\u044f', u'\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435', u'\u041f\u0440\u0430\u0432\u0430 \u0434\u043e\u0441\u0442\u0443\u043f\u0430', u'\u041a\u043b\u044e\u0447 \u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0438'], 'refresh': None, 'selectChanged': None, 'border': 0, 'size': (-1, -1), 'treeDict': {}, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'alias': None, 'component_module': None, 'proportion': 1, 'itemCollapsed': None, 'source': u'', 'itemActivated': None, 'itemExpanded': None, 'titleRoot': u'\u041f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0435', 'type': u'SimpleTreeListCtrl', 'res_module': None, 'enable': True, 'description': None, '_uuid': u'afd222b95c66f2028577b8c94351c2a0', 'style': 0, 'flag': 8192, 'recount': None, 'hideHeader': False, 'backgroundColor': None, 'child': [], 'name': u'view_treectrl', 'wcols': [100, 300, 100, 100], 'data_name': None, 'keyDown': None, 'itemChecked': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}, {'activate': 1, 'obj_module': None, 'show': 1, 'attach_focus': False, 'data_name': None, 'mouseClick': u"GetObject('contextViewerDialog').Close()", 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'alias': None, 'component_module': None, 'proportion': 0, 'label': u'\u0417\u0430\u043a\u0440\u044b\u0442\u044c', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'res_module': None, 'enable': True, 'description': None, '_uuid': u'52c5200d616783fbb27976e3c2512e43', 'userAttr': None, 'moveAfterInTabOrder': u'', 'flag': 2304, 'recount': None, 'name': u'close_button', 'mouseUp': None, 'keyDown': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None, 'refresh': None, 'mouseContextDown': None}], 'layout': u'vertical', 'name': u'DefaultName_1481', 'alias': None, 'init_expr': None, 'position': (0, 0), 'vgap': 0}], 'icon': None, 'setFocus': None, 'name': u'contextViewerDialog', 'data_name': None, 'keyDown': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}

#   Version
__version__ = (1, 0, 0, 6)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'icContextViewerDlg'


class icContextViewerDlg(icobjectinterface.icObjectInterface):

    def __init__(self, parent, Context_=None):
        """
        Конструктор интерфейса.
        """
        #   Вызываем конструктор базового класса
        icobjectinterface.icObjectInterface.__init__(self, parent, resource)
        
        try:
            viewer = self.GetNameObj('view_treectrl')
            if Context_ is None:
                Context_ = ic_user.getKernel().GetContext()
            variables = self._contextConvert(Context_)
            viewer.LoadTree(variables)
        except:
            io_prnt.outErr(u'Ошибка инициализации дерева просмотра хранилища переменных.')

    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK
    
    def _contextConvert(self, Context_):
        """
        Переконвертировать контекст в формат дерева.
        """
        result = []
        for name in Context_.keys():
            tree_item = {}
            context_item = Context_[name]
            tree_item['name'] = name
            tree_item['__record__'] = [name, str(context_item), '', '']
            result.append(tree_item)
        return result

    def design(self):
        """
        """
        self.getObject().ShowModal()


def test(par=0):
    """
    Тестируем класс.
    """
    
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)

    #
    # Тестовый код
    #
        
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
