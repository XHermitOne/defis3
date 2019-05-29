#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Формы поиска отсканированных документов.
"""

import sys
import os
import os.path
import wx
import sqlalchemy

from archive.forms import search_doc_form_proto
from archive.forms import scheme_doc_form
from archive.forms import browse_doc_links_panel
from ic import ic_bmp
from ic import log
from ic import ic_dlg
import ic
from ic.utils import ic_time

# Version
__version__ = (0, 1, 1, 1)


DEFAULT_DATE_FMT = '%Y.%m.%d'


class icSearchCritPanelCtrl:
    """
    Класс функций обработки панели выбора критериев поиска документов.
    """

    pass


class icSearchDocPanelCtrl(icSearchCritPanelCtrl):
    """
    Класс функций обработки панели поиска документов.
    """

    def init_images(self):
        """
        Инициализация картинок контролов.
        """
        # <wx.Tool>
        bmp = ic_bmp.createLibraryBitmap('eye.png')
        tool_id = self.view_tool.GetId()
        # ВНИМАНИЕ! Для смены образа инструмента не надо использовать
        # метод инструмента <tool.SetNormalBitmap(bmp)> т.к. НЕ РАБОТАЕТ!
        # Для этого вызываем метод панели инструметнтов
        # <toolbar.SetToolNormalBitmap(tool_id, bmp)>
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)

        bmp = ic_bmp.createLibraryBitmap('document--pencil.png')
        tool_id = self.edit_tool.GetId()
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)

        bmp = ic_bmp.createLibraryBitmap('schema.png')
        tool_id = self.scheme_tool.GetId()
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)

        bmp = ic_bmp.createLibraryBitmap('chain.png')
        tool_id = self.links_tool.GetId()
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)
        
        bmp = ic_bmp.createLibraryBitmap('application-dock-090.png')
        tool_id = self.collapse_tool.GetId()
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)

        bmp = ic_bmp.createLibraryBitmap('application-dock-270.png')
        tool_id = self.expand_tool.GetId()
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)

        self.ctrl_toolBar.Realize()

    def initListCtrl(self):
        """
        Инициализация списка документов.
        """
        # Добавить колонки в список
        self.docs_listCtrl.ClearAll()
        self.docs_listCtrl.InsertColumn(0, u'№', width=100)
        self.docs_listCtrl.InsertColumn(1, u'Дата', width=80)
        self.docs_listCtrl.InsertColumn(2, u'№ док. контрагента', width=100)
        self.docs_listCtrl.InsertColumn(3, u'Дата конрагента', width=80)
        self.docs_listCtrl.InsertColumn(4, u'Наименование', width=500)
        self.docs_listCtrl.InsertColumn(5, u'Описание', width=200)
        self.docs_listCtrl.InsertColumn(6, u'Коментарии', width=200)

    def init(self):
        """
        Общая инициализация панели.
        """
        self.init_images()
        self.initListCtrl()

        self.ctrl_toolBar.EnableTool(self.expand_tool.GetId(), False)
        self._last_sash_position = 0

        self.documents = list()

    def onClearButtonClick(self, event):
        """
        Обработчик кнопки <Очистить>.
        """
        self.search_crit_panel.docnum_textCtrl.SetValue(u'')
        self.search_crit_panel.docname_textCtrl.SetValue(u'')
        self.search_crit_panel.doc_type_ctrl.setValue(None)
        self.search_crit_panel.contragent_ctrl.setValue(None)
        self.search_crit_panel.entity_ctrl.setValue(None)
        self.search_crit_panel.description_textCtrl.SetValue(u'')
        self.search_crit_panel.comment_textCtrl.SetValue(u'')
        self.search_crit_panel.tag0_textCtrl.SetValue(u'')
        self.search_crit_panel.tag1_textCtrl.SetValue(u'')
        self.search_crit_panel.tag2_textCtrl.SetValue(u'')
        self.search_crit_panel.tag3_textCtrl.SetValue(u'')
        self.search_crit_panel.tag4_textCtrl.SetValue(u'')
        self.search_crit_panel.tag5_textCtrl.SetValue(u'')
        self.search_crit_panel.tag6_textCtrl.SetValue(u'')
        self.search_crit_panel.tag7_textCtrl.SetValue(u'')
        self.search_crit_panel.tag8_textCtrl.SetValue(u'')
        self.search_crit_panel.tag9_textCtrl.SetValue(u'')
        self.search_crit_panel.orderby_choice.SetSelection(wx.NOT_FOUND)
        self.search_crit_panel.orderby_checkBox.SetValue(False)

        self.search_crit_panel.date_checkBox.SetValue(False)
        self.search_crit_panel.one_date_checkBox.SetValue(False)        
        self.search_crit_panel.doc_type_checkBox.SetValue(False)
        self.search_crit_panel.entity_checkBox.SetValue(False)
        self.search_crit_panel.contragent_checkBox.SetValue(False)
        
        self.search_crit_panel.one_date_checkBox.Enable(False)        
        self.search_crit_panel.start_datePicker.Enable(False)
        self.search_crit_panel.end_datePicker.Enable(False)                
        self.search_crit_panel.doc_type_ctrl.Enable(False)
        self.search_crit_panel.entity_ctrl.Enable(False)
        self.search_crit_panel.contragent_ctrl.Enable(False)
                
        event.Skip()

    def search_doc_data(self, docnum, nobj, docname, 
                        docdate_start, docdate_end, 
                        objdate_start, objdate_end, 
                        doctype, contragent, entity,
                        description, comment,
                        tag0, tag1, tag2, tag3, tag4, tag5, tag6, tag7, tag8, tag9):
        """
        Получение списка записей удовлетворяющих критериям поиска.
        """
        tab = ic.metadata.THIS.tab.scan_document_tab.create()

        where = list()
        if docnum and self.search_crit_panel.docnum_radioBox.GetSelection():
            where.append(tab.c.n_doc == docnum)
        elif docnum and not self.search_crit_panel.docnum_radioBox.GetSelection():
            where.append(tab.c.n_doc.ilike(u'%'+docnum+u'%'))

        if nobj and self.search_crit_panel.nobj_radioBox.GetSelection():
            where.append(tab.c.n_obj == nobj)
        elif nobj and not self.search_crit_panel.nobj_radioBox.GetSelection():
            where.append(tab.c.n_obj.ilike(u'%'+nobj+u'%'))

        if docname:
            where.append(tab.c.doc_name.ilike(u'%'+docname+u'%'))

        if docdate_start and docdate_end:
            if docdate_start == docdate_end:
                where.append(tab.c.doc_date == docdate_start)
            else:
                where.append(tab.c.doc_date.between(docdate_start, docdate_end))

        if objdate_start and objdate_end:
            if objdate_start == objdate_end:
                where.append(tab.c.obj_date == objdate_start)
            else:
                where.append(tab.c.obj_date.between(objdate_start, objdate_end))

        if doctype:
            where.append(tab.c.doc_type == doctype)

        if contragent:
            if isinstance(contragent, list):
                # Контрагенты могут задаваться списком
                contragent_where = [tab.c.c_agent == contragent_cod for contragent_cod in contragent]
                where.append(sqlalchemy.or_(*contragent_where))
            else:
                # Контрагент задается просто кодом
                where.append(tab.c.c_agent == contragent)

        if entity:
            where.append(tab.c.entity == entity)

        if description:
            where.append(tab.c.description.ilike(u'%'+description+u'%'))
        if comment:
            where.append(tab.c.comment.ilike(u'%'+comment+u'%'))

        tags = [tag0, tag1, tag2, tag3, tag4, tag5, tag6, tag7, tag8, tag9]
        tags = [tag for tag in tags if tag]
        for tag in tags:
            where.append(tab.c.tags.ilike(u'%'+tag+u'%'))

        query = tab.dataclass.select().where(sqlalchemy.and_(*where))

        # Сортировка
        orderby_idx = self.search_crit_panel.orderby_choice.GetSelection()
        is_desc = self.search_crit_panel.orderby_checkBox.GetValue()
        if orderby_idx == 1:
            query = query.order_by(tab.c.n_doc) if not is_desc else query.order_by(sqlalchemy.desc(tab.c.n_doc))
        elif orderby_idx == 2:
            query = query.order_by(tab.c.doc_name) if not is_desc else query.order_by(sqlalchemy.desc(tab.c.doc_name))
        elif orderby_idx == 3:
            query = query.order_by(tab.c.doc_date) if not is_desc else query.order_by(sqlalchemy.desc(tab.c.doc_date))

        recordset = query.execute()
        # Преобразовать рекорсет в список словарей записей
        records = [dict(rec) for rec in recordset]

        if not records:
            log.warning(u'Пустое значение поиска по параметрам:')
            log.warning(u'\tНомер документа <%s>' % docnum)
            log.warning(u'\tНаименование документа <%s>' % docname)
            log.warning(u'\tТип документа <%s>' % doctype)
            log.warning(u'\tКонтрагент <%s>' % contragent)
            log.warning(u'\tПодразделение <%s>' % entity)
            log.warning(u'\tОписание <%s>' % description)
            log.warning(u'\tКомментарии <%s>' % comment)
            log.warning(u'\tТэги [%s : %s : %s : %s : %s : %s : %s : %s : %s : %s]' % (tag0, tag1, tag2, tag3, tag4, tag5, tag6, tag7, tag8, tag9))

        return records

    def onSearchButtonClick(self, event):
        """
        Обработчик кнопки <Искать>.
        """
        # Определение критериев поиска
        docnum = self.search_crit_panel.docnum_textCtrl.GetValue().strip()
        nobj = self.search_crit_panel.nobj_textCtrl.GetValue().strip()
        docname = self.search_crit_panel.docname_textCtrl.GetValue().strip()
        
        wx_date = self.search_crit_panel.start_datePicker.GetValue()
        docdate_start = ic_time.wxdate2pydate(wx_date) if self.search_crit_panel.date_checkBox.IsChecked() else None
        wx_date = self.search_crit_panel.end_datePicker.GetValue()
        docdate_end = ic_time.wxdate2pydate(wx_date) if self.search_crit_panel.date_checkBox.IsChecked() else None
        
        wx_date = self.search_crit_panel.obj_start_datePicker.GetValue()
        objdate_start = ic_time.wxdate2pydate(wx_date) if self.search_crit_panel.obj_date_checkBox.IsChecked() else None
        wx_date = self.search_crit_panel.obj_end_datePicker.GetValue()
        objdate_end = ic_time.wxdate2pydate(wx_date) if self.search_crit_panel.obj_date_checkBox.IsChecked() else None

        doctype = self.search_crit_panel.doc_type_ctrl.getValue()
        contragent = self.search_crit_panel.contragent_ctrl.getValue()
        entity = self.search_crit_panel.entity_ctrl.getValue()
        description = self.search_crit_panel.description_textCtrl.GetValue().strip()
        comment = self.search_crit_panel.comment_textCtrl.GetValue().strip()
        tag0 = self.search_crit_panel.tag0_textCtrl.GetValue().strip()
        tag1 = self.search_crit_panel.tag1_textCtrl.GetValue().strip()
        tag2 = self.search_crit_panel.tag2_textCtrl.GetValue().strip()
        tag3 = self.search_crit_panel.tag3_textCtrl.GetValue().strip()
        tag4 = self.search_crit_panel.tag4_textCtrl.GetValue().strip()
        tag5 = self.search_crit_panel.tag5_textCtrl.GetValue().strip()
        tag6 = self.search_crit_panel.tag6_textCtrl.GetValue().strip()
        tag7 = self.search_crit_panel.tag7_textCtrl.GetValue().strip()
        tag8 = self.search_crit_panel.tag8_textCtrl.GetValue().strip()
        tag9 = self.search_crit_panel.tag9_textCtrl.GetValue().strip()

        # Формирование запроса
        self.documents = self.search_doc_data(docnum, nobj, docname, 
                                              docdate_start, docdate_end, 
                                              objdate_start, objdate_end, 
                                              doctype, contragent, entity,
                                              description, comment,
                                              tag0, tag1, tag2, tag3, tag4, tag5, tag6, tag7, tag8, tag9)

        # Заполнить список документов
        self.refreshDocList()
        
        # Отобразить количество найденных документов
        doc_count = len(self.documents) if self.documents else 0
        self.search_count_staticText.SetLabel(str(doc_count))

        event.Skip()
        
    def refreshDocList(self):
        """
        Обновление списка документов.
        """
        self.docs_listCtrl.DeleteAllItems()
        for record in self.documents:
            row_idx = self.docs_listCtrl.InsertItem(sys.maxsize, record.get('n_doc', u''))
            
            str_doc_date = record['doc_date'].strftime(DEFAULT_DATE_FMT) if record.get('doc_date', None) else u''
            self.docs_listCtrl.SetItem(row_idx, 1, str_doc_date)
            
            self.docs_listCtrl.SetItem(row_idx, 2, record.get('n_obj', u''))
            
            str_obj_date = record['obj_date'].strftime(DEFAULT_DATE_FMT) if record.get('obj_date', None) else u''
            self.docs_listCtrl.SetItem(row_idx, 3, str_obj_date)
            
            self.docs_listCtrl.SetItem(row_idx, 4, record.get('doc_name', u''))
            
            description = record.get('description', u'')
            description = description if isinstance(description, str) else u''
            self.docs_listCtrl.SetItem(row_idx, 5, description)
            
            comment = record.get('comment', u'')
            comment = comment if isinstance(comment, str) else u''
            self.docs_listCtrl.SetItem(row_idx, 6, comment)

    def onViewToolClicked(self, event):
        """
        Обработчик инструмента просмотра документа.
        """
        idx = self.docs_listCtrl.GetFirstSelected()
        if idx != -1:
            document = self.documents[idx]
            doc_filename = document['file_name']
            if not os.path.exists(doc_filename):
                log.warning(u'Файл <%s> не найден для просмотра' % doc_filename)
                event.Skip()
                return

            doc_file_ext = os.path.splitext(doc_filename)[1].lower()
            cmd = u''
            if doc_file_ext == '.pdf':
                cmd = u'evince %s&' % doc_filename
            elif doc_file_ext in ('.jpg', '.jpeg', '.tiff', '.bmp'):
                cmd = u'eog %s&' % doc_filename
            else:
                log.warning(u'Не поддерживаемый тип файла <%s>' % doc_file_ext)
            if cmd:
                os.system(cmd)
        else:
            ic_dlg.icWarningBox(u'ВНИМАНИЕ!', u'Выберите документ')

        event.Skip()

    def onEditToolClicked(self, event):
        """
        Обработчик инструмента редактирования документа.
        """
        idx = self.docs_listCtrl.GetFirstSelected()
        if idx != -1:
            document = self.documents[idx]
            doc_uuid = document['uuid']
            doc = ic.metadata.THIS.mtd.scan_document.create()
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
            ic_dlg.icWarningBox(u'ВНИМАНИЕ!', u'Выберите документ')

        event.Skip()

    def onSchemeToolClicked(self, event):
        """
        Обработчик инструмента редактирования документа.
        """
        idx = self.docs_listCtrl.GetFirstSelected()
        if idx != -1:
            document = self.documents[idx]
            doc_uuid = document['uuid']
            doc = ic.metadata.THIS.mtd.scan_document.create()
            doc.load_obj(doc_uuid)
            log.debug(u'Показать схему документа UUID <%s>' % doc_uuid)
            scheme = doc.GetManager().get_scheme_data()

            main_win = ic.getMainWin()
            scheme_page = scheme_doc_form.icSchemeDocPanel(parent=main_win)
            scheme_page.init()
            scheme_page.scheme_viewer_ctrl.setDiagram(scheme)
            main_win.AddOrgPage(scheme_page, u'Схема документа <%s>' % doc.getRequisiteValue('doc_name'))
        else:
            ic_dlg.icWarningBox(u'ВНИМАНИЕ!', u'Выберите документ')

        event.Skip()

    def onLinksToolClicked(self, event):
        """
        Обработчик инструмента просмотра связей с документом.
        """
        idx = self.docs_listCtrl.GetFirstSelected()
        if idx != -1:
            document = self.documents[idx]
            doc_uuid = document['uuid']
            doc = ic.metadata.THIS.mtd.scan_document.create()
            doc.load_obj(doc_uuid)
            log.debug(u'Показать связи документа UUID <%s>' % doc_uuid)

            browse_doc_links_panel.browse_doc_links_panel(doc)
        else:
            ic_dlg.icWarningBox(u'ВНИМАНИЕ!', u'Выберите документ')
        
        event.Skip()

    def onDateCheckBox(self, event):
        """
        Обработчик выбора флага поиска по дате.
        """
        check = event.IsChecked()
        self.search_crit_panel.start_datePicker.Enable(check)
        self.search_crit_panel.end_datePicker.Enable(check)
        self.search_crit_panel.one_date_checkBox.Enable(check)
        event.Skip()

    def onOneDateCheckBox(self, event):
        """
        Обработчик выбора флага поиска на определенную дату.
        """
        check = event.IsChecked()
        if check:
            self.search_crit_panel.end_datePicker.SetValue(self.search_crit_panel.start_datePicker.GetValue())
            self.search_crit_panel.end_datePicker.Enable(False)
        else:
            self.search_crit_panel.end_datePicker.Enable(True)

        event.Skip()

    def onStartDatePickerChanged(self, event):
        """
        Обработчик изменения начальной даты документа для поиска.
        """
        wx_date = event.GetDate()
        if self.search_crit_panel.end_datePicker.IsEnabled() and wx_date > self.search_crit_panel.end_datePicker.GetValue():
            self.search_crit_panel.end_datePicker.SetValue(wx_date)
        elif not self.search_crit_panel.end_datePicker.IsEnabled():
            self.search_crit_panel.end_datePicker.SetValue(wx_date)
        event.Skip()

    def onEndDatePickerChanged(self, event):
        """
        Обработчик изменения конечной даты документа для поиска.
        """
        wx_date = event.GetDate()
        if self.search_crit_panel.start_datePicker.IsEnabled() and wx_date < self.search_crit_panel.start_datePicker.GetValue():
            self.search_crit_panel.start_datePicker.SetValue(wx_date)
        elif not self.search_crit_panel.start_datePicker.IsEnabled():
            self.search_crit_panel.start_datePicker.SetValue(wx_date)
        event.Skip()

    def onObjDateCheckBox(self, event):
        """
        Обработчик выбора флага поиска по дате.
        """
        check = event.IsChecked()
        self.search_crit_panel.obj_start_datePicker.Enable(check)
        self.search_crit_panel.obj_end_datePicker.Enable(check)
        self.search_crit_panel.obj_one_date_checkBox.Enable(check)
        event.Skip()

    def onObjOneDateCheckBox(self, event):
        """
        Обработчик выбора флага поиска на определенную дату.
        """
        check = event.IsChecked()
        if check:
            self.search_crit_panel.obj_end_datePicker.SetValue(self.search_crit_panel.obj_start_datePicker.GetValue())
            self.search_crit_panel.obj_end_datePicker.Enable(False)
        else:
            self.search_crit_panel.obj_end_datePicker.Enable(True)

        event.Skip()

    def onObjStartDatePickerChanged(self, event):
        """
        Обработчик изменения начальной даты документа для поиска.
        """
        wx_date = event.GetDate()
        if self.search_crit_panel.obj_end_datePicker.IsEnabled() and wx_date > self.search_crit_panel.obj_end_datePicker.GetValue():
            self.search_crit_panel.obj_end_datePicker.SetValue(wx_date)
        elif not self.search_crit_panel.obj_end_datePicker.IsEnabled():
            self.search_crit_panel.obj_end_datePicker.SetValue(wx_date)
        event.Skip()

    def onObjEndDatePickerChanged(self, event):
        """
        Обработчик изменения конечной даты документа для поиска.
        """
        wx_date = event.GetDate()
        if self.search_crit_panel.obj_start_datePicker.IsEnabled() and wx_date < self.search_crit_panel.obj_start_datePicker.GetValue():
            self.search_crit_panel.obj_start_datePicker.SetValue(wx_date)
        elif not self.search_crit_panel.obj_start_datePicker.IsEnabled():
            self.search_crit_panel.obj_start_datePicker.SetValue(wx_date)
        event.Skip()

    def onDocTypeCheckBox(self, event):
        """
        Обработчик выбора флага поиска по типу документа.
        """
        check = event.IsChecked()
        self.search_crit_panel.doc_type_ctrl.Enable(check)
        if not check:
            self.search_crit_panel.doc_type_ctrl.setValue(None)
        event.Skip()

    def onEntityCheckBox(self, event):
        """
        Обработчик выбора флага поиска по подразделению.
        """
        check = event.IsChecked()
        self.search_crit_panel.entity_ctrl.Enable(check)
        if not check:
            self.search_crit_panel.entity_ctrl.setValue(None)
        event.Skip()

    def onContragentCheckBox(self, event):
        """
        Обработчик выбора флага поиска по контрагенту.
        """
        check = event.IsChecked()
        self.search_crit_panel.contragent_ctrl.Enable(check)
        if not check:
            self.search_crit_panel.contragent_ctrl.setValue(None)
        event.Skip()

    def onCollapseToolClicked(self, event):
        """
        Обработчик инструмента свертывания панели критериев поиска.
        """
        self._last_sash_position = self.panel_splitter.GetSashPosition()
        # ВНИМАНИЕ! Указывать позицию сплитера как 0 нельзя
        # иначе схлопывание панели будет не полным
        #                                   v
        self.panel_splitter.SetSashPosition(1)
        self.ctrl_toolBar.EnableTool(self.collapse_tool.GetId(), False)
        self.ctrl_toolBar.EnableTool(self.expand_tool.GetId(), True)
        event.Skip()

    def onExpandToolClicked(self, event):
        """
        Обработчик инструмента развертывания панели критериев поиска.
        """
        self.panel_splitter.SetSashPosition(self._last_sash_position)
        self.ctrl_toolBar.EnableTool(self.collapse_tool.GetId(), True)
        self.ctrl_toolBar.EnableTool(self.expand_tool.GetId(), False)
        event.Skip()


class icSearchDocPanel(icSearchDocPanelCtrl,
                       search_doc_form_proto.icSearchDocPanelProto):
    """
    Панель поиска документов.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        search_doc_form_proto.icSearchDocPanelProto.__init__(self, *args, **kwargs)

        self.init()

        self.search_crit_panel.start_datePicker.Bind(wx.EVT_DATE_CHANGED, self.onStartDatePickerChanged)
        self.search_crit_panel.end_datePicker.Bind(wx.EVT_DATE_CHANGED, self.onEndDatePickerChanged)

        self.search_crit_panel.date_checkBox.Bind(wx.EVT_CHECKBOX, self.onDateCheckBox)
        self.search_crit_panel.one_date_checkBox.Bind(wx.EVT_CHECKBOX, self.onOneDateCheckBox)

        self.search_crit_panel.doc_type_checkBox.Bind(wx.EVT_CHECKBOX, self.onDocTypeCheckBox)
        self.search_crit_panel.entity_checkBox.Bind(wx.EVT_CHECKBOX, self.onEntityCheckBox)
        self.search_crit_panel.contragent_checkBox.Bind(wx.EVT_CHECKBOX, self.onContragentCheckBox)

        # Необходимо перепривязать обработчик кнопок
        self.search_crit_panel.clear_button.Bind(wx.EVT_BUTTON, self.onClearButtonClick)
        self.search_crit_panel.search_button.Bind(wx.EVT_BUTTON, self.onSearchButtonClick)


class icSearchDocDlg(icSearchDocPanelCtrl,
                     search_doc_form_proto.icSearchDocDlgProto):
    """
    Диалоговое окно поиска и выбора документов.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        search_doc_form_proto.icSearchDocDlgProto.__init__(self, *args, **kwargs)

        self.init()

        self.search_crit_panel.start_datePicker.Bind(wx.EVT_DATE_CHANGED, self.onStartDatePickerChanged)
        self.search_crit_panel.end_datePicker.Bind(wx.EVT_DATE_CHANGED, self.onEndDatePickerChanged)

        self.search_crit_panel.date_checkBox.Bind(wx.EVT_CHECKBOX, self.onDateCheckBox)
        self.search_crit_panel.one_date_checkBox.Bind(wx.EVT_CHECKBOX, self.onOneDateCheckBox)

        self.search_crit_panel.doc_type_checkBox.Bind(wx.EVT_CHECKBOX, self.onDocTypeCheckBox)
        self.search_crit_panel.entity_checkBox.Bind(wx.EVT_CHECKBOX, self.onEntityCheckBox)
        self.search_crit_panel.contragent_checkBox.Bind(wx.EVT_CHECKBOX, self.onContragentCheckBox)

        # Необходимо перепривязать обработчик кнопок
        self.search_crit_panel.clear_button.Bind(wx.EVT_BUTTON, self.onClearButtonClick)
        self.search_crit_panel.search_button.Bind(wx.EVT_BUTTON, self.onSearchButtonClick)


    def onCancelButtonClick(self, event):
        """
        Обработчик кнопки <Отмена>.
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        Обработчик кнопки <Оk>.
        """
        self.selected_doc_uuid = None

        idx = self.docs_listCtrl.GetFirstSelected()
        if idx != -1:
            self.selected_doc_uuid = self.documents[idx]['uuid']

        self.EndModal(wx.ID_OK)
        event.Skip()

    def getSelectedDocUUID(self):
        """
        UUID выбранного документа.
        """
        log.debug(u'Выбранные документ uuid <%s>' % self.selected_doc_uuid)
        return self.selected_doc_uuid

    def init(self):
        """
        Общая инициализация панели.
        """
        self.init_images()
        
        self.initListCtrl()

        self.documents = list()

        # Необходимо перепривязать обработчик кнопок
        self.search_crit_panel.clear_button.Bind(wx.EVT_BUTTON, self.onClearButtonClick)
        self.search_crit_panel.search_button.Bind(wx.EVT_BUTTON, self.onSearchButtonClick)

    def init_images(self):
        """
        Инициализация картинок контролов.
        """
        # <wx.Tool>
        bmp = ic_bmp.createLibraryBitmap('application-dock-090.png')
        tool_id = self.collapse_tool.GetId()
        # ВНИМАНИЕ! Для смены образа инструмента не надо использовать
        # метод инструмента <tool.SetNormalBitmap(bmp)> т.к. НЕ РАБОТАЕТ!
        # Для этого вызываем метод панели инструметнтов
        # <toolbar.SetToolNormalBitmap(tool_id, bmp)>
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)

        bmp = ic_bmp.createLibraryBitmap('application-dock-270.png')
        tool_id = self.expand_tool.GetId()
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)

        self.ctrl_toolBar.Realize()


class icChoiceDocsDlg(icSearchDocPanelCtrl,
                      search_doc_form_proto.icChoiceDocsDlgProto):
    """
    Диалоговое окно поиска и выбора сразу нескольких документов.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        search_doc_form_proto.icChoiceDocsDlgProto.__init__(self, *args, **kwargs)

        self.init()

        self.search_crit_panel.start_datePicker.Bind(wx.EVT_DATE_CHANGED, self.onStartDatePickerChanged)
        self.search_crit_panel.end_datePicker.Bind(wx.EVT_DATE_CHANGED, self.onEndDatePickerChanged)

        self.search_crit_panel.date_checkBox.Bind(wx.EVT_CHECKBOX, self.onDateCheckBox)
        self.search_crit_panel.one_date_checkBox.Bind(wx.EVT_CHECKBOX, self.onOneDateCheckBox)

        self.search_crit_panel.doc_type_checkBox.Bind(wx.EVT_CHECKBOX, self.onDocTypeCheckBox)
        self.search_crit_panel.entity_checkBox.Bind(wx.EVT_CHECKBOX, self.onEntityCheckBox)
        self.search_crit_panel.contragent_checkBox.Bind(wx.EVT_CHECKBOX, self.onContragentCheckBox)

        # Необходимо перепривязать обработчик кнопок
        self.search_crit_panel.clear_button.Bind(wx.EVT_BUTTON, self.onClearButtonClick)
        self.search_crit_panel.search_button.Bind(wx.EVT_BUTTON, self.onSearchButtonClick)

    def onCancelButtonClick(self, event):
        """
        Обработчик кнопки <Отмена>.
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        Обработчик кнопки <Оk>.
        """
        self.selected_docs_uuid = list()

        for i in range(self.docs_listCtrl.GetItemCount()):
            if self.docs_listCtrl.IsChecked(i):
                document = self.documents[i]
                doc_uuid = document['uuid']
                self.selected_docs_uuid.append(doc_uuid)

        self.EndModal(wx.ID_OK)
        event.Skip()

    def onAllCheckBox(self, event):
        """
        Обработчик выделения всех документов.
        """
        check = event.IsChecked()
        for i in range(self.docs_listCtrl.GetItemCount()):
            self.docs_listCtrl.CheckItem(i, check=check)
        event.Skip()
        
    def getSelectedDocsUUID(self):
        """
        Список UUIDов выбранных документов.
        """
        log.debug(u'Выбранные документы uuid <%s>' % self.selected_docs_uuid)
        return self.selected_docs_uuid

    def init(self):
        """
        Общая инициализация панели.
        """
        self.init_images()
        
        self.initListCtrl()

        self.documents = list()

        # Необходимо перепривязать обработчик кнопок
        # self.search_crit_panel.clear_button.Bind(wx.EVT_BUTTON, self.onClearButtonClick)
        # self.search_crit_panel.search_button.Bind(wx.EVT_BUTTON, self.onSearchButtonClick)

    def init_images(self):
        """
        Инициализация картинок контролов.
        """
        # <wx.Tool>
        bmp = ic_bmp.createLibraryBitmap('application-dock-090.png')
        tool_id = self.collapse_tool.GetId()
        # ВНИМАНИЕ! Для смены образа инструмента не надо использовать
        # метод инструмента <tool.SetNormalBitmap(bmp)> т.к. НЕ РАБОТАЕТ!
        # Для этого вызываем метод панели инструметнтов
        # <toolbar.SetToolNormalBitmap(tool_id, bmp)>
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)

        bmp = ic_bmp.createLibraryBitmap('application-dock-270.png')
        tool_id = self.expand_tool.GetId()
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)

        self.ctrl_toolBar.Realize()

    def set_filter(self, filter_requisites=None):
        """
        Установить фильтр документов по значениям реквизитов карточки документа.
        @param filter_requisites: Словарь значений реквизитов по которым происходит фильтрация.
        """
        # Если фильтр не указан, то не производить фильтрацию
        if not filter_requisites:
            log.warning(u'Не указан фильтр окна выбора документов')
            return
        
        # Определение критериев поиска
        for requisite_name, requisite_value in filter_requisites.items():
            if requisite_name == 'n_doc':
                self.search_crit_panel.docnum_textCtrl.SetValue(requisite_value)
            elif requisite_name == 'n_obj':
                self.search_crit_panel.nobj_textCtrl.SetValue(requisite_value)
            elif requisite_name == 'doc_name':
                self.search_crit_panel.docname_textCtrl.SetValue(requisite_value)
            elif requisite_name == 'doc_date':
                wx_date = ic_time.pydate2wxdate(requisite_value)
                self.search_crit_panel.date_checkBox.SetValue(True)
                self.search_crit_panel.start_datePicker.SetValue(wx_date)
                self.search_crit_panel.one_date_checkBox.SetValue(True)
            elif requisite_name == 'obj_date':
                wx_date = ic_time.pydate2wxdate(requisite_value)
                self.search_crit_panel.obj_date_checkBox.SetValue(True)
                self.search_crit_panel.obj_start_datePicker.SetValue(wx_date)
                self.search_crit_panel.obj_one_date_checkBox.SetValue(True)
            elif requisite_name == 'doc_type':
                self.search_crit_panel.doc_type_checkBox.SetValue(True)
                self.search_crit_panel.doc_type_ctrl.Enable(True)
                self.search_crit_panel.doc_type_ctrl.setValue(requisite_value)
            elif requisite_name == 'c_agent':
                log.debug(u'Выборка по контрагенту <%s>' % requisite_value)
                self.search_crit_panel.contragent_checkBox.SetValue(True)
                self.search_crit_panel.contragent_ctrl.Enable(True)
                self.search_crit_panel.contragent_ctrl.setValue(requisite_value)
            elif requisite_name == 'entity':
                self.search_crit_panel.entity_checkBox.SetValue(True)
                self.search_crit_panel.entity_ctrl.Enable(True)
                self.search_crit_panel.entity_ctrl.setValue(requisite_value)
            elif requisite_name == 'description':
                self.search_crit_panel.description_textCtrl.SetValue(requisite_value)
            elif requisite_name == 'comment':
                self.search_crit_panel.comment_textCtrl.SetValue(requisite_value)
            elif requisite_name == 'tag0':
                self.search_crit_panel.tag0_textCtrl.SetValue(requisite_value)
            elif requisite_name == 'tag1':
                self.search_crit_panel.tag1_textCtrl.SetValue(requisite_value)
            elif requisite_name == 'tag2':
                self.search_crit_panel.tag2_textCtrl.SetValue(requisite_value)
            elif requisite_name == 'tag3':
                self.search_crit_panel.tag3_textCtrl.SetValue(requisite_value)
            elif requisite_name == 'tag4':
                self.search_crit_panel.tag4_textCtrl.SetValue(requisite_value)
            elif requisite_name == 'tag5':
                self.search_crit_panel.tag5_textCtrl.SetValue(requisite_value)
            elif requisite_name == 'tag6':
                self.search_crit_panel.tag6_textCtrl.SetValue(requisite_value)
            elif requisite_name == 'tag7':
                self.search_crit_panel.tag7_textCtrl.SetValue(requisite_value)
            elif requisite_name == 'tag8':
                self.search_crit_panel.tag8_textCtrl.SetValue(requisite_value)
            elif requisite_name == 'tag9':
                self.search_crit_panel.tag9_textCtrl.SetValue(requisite_value)
        
        # Формирование запроса
        self.documents = self.search_doc_data(filter_requisites.get('n_doc', u''), 
                                              filter_requisites.get('n_obj', u''), 
                                              filter_requisites.get('doc_name', u''), 
                                              filter_requisites.get('doc_date', u''), filter_requisites.get('doc_date', u''), 
                                              filter_requisites.get('obj_date', u''), filter_requisites.get('obj_date', u''), 
                                              filter_requisites.get('doc_type', u''), 
                                              filter_requisites.get('c_agent', u''), 
                                              filter_requisites.get('entity', u''),
                                              filter_requisites.get('description', u''), 
                                              filter_requisites.get('comment', u''),
                                              filter_requisites.get('tag0', u''), 
                                              filter_requisites.get('tag1', u''), 
                                              filter_requisites.get('tag2', u''), 
                                              filter_requisites.get('tag3', u''), 
                                              filter_requisites.get('tag4', u''), 
                                              filter_requisites.get('tag5', u''), 
                                              filter_requisites.get('tag6', u''), 
                                              filter_requisites.get('tag7', u''), 
                                              filter_requisites.get('tag8', u''), 
                                              filter_requisites.get('tag9', u''))

        # Заполнить список документов
        self.refreshDocList()
    
    
def search_doc_dlg(parent=None):
    """
    Поиск и выбор документа с помощью диалоговой формы.
    """
    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    dlg = icSearchDocDlg(parent=parent)
    dlg.init()
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        return dlg.getSelectedDocUUID()
    return None


def choice_docs_dlg(parent=None, prev_filter=None):
    """
    Поиск и выбор сразу нескольких документов с помощью диалоговой формы.
    @param parent: Родительское окно.
    @param prev_filter: Словарь предварительного фильтра документов по
        значениям атрибутам карточки документа.
    """
    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    dlg = icChoiceDocsDlg(parent=parent)
    dlg.init()
    
    if prev_filter:
        dlg.set_filter(prev_filter)
        
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        return dlg.getSelectedDocsUUID()
    return None


def test():
    """
    Функция тестирования.
    """
    app = wx.PySimpleApp()

    dlg = icSearchDocDlg(None)
    dlg.ShowModal()

    app.MainLoop()


if __name__ == '__main__':
    test()
