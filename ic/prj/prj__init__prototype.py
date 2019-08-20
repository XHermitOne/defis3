#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Пакет приложения.
"""

import os
import os.path

from ic.engine import glob_functions
from ic.utils import ic_mode
from ic.kernel import ic_dot_use

# Версия
__version__ = (0, 1, 1, 1)


def init_env():
    """
    Инициализация окружения.
    """
    pth, fl = os.path.split(__file__)
    pth = pth.replace('\\', '/')
    ln = pth.split('/')[-1]
    ic_mode.setRuntimeMode(False)
    glob_functions.icEditorLogin(None, None, '-s',
                                 PrjDir_=os.path.join(pth, ln), DEBUG_MODE=False)


def get_metadata(bInitEnv=False):
    """
    Возвращает объект метоописания системы.
    """
    if bInitEnv:
        init_env()
        
    return ic_dot_use.icMetaDataDotUse()
