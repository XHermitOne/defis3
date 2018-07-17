#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import ic.interfaces.ictemplate as ictemplate
import ic.utils.util as util
import copy
import ic.components.user.ic_imglib_wrp as parentModule
import ic.PropertyEditor.icDefInf as icDefInf
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
__version__ = (1, 0, 0, 3)


class CImageList(wx.ImageList, parentClass):
    """
    User component class.
    @type component_spc: C{dictionary}
    @cvar component_spc: Specification.
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
        for key in [x for x in component.keys() if not x.startswith('__')]:
            setattr(self, key, component[key])
   
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        prs.icResourceParser(self, self.child, None, evalSpace=self.evalSpace,
                             bCounter=bCounter, progressDlg=progressDlg)


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
