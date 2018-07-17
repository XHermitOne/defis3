#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.interfaces.icobjectinterface as icobjectinterface

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'pic': None, 'can_contain': u"['docFolder']", 'storage_type': u'DirStorage', 'spc': {}, 'description': u'\u0425\u0440\u0430\u043d\u0438\u043b\u0438\u0449\u0435 \u043f\u0430\u043f\u043a\u0438 \u0430\u0440\u0445\u0438\u0432\u043d\u044b\u0445 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u043e\u0432', 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'source': None, 'init': None, 'can_not_contain': None, 'type': u'Reestr', 'const_spc': {}, '_uuid': u'064490231acfffb80dfcca8f5f4926f9', 'child': [{'activate': 1, 'pic': None, 'can_contain': u"['document']", 'storage_type': u'FileStorage', 'spc': {}, 'const_spc': {}, 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'init': None, 'can_not_contain': None, 'type': u'ReestrObject', 'description': u'\u041f\u0430\u043f\u043a\u0430', '_uuid': u'f80acb4abdb0d7cd30c6f132b9c264af', 'child': [], 'report': None, 'edit_form': None, 'name': u'mainDocFolder', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}, {'activate': 1, 'pic': None, 'can_contain': u"['document']", 'storage_type': u'FileNodeStorage', 'spc': {}, 'const_spc': {}, 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'init': None, 'can_not_contain': None, 'type': u'ReestrObject', 'description': u'\u041f\u0430\u043f\u043a\u0430', '_uuid': u'05269a746067bc567a3931762a209a17', 'child': [], 'report': None, 'edit_form': None, 'name': u'docFolder', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}, {'activate': 1, 'pic': None, 'can_contain': None, 'storage_type': u'FileNodeStorage', 'spc': {}, 'const_spc': {}, 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'init': None, 'can_not_contain': None, 'type': u'ReestrObject', 'description': u'\u0414\u043e\u043a\u0443\u043c\u0435\u043d\u0442', '_uuid': u'8146303524da6d89ac752c4419cd484d', 'child': [], 'report': None, 'edit_form': None, 'name': u'document', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}], 'report': None, 'edit_form': None, 'name': u'archiveDocsReestr', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}

#   Версия объекта
__version__ = (1, 0, 0, 2)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'IArchiveDocsReestr'

class IArchiveDocsReestr(icobjectinterface.icObjectInterface):
    def __init__(self, parent):
        '''
        Конструктор интерфейса.
        '''
        #
        
        #   Вызываем конструктор базового класса
        icobjectinterface.icObjectInterface.__init__(self, parent, resource)
            
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK
    
def test(par=0):
    '''
    Тестируем класс IArchiveDocsReestr.
    '''
    
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
    
    