#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль класса окружения проекта.
"""

# Подключение библиотек
import wx
import ic.imglib.common as imglib
from ic.editor import icenvironmenteditor
from . import prj_node
from ic.kernel import icsettings

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

    def design(self):
        """
        Запуск дизайнера.
        """
        # Т.к. *.ini файл мог быть отредактирован, то
        # переписать переменные в окружении
        prj_name = self.getRoot().name
        icsettings.setProjectSettingsToEnvironment(prj_name,
                                                   ReDefine_=True)
        
        self.designer = icenvironmenteditor.icEnvironmentEditDlg(self.getRoot().getParent().ide_frame,
                                                                 ProjectRoot_=self.getRoot())
        self.designer.design()

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
