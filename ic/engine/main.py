#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль запуска системы.
main.py  - Запуск системы. 
            Первый параметр - режим работы системы -run/-cfg/-srv.
            Второй параметр - путь к БД.
            Третий параметр - путь к ресурсым файлам.
            Четвертый параметр - Режим использования БД Монопольный-m/Распределенный-s.
            Пятый параметр - имя пользователя, зарегестрированного в системе.
            Шестой параметр - пароль пользователя.

Использование:

    main.py -run ./db/ ./res/ -m Engineer qwerty
    main.py -cfg ./db/
    main.py -srv ./res/
"""

import os
import sys
import copy

from ic.engine import glob_functions
from ic.utils import modefunc

__version__ = (0, 1, 1, 2)


def main(args):
    """
    Тело основной запускаемой процедуры.
    """
    import ic
    args = copy.deepcopy(args)
    
    # Проверка аргументов запуска
    if not args or ('-h' in args):
        print(__doc__)
        return

    # Установка режима отладки
    debug = False
    if '-dbg' in args:
        del args[args.index('-dbg')]
        debug = True
        modefunc.setDebugMode(debug)
        
    if '-cfg' in args:
        del args[args.index('-cfg')]
        
        # Запуск конфигуратора
        modefunc.setRuntimeMode(False)
        modefunc.setConsoleMode(False)

        prj_path = None
        if args:
            prj_path = args[0]
            ic.set_log_prj(prj_path)
            ic.set_ini_file(prj_path)

        try:
            from ic.PropertyEditor import icResTree
            icResTree.editor_main(0, path=prj_path)
        except:
            ic.log.fatal(u'Ошибка запуска редактора', bForcePrint=True)
            return

    elif '-run' in args:
        del args[args.index('-run')]
        
        modefunc.setRuntimeMode(True)
        if args:
            prj_path = args[0]
            ic.set_log_prj(prj_path)
            ic.set_ini_file(prj_path)

        if len(args) > 3:
            glob_functions.icLogin(args[2], args[3], args[1], prj_dirname=prj_path)
        elif len(args) > 2:
            glob_functions.icLogin(args[2], '', args[1], prj_dirname=prj_path)
        elif len(args) > 1:
            glob_functions.icLogin(None, None, args[1], prj_dirname=prj_path)
        else:
            glob_functions.icLogin()

    elif '-cui' in args:
        del args[args.index('-cui')]

        modefunc.setConsoleMode(True)
        if args:
            prj_path = args[0]
            ic.set_log_prj(prj_path)
            ic.set_ini_file(prj_path)

        if len(args) > 3:
            glob_functions.icLogin(args[2], args[3], args[1], prj_dirname=prj_path)
        elif len(args) > 2:
            glob_functions.icLogin(args[2], '', args[1], prj_dirname=prj_path)
        elif len(args) > 1:
            glob_functions.icLogin(None, None, args[1], prj_dirname=prj_path)
        else:
            glob_functions.icLogin()

    elif '-srv' in args:
        # Режим работы СЕРВИСНОГО СЕРВЕРА
        pass
    else:
        ic.log.warning(u'Не определенный режим запуска', bForcePrint=True)


def run():
    """
    Функция запуска. Точка входа.
    """
    main(sys.argv[1:])
