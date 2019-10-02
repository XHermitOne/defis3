#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль класса окружения проекта.
"""

# Подключение библиотек
import wx

from ic.imglib import common as imglib
from ic.editor import environment_edit_dlg

from . import prj_node
from ic.kernel import icsettings

__version__ = (0, 1, 2, 1)

_ = wx.GetTranslation


class icPrjEnv(prj_node.icPrjNode):
    """
    Окружение.
    """
    def __init__(self, parent=None):
        """
        Конструктор.
        """
        prj_node.icPrjNode.__init__(self, parent)
        self.img = imglib.imgEdtEnv
        self.description = u'Окружение'
        self.name = u'Окружение'

        # Объект дизайнера
        self.designer = None

    def design(self):
        """
        Запуск дизайнера.
        """
        # Т.к. *.ini файл мог быть отредактирован, то
        # переписать переменные в окружении
        prj_name = self.getRoot().name
        icsettings.setProjectSettingsToEnvironment(prj_name,
                                                   ReDefine_=True)
        
        self.designer = environment_edit_dlg.icEnvironmentEditDlg(parent=self.getRoot().getPrjTreeCtrl(),
                                                                  project_root=self.getRoot())

        self.designer.design()
        self.designer = None

    def onNodeActivated(self, event):
        """
        Активация узла (двойной щелчок мыши на узле).
        """
        self.design()

    def onNodePopup(self, event):
        """
        Вызов всплывающего меню узла.
        """
        pass
