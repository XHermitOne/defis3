#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Панель создания нового архивного документа в системе.
"""

import sys
import os
import os.path
import datetime
import wx
import ic
from ic import config
from ic.bitmap import ic_bmp
from ic.log import log
from ic.dlg import ic_dlg
from ic.dlg import wait_box
from ic.utils import ic_extend
from ic.utils import ic_str
from ic.utils import ic_file
from ic.utils import txtgen
from ic.utils import ic_time
from ic.utils import ic_uuid
from ic.scanner import scanner_manager
from archive.forms import new_doc_form_proto
from work_flow.doc_sys import icdocselectdlg
from archive.forms import search_doc_form
from ic.engine import form_manager

# Version
__version__ = (0, 0, 3, 2)

DEFAULT_SCAN_FILENAME = os.path.join(ic_file.getPrjProfilePath(),
                                     'scan_filename.pdf')

DEFAULT_SCAN_BMP_FILENAMES = ('/usr/share/icons/gnome/48x48/devices/scanner.png',                              
                              '/usr/share/icons/Adwaita/48x48/devices/scanner.png',
                              '/usr/share/icons/HighContrast/48x48/devices/scanner.png')

DEFAULT_DATE_FMT = '%Y.%m.%d'

# Не текстовые символы (не должны попадать в текст документа)
NOT_TXT_SYMBOLS = [unichr(c) for c in range(0x2500, 0x25A0)]


def gen_scan_filename(doc, file_ext='.pdf'):
    """
    Генерация имени сканируемого файла по карточке.
    """
    doc_date = doc.getRequisiteValue('doc_date')
    if doc_date:
        doc_year = doc_date.year
    else:
        doc_year = 'XXXX'        
    doc_uuid = doc.getUUID() if doc.getUUID() else ic_uuid.get_uuid()
    scan_filename = '%s.%s.%s.%s%s' % (doc.getRequisiteValue('c_agent'),
                                       doc_year,
                                       doc.getRequisiteValue('doc_type'),
                                       doc_uuid,
                                       file_ext)
    return scan_filename


def put_doc_catalog(doc, scan_filename, doRemoveScan=True):
    """
    Разместить документ в каталоге.
    @param doc: Объект документа карточки скана.
    @param scan_filename: Имя файла сканированого документа.
    @param doRemoveScan: Удалить промежуточный файл скана?
    @return: True/False.
    """                
    file_ext = os.path.splitext(scan_filename)[1]
    doc_filename = gen_scan_filename(doc, file_ext)
    doc_filename = os.path.join(os.path.dirname(scan_filename), doc_filename)

    #if os.path.exists(doc_filename):
    #    ic_dlg.icWarningBox(u'ВНИМАНИЕ!', u'Сканированный файл <%s> уже зарегистрирован в БД. Скан не сохраняется' % doc_filename)
    #    return False
        
    ic_file.icCopyFile(scan_filename, doc_filename)
    
    cataloger = ic.metadata.THIS.mtd.doc_cataloger.create()
    cataloger.put_object(doc_filename, do_remove=doRemoveScan)
    new_filename = cataloger.getLastObjPath()
    log.debug(u'Файл размещен в каталоге <%s>' % new_filename)
    doc.setRequisiteValue('file_name', new_filename)

    #if doRemoveScan:
    #    # После удачного переноса скана в каталог
    #    # удалить файл скана в папке .icscanner
    #    try:
    #        log.info(u'Удаление файла <%s>' % doc_filename)
    #        os.remove(doc_filename)
    #    except:
    #        log.fatal(u'Ошибка удаления файла <%s>' % doc_filename)
        
    return True
    
    
class icDocCardPanelManager():
    """
    Менеджер панели карточки документа.
    """
    
    def valid(self, data):
        """
        Валидация. Проверка правильности заполнения экранной формы.
        @param data: Данные экранной формы в виде словаря.
        @return: True - проверка прошла успешно.
            False - ошибка заполнения данных.
        """
        if data:
            filename = data['file_name'].strip()
            if not filename:
                # Если не определен файл документа
                ic_dlg.icErrBox(u'ОШИБКА', 
                                u'Не определен файл регистрируемого документа')
                return False
            elif not os.path.exists(filename):
                # Если не существует файл документа
                ic_dlg.icErrBox(u'ОШИБКА', 
                                u'Файл регистрируемого документа <%s> не существует' % filename)
                return False
            elif not data['doc_name'].strip():
                # Если не определено имя документа
                ic_dlg.icErrBox(u'ОШИБКА', 
                                u'Имя документа не определено')
                return False
            elif not data['n_doc'].strip():
                # Если не определен номер документа
                ic_dlg.icErrBox(u'ОШИБКА', 
                                u'Не определен номер документа')
                return False
            elif not data.get('doc_type', None):
                # Если не определен тип документа
                # То валидация не проходит, т.к. тип документа присутствует в 
                # имени файла скана
                ic_dlg.icErrBox(u'ОШИБКА', 
                                u'Не определен тип документа')
                return False
            elif not data.get('c_agent', None):
                # Если не определен контрагент
                # То валидация не проходит, т.к. контрагент присутствует в 
                # имени файла скана
                ic_dlg.icErrBox(u'ОШИБКА', 
                                u'Не определен контрагент документа')
                return False
            return True
        else:
            log.warning(u'Не определены данные экранной формы')
        return False

    def put_doc_catalog(self, doc, scan_filename, doRemoveScan=True):
        """
        Разместить документ в каталоге.
        @param doc: Объект документа карточки скана.
        @param scan_filename: Имя файла сканированого документа.
        @param doRemoveScan: Удалить промежуточный файл скана?
        @return: True/False.
        """                
        return put_doc_catalog(doc, scan_filename, doRemoveScan)

    def valid_link(self, doc_uuid):
        """
        Проверка корректности добавляемой ссылки на документ.
        Нельзя добавлять уже существующие связи.
        Также нельзя чтобы документ ссылался сам на себя.
        @param doc_uuid: UUID документа добавляемой связи/ссылки.
        @return: True - все ок. False - нельзя добавлять ссылку на объект.
        """
        return (doc_uuid is not None) and (doc_uuid not in self._link_to_uuids)

    def valid_links(self, docs_uuid):
        """
        Проверка корректности списка добавляемых ссылок на документы.
        @param docs_uuid: Список UUID документов добавляемой связи/ссылки.
        @return: True - все ок. False - нельзя добавлять ссылку на объект.
        """
        return min([self.valid_link(doc_uuid) for doc_uuid in docs_uuid])

    # Конвертация длительный процесс. Ставим тут ожидание
    @wait_box.wait_deco
    def _getDocText(self, doc_filename):
        """
        Получить текст документа.
        @param doc_filename: Полное имя файла документа.
        """
        if not os.path.exists(doc_filename):
            log.warning(u'Определение текста документа. Файл <%s> не найден.' % doc_filename)
            return u''
        
        file_ext = os.path.splitext(doc_filename)[1]
        
        sprav_manager = ic.metadata.THIS.mtd.nsi_archive.create()
        sprav = sprav_manager.getSpravByName('nsi_body_type')
        
        code = ic_str.limit_len_text(file_ext.replace('.', '').upper(), 4, '-')
        cmd = sprav.Find(code, 's2')
        replaces = {'FILENAME': doc_filename, 
                    'PROFILE_DIR': ic_file.getPrjProfilePath()}
        cmd = txtgen.gen(cmd, replaces)
        log.info(u'Run command <%s>' % cmd)
        
        doc_txt = os.popen3(cmd)[1].read()
        
        # Перевести текст в юникод
        doc_txt = unicode(doc_txt, ic.config.DEFAULT_ENCODING)
        
        # Удалить все не нужные символы
        for c in NOT_TXT_SYMBOLS:
            doc_txt = doc_txt.replace(c, u'')
        
        return doc_txt
   
    def viewDocFile(self, doc_filename):
        """
        Просмотр файла отсканированного документа.
        """
        if not os.path.exists(doc_filename):
            log.warning(u'Файл <%s> не найден для просмотра' % doc_filename)
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
        
    
class icNewArchiveDocPanel(new_doc_form_proto.icNewDocPanelProto,
                           icDocCardPanelManager,
                           form_manager.icFormManager):
    """
    Панель создания нового архивного документа в системе.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        form_manager.icFormManager.__init__(self)    
        new_doc_form_proto.icNewDocPanelProto.__init__(self, *args, **kwargs)
   
    def init(self):
        """
        Инициализация панели.
        """ 
        self.autocomplit.LoadDict()     # Загрузить частотные словари для авто заполнений
        
        # Список UUID документов с которыми связан текущий документ
        self._link_to_uuids = list()
        
        bmp = ic_bmp.findBitmap(*DEFAULT_SCAN_BMP_FILENAMES)
        if bmp:
            self.scan_bpButton.SetBitmap(bmp)
        
        doc = ic.metadata.THIS.mtd.scan_document.create()
        requisites = [requisite for requisite in doc.getChildrenRequisites() if requisite.isDescription()]
        for i, requisite in enumerate(requisites):
            self.link_listCtrl.InsertColumn(i, requisite.getLabel(), 
                                            width=wx.LIST_AUTOSIZE)
            
        doc_dir = ic.settings.THIS.SETTINGS.doc_dir.get()
        doc_dir = ic.getHomeDir() if doc_dir is None else doc_dir
        self.select_filePicker.SetInitialDirectory(doc_dir)
            
    def get_ctrl_data(self):
        """
        Получить данные из контролов в виде словаря.
        """    
        data = dict()
        data['file_name'] = self.select_filePicker.GetPath()
        data['n_doc'] = self.ndoc_textCtrl.GetValue()
        data['n_obj'] = self.nobj_textCtrl.GetValue()
        data['doc_date'] = ic_time.wxdate2pydate(self.doc_datePicker.GetValue())
        data['obj_date'] = ic_time.wxdate2pydate(self.obj_datePicker.GetValue())
        data['doc_name'] = self.docname_textCtrl.GetValue()
        data['doc_type'] = self.doc_type_ctrl.getValue()
        data['c_agent'] = self.contragent_ctrl.getValue()
        data['entity'] = self.entity_ctrl.getValue()
        data['description'] = self.description_textCtrl.GetValue()
        data['comment'] = self.comment_textCtrl.GetValue()
        tag0 = self.tag0_textCtrl.GetValue()
        tag1 = self.tag1_textCtrl.GetValue()
        tag2 = self.tag2_textCtrl.GetValue()
        tag3 = self.tag3_textCtrl.GetValue()
        tag4 = self.tag4_textCtrl.GetValue()
        tag5 = self.tag5_textCtrl.GetValue()
        tag6 = self.tag6_textCtrl.GetValue()
        tag7 = self.tag7_textCtrl.GetValue()
        tag8 = self.tag8_textCtrl.GetValue()
        tag9 = self.tag9_textCtrl.GetValue()
        tags = [tag0, tag1, tag2, tag3, tag4, tag5, tag6, tag7, tag8, tag9]
        tags = [tag for tag in tags if tag]
        data['tags'] = ';'.join(tags)
        data['link_to'] = self._link_to_uuids
        return data        

    def reg_doc(self, doc_data):
        """
        Регистрация нового документа в архиве.
        @param doc_data: Данные о регистрируемомом документе.
        """
        if not os.path.exists(doc_data['file_name']):
            msg = u'Не существует файла скана <%s>. Документ не зарегистрирован' % doc_data['file_name']
            log.warning(msg)
            ic_dlg.icWarningBox(u'ВНИМАНИЕ!', msg, parent=self)
            return
        else:
            log.debug(u'Регистрация файла <%s>' % doc_data['file_name'])
        
        log.debug(u'Регистрация документа. Вид: <%s> Подразделение: <%s>' % (doc_data['doc_type'], doc_data['entity']))
        doc = ic.metadata.THIS.mtd.scan_document.create()

        doc.setRequisiteValue('n_doc', doc_data['n_doc'])        
        doc.setRequisiteValue('n_obj', doc_data['n_obj'])        
        doc.setRequisiteValue('doc_date', doc_data['doc_date'])
        doc.setRequisiteValue('obj_date', doc_data['obj_date'])
        doc.setRequisiteValue('doc_name', doc_data['doc_name'])
        doc.setRequisiteValue('description', doc_data['description'])
        doc.setRequisiteValue('comment', doc_data['comment'])
        doc.setRequisiteValue('doc_type', doc_data['doc_type'])
        doc.setRequisiteValue('c_agent', doc_data['c_agent'])
        doc.setRequisiteValue('entity', doc_data['entity'])

        #tags = doc_data['tags'].split(';')
        #tags += [u'']*(10-len(tags))        
        doc.setRequisiteValue('tags', doc_data['tags'])
        
        file_ext = os.path.splitext(doc_data['file_name'])[1]
        doc.setRequisiteValue('body_type', 
                              ic_str.limit_len_text(file_ext.upper(), 4, '-'))
        
        doc.setRequisiteValue('file_name', doc_data['file_name'])
        
        # А теперь размещаем объект в каталоге
        self.put_doc_catalog(doc, doc_data['file_name'])
        
        # body_txt = self._getDocText(doc_data['file_name'])
        # doc.setRequisiteValue('txt_body', body_txt)
        # log.debug(u'Текст документа <%s>' % body_txt)

        doc.setRequisiteValue('scan_doc_to', 
                              [dict(link_to=doc_uuid) for doc_uuid in self._link_to_uuids])
        doc.setRequisiteValue('scan_doc_from', list())        
        
        # Настроить обоюдную связь с другими документами
        for link_doc_uuid in self._link_to_uuids:
            link_doc = ic.metadata.THIS.mtd.scan_document.create()
            link_doc.load_obj(link_doc_uuid)
            requisite = link_doc.getRequisite('scan_doc_from')
            requisite.addRow(link_from=doc.getUUID())
            link_doc.save_obj()
        
        doc.do_operation('create')              
     
    def clear_ctrl_data(self):
        """
        Очистить контролы для заполнения следующего документа.
        """
        self.select_filePicker.SetPath(u'')
        self.ndoc_textCtrl.SetValue(u'')
        self.nobj_textCtrl.SetValue(u'')
        # self.doc_datePicker.SetValue(ic_time.pydate2wxdate(datetime.date.today()))
        self.docname_textCtrl.SetValue(u'')
        
        # Отключил очистку контролов справочника типа документа и
        # справочника подразделения по просьбе архивариуса
        # После регистрации будет оставаться предыдущее значение для
        # ускорения ручного ввода документов
        #               V
        # self.doc_type_ctrl.setValue(None)
        # self.entity_ctrl.setValue(None)
        self.contragent_ctrl.setValue(None)
        
        self.description_textCtrl.SetValue(u'')
        self.comment_textCtrl.SetValue(u'')
        
        self.tag0_textCtrl.SetValue(u'')
        self.tag1_textCtrl.SetValue(u'')
        self.tag2_textCtrl.SetValue(u'')
        self.tag3_textCtrl.SetValue(u'')
        self.tag4_textCtrl.SetValue(u'')
        self.tag5_textCtrl.SetValue(u'')
        self.tag6_textCtrl.SetValue(u'')
        self.tag7_textCtrl.SetValue(u'')
        self.tag8_textCtrl.SetValue(u'')
        self.tag9_textCtrl.SetValue(u'')
        
        self.link_listCtrl.DeleteAllItems()
        
    def onRegButtonClick(self, event):
        """
        Обработчик кномпки <Зарегистрировать>.
        """
        self.saveAutoComplit()
        
        ctrl_data = self.get_ctrl_data()
        if self.valid(ctrl_data):
            # Валидация прошла успешно можно регистрировать документ
            self.reg_doc(ctrl_data)
            self.clear_ctrl_data()
            
            ic_dlg.icMsgBox(u'РЕГИСТРАЦИЯ', 
                            u'Новый документ <%s> зарегистрирован в БД.' % ctrl_data.get('n_doc', u''))
            #if not ic_dlg.icAskBox(u'РЕГИСТРАЦИЯ', 
            #                       u'Новый документ <%s> зарегистрирован в БД. Продолжить регистрацию?' % ctrl_data.get('n_doc', u'')):
            #    main_win = ic.getMainWin()
            #    main_win.delPageByTitle(u'Регистрация новых документов')
        
        event.Skip()
    
    def onAddLinkButtonClick(self, event):
        """
        Добавление связи с документом.
        """
        doc = ic.metadata.THIS.mtd.scan_document.create()
        docs_uuid = search_doc_form.choice_docs_dlg()
        
        if docs_uuid:            
            for doc_uuid in docs_uuid:
                doc_data = doc.loadRequisiteData(doc_uuid)
                
                if not self.valid_link(doc_uuid):
                    log.warning(u'Попытка добавления уже существующей связи с документом')
                    ic_dlg.icWarningBox(u'ВНИМАНИЕ', u'Связь с документом <%s> уже есть в списке' % doc_data.get('doc_name', u'-'))
                    continue
            
                self._link_to_uuids.append(doc_uuid)
            
                requisites = [requisite for requisite in doc.getChildrenRequisites() if requisite.isDescription()]
                row_idx = 0
                for i, requisite in enumerate(requisites):
                
                    if requisite.__class__.__name__ == 'icNSIRequisite':
                        value = requisite.getStrData()
                    else:
                        value = requisite.getValue()
                    
                    if isinstance(value, datetime.datetime):
                        value = value.strftime(DEFAULT_DATE_FMT)
                    elif not isinstance(value, str) and not isinstance(value, unicode):
                        value = str(value)
                    
                    if i == 0:
                        row_idx = self.link_listCtrl.InsertStringItem(sys.maxint, value, i)
                    else:
                        self.link_listCtrl.SetStringItem(row_idx, i, value)
                # Обновить размер колонок
                for i in range(len(requisites)):
                    self.link_listCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE)        
            
        event.Skip()
        
    def onDelLinkButtonClick(self, event):
        """
        Удаление связи с документом.
        """
        idx = self.link_listCtrl.GetFirstSelected()
        if idx != -1:
            del self._link_to_uuids[idx]
            self.link_listCtrl.DeleteItem(idx)
            
        event.Skip()        
        
    def onScanButtonClick(self, event):
        """
        Запуск сканирования.
        """
        scanner_mgr = scanner_manager.icScannerManager()
        # Перед сканированием удалить сканированный ранее файл
        if os.path.exists(DEFAULT_SCAN_FILENAME):
            os.remove(DEFAULT_SCAN_FILENAME)
        # Запуск сканирования
        result = scanner_mgr.do_scan_export(DEFAULT_SCAN_FILENAME)
        
        if result and os.path.exists(DEFAULT_SCAN_FILENAME):
            # Если файл существует, то значит сканирование прошло успешно
            self.select_filePicker.SetInitialDirectory(os.path.dirname(DEFAULT_SCAN_FILENAME))
            self.select_filePicker.SetPath(DEFAULT_SCAN_FILENAME)
        else:
            log.warning(u'Файл сканирования не найден')
            self.select_filePicker.SetPath(u'')
        
        event.Skip()                
        
    def onDocNameText(self, event):
        """
        Ввод текста наименования документа.
        """
        # Автозаполнение
        txt_ctrl = event.GetEventObject()
        self.autocomplit.AutoTextFill(txt_ctrl, 'docname_textCtrl')
        
        event.Skip()
        
    def doCapitalizeDocName(self):
        """
        Наименование документа сделать с большой буквы.
        """
        selection = self.docname_textCtrl.GetSelection()
        # Наименование сделать всегда с большой буквы
        txt = self.docname_textCtrl.GetValue()
        if txt:
            txt = txt[0].capitalize() + txt[1:]
        self.docname_textCtrl.ChangeValue(txt)            
        self.docname_textCtrl.SetSelection(*selection)            
        
    def onTag0Text(self, event):
        """
        Авто заполнение тегов.
        """
        txt_ctrl = event.GetEventObject()
        self.autocomplit.AutoTextFill(txt_ctrl, 'tag0_textCtrl')
        event.Skip()

    def onTag1Text(self, event):
        """
        Авто заполнение тегов.
        """
        txt_ctrl = event.GetEventObject()
        self.autocomplit.AutoTextFill(txt_ctrl, 'tag1_textCtrl')
        event.Skip()

    def onTag2Text(self, event):
        """
        Авто заполнение тегов.
        """
        txt_ctrl = event.GetEventObject()
        self.autocomplit.AutoTextFill(txt_ctrl, 'tag2_textCtrl')
        event.Skip()

    def onTag3Text(self, event):
        """
        Авто заполнение тегов.
        """
        txt_ctrl = event.GetEventObject()
        self.autocomplit.AutoTextFill(txt_ctrl, 'tag3_textCtrl')
        event.Skip()

    def onTag4Text(self, event):
        """
        Авто заполнение тегов.
        """
        txt_ctrl = event.GetEventObject()
        self.autocomplit.AutoTextFill(txt_ctrl, 'tag4_textCtrl')
        event.Skip()

    def onTag5Text(self, event):
        """
        Авто заполнение тегов.
        """
        txt_ctrl = event.GetEventObject()
        self.autocomplit.AutoTextFill(txt_ctrl, 'tag5_textCtrl')
        event.Skip()
        
    def onTag6Text(self, event):
        """
        Авто заполнение тегов.
        """
        txt_ctrl = event.GetEventObject()
        self.autocomplit.AutoTextFill(txt_ctrl, 'tag6_textCtrl')
        event.Skip()

    def onTag7Text(self, event):
        """
        Авто заполнение тегов.
        """
        txt_ctrl = event.GetEventObject()
        self.autocomplit.AutoTextFill(txt_ctrl, 'tag7_textCtrl')
        event.Skip()
        
    def onTag8Text(self, event):
        """
        Авто заполнение тегов.
        """
        txt_ctrl = event.GetEventObject()
        self.autocomplit.AutoTextFill(txt_ctrl, 'tag8_textCtrl')
        event.Skip()

    def onTag9Text(self, event):
        """
        Авто заполнение тегов.
        """
        txt_ctrl = event.GetEventObject()
        self.autocomplit.AutoTextFill(txt_ctrl, 'tag9_textCtrl')
        event.Skip()
        
    def saveAutoComplit(self):
        """
        Сохранить авто заполнения.
        """
        # Запомнить введенные слова для авто заполнения
        self.autocomplit.saveTextFillControls(docname_textCtrl=self.docname_textCtrl,
                                              tag0_textCtrl=self.tag0_textCtrl,
                                              tag1_textCtrl=self.tag1_textCtrl,
                                              tag2_textCtrl=self.tag2_textCtrl,
                                              tag3_textCtrl=self.tag3_textCtrl,
                                              tag4_textCtrl=self.tag4_textCtrl,
                                              tag5_textCtrl=self.tag5_textCtrl,
                                              tag6_textCtrl=self.tag6_textCtrl,
                                              tag7_textCtrl=self.tag7_textCtrl,
                                              tag8_textCtrl=self.tag8_textCtrl,
                                              tag9_textCtrl=self.tag9_textCtrl)
        