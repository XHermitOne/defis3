#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
Стандартные пакеты
log - пакте для работы с файлами лога.
dlg - пакет для работы со стандартными окнами сообщений и диалогами.
bitmap - работа с bitmap.
"""


import os.path

# Импортируем исключения ядра
import ic.utils.impfunc
from ic.kernel.icexceptions import *
# from ic.kernel import io_prnt

from ic.utils import ic_mode        # Режимы работы
from ic.utils import coderror       # Коды ошибок
from ic.dlg import ic_dlg           # Диалоговые функции
from ic.bitmap import bmpfunc        # Функции работы с образами
from ic.utils import ic_time        # Функции работы с датой/временем
from ic.utils import ini
from ic.log import log
from ic.utils import util

from ic.engine.ic_user import *
from ic.engine.form_manager import *
from ic.utils.ic_extend import *
from ic.utils.ic_file import *

from ic.report import REPORT_MANAGER

# ic series version number
# (note that subpackages have their own version number)
__version__ = (0, 1, 1, 1)

# Copyright notice string
__copyright__ = u'Copyright (c) 2002, Kolchanov Alexander xhermitone@gmail.com'

ini_file = None
# Загрузчик ресурсов
resource_loader = None


def set_log_prj(prj_path):
    """
    Устанавливает систему журнилирования проекта.
    """
    prj_path = os.path.normpath(prj_path)
    cfg_filename = os.path.join(prj_path, 'config.py')
    if os.path.exists(cfg_filename):
        cfg_module = ic.utils.impfunc.loadSource('cfg_module', cfg_filename)
        log.init(cfg_module)
    else:
        from . import config
        log.init(config)


def set_ini_file(prj_path):
    """
    Устанавливает имя ini файла проекта.
    """
    global ini_file
    prj_path = os.path.normpath(prj_path)
    ini_file = os.path.join(prj_path, '%s.ini' % prj_path.split('/')[-2])
    log.info('SET INI FILE VARIABLE ini_file=%s' % ini_file)


def load_ini_param(section, par):
    if ini_file and os.path.isfile(ini_file):
        return ini.loadParamINI(ini_file, section, par)
    else:
        log.info('(!) INI File [%s] not found' % ini_file)


def get_loader():
    global resource_loader
    if not resource_loader:
        resource_loader = icGet('LOADER')
    return resource_loader


def Login(user, passw, path, runtime_mode=False):
    """
    Вход в систему.
    1. Исключение LoginErrorException возбуждается если пользователь с таким именем
    уже вошел в систему.
    2. LoginInvalidException возбуждается если неверен логин либо пароль.
    @param user: Имя пользователя.
    @param passw: Пароль пользователя.
    @param path: Путь до папки проекта (c:/defis/tutorial/tutorial/)."""
    ic_mode.setRuntimeMode(runtime_mode)
    set_ini_file(path)
    if not runtime_mode:
        result = icEditorLogin(user, passw, '-s', PrjDir_=path, DEBUG_MODE=False)
    else:
        result = icLogin(user, passw, '-s', PrjDir_=path, DEBUG_MODE=False)
    return result


def Logout():
    return icLogout()
