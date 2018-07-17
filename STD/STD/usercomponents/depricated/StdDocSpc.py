#!/usr/bin/env python
# -*- coding: utf-8 -*-
### TEMPLATE_MODULE:
"""
Спецификация документа.
"""
import wx
import ic.interfaces.ictemplate as ictemplate
import ic.utils.util as util
import copy
from STD import reestr_img

### Общий интерфейс компонента
ictemplate.init_component_interface(globals(), ic_class_name = 'CStdDocSpc')

ic_class_spc = {'name':'defaultSpc',
                'type':'StdDocSpc',
                'child':[],
                'nest':'Unit:attributes',
                '__lists__':{'nest':['Unit:attributes']},
                '__parent__':ictemplate.SPC_IC_TEMPLATE}

ic_class_pic = reestr_img.DocSpc
ic_class_pic2 = reestr_img.DocSpc
ic_can_contain = ['Attribute']

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'style': 0, 'activate': 1, 'name': u'Spc', 'component_module': None, '_uuid': u'55cfdafa1546ec3b4ef4c902f53e978c', 'value': None, 'alias': None, 'init_expr': None, 'child': [{'style': 0, 'activate': 1, 'name': u'StdAttributes', 'component_module': None, '_uuid': u'60223d55f7e0a99704b3a13de4383c20', 'value': None, 'alias': None, 'init_expr': None, 'child': [{'style': 0, 'activate': 1, 'name': u'spc_id', 'component_module': None, '_uuid': u'cbc97ea61446a7640fcbcf1715a3a672', 'value': None, 'alias': None, 'init_expr': None, 'child': [], 'type': u'Unit', 'description': None}, {'style': 0, 'activate': 1, 'name': u'spc_name', 'component_module': None, '_uuid': u'94590e318ce6825a114b747843e6460f', 'value': None, 'alias': None, 'init_expr': None, 'child': [], 'type': u'Unit', 'description': None}], 'type': u'Unit', 'description': None}, {'style': 0, 'activate': 1, 'name': u'attributes', 'component_module': None, '_uuid': u'60223d55f7e0a99704b3a13de4383c20', 'value': None, 'alias': None, 'init_expr': None, 'child': [], 'type': u'Unit', 'description': None}], 'type': u'Unit', 'description': None}

#   Версия объекта
__version__ = (1, 0, 1, 0)
###END SPECIAL BLOCK

class CStdDocSpc(ictemplate.icTemplateInterface):
    """
    Описание пользовательского компонента.
    
    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{type='defaultType'}:
        - B{name='default'}:
    """
    component_spc = ic_class_spc
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace = None, bCounter=False, progressDlg=None):
        """
        Конструктор интерфейса.
        """
        #   Дополняем до спецификации
        component = util.icSpcDefStruct(ic_class_spc, component)
        ictemplate.icTemplateInterface.__init__(self, parent, id, component, logType, evalSpace,
                                                bCounter, progressDlg)
    def _init_template_resource(self):
        """
        Инициализация ресурса шаблона.
        """
        self._templRes = resource
    
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK
    
def test(par=0):
    """
    Тестируем класс CStdDocSpc.
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