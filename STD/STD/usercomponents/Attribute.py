#!/usr/bin/env python
# -*- coding: utf-8 -*-
### TEMPLATE_MODULE:
"""
Атрибут документа.
"""
import wx
import ic.interfaces.ictemplate as ictemplate
import ic.PropertyEditor.icDefInf as icDefInf
import ic.utils.util as util
import copy
from STD import reestr_img
import ic.engine.ic_user as ic_user


### Общий интерфейс компонента
ictemplate.init_component_interface(globals(), ic_class_name = 'CAttribute')

ic_class_spc = {'name':'defaultAttribute',
                'type':'Attribute',
                'attrType':None,
                'sprav_type':None,
                'init':None,
                'nest':'Unit:attributes',
                '__attr_types__': {icDefInf.EDT_CHOICE:['sprav_type', 'attrType']},
                '__lists__':{'nest':['Unit:attributes'],
                             'attrType':ic_user.get_names_in_res(('mtd',), 'AttributeType')},
                '__parent__':ictemplate.SPC_IC_TEMPLATE}

ic_class_pic = reestr_img.Requisite
ic_class_pic2 = reestr_img.Requisite
                
### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'style': 0, 'activate': 1, 'obj_module': None, 'name': u'attributes', 'component_module': None, '_uuid': u'42d46718e37df3d399af0d64f865d02f', 'value': None, 'alias': None, 'init_expr': None, 'child': [], 'res_module': None, 'type': u'Unit', 'description': None}

#   Версия объекта
__version__ = (1, 0, 1, 0)
###END SPECIAL BLOCK

class CAttribute(ictemplate.icTemplateInterface):
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
    Тестируем класс CAttribute.
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