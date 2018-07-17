#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GridDataset Editor Resource Manager.
"""

import wx
from ic.interfaces import icedtresourcemanager
from ic.utils import util
from ic.utils import ic_uuid

_ = wx.GetTranslation

__version__ = (0, 0, 0, 2)


class ERMGridDataset(icedtresourcemanager.IEditorResourceManager):
    component_class = None
    
    @staticmethod
    def DeleteChild(res, child, *arg, **kwarg):
        if len(res['cols']) <= 1:
            wx.MessageBox(_('Invalid action. Number of column must be more or equal one'))
            return False
        return True
    
    @staticmethod
    def InitResource(res, *arg, **kwarg):
        if len(res['cols']) == 0:
            from ic.components import icgrid, icfont
            component = {}
            component['type'] = 'GridCell'
            spc = icgrid.SPC_IC_CELL
            util.icSpcDefStruct(icgrid.SPC_IC_CELL, component, True)
            util.icSpcDefStruct(icgrid.SPC_IC_CELLATTR, component['cell_attr'], True)
            util.icSpcDefStruct(icfont.SPC_IC_FONT, component['cell_attr']['font'], True)
            component['_uuid'] = ic_uuid.get_uuid()
            res['cols'].append(component)
            wx.MessageBox(_('Editor add default column to GridDataset'))
            
        return res
