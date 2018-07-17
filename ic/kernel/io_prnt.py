#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль функций ввода-вывода
"""

# Подключение библиотек
import os
import traceback
import sys
import ic.config
from ic.log import log


def SetUserLog(user, kernel=None, filemode='a'):
    """
    Установка пользовательского лога.
    """
    if not kernel:
        path = 'C:/DEFISWRK/'
    else:
        path = kernel.GetContext()['LOG_DIR']

    if not os.path.isdir(path):
        os.makedirs(path)

    user_name = user
    if not isinstance(user_name, unicode):
        user_name = unicode(str(user), 'utf-8')

    fn = path + user_name+'.log'

    log.init(ic.config, fn)


def ReCodeString(String_, StringCP_, NewCP_):
    """
    Перекодировать из одной кодировки в другую.
    @param String_: Строка.
    @param StringCP_: Кодовая страница строки.
    @param NewCP_: Новая кодовая страница строки.
    """
    if NewCP_.upper() == 'UNICODE':
        # Кодировка в юникоде.
        if isinstance(String_, str):
            return unicode(String_, StringCP_)
        else:
            return String_

    if NewCP_.upper() == 'OCT' or NewCP_.upper() == 'HEX':
        # Закодировать строку в восьмеричном/шестнадцатеричном виде.
        return OctHexString(String_, NewCP_)

    if isinstance(String_, str):
        string = unicode(String_, StringCP_)
    elif isinstance(String_, unicode):
        string = String_
    try:
        return string.encode(NewCP_)
    except:
        log.error('Decode string error: <%s> -> <%s>.' % (StringCP_, NewCP_))
        return string


def OctHexString(String_, Code_):
    """
    Закодировать строку в восьмеричном/шестнадцатеричном виде.
    Символы с кодом < 128 не кодируются.
    @param String_:
    @param Code_: Кодировка 'OCT'-восьмеричное представление.
                            'HEX'-шестнадцатеричное представление.
    @return: Возвращает закодированную строку.
    """
    try:
        if Code_.upper() == 'OCT':
            fmt = '\\%o'
        elif Code_.upper() == 'HEX':
            fmt = '\\x%x'
        else:
            # Ошибка аргументов
            outLog(u'Функция OctHexString: Ошибка аргументов.')
            return None
        # Перебор строки по символам
        ret_str = ''
        for char in String_:
            code_char = ord(char)
            # Символы с кодом < 128 не кодируются.
            if code_char > 128:
                ret_str += fmt % code_char
            else:
                ret_str += char
        return ret_str
    except:
        outErr()
        return None

# Устройства вывода
IC_CONSOLE = 0x0001
IC_CONSOLE_INFO = 0x0002
IC_CONSOLE_ERR = 0x0004
IC_CONSOLE_WARN = 0x0008
IC_CONSOLE_DBG = 0x0010
IC_FILE = 0x0020
IC_LOG = 0x0040
IC_LOG_CONSOLE = 0x0080
IC_MSG_INFO = 0x0100
IC_MSG_ERR = 0x0200

# Файла лога по умолчанию
IC_LOG_FILE_DEFAULT = './log_file.txt'

# Кодовые страницы текста и устройства по умолчанию
IC_TXT_CODEPAGE = 'utf-8'


def getConsoleEncoding():
    if sys.platform[:3].lower() == 'win':
        return 'CP866'
    else:
        return 'utf-8'

IC_CONSOLE_CODEPAGE = getConsoleEncoding()


def outDevice(msg, Device_=IC_CONSOLE):
    """
    Вывод на устройство регистрации специальных сообщений.
    @type msg: C{string}
    @param msg: Сообщение об ошибке.
    @type Device_: C{int}
    @param Device_: Указание устройства вывода.
    """
    if Device_ & IC_CONSOLE:
        try:
            print(msg)
        except:
            return False

    if Device_ & IC_CONSOLE_INFO:
        try:
            log.info(msg)
        except:
            return False

    if Device_ & IC_CONSOLE_ERR:
        try:
            log.error(msg)
        except:
            return False

    if Device_ & IC_CONSOLE_WARN:
        try:
            log.warning(msg)
        except:
            return False

    if Device_ & IC_CONSOLE_DBG:
        try:
            log.debug(msg)
        except:
            return False

    if Device_ & IC_FILE:
        try:
            log_file = None
            log_file = open(IC_LOG_FILE_DEFAULT, 'w+')
            log_file.write(msg)
            log_file.close()
        except:
            if log_file:
                log_file.close()
            return False
    if Device_ & IC_MSG_INFO:
        import ic.dlg
        ic.dlg.ic_dlg.icMsgBox(u'ВНИМАНИЕ', msg)
    if Device_ & IC_MSG_ERR:
        import ic.dlg
        ic.dlg.ic_dlg.icErrBox(u'ОШИБКА', msg)
    return True


def outLog(msg, TxtCP_=IC_TXT_CODEPAGE, DevCP_=IC_CONSOLE_CODEPAGE, Device_=IC_CONSOLE_INFO):
    """
    Выдает сообщение в регистратор (на консоль).
    @param msg: Текст сообщения.
    @param TxtCP_: Кодовая страница текста сообщения.
    @param DevCP_: Кодовая страница вывода на устройство.
    @param Device_: Указание устройства вывода.
    """
    txt = ReCodeString(msg, TxtCP_, DevCP_)
    if Device_ == IC_LOG:
        log.info(txt)
        return True
    elif Device_ == IC_LOG_CONSOLE:
        log.info(txt)
        Device_ = IC_CONSOLE

    return outDevice(txt, Device_)


def outWarning(msg, TxtCP_=IC_TXT_CODEPAGE, DevCP_=IC_CONSOLE_CODEPAGE, Device_=IC_CONSOLE_WARN):
    """
    Выдает сообщение в регистратор (на консоль).
    @param msg: Текст сообщения.
    @param TxtCP_: Кодовая страница текста сообщения.
    @param DevCP_: Кодовая страница вывода на устройство.
    @param Device_: Указание устройства вывода.
    """
    return outLog(msg, TxtCP_, DevCP_, Device_)


def outErr(msg=u'', TxtCP_=IC_TXT_CODEPAGE, DevCP_=IC_CONSOLE_CODEPAGE, Device_=IC_CONSOLE_ERR):
    """
    Выдает сообщение о последней ошибке в регистратор (эту функцию можно
    использовать только в блоке exception).
    @param msg: Текст сообщения.
    @param TxtCP_: Кодовая страница текста сообщения.
    @param DevCP_: Кодовая страница вывода на устройство.
    @param Device_: Указание устройства вывода.
    """
    txt = u''
    if msg:
        txt = ReCodeString(msg, TxtCP_, DevCP_)

    if Device_ == IC_LOG:
        log.error(txt)
        return True
    elif Device_ == IC_LOG_CONSOLE:
        log.error(txt)
        Device_ = IC_CONSOLE

    return outLastErr(txt, Device_)


def outLastErr(msg, Device_=IC_CONSOLE_ERR):
    """
    Записывает сообщение о последней ошибке в устройство вывода.
    @type msg: C{string}
    @param msg: Заголовок сообщения об ошибке.
    @type Device_: C{int}
    @param Device_: Указание устройства вывода.
    """
    outDevice(msg, Device_)
    trace_txt = traceback.format_exc()
    outDevice(trace_txt, Device_)
    return trace_txt


def _to_unicode(String_, DefaultCP_='utf-8'):
    """
    Подбор кодировки для превращения строки в юникод.
    """
    if isinstance(String_, unicode):
        return String_
    elif isinstance(String_, str):
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

