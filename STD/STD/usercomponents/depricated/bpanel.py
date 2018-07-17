#!/usr/bin/env python
# -*- coding: utf-8 -*-
### TEMPLATE_MODULE:

import wx
import ic.interfaces.ictemplate as ictemplate
import ic.utils.util as util
import copy
import ic.components.icwxpanel as parentModule
import ic.components.custom.icsplitter as split_mod
import ic.PropertyEditor.icDefInf as icDefInf
from ic.kernel import io_prnt

### Standart component interface
ictemplate.inherit_component_interface(globals(), parentModule, ic_class_name='CBrPanel')

#   Component version
__version__ = (1, 0, 0, 2)

XP_BACKGROUND_COLOR = (225, 235, 250)
XP_BORDER_COLOR = (180, 199, 239)

ic_class_spc = dict({'name': 'default',
                     'type': 'BrPanel',
                     'step': 0,
                     'backgroundColor': None,
                     'border_color': None,
                     '__attr_types__': {icDefInf.EDT_COLOR: ['border_color'],
                                        icDefInf.EDT_NUMBER: ['step']},
                     '__parent__': parentModule.ic_class_spc
                     })

# Приписываем компонент у сплитера в разрешенных                
split_mod.ic_can_contain.append(ic_class_spc['type'])
parentClass = getattr(parentModule, parentModule.ic_class_name)


class CBrPanel(parentClass):
    """
    User component class.
    @type component_spc: C{dictionary}
    @cvar component_spc: Specification.
        - B{type='defaultType'}:
        - B{name='default'}:
    """

    @staticmethod
    def TestComponentResource(res, context, parent, *arg, **kwarg):
        prs = kwarg['parsemodule']
        testObj = prs.CreateForm('Test', formRes=res,
                                 evalSpace=context, parent=parent, bIndicator=True)
        #   Для оконных компонентов надо вызвать метод Show
        try:
            testObj.context['_root_obj'].Show(True)
            testObj.context['_root_obj'].SetFocus()
        except: 
            io_prnt.outErr()
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace = None,
                 bCounter=False, progressDlg=None):
        """
        Interface constructor.
        """
        # Append for specification
        component = util.icSpcDefStruct(ic_class_spc, component)
        for key in [x for x in ic_class_spc.keys() if not x.startswith('__')]:
            if component[key] is None:
                component[key] = ic_class_spc[key]
            
        parentClass.__init__(self, parent, id, component, logType, evalSpace,
                             bCounter, progressDlg)
        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        for key in [x for x in component.keys() if not x.startswith('__')]:
            setattr(self, key, component[key])
    
        self.SetBorderMode(self.border_color, self.step)
        

def test(par=0):
    """
    Test class Cbpanel.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = CBrPanel(frame, -1, {'step': 4, 'backgroundColor': None})

    #
    # Test code
    #
        
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
