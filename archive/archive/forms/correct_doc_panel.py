#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Панель коррекции сканированных документов.

В случае не соответствия карточки документа 
и отсканированного экземпляра документа с помощью 
этой панели может пересканировать документ или подкорректировать карточку.
"""

import sys
import os
import os.path
import wx
import new_doc_form_proto
import datetime

import ic
from ic.log import log
from ic.dlg import dlgfunc
from ic.utils import ic_time
from ic.bitmap import bmpfunc
from ic.scanner import scanner_manager

import new_doc_panel

# Version
__version__ = (0, 0, 0, 1)


# Формат SQL выражения фильтра карточек документов по дате создания
DEFAULT_FILTER_SQL_FMT = '''-- фильтр карточек документов по дате создания
SELECT 
    scan_document_tab.uuid
FROM 
    scan_document_tab
WHERE 
    scan_document_tab.dt_create BETWEEN '%s 00:00:00' AND '%s 23:59:59'
ORDER BY 
    scan_document_tab.dt_create;
'''

DB_DATE_FMT = '%Y-%m-%d'

DEFAULT_SCAN_BMP_FILENAMES = ('/usr/share/icons/gnome/48x48/devices/scanner.png',                              
                              '/usr/share/icons/Adwaita/48x48/devices/scanner.png',
                              '/usr/share/icons/HighContrast/48x48/devices/scanner.png')


class icCorrectFilterDlg(new_doc_form_proto.icCorrectFilterDlgProto):
    """
    Диалоговое окно фильтра карточек документов по дате создания.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        new_doc_form_proto.icCorrectFilterDlgProto.__init__(self, *args, **kwargs)
        
        # Сгенерированное SQL выражение
        self.sql = ''        
        
        self.init()

    def refreshSQLCtrl(self):
        """
        Обновить контрол SQL.
        """
        wx_begin_date = self.begin_datePicker.GetValue()
        wx_end_date = self.end_datePicker.GetValue()
        
        self.sql = self.genSQL(begin_date=ic_time.wxdate2pydate(wx_begin_date),
                               end_date=ic_time.wxdate2pydate(wx_end_date))
        self.sql_textCtrl.SetValue(self.sql)
        
    def init(self):
        """
        Инициализация диалогового окна.
        """
        self.refreshSQLCtrl()
        
    def getSQL(self):
        return self.sql
    
    def genSQL(self, begin_date, end_date):
        """
        Генерация SQL.
        @param begin_date: Начальная дата.
        @param end_date: Конечная дата.
        """
        min_date = min(begin_date, end_date)
        max_date = max(begin_date, end_date)        
        
        return DEFAULT_FILTER_SQL_FMT % (min_date.strftime(DB_DATE_FMT), 
                                         max_date.strftime(DB_DATE_FMT))
        
    def onBeginDateChanged(self, event):
        """
        Обработчик изменения начальной даты фильтра.
        """
        self.refreshSQLCtrl()
        event.Skip()

    def onEndDateChanged(self, event):
        """
        Обработчик изменения конечной даты фильтра.
        """
        self.refreshSQLCtrl()
        event.Skip()

    def onCancelButtonClick(self, event):
        """
        Обработчик кнопки <Отмена>.
        """
        self.sql = ''
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        Обработчик кнопки <ОK>.
        """
        self.EndModal(wx.ID_OK)
        event.Skip()
        
        
def get_sql_correct_filter(parent=None):
    """
    Функция определения SQL выражения с помощью диалога.
    @param parent: Родительское окно.    
    """
    if parent is None:
        parent = ic.getMainWin()
    
    dlg = None
    sql = ''
    try:
        dlg = icCorrectFilterDlg(parent)
        result = dlg.ShowModal()
    
        sql = dlg.getSQL()
    except:
        log.fatal(u'Ошибка диалогового окна фильтра карточек документов по дате создания')
    
    if dlg:
        dlg.Destroy()
    return sql


class icCorrectScanDocPanel(new_doc_form_proto.icCorrectScanDocPanelProto,
                            new_doc_panel.icDocCardPanelManager):
    """
    Панель коррекции сканированных документов.
    """    

    def init(self):
        """
        Инициализация панели.
        """
        self.i_doc = -1
        
        # Список UUID документов с которыми связан текущий документ
        self._link_to_uuids = list()
        
        # Cписок обрабатываемых UUID документов
        self.doc_uuid_list = list()
        
        self.init_images()        
        self.init_ctrl()
        
        # Заблокировать кнопку регистрации нового документа
        self.doc_card_panel.reg_button.Enable(False)
    
    def init_images(self):
        """
        Инициализация образов.
        """
        bmp = bmpfunc.findBitmap(*DEFAULT_SCAN_BMP_FILENAMES)
        if bmp:
            self.doc_card_panel.scan_bpButton.SetBitmap(bmp)

    def init_ctrl(self, doc=None):
        """
        Инициализация контролов.
        """
        if doc is None:
            doc = ic.metadata.archive.mtd.scan_document.create()
            doc_uuid = self.getCurrentDocUUID()
            doc.load_obj(doc_uuid)
        # Колонки списка связей
        requisites = [requisite for requisite in doc.getChildrenRequisites() if requisite.isDescription()]
        for i, requisite in enumerate(requisites):
            self.doc_card_panel.link_listCtrl.InsertColumn(i, requisite.getLabel(),
                                                           width=wx.LIST_AUTOSIZE)
        # Перепривязать обработчики кнопок
        self.doc_card_panel.scan_bpButton.Bind(wx.EVT_BUTTON, self.onScanButtonClick)
        self.doc_card_panel.add_link_button.Bind(wx.EVT_BUTTON, self.onAddLinkButtonClick)
        self.doc_card_panel.del_link_button.Bind(wx.EVT_BUTTON, self.onDelLinkButtonClick)

        # Отключить все контролы редактирования
        self.off_ctrl()
        
        # Выключить кнопку сохранения
        self.ctrl_toolBar.EnableTool(self.save_tool.GetId(), False)
        
    def setDocUUIDList(self, *doc_uuid_list):
        """
        Установить список обрабатываемых UUID документов.
        @param doc_uuid_list: Список UUID документов.
        """
        self.doc_uuid_list = doc_uuid_list
        self.i_doc = 0 if self.doc_uuid_list else -1
        
        self.refreshDocIdx(self.i_doc)

    def getCurrentDocUUID(self, doc_idx=None):
        """
        UUID текущего документа.
        @param doc_idx: Индекс в списке обрабатываемых документов.
        """
        if doc_idx is None:
            pass
        elif isinstance(doc_idx, int) and doc_idx < 0:
            log.warning(u'Не определен индекс документа для коррекции')
            return None
        else:
            self.i_doc = doc_idx
        
        doc_uuid = None
        try:
            if self.i_doc >= 0:
                doc_uuid = self.doc_uuid_list[self.i_doc]
        except ValueError:
            log.warning(u'Не корректный индекс документа для коррекции')
        return doc_uuid
        
    def getCurrentDoc(self, doc_idx=None):
        """
        Текущий обрабатываемый документ.
        """
        doc_uuid = self.getCurrentDocUUID(doc_idx)
                
        doc = None
        if doc_uuid:
            doc = ic.metadata.archive.mtd.scan_document.create()
            doc.load_obj(doc_uuid)            
        return doc
        
    def refreshDocIdx(self, doc_idx=None):
        """
        Обновить карточку текущего документа.
        @param doc_idx: Индекс в списке обрабатываемых документов.
        """
        doc = self.getCurrentDoc(doc_idx)
        if doc:
            self.set_data(doc)
            
            label = '/%d' % len(self.doc_uuid_list)
            self.idx_staticText.SetLabel(label)
            self.card_spinCtrl.SetRange(1, len(self.doc_uuid_list))
            self.card_spinCtrl.SetValue(self.i_doc + 1)            
            
            
    def onAddLinkButtonClick(self, event):
        """
        Обработчик кнопки <Добавить>.
        """
        doc = ic.metadata.THIS.mtd.scan_document.create()
        docs_uuid = search_doc_form.choice_docs_dlg()
        
        if docs_uuid:
            for doc_uuid in docs_uuid:
                doc_data = doc.loadRequisiteData(doc_uuid)
                if not self.valid_link(doc_uuid):
                    log.warning(u'Попытка добавления уже существующей связи с документом')
                    dlgfunc.openWarningBox(u'ВНИМАНИЕ', u'Связь с документом <%s> уже есть в списке' % doc_data.get('doc_name', u'-'))
                    continue
            
                self._link_to_uuids.append(doc_uuid)
            
                self._addLinkCtrl(doc, doc_uuid)

        event.Skip()

    def onDelLinkButtonClick(self, event):
        """
        Обработчик кнопки <Удалить>.
        """
        idx = self.doc_card_panel.link_listCtrl.GetFirstSelected()
        if idx != -1:
            del self._link_to_uuids[idx]
            self.doc_card_panel.link_listCtrl.DeleteItem(idx)
        event.Skip()

    def _addLinkCtrl(self, doc, link_to):
        """
        Добавить связь в контрол списка.
        @param doc: Объект документа.
        @param link_to: UUID документа, на который ссылаемся.
        """
        if link_to not in self._link_to_uuids:
            self._link_to_uuids.append(link_to)
        
        doc.load_obj(link_to)
        requisites = [requisite for requisite in doc.getChildrenRequisites() if requisite.isDescription()]
        
        row_idx = 0
        for i, requisite in enumerate(requisites):

            if requisite.__class__.__name__ == 'icNSIRequisite':
                value = requisite.getStrData()
            else:
                value = requisite.getValue()

            if isinstance(value, datetime.datetime):
                value = value.strftime(DB_DATE_FMT)
            elif not isinstance(value, str):
                value = str(value)

            if i == 0:
                row_idx = self.doc_card_panel.link_listCtrl.InsertItem(sys.maxsize, value, i)
            else:
                self.doc_card_panel.link_listCtrl.SetItem(row_idx, i, value)

    def _addLinksCtrl(self, doc, links_to):
        """
        Добавление нескольких связей в контрол списка связей.
        @param doc: Объект документа.
        @param links_to: Список UUID документов, на которые ссылаемся.
        """
        for link_to in links_to:
            self._addLinkCtrl(doc, link_to['link_to'] if 'link_to' in link_to else link_to)

        # Обновить размер колонок
        requisites = [requisite for requisite in doc.getChildrenRequisites() if requisite.isDescription()]
        for i in range(len(requisites)):
            self.doc_card_panel.link_listCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE)

    def set_data(self, doc):
        """
        Расставить значения реквизитов редактируеиого документа в контролы.
        """
        # Расставляем значения реквизитов в контролы
        self.doc_card_panel.select_filePicker.SetPath(doc.getRequisiteValue('file_name'))
        
        self.doc_card_panel.ndoc_textCtrl.SetValue(doc.getRequisiteValue('n_doc'))
        doc_date = doc.getRequisiteValue('doc_date')
        wx_doc_date = ic_time.pydate2wxdate(doc_date)
        self.doc_card_panel.doc_datePicker.SetValue(wx_doc_date)
        self.doc_card_panel.docname_textCtrl.SetValue(doc.getRequisiteValue('doc_name'))
        
        doc_type_code = doc.getRequisiteValue('doc_type')
        log.debug(u'edit. Установка данных. Код вида документа <%s>' % doc_type_code)
        self.doc_card_panel.doc_type_ctrl.setValue(doc_type_code)
        
        self.doc_card_panel.contragent_ctrl.setValue(doc.getRequisiteValue('c_agent'))
        
        entity_code = doc.getRequisiteValue('entity')
        log.debug(u'edit. Установка данных. Код подразделения <%s>' % entity_code)
        self.doc_card_panel.entity_ctrl.setValue(entity_code)
        
        self.doc_card_panel.description_textCtrl.SetValue(doc.getRequisiteValue('description'))
        self.doc_card_panel.comment_textCtrl.SetValue(doc.getRequisiteValue('comment'))
        tags = doc.getRequisiteValue('tags').split(';')
        tags += [u''] * (10-len(tags))
        self.doc_card_panel.tag0_textCtrl.SetValue(tags[0])
        self.doc_card_panel.tag1_textCtrl.SetValue(tags[1])
        self.doc_card_panel.tag2_textCtrl.SetValue(tags[2])
        self.doc_card_panel.tag3_textCtrl.SetValue(tags[3])
        self.doc_card_panel.tag4_textCtrl.SetValue(tags[4])
        self.doc_card_panel.tag5_textCtrl.SetValue(tags[5])
        self.doc_card_panel.tag6_textCtrl.SetValue(tags[6])
        self.doc_card_panel.tag7_textCtrl.SetValue(tags[7])
        self.doc_card_panel.tag8_textCtrl.SetValue(tags[8])
        self.doc_card_panel.tag9_textCtrl.SetValue(tags[9])

        links_to = doc.getRequisiteValue('scan_doc_to')
        doc = ic.metadata.THIS.mtd.scan_document.create()
        self._addLinksCtrl(doc, links_to)

    def get_data(self, doc):
        """
        Записать данные в редактируемый документ из контролов.
        """
        data = self.get_data_ctrl()

        if self.valid(data):
            doc.setRequisiteValue('n_doc', data['n_doc'])
            doc.setRequisiteValue('doc_date', data['doc_date'])
            doc.setRequisiteValue('doc_name', data['doc_name'])
            doc.setRequisiteValue('doc_type', data['doc_type'])
            doc.setRequisiteValue('c_agent', data['c_agent'])
            doc.setRequisiteValue('entity', data['entity'])
            doc.setRequisiteValue('description', data['description'])
            doc.setRequisiteValue('comment', data['comment'])
            doc.setRequisiteValue('tags', data['tags'])
            links_to = [dict(link_to=doc_uuid) for doc_uuid in data['links_to']]
            doc.setRequisiteValue('scan_doc_to', links_to)
        return doc

    def get_data_ctrl(self):
        """
        Получить данные из контролов в виде словаря.
        """
        filename = self.doc_card_panel.select_filePicker.GetPath().strip()
        docnum = self.doc_card_panel.ndoc_textCtrl.GetValue().strip()
        wx_docdate = self.doc_card_panel.doc_datePicker.GetValue()
        docdate = ic_time.wxdate2pydate(wx_docdate)
        docname = self.doc_card_panel.docname_textCtrl.GetValue().strip()
        doctype = self.doc_card_panel.doc_type_ctrl.getValue()
        contragent = self.doc_card_panel.contragent_ctrl.getValue()
        entity = self.doc_card_panel.entity_ctrl.getValue()
        description = self.doc_card_panel.description_textCtrl.GetValue().strip()
        comment = self.doc_card_panel.comment_textCtrl.GetValue().strip()
        tag0 = self.doc_card_panel.tag0_textCtrl.GetValue().strip()
        tag1 = self.doc_card_panel.tag1_textCtrl.GetValue().strip()
        tag2 = self.doc_card_panel.tag2_textCtrl.GetValue().strip()
        tag3 = self.doc_card_panel.tag3_textCtrl.GetValue().strip()
        tag4 = self.doc_card_panel.tag4_textCtrl.GetValue().strip()
        tag5 = self.doc_card_panel.tag5_textCtrl.GetValue().strip()
        tag6 = self.doc_card_panel.tag6_textCtrl.GetValue().strip()
        tag7 = self.doc_card_panel.tag7_textCtrl.GetValue().strip()
        tag8 = self.doc_card_panel.tag8_textCtrl.GetValue().strip()
        tag9 = self.doc_card_panel.tag9_textCtrl.GetValue().strip()
        tags = [tag0, tag1, tag2, tag3, tag4, tag5, tag6, tag7, tag8, tag9]
        tags = [tag for tag in tags if tag]
        tags = ';'.join(tags)
        links_to = self._link_to_uuids
        return dict(file_name=filename,
                    n_doc=docnum, doc_date=docdate, doc_name=docname,
                    doc_type=doctype, c_agent=contragent, entity=entity,
                    description=description, comment=comment,
                    tags=tags, links_to=links_to)

    def onPrevToolClicked(self, event):
        """
        Обработчик инструмента <Предыдущий документ>.
        """
        self.i_doc = max(0, self.i_doc - 1)        
        self.refreshDocIdx(self.i_doc)
        event.Skip()

    def onNextToolClicked(self, event):
        """
        Обработчик инструмента <Следующий документ>.
        """
        self.i_doc = min(len(self.doc_uuid_list) - 1, self.i_doc + 1)        
        self.refreshDocIdx(self.i_doc)
        event.Skip()

    def onEditToolClicked(self, event):
        """
        Обработчик инструмента переключения в режим редактирования карточки документа.
        """
        is_on = event.IsChecked()
        self.ctrl_toolBar.EnableTool(self.save_tool.GetId(), is_on)
        self.ctrl_toolBar.EnableTool(self.prev_tool.GetId(), not is_on)
        self.ctrl_toolBar.EnableTool(self.next_tool.GetId(), not is_on)
        if is_on:
            self.on_ctrl()
        else:
            self.off_ctrl()
        event.Skip()

    def onSaveToolClicked(self, event):
        """
        Обработчик инструмента сохранения.
        """
        self.ctrl_toolBar.EnableTool(self.save_tool.GetId(), False)
        self.ctrl_toolBar.EnableTool(self.prev_tool.GetId(), True)
        self.ctrl_toolBar.EnableTool(self.next_tool.GetId(), True)
        
        self.off_ctrl()        
        self.ctrl_toolBar.ToggleTool(self.edit_tool.GetId(), False)
        
        doc = self.getCurrentDoc()
        self.get_data(doc)
        # А теперь размещаем объект в каталоге
        scan_filename = self.doc_card_panel.select_filePicker.GetPath()
        self.put_doc_catalog(doc, scan_filename)
        doc.save_obj()
        
        event.Skip()
        
    def onViewToolClicked(self, event):
        """
        Обработчик инструмента просмотра PDF сканированного документа.
        """
        doc = self.getCurrentDoc()
        if doc:
            doc_filename = doc.getRequisiteValue('file_name')
            if doc_filename:
                self.viewDocFile(doc_filename)
            else:
                log.warning(u'Не определен файл для просмотра')
        else:
            log.warning(u'Не определен документ для просмотра')
        event.Skip()

    def enable_ctrl(self, enable=True):
        """
        Вкл/выкл контролы формы.
        """
        self.doc_card_panel.scan_bpButton.Enable(enable)
        self.doc_card_panel.select_filePicker.Enable(enable)
        self.doc_card_panel.ndoc_textCtrl.Enable(enable)
        self.doc_card_panel.doc_datePicker.Enable(enable)
        self.doc_card_panel.docname_textCtrl.Enable(enable)
        self.doc_card_panel.doc_type_ctrl.Enable(enable)
        self.doc_card_panel.contragent_ctrl.Enable(enable)
        self.doc_card_panel.entity_ctrl.Enable(enable)
        self.doc_card_panel.description_textCtrl.Enable(enable)
        self.doc_card_panel.comment_textCtrl.Enable(enable)
        self.doc_card_panel.tag0_textCtrl.Enable(enable)
        self.doc_card_panel.tag1_textCtrl.Enable(enable)
        self.doc_card_panel.tag2_textCtrl.Enable(enable)
        self.doc_card_panel.tag3_textCtrl.Enable(enable)
        self.doc_card_panel.tag4_textCtrl.Enable(enable)
        self.doc_card_panel.tag5_textCtrl.Enable(enable)
        self.doc_card_panel.tag6_textCtrl.Enable(enable)
        self.doc_card_panel.tag7_textCtrl.Enable(enable)
        self.doc_card_panel.tag8_textCtrl.Enable(enable)
        self.doc_card_panel.tag9_textCtrl.Enable(enable)
        
    def off_ctrl(self):
        """
        Выкл контролы формы.
        """
        self.enable_ctrl(False)

    def on_ctrl(self):
        """
        Вкл контролы формы.
        """
        self.enable_ctrl(True)

    def onScanButtonClick(self, event):
        """
        Запуск сканирования.
        """
        scanner_mgr = scanner_manager.icScannerManager()
        # Перед сканированием удалить сканированный ранее файл
        if os.path.exists(new_doc_panel.DEFAULT_SCAN_FILENAME):
            os.remove(new_doc_panel.DEFAULT_SCAN_FILENAME)
        # Запуск сканирования
        result = scanner_mgr.do_scan_export(new_doc_panel.DEFAULT_SCAN_FILENAME)
        
        if result and os.path.exists(new_doc_panel.DEFAULT_SCAN_FILENAME):
            # Если файл существует, то значит сканирование прошло успешно
            self.doc_card_panel.select_filePicker.SetInitialDirectory(os.path.dirname(new_doc_panel.DEFAULT_SCAN_FILENAME))
            self.doc_card_panel.select_filePicker.SetPath(new_doc_panel.DEFAULT_SCAN_FILENAME)
        else:
            log.warning(u'Файл сканирования не найден')
            self.doc_card_panel.select_filePicker.SetPath(u'')
        
        event.Skip()                

    def onCardSpinCtrlText(self, event):
        """
        Обработчик изменения номера документа в списке.
        """
        spin_idx = self.card_spinCtrl.GetValue()
        self.i_doc = spin_idx - 1
        
        doc = self.getCurrentDoc()
        if doc:
            self.set_data(doc)
            
        event.Skip()
        
        
def open_correct_doc_panel(parent=None):
    """
    Открыть панель коррекции отсканированных документов.
    @param parent: Родительское окно.
    """
    if parent is None:
        parent = ic.getMainWin()        
    
    sql = get_sql_correct_filter(parent)
    if sql:
        # Отфильтровать записи
        db = ic.metadata.archive.src.archive_db.create()
        recordset = db.executeSQL(sql, to_dict=True)
        doc_uuid_lst = [rec['uuid'] for rec in recordset['__data__']] if recordset else list()
        
        main_win = ic.getMainWin()
        page = icCorrectScanDocPanel(parent=main_win)        
        page.init()        
        page.setDocUUIDList(*doc_uuid_lst)
        main_win.addOrgPage(page, u'Коррекция сканированных документов')        
    else:
        # Нажата <отмена> или ошибка
        pass
