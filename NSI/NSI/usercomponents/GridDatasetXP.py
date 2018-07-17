#!/usr/bin/env python
# -*- coding: utf-8 -*-
### TEMPLATE_MODULE:

import wx
import ic.interfaces.ictemplate as ictemplate
import ic.utils.util as util
import copy
import ic.components.icgriddataset as parentModule
from ic.components.renders import xpgridrenders as xpr
from ic.components import icfont

### Standart component interface
ictemplate.inherit_component_interface(globals(), parentModule, ic_class_name = 'CGridDatasetXP')
ic_class_pic = '@ic.imglib.newstyle_img.xpgrid'
ic_class_pic2 = '@ic.imglib.newstyle_img.xpgrid'

#   Component version
__version__ = (1,0,0,1)

ic_class_spc = {'name':'default',
                'type':'GridDatasetXP',
                
                #ВНИМАНИЕ!
                #В спецификации необходимо повторить ключ '__list__' из
                #родительской спецификации, потому что он не переносится автоматически!
                '__lists__':{'selection_mode':parentModule.GRID_SELECTION_MODES.keys(),
                            },
                            
                '__parent__':parentModule.ic_class_spc}

parentClass = getattr(parentModule, parentModule.ic_class_name)
class CGridDatasetXP(parentClass):
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
        
        self.SetCornerLabelRenderer(xpr.XPCornerLabelRenderer())
        self._colAttrs = []
        for col in xrange(self.GetNumberCols()):
            rndr = xpr.XPColLabelRenderer()
            if not self.cols[col]['sort'] in (None, 0, '0', 'False','None'):
                rndr.SetSortFlag()
                
#            self._colRendr.append(rndr)
            self.SetColLabelRenderer(col, rndr)
            attr = xpr.XPColAttr()
            self.SetColAttr(col, attr)
            self._colAttrs.append(attr)
        
        self._cell_height = 18
        self.SetColLabelSize(self._cell_height)
        font = icfont.icFont({})
        self.SetLabelFont(font)
        self.SetDefaultCellBackgroundColour(xpr.DEFAULT_EMPTY_BGR_CLR)
        self.SetLabelTextColour(xpr.TEXT_LAB_CLR)
        self.SetGridLineColour(xpr.GRID_LINE_CLR)
        self.SetLabelBackgroundColour(xpr.BOT_LAB_CLR)
    
    def GetColLabelRenderer(self, col):
        """ Возвращает текущий рендерер на колонку."""
        try:
            return self._colRenderers[col]
        except KeyError:
            return self._defColRenderer

    
def test(par=0):
    """ Test class CGridDatasetXP."""
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