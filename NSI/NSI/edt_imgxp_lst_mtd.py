#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Resource module <C:/defis/NSI/NSI/edt_imgxp_lst.mtd>.
"""
### RESOURCE_MODULE: C:/defis/NSI/NSI/edt_imgxp_lst.mtd
# -----------------------------------------------------------------------------
# Name:        C:/defis/NSI/NSI/edt_imgxp_lst_mtd.py
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
from ic.interfaces import icmanagerinterface

class ResObjectManager(icmanagerinterface.icWidgetManager):
    def Init(self):
        pass

manager_class = ResObjectManager