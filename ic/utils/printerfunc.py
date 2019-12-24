#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
Функции работы спринтерами/печатью/и т.п.

Печать производится утилитой lpr.
Например:
lpr -o fit-to-page -P "PrinterName" /.nixprint/print.pdf

Дополнителные опции печати для каждого принтера можно узнать при помощи утилиты lpoptions.
Например:
lpoptions -p <Имя принтера> -l
lpoptions -p WorkCentre-5325 -l
"""

import os
import os.path
import subprocess
import locale

from ic.log import log

__version__ = (0, 1, 1, 1)

NO_DEFAULT_PRINTER_MSG = 'no system default destination'


def _get_exec_cmd_stdout_lines(cmd):
    """
    Выполнить команду ОС и верноть список строк выходного потока.

    :param cmd: Комманда. М.б. в строковом виде или в виде списка.
        Напрмер:
        'lpstat -d' или ('lpstat', '-d')
    :return: Список строк - результат выполнения команды в stdout.
        В случае ошибки возвращается пустой список.
    """
    if isinstance(cmd, str):
        cmd = cmd.split(u' ')
    if not isinstance(cmd, tuple) and not isinstance(cmd, list):
        log.warning(u'Не поддерживаемый тип команды OS <%s>' % str(cmd))
        return list()

    lines = list()
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        b_lines = process.stdout.readlines()
        console_encoding = locale.getpreferredencoding()
        lines = [line.decode(console_encoding).strip() for line in b_lines]
    except:
        log.fatal(u'Ошибка выполнения команды ОС <%s> и получения списка строк из stdout' % cmd)
    return lines


def noDefaultPrinter(sLPStatResult=None):
    """
    Проверка на установленный по умолчанию принтер в системе.

    :param sLPStatResult: Результат команды lpstat -d. Если None,
                то функция сама вызовет команду lpstat -d.
    :return: True-нет принтера по умалчанию, False - есть принтер по умолчанию.
    """
    if sLPStatResult is None:
        cmd = ('lpstat', '-d')
        # sLPStatResult = os.popen3(cmd)[1].readlines()[0]
        lines = _get_exec_cmd_stdout_lines(cmd)
        sLPStatResult = lines[0]

    if sLPStatResult:
        return sLPStatResult.lower().strip() == NO_DEFAULT_PRINTER_MSG
    return False


def getDefaultPrinter():
    """
    Имя принтера по умолчанию.

    :return: Имя принтера по умолчанию или None, если не установлен.
    """
    cmd = ('lpstat', '-d')
    lines = _get_exec_cmd_stdout_lines(cmd)

    if (not lines) or noDefaultPrinter(lines[0]):
        return None
    else:
        result = lines[0].split(': ')[1].strip()
        return result


def getPrinterDevices():
    """
    Получить список устройств принтеров.
    Функция работает через утилиту lpstat.

    :return: Список [(имя принтера, адрес подключения),...].
    """
    cmd = ('lpstat', '-v')
    lines = _get_exec_cmd_stdout_lines(cmd)
    if not lines:
        return None
    else:
        result = [printer.split(' ') for printer in lines]
        result = [(device[2][:-1], device[3]) for device in result]
        return result


def getNetworkPrinters():
    """
    Список имен сетевых принтеров.

    :return: Список строк имен принтеров у которых сетевой адрес.
    """
    printer_devices = getPrinterDevices()
    return [device[0] for device in printer_devices if device[1].startswith('ipp://') or device[1].startswith('socket://')]


def getPrinters():
    """
    Получить список инсталированных принтеров.
    Функция работает через утилиту lpstat.

    :return: Список строк (имен принтеров).
    """
    cmd = ('lpstat', '-a')
    lines = _get_exec_cmd_stdout_lines(cmd)
    if not lines:
        return None
    else:
        result = [printer.split(' ')[0] for printer in lines]
        return result


def getPrintersInfo():
    """
    Получить информацию о принтерах.

    :return: Список кортежей
        [(По умолчанию?, Название принтера, Сетевой принтер?),...].
    """
    printers = getPrinters()
    network_printers = getNetworkPrinters()

    if printers is None:
        return None
    else:
        default_printer = getDefaultPrinter()
        return [(printer == default_printer, printer, printer in network_printers) for printer in printers]


def printPDF(sPDFFileName, sPrinter=None, iCopies=1):
    """
    Отправить на печать PDF файл.

    :type sPDFFileName: C{string}
    :param sPDFFileName: Имя PDF файла для печати.
    :type sPrinter: C{string}
    :param sPrinter: Имя принтера для печати. Если не указан,то
         на печать принтера по умолчанию.
    :param iCopies: Количество копий.
    :return: True - файл отправлен на печать, False - нет.
    """
    if not os.path.exists(sPDFFileName):
        log.warning('PDF file %s not exists' % sPDFFileName)
        return False

    if sPrinter is None:
        sPrinter = getDefaultPrinter()

    if sPrinter:
        cmd = 'lpr -o fit-to-page -P "%s" %s' % (sPrinter, sPDFFileName)
    else:
        # А все равно попробывать
        cmd = 'lpr -o fit-to-page %s' % sPDFFileName

    for i in range(iCopies):
        os.system(cmd)
    return True


def print_file(filename, printer_name=None, copies=1):
    """
    Распечатать файл.
    Файлы распознаются по расширению.
    PDF файлы печатаются функцией printPDF.
    Графические файлы сначала конвертируем в PDF
    а затем печатаем как обычный PDF.

    :param filename: Полное имя печатаемого файла.
    :param printer_name: Имя принтера для печати. Если не указан,то
         на печать принтера по умолчанию.
    :param copies: Количество копий.
    :return: True - файл отправлен на печать, False - нет.
    """
    filename_ext = os.path.splitext(filename)[1].lower()
    if filename_ext == '.pdf':
        # PDF файлы
        return printPDF(filename, printer_name, copies)
    elif filename_ext in ('.jpg', '.jpeg', '.tiff', '.tif', '.bmp', '.png', '.gif'):
        # Графические файлы

        # Сначала конвертируем в PDF а затем печатаем как обычно
        pdf_filename = os.path.splitext(filename)+'.pdf'
        if os.path.exists(pdf_filename):
            os.remove(pdf_filename)
        cmd = 'convert %s %s' % (filename, pdf_filename)
        os.system(cmd)

        return printPDF(pdf_filename, printer_name, copies)
    else:
        log.warning(u'Печать. Не поддерживаемое расширение файла печати <%s>' % filename_ext)
    return False
