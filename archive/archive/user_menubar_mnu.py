#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Resource module </mnt/defis/defis/ayan_archive/ayan_archive/user_menubar.mnu>
File            </mnt/defis/defis/ayan_archive/ayan_archive/user_menubar_mnu.py>
Description     <Resource module>
"""

import os
import os.path 
import sqlalchemy

import ic
from ayan_archive import admin_menubar_mnu
# from ic.interfaces import icmanagerinterface
from ayan_archive.forms import new_doc_panel
from ayan_archive.forms import search_doc_form
from ayan_archive.forms import print_doc_form
from ic.dlg import about_box
from ic.utils import datefunc
from ic.utils import ic_file
from ic.dlg import std_dlg
from ic.dlg import ic_dlg
from ic.log import log

### RESOURCE_MODULE: /mnt/defis/defis/ayan_archive/ayan_archive/user_menubar.mnu

### ---- Import external modules -----
### RESOURCE_MODULE_IMPORTS

#   Version
__version__ = (0, 0, 2, 2)


class icUserMenuBarManager(admin_menubar_mnu.icAdminMenuBarManager):

    def onInit(self, evt):
        pass

    ###BEGIN EVENT BLOCK

    def onNewDocMenuItemSelected(self, event):
        """
        Обработчик выбора меню <Новый документ>
        """
        main_win = ic.getMainWin()
        page = new_doc_panel.icNewArchiveDocPanel(parent = main_win)
        page.init()
        main_win.AddOrgPage(page, u'Регистрация новых документов')
        event.Skip()

    def onSearchDocMenuItemSelected(self, event):
        """
        Поиск документов.
        """
        main_win = ic.getMainWin()
        # page = search_doc_form.icSearchDocPanel(parent=main_win)
        page = print_doc_form.icPrintDocPanel(parent=main_win)
        main_win.AddOrgPage(page, u'Поиск документов')

        event.Skip()

    def onAboutMenuItemSelected(self, event):
        """
        Окно о программе.
        """
        about_box.showAbout()

    def onDateRangeReportMenuItemSelected(self, event):
        """
        Список документов за период.
        """
        rep_manager = ic.getReportManager()
        rep_manager.post_select_action('doc_ext/daterange_document_list.ods')

    def onClearPackDocMenuItemSelected(self, event):
        """
        Очистка пакетной обработка отсканированных документов за месяц.
        """
        first_day_of_month = std_dlg.getMonthDlg(ic.getMainWin())
        if first_day_of_month is None:
            # Нажата отмена
            event.Skip()
            return
        
        last_day = datefunc.get_last_day_of_month(year=first_day_of_month.year,
                                                  month=first_day_of_month.month)

        # Удалить файлы
        dst_path = os.path.join(ic_file.getRootProjectDir(), 'db', 
                                str(first_day_of_month.year))
        
        str_month = '%X' % first_day_of_month.month
        del_path = os.path.join(dst_path, 'FDOC')
        file_masks = ('R0*.DBF', 'R0*.DCM',
                      'R%s*.DBF' % str_month, 'R%s*.DCM' % str_month,
                      'TI%s*.DBF' % str_month, 'TI%s*.DCM' % str_month, 
                      'TO%s*.DBF' % str_month, 'TO%s*.DCM' % str_month)
        ic_file.delAllFilesFilter(del_path, *file_masks)

        del_path = os.path.join(dst_path, 'FDSB')
        file_masks = ('SB%s111.DBF' % str_month, 'SB%s111.DCB' % str_month,
                      'SB%s111.DSB' % str_month, 'SB%s111S.DBF' % str_month)
        ic_file.delAllFilesFilter(del_path, *file_masks)
        
        # Удалить записи из таблицы пакетной обработки
        doc = ic.metadata.ayan_archive.mtd.scan_document_pack.create()
        tab = doc.getTable()
        
        msg = u'Удаление пакета документов с <%s> по <%s>' % (str(first_day_of_month), str(last_day))
        log.debug(u'Удаление пакета документов с <%s> по <%s>' % (str(first_day_of_month), str(last_day)))
        tab.del_where(tab.c.doc_date.between(first_day_of_month, last_day))        
        
        ic_dlg.icMsgBox(u'УДАЛЕНИЕ', msg+u' успешно завершено')
        event.Skip()
        
    def onClearZtrDocsMenuItemSelected(self, event):
        """
        ЗАТРАТЫ. Удаление данных пакетной обработки за год.
        """
        clear_year = std_dlg.getYearDlg(ic.getMainWin())
        if clear_year is None:
            # Нажата отмена
            event.Skip()
            return
        
        # Удалить файлы
        dst_path = os.path.join(ic_file.getRootProjectDir(), 'db', 
                                str(clear_year.year))
        
        del_path = os.path.join(dst_path, 'FDOC')
        file_masks = ('BS0Z76.DBF', 'BS0Z76.DBS', 'BS7606.DBF', 'BS7606.DBS')
        ic_file.delAllFilesFilter(del_path, *file_masks)

        # Удалить записи из таблицы пакетной обработки
        doc = ic.metadata.ayan_archive.mtd.scan_document_pack.create()
        tab = doc.getTable()
        
        first_day_year = datefunc.get_first_day_of_month(year=clear_year.year,
                                                         month=1)
        last_day_year = datefunc.get_last_day_of_month(year=clear_year.year,
                                                       month=12)

        tab.del_where(sqlalchemy.and_(tab.c.doc_date.between(first_day_year, last_day_year),
                                      tab.c.n_doc.ilike(u'ЗТР.%')))
        
        msg = u'Удаление пакета документов с <%s> по <%s>' % (str(first_day_year), str(last_day_year))
        ic_dlg.icMsgBox(u'УДАЛЕНИЕ', msg+u' успешно завершено')
        event.Skip()
        
    def onClearMtDocsMenuItemSelected(self, event):
        """
        МАТЕРИАЛЫ. Удаление данных пакетной обработки за год.
        """
        clear_year = std_dlg.getYearDlg(ic.getMainWin())
        if clear_year is None:
            # Нажата отмена
            event.Skip()
            return
        
        # Удалить файлы
        dst_path = os.path.join(ic_file.getRootProjectDir(), 'db', 
                                str(clear_year.year))
        
        del_path = os.path.join(dst_path, 'FDOC')
        file_masks = ('MI*.DBF', 'MI*.DCM', 'MI*.DCS', 
                      'MO*.DBF', 'MO*.DCM', 'MO*.DCS',
                      'BS6068.DBF', 'BS6068.DBS',)
        ic_file.delAllFilesFilter(del_path, *file_masks)

        # Удалить записи из таблицы пакетной обработки
        doc = ic.metadata.ayan_archive.mtd.scan_document_pack.create()
        tab = doc.getTable()
        
        first_day_year = datefunc.get_first_day_of_month(year=clear_year.year,
                                                         month=1)
        last_day_year = datefunc.get_last_day_of_month(year=clear_year.year,
                                                       month=12)

        tab.del_where(sqlalchemy.and_(tab.c.doc_date.between(first_day_year, last_day_year),
                                      tab.c.n_doc.ilike(u'МТ.%')))
        
        msg = u'Удаление пакета документов с <%s> по <%s>' % (str(first_day_year), str(last_day_year))
        ic_dlg.icMsgBox(u'УДАЛЕНИЕ', msg+u' успешно завершено')
        event.Skip()

    def onClearOsDocsMenuItemSelected(self, event):
        """
        ОСНОВНЫЕ СРЕДСТВА. Удаление данных пакетной обработки за год.
        """
        clear_year = std_dlg.getYearDlg(ic.getMainWin())
        if clear_year is None:
            # Нажата отмена
            event.Skip()
            return
        
        # Удалить файлы
        dst_path = os.path.join(ic_file.getRootProjectDir(), 'db', 
                                str(clear_year.year))
        
        del_path = os.path.join(dst_path, 'FDOC')
        file_masks = ('OSN*.DBF', 'OSN*.DCO', 
                      'ROSN*.DBF', 'ROSN*.DCM',
                      'XS*.DBF', 'XS*.DBS',
                      'PLO153.DBF', 'PLO153.PLD')
        ic_file.delAllFilesFilter(del_path, *file_masks)

        # Удалить записи из таблицы пакетной обработки
        doc = ic.metadata.ayan_archive.mtd.scan_document_pack.create()
        tab = doc.getTable()
        
        first_day_year = datefunc.get_first_day_of_month(year=clear_year.year,
                                                         month=1)
        last_day_year = datefunc.get_last_day_of_month(year=clear_year.year,
                                                       month=12)

        tab.del_where(sqlalchemy.and_(tab.c.doc_date.between(first_day_year, last_day_year),
                                      tab.c.n_doc.ilike(u'ОС.%')))
        
        msg = u'Удаление пакета документов с <%s> по <%s>' % (str(first_day_year), str(last_day_year))
        ic_dlg.icMsgBox(u'УДАЛЕНИЕ', msg+u' успешно завершено')
        event.Skip()

    ###END EVENT BLOCK

manager_class = icUserMenuBarManager
