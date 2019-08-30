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

__version__ = (0, 1, 1, 1)


class icResPrjNodeViewer(icprjnodeviewer.icPrjNodeViewerInterface,
                         icResTree.icResTree):
    """
    Просмотрщик ресурсного узла проекта.
    """

    def __init__(self, parent, node):
        """
        Конструктор.
        """
        icprjnodeviewer.icPrjNodeViewerInterface.__init__(self, parent, node)

        eval_space = util.InitEvalSpace()
        icResTree.icResTree.__init__(self, parent, evalSpace=eval_space)
        
        self._full_res_file_name = node.getFullResFileName()
        
        # Прочитать ресурс
        res = self._getNodeRes(node)
        self.parseTree(res[list(res.keys())[0]])
        self.Expand(self.root)

    def getNodeResFileName(self):
        """
        Имя файла резурса.
        """
        return self._full_res_file_name
        
    def _getNodeRes(self, node):
        """
        Определить ресурс узла.
        """
        try:
            return node.getMyRes()
        except:
            log.fatal(u'Ошибка определения ресурса узла проекта')
        return dict()
        
    def getSelectedObject(self):
        """
        Выделенный объект.
        """
        item = self.GetSelection()
        if item.IsOk():
            return self.GetItemData(item)
        return None

    def OnSelChanged(self, event):
        """
        Функция отрабатывает при изменении выбранного пункта дерева.
        """
        try:
            self.parent.GetParent().setPassportLabel()
        except:
            self.parent.GetParent().setPassportLabel(u'')

