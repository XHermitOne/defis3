#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Создание и ведение лога системы.
"""

import traceback
import sys
from ic.dlg.msgbox import MsgBox
from . import log

IC_CONSOLE_LOGTYPE = 0
IC_FILE_LOGTYPE = 1
IC_WIN_LOGTYPE = 2
IC_MSGBOX_LOGTYPE = 3


#   Выдает сообщение о последней ошибке
def MsgLastError(parent, beg_msg):
    """
    Выводит сообщение о последней ошибке в диалоговое окно.

    @type parent: C{wxWindow}
    @param parent: Родительское окно.
    @type beg_msg: C{string}
    @param beg_msg: Заголовок сообщения об ошибке.
    """
    trace = traceback.extract_tb(sys.exc_traceback)
    last = len(trace) - 1

    if last >= 0:
        msg = genTxtLastError(beg_msg)
        MsgBox(parent, msg)

    return msg


def genTxtLastError(beg_msg, msg_encoding='utf-8'):
    """
    Сгенерировать текстовое сообщение ошибки.
    """
    err_txt = traceback.format_exc()
    msg = _to_unicode(beg_msg + '\n' + err_txt, msg_encoding)
    return msg


def genTxtLastError_depricate(beg_msg, msg_encoding='utf-8'):
    """
    Сгенерировать текстовое сообщение ошибки.
    """
    trace = traceback.extract_tb(sys.exc_traceback)
    ltype = sys.exc_type
    last = len(trace) - 1
    msg = u''

    if last >= 0:
        lt = trace[last]
        if not isinstance(beg_msg, unicode):
            beg_msg = unicode(beg_msg, msg_encoding)
        file_info = lt[0]
        func_info = lt[2]
        txt_info = lt[3]
        if not isinstance(txt_info, unicode):
            txt_info = unicode(str(txt_info), msg_encoding)
            
        sys_info = sys.exc_info()
        if hasattr(sys_info[1], 'strerror'):
            sys_info_msg = _to_unicode(sys_info[1].strerror, msg_encoding)
        else:
            sys_info_msg = _to_unicode(sys_info[1].message, msg_encoding)
        
        msg = beg_msg + u''' in file: %s, func: %s, line: %i, 
        text: 
            %s
        type:%s
        comments:%s''' % (file_info, func_info,
                          lt[1], txt_info, ltype, sys_info_msg)
    return msg


def _to_unicode(String_, DefaultCP_='utf-8'):
    """
    Подбор кодировки для превращения строки в юникод.
    """
    if isinstance(String_, unicode):
        return String_
    elif not isinstance(String_, str):
        String_ = str(String_)

    u_str = u''
    try:
        u_str = unicode(String_, DefaultCP_)
    except:
        if sys.platform[:3].lower() == 'win':
            # Windows
            u_str = unicode(String_, 'cp1251')
        else:
            # Linux
            u_str = unicode(String_, 'koi8-r')
    return u_str


def LogLastError(beg_msg, logType = 0, msg_encoding='utf-8'):
    """
    Записывает сообщение о последней ошибке в лог.
    @type beg_msg: C{string}
    @param beg_msg: Заголовок сообщения об ошибке.
    @type logType: C{int}
    @param logType: Тип лога (0 - консоль, 1 - файл, 2 - окно лога, 3 - окно сообщений)
    """
    trace = traceback.extract_tb(sys.exc_traceback)
    last = len(trace) - 1

    if last >= 0:
        msg = genTxtLastError(beg_msg, msg_encoding)
        toLog(msg, logType)

    return msg


def toLog(msg, logType = 0):
    """
    Вывод на устройство регистрации специальных сообщений.
    @type msg: C{string}
    @param msg: Сообщение об ошибке.
    @type logType: C{int}
    @param logType: Тип лога (0 - консоль, 1 - файл, 2 - окно лога, 3 - окно сообщений)
    """

    if logType == IC_FILE_LOGTYPE:
        pass
    elif logType == IC_WIN_LOGTYPE:
        pass
    elif logType == IC_MSGBOX_LOGTYPE:
        MsgBox(None, msg)
    else:
        try:
            log.debug(msg)
        except:
            pass
