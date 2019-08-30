#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resource module </mnt/defis/defis3/archive/archive/doc_cataloger.mtd>
File            </mnt/defis/defis3/archive/archive/doc_cataloger_mtd.py>
Description     <Resource module>
"""

from ic.interfaces import icmanagerinterface

### RESOURCE_MODULE: /mnt/defis/defis3/archive/archive/doc_cataloger.mtd

### ---- Import external modules -----
### RESOURCE_MODULE_IMPORTS

#   Version
__version__ = (0, 0, 0, 1)


class ResObjectManager(icmanagerinterface.icWidgetManager):

    def onInit(self, event):
        pass

    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK

manager_class = ResObjectManager
