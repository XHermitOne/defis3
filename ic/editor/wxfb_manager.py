#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер управления дизайнером форм wxFormBuilder.
"""

import os
import os.path

from ic.interfaces import icdesignerinterface
from ic.log import log
from ic.utils import filefunc
from ic import config

__version__ = (0, 1, 1, 1)

STARTSWITH_SIGNATURE = '..)'
ENDSWITH_SIGNATURE = '(..'
CONTAIN_SIGNATURE = '(..)'

# Замены для адаптации модуля
ADAPTATION_REPLACES = (dict(compare=STARTSWITH_SIGNATURE, src='import wx.combo', dst='# import wx.combo'),
                       dict(compare=STARTSWITH_SIGNATURE, src='import wx.xrc', dst='import wx.adv'),
                       dict(compare=CONTAIN_SIGNATURE, src='wx.combo.', dst='wx.adv.'),
                       # Calendar
                       dict(compare=STARTSWITH_SIGNATURE, src='import wx.calendar', dst='# import wx.calendar'),
                       dict(compare=CONTAIN_SIGNATURE, src='wx.calendar.', dst='wx.adv.'),
                       # DatePickerCtrl
                       dict(compare=CONTAIN_SIGNATURE, src='wx.DatePickerCtrl', dst='wx.adv.DatePickerCtrl'),
                       dict(compare=CONTAIN_SIGNATURE, src='wx.DP_DEFAULT', dst='wx.adv.DP_DEFAULT'),
                       dict(compare=CONTAIN_SIGNATURE, src='wx.EVT_DATE_CHANGED', dst='wx.adv.EVT_DATE_CHANGED'),
                       # Bitmap
                       dict(compare=CONTAIN_SIGNATURE, src='.Ok()', dst='.IsOk()'),
                       # Sizers
                       dict(compare=CONTAIN_SIGNATURE, src='.AddSpacer( ( 0, 0), 1, wx.EXPAND,', dst='.AddSpacer('),
                       dict(compare=CONTAIN_SIGNATURE, src='.SetSizeHintsSz', dst='.SetSizeHints'),
                       # ToolBar
                       dict(compare=CONTAIN_SIGNATURE, src='.AddLabelTool(', dst='.AddTool('),
                       # Wizard
                       dict(compare=CONTAIN_SIGNATURE, src='wx.wizard', dst='wx.adv'),
                       )


def get_wxformbuilder_executable():
    """
    Путь до основной запускаемой программы wxFormBuilder.
    """
    if os.path.exists('/bin/wxformbuilder') or os.path.exists('/usr/bin/wxformbuilder'):
        return 'wxformbuilder'
    else:
        alter_wxfb_path = filefunc.normal_path(config.ALTER_WXFORMBUILDER)
        if os.path.exists(alter_wxfb_path):
            return alter_wxfb_path
        else:
            log.warning(u'Альтернативный путь запуска wxFormBuilder <%s> не найден' % alter_wxfb_path)
    return None


def run_wxformbuilder(filename=None, do_generate=False, language=None):
    """
    Запуск wxFormBuilder.
        Для более подроного описания параметров запуска wxFormBuilder, запустите:
        wxformbuilder --help
    @param filename: Файл открываемый в wxFormBuilder.
        Если не указан, то ничего не открывается.
    @param do_generate: Произвести генерацию результирующего ресурса/модуля проекта.
    @param language: Явное указание языка для генерации.
    @return: True/False
    """
    cmd = ''
    cmd_args = filename
    if cmd_args:
        cmd_args += '--generate' if do_generate else ''
        cmd_args += ('--language=%s' % language) if language else ''

    wxformbuilder_exec = get_wxformbuilder_executable()
    if wxformbuilder_exec:
        cmd = '%s %s&' % (wxformbuilder_exec, cmd_args) if cmd_args else '%s &' % wxformbuilder_exec

    if cmd:
        try:
            log.info(u'Выполнение комманды ОС <%s>' % cmd)
            os.system(cmd)
        except:
            log.fatal(u'Ошибка выполнения комманды ОС <%s>' % cmd)


class icWXFormBuilderManager(icdesignerinterface.icExtFormDesignerInterface):
    """
    Менеджер управления дизайнером форм wxFormBuilder.
    """

    def open_project(self, prj_filename):
        """
        Открыть файл проекта.
        @param prj_filename: Полное имя файла проекта.
        @return: True/False
        """
        try:
            run_wxformbuilder(prj_filename)
            return True
        except:
            log.fatal(u'Ошибка открытия файла проекта wxFormBuilder <%s>' % prj_filename)
        return False

    def create_project(self, default_prj_filename=None):
        """
        Создание нового файла проекта.
        @param default_prj_filename: Имя файла проекта по умолчанию.
        @return: True/False.
        """
        try:
            run_wxformbuilder(default_prj_filename)
            return True
        except:
            log.fatal(u'Ошибка создания файла проекта wxFormBuilder <%s>' % default_prj_filename)
        return False

    def generate(self, prj_filename, *args, **kwargs):
        """
        Дополнительная генерация проекта.
        @param prj_filename: Полное имя файла проекта.
        @return: True/False.
        """
        try:
            run_wxformbuilder(prj_filename, do_generate=True, *args, **kwargs)
            return True
        except:
            log.fatal(u'Ошибка генерации файла проекта wxFormBuilder <%s>' % prj_filename)
        return False

    def adaptation_form_py(self, py_filename):
        """
        Адаптация сгенерированного модуля Python для использования в программе
        с текущей версией wxPython.
        Движок DEFIS ориентирован и отлажен только с конкретной версией wxPython.
        Поэтому адаптация производится к этой конкретной версии wxPython.
        @param py_filename: Полное имя сгенерированного модуля формы средствами wxFormBuilder.
        @return: True - адаптация прошла без ошибок / False - ошибка адаптации модуля.
        """
        if not os.path.exists(py_filename):
            log.warning(u'Файл <%s> не найден' % py_filename)
            return False

        # Чтение линий модуля
        lines = list()
        file_obj = None
        try:
            file_obj = open(py_filename, 'rt')
            lines = file_obj.readlines()
            file_obj.close()
        except:
            log.fatal(u'Ошибка чтения файла модуля <%s> для адаптации' % py_filename)
            if file_obj:
                file_obj.close()
            return False

        # Произвести замены во всех линиях модуля
        for i, line in enumerate(lines):
            new_line = line
            for replacement in ADAPTATION_REPLACES:
                signature = replacement.get('compare', None)
                if signature == STARTSWITH_SIGNATURE and new_line.startswith(replacement['src']):
                    new_line = new_line.replace(replacement['src'], replacement['dst'])
                elif signature == ENDSWITH_SIGNATURE and new_line.endswith(replacement['src']):
                    new_line = new_line.replace(replacement['src'], replacement['dst'])
                elif signature == CONTAIN_SIGNATURE and replacement['src'] in new_line:
                    new_line = new_line.replace(replacement['src'], replacement['dst'])
                # else:
                #    log.warning(u'Не распознанная сигнатура <%s> автозамены адаптации модуля' % str(signature))
            lines[i] = new_line

        # Запись линий в результирующий модуль
        file_obj = None
        try:
            file_obj = open(py_filename, 'wt')
            file_obj.writelines(lines)
            file_obj.close()
            return True
        except:
            log.fatal(u'Ошибка записи файла модуля <%s> для адаптации' % py_filename)
            if file_obj:
                file_obj.close()
        return False


def adapt_wxformbuilder_py(py_filename):
    """
    Адаптация сгенерированного модуля Python для использования в программе
    с текущей версией wxPython.
    Движок DEFIS ориентирован и отлажен только с конкретной версией wxPython.
    Поэтому адаптация производится к этой конкретной версии wxPython.
    @param py_filename: Полное имя сгенерированного модуля формы средствами wxFormBuilder.
    @return: True - адаптация прошла без ошибок / False - ошибка адаптации модуля.
    """
    manager = icWXFormBuilderManager()
    result = manager.adaptation_form_py(py_filename)
    if result:
        log.info(u'Адаптация Python модуля wxFormBuilder <%s> прошла успешно' % py_filename)
    else:
        log.warning(u'Адаптация Python модуля wxFormBuilder <%s> закончилась неудачно' % py_filename)
    return result
