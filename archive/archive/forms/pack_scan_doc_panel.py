#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль формы <icPackScanDocPanelProto>.
Сгенерирован проектом DEFIS по модулю формы-прототипа wxFormBuider.
"""

import os
import os.path
import wx
from . import pack_scan_doc_panel_proto
from . import edit_doc_form_proto

import ic
from ic.log import log
from ic.dlg import std_dlg
from ic.dlg import ic_dlg
from ic.dlg import quick_entry_panel
from ic.engine import glob_functions

from . import group_manipulation_dlg
from . import new_doc_panel

# Для управления взаимодействия с контролами wxPython
# используется менеджер форм <form_manager.icFormManager>
from ic.engine import form_manager

__version__ = (0, 1, 1, 2)

DEFAULT_DB_DATE_FMT = '%Y-%m-%d'
DEFAULT_DATE_FMT = '%d.%m.%Y'
NONE_DATE = '00.00.0000'


class icQuickEntryPackScanPanel(edit_doc_form_proto.icQuickEntryPackScanPanelProto):
    """
    Панель быстрого ввода.
    """
    pass


class icPackScanDocPanel(pack_scan_doc_panel_proto.icPackScanDocPanelProto,
                         form_manager.icFormManager,
                         new_doc_panel.icDocCardPanelManager):
    """
    Форма пакетной обработки документов.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        pack_scan_doc_panel_proto.icPackScanDocPanelProto.__init__(self, *args, **kwargs)

        # Режим быстрого ввода
        self.quick_entry_mode = False

    def init(self):
        """
        Инициализация панели.
        """
        self.init_img()
        self.init_ctrl()

        # Инициализация навигатора документов
        self.doc_navigator = ic.metadata.archive.mtd.pack_scan_doc_form_manager.create()
        self.doc_navigator.setDocListCtrlColumns('nn', 'n_scan_pages', lambda rec: '+' if rec['is_duplex'] else '',
                                                 'n_doc', lambda rec: rec['doc_date'].strftime(DEFAULT_DATE_FMT) if rec['doc_date'] else NONE_DATE,
                                                 'n_obj', lambda rec: rec['obj_date'].strftime(DEFAULT_DATE_FMT) if rec['obj_date'] else NONE_DATE,
                                                 'doc_name', 'c_agent')
        self.doc_navigator.setSlaveListCtrl(self.docs_listCtrl)

        self.refreshDocList()

    def init_img(self):
        """
        Инициализация изображений.
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

    def init_ctrl(self):
        """
        Инициализация контролов.
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
        dataset = self.doc_navigator.getDocDataset()
        scan_pages = [dataset[idx].get('n_scan_pages', 0) for idx in check_idx_list]
        return sum(scan_pages)

    def onArchiveToolClicked(self, event):
        """
        Обработчик передачи пакета в архив.
        """
        doc_indexes = self.getCheckedItems_list_ctrl(self.docs_listCtrl)
        if doc_indexes:
            archive_doc = ic.metadata.archive.mtd.scan_document.create()
            pack_result = True
            # ВНИМАНИЕ! Чтобы не было нарушения индексов перенос документов
            # делаем с конца списка документов (старших индексов).
            # Для этого делаем обратную сортировку списка индексов.
            doc_indexes = sorted(doc_indexes, reverse=True)
            log.debug(u'Перенос в архив документов. Индексы: %s' % str(doc_indexes))
            for doc_idx in doc_indexes:
                doc = self.doc_navigator.getSlaveDocument(index=doc_idx)
                scan_filename = doc.getRequisiteValue('file_name')
                if scan_filename and os.path.exists(scan_filename):
                    result = self.doc_navigator.remove_toDoc(UUID=doc.getUUID(), to_document=archive_doc,
                                                             requisite_replace={'scan_doc_to': 'pack_doc_scan_to',
                                                                                'scan_doc_from': 'pack_doc_scan_from'},
                                                             bRefresh=False)
                    if not result:
                        ic_dlg.icWarningBox(u'ВНИМАНИЕ',
                                            u'Ошибка переноса документа <%s> в архив' % doc.getRequisiteValue('n_doc'))

                    pack_result = pack_result and result
                else:
                    n_doc = doc.getRequisiteValue('n_doc')
                    msg = u'Файл скана отсутствует в карточке документа <%s>. Перенос не выполнен' % n_doc
                    log.warning(msg)
                    ic_dlg.icWarningBox(u'ВНИМАНИЕ', msg)
                    pack_result = False

            if pack_result:
                ic_dlg.icMsgBox(u'АРХИВ',
                                u'Пакет документов перенесен в архив')
            self.refreshDocList(True)
        event.Skip()

    def onEditToolClicked(self, event):
        """
        Обработчик редактирования карточки документа.
        """
        from archive.forms import edit_doc_form
        self.doc_navigator.editDoc(edit_form_method=edit_doc_form.edit_document_dlg)
        event.Skip()

    def onGroupToolClicked(self, event):
        """
        Обработчик инструмента групповой настройки параметров сканирования документа.
        """
        pos = self.getToolLeftBottomPoint(self.ctrl_toolBar, self.group_tool)
        doc_dataset = self.doc_navigator.getDocDataset()
        nn_max = doc_dataset[-1].get('nn', 0) if doc_dataset else 0
        value = group_manipulation_dlg.show_group_manipulation_dlg(self,
                                                                   n_max=nn_max,
                                                                   position=pos)
        if value:
            n_begin = value.get('n_begin', 1)
            n_begin = n_begin - 1 if n_begin else 0
            n_end = value.get('n_end', self.docs_listCtrl.GetItemCount())
            n_end = n_end - 1 if n_end else self.docs_listCtrl.GetItemCount() - 1
            # self.checkItems_list_ctrl(self.docs_listCtrl, value.get('on_off', False),
            #                          n_begin, n_end)
            # log.debug(u'Диапазон [%d : %d]' % (n_begin, n_end))
            check_list = self.checkItems_requirement(self.docs_listCtrl, rows=self.doc_navigator.getDocDataset(),
                                                     requirement=lambda i, rec: rec['nn'] in list(range(n_begin+1, n_end+2)),
                                                     bSet=True)
            # log.debug(u'Индексы меток %s' % str(check_list))

            if value.get('n_pages', None) or value.get('is_duplex', None):
                n_pages = value.get('n_pages', None)
                n_pages = int(n_pages) if n_pages else 1
                is_duplex = value.get('is_duplex', None)
                is_duplex = bool(is_duplex) if is_duplex else False

                # for i in range(n_begin, n_end + 1):
                for i in check_list:
                    doc = self.doc_navigator.getSlaveDocument(index=i)
                    doc_uuid = doc.getUUID()
                    self._set_doc_pages_and_duplex(i, doc, doc_uuid,
                                                   n_pages, is_duplex)

            # Количество документов и страниц в обработке
            self.doc_count_staticText.SetLabel(str(self.getScanDocCount()))
            self.page_count_staticText.SetLabel(str(self.getScanPageCount()))

        event.Skip()

    def onImportToolClicked(self, event):
        """
        Обработчик импорта документов из БАЛАНСА.
        """
        popup_menu = ic.metadata.archive.mnu.load_select_popup_menu.create()

        # Включить все пункты меню для администратора
        is_admin = glob_functions.isAdministratorCurUser()
        log.info(u'Включение всех пунктов меню импорта для АДМИНИСТРАТОРА [%s]' % is_admin)
        popup_menu.findMenuItemByName('load_rlz_menuitem').Enable(is_admin)
        popup_menu.findMenuItemByName('load_ztr_menuitem').Enable(is_admin)
        popup_menu.findMenuItemByName('load_mt_menuitem').Enable(True)
        popup_menu.findMenuItemByName('load_os_menuitem').Enable(is_admin)

        popup_menu.GetManager().setPackScanPanel(self)
        popup_menu.popupByTool(self.import_tool)

        event.Skip()

    def onNPagesToolClicked(self, event):
        """
        Обработчик инструмента установки количества страниц документа.
        """
        idx = self.getItemSelectedIdx(self.docs_listCtrl)
        if idx != -1:
            document = self.doc_navigator.getSlaveDocument(index=idx, bLoad=True)
            n_pages = std_dlg.getIntegerDlg(self, u'СКАНИРОВАНИЕ',
                                            u'Укажите количество страниц документа',
                                            1, 500)
            is_duplex = std_dlg.getRadioChoiceDlg(self, u'СКАНИРОВАНИЕ',
                                                  u'Сканирование листа с 2-ч сторон?',
                                                  choices=(u'НЕТ', u'ДА'))
            if n_pages:
                document.setRequisiteValue('n_scan_pages', n_pages)

            if is_duplex is not None:
                document.setRequisiteValue('is_duplex', is_duplex)

            if n_pages or is_duplex is not None:
                document.save_obj()
                self.refreshDocList(bAutoUpdate=True)
        else:
            ic_dlg.icWarningBox(u'ВНИМАНИЕ!', u'Выберите документ для редактирования')
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

    def onScanToolClicked(self, event):
        """
        Обработчик запуска сканирования документов.
        """
        scan_manager = ic.getScanManager()
        check_idx_list = self.getCheckedItems_list_ctrl(ctrl=self.docs_listCtrl)
        log.debug(u'Список индексов сканированных документов в пакете %s' % check_idx_list)
        dataset = self.doc_navigator.getDocDataset()
        # ВНИМАНИЕ! У нас указываются листы. Если указывается дуплекс, то
        # количество страниц увеличивается в 2 раза
        scan_filenames = [(os.path.join(scan_manager.getScanPath(), 'scan%04d.pdf' % i),
                           int(dataset[item_idx]['n_scan_pages']) * (
                               2 if bool(dataset[item_idx]['is_duplex']) else 1),
                           bool(dataset[item_idx]['is_duplex'])) for i, item_idx in enumerate(check_idx_list)]
        scan_result = scan_manager.do_scan_pack(*scan_filenames)
        if not scan_result:
            event.Skip()
            log.warning(u'Ошибка сканирования пакета документов')
            return

        if check_idx_list:
            for i, item_idx in enumerate(check_idx_list):
                scan_filename, n_pages, is_duplex = scan_filenames[i]
                if not os.path.exists(scan_filename):
                    log.warning(u'Файл скана <%s> не найден' % scan_filename)
                    continue
                document = self.doc_navigator.getSlaveDocument(index=item_idx)
                log.debug(u'UUID сканируемого документа <%s>' % document.getUUID())
                result = self.put_doc_catalog(document, scan_filename)
                if result:
                    document.save_obj()

            ic_dlg.icMsgBox(u'СКАНИРОВАНИЕ',
                            u'Сканирование пакета документов завершено успешно')
            self.refreshDocList(True)

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

    def _viewDoc(self, document):
        """
        Просмотр документа.
        @param document: Объект документа.
        @return:
        """
        doc_filename = document.getRequisiteValue('file_name')
        if doc_filename and os.path.exists(doc_filename):
            self.viewDocFile(doc_filename)
        else:
            if doc_filename:
                ic_dlg.icWarningBox(u'ВНИМАНИЕ!',
                                    u'Не найден файл скана <%s> документа для просмотра' % doc_filename)
            else:
                ic_dlg.icWarningBox(u'ВНИМАНИЕ!', u'Отсутствует файл скана документа')

    def onViewToolClicked(self, event):
        """
        Обработчик просмотра документа.
        """
        self.doc_navigator.viewDoc(view_form_method=self._viewDoc)
        event.Skip()

    def onSelectDocItem(self, event):
        """
        Обработчик выбора документа.
        ВНИМАНИЕ! При выборе нового элемента списка и включенном режиме
        быстрого ввода необходимо выводить диалоговое окно
        быстрого ввода автоматически.
        """
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

    def _show_quick_entry_dlg(self, item_idx):
        """
        Отобразить окно быстрого ввода.
        @param item_idx: Индекс выбранного элемента.
        """
        dataset = self.doc_navigator.getDocDataset()
        # Получить текущую запись
        doc_rec = dataset[item_idx]
        # Подготовить данные для редактирования
        values = dict(docname_staticText=u'%d. %s' % (item_idx + 1, doc_rec['doc_name']),
                      ndoc_staticText=doc_rec['n_doc'],
                      docdate_staticText=doc_rec['doc_date'].strftime(DEFAULT_DATE_FMT) if doc_rec['doc_date'] else u'',
                      cagent_ndoc_staticText=u'Данные контрагента: ' + (doc_rec['n_obj'] if doc_rec['n_obj'] else u''),
                      cagent_docdate_staticText=(u'от ' + doc_rec['obj_date'].strftime(DEFAULT_DATE_FMT)) if doc_rec['obj_date'] else u'',
                      npages_spinCtrl=doc_rec['n_scan_pages'],
                      duplex_checkBox=bool(doc_rec['is_duplex']),
                      c_ndoc_staticText=doc_rec['n_obj'],
                      c_docdate_staticText=doc_rec['obj_date'].strftime(DEFAULT_DATE_FMT) if doc_rec['obj_date'] else u'')
        # Вызываем окно быстрого ввода
        edit_result = quick_entry_panel.quick_entry_edit_dlg(self,
                                                             title=u'Режим быстрого ввода',
                                                             size=wx.Size(525, 280),
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
            self.checkItems_list_ctrl(ctrl=self.docs_listCtrl,
                                      n_begin=item_idx, n_end=item_idx)
            # Перейти на следущую строку
            self.selectItem_list_ctrl(ctrl=self.docs_listCtrl,
                                      item_idx=item_idx + 1)

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
            doc = self.doc_navigator.getSlaveDocument()

        if doc_uuid is None:
            doc_uuid = doc.getUUID()

        # Обновить в БД отредактированные данные
        doc.update_obj(doc_uuid,
                       n_scan_pages=int(n_scan_pages),
                       is_duplex=int(is_duplex))

        dataset = self.doc_navigator.getDocDataset()
        # Обновить только одну строку списка
        dataset[item_idx]['n_scan_pages'] = int(n_scan_pages)
        dataset[item_idx]['is_duplex'] = int(is_duplex)

        self.doc_navigator.refreshDocListCtrlRow(index=item_idx)

    def refreshDocList(self, bAutoUpdate=False):
        """
        Обновление списка документов.
        @param bAutoUpdate: Произвести обновление датасета из БД?
        """
        if bAutoUpdate:
            self.doc_navigator.updateDocDataset()

        self.doc_navigator.refreshSortDocListCtrlRows(sort_fields=('nn', ))

        # Расцветка строк
        for i, doc_rec in enumerate(self.doc_navigator.getDocDataset()):
            if doc_rec['file_name'] and os.path.exists(doc_rec['file_name']):
                self.setRowForegroundColour_list_ctrl(self.docs_listCtrl,
                                                      i, wx.Colour('DARKGREEN'))
            else:
                self.setRowForegroundColour_list_ctrl(self.docs_listCtrl,
                                                      i, wx.Colour('DARKGOLDENROD'))


def show_pack_scan_doc_panel(title=u''):
    """
    @param title: Заголовок страницы нотебука главного окна.
    """
    try:
        main_win = ic.getMainWin()

        panel = icPackScanDocPanel(main_win)
        panel.init()
        main_win.AddPage(panel, title)
    except:
        log.fatal(u'Ошибка')


def open_pack_scan_doc_page(main_win=None, title=u'Пакетная обработка документов'):
    """
    Открыть страницу пакетной обработки и сканирования документов.
    @param main_win: Главное окно приложения.
    """
    try:
        if main_win is None:
            main_win = ic.getMainWin()

        page = icPackScanDocPanel(parent=main_win)
        page.init()
        main_win.AddOrgPage(page, title)
    except:
        log.fatal(u'Ошибка открытия страницы пакетной обработки')
