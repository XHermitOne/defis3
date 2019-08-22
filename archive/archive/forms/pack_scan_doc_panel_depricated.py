#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль формы <icPackScanDocPanelProto>. 
Сгенерирован проектом DEFIS по модулю формы-прототипа wxFormBuider.
"""

import datetime
import operator
import os
import wx
from . import edit_doc_form_proto

import ic
from ic.log import log
from ic.dlg import std_dlg
from ic.dlg import dlgfunc
from ic.dlg import quick_entry_panel
from ic.utils import ic_str
from ic.utils import ic_time

from ic.engine import form_manager

from archive.convert import import_fdoc
from STD.queries import filter_generate
from . import new_doc_panel
from . import group_manipulation_dlg

__version__ = (0, 1, 6, 1)

DEFAULT_DB_DATE_FMT = '%Y-%m-%d'
DEFAULT_DATE_FMT = '%d.%m.%Y'


class icQuickEntryPackScanPanel(edit_doc_form_proto.icQuickEntryPackScanPanelProto):
    """
    Панель быстрого ввода.
    """
    pass


class icPackScanDocPanel(edit_doc_form_proto.icPackScanDocPanelProto,
                         form_manager.icFormManager,
                         new_doc_panel.icDocCardPanelManager):
    """
    Форма пакетной обработки документов.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        edit_doc_form_proto.icPackScanDocPanelProto.__init__(self, *args, **kwargs)
        
        # Диапазон дат
        self.dt_begin = None
        self.dt_end = None
        
        # Выбранный склад
        self.n_warehouse = None
        
        # Дополнительный тег для фильтра
        # self.ext_tag = None
        
        # Признак приходного документа
        self.is_input = False
        
        # Режим быстрого ввода
        self.quick_entry_mode = False
        
    def onNPagesToolClicked(self, event):
        """
        Обработчик инструмента установки количества страниц документа.
        """
        idx = self.getItemSelectedIdx(self.docs_listCtrl)
        if idx != -1:
            document = self.documents[idx]
            doc_uuid = document['uuid']
            doc = ic.metadata.THIS.mtd.scan_document_pack.create()
            doc.load_obj(doc_uuid)
            n_pages = std_dlg.getIntegerDlg(self, u'СКАНИРОВАНИЕ', 
                                            u'Укажите количество страниц документа',
                                            1, 500)
            is_duplex = std_dlg.getRadioChoiceDlg(self, u'СКАНИРОВАНИЕ',
                                                  u'Сканирование листа с 2-ч сторон?', 
                                                  choices=(u'НЕТ', u'ДА'))
            if n_pages:
                doc.setRequisiteValue('n_scan_pages', n_pages)

            if is_duplex is not None:
                doc.setRequisiteValue('is_duplex', is_duplex)

            if n_pages or is_duplex is not None:
                doc.save_obj()
                self.refreshDocList()
        else:
            dlgfunc.openWarningBox(u'ВНИМАНИЕ!', u'Выберите документ для редактирования')
        event.Skip()

    def onArchiveToolClicked(self, event):
        """
        Обработчик передачи пакета в архив.
        """
        doc_indexes = self.getCheckedItems_list_ctrl(self.docs_listCtrl)
        if doc_indexes:
            doc = ic.metadata.archive.mtd.scan_document_pack.create()
            archive_doc = ic.metadata.archive.mtd.scan_document.create()
            pack_result = True
            for doc_idx in doc_indexes:
                doc_uuid = self.documents[doc_idx]['uuid']
                doc.load_obj(doc_uuid)
                scan_filename = doc.getRequisiteValue('file_name')
                if scan_filename and os.path.exists(scan_filename):
                    result = doc.remove_to(archive_doc, doc_uuid=doc_uuid, 
                                           requisite_replace={'scan_doc_to': 'scan_doc_pack_to',
                                                              'scan_doc_from': 'scan_doc_pack_from'})
                    if not result:
                        dlgfunc.openWarningBox(u'ВНИМАНИЕ',
                                            u'Ошибка переноса документа <%s> в архив' % doc.getRequisiteValue('n_doc'))
                
                    pack_result = pack_result and result
                else:
                    msg = u'Файл скана отсутствует в карточке документа <%s>. Перенос не выполнен' % doc.getRequisiteValue('n_doc')
                    log.warning(msg)
                    dlgfunc.openWarningBox(u'ВНИМАНИЕ', msg)
                    pack_result = False

            if pack_result:
                dlgfunc.openMsgBox(u'АРХИВ',
                                u'Пакет документов перенесен в архив')
            self.refreshDocList()

        event.Skip()

    def onEditToolClicked(self, event):
        """
        Обработчик редактирования карточки документа.
        """
        idx = self.docs_listCtrl.GetFirstSelected()
        if idx != -1:
            document = self.documents[idx]
            doc_uuid = document['uuid']
            doc = ic.metadata.THIS.mtd.scan_document_pack.create()
            doc.load_obj(doc_uuid)
            log.debug(u'Редактирование документа UUID <%s>' % doc_uuid)
            from archive.forms import edit_doc_form
            result = edit_doc_form.edit_doc_dlg(doc=doc)
            if result:
                doc.save_obj()
                # Обновить выделенный документ после радактирования
                self.documents[idx] = doc.getRequisiteData()
                # Обновить список документов если нормально отредактировали документ
                self.refreshDocList()
        else:
            dlgfunc.openWarningBox(u'ВНИМАНИЕ!', u'Выберите документ для редактирования')
        
        event.Skip()

    def onChangeDocType(self, event):
        """
        Обработчик изменения типа документа.
        """
        self.refreshDocList()
        
        if event:
            event.Skip()

    def onChangeContragent(self, event):
        """
        Обработчик изменения контрагента.
        """
        self.refreshDocList()
        
        if event:
            event.Skip()            

    def onTagChoice(self, event):
        """
        Обработчик изменения дополнительного признака.
        """
        self.refreshDocList()
        
        if event:
            event.Skip()            

    def onSortRadioBox(self, event):
        """
        Обработчик изменения способа сортировки.
        """
        self.refreshDocList()
        
        if event:
            event.Skip()            

    def onGroupRadioBox(self, event):
        """
        Обработчик изменения способа группировки.
        """
        self.refreshDocList()
        
        if event:
            event.Skip()            
    
    def onImportToolClicked(self, event):
        """
        Обработчик импорта документов из БАЛАНСА.
        """
        popup_menu = ic.metadata.archive.mnu.import_select_popup_menu.create()
        popup_menu.GetManager().setPackScanPanel(self)
        popup_menu.popupByTool(self.import_tool)
        event.Skip()

    def getScanDocCount(self):
        """
        Определить количество сканируемых документов.
        """
        check_idx_list = self.getCheckedItems_list_ctrl(ctrl=self.docs_listCtrl)
        return len(check_idx_list)            
        
    def getScanPageCount(self):
        """
        Определить количество сканируемых страниц.
        """
        check_idx_list = self.getCheckedItems_list_ctrl(ctrl=self.docs_listCtrl)
        scan_pages = [self.documents[idx].get('n_scan_pages', 0) for idx in check_idx_list]
        return sum(scan_pages)

    def _extractNDocWarehouse(self, doc_rec):
        """
        Определить номер документа в виде №документа\№склада.        
        """
        sub_n_doc = doc_rec['n_doc'].split('.')[-1]
        return sub_n_doc
    
    def _extractNDoc(self, doc_rec):
        """
        Определить номер документа в виде 
        целого числа (по первой части номера) + наименование
        """
        sub_n_doc = doc_rec['n_doc'].split('.')[-1]
        num_n_doc = sub_n_doc.split(u'/')[0]
        n_doc = u'%s%s' % (u'0'*(9-len(num_n_doc))+num_n_doc, 
                           ic_str.toUnicode(doc_rec['doc_name']))
        return n_doc
    
    def _extractNWarehouse(self, doc_rec):
        """
        Определить номер склада документа в виде 
        целого числа (по сторой части номера)
        """
        sub_n_doc = doc_rec['n_doc'].split('.')[-1]
        num_warehouse = sub_n_doc.split(u'/')[-1]
        return num_warehouse

    def _extractOperationCode(self, doc_rec):
        """
        Определить Код операции.
        """
        tag_oper_cod = doc_rec['tags'].split(';')[2]
        parse_oper_cod = tag_oper_cod.strip().split(' ') if tag_oper_cod.strip() else []
        if len(parse_oper_cod) >= 3  and parse_oper_cod[0] == u'Код' and parse_oper_cod[1] == u'операции':
            str_oper_cod = parse_oper_cod[-1]
            return int(str_oper_cod)
        return 0

    def _extractOperationDate(self, doc_rec):
        """
        Определить дату операции.
        """
        return doc_rec['dt_oper'] if doc_rec['dt_oper'] else doc_rec['doc_date']

    def _extractInvNom(self, doc_rec):
        """
        Определить инвентарный номер.
        """
        n_inv = doc_rec['tags'].split(';')[2]
        return n_inv
  
    def _extractCodeForm(self, doc_rec):
        """
        Определить код формы БАЛАНС+.
        ВНИМАНИЕ! Код формы указывается в тегах 6-м тегом.
        """
        codf = doc_rec['tags'].split(';')[5]
        return codf
    
    def sortDocList(self, documents, sort_n_doc=None, sort_contragent=None,
                    sort_date=None, sort_inv=None):
        """
        Отсортировать список документов.
        @param documents: Список документов.
        @param sort_n_doc: Сортировать по номеру документа?
            Если не определено (None), то берется из контрола сортировки.
        @param sort_contragent: Сортировать по имени контрагента?
            Если не определено (None), то берется из контрола сортировки.
        @param sort_date: Сортировать по дате документа.
            Если не определено (None), то берется из контрола сортировки.
        @param sort_inv: Сортировать по инвентарному номеру (Основные средства).
            Если не определено (None), то берется из контрола сортировки.
        @return: Отсортированный список документов.
        """
        ctrl_sort = bool(sort_n_doc) or bool(sort_contragent) or bool(sort_date) or bool(sort_inv)
        if not ctrl_sort:
            # Если не определена никакая сортировка, 
            # то надо ее определить из контрола сортировки
            sort_selection = self.sort_radioBox.GetSelection()
            sort_n_doc = sort_selection == 0
            sort_contragent = sort_selection == 1
            sort_date = sort_selection == 2
            sort_inv = sort_selection == 3
            
        if sort_n_doc:
            # Здесь выполнена сортировка по номеру документа в виде 
            # целого числа (по первой части номера) + наименование
            # for item in self.documents:
            #    print(item['n_doc'].split(u'/')[0], ic_str.toUnicode(item['doc_name']))
            documents = sorted(documents, 
                               key=lambda item: self._extractNDoc(item))
        elif sort_contragent:
            documents = sorted(documents, 
                               key=lambda item: (item['c_agent'].upper() if item['c_agent'] else u'', 
                                                 item['doc_date'],
                                                 ic_str.get_str_digit_as_int(item['n_doc']),
                                                 item['_doc_type']), 
                               reverse=False)
        elif sort_date:
            if self.tag_choice.GetStringSelection() == u'Реализация':
                # Сортировка по дате документа для учатска реализации
                # Согласно сортировке в книге покупок и продаж в БАЛАНС+
                documents = sorted(documents,
                                   key=lambda item: (self._extractOperationDate(item),
                                                     item['doc_date'] if item['doc_date'] else datetime.datetime.now(),
                                                     self._extractCodeForm(item),
                                                     self._extractNWarehouse(item),
                                                     self._extractNDoc(item),
                                                     #item['c_agent'],
                                                     ),
                                    reverse=False)
            elif self.tag_choice.GetStringSelection() == u'Затраты на производство':
                # Сортировка по дате документа для участка затрат
                # Согласно сортировке в книге покупок и продаж в БАЛАНС+
                documents = sorted(documents,
                                   key=lambda item: (self._extractOperationDate(item),
                                                     item['doc_date'] if item['doc_date'] else datetime.datetime.now(),
                                                     self._extractCodeForm(item),
                                                     self._extractNDoc(item),
                                                     # self._extractOperationCode(item),
                                                     # self._extractNDocWarehouse(item),
                                                     # item['c_agent'],
                                                     ),
                                    reverse=False)
            else:
                # Сортировка по дате документа
                # Согласно сортировке в книге покупок и продаж в БАЛАНС+
                documents = sorted(documents,
                                   key=lambda item: (self._extractOperationDate(item),
                                                     item['doc_date'] if item['doc_date'] else datetime.datetime.now(),
                                                     self._extractCodeForm(item),
                                                     self._extractNDoc(item),
                                                     item['c_agent'],
                                                     ),
                                    reverse=False)
        elif sort_inv:
            documents = sorted(documents, 
                               key=lambda item: (self._extractInvNom(item),
                                                 item['_doc_type']), 
                               reverse=False)
        return documents

    def groupDocList(self, documents, group_n_doc=None, group_contragent=None):
        """
        Группировать список документов.
        @param documents: Список документов.
        @param group_n_doc: Группировать по номеру документа?
            Если не определено (None), то берется из контрола группировки.
        @param group_contragent: Группировать по имени контрагента?
            Если не определено (None), то берется из контрола группировки.
        @return: Сгруппированный список документов.
        """
        if group_n_doc is None and group_contragent is None:
            group_selection = self.group_radioBox.GetSelection()
            group_n_doc = False
            group_contragent = group_selection == 1
            
        if group_n_doc:
            documents = sorted(documents, key=lambda item: (self._extractNDoc(item), 
                                                            item['doc_type']))
        elif group_contragent:
            documents = sorted(documents, key=lambda item: (item['c_agent'].upper(),
                                                            self._extractNDoc(item)))
        return documents

    def clearDocList(self):
        """
        Очистка списка документов.
        """
        self.documents = list()
        
    def refreshDocList(self, dt_begin=None, dt_end=None, n_warehouse=None, 
                       ext_tag=None, ext_tag2=None):
        """
        Обновить список документов.
        """
        if dt_begin:
            self.start_datePicker.SetValue(ic_time.pydate2wxdate(dt_begin))
        if dt_end:
            self.end_datePicker.SetValue(ic_time.pydate2wxdate(dt_end))
            
        if dt_begin is None:
            dt_begin = ic_time.wxdate2pydate(self.start_datePicker.GetValue())
        if dt_end is None:
            dt_end = ic_time.wxdate2pydate(self.end_datePicker.GetValue())
        # if n_warehouse is None:
        #    n_warehouse = self.n_warehouse
        if ext_tag is None:
            selection = self.tag_choice.GetSelection()
            ext_tag = u';%s;' % self.tag_choice.GetString(selection).strip() if selection else None
        if ext_tag2 is None:
            selection = self.ext_tag_choice.GetSelection()
            ext_tag2 = u';%s;' % self.ext_tag_choice.GetString(selection).strip() if selection else None
        
        if not dt_begin or not dt_end:
            log.warning(u'Обновление списка документов. Не корректный диапазон дат')
            return 
        
        doc = ic.metadata.archive.mtd.scan_document_pack.create()
        
        dt_compare = filter_generate.create_filter_compare_requisite('doc_date', '>..<', 
                                                                     dt_begin.strftime(DEFAULT_DB_DATE_FMT),
                                                                     dt_end.strftime(DEFAULT_DB_DATE_FMT))
    
        doc_type_code = self.doc_type_ctrl.getValue()
        contragent_code = self.contragent_ctrl.getValue()
        
        compare = list()
        if doc_type_code:
            compare.append(filter_generate.create_filter_compare_requisite('doc_type', '==', doc_type_code))
        if contragent_code:
            compare.append(filter_generate.create_filter_compare_requisite('c_agent', '==', contragent_code))
        if ext_tag:
            compare.append(filter_generate.create_filter_compare_requisite('tags', '(..)', ext_tag))
        if ext_tag2:
            compare.append(filter_generate.create_filter_compare_requisite('tags', '(..)', ext_tag2))

        compare.append(dt_compare)

        #if doc_type_code and doc_type_code != '2004000000000':
        #    # ВНИМАНИЕ! Для ТТН номер указывается как номер пропуска
        #    # а он к складу не имеет никакого отношения
        #    log.debug(u'Выбранный склад: %s' % n_warehouse)
        #    wh_compare = filter_generate.create_filter_compare_requisite('n_doc', '(..', 
        #                                                                 '/%s' % n_warehouse)
        #    compare.append(wh_compare)
        
        dt_filter = filter_generate.create_filter_group_AND(*compare)        
        
        self.documents = doc.getDataDict(dt_filter)
        if not self.documents:
            log.warning(u'Пустой список документов. Фильтр <%s>' %  str(dt_filter))
        
        #if self.group_radioBox.GetSelection():
        #    # Группировка
        #    self.documents = self.groupDocList(self.documents)
        #else:
        # Сортировка
        self.documents = self.sortDocList(self.documents)
        
        rows = [(i+1, rec['n_scan_pages'],
                 u'+' if rec['is_duplex'] else u'',
                 rec['n_doc'], 
                 rec['doc_date'].strftime(DEFAULT_DB_DATE_FMT),
                 rec['n_obj'], 
                 rec['obj_date'].strftime(DEFAULT_DB_DATE_FMT) if rec['obj_date'] else u'', 
                 rec['doc_name'], 
                 rec['c_agent']) for i, rec in enumerate(self.documents)]
        
        self.setRows_list_ctrl(ctrl=self.docs_listCtrl, 
                               rows=rows,
                               evenBackgroundColour=wx.WHITE,
                               oddBackgroundColour=wx.LIGHT_GREY,
                               doSavePos=True)
        for i, doc_rec in enumerate(self.documents):
            if doc_rec['file_name'] and os.path.exists(doc_rec['file_name']):
                self.setRowForegroundColour_list_ctrl(self.docs_listCtrl, 
                                                      i, wx.Colour('DARKGREEN'))
            else:
                self.setRowForegroundColour_list_ctrl(self.docs_listCtrl, 
                                                      i, wx.Colour('DARKGOLDENROD'))
        # Количество документов и страниц в обработке
        self.doc_count_staticText.SetLabel(str(self.getScanDocCount()))
        self.page_count_staticText.SetLabel(str(self.getScanPageCount()))
        
    def onScanToolClicked(self, event):
        """
        Обработчик запуска сканирования документов.
        """
        scan_manager = ic.getScanManager()
        check_idx_list = self.getCheckedItems_list_ctrl(ctrl=self.docs_listCtrl)
        log.debug(u'Список индексов сканированных документов в пакете %s' % check_idx_list)
        # ВНИМАНИЕ! У нас указываются листы. Если указывается дуплекс, то
        # количество страниц увеличивается в 2 раза
        scan_filenames = [(os.path.join(scan_manager.getScanPath(), 'scan%04d.pdf' % i), 
                           int(self.documents[item_idx]['n_scan_pages']) * (2 if bool(self.documents[item_idx]['is_duplex']) else 1),
                           bool(self.documents[item_idx]['is_duplex'])) for i, item_idx in enumerate(check_idx_list)]
        scan_result = scan_manager.do_scan_pack(*scan_filenames)
        if not scan_result:
            event.Skip()
            log.warning(u'Ошибка сканирования пакета документов')
            return
        
        doc = ic.metadata.archive.mtd.scan_document_pack.create()
        
        if check_idx_list:
            for i, item_idx in enumerate(check_idx_list):
                scan_filename, n_pages, is_duplex = scan_filenames[i]
                if not os.path.exists(scan_filename):
                    log.warning(u'Файл скана <%s> не найден' % scan_filename)
                    continue
                doc_uuid = self.documents[item_idx]['uuid']
                doc.load_obj(doc_uuid)
                result = self.put_doc_catalog(doc, scan_filename)
                if result:
                    doc.save_obj()
                
            dlgfunc.openMsgBox(u'СКАНИРОВАНИЕ',
                            u'Сканирование пакета документов завершено успешно')
            self.refreshDocList()
        
        event.Skip()

    def onViewToolClicked(self, event):
        """
        Обработчик запуска сканирования документов.
        """
        idx = self.docs_listCtrl.GetFirstSelected()
        if idx != -1:
            document = self.documents[idx]
            doc_uuid = document['uuid']
            doc = ic.metadata.THIS.mtd.scan_document_pack.create()
            doc.load_obj(doc_uuid)
            log.debug(u'Просмотр документа UUID <%s>' % doc_uuid)
            doc_filename = doc.getRequisiteValue('file_name')
            if doc_filename and os.path.exists(doc_filename):
                self.viewDocFile(doc_filename)
            else:
                if doc_filename:
                    dlgfunc.openWarningBox(u'ВНИМАНИЕ!', u'Не найден файл скана <%s> документа для просмотра' % doc_filename)
                else:
                    dlgfunc.openWarningBox(u'ВНИМАНИЕ!', u'Отсутствует файл скана документа')
        else:
            dlgfunc.openWarningBox(u'ВНИМАНИЕ!', u'Выберите документ для просмотра')
            
        event.Skip()

    def onToggleCheckBox(self, event):
        """
        Обработчик вкл./выкл. документов в обработку.
        """
        check = event.IsChecked()
        self.checkAllItems_list_ctrl(self.docs_listCtrl, check)
        
        # Количество документов и страниц в обработке
        self.doc_count_staticText.SetLabel(str(self.getScanDocCount()))
        self.page_count_staticText.SetLabel(str(self.getScanPageCount()))
        
        event.Skip()

    def onToggleDocItem(self, event):
        """
        Обработчик вкл./выкл. документа в обработку.
        """
        # Количество документов и страниц в обработке
        self.doc_count_staticText.SetLabel(str(self.getScanDocCount()))
        self.page_count_staticText.SetLabel(str(self.getScanPageCount()))        

    def _set_doc_pages_and_duplex(self, item_idx, doc=None, doc_uuid=None, 
                                  n_scan_pages=1, is_duplex=False):
        """
        Установить количество сканированных страниц и признак дуплекса в документе.
        @param item_idx: Индекс текущего элемента списка, соответствующего документу.
        @param doc: Объект документа.
        @param doc_uuid: UUID документа.
        @param n_scan_pages: Количество сканируемых страниц.
        @param is_duplex: Признак дуплекса.
        """
        if doc is None:
            doc = ic.metadata.THIS.mtd.scan_document_pack.create()
                    
        if doc_uuid is None:
            doc_uuid = doc.getUUID()
            
        # Обновить в БД отредактированные данные
        doc.update_obj(doc_uuid, 
                       n_scan_pages=int(n_scan_pages),
                       is_duplex=int(is_duplex))
                    
        # Обновить только одну строку списка
        self.documents[item_idx]['n_scan_pages'] = int(n_scan_pages)
        self.documents[item_idx]['is_duplex'] = int(is_duplex)
        
        rec = self.documents[item_idx]
                    
        row = (item_idx+1, rec['n_scan_pages'],
               u'+' if rec['is_duplex'] else u'',
               rec['n_doc'], 
               rec['doc_date'].strftime(DEFAULT_DB_DATE_FMT),
               rec['n_obj'], 
               rec['obj_date'].strftime(DEFAULT_DB_DATE_FMT) if rec['obj_date'] else u'', 
               rec['doc_name'],                
               rec['c_agent'])
        self.setRow_list_ctrl(ctrl=self.docs_listCtrl, 
                              row_idx=item_idx,
                              row=row,
                              evenBackgroundColour=wx.WHITE,
                              oddBackgroundColour=wx.LIGHT_GREY)
        
    def _show_quick_entry_dlg(self, item_idx):
        """
        Отобразить окно быстрого ввода.
        @param item_idx: Индекс выбранного элемента.
        """
        # Получить текущую запись
        doc_rec = self.documents[item_idx]
        # Подготовить данные для редактирования
        values = dict(docname_staticText=u'%d. %s' % (item_idx + 1, doc_rec['doc_name']),
                      ndoc_staticText=doc_rec['n_doc'],
                      docdate_staticText=doc_rec['doc_date'].strftime(DEFAULT_DATE_FMT) if doc_rec['doc_date'] else u'',
                      cagent_ndoc_staticText=u'Данные контрагента: ' + (doc_rec['n_obj'] if doc_rec['n_obj'] else u''),
                      cagent_docdate_staticText=(u'от ' + doc_rec['obj_date'].strftime(DEFAULT_DATE_FMT)) if doc_rec['obj_date'] else u'',
                      npages_spinCtrl=doc_rec['n_scan_pages'],
                      duplex_checkBox=bool(doc_rec['is_duplex']))
        # Вызываем окно быстрого ввода
        edit_result = quick_entry_panel.quick_entry_edit_dlg(self, 
                                                             title=u'Режим быстрого ввода',
                                                             size=wx.Size(525, 240),
                                                             quick_entry_panel_class=icQuickEntryPackScanPanel,
                                                             defaults=values)
        if edit_result == quick_entry_panel.GO_PREV_ITEM_CMD:
            # Переход к предыдущему элементу
            self.selectItem_list_ctrl(ctrl=self.docs_listCtrl, 
                                      item_idx=item_idx - 1)
        elif edit_result == quick_entry_panel.GO_NEXT_ITEM_CMD:
            # Переход к следующему элементу
            self.selectItem_list_ctrl(ctrl=self.docs_listCtrl, 
                                      item_idx=item_idx + 1)
        elif edit_result is not None:
            # Обновить в БД отредактированные данные
            self._set_doc_pages_and_duplex(item_idx, doc_uuid=doc_rec['uuid'],
                                           n_scan_pages=edit_result['npages_spinCtrl'],
                                           is_duplex=edit_result['duplex_checkBox'])
            # Перейти на следущую строку
            self.selectItem_list_ctrl(ctrl=self.docs_listCtrl, 
                                      item_idx=item_idx + 1)                    
        
    def onSelectDocItem(self, event):
        """
        Обработчик выделения документа.
        """  
        if self.quick_entry_mode:
            item_idx = self.getItemSelectedIdx(event)
            if item_idx >= 0:
                self._show_quick_entry_dlg(item_idx)
        
        if event:
            event.Skip()

    def onQuickToolClicked(self, event):
        """
        Обработчик вкл./выкл. режима быстрого ввода.
        """
        self.quick_entry_mode = event.IsChecked()
        # Выключаем инструменты ввода
        self.ctrl_toolBar.EnableTool(self.n_pages_tool.GetId(), not self.quick_entry_mode)
        self.ctrl_toolBar.EnableTool(self.edit_tool.GetId(), not self.quick_entry_mode)
        
        item_selected_idx = self.getItemSelectedIdx(self.docs_listCtrl)
        if self.quick_entry_mode and item_selected_idx == -1:
            # Если включен режим и никакой документ не выбран, то
            # Выбираем первый элемент списка и открываем окно ввода
            self.docs_listCtrl.Select(0)
        elif self.quick_entry_mode and item_selected_idx >= 0:
            # Если выбран элемент, то просто отобразить окно быстрого ввода для 
            # этого документа
            self._show_quick_entry_dlg(item_selected_idx)
        
        event.Skip()
        
    def onClearDocTypeButtonClick(self, event):
        """
        Обработка очистки фильтра по типу документа.
        """
        self.doc_type_ctrl.setValue(None)
        self.refreshDocList()
        if event:
            event.Skip()

    def onClearContragentButtonClick(self, event):
        """
        Обработка очистки фильтра по контрагенту.
        """
        self.contragent_ctrl.setValue(None)
        self.refreshDocList()
        if event:
            event.Skip()

    def onGroupToolClicked(self, event):
        """
        Обработчик инструмента групповой настройки параметров сканирования документа.
        """
        pos = self.getToolLeftBottomPoint(self.ctrl_toolBar, self.group_tool)        
        value = group_manipulation_dlg.show_group_manipulation_dlg(self, 
                                                                   n_max=self.docs_listCtrl.GetItemCount(),
                                                                   position=pos)
        if value:
            n_begin = value.get('n_begin', 1)
            n_begin = n_begin - 1 if n_begin else 0
            n_end = value.get('n_end', self.docs_listCtrl.GetItemCount())
            n_end = n_end - 1 if n_end else self.docs_listCtrl.GetItemCount()-1
            self.checkItems_list_ctrl(self.docs_listCtrl, value.get('on_off', False), 
                                      n_begin, n_end)
            
            if value.get('n_pages', None) or value.get('is_duplex', None):
                n_pages = value.get('n_pages', None)
                n_pages = int(n_pages) if n_pages else 1
                is_duplex = value.get('is_duplex', None)
                is_duplex = bool(is_duplex) if is_duplex else False
                
                doc = ic.metadata.THIS.mtd.scan_document_pack.create()
                for i in range(n_begin, n_end + 1):
                    doc_uuid = self.documents[i]['uuid']
                    self._set_doc_pages_and_duplex(i, doc, doc_uuid,
                                                   n_pages, is_duplex)
        
            # Количество документов и страниц в обработке
            self.doc_count_staticText.SetLabel(str(self.getScanDocCount()))
            self.page_count_staticText.SetLabel(str(self.getScanPageCount()))
        event.Skip()
        
    def init(self):
        """
        Общая инициализация панели.
        """
        self.init_images()
        self.initListCtrl()
        
        # Используемые справочники
        sprav_manager = ic.metadata.archive.mtd.nsi_archive.create()
        self.contragent_sprav = sprav_manager.getSpravByName('nsi_c_agent')

        self.documents = list()

    def init_images(self):
        """
        Инициализация картинок контролов.
        """
        self.setLibImages_ToolBar(tool_bar=self.ctrl_toolBar,
                                  import_tool='import.png',
                                  view_tool='eye.png',
                                  edit_tool='document--pencil.png',
                                  scan_tool='scanner.png',
                                  archive_tool='file_manager.png',
                                  n_pages_tool='document-number.png',
                                  quick_tool='application-run.png',
                                  group_tool='document-task.png')

    def initListCtrl(self):
        """
        Инициализация списка документов.
        """
        # Добавить колонки в список
        self.setColumns_list_ctrl(ctrl=self.docs_listCtrl, 
                                  cols=((u'№', 80),
                                        ('Лист.', 40),
                                        ('2 стор.', 40),
                                        (u'№ док.', 150),
                                        (u'Дата док.', 80),
                                        (u'№ док. контрагента', 200),
                                        (u'Дата контрагента', 80),
                                        (u'Наименование', 150),
                                        ('Контрагент', 500)))


    def onStartDateChanged(self, event):
        """
        Обработчик выбора диапазона дат.
        """
        start_date = ic_time.wxdate2pydate(event.GetDate())
        end_date = ic_time.wxdate2pydate(self.end_datePicker.GetValue())
        
        if start_date > end_date:
            self.end_datePicker.SetValue(event.GetDate())
        
        self.refreshDocList()
        event.Skip()
        
    def onEndDateChanged(self, event):
        """
        Обработчик выбора диапазона дат.
        """
        start_date = ic_time.wxdate2pydate(self.start_datePicker.GetValue())
        end_date = ic_time.wxdate2pydate(event.GetDate())
        
        if start_date > end_date:
            self.start_datePicker.SetValue(event.GetDate())
            
        self.refreshDocList()
        event.Skip()

        
def open_pack_scan_doc_page(main_win=None):
    """
    Открыть страницу пакетной обработки и сканирования документов.
    @param main_win: Главное окно приложения.
    """
    if main_win is None:
        main_win = ic.getMainWin()

    page = icPackScanDocPanel(parent=main_win)
    page.init()
    main_win.addOrgPage(page, u'Пакетная обработка документов')
    return
