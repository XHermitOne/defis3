#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговая форма редактирования настроек приложения.
"""

import wx
from archive.forms import settings_form_proto
import ic

# Version
__version__ = (0, 0, 1, 1)


class icSettingsEditDlg(settings_form_proto.icSettingsDlgProto):
    """
    Диалоговая форма редактирования настроек приложения.
    """
    
    def onSettingsInitDialog(self, event):
        """
        Инициализация.
        """
        doc_dir = ic.settings.THIS.SETTINGS.doc_dir.get()
        doc_dir = ic.getHomeDir() if doc_dir is None else doc_dir
        self.docdir_dirPicker.SetPath(doc_dir)

        event.Skip()
    
    def onCancelButtonClick(self, event):
        """
        Обработчик кнопки <Отмена>.
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()
        
    def onOkButtonClick(self, event):
        """
        Обработчик кнопки <OK>.
        """
        ic.settings.THIS.SETTINGS.doc_dir.set(self.docdir_dirPicker.GetPath())
        
        self.EndModal(wx.ID_OK)
        event.Skip()


def edit_settings_dlg(parent=None):
    """
    Функция вызова фрмы редактирования настроек приложения.
    """
    if parent is None:
        parent = ic.getMainWin()
        
    dlg = icSettingsEditDlg(parent=parent)
    dlg.ShowModal()
    
                      
def test():
    """
    Функция тестирования.
    """    
    app = wx.PySimpleApp()
    
    dlg = icSettingsEditDlg(parent=None)
    dlg.ShowModal()
    
    app.MainLoop()
    

if __name__ == '__main__':
    test()
