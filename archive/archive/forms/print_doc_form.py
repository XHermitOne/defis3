#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Формы поиска и печати отсканированных документов.
"""

import sys
import os
import os.path
import wx
import wx.adv
import sqlalchemy

from archive.forms import search_doc_form_proto
from archive.forms import edit_doc_form
from archive.forms import scheme_doc_form
from ic import ic_bmp
from ic import log
from ic import ic_dlg
from ic.utils import ic_time
import ic
from archive.forms import search_doc_form
from ic.dlg import ic_printer_dlg
from ic.utils import printerfunc
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
        @param doc_filename: Полное имя файла документа.
        @param printer_name: Наименование принтера,
            на который будет производиться печать.
        """
        if os.path.exists(doc_filename):
            log.debug(u'Печать документа <%s>' % doc_filename)
            printerfunc.print_file(doc_filename, printer_name)
        else:
            log.warning(u'Не найден файла <%s> для печати' % doc_filename)

    def onPrintToolClicked(self, event):
        """
        Обработчик инструмента пакетной печати выбранных документов.
        """
        printer_info = ic_printer_dlg.choice_printer_dlg(self)
        if printer_info is None:
            ic_dlg.icWarningBox(u'ВНИМАНИЕ', u'Не выбран принтер для печати. Печать документов отменена.')
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
        docdate_start = ic_time.wxdate2pydate(wx_date).strftime(DB_DATE_FMT) if self.search_crit_panel.date_checkBox.IsChecked() else ''
        wx_date = self.search_crit_panel.end_datePicker.GetValue()
        docdate_end = ic_time.wxdate2pydate(wx_date).strftime(DB_DATE_FMT) if self.search_crit_panel.date_checkBox.IsChecked() else ''

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


def open_print_search_doc_page(main_win=None):
    """
    Открыть страницу поиска/печати документа из архива.
    @param main_win: Главное окно приложения.
    """
    try:
        if main_win is None:
            main_win = ic.getMainWin()

        page = icPrintDocPanel(parent=main_win)
        main_win.AddOrgPage(page, u'Поиск документов')
    except:
        log.fatal(u'Ошибка открытия страницы поиска/печати документа архива')
    return
