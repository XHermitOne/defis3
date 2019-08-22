#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resource module </mnt/defis/defis3/archive/archive/admin_menubar.mnu>
File            </mnt/defis/defis3/archive/archive/admin_menubar_mnu.py>
Description     <Resource module>
"""

import sqlalchemy
import os.path
import ic
from ic.log import log
from ic.dlg import std_dlg
from ic.dlg import ic_dlg
from ic.utils import datefunc
from ic.utils import filefunc
# from ic.interfaces import icmanagerinterface

from archive.forms import ctrl_doc_form

from archive import user_menubar_mnu

### RESOURCE_MODULE: /mnt/defis/defis3/archive/archive/admin_menubar.mnu

### ---- Import external modules -----
### RESOURCE_MODULE_IMPORTS

#   Version
__version__ = (0, 1, 2, 1)


class icAdminMenuBarManager(user_menubar_mnu.icUserMenuBarManager):

    def onInit(self, evt):
        pass

    ###BEGIN EVENT BLOCK

    def onImpDocStateMenuItemSelected(self, event):
        """
        Заполнение справочника состояний документа
        """
        tab = ic.metadata.THIS.tab.nsi_scan_doc_state.create()
        tab.GetManager().set_default_data()
        # После заполнения справочника сбросить его кеш,
        # чтобы отобразить изменения в уже запущенной программе
        spravmanager = ic.metadata.THIS.mtd.nsi_archive.create()
        sprav = spravmanager.getSpravByName('nsi_scan_doc_state')
        sprav.clearInCache()
        event.Skip()

    def onImpBodyTypeMenuItemSelected(self, event):
        """
        Заполнение справочника видов содержания документа
        """
        tab = ic.metadata.THIS.tab.nsi_body_type.create()
        tab.GetManager().set_default_data()
        # После заполнения справочника сбросить его кеш,
        # чтобы отобразить изменения в уже запущенной программе
        spravmanager = ic.metadata.THIS.mtd.nsi_archive.create()
        sprav = spravmanager.getSpravByName('nsi_body_type')
        sprav.clearInCache()
        event.Skip()

    def onImpDocTypeMenuItemSelected(self, event):
        """
        Заполнение справочника видов документа
        """
        tab = ic.metadata.THIS.tab.nsi_doc_type.create()
        tab.GetManager().set_default_data()
        # После заполнения справочника сбросить его кеш,
        # чтобы отобразить изменения в уже запущенной программе
        spravmanager = ic.metadata.THIS.mtd.nsi_archive.create()
        sprav = spravmanager.getSpravByName('nsi_doc_type')
        sprav.clearInCache()

        event.Skip()

    def onImpCAgentMenuItemSelected(self, event):
        """
        Заполнение справочника контрагентов
        """
        tab = ic.metadata.THIS.tab.nsi_c_agent.create()
        tab.GetManager().set_default_data()
        # После заполнения справочника сбросить его кеш,
        # чтобы отобразить изменения в уже запущенной программе
        spravmanager = ic.metadata.THIS.mtd.nsi_archive.create()
        sprav = spravmanager.getSpravByName('nsi_c_agent')
        sprav.clearInCache()

        event.Skip()

    def onImpEntityMenuItemSelected(self, event):
        """
        Заполнение справочника подразделений
        """
        tab = ic.metadata.THIS.tab.nsi_entity.create()
        tab.GetManager().set_default_data()
        # После заполнения справочника сбросить его кеш,
        # чтобы отобразить изменения в уже запущенной программе
        spravmanager = ic.metadata.THIS.mtd.nsi_archive.create()
        sprav = spravmanager.getSpravByName('nsi_entity')
        sprav.clearInCache()

        event.Skip()

    def onEditCAgentMenuItemSelected(self, event):
        """
        Редактирование справочника контрагентов
        """
        sprav_manager = ic.metadata.THIS.mtd.nsi_archive.create()
        sprav = sprav_manager.getSpravByName('nsi_c_agent')
        sprav.edit(parent=ic.getMainWin())
        event.Skip()

    def onTestSelectDocMenuItemSelected(self, event):
        """
        Тестирование выбора документа.
        """
        from work_flow.doc_sys import icdocselectdlg

        doc = ic.metadata.THIS.mtd.scan_document.create()
        print(icdocselectdlg.select_document_dlg(doc=doc))
        event.Skip()

    def onEditSettingsMenuItemSelected(self, event):
        """
        Редактирование настроек.
        """
        from archive.forms import settings_edit_dlg
        settings_edit_dlg.edit_settings_dlg()
        event.Skip()

    def onTestSearchDocMenuItemSelected(self, event):
        """
        Тестирование поиска документа.
        """
        from .forms import search_doc_form

        main_win = ic.getMainWin()
        page = search_doc_form.icSearchDocPanel(parent=main_win)
        main_win.addOrgPage(page, u'Тест поиска документов')

        event.Skip()

    def onTestPrintDocMenuItemSelected(self, event):
        """
        Тестирование поиска и печати документа.
        """
        from .forms import print_doc_form

        main_win = ic.getMainWin()
        page = print_doc_form.icPrintDocPanel(parent=main_win)
        main_win.addOrgPage(page, u'Тест печати документов')

        event.Skip()

    def onTestSearchDlgMenuItemSelected(self, event):
        """
        Тестирование поиска документа.
        """
        from .forms import search_doc_form

        search_doc_form.search_doc_dlg()
        event.Skip()

    def onTestPrintersMenuItemSelected(self, event):
        """
        Тестирование диалогового окна выбора принтера.
        """
        from ic.dlg import ic_printer_dlg

        main_win = ic.getMainWin()
        selected = ic_printer_dlg.choice_printer_dlg(parent=main_win)
        print('Printer', selected)

        event.Skip()

    def onCtrlDocMenuItemSelected(self, event):
        """
        Поиск и управление документами.
        """
        ctrl_doc_form.open_ctrl_search_doc_page()

        event.Skip()

    def onCorrectDocMenuItemSelected(self, event):
        """
        Коррекция отсканированных документов.
        """
        from archive.forms import correct_doc_panel

        correct_doc_panel.open_correct_doc_panel()

        event.Skip()

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
        dst_path = os.path.join(filefunc.getRootProjectDir(), 'db',
                                str(first_day_of_month.year))

        str_month = '%X' % first_day_of_month.month
        del_path = os.path.join(dst_path, 'FDOC')
        file_masks = ('R0*.DBF', 'R0*.DCM',
                      'R%s*.DBF' % str_month, 'R%s*.DCM' % str_month,
                      'TI%s*.DBF' % str_month, 'TI%s*.DCM' % str_month,
                      'TO%s*.DBF' % str_month, 'TO%s*.DCM' % str_month)
        filefunc.delAllFilesFilter(del_path, *file_masks)

        del_path = os.path.join(dst_path, 'FDSB')
        file_masks = ('SB%s111.DBF' % str_month, 'SB%s111.DCB' % str_month,
                      'SB%s111.DSB' % str_month, 'SB%s111S.DBF' % str_month)
        filefunc.delAllFilesFilter(del_path, *file_masks)

        # Удалить записи из таблицы пакетной обработки
        doc = ic.metadata.archive.mtd.scan_document_pack.create()
        tab = doc.getTable()

        msg = u'Удаление пакета документов с <%s> по <%s>' % (str(first_day_of_month), str(last_day))
        log.debug(u'Удаление пакета документов с <%s> по <%s>' % (str(first_day_of_month), str(last_day)))
        tab.del_where(tab.c.doc_date.between(first_day_of_month, last_day))

        ic_dlg.openMsgBox(u'УДАЛЕНИЕ', msg + u' успешно завершено')
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
        dst_path = os.path.join(filefunc.getRootProjectDir(), 'db',
                                str(clear_year.year))

        del_path = os.path.join(dst_path, 'FDOC')
        file_masks = ('BS0Z76.DBF', 'BS0Z76.DBS', 'BS7606.DBF', 'BS7606.DBS')
        filefunc.delAllFilesFilter(del_path, *file_masks)

        # Удалить записи из таблицы пакетной обработки
        doc = ic.metadata.archive.mtd.scan_document_pack.create()
        tab = doc.getTable()

        first_day_year = datefunc.get_first_day_of_month(year=clear_year.year,
                                                         month=1)
        last_day_year = datefunc.get_last_day_of_month(year=clear_year.year,
                                                       month=12)

        tab.del_where(sqlalchemy.and_(tab.c.doc_date.between(first_day_year, last_day_year),
                                      tab.c.n_doc.ilike(u'ЗТР.%')))

        msg = u'Удаление пакета документов с <%s> по <%s>' % (str(first_day_year), str(last_day_year))
        ic_dlg.openMsgBox(u'УДАЛЕНИЕ', msg + u' успешно завершено')
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
        dst_path = os.path.join(filefunc.getRootProjectDir(), 'db',
                                str(clear_year.year))

        del_path = os.path.join(dst_path, 'FDOC')
        file_masks = ('MI*.DBF', 'MI*.DCM',
                      'MO*.DBF', 'MO*.DCM',
                      'BS6068.DBF', 'BS6068.DBS',)
        filefunc.delAllFilesFilter(del_path, *file_masks)

        # Удалить записи из таблицы пакетной обработки
        doc = ic.metadata.archive.mtd.scan_document_pack.create()
        tab = doc.getTable()

        first_day_year = datefunc.get_first_day_of_month(year=clear_year.year,
                                                         month=1)
        last_day_year = datefunc.get_last_day_of_month(year=clear_year.year,
                                                       month=12)

        tab.del_where(sqlalchemy.and_(tab.c.doc_date.between(first_day_year, last_day_year),
                                      tab.c.n_doc.ilike(u'МТ.%')))

        msg = u'Удаление пакета документов с <%s> по <%s>' % (str(first_day_year), str(last_day_year))
        ic_dlg.openMsgBox(u'УДАЛЕНИЕ', msg + u' успешно завершено')
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
        dst_path = os.path.join(filefunc.getRootProjectDir(), 'db',
                                str(clear_year.year))

        del_path = os.path.join(dst_path, 'FDOC')
        file_masks = ('OSN*.DBF', 'OSN*.DCO',
                      'ROSN*.DBF', 'ROSN*.DCM',
                      'XS*.DBF', 'XS*.DBS',
                      'PLO153.DBF', 'PLO153.PLD')
        filefunc.delAllFilesFilter(del_path, *file_masks)

        # Удалить записи из таблицы пакетной обработки
        doc = ic.metadata.archive.mtd.scan_document_pack.create()
        tab = doc.getTable()

        first_day_year = datefunc.get_first_day_of_month(year=clear_year.year,
                                                         month=1)
        last_day_year = datefunc.get_last_day_of_month(year=clear_year.year,
                                                       month=12)

        tab.del_where(sqlalchemy.and_(tab.c.doc_date.between(first_day_year, last_day_year),
                                      tab.c.n_doc.ilike(u'ОС.%')))

        msg = u'Удаление пакета документов с <%s> по <%s>' % (str(first_day_year), str(last_day_year))
        ic_dlg.openMsgBox(u'УДАЛЕНИЕ', msg + u' успешно завершено')
        event.Skip()
    ###END EVENT BLOCK

manager_class = icAdminMenuBarManager
