#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль классов приложений.
"""

# --- Подключение библиотек ---
import os
import os.path
import locale
import wx

from ic.kernel import ickernel
from ic.log import log

__version__ = (0, 1, 1, 1)

# Русская локаль
RU_LOCALE = 'ru_RU.UTF-8'


class icWXApp(wx.App, ickernel.icKernel):
    """
    Класс приложения библиотеки WX.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        # Вызвать конструктор приложения Wx
        wx.App.__init__(self, 0)

        # ВНИМАНИЕ! Выставить русскую локаль
        # Это необходимо для корректного отображения календарей,
        # форматов дат, времени, данных и т.п.

        # Системная локаль Python
        locale.setlocale(locale.LC_ALL, RU_LOCALE)
        # Локаль wxPython
        self.locale = wx.Locale()
        self.locale.Init(wx.LANGUAGE_RUSSIAN)

        # Ядро
        ickernel.icKernel.__init__(self)

    # --- Управление поведением системы ---
    def setBehaviour(self, behaviour_res_filename):
        """
        Установить поведение системы.

        :param behaviour_res_filename: Имя файла ресурса со связями.
        """
        from ic.components import icResourceParser
        try:
            file_name, file_ext = os.path.splitext(behaviour_res_filename)
            return icResourceParser.icCreateObject(file_name, file_ext[1:])
        except:
            log.fatal(u'Ошибка установки поведения системы из файла: <%s>' % behaviour_res_filename)
        return None
