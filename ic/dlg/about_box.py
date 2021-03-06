#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль диалоговых функций окна <О программе...>.
"""

import os
import os.path
import wx
import wx.adv
from wx.lib.wordwrap import wordwrap

from ic.engine import glob_functions
from ic.utils import extfunc
from ic import config
from ic.log import log

__version__ = (0, 1, 1, 1)

# Текст копирайта по умолчанию
DEFAULT_COPYRIGHT = u'(C) 2002 Alexander Kolchanov and Andrei Okoneshnikov'
DEFAULT_AUTHORS = (u'Alexander Kolchanov / Александр Колчанов',
                   u'Andrei Okoneshnikov / Андрей Оконешников',)
DEFAULT_LICENSE_FILENAME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'license.txt')


def _show_about_box(parent, name, version, description,
                    copyright, authors,
                    web_site_url, web_site_label,
                    license, icon):
    """
    Отобразить диалоговое окно <О программе...>

    :param parent: Родительское окно.
    :param name: Наименование программы.
    :param version: Версия программы.
    :param description: Описание программы.
    :param copyright: Копирайт.
    :param authors: Авторы программы.
    :param web_site_url: Адрес веб-сайта программы.
    :param web_site_label: Надпись ссылкы веб-сайта программы.
    :param license: Текст лицензии.
    :param icon: Объект wx.Icon иконки программы.
    """
    try:
        info = wx.adv.AboutDialogInfo()
        info.Name = name
        info.Version = version
        info.Copyright = copyright
        info.Description = wordwrap(description, 350, wx.ClientDC(parent))
        if web_site_url:
            info.WebSite = (web_site_url,
                            web_site_label if web_site_label else web_site_url)
        info.Developers = list(authors)

        info.License = wordwrap(license, 500, wx.ClientDC(parent))
        if isinstance(icon, wx.Icon):
            info.Icon = icon

        # Then we call wx.AboutBox giving it that info object
        wx.adv.AboutBox(info)
    except:
        log.fatal(u'Ошибка отображения окна <О программе...>')


def showAbout(parent=None, name=None, version=None, description=None,
              copyright=None, authors=None,
              web_site_url=None, web_site_label=None,
              license=None, icon_filename=None):
    """
    Отобразить диалоговое окно <О программе...>

    :param parent: Родительское окно.
    :param name: Наименование программы.
    :param version: Версия программы.
    :param description: Описание программы.
    :param copyright: Копирайт.
    :param authors: Авторы программы.
    :param web_site_url: Адрес веб-сайта программы.
    :param web_site_label: Надпись ссылкы веб-сайта программы.
    :param license: Текст лицензии.
    :param icon_filename: Имя файла иконки программы.
    """
    if parent is None:
        parent = glob_functions.getMainWin()

    if name is None:
        main_win = glob_functions.getMainWin()
        name = main_win.getTitle()

    prj_package = None
    if version is None or description is None:
        prj_package = glob_functions.getPrjPackage()

    if version is None:
        try:
            version = prj_package.__version__
            if type(version) in (list, tuple):
                version = u'.'.join([str(v) for v in version])
        except AttributeError:
            version = u''

    if description is None:
        try:
            description = prj_package.__doc__
        except AttributeError:
            description = u''

    if copyright is None:
        copyright = DEFAULT_COPYRIGHT
    if authors is None:
        authors = DEFAULT_AUTHORS
    if license is None:
        license = extfunc.load_file_text(DEFAULT_LICENSE_FILENAME,
                                         to_unicode=True)
    if icon_filename is None:
        main_win = glob_functions.getMainWin()
        icon_filename = main_win.getIconFilename()
    icon = wx.Icon(icon_filename, wx.BITMAP_TYPE_ICO) if icon_filename else None

    return _show_about_box(parent=parent, name=name,
                           version=version, description=description,
                           copyright=copyright, authors=authors,
                           web_site_url=web_site_url, web_site_label=web_site_label,
                           license=license, icon=icon)
