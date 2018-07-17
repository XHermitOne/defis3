#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.interfaces.icobjectinterface as icobjectinterface

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'pic': None, 'can_contain': u"['docFolder']", 'storage_type': u'DirStorage', 'spc': {}, 'const_spc': {}, 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'source': u'public_docs_storage', 'init': None, 'can_not_contain': None, 'type': u'Reestr', 'description': u'\u0425\u0440\u0430\u043d\u0438\u043b\u0438\u0449\u0435 \u043f\u0430\u043f\u043a\u0438 \u043e\u0431\u0449\u0438\u0445 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u043e\u0432', '_uuid': u'17d9e818738c140b2eaf3507719498f6', 'child': [{'activate': 1, 'pic': u'from ic.imglib import common\r\nreturn common.imgFolder', 'can_contain': u"['document']", 'storage_type': u'FileStorage', 'spc': {}, 'description': u'\u041f\u0430\u043f\u043a\u0430 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u043e\u0432', 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'init': None, 'can_not_contain': None, 'type': u'ReestrObject', 'const_spc': {}, '_uuid': u'596d4363fbdd9aa44ee1c56eb6b9be1f', 'child': [], 'report': None, 'edit_form': None, 'name': u'mainDocFolder', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}, {'activate': 1, 'pic': u'from ic.imglib import common\r\nreturn common.imgFolder', 'can_contain': u"['document']", 'storage_type': u'FileNodeStorage', 'spc': {}, 'description': u'\u041f\u0430\u043f\u043a\u0430 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u043e\u0432', 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'init': None, 'can_not_contain': None, 'type': u'ReestrObject', 'const_spc': {}, '_uuid': u'15d7095d7c24f767233e2afc32723b33', 'child': [], 'report': None, 'edit_form': None, 'name': u'docFolder', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}, {'activate': 1, 'pic': u'from ic.imglib import common\r\nreturn common.imgNew', 'report': None, 'storage_type': u'FileNodeStorage', 'spc': {}, 'const_spc': {}, 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'init': None, 'can_not_contain': None, 'type': u'ReestrObject', 'description': u'\u0414\u043e\u043a\u0443\u043c\u0435\u043d\u0442', '_uuid': u'678fb2a0f46c98858b097de87f48bc2c', 'child': [], 'can_contain': None, 'edit_form': None, 'name': u'document', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}], 'report': None, 'edit_form': None, 'name': u'publicDocsReestr', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}

#   Версия объекта
__version__ = (1, 0, 0, 5)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'IPublicDocsReestr'

class IPublicDocsReestr(icobjectinterface.icObjectInterface):
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
    Тестируем класс IPublicDocsReestr.
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
    
    