#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Функции логирования с использованием консоли.
"""

import os
import time
import wx

from . import log

DEFAULT_LOG_FILENAME = log.CONFIG.LOG_FILENAME if log.CONFIG else './log.txt'
DEFAULT_LOG_DATETIME_FMT = '%Y.%m.%d %H:%M:%S'


__version__ = (0, 0, 0, 2)


def log_to_file(txt, filename=DEFAULT_LOG_FILENAME, datetime_fmt=DEFAULT_LOG_DATETIME_FMT):
    """
    Записать лог в текстовый файл.
    @param txt: Текст сообщения.
    @param filename: Имя текстового файла лога.
    @param datetime_fmt: Формат вывода даты-времени в сообщении лога.
    """
    f = None
    try:
        f = open(filename, 'a')
        now_time = time.strftime(datetime_fmt, time.localtime(time.time()))
        now_time += ':\n'
        f.write(now_time)

        if isinstance(txt, unicode):
            import sys
            txt = txt.encode(sys.getfilesystemencoding())

        f.write(txt)
        f.write('\n')
        f.close()
    except:
        if f:
            f.close()
            f = None
        raise


def log_cmd(cmd, txt_ctrl=None):
    """
    Запуск комманды ОС с логированием.
    @param cmd: Текст комманды.
    @param txt_ctrl: Объект wxTextCtrl для логирования.
        Если указывается, то вывод лога производим в wxTextControl,
        иначе вывод будет производиться в текстовый файл.
    """
    if isinstance(cmd, unicode):
        import sys
        cmd = cmd.encode(sys.getfilesystemencoding())
    result = os.popen3(cmd)
    if txt_ctrl:
        log_to_ctrl(txt_ctrl, result)
    else:
        log_to_file(cmd2Txt(result))


def cmd2Txt(cmd):
    """
    Конвертация результата выполнения команды popen в текст.
    """
    result = ''
    if cmd:
        if not isinstance(cmd, tuple):
            # Обработка результат popen
            txt = cmd.readline().strip()
            while txt:
                result += txt + '\n'
                txt = cmd.readline().strip()
        elif isinstance(cmd, tuple) and len(cmd) == 3:
            # Обработка результат popen3
            out = cmd[1].readline()
            err = cmd[2].readline()

            while out or err:
                if out:
                    result += out + '\n'
                if err:
                    start = len(result)
                    result += err + '\n'

                out = cmd[1].readline()
                err = cmd[2].readline()
    return result


def log_to_ctrl(txt_ctrl, cmd=None):
    """
    Вывод результата выполнения комманды в объект wxTextCtrl.
    @param txt_ctrl: Объект wxTextCtrl для логирования.
    @param cmd: Текст комманды.
    """
    if cmd:
        if not isinstance(cmd, tuple):
            # Обработка результат popen
            txt = cmd.readline().strip()
            while txt:
                txt_ctrl.AppendText(txt)
                txt = cmd.readline().strip()
        elif isinstance(cmd, tuple) and len(cmd) == 3:
            # Обработка результат popen3
            out = cmd[1].readline()
            err = cmd[2].readline()

            while out or err:
                if out:
                    txt_ctrl.AppendText(out)
                if err:
                    start = len(txt_ctrl.GetValue())
                    txt_ctrl.AppendText(err)
                    # Закрасить в красный цвет ошибки
                    end = len(txt_ctrl.GetValue())
                    txt_ctrl.SetStyle(start, end, wx.TextAttr('RED', wx.NullColour))

                out = cmd[1].readline()
                err = cmd[2].readline()
