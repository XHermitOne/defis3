#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль формы <icBrowseDocLinksPanelProto>. 
Сгенерирован проектом DEFIS по модулю формы-прототипа wxFormBuider.
"""

import wx

import ic
from ic.log import log
from ic.dlg import dlgfunc

# Для управления взаимодействия с контролами wxPython
# используется менеджер форм <form_manager.icFormManager>
from ic.engine import form_manager

from . import browse_doc_links_proto

__version__ = (0, 1, 1, 1)


class icBrowseDocLinksPanel(browse_doc_links_proto.icBrowseDocLinksPanelProto, form_manager.icFormManager):
    """
    Форма просмотра связанных по ссылкам документов.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        browse_doc_links_proto.icBrowseDocLinksPanelProto.__init__(self, *args, **kwargs)
        
    def onEditToolClicked(self, event):
        """
        Обработчик инструмента редактирования карточки документа.
        """
        selected_item = self.links_treeListCtrl.GetSelection()
        if selected_item:
            record = self.links_treeListCtrl.GetItemData(selected_item)
            if record:
                doc_uuid = record['uuid']
                doc = ic.metadata.archive.mtd.scan_document.create()
                doc.load_obj(doc_uuid)
                log.debug(u'Редактирование документа UUID <%s>' % doc_uuid)            
                from archive.forms import edit_doc_form
                
                result = edit_doc_form.edit_doc_dlg(doc=doc)
                if result:
                    doc.save_obj()
                    self.refresh_tree()
            else:
                log.warning(u'Нет прикрепленных данных к элементу дерева')
        else:
            dlgfunc.openWarningBox(u'ВНИМАНИЕ',
                                u'Выберите документ для редактирования')
        event.Skip()

    def onViewToolClicked(self, event):
        """
        Обработчик инструмента просмотра сканированного документа.
        """
        selected_item = self.links_treeListCtrl.GetSelection()
        if selected_item:
            record = self.links_treeListCtrl.GetItemData(selected_item)
            if record:
                filename = record['file_name']
                doc = ic.metadata.archive.mtd.scan_document.create()
                doc.GetManager().view_scan_file(filename)               
            else:
                log.warning(u'Нет прикрепленных данных к элементу дерева')
        else:
            dlgfunc.openWarningBox(u'ВНИМАНИЕ',
                                u'Выберите документ для просмотра')
        event.Skip()

    def init(self):
        """
        Инициализация панели.
        """
        self.init_img()
        self.init_ctrl()
        
    def init_img(self):
        """
        Инициализация изображений.
        """
        self.setLibImages_ToolBar(self.ctrl_toolBar, 
                                  view_tool='eye.png',
                                  edit_tool='document--pencil.png')
        
    def init_ctrl(self):
        """
        Инициализация контролов.
        """
        self.links_treeListCtrl.AddColumn(u'Наименование')
        self.links_treeListCtrl.AddColumn(u'№ док.')
        self.links_treeListCtrl.AddColumn(u'Дата')
        self.links_treeListCtrl.AddColumn(u'№ док. контрагента')
        self.links_treeListCtrl.AddColumn(u'Дата контрагента')
        self.links_treeListCtrl.AddColumn(u'Контрагент')
        self.links_treeListCtrl.AddColumn(u'Описание')
        self.links_treeListCtrl.AddColumn(u'Комментарии')
        self.links_treeListCtrl.SetMainColumn(0)

        self.links_treeListCtrl.SetColumnWidth(0, 600)
        self.links_treeListCtrl.SetColumnWidth(1, 100)
        self.links_treeListCtrl.SetColumnWidth(2, 80)
        self.links_treeListCtrl.SetColumnWidth(3, 100)
        self.links_treeListCtrl.SetColumnWidth(4, 80)
        self.links_treeListCtrl.SetColumnWidth(5, 450)
        self.links_treeListCtrl.SetColumnWidth(6, wx.COL_WIDTH_AUTOSIZE)
        self.links_treeListCtrl.SetColumnWidth(7, wx.COL_WIDTH_AUTOSIZE)

    def init_tree(self, tree_data, doc_uuid=None):
        """
        Заполнение дерева связей.
        """
        self.doc_uuid = doc_uuid
        def set_cur_doc_bold(tree_ctrl, item, node):
            """
            Выделить жирным текущий документ.
            """
            if node.get('uuid', '') == doc_uuid:
                tree_ctrl.SetItemBold(item)
                
        self.setTree_TreeListCtrl(self.links_treeListCtrl, tree_data,
                                  columns=('doc_name', 'n_doc', 'doc_date_str', 'n_obj', 'obj_date_str', 'contragent', 'description', 'comment'),
                                  do_expand_all=True,
                                  ext_func=set_cur_doc_bold)

    def refresh_tree(self, doc_uuid=None):
        """
        Обновить дерево для указанного документа.
        """
        if doc_uuid is None:
            doc_uuid = self.doc_uuid
            
        doc = ic.metadata.archive.mtd.scan_document.create()
        doc.load_obj(doc_uuid)
        links_data = doc.GetManager().get_doc_links(doc)
        self.init_tree(links_data, doc_uuid)
        
    
def browse_doc_links_panel(doc=None, title=u''):
    """
    Просмотр связанных документов.
    """
    if doc is None:
        log.warning(u'Просмотр связей документа. Не указан документ')
        return 
    links_data = doc.GetManager().get_doc_links(doc)
    # log.debug(u'Данные о связях: %s' % str(links_data))
    
    if not title:
        title = u'Связи документа <%s %s>' % (doc.getRequisiteValue('doc_name'), 
                                              doc.getRequisiteValue('n_doc'))
        
    main_win = ic.getMainWin()
        
    panel = icBrowseDocLinksPanel(main_win)
    panel.init()
    panel.init_tree(links_data, doc.getUUID())
    main_win.addPage(panel, title)
    