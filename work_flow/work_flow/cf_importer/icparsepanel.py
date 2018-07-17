#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
Класс панели парсинга файла CF конфигурации 1с.
"""

# --- Imports ---
import os
import os.path

from . import icWizardPanelProto

from ic.dlg import ic_dlg
# from ic.log import util

__version__ = (0, 0, 0, 2)


class icParsePanel(icWizardPanelProto.icParsePanelPrototype):
    """
    Класс панели парсинга файла CF конфигурации 1с.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструтор.
        """
        icWizardPanelProto.icParsePanelPrototype.__init__(self, *args, **kwargs)

    def onCFFileChoiceButtonMouseClick(self, event):
        """
        Обработчик кнопки выбора CF файла конфигурации 1с.
        """
        default_dir = os.getcwd()
        cf_file_name = ic_dlg.icFileDlg(self, u'Выберите файл конфигурации 1с',
                                        u'Файл конфигурации 1с(*.cf)|*.cf', default_dir)
        if cf_file_name:
            self.cfFileTxt.SetValue(cf_file_name)
            default_dir = os.path.join(os.path.dirname(cf_file_name),
                                       os.path.basename(cf_file_name).replace('.', '_').replace(' ', '_'))
            default_dir = os.path.abspath(default_dir)
            self.cfDirTxt.SetValue(default_dir)
            
        if not self.cfFileTxt.GetValue() or not self.cfDirTxt.GetValue():
            wizard = self.GetParent().GetParent()
            self.GetParent().SetNext(wizard.getFinishPage())
        else:
            wizard = self.GetParent().GetParent()
            self.GetParent().SetNext(wizard.getNextPage(self.GetParent()))
            
        event.Skip()
    
    def onCFDirChoiceButtonMouseClick(self, event):
        """
        Обработчик кнопки выбора папки конфигурации 1с.
        """
        default_dir = os.getcwd()
        cf_dir_path = ic_dlg.icDirDlg(self, u'Выберите папку конфигурации 1с', default_dir)
        if cf_dir_path:
            self.cfDirTxt.SetValue(cf_dir_path)
            
        if not self.cfFileTxt.GetValue() or not self.cfDirTxt.GetValue():
            wizard = self.GetParent().GetParent()
            self.GetParent().SetNext(wizard.getFinishPage())
        else:
            wizard = self.GetParent().GetParent()
            self.GetParent().SetNext(wizard.getNextPage(self.GetParent()))
            
        event.Skip()
