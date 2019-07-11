#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер управления дизайнером форм wxCrafter.
"""

import os
import os.path

from ic.interfaces import icdesignerinterface
from ic.log import log
from ic.utils import filefunc
from ic import config

__version__ = (0, 1, 1, 1)


def get_wxcrafter_executable():
    """
    Путь до основной запускаемой программы wxCrafter.
    """
    if os.path.exists('/bin/wxcrafter') or os.path.exists('/usr/bin/wxcrafter'):
        return 'wxcrafter'
    else:
        alter_wxcrafter = config.get_cfg_var('ALTER_WXCRAFTER')
        if alter_wxcrafter:
            alter_wxcrafter_path = filefunc.normal_path(alter_wxcrafter)
            if os.path.exists(alter_wxcrafter_path):
                return alter_wxcrafter_path
            else:
                log.warning(u'Альтернативный путь запуска wxCrafter <%s> не найден' % alter_wxcrafter_path)
    return None


def run_wxcrafter(filename=None):
    """
    Запуск wxCrafter.
        Для более подробного описания параметров запуска wxCrafter, запустите:
        wxcrafter --help
    @param filename: Файл проекта открываемый в wxCrafter.
        Если не указан, то ничего не открывается.
    @return: True/False
    """
    cmd = ''
    cmd_args = filename

    wxcrafter_exec = get_wxcrafter_executable()
    if wxcrafter_exec:
        cmd = '%s %s&' % (wxcrafter_exec, cmd_args) if cmd_args else '%s &' % wxcrafter_exec

    if cmd:
        try:
            log.info(u'Выполнение комманды ОС <%s>' % cmd)
            os.system(cmd)
        except:
            log.fatal(u'Ошибка выполнения комманды ОС <%s>' % cmd)


class icWXCrafterManager(icdesignerinterface.icExtFormDesignerInterface):
    """
    Менеджер управления дизайнером форм wxCrafter.
    """

    def open_project(self, prj_filename):
        """
        Открыть файл проекта.
        @param prj_filename: Полное имя файла проекта.
        @return: True/False
        """
        try:
            run_wxcrafter(prj_filename)
            return True
        except:
            log.fatal(u'Ошибка открытия файла проекта wxCrafter <%s>' % prj_filename)
        return False

    def create_project(self, default_prj_filename=None):
        """
        Создание нового файла проекта.
        @param default_prj_filename: Имя файла проекта по умолчанию.
        @return: True/False.
        """
        try:
            run_wxcrafter(default_prj_filename)
            return True
        except:
            log.fatal(u'Ошибка создания файла проекта wxCrafter <%s>' % default_prj_filename)
        return False

    def generate(self, prj_filename, *args, **kwargs):
        """
        Дополнительная генерация проекта.
        @param prj_filename: Полное имя файла проекта.
        @return: True/False.
        """
        try:
            run_wxcrafter(prj_filename)
            return True
        except:
            log.fatal(u'Ошибка генерации файла проекта wxCrafter <%s>' % prj_filename)
        return False
