#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Resource module </mnt/samba/defis/WMS/WMS/main_menu.mnu>
File            </mnt/samba/defis/WMS/WMS/main_menu_mnu.py>
Description     <Resource module>
"""

### RESOURCE_MODULE: /mnt/samba/defis/WMS/WMS/main_menu.mnu

### ---- Import external modules -----
### RESOURCE_MODULE_IMPORTS

#   Version
__version__ = (0, 0, 0, 1)
from ic.interfaces import icmanagerinterface
from .wms_constructor import truck_constructor_panel


class icMainMenuBarManager(icmanagerinterface.icWidgetManager):

    def onInit(self, evt):
        pass

    ###BEGIN EVENT BLOCK
    
    def onTestMenuItemSelected(self, event):
        """
        """
        print('<Test constructor>')
        truck_constructor_panel.test_defis()        
        
    ###END EVENT BLOCK

manager_class = icMainMenuBarManager
