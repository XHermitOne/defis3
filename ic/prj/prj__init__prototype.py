#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Пакет приложения.
"""

from ic.engine import ic_user as ic_user
from ic.utils import ic_mode
import os
from ic.kernel import ic_dot_use

# Версия
__version__ = (0, 0, 0, 2)


def init_env():
    """
    Инициализация окружения.
    """
    pth, fl = os.path.split(__file__)
    pth = pth.replace('\\', '/')
    ln = pth.split('/')[-1]
    ic_mode.setRuntimeMode(False)
    ic_user.icEditorLogin(None, None, '-s', PrjDir_=pth+'/'+ln, DEBUG_MODE=False)


def get_metadata(bInitEnv=False):
    """
    Возвращает объект метоописания системы.
    """
    if bInitEnv:
        init_env()
        
    return ic_dot_use.icMetaDataDotUse()
