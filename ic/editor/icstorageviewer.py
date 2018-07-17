#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Окно просмотра хранилища переменных.
"""

import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.interfaces.icobjectinterface as icobjectinterface

from ic.kernel import io_prnt
from ic.engine import ic_user

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'obj_module': None, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (500, 400), 'style': 536877056, 'foregroundColor': None, 'span': (1, 1), 'title': u'\u0425\u0440\u0430\u043d\u0438\u043b\u0438\u0449\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0445:', 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'Dialog', 'res_module': None, 'description': None, 'onClose': None, '_uuid': u'c2503029d51fe455f7189c0fc5cce99d', 'moveAfterInTabOrder': u'', 'killFocus': None, 'flag': 0, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'obj_module': None, 'description': None, 'position': (0, 0), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'1b8806cf6c2d638c25d3c59ff3c112d6', 'proportion': 0, 'name': u'DefaultName_1481', 'alias': None, 'flag': 8192, 'init_expr': None, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'labels': [u'\u0418\u043c\u044f', u'\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435', u'\u041f\u0440\u0430\u0432\u0430 \u0434\u043e\u0441\u0442\u0443\u043f\u0430', u'\u041a\u043b\u044e\u0447 \u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0438'], 'refresh': None, 'selectChanged': None, 'border': 0, 'titleRoot': u'\u041f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0435', 'treeDict': {}, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'source': u'', 'itemExpanded': None, 'size': (-1, -1), 'type': u'SimpleTreeListCtrl', 'res_module': None, 'description': None, '_uuid': u'afd222b95c66f2028577b8c94351c2a0', 'style': 0, 'flag': 8192, 'recount': None, 'itemCollapsed': None, 'backgroundColor': None, 'name': u'view_treectrl', 'wcols': [100, 300, 100, 100], 'keyDown': None, 'alias': None, 'itemActivated': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}, {'activate': 1, 'obj_module': None, 'show': 1, 'attach_focus': False, 'mouseClick': u"GetObject('storageViewerDialog').Close()", 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u0417\u0430\u043a\u0440\u044b\u0442\u044c', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'res_module': None, 'description': None, '_uuid': u'8d35cc64bd3403c924cf9ca2d9f62a0e', 'userAttr': None, 'moveAfterInTabOrder': u'', 'flag': 2304, 'recount': None, 'name': u'close_button', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None, 'refresh': None, 'mouseContextDown': None}], 'span': (1, 1), 'res_module': None, 'border': 0, 'layout': u'vertical', 'vgap': 0, 'size': (-1, -1)}], 'setFocus': None, 'name': u'storageViewerDialog', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}

#   Версия объекта
__version__ = (1, 0, 0, 3)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'icStorageViewerDlg'


class icStorageViewerDlg(icobjectinterface.icObjectInterface):

    def __init__(self, parent):
        """
        Конструктор интерфейса.
        """
        #   Вызываем конструктор базового класса
        icobjectinterface.icObjectInterface.__init__(self, parent, resource)
        
        try:
            viewer = self.GetNameObj('view_treectrl')
            var_storage = ic_user.getVarStorage().getStorage()
            io_prnt.outLog(u'VAR STORAGE VIEWER: <%s>' % var_storage)
            variables = self._storageConvert(var_storage)
            viewer.LoadTree(variables)
        except:
            io_prnt.outErr(u'Ошибка инициализации дерева просмотра хранилища переменных.')

    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK
    
    def _storageConvert(self, VarStorage_):
        """
        Переконвертировать хранилище в формат дерева.
        """
        result = []
        for name in VarStorage_.keys():
            tree_item = {}
            storage_item = VarStorage_[name]
            tree_item['name'] = name
            tree_item['__record__'] = [name, str(storage_item['data']),
                                       str(storage_item['security']),
                                       str(storage_item['lock_key'])]
            if storage_item['folder']:
                tree_item['child'] = self._storageConvert(storage_item['folder'])
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
