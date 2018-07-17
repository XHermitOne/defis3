#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Resource module </mnt/samba/defis/SCADA/SCADA/test_menubar.mnu>
File            </mnt/samba/defis/SCADA/SCADA/test_menubar_mnu.py>
Description     <Resource module>
"""

import ic
from ic.interfaces import icmanagerinterface

### RESOURCE_MODULE: /mnt/samba/defis/SCADA/SCADA/test_menubar.mnu

### ---- Import external modules -----
### RESOURCE_MODULE_IMPORTS

#   Version
__version__ = (0, 0, 0, 2)


class icTestMenubarManager(icmanagerinterface.icWidgetManager):

    def onInit(self, evt):
        pass

    ###BEGIN EVENT BLOCK
    
    def onTestMenuItemSelect(self, event):
        """
        Обработчик выбора пункта меню.
        """
        obj = ic.metadata.THIS.frm.test_form.create()
        if obj:
            obj.Show()
        
        event.Skip()
        
    ###END EVENT BLOCK

manager_class = icTestMenubarManager
