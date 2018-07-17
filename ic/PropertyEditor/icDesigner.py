#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Редактор ресурсов и форм.
"""

import wx
import sys
from ic.utils import ic_i18n

_ = wx.GetTranslation

__version__ = (1, 0, 0, 5)


class icDesignerApp(wx.App):
    """
    Приложение дезайнера.
    """

    def OnInit(self):
        """
        Инициализация приложения.
        """
        self.locale = None
        lang = wx.LANGUAGE_DEFAULT
        wx.Locale.AddCatalogLookupPathPrefix(ic_i18n.LANG_DIR)
        self.updateLanguage(lang)
        return True
        
    def OnExit(self):
        pass

    def updateLanguage(self, lang):
        # Make *sure* any existing locale is deleted before the new
        # one is created.  The old C++ object needs to be deleted
        # before the new one is created, and if we just assign a new
        # instance to the old Python variable, the old C++ locale will
        # not be destroyed soon enough, likely causing a crash.
        if self.locale:
            assert sys.getrefcount(self.locale) <= 2
            del self.locale
        
        # create a locale object for this language
        self.locale = wx.Locale(lang)
        if self.locale.IsOk():
            self.locale.AddCatalog('restree')
        else:
            self.locale = None

if __name__ == '__main__':
    # Тестируем
    app = icDesignerApp(0)
    frame = wx.Frame(None, -1, 'Frame')
    panel = wx.Panel(frame)
    st1 = wx.StaticText(panel, -1, _('Add'), pos=(10, 10))
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()
