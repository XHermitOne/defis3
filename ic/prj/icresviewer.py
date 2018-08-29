#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Просмотрщик ресурсного узла проекта.
"""

# --- Подключение библиотек ---
from ic.utils import util
from ic.interfaces import icprjnodeviewer
from ic.PropertyEditor import icResTree
from ic.log import log


class icResPrjNodeViewer(icprjnodeviewer.icPrjNodeViewerInterface,
                         icResTree.icResTree):
    """
    Просмотрщик ресурсного узла проекта.
    """

    def __init__(self, parent, Node_):
        """
        Конструктор.
        """
        icprjnodeviewer.icPrjNodeViewerInterface.__init__(self, parent, Node_)

        eval_space = util.InitEvalSpace()
        icResTree.icResTree.__init__(self, parent, evalSpace=eval_space)
        
        self._full_res_file_name = Node_.getFullResFileName()
        
        # Прочитать ресурс
        res = self._getNodeRes(Node_)
        self.parseTree(res[list(res.keys())[0]])
        self.Expand(self.root)

    def getNodeResFileName(self):
        """
        Имя файла резурса.
        """
        return self._full_res_file_name
        
    def _getNodeRes(self, Node_):
        """
        Определить ресурс узла.
        """
        try:
            return Node_.getMyRes()
        except:
            log.error()
            return {}
        
    def getSelectedObject(self):
        """
        Выделенный объект.
        """
        item = self.GetSelection()
        if item.IsOk():
            return self.GetItemData(item)
        return None

    def OnSelChanged(self, evt):
        """
        Функция отрабатывает при изменении выбранного пункта дерева.
        """
        try:
            self.parent.GetParent().setPassportLabel()
        except:
            self.parent.GetParent().setPassportLabel(u'')

