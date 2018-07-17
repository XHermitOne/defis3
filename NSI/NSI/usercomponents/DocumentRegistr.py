#!/usr/bin/env python
# -*- coding: utf-8 -*-
### TEMPLATE_MODULE:

import wx
import ic.interfaces.ictemplate as ictemplate
import ic.utils.util as util
import copy
from . import sprav as parentModule
from . import spravmanager

### Standart component interface
ictemplate.inherit_component_interface(globals(), parentModule, ic_class_name = 'CDocumentRegistr')

#   Component version
__version__ = (1,0,0,1)

ic_class_spc = {'name':'default',
                'type':'DocumentRegistr',
                '__parent__':parentModule.ic_class_spc}
spravmanager.ic_can_contain.append(ic_class_spc['type'])
parentClass = getattr(parentModule, parentModule.ic_class_name)
class CDocumentRegistr(parentClass):
    """ User component class.
    @type component_spc: C{dictionary}
    @cvar component_spc: Specification.
        - B{type='defaultType'}:
        - B{name='default'}:
    """
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace = None, bCounter=False, progressDlg=None):
        """ Interface constructor."""
        # Append for specification
        component = util.icSpcDefStruct(ic_class_spc, component)
        parentClass.__init__(self, parent, id, component, logType, evalSpace,
                                                bCounter, progressDlg)
        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        for key in [x for x in component.keys() if not x.startswith('__')]:
            setattr(self, key, component[key])
    
def test(par=0):
    """ Test class CDocumentRegistr."""
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)

    ################
    # Test code    #
    ################
        
    frame.Show(True)
    app.MainLoop()
    
if __name__ == '__main__':
    test()