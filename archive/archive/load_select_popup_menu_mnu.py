#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль      </mnt/defis/defis3/archive/archive/load_select_popup_menu.mnu>
Файл        </mnt/defis/defis3/archive/archive/load_select_popup_menu_mnu.py>
Описание    <Resource module>
"""

import os
import os.path
import fnmatch

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
__version__ = (0, 1, 7, 2)

DOC_FILE_TYPES = ('RLZ', 'ZTR', 'MTS', 'OSN', 'ARN', 'USL')


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

    def choiceLoadFileName(self, file_masks, choice_year=None, choice_month=None):
        """
        Выбрать загружаемый файл.

        :param file_masks: Маски загружаемого файла.
        :param choice_year: Отфильтровать год.
        :param choice_year: Отфильтровать месяц.
        :return: Полное имя загружаемого файла или None, если нажата <отмена>.
        """
        load_doc_dir = ic.settings.archive.SETTINGS.load_doc_dir.get()
        # log.debug(u'Папка загрузки документов <%s>' % load_doc_dir)
        if load_doc_dir and os.path.exists(load_doc_dir):
            all_filenames = os.listdir(load_doc_dir)
            
            if isinstance(file_masks, str):
                filenames = fnmatch.filter(all_filenames, file_masks)
            elif isinstance(file_masks, (list, tuple)):
                filenames = []
                for file_mask in file_masks:
                    filenames += fnmatch.filter(all_filenames, file_mask)
            log.debug(u'Список обрабатываемых файлов %s' % str(filenames))
                    
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
        file_ext = dbf_filename[8:11].upper()
        log.debug(u'Тип файла %s' % file_ext)

        label = u''
        if fnmatch.fnmatch(dbf_filename, load_net_config.REALIZ_FILE_MASKS):
            # Участок РЕАЛИЗАЦИЯ
            warehouse = dbf_filename[2:5]
            label += u'Реализация. ' + (u'' if warehouse == '000' or not warehouse.isdigit() else u'Склад %d. ' % int(warehouse))
            prefix = self.getMonthLabel(dbf_filename)
            if dbf_filename[1:2].upper() == 'U' and file_ext == 'ASF':
                label += u'Ремонт. СФ '
            elif dbf_filename[1:2].upper() == 'R' and file_ext == 'ASF':
                label += u'Продажа. СФ '
            elif dbf_filename[1:2].upper() == 'P' and file_ext == 'ASF':
                label += u'Покупка. СФ '
            elif dbf_filename[1:2].upper() == 'T' and file_ext == 'ATT':
                label += u'Продажа. ТТН '
            elif dbf_filename[1:2].upper() == 'R' and file_ext == 'ATG':
                label += u'Продажа. ТОРГ12 '
            elif dbf_filename[1:2].upper() == 'P' and file_ext == 'ATG':
                label += u'Покупка. ТОРГ12 '
            elif dbf_filename[1:2].upper() == 'R' and file_ext == 'UP2':
                label += u'Продажа. УПД2. '
            elif dbf_filename[1:2].upper() == 'P' and file_ext == 'UP2':
                label += u'Покупка. УПД2. '
            else:
                label += u'Документы '
            
        elif any([fnmatch.fnmatch(dbf_filename, file_mask) for file_mask in load_net_config.ZATRATY_FILE_MASKS]):
            # Участок ЗАТРАТЫ/Акцептованные счета
            label += u'Услуги. ' + self.getSchetLabel(dbf_filename) + u' '
            prefix = self.getQuartalLabel(dbf_filename)
            log.debug(u'Затраты <%s>' % dbf_filename)
            if dbf_filename[1:2].upper() == 'R' and file_ext == 'ASF':
                label += u'Продажа. СФ '
            elif dbf_filename[1:2].upper() == 'P' and file_ext == 'ASF':
                label += u'Покупка. СФ '
            elif dbf_filename[1:2].upper() == 'O' and file_ext == 'ASF':
                label += u'Счет-фактуры '
            elif dbf_filename[1:2].upper() == 'O' and file_ext in ('AКТ', 'AKT'):
                label += u'Акты '
            elif dbf_filename[1:2].upper() == 'P' and file_ext in ('AКТ', 'AKT'):
                label += u'Покупка. Акты '
            elif dbf_filename[1:2].upper() == 'R' and file_ext in ('AКТ', 'AKT'):
                label += u'Продажа. Акты '
            elif dbf_filename[1:2].upper() == 'R' and file_ext == 'ARH':
                # label += u'Продажа. Документы '
                return None
            elif dbf_filename[1:2].upper() == 'P' and file_ext == 'ARH':
                # label += u'Покупка. Документы '
                return None
            elif dbf_filename[1:2].upper() == 'O' and file_ext == 'ARH':
                label += u'Документы '
            elif file_ext == 'ARX':
                return None

        elif fnmatch.fnmatch(dbf_filename, load_net_config.MATERIAL_FILE_MASKS):
            # Участок материалы
            warehouse = dbf_filename[2:5]
            label += u'Материалы. ' + (u'' if warehouse == '000' or not warehouse.isdigit() else u'Склад %d. ' % int(warehouse))
            prefix = self.getMonthLabel(dbf_filename)
            if dbf_filename[1:2].upper() == 'R' and file_ext == 'ASF':
                label += u'Продажа. СФ '
            elif dbf_filename[1:2].upper() == 'P' and file_ext == 'ASF':
                label += u'Покупка. СФ '
            elif dbf_filename[1:2].upper() == 'R' and file_ext == 'ATG':
                label += u'Продажа. ТОРГ12 '
            elif dbf_filename[1:2].upper() == 'P' and file_ext == 'ATG':
                label += u'Покупка. ТОРГ12 '
            
        elif fnmatch.fnmatch(dbf_filename, load_net_config.OSN_FILE_MASK):
            # Участок ОСНОВНЫЕ СРЕДСТВА
            # label += u'Основные средства. '
            prefix = self.getOSNLabel(dbf_filename)
            if dbf_filename[1:2].upper() == 'R' and file_ext == 'ASF':
                label += u'Продажа. СФ. '
            elif dbf_filename[1:2].upper() == 'P' and file_ext == 'ASF':
                label += u'Покупка. СФ. '
            elif dbf_filename[1:2].upper() == 'R' and file_ext == 'ATG':
                label += u'Продажа. Документы. '
            elif dbf_filename[1:2].upper() == 'P' and file_ext == 'ATG':
                label += u'Покупка. Документы. '
            elif dbf_filename[1:2].upper() == 'R' and file_ext == 'APX':
                return None
            elif dbf_filename[1:2].upper() == 'P' and file_ext == 'APX':
                return None
            elif dbf_filename[1:2].upper() == 'R' and file_ext == 'ARH':
                # label += u'Продажа. Документы '
                pass
            elif dbf_filename[1:2].upper() == 'P' and file_ext == 'ARH':
                # label += u'Покупка. Документы '
                pass
            
        elif fnmatch.fnmatch(dbf_filename, load_net_config.AREND_FILE_MASKS):
            # Участок АРЕНДА
            label += u'Аренда. ' + self.getSchetLabel(dbf_filename) + u' '
            prefix = self.getQuartalLabel(dbf_filename)
            if dbf_filename[1:2].upper() == 'R' and file_ext == 'ASF':
                label += u'Продажа. СФ '
            elif dbf_filename[1:2].upper() == 'P' and file_ext == 'ASF':
                label += u'Покупка. СФ '
            elif dbf_filename[1:2].upper() == 'O' and file_ext == 'ASF':
                label += u'Счет-фактуры '
            elif dbf_filename[1:2].upper() == 'O' and file_ext == 'ARX':
                label += u'Документы '
            elif dbf_filename[1:2].upper() == 'O' and file_ext == 'AКТ':
                label += u'Акты '
            elif dbf_filename[1:2].upper() == 'P' and file_ext == 'AКТ':
                label += u'Продажа. Акты '
            elif dbf_filename[1:2].upper() == 'R' and file_ext == 'AКТ':
                label += u'Покупка. Акты '
            elif dbf_filename[1:2].upper() == 'R' and file_ext == 'ARH':
                label += u'Продажа. Документы '
            elif dbf_filename[1:2].upper() == 'P' and file_ext == 'ARH':
                label += u'Покупка. Документы '
            elif dbf_filename[1:2].upper() == 'O' and file_ext == 'ARH':
                label += u'Документы '
            
        elif any([fnmatch.fnmatch(dbf_filename, file_mask) for file_mask in load_net_config.USLUGI_FILE_MASKS]):
            label += u'Услуги. ' + self.getSchetLabel(dbf_filename) + u' '
            prefix = self.getQuartalLabel(dbf_filename)
            if dbf_filename[1:2].upper() == 'R' and file_ext == 'ASF':
                label += u'Продажа. СФ '
            elif dbf_filename[1:2].upper() == 'P' and file_ext == 'ASF':
                label += u'Покупка. СФ '
            elif dbf_filename[1:2].upper() == 'O' and file_ext == 'ASF':
                label += u'Счет-фактуры '
            elif dbf_filename[1:2].upper() == 'O' and file_ext == 'ARX':
                label += u'Документы '
            elif dbf_filename[1:2].upper() == 'O' and file_ext in ('AКТ', 'AKT'):
                label += u'Акты '
            elif dbf_filename[1:2].upper() == 'P' and file_ext in ('AКТ', 'AKT'):
                label += u'Покупка. Акты '
            elif dbf_filename[1:2].upper() == 'R' and file_ext in ('AКТ', 'AKT'):
                label += u'Продажа. Акты '
            elif dbf_filename[1:2].upper() == 'R' and file_ext == 'ARH':
                label += u'Продажа. Документы '
            elif dbf_filename[1:2].upper() == 'P' and file_ext == 'ARH':
                label += u'Покупка. Документы '
            elif dbf_filename[1:2].upper() == 'O' and file_ext == 'ARH':
                label += u'Документы '
            else:
                log.warning(u'Ошика определения типа файла <%s : %s>' % (dbf_filename, file_ext))

        elif any([fnmatch.fnmatch(dbf_filename, file_mask) for file_mask in load_net_config.USLUGI7603_FILE_MASKS]):
            label += u'Услуги. ' + self.getSchetLabel(dbf_filename) + u' '
            prefix = self.getQuartalLabel(dbf_filename)
            if dbf_filename[1:2].upper() == 'R' and file_ext == 'ASF':
                label += u'Продажа. СФ '
            elif dbf_filename[1:2].upper() == 'P' and file_ext == 'ASF':
                label += u'Покупка. СФ '
            elif dbf_filename[1:2].upper() == 'O' and file_ext == 'ASF':
                label += u'Счет-фактуры '
            elif dbf_filename[1:2].upper() == 'O' and file_ext == 'ARX':
                label += u'Документы '
            elif dbf_filename[1:2].upper() == 'O' and file_ext in ('AКТ', 'AKT'):
                label += u'Акты '
            elif dbf_filename[1:2].upper() == 'P' and file_ext in ('AКТ', 'AKT'):
                label += u'Покупка. Акты '
            elif dbf_filename[1:2].upper() == 'R' and file_ext in ('AКТ', 'AKT'):
                label += u'Продажа. Акты '
            elif dbf_filename[1:2].upper() == 'R' and file_ext == 'ARH':
                label += u'Продажа. Документы '
            elif dbf_filename[1:2].upper() == 'P' and file_ext == 'ARH':
                label += u'Покупка. Документы '
            elif dbf_filename[1:2].upper() == 'O' and file_ext == 'ARH':
                label += u'Документы '
            else:
                log.warning(u'Ошибка определения типа файла <%s : %s>' % (dbf_filename, file_ext))
            
        else:
            label += u'Не определенный участок. '

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
        elif schet == '769':
            label = u'Счет 76-05.3'
        elif schet == '762':
            label = u'Счет 76-12'
        elif schet == '767':
            label = u'Счет 76-05.1'
        elif schet == '768':
            label = u'Счет 76-05.2'
        elif schet == '000':
            label = u'Прочие'
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
        if dbf_filename[1:2] == 'P':
            label += u'. Покупка. '
        elif dbf_filename[1:2] == 'R':
            label += u'. Продажа. '
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

    def downloadArchiveDBF(self, arch_year, arch_month, from_1c=False):
        """
        Произвести загрузку файлов архивных данных.

        :param bYear: Определить дату как Год.
        :param bMonth: Определить дату как Год-Месяц.
        :param from_1c: Загрузка DBF из 1С?
        :return: True - загрузка произведена, False - нажата <Отмена>.
        """
        # Удалить все ранее загруженные файлы
        dbf_filenames = filefunc.getFilenamesByExt(load_net_config.DEST_PATH, '.DBF')
        for dbf_filename in dbf_filenames:
            if not dbf_filename.endswith('SPRVENT.DBF') and not dbf_filename.endswith('ZPL.DBF'):
                filefunc.removeFile(dbf_filename)

        # Загрузить все данные за указанный год - месяц
        urls_fmt = load_net_config.ARCH_1C_SMB_URLS_FMT if from_1c else load_net_config.ARCH_SMB_URLS_FMT
        result = load_net_dbf.download_archive_files(arch_year, arch_month, urls_fmt=urls_fmt)
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

        from_1c = dlgfunc.openAskBox(u'ЗАГРУЗКА', u'Загрузить данные из 1С?')
        self.downloadArchiveDBF(arch_year, arch_month, from_1c=from_1c)
        filename = self.choiceLoadFileName(load_net_config.REALIZ_FILE_MASKS, arch_year, arch_month)

        if filename:
            manager = load_manager.icDBFDocLoadManager(self.pack_scan_panel)
            manager.load_doc(filename, 'R', from_1c=False)

        if event:
            event.Skip()

    def onLoadZtrDocMenuItemSelected(self, event):
        """
        Выбор пункта меню загрузки документов затрат на производство.
        """
        log.debug(u'Выбор пункта меню загрузки документов затрат на производство.')

        arch_year, arch_quarter = self.getQuarterDlg()
        if not arch_year:
            if event:
                event.Skip()
            return

        from_1c = dlgfunc.openAskBox(u'ЗАГРУЗКА', u'Загрузить данные из 1С?')
        self.downloadArchiveDBF(arch_year, arch_quarter, from_1c=from_1c)
        filename = self.choiceLoadFileName(load_net_config.ZATRATY_FILE_MASKS, arch_year, arch_quarter)

        if filename:
            manager = load_manager.icDBFDocLoadManager(self.pack_scan_panel)
            manager.load_doc(filename, 'Z', from_1c=from_1c)

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

        from_1c = dlgfunc.openAskBox(u'ЗАГРУЗКА', u'Загрузить данные из 1С?')
        self.downloadArchiveDBF(arch_year, arch_month, from_1c=from_1c)
        filename = self.choiceLoadFileName(load_net_config.MATERIAL_FILE_MASKS, arch_year, arch_month)

        if filename:
            manager = load_manager.icDBFDocLoadManager(self.pack_scan_panel)
            manager.load_doc(filename, 'M', from_1c=from_1c)

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

        from_1c = dlgfunc.openAskBox(u'ЗАГРУЗКА', u'Загрузить данные из 1С?')
        self.downloadArchiveDBF(arch_year, arch_quarter, from_1c=from_1c)
        filename = self.choiceLoadFileName(load_net_config.OSN_FILE_MASK, arch_year, arch_quarter)

        if filename:
            manager = load_manager.icDBFDocLoadManager(self.pack_scan_panel)
            manager.load_doc(filename, 'O', from_1c=from_1c)

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

        from_1c = dlgfunc.openAskBox(u'ЗАГРУЗКА', u'Загрузить данные из 1С?')
        self.downloadArchiveDBF(arch_year, arch_quarter, from_1c=from_1c)
        filename = self.choiceLoadFileName(load_net_config.AREND_FILE_MASKS, arch_year, arch_quarter)

        if filename:
            manager = load_manager.icDBFDocLoadManager(self.pack_scan_panel)
            manager.load_doc(filename, 'A', from_1c=from_1c)

        if event:
            event.Skip()

    def onLoadUslDocMenuItemSelected(self, event):
        """
        Выбор пункта меню загрузки документов <Услуги>.
        """
        log.debug(u'Выбор пункта меню загрузки документов <Услуги>.')

        arch_year, arch_quarter = self.getQuarterDlg()
        if not arch_year:
            if event:
                event.Skip()
            return

        from_1c = dlgfunc.openAskBox(u'ЗАГРУЗКА', u'Загрузить данные из 1С?')
        self.downloadArchiveDBF(arch_year, arch_quarter, from_1c=from_1c)
        filename = self.choiceLoadFileName(load_net_config.USLUGI_FILE_MASKS, arch_year, arch_quarter)

        if filename:
            manager = load_manager.icDBFDocLoadManager(self.pack_scan_panel)
            manager.load_doc(filename, 'U', from_1c=from_1c)

        if event:
            event.Skip()

    def onLoadUsl7603DocMenuItemSelected(self, event):
        """
        Выбор пункта меню загрузки документов <Услуги. 76-03>.
        """
        log.debug(u'Выбор пункта меню загрузки документов <Услуги. 76-03>.')

        arch_year, arch_quarter = self.getQuarterDlg()
        if not arch_year:
            if event:
                event.Skip()
            return

        from_1c = dlgfunc.openAskBox(u'ЗАГРУЗКА', u'Загрузить данные из 1С?')
        self.downloadArchiveDBF(arch_year, arch_quarter, from_1c=from_1c)
        filename = self.choiceLoadFileName(load_net_config.USLUGI7603_FILE_MASKS, arch_year, arch_quarter)

        if filename:
            manager = load_manager.icDBFDocLoadManager(self.pack_scan_panel)
            manager.load_doc(filename, 'U', from_1c=from_1c)

        if event:
            event.Skip()

    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK

manager_class = icLoadSelectPopupMenuManager
