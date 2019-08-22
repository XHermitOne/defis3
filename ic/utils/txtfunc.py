#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Функции работы с текстовыми файлами.
"""

# --- Imports ---
import os
import os.path

from .extfunc import save_file_text
from .extfunc import load_file_text

# Эти функции добавлены для возможности
# импортировать их из этого модуля
# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
from .extfunc import load_file_unicode
from .extfunc import recode_text_file
from .extfunc import text_file_append
from .extfunc import text_file_find
from .extfunc import text_file_replace
from .extfunc import text_file_subdelete
from .extfunc import text_file_subreplace
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

from . import extfunc
from . import ic_str
from ic.log import log

__version__ = (0, 1, 1, 1)

DEFAULT_ENCODING = 'utf-8'


def createTxtFile(filename, txt=None):
    """
    Создать текстовый файл.
    @param filename: Имя создаваемого файла.
    @param txt: Текст по умолчанию записываемый в файл.
    @return: True/False.
    """
    txt = util.encodeText(txt)
    f = None
    try:
        if os.path.exists(filename):
            os.remove(filename)
        f = open(filename, 'w')
        if txt:
            f.write(txt)
        f.close()
        return True
    except:
        if f:
            f.close()
            f = None
        raise
    return False


def save_file_csv(csv_filename, records=(),
                  delim=u',', encoding=DEFAULT_ENCODING):
    """
    Запись в CSV файл списка записей.
    @param csv_filename: Имя CSV файла.
    @param records: Список записей.
        Каждая запись представляет собой список значений полей.
    @param delim: Разделитель.
    @param encoding: Кодировка результирующего файла.
    @return: True/False
    """
    txt = u'\n'.join([delim.join([ic_str.toUnicode(field, encoding) for field in record]) for record in records])
    return save_file_text(csv_filename, txt)


def load_file_csv(csv_filename, delim=u',',
                  encoding=DEFAULT_ENCODING, to_unicode=True):
    """
    Чтение csv файла в виде списка записей.
    @param csv_filename; Имя CSV файла.
    @param delim: Разделитель.
    @param encoding: Кодовая страница файла
        (для преобразования в Unicode).
    @paran to_unicode: Преобразовать сразу в Unicode?
    @return: Список записей.
        Каждая запись представляет собой список значений полей.
        Либо None в слечае ошибки.
    """
    if not os.path.exists(csv_filename):
        log.warning(u'Файл <%s> не найден' % csv_filename)
        return None

    txt = load_file_text(csv_filename,
                         code_page=encoding, to_unicode=to_unicode)
    if txt:
        txt = txt.strip()

        try:
            records = list()
            txt_lines = txt.split(u'\n')
            for txt_line in txt_lines:
                record = [extfunc.wise_type_translate_str(field) for field in txt_line.split(delim)]
                records.append(record)
            return records
        except:
            log.fatal(u'Ошибка конвертации содержимого CSV файла <%s> в список записей' % csv_filename)
    return None
