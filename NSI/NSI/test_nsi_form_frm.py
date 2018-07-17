#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Resource module <C:/defis/NSI/NSI/test_nsi_form.frm>.
"""
### RESOURCE_MODULE: C:/defis/NSI/NSI/test_nsi_form.frm
# -----------------------------------------------------------------------------
# Name:        C:/defis/NSI/NSI/test_nsi_form_frm.py
# Purpose:     Resource module.
#
# Author:      <...>
#
# Created:
# RCS-ID:      $Id: $
# Copyright:   (c)
# Licence:     <your licence>
# -----------------------------------------------------------------------------
### ---- Import external modules -----
### RESOURCE_MODULE_IMPORTS

#   Version
__version__ = (0,0,0,1)
import ic
from ic.utils import coderror 
import wx

def test_urls():
    if ic.Login('admin', '', 'C:/defis/NSI/NSI/'):
        sprav = ic.metadata.NSI.mtd.nsi_sprav.create()
        try:
            print(sprav)
        except:
            print('Error!')
            
    ic.Logout()

def OnHelp(obj, evt):
    """ """
    print('Help Sprav')
    sprav = ic.metadata.NSI.mtd.nsi_sprav.create()
    result = sprav.NSITst.Hlp(parentForm=obj)
    val = result[1]
    #wx.MessageBox(str(result[1]))
    ctrl = obj.GetContext().GetObject('default_1047')
    if val:
        ctrl.SetValue(val)
    
if __name__ == '__main__':
    test_urls()


def fieldCtrl(obj, value, evt):
    sprav = ic.metadata.NSI.mtd.nsi_sprav.create()
    ret = sprav.NSITst.Ctrl(value, field='cod')
    print('*** CtrlSprav', value, ret)
    return ret