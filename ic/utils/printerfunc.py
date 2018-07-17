#!/usr/bin/env python
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
from ic.log import log

NO_DEFAULT_PRINTER_MSG = 'no system default destination'


def noDefaultPrinter(sLPStatResult=None):
    """
    Проверка на установленный по умолчанию принтер в системе.
    @param sLPStatResult: Результат комманды lpstat -d. Если None,
                то функция сама вызовет команду lpstat -d.
    @return: True-нет принтера по умалчанию, False - есть принтер по умолчанию.
    """
    if sLPStatResult is None:
        cmd = 'lpstat -d'
        sLPStatResult = os.popen3(cmd)[1].readlines()[0]
    if sLPStatResult:
        return sLPStatResult.lower().strip() == NO_DEFAULT_PRINTER_MSG
    return False


def getDefaultPrinter():
    """
    Имя принтера по умолчанию.
    @return: Имя принтера по умолчанию или None, если не установлен.
    """
    cmd = 'lpstat -d'
    result = os.popen3(cmd)[1].readlines()
    if (not result) or noDefaultPrinter(result[0]):
        return None
    else:
        result = result[0].split(': ')[1].strip()
        return result


def getPrinterDevices():
    """
    Получить список устройств принтеров.
    Функция работает через утилиту lpstat.
    @return: Список [(имя принтера, адрес подключения),...].
    """
    cmd = 'lpstat -v'
    result = os.popen3(cmd)[1].readlines()
    if not result:
        return None
    else:
        result = [printer.split(' ') for printer in result]
        result = [(device[2][:-1], device[3]) for device in result]
        return result


def getNetworkPrinters():
    """
    Список имен сетевых принтеров.
    @return: Список строк имен принтеров у которых сетевой адрес.
    """
    printer_devices = getPrinterDevices()
    return [device[0] for device in printer_devices if device[1].startswith('ipp://') or device[1].startswith('socket://')]


def getPrinters():
    """
    Получить список инсталированных принтеров.
    Функция работает через утилиту lpstat.
    @return: Список строк (имен принтеров).
    """
    cmd = 'lpstat -a'
    result = os.popen3(cmd)[1].readlines()
    if not result:
        return None
    else:
        result = [printer.split(' ')[0] for printer in result]
        return result


def getPrintersInfo():
    """
    Получить информацию о принтерах.
    @return: Список кортежей
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
    @type sPDFFileName: C{string}
    @param sPDFFileName: Имя PDF файла для печати.
    @type sPrinter: C{string}
    @param sPrinter: Имя принтера для печати. Если не указан,то
         на печать принтера по умолчанию.
    @param iCopies: Количество копий.
    @return: True - файл отправлен на печать, False - нет.
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
    @param filename: Полное имя печатаемого файла.
    @param printer_name: Имя принтера для печати. Если не указан,то
         на печать принтера по умолчанию.
    @param copies: Количество копий.
    @return: True - файл отправлен на печать, False - нет.
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
