#!/usr/bin/env python
# -*- coding: utf-8 -*-
### TEMPLATE_MODULE:
"""
Описание типа атрибута документа.
"""
import wx
import ic.interfaces.ictemplate as ictemplate
import ic.utils.util as util
import copy

### Общий интерфейс компонента
ictemplate.init_component_interface(globals(), ic_class_name = 'CAttributeType')

ic_class_spc = {'name':'defaultPanel',
                'type':'AttributeType',
                'nest':'Unit:types',
                '__lists__':{'nest':['Unit:types']},
                '__parent__':ictemplate.SPC_IC_TEMPLATE}
                
### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'style': 0, 'activate': 1, 'obj_module': None, 'name': u'types', 'component_module': None, '_uuid': u'42d46718e37df3d399af0d64f865d02f', 'value': None, 'alias': None, 'init_expr': None, 'child': [], 'res_module': None, 'type': u'Unit', 'description': None}

#   Версия объекта
__version__ = (1, 0, 0, 6)
###END SPECIAL BLOCK

class CAttributeType(ictemplate.icTemplateInterface):
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
    Тестируем класс CAttributeType.
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