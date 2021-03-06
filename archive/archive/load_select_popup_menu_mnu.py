#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль      </mnt/defis/defis3/archive/archive/load_select_popup_menu.mnu>
Файл        </mnt/defis/defis3/archive/archive/load_select_popup_menu_mnu.py>
Описание    <Resource module>
"""

import os
import os.path

from ic.interfaces import icmanagerinterface
from ic.log import log
# from ic.log import iclogbrowser
from ic.dlg import dlgfunc
from ic.dlg import std_dlg
from ic.utils import filefunc
from ic.utils import datefunc

import ic

from archive.convert import load_manager
from archive.convert import load_net_dbf
from archive.convert import load_net_config

### RESOURCE_MODULE: /mnt/defis/defis3/archive/archive/load_select_popup_menu.mnu

### ---- Import external modules -----
### RESOURCE_MODULE_IMPORTS

#   Version
__version__ = (0, 1, 5, 1)

DOC_FILE_TYPES = ('RLZ', 'ZTR', 'MTS', 'OSN', 'ARN')


class icLoadSelectPopupMenuManager(icmanagerinterface.icWidgetManager):

    def onInit(self, event):
        pass

    def setPackScanPanel(self, pack_scan_panel):
        """
        Установить панель пакетного сканирования.
        """
        log.debug(u'Установить панель пакетного сканирования.')
        self.pack_scan_panel = pack_scan_panel

    def onInitLoadMenu(self, event):
        """
        Инициализация меню.
        """
        if event:
            event.Skip()

    def choiceLoadFileName(self, sFileType, choice_year=None, choice_month=None):
        """
        Выбрать загружаемый файл.

        :param sFileType: Тип загружаемого файла.
        :param choice_year: Отфильтровать год.
        :param choice_year: Отфильтровать месяц.
        :return: Полное имя загружаемого файла или None, если нажата <отмена>.
        """
        load_doc_dir = ic.settings.archive.SETTINGS.load_doc_dir.get()
        # log.debug(u'Папка загрузки документов <%s>' % load_doc_dir)
        if load_doc_dir and os.path.exists(load_doc_dir):
            all_filenames = os.listdir(load_doc_dir)
            filenames = [filename for filename in all_filenames if filename.startswith(sFileType) and os.path.splitext(filename)[1].lower() == '.dbf']
            # log.debug(u'Список файлов %s' % str(filenames))
            if choice_year and not choice_month:
                filenames = [filename for filename in filenames if filename.endswith('_%d.DBF' % choice_year)]
                # log.debug(u'Список файлов за год %s' % str(filenames))
            elif choice_year and choice_month:
                filter_func = lambda filename: any([filename.endswith('%02d_%s_%d.DBF' % (choice_month, ext, choice_year)) for ext in load_net_config.DOWNLOAD_FILE_EXT_UPPER])
                filenames = [filename for filename in filenames if filter_func(filename)]
                # log.debug(u'Список файлов за месяц %s' % str(filenames))
            labels = [self.getLabelByDBFFilename(filename) for filename in filenames]

            #  Загрузка некоторых файлов может быть отключена через список надписей
            filenames = [None if labels[i] is None else filename for i, filename in enumerate(filenames)]
            filenames = [filename for filename in filenames if filename is not None]
            labels = [label for label in labels if label is not None]

            if filenames:
                filename_idx = dlgfunc.getSingleChoiceIdxDlg(None, u'ЗАГРУЗКА', u'Выберите файл загрузки', labels)
                if filename_idx >= 0:
                    filename = os.path.join(load_doc_dir, filenames[filename_idx])
                    log.info(u'Загрузка документа <%s>' % filename)
                    return filename
            else:
                dlgfunc.openErrBox(u'ЗАГРУЗКА', u'Файлы списка документов для загрузки не найдены!')
        return None

    def getLabelByDBFFilename(self, dbf_filename):
        """
        Определить надпись по имени загружаемого файла.
        """
        label = u''
        if dbf_filename.startswith('R'):
            warehouse = dbf_filename[2:5]
            label += u'Реализация. ' + (u'' if warehouse == '000' or not warehouse.isdigit() else u'Склад %d. ' % int(warehouse))
            prefix = self.getMonthLabel(dbf_filename)
        elif dbf_filename.startswith('Z'):
            label += u'Затраты. ' + self.getSchetLabel(dbf_filename) + u' '
            prefix = self.getMonthLabel(dbf_filename)
            log.debug(u'Затраты <%s>' % dbf_filename)
        elif dbf_filename.startswith('M'):
            warehouse = dbf_filename[2:5]
            label += u'Материалы. ' + (u'' if warehouse == '000' or not warehouse.isdigit() else u'Склад %d. ' % int(warehouse))
            prefix = self.getMonthLabel(dbf_filename)
        elif dbf_filename.startswith('O'):
            # label += u'Основные средства. '
            prefix = self.getOSNLabel(dbf_filename)
        elif dbf_filename.startswith('U'):
            label += u'Аренда. ' + self.getSchetLabel(dbf_filename) + u' '
            prefix = self.getQuartalLabel(dbf_filename)
        else:
            label += u'Не определенный участок. '

        file_ext = dbf_filename[8:11].upper()
        log.debug(u'Тип файла %s' % file_ext)
        # Участок материалы
        if dbf_filename.startswith('M') and dbf_filename[1:2].upper() == 'R' and file_ext == 'ASF':
            label += u'Продажа. СФ '
        elif dbf_filename.startswith('M') and dbf_filename[1:2].upper() == 'P' and file_ext == 'ASF':
            label += u'Покупка. СФ '
        elif dbf_filename.startswith('M') and dbf_filename[1:2].upper() == 'R' and file_ext == 'ATG':
            label += u'Продажа. ТОРГ12 '
        elif dbf_filename.startswith('M') and dbf_filename[1:2].upper() == 'P' and file_ext == 'ATG':
            label += u'Покупка. ТОРГ12 '
        # Участок ЗАТРАТЫ
        elif dbf_filename.startswith('Z') and dbf_filename[1:2].upper() == 'R' and file_ext == 'ASF':
            return None
        elif dbf_filename.startswith('Z') and dbf_filename[1:2].upper() == 'P' and file_ext == 'ASF':
            return None
        elif dbf_filename.startswith('Z') and dbf_filename[1:2].upper() == 'R' and file_ext == 'APX':
            return None
        elif dbf_filename.startswith('Z') and dbf_filename[1:2].upper() == 'P' and file_ext == 'APX':
            return None
        elif dbf_filename.startswith('Z') and dbf_filename[1:2].upper() == 'T' and file_ext == 'APX':
            return None
        elif dbf_filename.startswith('Z') and dbf_filename[1:2].upper() == 'R' and file_ext == 'ARH':
            # label += u'Продажа. Документы '
            return None
        elif dbf_filename.startswith('Z') and dbf_filename[1:2].upper() == 'P' and file_ext == 'ARH':
            # label += u'Покупка. Документы '
            return None
        elif dbf_filename.startswith('Z') and dbf_filename[1:2].upper() == 'O' and file_ext == 'ARH':
            label += u'Документы '
        # Участок АРЕНДА
        elif dbf_filename.startswith('U') and dbf_filename[1:2].upper() == 'R' and file_ext == 'ASF':
            label += u'Продажа. СФ '
        elif dbf_filename.startswith('U') and dbf_filename[1:2].upper() == 'P' and file_ext == 'ASF':
            label += u'Покупка. СФ '
        elif dbf_filename.startswith('U') and dbf_filename[1:2].upper() == 'O' and file_ext == 'APX':
            label += u'Документы '
        elif dbf_filename.startswith('U') and dbf_filename[1:2].upper() == 'P' and file_ext == 'APX':
           return None
        elif dbf_filename.startswith('U') and dbf_filename[1:2].upper() == 'R' and file_ext == 'APX':
           return None
        elif dbf_filename.startswith('U') and dbf_filename[1:2].upper() == 'R' and file_ext == 'ARH':
            label += u'Продажа. Документы '
        elif dbf_filename.startswith('U') and dbf_filename[1:2].upper() == 'P' and file_ext == 'ARH':
            label += u'Покупка. Документы '
        # Участок ОСНОВНЫЕ СРЕДСТВА
        elif dbf_filename.startswith('O') and dbf_filename[1:2].upper() == 'R' and file_ext == 'ASF':
            return None
        elif dbf_filename.startswith('O') and dbf_filename[1:2].upper() == 'P' and file_ext == 'ASF':
            return None
        elif dbf_filename.startswith('O') and dbf_filename[1:2].upper() == 'R' and file_ext == 'APX':
            return None
        elif dbf_filename.startswith('O') and dbf_filename[1:2].upper() == 'P' and file_ext == 'APX':
            return None
        elif dbf_filename.startswith('O') and file_ext == 'ATG':
            return None
        elif dbf_filename.startswith('O') and dbf_filename[1:2].upper() == 'R' and file_ext == 'ARH':
            # label += u'Продажа. Документы '
            pass
        elif dbf_filename.startswith('O') and dbf_filename[1:2].upper() == 'P' and file_ext == 'ARH':
            # label += u'Покупка. Документы '
            pass
        # Участок РЕАЛИЗАЦИЯ
        elif dbf_filename.startswith('R') and dbf_filename[1:2].upper() == 'U' and file_ext == 'ASF':
            label += u'Ремонт. СФ '
        elif dbf_filename.startswith('R') and dbf_filename[1:2].upper() == 'R' and file_ext == 'ASF':
            label += u'Продажа. СФ '
        elif dbf_filename.startswith('R') and dbf_filename[1:2].upper() == 'P' and file_ext == 'ASF':
            label += u'Покупка. СФ '
        elif dbf_filename.startswith('R') and dbf_filename[1:2].upper() == 'T' and file_ext == 'ATT':
            label += u'Продажа. ТТН '
        elif dbf_filename.startswith('R') and dbf_filename[1:2].upper() == 'R' and file_ext == 'ATG':
            label += u'Продажа. ТОРГ12 '
        elif dbf_filename.startswith('R') and dbf_filename[1:2].upper() == 'P' and file_ext == 'ATG':
            label += u'Покупка. ТОРГ12 '
        else:
            label += u'Документы '

        try:
            arch_year = os.path.splitext(dbf_filename)[0][-4:]
        except:
            arch_year = u'0000'
        label += u'%s %s год' % (prefix, arch_year)
        return label

    def getQuartalLabel(self, dbf_filename):
        """
        """
        label = u''

        # ... это квартал
        quartal = int(dbf_filename[5:7]) if dbf_filename[5:7].isdigit() else 0
        if quartal:
            label = u'за %d квартал' % quartal
        return label

    def getSchetLabel(self, dbf_filename):
        """
        Получить номер счета.
        """
        schet = dbf_filename[2:5]
        label = u''
        if schet == '761':
            label = u'Счет 76-01'
        elif schet == '766':
            label = u'Счет 76-06'
        elif schet == '762':
            label = u'Счет 76-12'
        return label

    def getMonthLabel(self, dbf_filename):
        """
        """
        # последние 2 цифры это месяц ...
        month = int(dbf_filename[5:7]) if dbf_filename[5:7].isdigit() else 0
        str_month = datefunc.MONTHS[month - 1] if 1 <= month <= 12 else u''
        label = u'за ' + str_month
        return label

    def getOSNLabel(self, dbf_filename):
        """
        """
        label = u''
        if not dbf_filename[2:5].isdigit() and dbf_filename.startswith('O'):
            # Это основные средства. Акты
            if dbf_filename[2:5].upper() == 'OC1':
                label += 'Акты приема-передачи '
            elif dbf_filename[2:5].upper() == 'OC3':
                label += 'Акты модернизации '
            elif dbf_filename[2:5].upper() == 'OC4':
                label += 'Акты списания '
            elif dbf_filename[2:5].upper() == 'OCA':
                label += 'Акты списания автотранспорта '
        quartal = int(dbf_filename[5:7]) if dbf_filename[5:7].isdigit() else 0
        if quartal:
            label += u'Документы за %d квартал' % quartal
        return label

    def getYearMonthDlg(self, bYear=True, bMonth=False):
        """
        Получить год или месяц.

        :param bYear: Определить дату как Год.
        :param bMonth: Определить дату как Год-Месяц.
        """
        arch_year = None
        arch_month = None
        if bMonth:
            arch_month = std_dlg.getMonthDlg()
            arch_year = arch_month.year if arch_month else None
            arch_month = arch_month.month if arch_month else None
        elif bYear:
            arch_year = std_dlg.getYearDlg()
            arch_year = arch_year.year if arch_year else None
        return arch_year, arch_month

    def getQuarterDlg(self):
        """
        Получить год или квартал.
        """
        arch_quarter = std_dlg.getQuarterDlg()
        arch_year = arch_quarter[0] if arch_quarter else None
        arch_quarter = arch_quarter[1] if arch_quarter else None
        return arch_year, arch_quarter

    def downloadArchiveDBF(self, arch_year, arch_month):
        """
        Произвести загрузку файлов архивных данных.

        :param bYear: Определить дату как Год.
        :param bMonth: Определить дату как Год-Месяц.
        :return: True - загрузка произведена, False - нажата <Отмена>.
        """
        # Удалить все ранее загруженные файлы
        dbf_filenames = filefunc.getFilenamesByExt(load_net_config.DEST_PATH, '.DBF')
        for dbf_filename in dbf_filenames:
            if not dbf_filename.endswith('SPRVENT.DBF') and not dbf_filename.endswith('ZPL.DBF'):
                filefunc.removeFile(dbf_filename)

        # Загрузить все данные за указанный год - месяц
        result = load_net_dbf.download_archive_files(arch_year, arch_month)
        if not result:
            dlgfunc.openWarningBox(u'ЗАГРУЗКА', u'Ошибка загрузки файлов данных архива')
        return result

    def onLoadRlzDocMenuItemSelected(self, event):
        """
        Выбор пункта меню загрузки документов реализации.
        """
        log.debug(u'Выбор пункта меню загрузки документов <Реализация>.')

        arch_year, arch_month = self.getYearMonthDlg(bYear=False, bMonth=True)
        if not arch_year:
            if event:
                event.Skip()
            return

        self.downloadArchiveDBF(arch_year, arch_month)
        filename = self.choiceLoadFileName('R', arch_year, arch_month)

        if filename:
            manager = load_manager.icDBFDocLoadManager(self.pack_scan_panel)
            manager.load_doc(filename, 'R')

        if event:
            event.Skip()

    def onLoadZtrDocMenuItemSelected(self, event):
        """
        Выбор пункта меню загрузки документов затрат на производство.
        """
        log.debug(u'Выбор пункта меню загрузки документов затрат на производство.')

        arch_year, arch_month = self.getYearMonthDlg(bYear=False, bMonth=True)
        if not arch_year:
            if event:
                event.Skip()
            return

        self.downloadArchiveDBF(arch_year, arch_month)
        filename = self.choiceLoadFileName('Z', arch_year, arch_month)

        if filename:
            manager = load_manager.icDBFDocLoadManager(self.pack_scan_panel)
            manager.load_doc(filename, 'Z')

        if event:
            event.Skip()

    def onLoadMtDocMenuItemSelected(self, event):
        """
        Выбор пункта меню загрузки документов <Материалы>.
        """
        log.debug(u'Выбор пункта меню загрузки документов <Материалы>.')

        arch_year, arch_month = self.getYearMonthDlg(bYear=False, bMonth=True)
        if not arch_year:
            if event:
                event.Skip()
            return

        self.downloadArchiveDBF(arch_year, arch_month)
        filename = self.choiceLoadFileName('M', arch_year, arch_month)

        if filename:
            manager = load_manager.icDBFDocLoadManager(self.pack_scan_panel)
            manager.load_doc(filename, 'M')

        if event:
            event.Skip()

    def onLoadOsDocMenuItemSelected(self, event):
        """
        Выбор пункта меню загрузки документов <Основные средства>.
        """
        log.debug(u'Выбор пункта меню загрузки документов <Основные средства>.')

        arch_year, arch_quarter = self.getQuarterDlg()
        if not arch_year:
            if event:
                event.Skip()
            return

        self.downloadArchiveDBF(arch_year, arch_quarter)
        filename = self.choiceLoadFileName('O', arch_year, arch_quarter)

        if filename:
            manager = load_manager.icDBFDocLoadManager(self.pack_scan_panel)
            manager.load_doc(filename, 'O')

        if event:
            event.Skip()

    def onLoadArnDocMenuItemSelected(self, event):
        """
        Выбор пункта меню загрузки документов <Аренда>.
        """
        log.debug(u'Выбор пункта меню загрузки документов <Аренда>.')

        arch_year, arch_quarter = self.getQuarterDlg()
        if not arch_year:
            if event:
                event.Skip()
            return

        self.downloadArchiveDBF(arch_year, arch_quarter)
        filename = self.choiceLoadFileName('U', arch_year, arch_quarter)

        if filename:
            manager = load_manager.icDBFDocLoadManager(self.pack_scan_panel)
            manager.load_doc(filename, 'U')

        if event:
            event.Skip()

    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK

manager_class = icLoadSelectPopupMenuManager
