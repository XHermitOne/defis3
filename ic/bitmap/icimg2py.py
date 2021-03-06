#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Функции серилизации изображений/картинок.
"""

# --- Подключение библиотек ---
import os
import zlib
import io
import wx
import tempfile                 # Работа со временными файлами
from wx.tools import img2img    # Функции серилизации образов wx
from wx.tools import img2py     # Функции серилизации образов wx

from . import bmpfunc
from ic.log import log

__version__ = (0, 1, 1, 2)


# --- Определение функций ---
def getImgFileData(img_filename):
    """
    Получить данные файла образа.

    :param img_filename: Имя файла образа.
    :return: Данные образа или None  в случае ошибки.
    """
    try:
        # Определить тип образа и расширение файла
        img_file_type = bmpfunc.getImageFileType(img_filename)
        img_file_ext = os.path.splitext(img_filename)[1]
        # Конвертировать файл образа во временный файл
        tmp_file_name = tempfile.mktemp()
        log.info(u'Серилизация файла образа [%s : %s : %s]' % (img_filename, img_file_ext, img_file_type))
        ok, msg = img2img.convert(img_filename, None,
                                  None, tmp_file_name, img_file_type, img_file_ext)
        # Все нормально?
        if not ok:
            log.info(msg)
            return None
        # Получить данные из временного файла
        tmp_file = open(tmp_file_name, 'rb').read()
        data = crunchImgData(tmp_file)
        os.unlink(tmp_file_name)
        return data
    except:
        log.error(u'Ошибка серилизации файла образа <%s> в строку.' % img_filename)
        return None


def crunchImgData(img_data):
    """
    Нормализовать данные для записи в файл *.py.

    :param img_data: Данные образа.
    """
    try:
        return img2py.crunch_data(img_data, 0)
    except:
        return create_crunch_data(img_data, 0)


def create_crunch_data(data, compressed):
    """
    Функция создает строку по данным файла образа.
    Эта функция взята из старой версии wxPython.
    В новой версии ее зачем-то удалили.
    """
    # compress it?
    if compressed:
        data = zlib.compress(data, 9)

    # convert to a printable format, so it can be in a Python source file
    data = repr(data)

    # This next bit is borrowed from PIL.  It is used to wrap the text intelligently.
    fp = io.BytesIO()
    data += ' '  # buffer for the +1 test
    c = i = 0
    word = ''
    octdigits = '01234567'
    hexdigits = '0123456789abcdef'
    while i < len(data):
        if data[i] != '\\':
            word = data[i]
            i += 1
        else:
            if data[i+1] in octdigits:
                for n in range(2, 5):
                    if data[i+n] not in octdigits:
                        break
                word = data[i:i+n]
                i += n
            elif data[i+1] == 'x':
                for n in range(2, 5):
                    if data[i+n] not in hexdigits:
                        break
                word = data[i:i+n]
                i += n
            else:
                word = data[i:i+2]
                i += 2

        l = len(word)
        if c + l >= 78-1:
            fp.write('\\\n')
            c = 0
        fp.write(word)
        c += l

    # return the formatted compressed data
    return fp.getvalue()


def getImageFromData(img_data):
    """
    Создание wx.Image из строки серилизованной картинки.

    :param img_data: Данные строки серилизованной картинки.
    """
    stream = io.BytesIO(img_data)
    return wx.Image(stream)


def getBitmapFromData(img_data):
    """
    Создание wx.Bitmap из строки серилизованной картинки.

    :param img_data: Данные строки серилизованной картинки.
    """
    image = getImageFromData(img_data)
    return wx.Bitmap(image)


def getIconFromData(img_data):
    """
    Создание wx.Icon из строки серилизованной картинки.

    :param img_data: Данные строки серилизованной картинки.
    """
    icon = wx.Icon()
    icon.CopyFromBitmap(getBitmapFromData(img_data))
    return icon
