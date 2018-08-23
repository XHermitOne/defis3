#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resource module </mnt/defis/defis/archive/archive/import_select_popup_menu.mnu>
File            </mnt/defis/defis/archive/archive/import_select_popup_menu_mnu.py>
Description     <Resource module>
"""

import datetime
from ic.interfaces import icmanagerinterface
from ic.log import log
from ic.log import iclogbrowser
from ic.dlg import ic_dlg

from archive.convert import rlz_imp_manager
from archive.convert import ztr_imp_manager
from archive.convert import mt_imp_manager
from archive.convert import osn_imp_manager


### RESOURCE_MODULE: /mnt/defis/defis/archive/archive/import_select_popup_menu.mnu

### ---- Import external modules -----
### RESOURCE_MODULE_IMPORTS

#   Version
__version__ = (0, 0, 2, 1)


class icImportSelectPopupMenuManager(icmanagerinterface.icWidgetManager):

    def onInit(self, evt):
        pass

    def setPackScanPanel(self, pack_scan_panel):
        """
        Установить панель пакетного сканирования.
        """
        log.debug(u'Установить панель пакетного сканирования.')
        self.pack_scan_panel = pack_scan_panel

    def onImportRlzDocMenuItemSelected(self, event):
        """
        Выбор пункта меню импорта документов реализации.
        """
        log.debug(u'Выбор пункта меню импорта документов <Реализация>.')

        imp_manager = rlz_imp_manager.icRealizImportManager(self.pack_scan_panel)
        imp_manager.init()
        imp_manager.import_docs()

        if event:
            event.Skip()

    def onImportZtrDocMenuItemSelected(self, event):
        """
        Выбор пункта меню импорта документов затрат на производство.
        """
        log.debug(u'Выбор пункта меню импорта документов затрат на производство.')

        imp_manager = ztr_imp_manager.icZatratyImportManager(self.pack_scan_panel)
        imp_manager.init()
        imp_manager.import_docs()
        
        if event:
            event.Skip()
            
    def onImportMtDocMenuItemSelected(self, event):
        """
        Выбор пункта меню импорта документов <Материалы>.
        """
        log.debug(u'Выбор пункта меню импорта документов <Материалы>.')

        imp_manager = mt_imp_manager.icMaterialImportManager(self.pack_scan_panel)
        imp_manager.init()
        imp_manager.import_docs()

        if event:
            event.Skip()

    def onImportOsDocMenuItemSelected(self, event):
        """
        Выбор пункта меню импорта документов <Основные средства>.
        """
        log.debug(u'Выбор пункта меню импорта документов <Основные средства>.')

        imp_manager = osn_imp_manager.icOsnovnImportManager(self.pack_scan_panel)
        imp_manager.init()
        imp_manager.import_docs()

        if event:
            event.Skip()

    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK

manager_class = icImportSelectPopupMenuManager
