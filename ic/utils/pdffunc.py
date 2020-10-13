#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
Функции обработки PDF файлов.
"""

import os
import os.path

from ic.log import log

from . import printerfunc
from . import filefunc

__version__ = (0, 1, 1, 1)


def concatenatePDF(src_pdf_filenames, dst_pdf_filename):
    """
    Конкатинация PDF файлов в один.

    :param src_pdf_filenames: Список файлов-источников.
        Все файлы должны присутствовать!
        Иначе они не будут добавлены в результирующий.
    :param dst_pdf_filename: Полное имя результирующего PDF файла.
    :return: True/False.
    """
    try:
        pdf_filenames_str = ' '.join(['\'%s\'' % pdf_filename for pdf_filename in src_pdf_filenames if os.path.exists(pdf_filename)])

        cmd = 'pdftk %s cat output \'%s\'' % (pdf_filenames_str, dst_pdf_filename)

        log.debug(u'Команда конкатенации в PDF <%s>' % cmd)
        os.system(cmd)

        if os.path.exists(dst_pdf_filename):
            return True
        else:
            log.warning(u'Ошибка формирования PDF файла <%s> при конкатенации' % dst_pdf_filename)
    except:
        log.fatal(u'Ошибка конкатинации PDF файлов')
    return False


DEFAULT_COMPRESSED_FILENAME = 'compress.pdf'


def compressPDF(pdf_filename, new_pdf_filename=None):
    """
    Попытка уменьшить размер PDF файла.
        Сжатие PDF файла производиться через виртуальный принтер CUPS-PDF
        Для сжатия в настройках PDF принтера в /etc/cups/cups-pdf.conf
        параметр -dPDFSETTINGS д.б. установлен как /ebook что соответствует 150dpi
        Другие значения параметра:
        /screen - 72dpi
        /ebook - 150dpi
        /printer - 300dpi
        /prepress - color300dpi

    :param pdf_filename: Сжимаемый PDF файл.
    :param new_pdf_filename: Новый PDF файл.
        Если не указан, то происходит перезапись существующего PDF файла.
    :return: True/False.
    """
    try:
        log.info(u'Сжатие PDF файла <%s> через виртуальный принтер CUPS-PDF' % pdf_filename)
        log.info(u'\tДля сжатия в настройках PDF принтера в /etc/cups/cups-pdf.conf')
        log.info(u'\tпараметр -dPDFSETTINGS д.б. установлен как /ebook что соответствует 150dpi')

        if printerfunc.isCupsPDF():
            dst_pdf_filename = printerfunc.printToCupsPDF(pdf_filename)
            if dst_pdf_filename:
                if new_pdf_filename is None:
                    filefunc.copyFile(dst_pdf_filename, pdf_filename)
                else:
                    filefunc.copyFile(dst_pdf_filename, new_pdf_filename)
                filefunc.removeFile(dst_pdf_filename)
                return True
        else:
            log.warning(u'Не найден установленный CUPS-PDF принтер в системе для сжатия PDF файла <%s>' % pdf_filename)
    except:
        log.fatal(u'Ошибка сжатия PDF файла <%s>' % pdf_filename)
    return False
