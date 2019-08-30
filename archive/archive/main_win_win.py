#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resource module </mnt/defis/defis3/archive/archive/main_win.win>
File            </mnt/defis/defis3/archive/archive/main_win_win.py>
Description     <Resource module>
"""

import ic
from ic.dlg import dlgfunc
from ic.utils import system
from ic.interfaces import icmanagerinterface
from archive.forms import print_doc_form

from archive.convert import import_sprvent
from archive import valid_catalog

### RESOURCE_MODULE: /mnt/defis/defis3/archive/archive/main_win.win

### ---- Import external modules -----
### RESOURCE_MODULE_IMPORTS

#   Version
__version__ = (0, 1, 1, 2)


class icMainWinManager(icmanagerinterface.icWidgetManager):

    def onInit(self, event):
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
        result = dlgfunc.openAskBox(u'ВЫХОД', u'Закрыть приложение?')
        if event:
            event.Skip()
        return result

    def init_app(self):
        """
        Функция инициализации приложения/главного окна.
        """
        # Проверка наличия уже запущенной копии программы
        if system.getActiveProcessCount('archivarius') > 1:
            dlgfunc.openWarningBox(u'ВНИМАНИЕ', u'Уже запущена одна копия программы')
            ic.closeAppForce()
            return
            
        # Перед началом работы проверить наличие примонтированной папки каталога
        # Если папка пустая, то дальнейшая работа безсмыслена
        if not valid_catalog.validZipDocCatalog():
            zipdoc_dir = ic.settings.archive.SETTINGS.zipdoc_dir.get()
            msg = u'Не подключен каталог документов <%s>. Дальнейшая работа не возможна' % zipdoc_dir
            dlgfunc.openErrBox(u'ОШИБКА', msg)
            ic.closeAppForce()
            return
        else:
            import_sprvent.import_sprvent()
    
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK

manager_class = icMainWinManager
