#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wx
import ic.interfaces.ictemplate as ictemplate
from ic.utils import util
import copy
import ic.components.user.ic_imglib_wrp as parentModule
from ic.PropertyEditor import icDefInf
import ic.components.icResourceParser as prs

# Standart component interface
ictemplate.inherit_component_interface(globals(), parentModule, ic_class_name='CImageList')

ic_class_spc = {'name': 'default',
                'type': 'icImageList',
                'img_size': (16, 16),

                '__attr_types__': {icDefInf.EDT_SIZE: ['img_size'],
                                   },
                '__parent__': parentModule.ic_class_spc
                }


parentClass = getattr(parentModule, parentModule.ic_class_name)

#   Component version
__version__ = (1, 1, 1, 2)


class CImageList(wx.ImageList, parentClass):
    """
    User component class.

    :type component_spc: C{dictionary}
    :cvar component_spc: Specification.
        - B{type='defaultType'}:
        - B{name='default'}:
    """

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Interface constructor.
        """
        # Append for specification
        component = util.icSpcDefStruct(ic_class_spc, component)
        sx, sy = component['img_size']
        wx.ImageList.__init__(self, sx, sy)
        parentClass.__init__(self, parent, id, component, logType, evalSpace,
                             bCounter, progressDlg)
        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        self.createAttributes(component)


def test(par=0):
    """
    Test class CicImageList.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)

    #
    # Test code
    #
        
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
