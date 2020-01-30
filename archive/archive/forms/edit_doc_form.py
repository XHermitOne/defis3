#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Функции вызова редактирования документа.
"""

import sys
import os
import os.path
import datetime
import wx
from archive.forms import edit_doc_form_proto
from archive.forms import new_doc_panel

import ic
from ic import log
from ic import datetimefunc
from ic import bmpfunc
from ic import filefunc
from ic.dlg import dlgfunc
from work_flow.doc_sys import icdocselectdlg
from archive.forms import search_doc_form
from ic.scanner import scanner_manager

# Version
__version__ = (0, 1, 1, 1)

DEFAULT_DATE_FMT = '%Y.%m.%d'

DEFAULT_SCAN_FILE_EXT = '.pdf'


class icEditDocDlg(edit_doc_form_proto.icEditDocDlgProto):
    """
    Диалоговая форма редактирования документа.
    """

    def onCancelButtonClick(self, event):
        """
        Обработчик кнопки <Отмена>.
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onSaveButtonClick(self, event):
        """
        Обработчик кнопки <Сохранить>.
        """
        self.get_data()

        # Настроить обоюдную связь с другими документами
        for link_doc_uuid in self._link_to_uuids:
            link_doc = ic.metadata.THIS.mtd.scan_document.create()
            link_doc.load_obj(link_doc_uuid)
            requisite = link_doc.getRequisite('scan_doc_from')
            requisite.addRow(link_from=self.document.getUUID())
            link_doc.save_obj()

        self.EndModal(wx.ID_OK)
        event.Skip()

    def onReScanButtonClick(self, event):
        """
        Обработчик кнопки пересканирования.
        """
        scan_filename = self.document.getRequisiteValue('file_name')
        if scan_filename:
            # Необходимо заново сгенерировать имя файла скана, т.к.
            # имя файла может быть не корректным
            file_ext = os.path.splitext(scan_filename)[1]

            new_scan_filename = new_doc_panel.gen_scan_filename(self.document, file_ext)
            new_scan_filename = os.path.join(os.path.dirname(scan_filename),
                                             new_scan_filename)
        else:
            # Имя скана не определено. Необходимо заново сгенерировать имя по документу
            new_scan_filename = new_doc_panel.gen_scan_filename(self.document, DEFAULT_SCAN_FILE_EXT)
            new_scan_filename = os.path.join(os.path.dirname(new_doc_panel.DEFAULT_SCAN_FILENAME),
                                             new_scan_filename)

        # Перед сканированием удалить сканированный ранее файл
        if os.path.exists(new_doc_panel.DEFAULT_SCAN_FILENAME):
            try:
                log.info(u'Удаление файла <%s>' % new_doc_panel.DEFAULT_SCAN_FILENAME)
                os.remove(new_doc_panel.DEFAULT_SCAN_FILENAME)
            except:
                log.fatal(u'Ошибка удаления файла <%s>' % new_doc_panel.DEFAULT_SCAN_FILENAME)

        # Запуск сканирования
        scanner_mgr = scanner_manager.icScannerManager()
        result = scanner_mgr.do_scan_export(new_doc_panel.DEFAULT_SCAN_FILENAME)

        if result and os.path.exists(new_doc_panel.DEFAULT_SCAN_FILENAME):
            # Если файл существует, то значит сканирование прошло успешно
            # Необходимо скопировать в новый файл
            filefunc.copyFile(new_doc_panel.DEFAULT_SCAN_FILENAME, new_scan_filename)
            if not scan_filename:
                # Если ранее не определен отсканированный файл, то расположить его в каталоге
                new_doc_panel.put_doc_catalog(self.document, new_scan_filename)
            else:
                self.document.setRequisiteValue('file_name', new_scan_filename)

            self.edit_doc_panel.scan_filename_staticText.SetLabel(os.path.basename(new_scan_filename))
        else:
            log.warning(u'Файл сканирования <%s> не найден' % new_doc_panel.DEFAULT_SCAN_FILENAME)
            self.edit_doc_panel.scan_filename_staticText.SetLabel(os.path.basename(scan_filename))

        event.Skip()

    def valid_link(self, doc_uuid):
        """
        Проверка корректности добавляемой ссылки на документ.
        Нельзя добавлять уже существующие связи.
        Также нельзя чтобы документ ссылался сам на себя.
        :param doc_uuid: UUID документа добавляемой связи/ссылки.
        :return: True - все ок. False - нельзя добавлять ссылку на объект.
        """
        return (doc_uuid is not None) and (doc_uuid not in self._link_to_uuids) and doc_uuid != self.document.getUUID()

    def valid_links(self, docs_uuid):
        """
        Проверка корректности списка добавляемых ссылок на документы.
        :param docs_uuid: Список UUID документов добавляемой связи/ссылки.
        :return: True - все ок. False - нельзя добавлять ссылку на объект.
        """
        return min([self.valid_link(doc_uuid) for doc_uuid in docs_uuid])

    def onAddLinkButtonClick(self, event):
        """
        Обработчик кнопки <Добавить>.
        """
        doc = ic.metadata.THIS.mtd.scan_document.create()
        requisites_filter=dict(n_doc=self.document.getRequisiteValue('n_doc'),
                               c_agent=self.document.getRequisiteValue('c_agent'),
                               entity=self.document.getRequisiteValue('entity'))
        docs_uuid = search_doc_form.choice_docs_dlg(prev_filter=requisites_filter)

        if docs_uuid:
            for doc_uuid in docs_uuid:
                doc_data = doc.loadRequisiteData(doc_uuid)
                if not self.valid_link(doc_uuid):
                    log.warning(u'Попытка добавления уже существующей связи с документом')
                    dlgfunc.openWarningBox(u'ВНИМАНИЕ',
                                        u'Связь с документом <%s> уже есть в списке' % doc_data.get('doc_name', u'-'),
                                           parent=self)
                    continue

                self._link_to_uuids.append(doc_uuid)

                self._addLinkCtrl(doc, doc_uuid)

        event.Skip()

    def onDelLinkButtonClick(self, event):
        """
        Обработчик кнопки <Удалить>.
        """
        idx = self.edit_doc_panel.link_listCtrl.GetFirstSelected()
        if idx != -1:
            del self._link_to_uuids[idx]
            self.edit_doc_panel.link_listCtrl.DeleteItem(idx)
        event.Skip()

    def onDocNameText(self, event):
        """
        Ввод текста наименования документа.
        """
        event.Skip()
        selection = self.docname_textCtrl.GetSelection()
        # Наименование сделать всегда с большой буквы
        txt = self.docname_textCtrl.GetValue()
        if txt:
            txt = txt[0].capitalize() + txt[1:]
        self.docname_textCtrl.ChangeValue(txt)
        self.docname_textCtrl.setSelection(*selection)

    def setEditDoc(self, document):
        """
        Установить редактируемый объект документа.
        """
        self.document = document

    def init_ctrl(self):
        """
        Инициализация контролов.
        """
        bmp = bmpfunc.findBitmap(*new_doc_panel.DEFAULT_SCAN_BMP_FILENAMES)
        if bmp:
            self.edit_doc_panel.scan_bpButton.SetBitmap(bmp)

        # Колонки списка связей
        requisites = [requisite for requisite in self.document.getChildrenRequisites() if requisite.isDescription()]
        for i, requisite in enumerate(requisites):
            self.edit_doc_panel.link_listCtrl.InsertColumn(i, requisite.getLabel(),
                                                           width=wx.LIST_AUTOSIZE)
        # Перепривязать обработчики кнопок
        self.edit_doc_panel.add_link_button.Bind(wx.EVT_BUTTON, self.onAddLinkButtonClick)
        self.edit_doc_panel.del_link_button.Bind(wx.EVT_BUTTON, self.onDelLinkButtonClick)

        self.edit_doc_panel.scan_bpButton.Bind(wx.EVT_BUTTON, self.onReScanButtonClick)

    def set_data(self):
        """
        Расставить значения реквизитов редактируеиого документа в контролы.
        """
        # Расставляем значения реквизитов в контролы
        scan_filename = self.document.getRequisiteValue('file_name')
        base_scan_filename = os.path.basename(scan_filename) if scan_filename else u''
        self.edit_doc_panel.scan_filename_staticText.SetLabel(base_scan_filename)

        n_doc = self.document.getRequisiteValue('n_doc')
        if n_doc is None:
            msg = u'Не определен номер документа'
            log.warning(msg)
            dlgfunc.openWarningBox(u'ВНИМАНИЕ!', u'Ошибка данных документа: %s' % msg, parent=self)
            # При ошибке данных документа вообще не отображать
            return

        n_obj = self.document.getRequisiteValue('n_obj')

        self.edit_doc_panel.ndoc_textCtrl.SetValue(n_doc)
        self.edit_doc_panel.nobj_textCtrl.SetValue(n_obj)

        doc_date = self.document.getRequisiteValue('doc_date')
        wx_doc_date = datetimefunc.pydate2wxdate(doc_date)
        self.edit_doc_panel.doc_datePicker.SetValue(wx_doc_date)

        obj_date = self.document.getRequisiteValue('obj_date')
        wx_obj_date = datetimefunc.pydate2wxdate(obj_date) if obj_date else wx_doc_date
        self.edit_doc_panel.obj_datePicker.SetValue(wx_obj_date)

        self.edit_doc_panel.docname_textCtrl.SetValue(self.document.getRequisiteValue('doc_name'))

        doc_type_code = self.document.getRequisiteValue('doc_type')
        log.debug(u'edit. Установка данных. Код вида документа <%s>' % doc_type_code)
        self.edit_doc_panel.doc_type_ctrl.setValue(doc_type_code)

        # Для исходящих документов отключаем номер документа контрагента
        # self.edit_doc_panel.nobj_textCtrl.Enable(not (doc_type_code and doc_type_code.startswith('200')))

        self.edit_doc_panel.contragent_ctrl.setValue(self.document.getRequisiteValue('c_agent'))

        entity_code = self.document.getRequisiteValue('entity')
        log.debug(u'edit. Установка данных. Код подразделения <%s>' % entity_code)
        self.edit_doc_panel.entity_ctrl.setValue(entity_code)

        description = self.document.getRequisiteValue('description')
        self.edit_doc_panel.description_textCtrl.SetValue(description if description else u'')
        comment = self.document.getRequisiteValue('comment')
        self.edit_doc_panel.comment_textCtrl.SetValue(comment if comment else u'')
        tags = self.document.getRequisiteValue('tags').split(';')
        tags += [u''] * (10-len(tags))
        self.edit_doc_panel.tag0_textCtrl.SetValue(tags[0])
        self.edit_doc_panel.tag1_textCtrl.SetValue(tags[1])
        self.edit_doc_panel.tag2_textCtrl.SetValue(tags[2])
        self.edit_doc_panel.tag3_textCtrl.SetValue(tags[3])
        self.edit_doc_panel.tag4_textCtrl.SetValue(tags[4])
        self.edit_doc_panel.tag5_textCtrl.SetValue(tags[5])
        self.edit_doc_panel.tag6_textCtrl.SetValue(tags[6])
        self.edit_doc_panel.tag7_textCtrl.SetValue(tags[7])
        self.edit_doc_panel.tag8_textCtrl.SetValue(tags[8])
        self.edit_doc_panel.tag9_textCtrl.SetValue(tags[9])

        links_to = self.document.getRequisiteValue('scan_doc_to')
        doc = ic.metadata.THIS.mtd.scan_document.create()
        self._addLinksCtrl(doc, links_to)

    def _addLinksCtrl(self, doc, links_to):
        """
        Добавление нескольких связей в контрол списка связей.
        :param doc: Объект документа.
        :param links_to: Список UUID документов, на которые ссылаемся.
        """
        if links_to is None:
            links_to = list()

        for link_to in links_to:
            self._addLinkCtrl(doc, link_to['link_to'] if 'link_to' in link_to else link_to)

        # Обновить размер колонок
        requisites = [requisite for requisite in doc.getChildrenRequisites() if requisite.isDescription()]
        for i in range(len(requisites)):
            self.edit_doc_panel.link_listCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE)

    def _addLinkCtrl(self, doc, link_to):
        """
        Добавить связь в контрол списка.
        :param doc: Объект документа.
        :param link_to: UUID документа, на который ссылаемся.
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
                value = value.strftime(DEFAULT_DATE_FMT)
            elif not isinstance(value, str):
                value = str(value)

            if i == 0:
                row_idx = self.edit_doc_panel.link_listCtrl.InsertItem(sys.maxsize, value, i)
            else:
                self.edit_doc_panel.link_listCtrl.SetItem(row_idx, i, value)

    def init(self):
        """
        Общая инициализация диалогового окна.
        """
        # Список UUID документов с которыми связан текущий документ
        self._link_to_uuids = list()

        self.init_ctrl()
        self.set_data()

    def get_data(self):
        """
        Записать данные в редактируемый документ из контролов.
        """
        data = self.get_data_ctrl()

        if self.valid(data):
            self.document.setRequisiteValue('n_doc', data['n_doc'])
            self.document.setRequisiteValue('n_obj', data['n_obj'])
            self.document.setRequisiteValue('doc_date', data['doc_date'])
            self.document.setRequisiteValue('obj_date', data['obj_date'])
            self.document.setRequisiteValue('doc_name', data['doc_name'])
            self.document.setRequisiteValue('doc_type', data['doc_type'])
            self.document.setRequisiteValue('c_agent', data['c_agent'])
            self.document.setRequisiteValue('entity', data['entity'])
            self.document.setRequisiteValue('description', data['description'])
            self.document.setRequisiteValue('comment', data['comment'])
            self.document.setRequisiteValue('tags', data['tags'])
            links_to = [dict(link_to=doc_uuid) for doc_uuid in data['links_to']]
            self.document.setRequisiteValue('scan_doc_to', links_to)

    def get_data_ctrl(self):
        """
        Получить данные из контролов в виде словаря.
        """
        docnum = self.edit_doc_panel.ndoc_textCtrl.GetValue().strip()
        n_obj = self.edit_doc_panel.nobj_textCtrl.GetValue().strip()
        wx_docdate = self.edit_doc_panel.doc_datePicker.GetValue()
        docdate = datetimefunc.wxdate2pydate(wx_docdate)
        wx_objdate = self.edit_doc_panel.obj_datePicker.GetValue()
        objdate = datetimefunc.wxdate2pydate(wx_objdate)
        docname = self.edit_doc_panel.docname_textCtrl.GetValue().strip()
        doctype = self.edit_doc_panel.doc_type_ctrl.getValue()
        contragent = self.edit_doc_panel.contragent_ctrl.getValue()
        entity = self.edit_doc_panel.entity_ctrl.getValue()
        description = self.edit_doc_panel.description_textCtrl.GetValue().strip()
        comment = self.edit_doc_panel.comment_textCtrl.GetValue().strip()
        tag0 = self.edit_doc_panel.tag0_textCtrl.GetValue().strip()
        tag1 = self.edit_doc_panel.tag1_textCtrl.GetValue().strip()
        tag2 = self.edit_doc_panel.tag2_textCtrl.GetValue().strip()
        tag3 = self.edit_doc_panel.tag3_textCtrl.GetValue().strip()
        tag4 = self.edit_doc_panel.tag4_textCtrl.GetValue().strip()
        tag5 = self.edit_doc_panel.tag5_textCtrl.GetValue().strip()
        tag6 = self.edit_doc_panel.tag6_textCtrl.GetValue().strip()
        tag7 = self.edit_doc_panel.tag7_textCtrl.GetValue().strip()
        tag8 = self.edit_doc_panel.tag8_textCtrl.GetValue().strip()
        tag9 = self.edit_doc_panel.tag9_textCtrl.GetValue().strip()
        tags = [tag0, tag1, tag2, tag3, tag4, tag5, tag6, tag7, tag8, tag9]
        tags = [tag if tag else u'' for tag in tags]
        tags = ';'.join(tags)
        links_to = self._link_to_uuids
        return dict(n_doc=docnum, n_obj=n_obj,
                    doc_date=docdate, obj_date=objdate,
                    doc_name=docname,
                    doc_type=doctype, c_agent=contragent, entity=entity,
                    description=description, comment=comment,
                    tags=tags, links_to=links_to)

    def valid(self, data):
        """
        Валидация. Проверка правильности заполнения экранной формы.
        :param data: Данные экранной формы в виде словаря.
        :return: True - проверка прошла успешно.
            False - ошибка заполнения данных.
        """
        if data:
            #filename = data['file_name'].strip()
            #if not filename:
            #    # Если не определен файл документа
            #    ic_dlg.openErrBox(u'ОШИБКА',
            #                    u'Не определен файл регистрируемого документа')
            #    return False
            #elif not os.path.exists(filename):
            #    # Если не существует файл документа
            #    ic_dlg.openErrBox(u'ОШИБКА',
            #                    u'Файл регистрируемого документа <%s> не существует' % filename)
            #    return False
            if not data['doc_name'].strip():
                # Если не определено имя документа
                dlgfunc.openErrBox(u'ОШИБКА',
                                u'Имя документа не определено', parent=self)
                return False
            elif not data['n_doc'].strip():
                # Если не определен номер документа
                dlgfunc.openErrBox(u'ОШИБКА',
                                u'Не определен номер документа', parent=self)
                return False
            elif self.document.getUUID() in data['links_to']:
                # Если документ ссылается сам на себя, это считается ошибкой
                dlgfunc.openErrBox(u'ОШИБКА',
                                u'Документ ссылается сам на себя', parent=self)
                return False
            return True
        else:
            log.warning(u'Не определены данные экранной формы')
        return False


def valid_edit_doc(parent=None, doc=None):
    """
    Контроль данных редактируемого документа.
    :param parent: Родительское окно диалогового окна редактирования.
    :param doc: Объект редактируемого документа.
    :return: True/False.
    """
    n_doc = doc.getRequisiteValue('n_doc')
    if n_doc is None:
        msg = u'Контроль данных редактируемого документа. Не определен номер документа'
        log.warning(msg)
        dlgfunc.openWarningBox(u'ВНИМАНИЕ!', u'Ошибка данных документа: %s' % msg, parent=parent)
        # При ошибке данных документа вообще не отображать
        return False
    return True


def edit_doc_dlg(parent=None, doc=None):
    """
    Редактирование документа в диалоговом окне.
    :param parent: Родительское окно диалогового окна редактирования.
    :param doc: Объект редактируемого документа.
    :return: True/False.
    """
    if doc is None:
        log.warning(u'Не определен документ для редактирования')
        return False

    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    # Запрет на редактирование ошибочных документов
    if not valid_edit_doc(parent, doc):
        return False

    dlg = icEditDocDlg(parent=parent)
    dlg.setEditDoc(doc)
    dlg.init()
    result = dlg.ShowModal()

    return result == wx.ID_OK


def edit_document_dlg(doc=None, parent=None):
    """
    Редактирование документа в диалоговом окне.
    :param doc: Объект редактируемого документа.
    :param parent: Родительское окно диалогового окна редактирования.
    :return: True/False.
    """
    return edit_doc_dlg(parent, doc)
