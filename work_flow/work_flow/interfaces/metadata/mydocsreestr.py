#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from ic.imglib import common
import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.interfaces.icobjectinterface as icobjectinterface

from work_flow.usercomponents import document

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'pic': None, 'report': None, 'storage_type': u'DirStorage', 'spc': {}, 'const_spc': {}, 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'source': u'my_docs_storage', 'init': None, 'can_not_contain': None, 'type': u'Reestr', 'description': u'\u0425\u0440\u0430\u043d\u0438\u043b\u0438\u0449\u0435 \u043f\u0430\u043f\u043a\u0438 \u043b\u0438\u0447\u043d\u044b\u0445 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u043e\u0432', '_uuid': u'92aab957467277a2fd052fa995f89f84', 'child': [{'activate': 1, 'pic': u'WrapperObj.getPic_docFolder(self)', 'report': None, 'storage_type': u'FileStorage', 'spc': {'description': u'\u041f\u0430\u043f\u043a\u0430'}, 'const_spc': {}, 'style': 0, 'container': True, 'component_module': None, 'pic2': u'WrapperObj.getPic2_docFolder(self)', 'init': None, 'can_not_contain': None, 'type': u'ReestrObject', 'description': u'\u041f\u0430\u043f\u043a\u0430 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u043e\u0432', '_uuid': u'9db2bc0d3f5e767eb721c5c76924906d', 'child': [], 'can_contain': u"['docFolder']", 'init_obj': u'None', 'edit_form': u'work_flow.interfaces.forms.foldereditpanel.IFolderEditPanel', 'name': u'mainDocFolder', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}, {'activate': 1, 'pic': u'WrapperObj.getPic_docFolder(self)', 'report': None, 'storage_type': u'FileNodeStorage', 'spc': {'description': u'\u041f\u0430\u043f\u043a\u0430'}, 'const_spc': {}, 'style': 0, 'container': True, 'component_module': None, 'pic2': u'WrapperObj.getPic2_docFolder(self)', 'init': None, 'can_not_contain': None, 'type': u'ReestrObject', 'description': u'\u041f\u0430\u043f\u043a\u0430 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u043e\u0432', '_uuid': u'6c08b27b4597c1ff2aa9cdea0954f54a', 'child': [], 'can_contain': u"['document']", 'init_obj': u'None', 'edit_form': u'work_flow.interfaces.forms.foldereditpanel.IFolderEditPanel', 'name': u'docFolder', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}, {'activate': 1, 'pic': u'WrapperObj.getPic_docFolder(self)', 'report': None, 'storage_type': u'FileNodeStorage', 'spc': {'doc_type': None, 'doc_id': 0, 'description': u'\u0414\u043e\u043a\u0443\u043c\u0435\u043d\u0442'}, 'const_spc': {}, 'style': 0, 'container': True, 'component_module': None, 'pic2': u'WrapperObj.getPic2_docFolder(self)', 'init': None, 'can_not_contain': None, 'type': u'ReestrObject', 'description': u'\u0414\u043e\u043a\u0443\u043c\u0435\u043d\u0442', '_uuid': u'bb7d7a0a5cbf692e3a34c51a26ea0b96', 'child': [], 'can_contain': u'[]', 'init_obj': u'WrapperObj.initDocument(new_reestr_obj)', 'edit_form': u'@WrapperObj.editDocument(self)', 'name': u'document', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}], 'can_contain': u"['mainDocFolder']", 'edit_form': None, 'name': u'myDocsReestr', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}

#   Версия объекта
__version__ = (1, 0, 4, 5)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'IMyDocsReestr'

class IMyDocsReestr(icobjectinterface.icObjectInterface):
    def __init__(self, parent):
        '''
        Конструктор интерфейса.
        '''
        #
        
        #   Вызываем конструктор базового класса
        icobjectinterface.icObjectInterface.__init__(self, parent, resource)
            
    def getPic_docFolder(self, metaObj):
        """
        Атрибут <pic> на узлах funcDocFolder.
        """
        if metaObj.value.metatype.lower()=='document':
            return common.imgBlank
        else:
            if metaObj.value.name.lower()=='trash':
                return common.imgTrash
            elif metaObj.value.name.lower()=='input':
                return common.imgInputFolder
            elif metaObj.value.name.lower()=='output':
                return common.imgOutputFolder
            return common.imgFolder
        
    def getPic2_docFolder(self, metaObj):
        """
        Атрибут <pic> на узлах funcDocFolder.
        """
        if metaObj.value.metatype.lower()=='document':
            return common.imgBlank
        else:
            if metaObj.value.name.lower()=='trash':
                return common.imgTrash
            elif metaObj.value.name.lower()=='input':
                return common.imgInputFolderOpen
            elif metaObj.value.name.lower()=='output':
                return common.imgOutputFolderOpen
            return common.imgFolderOpen
        
    def initDocument(self,metaObj):
        '''
        Инициализация/создание документа.
        '''
        work_flow_obj=prs.icCreateObject('tech_work','mtd')
        #print '!!!',work_flow_obj
        doc_obj=None
        if work_flow_obj:
            doc_obj=work_flow_obj.createDocument()
            metaObj.value.doc_id=doc_obj.doc_id
            metaObj.value.doc_type=doc_obj.name
            print('initDocument',metaObj.value.name,metaObj.value.doc_type)
        return doc_obj
        
    def editDocument(self,metaObj):
        '''
        Форма редактирования документа.
        '''
        print('EDIT DOCUMENT START')
        work_flow_obj=prs.icCreateObject('tech_work','mtd')
                
        edit_panel=None
        if work_flow_obj:
            doc_obj=work_flow_obj.getCloneDocumentByName(metaObj.value.doc_type)
            doc_obj.loadRequisite(metaObj.value.doc_id)
            edit_panel=doc_obj.Edit()
        print('EDIT DOCUMENT',edit_panel)
        return edit_panel
        
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK
    
def test(par=0):
    '''
    Тестируем класс IMyDocsReestr.
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
    
    