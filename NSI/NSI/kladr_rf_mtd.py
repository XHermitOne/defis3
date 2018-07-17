#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Resource module </home/xhermit/dev/prj/work/defis/NSI/NSI/kladr_rf.mtd>
File            </home/xhermit/dev/prj/work/defis/NSI/NSI/kladr_rf_mtd.py>
Description     <Resource module>
"""

### RESOURCE_MODULE: /home/xhermit/dev/prj/work/defis/NSI/NSI/kladr_rf.mtd

### ---- Import external modules -----
### RESOURCE_MODULE_IMPORTS

# from spravGridDlgStd_frm import *

#   Version
__version__ = (0, 0, 0, 1)
from ic.interfaces import icmanagerinterface


class icKLADRManager(icmanagerinterface.icWidgetManager):

    def onInit(self, evt):
        pass

    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK

manager_class = icKLADRManager
