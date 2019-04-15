#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Панель ведения планирования.
"""

import wx

from . import edit_plan_panel_proto
from ic.log import log
from ic.engine import form_manager
from ic.engine import ic_user
from ic.utils import ic_util


__version__ = (0, 1, 1, 1)


class icEditPlanPanel(edit_plan_panel_proto.icEditPlanPanelProto,
                      form_manager.icFormManager):
    """
    Панель ведения планирования.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        edit_plan_panel_proto.icEditPlanPanelProto.__init__(self, *args, **kwargs)

        self.init()

    def init(self):
        """
        Инициализация внутренних контролов.
        @return: True/False.
        """
        # Отключить кнопку распахивания, т.к. уже распахнут сплиттер
        self.ctrl_toolBar.EnableTool(self.expand_tool.GetId(), False)
        return False

    def setPlanMetatree(self, plan_metatree=None):
        """
        Установить план для редактирования.
        @param plan_metatree: Объект метадерева плана.
        """
        self.plan_browser.setMetaTree(plan_metatree)

    def onCollapseToolClicked(self, event):
        """
        Обработчик свертывания дерева плана.
        """
        self.collapseSplitterPanel(self.plan_browser.browser_splitter, self.ctrl_toolBar,
                                   collapse_tool=self.collapse_tool, expand_tool=self.expand_tool)
        event.Skip()

    def onExpandToolClicked(self, event):
        """
        Обработчик развертывания дерева плана.
        """
        self.expandSplitterPanel(self.plan_browser.browser_splitter, self.ctrl_toolBar,
                                 collapse_tool=self.collapse_tool, expand_tool=self.expand_tool)
        event.Skip()


def show_edit_plan_panel(parent=None, plan_metatree=None):
    """
    Открыть панель ведения планирования.
    @param parent: Родительское окно панели.
        Если не определено, то берется главное окно приложения.
    @param plan_metatree: Объект дерева метадерева плана.
        Объект может задаваться паспортом или объектом
    @return: True/False.
    """
    try:
        if parent is None:
            parent = ic_user.getMainWin()

        panel = icEditPlanPanel(parent=parent)

        if ic_util.is_pasport(plan_metatree):
            # Если план задается паспортом, то необходимо
            # создать объект
            kernel = ic_user.getKernel()
            plan_metatree = kernel.Create(plan_metatree)

        # Установить метадерево плана
        panel.setPlanMetatree(plan_metatree)

        title = str(plan_metatree.description) if plan_metatree else u'---'
        result = ic_user.addMainNotebookPage(panel, title)
        return result is not None
    except:
        log.fatal(u'Ошибка открытия панели ведения планирования.')
    return False
