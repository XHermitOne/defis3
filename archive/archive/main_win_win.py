#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Resource module </mnt/defis/defis/ayan_archive/ayan_archive/main_win.win>
File            </mnt/defis/defis/ayan_archive/ayan_archive/main_win_win.py>
Description     <Resource module>
"""

import ic
from ic.dlg import ic_dlg
from ic.utils import system
from ic.interfaces import icmanagerinterface
from ayan_archive.forms import print_doc_form

from ayan_archive.convert import import_sprvent
from ayan_archive import valid_catalog

### RESOURCE_MODULE: /mnt/defis/defis/ayan_archive/ayan_archive/main_win.win

### ---- Import external modules -----
### RESOURCE_MODULE_IMPORTS

#   Version
__version__ = (0, 0, 1, 2)


class icMainWinManager(icmanagerinterface.icWidgetManager):

    def onInit(self, evt):
        pass

    def onOpen(self, event):
        """
        Открытие главногое окна.
        """
        print_doc_form.open_print_search_doc_page(self.get_object())

        if event:
            event.Skip()

    def onClose(self, event):
        """
        Закрытие главногое окна.
        """
        result = ic_dlg.icAskBox(u'ВЫХОД', u'Закрыть приложение?')
        if event:
            event.Skip()
        return result

    def init_app(self):
        """
        Функция инициализации приложения/главного окна.
        """
        # Проверка наличия уже запущенной копии программы
        if system.getActiveProcessCount('defis/ayan_archive/run.py') > 1:
            ic_dlg.icWarningBox(u'ВНИМАНИЕ', u'Уже запущена одна копия программы')
            ic.closeAppForce()
            return
            
        # Перед началом работы проверить наличие примонтированной папки каталога
        # Если папка пустая, то дальнейшая работа безсмыслена
        if not valid_catalog.validZipDocCatalog():
            zipdoc_dir = ic.settings.ayan_archive.SETTINGS.zipdoc_dir.get()
            msg = u'Не подключен каталог документов <%s>. Дальнейшая работа не возможна' % zipdoc_dir
            ic_dlg.icErrBox(u'ОШИБКА', msg)
            ic.closeAppForce()
            return
        else:
            import_sprvent.import_sprvent()
    
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK

manager_class = icMainWinManager
