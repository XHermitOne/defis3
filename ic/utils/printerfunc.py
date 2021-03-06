#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
Функции работы с принтерами/печатью/и т.п.

Печать производится утилитой lpr.
Например:
lpr -o fit-to-page -P "PrinterName" /.nixprint/print.pdf

Дополнителные опции печати для каждого принтера можно узнать при помощи утилиты lpoptions.
Например:
lpoptions -p <Имя принтера> -l
lpoptions -p WorkCentre-5325 -l

Для работы с CUPS-PDF виртуальным принтером необходим пакет cups-pdf:
sudo apt install cups-pdf
"""

import os
import os.path
import subprocess
import locale
import time

from ic.log import log

from . import filefunc
from . import strfunc

__version__ = (0, 1, 1, 1)

NO_DEFAULT_PRINTER_MSG = 'no system default destination'
PDF_EXT = '.pdf'
GRAPH_FILE_EXT = ('.jpg', '.jpeg', '.tiff', '.tif', '.bmp', '.png', '.gif')
# Параметры ожидания окончания печати принтера
TIMEOUT_BUSY_PRINTER = 5
TIMEOUT_COUNT_BUSY_PRINTER = 20


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


def toPDF(filename):
    """
    Конвертировать файл в PDF если возможно.

    :param filename: Полное имя печатаемого файла.
    :return: Имя PDF файла или None если конвертация не возможна.
    """
    filename_ext = os.path.splitext(filename)[1].lower()
    if filename_ext == PDF_EXT:
        # PDF файлы
        return filename
    elif filename_ext in GRAPH_FILE_EXT:
        # Графические файлы
        pdf_filename = os.path.splitext(filename)[0] + PDF_EXT
        if os.path.exists(pdf_filename):
            os.remove(pdf_filename)
        cmd = 'convert %s %s' % (filename, pdf_filename)
        os.system(cmd)
        return pdf_filename
    log.warning(u'Не поддерживается конвертация файла <%s> в PDF' % filename)
    return None


def printFile(filename, printer_name=None, copies=1):
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
    pdf_filename = toPDF(filename)
    return printPDF(pdf_filename, printer_name, copies)


DEFAULT_CUPS_PDF_DIRNAME = 'PDF'
DEFAULT_CUPS_PDF_DEVICE = 'cups-pdf:'


def printToCupsPDF(filename, printer_name=None, copies=1):
    """
    Печать файла на виртуальный принтер CUPS-PDF.
        Для печати документов с кирилическими именами файлов
        нужно в /etc/cups/cups-pdf.conf выставить
        TitlePref 1 и DecodeHexStrings 1

    :param filename: Полное имя печатаемого файла.
    :param printer_name: Имя принтера для печати.
        По умолчанию CUPS-PDF принтер назвается PDF.
    :param copies: Количество копий.
    :return: Новое имя напетанного PDF файла или None в случае ошибки.
    """
    if printer_name is None:
        printer_name = getCupsPDFPrinterName()
        if printer_name is None:
            log.warning(u'Не установлен CUPS-PDF принтер в системе')
            return None

    log.info(u'Для печати документов с кирилическими именами файлов')
    log.info(u'\tнужно в /etc/cups/cups-pdf.conf выставить')
    log.info(u'\tTitlePref 1 и DecodeHexStrings 1')

    result = printFile(filename=filename, printer_name=printer_name, copies=copies)

    if result:
        pdf_out_path = os.path.join(filefunc.getHomeDir(), DEFAULT_CUPS_PDF_DIRNAME)
        if not os.path.exists(pdf_out_path):
            log.warning(u'Не найден путь <%s> CUPS PDF принтера' % pdf_out_path)
            return None

        new_pdf_filename = os.path.join(pdf_out_path,
                                        os.path.splitext(os.path.basename(filename))[0] + PDF_EXT)

        # Необходимо подождать окончания печати
        if waitBusyPrinter(printer_name) and os.path.exists(new_pdf_filename):
            return new_pdf_filename

        log.warning(u'Результирующий PDF файл печати <%s> не создан' % new_pdf_filename)
    return None


def waitBusyPrinter(printer_name):
    """
    Ожидание окончания печати принтера.

    :param printer_name: Наименование принтера.
    :return: True - принтер свободен после печати.
        False - закончилось время ожидания (сработал таймаут).
    """
    for i_timeout in range(TIMEOUT_COUNT_BUSY_PRINTER):
        log.debug(u'Ожидание печати PDF принтера: %d' % i_timeout)
        if isBusyPrinter(printer_name):
            time.sleep(TIMEOUT_BUSY_PRINTER)
        else:
            break
    return not isBusyPrinter(printer_name)


def isCupsPDF():
    """
    Проверить установлен ли в системе CUPS-PDF принтер?

    :return: True - установлен, False - не установлен.
    """
    printer_devices = getPrinterDevices()
    return any([printer_dev.startswith(DEFAULT_CUPS_PDF_DEVICE) for printer_name, printer_dev in printer_devices])


def getCupsPDFPrinterName():
    """
    Получить имя CUPS-PDF принтера если он установлен.

    :return: Имя CUPS-PDF принтера или None если принтер не установлен.
    """
    printer_devices = getPrinterDevices()
    find_cups_pdf_printer_name = [printer_name for printer_name, printer_dev in printer_devices if printer_dev.startswith(DEFAULT_CUPS_PDF_DEVICE)]
    return find_cups_pdf_printer_name[0] if find_cups_pdf_printer_name else None


def isBusyPrinter(printer_name):
    """
    Проверка занятого принтера.
    Функция работает через утилиту lpstat.

    :param printer_name: Наименование принтера.
    :return: True - принтер занят / False - принтер свободен.
    """
    cmd = ('lpstat', '-p', printer_name)
    lines = _get_exec_cmd_stdout_lines(cmd)

    # Отладка
    # for line in lines:
    #     log.debug(line)

    if not lines:
        return None
    else:
        result = any([strfunc.txt_find_words(printer, u'свободен', 'free') for printer in lines])
        return not result


# Качество печати Ghostscript
GS_QUALITY_DEFAULT = 'default'
GS_QUALITY_PREPRESS = 'prepress'    # Color 300dpi
GS_QUALITY_PRINTER = 'printer'      # 300dpi
GS_QUALITY_EBOOK = 'ebook'          # 150dpi
GS_QUALITY_SCREEN = 'screen'        # 72dpi


def printToGhostscriptPDF(filename, new_pdf_filename=None, quality=GS_QUALITY_DEFAULT):
    """
    Печать файла с помощью Ghostscript в PDF.

    :param filename: Полное имя печатаемого файла.
    :param new_pdf_filename: Имя результирующего PDF файла.
        Если не указывается, то происходит перезапись результирующего файла.
    :param quality: Качество печати.
        GS_QUALITY_PREPRESS = 'prepress'    (Color 300dpi)
        GS_QUALITY_PRINTER = 'printer'      (300dpi)
        GS_QUALITY_EBOOK = 'ebook'          (150dpi)
        GS_QUALITY_SCREEN = 'screen'        (72dpi)
    :return: Новое имя напетанного PDF файла или None в случае ошибки.
    """
    try:
        pdf_filename = toPDF(filename)
        dst_pdf_filename = os.path.join(os.path.dirname(pdf_filename),
                                        '_'+os.path.basename(pdf_filename)) if new_pdf_filename is None else new_pdf_filename

        cmd = ('gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
               '-dPDFSETTINGS=/{}'.format(quality),
               '-dNOPAUSE', '-dQUIET', '-dBATCH',
               '-sOutputFile={}'.format(dst_pdf_filename),
               pdf_filename)
        subprocess.call(cmd)

        if not os.path.exists(dst_pdf_filename):
            log.warning(u'Не сформирован промежуточный файл печати <%s> с помощью Ghostscriopt в PDF' % dst_pdf_filename)
            return None

        if os.path.exists(dst_pdf_filename) and new_pdf_filename is None:
            filefunc.copyFile(dst_pdf_filename, pdf_filename, bRewrite=True)
            filefunc.removeFile(dst_pdf_filename)
            new_pdf_filename = pdf_filename

        if os.path.exists(new_pdf_filename):
            return new_pdf_filename
        log.warning(u'Не сформирован результирующий файл печати <%s> с помощью Ghostscriopt в PDF' % new_pdf_filename)
    except:
        log.fatal(u'Ошибка печати файла <%s> с помощью Ghostscriopt в PDF' % filename)
    return None

