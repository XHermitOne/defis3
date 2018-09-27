#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль класса окружения проекта.
"""

# Подключение библиотек
import wx

from ic.imglib import common as imglib
from ic.editor import icenvironmenteditor
from . import prj_node
from ic.kernel import icsettings

__version__ = (0, 1, 1, 1)

_ = wx.GetTranslation


class PrjEnv(prj_node.PrjNode):
    """
    Окружение.
    """
    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        prj_node.PrjNode.__init__(self, Parent_)
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
        
        self.designer = icenvironmenteditor.icEnvironmentEditDlg(parent=self.getRoot().getPrjTreeCtrl(),
                                                                 ProjectRoot_=self.getRoot())
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
