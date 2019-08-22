#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Редактор ресурсов и форм.
"""

import wx
import sys
# import locale

from ic.utils import i18nfunc
from ic.engine import glob_functions
from ic.utils import ic_util
from ic.log import log

_ = wx.GetTranslation

__version__ = (1, 1, 1, 1)


class icDesignerApp(wx.App):
    """
    Приложение дезайнера.
    """

    def OnInit(self):
        """
        Инициализация приложения.
        """
        # ВНИМАНИЕ! Выставить русскую локаль
        # Это необходимо для корректного отображения календарей,
        # форматов дат, времени, данных и т.п.

        # Системная локаль Python
        # locale.setlocale(locale.LC_ALL, RU_LOCALE)
        # Локаль wxPython
        # self.locale = wx.Locale()
        # self.locale.Init(wx.LANGUAGE_RUSSIAN)

        self.locale = None
        lang = wx.LANGUAGE_DEFAULT
        wx.Locale.AddCatalogLookupPathPrefix(i18nfunc.LANG_DIR)
        self.updateLanguage(lang)
        return True
        
    def OnExit(self):
        """
        Обработчик выхода из приложения.
        """
        cur_user = glob_functions.getCurUser()
        # Завершить работу пользователя
        if cur_user:
            cur_user.Logout()
        # Выполнение обработчика события при старте движка
        log.info(u'Выход из системы. Режим редактора')
        ic_util.print_defis_logo()
        return True

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
