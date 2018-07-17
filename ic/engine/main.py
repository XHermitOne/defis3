#!/usr/bin/env python
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

from ic.engine import ic_user
from ic.utils import ic_mode

__version__ = (0, 0, 1, 2)


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
        ic_mode.setDebugMode(debug)
        
    if '-cfg' in args:
        del args[args.index('-cfg')]
        
        # Запуск конфигуратора
        ic_mode.setRuntimeMode(False)

        prj_path = None
        if args:
            prj_path = args[0]
            ic.set_log_prj(prj_path)
            ic.set_ini_file(prj_path)

        try:
            from ic.PropertyEditor import icResTree
            icResTree.editor_main(0, path=prj_path)
        except:
            print(__doc__)
            return

    elif '-run' in args:
        del args[args.index('-run')]
        
        ic_mode.setRuntimeMode(True)
        if args:
            prj_path = args[0]
            ic.set_log_prj(prj_path)
            ic.set_ini_file(prj_path)

        if len(args) > 3:
            ic_user.icLogin(args[2], args[3], args[1], PrjDir_=prj_path)
        elif len(args) > 2:
            ic_user.icLogin(args[2], '', args[1], PrjDir_=prj_path)
        elif len(args) > 1:
            ic_user.icLogin(None, None, args[1], PrjDir_=prj_path)
        else:
            ic_user.icLogin()
    elif '-srv' in args:
        # Режим работы СЕРВИСНОГО СЕРВЕРА
        pass
    else:
        print(__doc__)


def run():
    """
    Функция запуска. Точка входа.
    """
    main(sys.argv[1:])
