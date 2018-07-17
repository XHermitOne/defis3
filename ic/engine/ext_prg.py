#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Функции запуска внешних программ.
Все внешние программы д.б. описаны в словаре
EXTERNAL_PROGRAMMS_CFG в формате:
    {
        'имя программмы': {
            'description': 'описание программы',
            'linux_cmd': 'команда запуска в linux системах',
            'windows_cmd': 'команда запуска в windows системах',
            ...
            }
    }
"""

import sys
import os
import os.path
import wx

from ic.log import log
from ic.utils import system

__version__ = (0, 0, 1, 1)


FILE_PKG_DIRNAME = os.path.dirname(__file__) if os.path.dirname(__file__) else os.getcwd()
FMSX_DIRNAME = os.path.join(os.path.dirname(FILE_PKG_DIRNAME), 'contrib', 'fMSX')
IDE_EDITRA_START = os.path.join(os.path.dirname(os.path.dirname(FILE_PKG_DIRNAME)), 'ide', 'Editra-0.7.20', 'editra')
PYREDITOR_START = os.path.join(os.path.dirname(FILE_PKG_DIRNAME), 'contrib', 'pyreditor', 'pyreditor.pyw')

EXTERNAL_PROGRAMMS_CFG = {'calculator': {'description': u'Калькулятор',
                                         'linux_cmd': 'gnome-calculator&',
                                         'windows_cmd': None},
                          'editra': {'description': u'IDE Editra',
                                     'linux_cmd': '%s %s&' % (sys.executable, IDE_EDITRA_START),
                                     'windows_cmd': None},
                          'pyreditor': {'description': u'PyReditor. Редактор регулярных выражений',
                                        'linux_cmd': '%s %s&' % (sys.executable, PYREDITOR_START),
                                        'windows_cmd': None},
                          # 'kv2': {'description': u'King\'s Valley II MSX game',
                          #        'linux_cmd': 'cd %s; ./fmsx "./games/kingsvalley2_msx_abandonware.rom"&' % FMSX_DIRNAME,
                          #        'windows_cmd': None},
                          }


def run_external_programm(programm_name=None, run_cmd=None):
    """
    Запустить внешнюю программу.
    @param programm_name: Имя программы.
        Если имя программы не определено, то выводиться
        диалоговое окно выбора внешней программы.
    @param run_cmd: Командная строка запуска.
        Если команда не определена, то по имени программы
        она находится в словаре описания внешних программ.
    @return: True/False.
    """
    if run_cmd:
        # Просто определена команда и надо ее запустить
        return run_command(run_cmd)
    elif run_cmd is None and programm_name:
        # Команда запуска не определена, но указано имя программы
        prg = EXTERNAL_PROGRAMMS_CFG.get(programm_name, None)
        if prg:
            run_cmd = prg.get('linux_cmd', None) if system.isLinuxPlatform() else prg.get('windows_cmd', None)
            return run_command(run_cmd)
    else:
        # Ничего не определено. Необходимо выбрать программу для запуска
        desc_to_name = dict(
            [(prg.get('description', u''), prg_name) for prg_name, prg in EXTERNAL_PROGRAMMS_CFG.items()])
        descriptions = desc_to_name.keys()
        descriptions.sort()

        parent_win = wx.GetApp().GetTopWindow()
        dlg = None
        try:
            dlg = wx.SingleChoiceDialog(
                parent_win, u'Выбор внешней программы для запуска', u'Внешние программы',
                descriptions, wx.CHOICEDLG_STYLE)

            if dlg.ShowModal() == wx.ID_OK:
                selected_description = dlg.GetStringSelection()
                prg_name = desc_to_name.get(selected_description, None)
                log.debug(u'Выбор <%s> - <%s>' % (selected_description, prg_name))
                prg = EXTERNAL_PROGRAMMS_CFG.get(prg_name, None)
                if prg:
                    run_cmd = prg.get('linux_cmd', None) if system.isLinuxPlatform() else prg.get('windows_cmd', None)
                    return run_command(run_cmd)

            dlg.Destroy()
            dlg = None
        except:
            if dlg:
                dlg.Destroy()
                dlg = None
            log.fatal(u'Ошибка выбора внешней программы для запуска')
    return False


def run_command(run_cmd):
    """
    Запуск комманды ОС.
    @param run_cmd: Команндная строка запуска.
    @return: True/False.
    """
    if run_cmd is None:
        log.warning(u'Команда запуска внешней программы не определена')
        return False

    log.debug(u'Запуск команды <%s> запуска внешней программы' % run_cmd)
    try:
        os.system(run_cmd)
        return True
    except:
        log.fatal(u'Ошибка запуска внешней программы')
    return False
