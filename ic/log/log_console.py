#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Функции логирования с использованием консоли.
"""

# import os
import subprocess
import time
import wx

from . import log

DEFAULT_LOG_FILENAME = log.CONFIG.LOG_FILENAME if log.CONFIG else './log.txt'
DEFAULT_LOG_DATETIME_FMT = '%Y.%m.%d %H:%M:%S'


__version__ = (0, 1, 1, 1)


def log_to_file(txt, filename=DEFAULT_LOG_FILENAME, datetime_fmt=DEFAULT_LOG_DATETIME_FMT):
    """
    Записать лог в текстовый файл.

    :param txt: Текст сообщения.
    :param filename: Имя текстового файла лога.
    :param datetime_fmt: Формат вывода даты-времени в сообщении лога.
    """
    f = None
    try:
        f = open(filename, 'at')
        now_time = time.strftime(datetime_fmt, time.localtime(time.time()))
        now_time += ':\n'
        f.write(now_time)

        # if isinstance(txt, str):
        #    import sys
        #    txt = txt.encode(sys.getfilesystemencoding())

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
    Запуск команды ОС с логированием.

    :param cmd: Текст команды.
    :param txt_ctrl: Объект wxTextCtrl для логирования.
        Если указывается, то вывод лога производим в wxTextControl,
        иначе вывод будет производиться в текстовый файл.
    """
    try:
        # result = os.popen3(cmd)
        log.info(u'Запуск команды <%s>' % cmd)
        cmd_list = [elem.strip('"') for elem in cmd.split(u' ')]
        result = subprocess.Popen(cmd_list)
        if txt_ctrl:
            log_to_ctrl(txt_ctrl, result.stdout)
        else:
            log_to_file(cmd2Txt(result.stdout))
    except:
        log.fatal(u'Ошибка в функции <log_cmd>')


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
    Вывод результата выполнения команды в объект wxTextCtrl.

    :param txt_ctrl: Объект wxTextCtrl для логирования.
    :param cmd: Текст команды.
    """
    if txt_ctrl is None:
        log.warning(u'Не определен объект для логирования')

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
