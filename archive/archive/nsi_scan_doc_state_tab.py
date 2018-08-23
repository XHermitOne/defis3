#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resource module </mnt/defis/defis3/archive/archive/nsi_scan_doc_state.tab>
File            </mnt/defis/defis3/archive/archive/nsi_scan_doc_state_tab.py>
Description     <Resource module>
"""

import copy
from ic.interfaces import icmanagerinterface

### RESOURCE_MODULE: /mnt/defis/defis3/archive/archive/nsi_scan_doc_state.tab

### ---- Import external modules -----
### RESOURCE_MODULE_IMPORTS

#   Version
__version__ = (0, 0, 0, 1)


DEFAULT_TAB_DATA = (dict(cod='00', name=u'Документ создан', s1='create'),
                    dict(cod='10', name=u'Документ опубликован', s1='public'),
                    )


class icNSIScanDocStateTabManager(icmanagerinterface.icWidgetManager):
    """
    Менеджер таблицы состояния архивного документа.
    """

    def onInit(self, evt):
        pass

    def set_default_data(self):
        """
        Установка значений справочника по умолчанию.
        """
        tab = self.get_object()
        
        # Очистить таблицу
        tab.clear()
        
        for record in DEFAULT_TAB_DATA:
            record['type'] = 'nsi_scan_doc_state'
            tab.add(**record)            

    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK

manager_class = icNSIScanDocStateTabManager
