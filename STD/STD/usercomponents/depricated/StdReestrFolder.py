#!/usr/bin/env python
# -*- coding: utf-8 -*-
### TEMPLATE_MODULE:
"""
Компонент папки объектов реестра (StdReestrFolder). Наследуется от MetaItem.
"""
import wx
import ic.interfaces.ictemplate as ictemplate
import ic.utils.util as util
import copy
from STD import reestr_img

### Общий интерфейс компонента
ictemplate.init_component_interface(globals(), ic_class_name = 'CReestrFolder')

ic_class_spc = {'name':'defaultPanel',
                'type':'StdReestrFolder',
                'nest':'MetaItem:ReestrFolder',
                'can_contain':None,     #Разрешающее правило
                'can_not_contain':None, #Запрещающее правило
                '__lists__':{'nest':['MetaItem:ReestrFolder']},
                '__parent__':ictemplate.SPC_IC_TEMPLATE}

ic_class_pic = reestr_img.imgReestrFolder
ic_class_pic2 = reestr_img.imgReestrFolder
ic_can_contain = ['StdReestrFolder','StdReestrObj']

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'pic': None, 'can_contain': u'[]', 'storage_type': u'FileNodeStorage', 'spc': {'data': []}, 'description': None, 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'init': None, 'can_not_contain': None, 'type': u'MetaItem', 'const_spc': {}, '_uuid': u'19f70bb1b2dcc02037d50b4c292a0773', 'child': [], 'report': None, 'edit_form': None, 'name': u'ReestrFolder', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}

#   Версия объекта
__version__ = (1, 0, 1, 7)
###END SPECIAL BLOCK

class CReestrFolder(ictemplate.icTemplateInterface):
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace = None, bCounter=False, progressDlg=None):
        """
        Конструктор интерфейса.
        """
        #   Дополняем до спецификации
        component = util.icSpcDefStruct(ic_class_spc, component)
        #   Доопределяем спецификацию
        self._init_spc(component)
        
        ictemplate.icTemplateInterface.__init__(self, parent, id, component, logType, evalSpace,
                                                bCounter, progressDlg)
        # Имя MetaItem делаем таким же как и имя реестра, т.к. у MetaTree типы
        # узлов определяются по именам.
        self.resource['name'] = component['name']
        #self.resource['_uuid'] = component['_uuid']
        self.resource['description'] = component['description']
        self.resource['can_contain'] = component['can_contain']
        self.resource['can_not_contain'] = component['can_not_contain']
        self.resource['pic'] = component['pic']
        self.resource['pic2'] = component['pic2']
                                                
    def _init_spc(self, component):
        """
        Доопределяет спецификацию.
        """
        component['storage_type'] = ic_metaitem_wrp.FILE_NODE_STORAGE_TYPE
        component['container'] = True
        
        if not component['pic']:
            component['pic'] = ic_class_pic
        if not component['pic2']:
            component['pic2'] = ic_class_pic2

    def _init_template_resource(self):
        """
        Инициализация ресурса шаблона.
        """
        self._templRes = resource
    
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK
    
def test(par=0):
    """
    Тестируем класс CReestrFolder.
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