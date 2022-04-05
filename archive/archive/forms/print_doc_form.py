#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Формы поиска и печати отсканированных документов.
"""

import sys
import os
import os.path
import datetime
import wx
import wx.adv
import sqlalchemy

from archive.forms import search_doc_form_proto
from archive.forms import edit_doc_form
from archive.forms import scheme_doc_form
from ic import bmpfunc
from ic import log
from ic import dlgfunc
from ic import filefunc
from ic.utils import datetimefunc
import ic
from archive.forms import search_doc_form
from ic.dlg import ic_printer_dlg
from ic.utils import printerfunc
from ic.utils import pdffunc
from ic.engine import form_manager

# Version
__version__ = (0, 1, 1, 1)

DB_DATE_FMT = '%Y-%m-%d'


class icPrintDocPanel(search_doc_form.icSearchDocPanelCtrl,
                      search_doc_form_proto.icPrintDocPanelProto,
                      form_manager.icFormManager):
    """
    Панель поиска и печати документов.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        form_manager.icFormManager.__init__(self)
        search_doc_form_proto.icPrintDocPanelProto.__init__(self, *args, **kwargs)

        self.init()
        # self.autocomplit.LoadDict()     # Загрузить частотные словари для авто заполнений

        # Необходимо перепривязать обработчики
        self.search_crit_panel.start_datePicker.Bind(wx.adv.EVT_DATE_CHANGED, self.onStartDatePickerChanged)
        self.search_crit_panel.end_datePicker.Bind(wx.adv.EVT_DATE_CHANGED, self.onEndDatePickerChanged)
        self.search_crit_panel.date_checkBox.Bind(wx.EVT_CHECKBOX, self.onDateCheckBox)
        self.search_crit_panel.one_date_checkBox.Bind(wx.EVT_CHECKBOX, self.onOneDateCheckBox)

        self.search_crit_panel.obj_start_datePicker.Bind(wx.adv.EVT_DATE_CHANGED, self.onObjStartDatePickerChanged)
        self.search_crit_panel.obj_end_datePicker.Bind(wx.adv.EVT_DATE_CHANGED, self.onObjEndDatePickerChanged)
        self.search_crit_panel.obj_date_checkBox.Bind(wx.EVT_CHECKBOX, self.onObjDateCheckBox)
        self.search_crit_panel.obj_one_date_checkBox.Bind(wx.EVT_CHECKBOX, self.onObjOneDateCheckBox)

        self.search_crit_panel.doc_type_checkBox.Bind(wx.EVT_CHECKBOX, self.onDocTypeCheckBox)
        self.search_crit_panel.entity_checkBox.Bind(wx.EVT_CHECKBOX, self.onEntityCheckBox)
        self.search_crit_panel.contragent_checkBox.Bind(wx.EVT_CHECKBOX, self.onContragentCheckBox)

        self.search_crit_panel.clear_button.Bind(wx.EVT_BUTTON, self.onClearButtonClick)
        self.search_crit_panel.search_button.Bind(wx.EVT_BUTTON, self.onSearchButtonClick)

        # log.debug(u'DOC CHECK LIST CTRL <%s>' % self.docs_listCtrl.__class__.__name__)

    def onAllCheckBox(self, event):
        """
        Установка/Снятие отметки выделения всех найденных документов.
        Обработчик события.
        """
        check = event.IsChecked()
        for i in range(self.docs_listCtrl.GetItemCount()):
            self.docs_listCtrl.CheckItem(i, check=check)

        event.Skip()

    def print_scan_document(self, doc_filename, printer_name):
        """
        Запустить печать документа.

        :param doc_filename: Полное имя файла документа.
        :param printer_name: Наименование принтера,
            на который будет производиться печать.
        """
        if os.path.exists(doc_filename):
            log.debug(u'Печать документа <%s>' % doc_filename)
            printerfunc.printFile(doc_filename, printer_name)
        else:
            log.warning(u'Не найден файла <%s> для печати' % doc_filename)

    def onPrintToolClicked(self, event):
        """
        Обработчик инструмента пакетной печати выбранных документов.
        """
        printer_info = ic_printer_dlg.choice_printer_dlg(self)
        if printer_info is None:
            dlgfunc.openWarningBox(u'ВНИМАНИЕ', u'Не выбран принтер для печати. Печать документов отменена.')
            event.Skip()
            return

        printer_name = printer_info['name']

        for i in range(self.docs_listCtrl.GetItemCount()):
            if self.docs_listCtrl.IsChecked(i):
                document = self.documents[i]
                doc_uuid = document['uuid']
                doc = ic.metadata.THIS.mtd.scan_document.create()
                doc.load_obj(doc_uuid)
                filename = doc.getRequisiteValue('file_name')
                self.print_scan_document(filename, printer_name)
            else:
                log.debug(u'Пропуск печати [%d]' % i)

        event.Skip()

    def onReportToolClicked(self, event):
        """
        Обработчик инструмента получения отчета списка документов.
        """
        rep_manager = ic.getReportManager()

        doc_type = self.search_crit_panel.doc_type_ctrl.getValue()
        contragents = self.search_crit_panel.contragent_ctrl.getValue()
        entity=self.search_crit_panel.entity_ctrl.getValue()

        wx_date = self.search_crit_panel.start_datePicker.GetValue()
        docdate_start = datetimefunc.wxdate2pydate(wx_date).strftime(DB_DATE_FMT) if self.search_crit_panel.date_checkBox.IsChecked() else ''
        wx_date = self.search_crit_panel.end_datePicker.GetValue()
        docdate_end = datetimefunc.wxdate2pydate(wx_date).strftime(DB_DATE_FMT) if self.search_crit_panel.date_checkBox.IsChecked() else ''

        orderby_idx = self.search_crit_panel.orderby_choice.GetSelection()

        vars = dict(docnum=self.search_crit_panel.docnum_textCtrl.GetValue(),
                    is_docnum_equal=bool(self.search_crit_panel.docnum_radioBox.GetSelection()),
                    docname=self.search_crit_panel.docname_textCtrl.GetValue(),
                    docdate_start=docdate_start,
                    docdate_end=docdate_end,
                    doctype= doc_type if doc_type else '',
                    contragents= contragents if contragents else '',
                    entity=entity if entity else '',
                    description=self.search_crit_panel.description_textCtrl.GetValue(),
                    comment=self.search_crit_panel.comment_textCtrl.GetValue(),
                    tag0=self.search_crit_panel.tag0_textCtrl.GetValue(),
                    tag1=self.search_crit_panel.tag1_textCtrl.GetValue(),
                    tag2=self.search_crit_panel.tag2_textCtrl.GetValue(),
                    tag3=self.search_crit_panel.tag3_textCtrl.GetValue(),
                    tag4=self.search_crit_panel.tag4_textCtrl.GetValue(),
                    tag5=self.search_crit_panel.tag5_textCtrl.GetValue(),
                    tag6=self.search_crit_panel.tag6_textCtrl.GetValue(),
                    tag7=self.search_crit_panel.tag7_textCtrl.GetValue(),
                    tag8=self.search_crit_panel.tag8_textCtrl.GetValue(),
                    tag9=self.search_crit_panel.tag9_textCtrl.GetValue(),
                    order_by_field=['', 'n_doc', 'doc_name', 'doc_date'][orderby_idx])
        rep_manager.prev_select_action('doc_ext/search_document_list.ods',
                                       variables=vars)
        event.Skip()

    def getSavePDFDirPath(self):
        """
        Определить папку для сохранения PDF файлов.
        :return:
        """
        save_pdf_dir = ic.settings.THIS.SETTINGS.save_pdf_dir.get()
        if not save_pdf_dir or not os.path.exists(save_pdf_dir):
            save_pdf_dir = dlgfunc.getDirDlg(parent=self,
                                             title=u'Папка сохранения PDF документов')
        return save_pdf_dir

    def savePDFDocs(self, save_doc_uuids, save_pdf_dir=None, bAutoClear=False,
                    bCompactName=False):
        """
        Сохранение PDF документов в разные PDF файлы.

        :param save_doc_uuids: UUIDы сохраняемых документов.
        :param save_pdf_dir: Папка для сохранения.
        :param bAutoClear: Автоматически очистить папку выгрузки?
        :param bCompactName: Сокращенное именование файлов документов?
        :return: True/False.
        """
        try:
            return self._savePDFDocs(save_doc_uuids=save_doc_uuids,
                                     save_pdf_dir=save_pdf_dir,
                                     bAutoClear=bAutoClear,
                                     bCompactName=bCompactName)
        except:
            log.fatal(u'Ошибка сохранения документов в PDF виде в папку <%s>' % save_pdf_dir)
        return False

    def _savePDFDocs(self, save_doc_uuids, save_pdf_dir=None, bAutoClear=False,
                     bCompactName=False):
        """
        Сохранение PDF документов в разные PDF файлы.

        :param save_doc_uuids: UUIDы сохраняемых документов.
        :param save_pdf_dir: Папка для сохранения.
        :param bAutoClear: Автоматически очистить папку выгрузки?
        :return: True/False.
        """
        if save_pdf_dir is None:
            save_pdf_dir = self.getSavePDFDirPath()
            if not save_pdf_dir:
                msg = u'Не определена папка для сохранения PDF файлов'
                log.warning(msg)
                dlgfunc.openWarningBox(u'ОШИБКА', msg)
                return False

        if os.path.exists(save_pdf_dir) and (bAutoClear or dlgfunc.openAskBox(u'Очистка папки',
                                                                              u'Удалить все файлы из папки <%s>?' % save_pdf_dir)):
            filefunc.clearDir(save_pdf_dir)

        if not os.path.exists(save_pdf_dir):
            msg = u'Не существует папка выгрузки PDF файлов <%s>' % save_pdf_dir
            log.warning(msg)
            dlgfunc.openWarningBox(u'ОШИБКА', msg)
            return False

        sprav_manager = ic.metadata.THIS.mtd.nsi_archive.create()
        c_agent = sprav_manager.getSpravByName('nsi_c_agent')
        doc = ic.metadata.THIS.mtd.scan_document.create()

        for i, doc_uuid in enumerate(save_doc_uuids):
            doc.load_obj(doc_uuid)
            filename = doc.getRequisiteValue('file_name')

            doc_name = doc.getRequisiteValue('doc_name')
            doc_date = doc.getRequisiteValue('doc_date')
            doc_n = doc.getRequisiteValue('n_doc')

            contragent_cod = doc.getRequisiteValue('c_agent')
            contragent_data = c_agent.Find(contragent_cod, ('name', 'inn', 'kpp'))
            # contragent_name = contragent_data.get('name', u'')
            contragent_inn = contragent_data.get('inn', u'')
            # contragent_kpp = contragent_data.get('kpp', u'')

            doc_contragent_n = doc.getRequisiteValue('n_obj')
            doc_contragent_date = doc.getRequisiteValue('obj_date')

            if bCompactName:
                words = ('%04d' % (i+1), u'INN'+contragent_inn)
            else:
                words = ('%04d' % (i+1),  doc_name, doc_n, doc_date.strftime('%d-%m-%Y'),
                         # contragent_name,
                         u'INN'+contragent_inn,
                         # u'КПП:'+contragent_kpp,
                         doc_contragent_n, doc_contragent_date.strftime('%d-%m-%Y'))

            base_filename = '.'.join(words).replace('/', '-').replace('\\', '-')
            new_filename = os.path.join(save_pdf_dir, base_filename + os.path.splitext(filename)[1])

            filefunc.copyFile(filename, new_filename, True)
        return True

    def onSaveToolClicked(self, event):
        """
        Обработчик сохранения документов в PDF.
        """
        save_pdf_dir = self.getSavePDFDirPath()
        if not save_pdf_dir:
            event.Skip()
            return

        doc_uuids = [self.documents[i]['uuid'] for i in range(self.docs_listCtrl.GetItemCount()) if self.docs_listCtrl.IsChecked(i)]
        self.savePDFDocs(save_doc_uuids=doc_uuids, save_pdf_dir=save_pdf_dir)

        event.Skip()

    def publicPDFDocs(self, save_doc_uuids, save_pdf_dir=None, bAutoClear=False,
                    bCompactName=False, catalog_order=('inn', 'kpp', 'year', 'doc_type'),
                    bProgress=True):
        """
        Сохранение PDF документов в разные PDF файлы.

        :param save_doc_uuids: UUIDы сохраняемых документов.
        :param save_pdf_dir: Папка для сохранения.
        :param bAutoClear: Автоматически очистить папку выгрузки?
        :param bCompactName: Сокращенное именование файлов документов?
        :param catalog_order: Порядо катологизации документов.
        :param bProgress: Отобразить прогресс бар?
        :return: True/False.
        """
        try:
            return self._publicPDFDocs(save_doc_uuids=save_doc_uuids,
                                     save_pdf_dir=save_pdf_dir,
                                     bAutoClear=bAutoClear,
                                     bCompactName=bCompactName,
                                     catalog_order=catalog_order,
                                     bProgress=bProgress)
        except:
            log.fatal(u'Ошибка сохранения документов в PDF виде в папку <%s>' % save_pdf_dir)
        return False

    def _publicPDFDocs(self, save_doc_uuids, save_pdf_dir=None, bAutoClear=False,
                       bCompactName=False, catalog_order=('inn', 'kpp', 'year', 'doc_type'),
                       bProgress=True):
        """
        Сохранение PDF документов в разные PDF файлы.

        :param save_doc_uuids: UUIDы сохраняемых документов.
        :param save_pdf_dir: Папка для сохранения.
        :param bAutoClear: Автоматически очистить папку выгрузки?
        :param bCompactName: Сокращенное именование файлов документов?
        :param catalog_order: Порядо катологизации документов.
        :param bProgress: Отобразить прогресс бар?
        :return: True/False.
        """
        if save_pdf_dir is None:
            save_pdf_dir = self.getSavePDFDirPath()
            if not save_pdf_dir:
                msg = u'Не определена папка для сохранения PDF файлов'
                log.warning(msg)
                dlgfunc.openWarningBox(u'ОШИБКА', msg)
                return False

        if os.path.exists(save_pdf_dir) and (bAutoClear or dlgfunc.openAskBox(u'Очистка папки',
                                                                              u'Удалить все файлы из папки <%s>?' % save_pdf_dir)):
            filefunc.clearDir(save_pdf_dir, bDelSubDirs=True)

        if not os.path.exists(save_pdf_dir):
            msg = u'Не существует папка выгрузки PDF файлов <%s>' % save_pdf_dir
            log.warning(msg)
            dlgfunc.openWarningBox(u'ОШИБКА', msg)
            return False

        try:
            if bProgress:
                dlgfunc.openProgressDlg(parent=None, title=u'ЗАГРУЗКА', prompt_text=u'',
                                        min_value=0, max_value=len(save_doc_uuids))
                                        
            sprav_manager = ic.metadata.THIS.mtd.nsi_archive.create()
            c_agent = sprav_manager.getSpravByName('nsi_c_agent')
            doc_types = sprav_manager.getSpravByName('nsi_doc_type')
            doc = ic.metadata.THIS.mtd.scan_document.create()

            for i, doc_uuid in enumerate(save_doc_uuids):
                doc.load_obj(doc_uuid)
                filename = doc.getRequisiteValue('file_name')

                doc_name = doc.getRequisiteValue('doc_name')
                doc_date = doc.getRequisiteValue('doc_date')
                doc_n = doc.getRequisiteValue('n_doc')
                doc_type_cod = doc.getRequisiteValue('doc_type')
                doc_type_name = doc_types.Find(doc_type_cod)

                contragent_cod = doc.getRequisiteValue('c_agent')
                contragent_data = c_agent.Find(contragent_cod, ('name', 'inn', 'kpp'))
                contragent_name = contragent_data.get('name', u'')
                contragent_inn = contragent_data.get('inn', u'')
                contragent_kpp = contragent_data.get('kpp', u'')

                doc_contragent_n = doc.getRequisiteValue('n_obj')
                doc_contragent_date = doc.getRequisiteValue('obj_date')
            
                # Распределение по подпапкам
                save_dir_names = dict(inn=contragent_inn, kpp=contragent_kpp, 
                                      year=str(doc_date.year) if isinstance(doc_date, (datetime.datetime, datetime.date)) else 'XXXX',
                                      doc_type=doc_type_name)
                save_subdirs = [save_pdf_dir] + [save_dir_names.get(catalog_name, 'X') for catalog_name in catalog_order]
                log.debug(str(save_subdirs))
                save_dir_path = os.path.join(*save_subdirs)
                if not os.path.exists(save_dir_path):
                    filefunc.makeDirs(save_dir_path)

                if bCompactName:
                    words = ('%04d' % (i+1), u'INN'+contragent_inn)
                else:
                    words = ('%04d' % (i+1), contragent_inn, 
                            contragent_kpp, doc_date.strftime('%d-%m-%Y'),
                            doc_type_name)

                base_filename = '_'.join(words).replace('/', '-').replace('\\', '-')
                new_filename = os.path.join(save_dir_path, base_filename + os.path.splitext(filename)[1])

                filefunc.copyFile(filename, new_filename, True)
                
                dlgfunc.updateProgressDlg(i, new_prompt_text=u'Загрузка файла <%s>' % base_filename)

            if bProgress:
                dlgfunc.closeProgressDlg()                
            return True
        except:
            log.fatal(u'Ошибка сохранения PDF файлов из БД')
            if bProgress:
                dlgfunc.closeProgressDlg()                
        return False

    def onSaveOnePDFToolClicked(self, event):
        """
        Обработчик сохранения документов в один PDF файл.
        """
        save_pdf_dir = self.getSavePDFDirPath()
        if not save_pdf_dir:
            event.Skip()
            return

        doc_uuids = [self.documents[i]['uuid'] for i in range(self.docs_listCtrl.GetItemCount()) if self.docs_listCtrl.IsChecked(i)]
        if not doc_uuids:
            dlgfunc.openWarningBox(u'СОХРАНЕНИЕ', u'Не выбраны документы для сохранения')
            event.Skip()
            return
            
        if self.publicPDFDocs(save_doc_uuids=doc_uuids, save_pdf_dir=save_pdf_dir, bAutoClear=True, bCompactName=False):
            dlgfunc.openMsgBox(u'СОХРАНЕНИЕ',
                               u'Документы успешно сохранены в <%s>. ' % save_pdf_dir)
        else:            
            dlgfunc.openWarningBox(u'СОХРАНЕНИЕ',
                                   u'Ошибка сохранения PDF файлов из БД')

        event.Skip()

    def onSaveOnePDFToolClicked_old(self, event):
        """
        Обработчик сохранения PDF документов для передачи третьим лицам в электронном виде.
        """
        save_pdf_dir = self.getSavePDFDirPath()
        if not save_pdf_dir:
            event.Skip()
            return

        doc_uuids = [self.documents[i]['uuid'] for i in range(self.docs_listCtrl.GetItemCount()) if self.docs_listCtrl.IsChecked(i)]
        self.savePDFDocs(save_doc_uuids=doc_uuids, save_pdf_dir=save_pdf_dir, bAutoClear=True, bCompactName=True)

        try:
            pdf_filenames = filefunc.getFilenamesByExt(save_pdf_dir, '.pdf')
            pdf_filenames.sort()
            first_pdf_name = os.path.splitext(os.path.basename(pdf_filenames[0]))[0]
            last_pdf_name = os.path.splitext(os.path.basename(pdf_filenames[-1]))[0]

            if pdf_filenames:
                new_pdf_filename = u'Docs.%s-%s.pdf' % (first_pdf_name, last_pdf_name)
                new_pdf_filename = os.path.join(save_pdf_dir,
                                                new_pdf_filename.replace('"', ' '))
                if pdffunc.concatenatePDF(src_pdf_filenames=pdf_filenames, dst_pdf_filename=new_pdf_filename):
                    pdffunc.compressCupsPDF(pdf_filename=new_pdf_filename)
                    # pdffunc.compressGhostscriptPDF(pdf_filename=new_pdf_filename,
                    #                                quality=printerfunc.GS_QUALITY_SCREEN)

                    for pdf_filename in pdf_filenames:
                        os.remove(pdf_filename)

                if os.path.exists(new_pdf_filename):
                    if dlgfunc.openAskBox(u'СОХРАНЕНИЕ',
                                          u'Документы успешно сохранены в PDF файл <%s>. Открыть для просмотра?' % new_pdf_filename):
                        self.viewDocFile(new_pdf_filename)
                else:
                    dlgfunc.openWarningBox(u'СОХРАНЕНИЕ',
                                           u'Ошибка сохранения документов в PDF файле')

        except:
            log.fatal(u'Ошибка сохранения одного PDF файла')

        event.Skip()


def open_print_search_doc_page(main_win=None):
    """
    Открыть страницу поиска/печати документа из архива.

    :param main_win: Главное окно приложения.
    """
    try:
        if main_win is None:
            main_win = ic.getMainWin()

        page = icPrintDocPanel(parent=main_win)
        main_win.addOrgPage(page, u'Поиск документов')
    except:
        log.fatal(u'Ошибка открытия страницы поиска/печати документа архива')
    return
