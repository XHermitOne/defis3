#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль      </mnt/defis/defis3/analiticIC/analiticIC/monitor_menubar.mnu>
Файл        </mnt/defis/defis3/analiticIC/analiticIC/monitor_menubar_mnu.py>
Описание    <Resource module>
"""

from ic.components import icResourceParser
from ic.interfaces import icmanagerinterface

from analitic import monitoring

### RESOURCE_MODULE: /mnt/defis/defis3/analiticIC/analiticIC/monitor_menubar.mnu

### ---- Import external modules -----
### RESOURCE_MODULE_IMPORTS

#   Version
__version__ = (0, 0, 0, 1)


class icMonitorMenubarManager(icmanagerinterface.icWidgetManager):

    def onInit(self, event):
        pass

    def onCompareAnalizeMenuItemSelected(self, event):
        """
        Обработчик пункта меню <Сравнительный анализ>.
        """
        icResourceParser.ModalForm('form1')

        if event:
            event.Skip()

    def onViewMonitorMenuItemSelected(self, event):
        """
        Обработчик пункта меню <Панель индикаторов>.
        """
        monitoring.showTextMonitorBrowser()

        if event:
            event.Skip()

    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK

manager_class = icMonitorMenubarManager
