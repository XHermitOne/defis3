#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Формы поиска и управления отсканированных документов.
Эти формы используются только в режиме администратора.
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
from ic import bmpfunc
from ic import log
from ic import ic_dlg
import ic
from archive.forms import search_doc_form

# Version
__version__ = (0, 0, 2, 1)


class icCtrlDocPanel(search_doc_form.icSearchDocPanelCtrl,
                     search_doc_form_proto.icCtrlDocPanelProto):
    """
    Панель поиска и управления документами.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        search_doc_form_proto.icCtrlDocPanelProto.__init__(self, *args, **kwargs)

        self.init()

        self.search_crit_panel.start_datePicker.Bind(wx.adv.EVT_DATE_CHANGED, self.onStartDatePickerChanged)
        self.search_crit_panel.end_datePicker.Bind(wx.adv.EVT_DATE_CHANGED, self.onEndDatePickerChanged)
        self.search_crit_panel.date_checkBox.Bind(wx.EVT_CHECKBOX, self.onDateCheckBox)
        self.search_crit_panel.one_date_checkBox.Bind(wx.EVT_CHECKBOX, self.onOneDateCheckBox)

        self.search_crit_panel.doc_type_checkBox.Bind(wx.EVT_CHECKBOX, self.onDocTypeCheckBox)
        self.search_crit_panel.entity_checkBox.Bind(wx.EVT_CHECKBOX, self.onEntityCheckBox)
        self.search_crit_panel.contragent_checkBox.Bind(wx.EVT_CHECKBOX, self.onContragentCheckBox)

        # Необходимо перепривязать обработчик кнопок
        self.search_crit_panel.clear_button.Bind(wx.EVT_BUTTON, self.onClearButtonClick)
        self.search_crit_panel.search_button.Bind(wx.EVT_BUTTON, self.onSearchButtonClick)

    def init_images(self):
        """
        Инициализация картинок контролов.
        """
        # Вызов родительского метода
        search_doc_form.icSearchDocPanelCtrl.init_images(self)
        
        # <wx.Tool>
        bmp = bmpfunc.createLibraryBitmap('minus.png')
        tool_id = self.del_tool.GetId()
        # ВНИМАНИЕ! Для смены образа инструмента не надо использовать
        # метод инструмента <tool.SetNormalBitmap(bmp)> т.к. НЕ РАБОТАЕТ!
        # Для этого вызываем метод панели инструметнтов
        # <toolbar.SetToolNormalBitmap(tool_id, bmp)>
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)

        # <wx.Tool>
        bmp = bmpfunc.createLibraryBitmap('broom-code.png')
        tool_id = self.clear_links_tool.GetId()
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)
        
        self.ctrl_toolBar.Realize()

    def del_document(self, doc_uuid, do_del_card=True, do_del_scanfile=False):
        """
        Процедура удаления документа с указанным UUID.
        @param doc_uuid: UUID удаляемого документа.
        @param do_del_card: Удалить карточку документа?
        @param do_del_scanfile: Удалить отсканированный файл документа?
        """
        doc = ic.metadata.THIS.mtd.scan_document.create()
        doc.load_obj(doc_uuid)

        if do_del_scanfile:
            doc_filename = doc.getRequisiteValue('file_name')
            log.debug(u'Удаление файла <%s>' % doc_filename)
            if doc_filename and os.path.exists(doc_filename):
                try:
                    os.remove(doc_filename)
                except:
                    log.fatal(u'Ошибка удаления файла <%s>' % doc_filename)
            else:
                log.warning(u'Файл <%s> не найден' % doc_filename)
        if do_del_card:
            log.debug(u'Удаление документа UUID <%s>' % doc_uuid)
            # Удалить запись в БД
            doc.delete(doc_uuid)
        
    def onDelToolClicked(self, event):
        """
        Обработчик инструмента удаления выбранного документа.
        """
        item_count = self.docs_listCtrl.GetItemCount()
        is_checked = bool(len([i for i in range(item_count) if self.docs_listCtrl.IsChecked(i)]))
        if is_checked:
            # Есть помеченные для удаления документы
            do_del_card = ic_dlg.icAskBox(u'УДАЛЕНИЕ', u'Удалить карточки документов?')                
            do_del_scanfile = ic_dlg.icAskBox(u'УДАЛЕНИЕ', u'Удалить электронные версии документов?')
            if not do_del_card and not do_del_scanfile:
                # Отмена операции удаления
                event.Skip()
                return
            
            try:
                ic_dlg.icOpenProgressDlg(ic.getMainWin(),
                                         u'Пакетная обработка', u'Удаление документов из архива',
                                         max_value=item_count)
                i_progress = 0
                for i in range(item_count - 1, -1, -1):
                    if self.docs_listCtrl.IsChecked(i):
                        document = self.documents[i]
                        doc_uuid = document['uuid']
                    
                        self.del_document(doc_uuid, do_del_card, do_del_scanfile)                    
                    
                        # Удалить из списка документов
                        del self.documents[i]
                        self.docs_listCtrl.DeleteItem(i)
                    else:
                        log.debug(u'Пропуск удаления [%d]' % i)                    
                        
                    i_progress += 1
                    ic_dlg.icUpdateProgressDlg(i_progress, u'Удаление документов из архива')

                ic_dlg.icCloseProgressDlg()
            except:
                ic_dlg.icCloseProgressDlg()
                log.fatal(u'Ошибка удаления документов')
        else:
            # Нет отмеченных документов, но есть текущий документ
            idx = self.docs_listCtrl.GetFirstSelected()
            if idx != -1:
                document = self.documents[idx]
                doc_uuid = document['uuid']
                do_del_card = ic_dlg.icAskBox(u'УДАЛЕНИЕ', u'Удалить карточку документа?')                
                do_del_scanfile = ic_dlg.icAskBox(u'УДАЛЕНИЕ', u'Удалить электронную версию документа?')
                if not do_del_card and not do_del_scanfile:
                    # Отмена операции удаления
                    event.Skip()
                    return
                
                self.del_document(doc_uuid, do_del_card, do_del_scanfile)
                
                # Удалить из списка документов
                del self.documents[idx]
                self.docs_listCtrl.DeleteItem(idx)

        event.Skip()

    def onAllCheckBox(self, event):
        """
        Установка/Снятие отметки выделения всех найденных документов.
        Обработчик события.
        """
        check = event.IsChecked()
        for i in range(self.docs_listCtrl.GetItemCount()):
            self.docs_listCtrl.CheckItem(i, check=check)

        event.Skip()

    def clear_not_exists_links_doc(self, doc_uuid):
        """
        Удалить не существующие ссылки документа.
        """
        doc = ic.metadata.THIS.mtd.scan_document.create()
        doc.load_obj(doc_uuid)
        return doc.GetManager().clear_not_exist_links(doc)
        
    def onClearLinksToolClicked(self, event):
        """
        Обработчик удаления не существующих ссылок.
        """
        item_count = self.docs_listCtrl.GetItemCount()
        is_checked = bool(len([i for i in range(item_count) if self.docs_listCtrl.IsChecked(i)]))
        if is_checked:
            try:
                for i in range(item_count - 1, -1, -1):
                    if self.docs_listCtrl.IsChecked(i):
                        document = self.documents[i]
                        doc_uuid = document['uuid']
                        self.clear_not_exists_links_doc(doc_uuid)
            except:
                log.fatal(u'Ошибка удаления не существующих ссылок документов')
        else:
            # Нет отмеченных документов, но есть текущий документ
            idx = self.docs_listCtrl.GetFirstSelected()
            if idx != -1:
                document = self.documents[idx]
                doc_uuid = document['uuid']
                self.clear_not_exists_links_doc(doc_uuid)
        
        event.Skip()
        
        
def open_ctrl_search_doc_page(main_win=None):
    """
    Открыть страницу поиска/печати документа из архива.
    @param main_win: Главное окно приложения.
    """
    if main_win is None:
        main_win = ic.getMainWin()

    page = icCtrlDocPanel(parent=main_win)
    main_win.AddOrgPage(page, u'Управление документами')
    return
