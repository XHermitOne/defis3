#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Диалоговое окно выбора документа.
"""

import os.path
import wx
from . import select_document_dlg_proto
from ic.log import log
from ic.utils import ic_file
from ic.engine import ic_user


class icDocumentSelectPanel(select_document_dlg_proto.icDocumentSelectPanelProto):
    """
    Панель выбора документов по фильтру.
    """
    pass


class icDocumentSelectDlg(select_document_dlg_proto.icDocumentSelectDlgProto):
    """
    Диалоговое окно выбора документов по фильтру.
    """

    def onInitDlg(self, event):
        """
        Инициализация диалога.
        """
        # UUID выбранного документа
        self._selected_doc_uuid = None

        event.Skip()

    def getSelectedDocUUID(self):
        """
        UUID выбранного документа.
        """
        return self._selected_doc_uuid

    def onCancelButtonClick(self, event):
        """
        Обработчик кнопки <Отмена>.
        """
        self._selected_doc_uuid = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        Обработчик кнопки <OK>.
        """
        self._selected_doc_uuid = self.doc_select_panel.document_list.getSelectedObjUUID()

        self.EndModal(wx.ID_OK)
        event.Skip()

    def init(self, doc=None):
        """
        Инициализация диалогового окна.
        @param doc: Объект документа.
        """
        if doc is None:
            log.warning(u'Не обределен объект документа для выбора')
            return

        self.SetTitle(u'Выбор документа <%s>' % doc.getDescription())

        self._initDocList(doc)
        self._initFilterCtrl(doc)

        # И обновляем контрол
        self.doc_select_panel.document_list.refreshDataset()

    def _initDocList(self, doc):
        """
        Инициализация списка документов.
        @param doc: Объект документа.
        """
        # Установить колонки списка документов
        # Колонки создаются только из описывающих объект реквизитов
        requisites = [requisite for requisite in doc.getChildrenRequisites() if requisite.isDescription()]
        columns = list()
        for requisite in requisites:
            name = requisite.getName()
            label = requisite.getLabel()
            column = dict(activate=True,
                          name=name,
                          label=label,
                          sort=False)
            columns.append(column)

        self.doc_select_panel.document_list.setColumnsSpc(*columns)
        # ВНИМАНИЕ! При инициализации устанавливаем источник данных
        self.doc_select_panel.document_list.setDataSource(doc)

    def _initFilterCtrl(self, doc):
        """
        Инициализация контрола фильтров документа.
        @param doc: Объект документа.
        """
        env = doc.getFilterEnv()
        self.doc_select_panel.doc_filter_ctrl.setEnvironment(env)
        filename = os.path.join(ic_file.getProfilePath(),
                                ic_user.getPrjName(),
                                'doc_%s_filter.save' % doc.getUUID())
        # ВНИМАНИЕ! При инициализации устанавливаем фильтр
        self.doc_select_panel.doc_filter_ctrl.setFilterFileName(filename)


def select_document_dlg(parent=None, doc=None):
    """
    Выбрать документ через диалоговое окно выбора документа.
    @param parent: Родительское окно.
    @param doc: Объект документа.
    @return: UUID выбранного документа.
    """
    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    dlg = icDocumentSelectDlg(parent)
    dlg.init(doc)
    dlg.ShowModal()
    return dlg.getSelectedDocUUID()


def test():
    """
    Функция тестирования диалогового окна.
    """
    app = wx.PySimpleApp()
    select_document_dlg()
    app.MainLoop()


if __name__ == '__main__':
    test()
