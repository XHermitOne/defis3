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

from ic.utils import modefunc        # Режимы работы
from ic.utils import coderror       # Коды ошибок
from ic.dlg import dlgfunc           # Диалоговые функции
from ic.bitmap import bmpfunc        # Функции работы с образами
from ic.utils import datetimefunc        # Функции работы с датой/временем
from ic.utils import inifunc
from ic.log import log
from ic.utils import util

from ic.engine.glob_functions import *
from ic.engine.form_manager import *
from ic.utils.extfunc import *
from ic.utils.filefunc import *

from ic.report import REPORT_MANAGER

# ic series version number
# (note that subpackages have their own version number)
__version__ = (0, 1, 1, 1)

# Copyright notice string
__copyright__ = u'Copyright (c) 2002, Kolchanov Alexander xhermitone@gmail.com'

# Файл настроек
INI_FILE = None

# Загрузчик ресурсов
RESOURCE_LOADER = None


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
    global INI_FILE
    prj_path = os.path.normpath(prj_path)
    INI_FILE = os.path.join(prj_path, '%s.ini' % prj_path.split('/')[-2])
    log.info('SET INI FILE VARIABLE INI_FILE=%s' % INI_FILE)


def load_ini_param(section, par):
    if INI_FILE and os.path.isfile(INI_FILE):
        return inifunc.loadParamINI(INI_FILE, section, par)
    else:
        log.info('(!) INI File [%s] not found' % INI_FILE)


def get_loader():
    global RESOURCE_LOADER
    if not RESOURCE_LOADER:
        RESOURCE_LOADER = getVar('LOADER')
    return RESOURCE_LOADER


def Login(user, passw, path, runtime_mode=False):
    """
    Вход в систему.
    1. Исключение LoginErrorException возбуждается если пользователь с таким именем
    уже вошел в систему.
    2. LoginInvalidException возбуждается если неверен логин либо пароль.
    :param user: Имя пользователя.
    :param passw: Пароль пользователя.
    :param path: Путь до папки проекта (c:/defis/tutorial/tutorial/)."""
    modefunc.setRuntimeMode(runtime_mode)
    set_ini_file(path)
    if not runtime_mode:
        result = icEditorLogin(user, passw, '-s', PrjDir_=path, DEBUG_MODE=False)
    else:
        result = icLogin(user, passw, '-s', PrjDir_=path, DEBUG_MODE=False)
    return result


def Logout():
    return icLogout()
