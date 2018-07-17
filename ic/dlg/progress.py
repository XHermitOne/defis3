#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль диалоговых функций пользователя для работы с прогресс барами.
"""

# --- Подключение пакетов ---
try:
    from ic.engine import ic_user
except ImportError:
    print('ic_user IMPORT ERROR')

__version__ = (0, 0, 1, 2)


# --- ДИАЛОГОВЫЕ ФУНКЦИИ ----
def icOpenProgressBar(Label_='', Min_=0, Max_=100):
    """
    Открыть прогресс бар статусной строки.
    @param Label_: Надпись статусной строки.
    @param Min_: Минимальное значение.
    @param Max_: Максимальное занчение.
    """
    main_win = ic_user.icGetMainWin()
    if main_win:
        return main_win.status_bar.openProgressBar(Label_, Min_, Max_)


def icCloseProgressBar(Label_=''):
    """
    Закрыть прогресс бар.
    @param Label_: Надпись статусной строки.
    """
    main_win = ic_user.icGetMainWin()
    if main_win:
        return main_win.status_bar.closeProgressBar(Label_)


def icUpdateProgressBar(Label_='', Value_=-1):
    """
    Обновить прогресс бар.
    @param Label_: Надпись статусной строки.
    @param Value_: Значение.
    """
    main_win = ic_user.icGetMainWin()
    if main_win:
        return main_win.status_bar.updateProgressBar(Label_, Value_)
