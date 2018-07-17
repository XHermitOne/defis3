#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Функции серилизации изображений/картинок.
"""

# --- Подключение библиотек ---
import zlib
import cStringIO

from wx import ImageFromStream, BitmapFromImage
from wx import EmptyIcon

import tempfile                 # Работа со временными файлами
from wx.tools import img2img    # Функции серилизации образов wx
from wx.tools import img2py     # Функции серилизации образов wx

from . import ic_bmp
from ic.utils import ic_file
from ic.kernel import io_prnt


# --- Определение функций ---
def getImgFileData(ImgFileName_):
    """
    Получить данные файла образа.
    @param ImgFileName_: Имя файла образа.
    @return: Данные образа или None  в случае ошибки.
    """
    try:
        # Определить тип образа и расширение файла
        img_file_type = ic_bmp.getImageFileType(ImgFileName_)
        img_file_ext = ic_file.SplitExt(ImgFileName_)[1]
        # Конвертировать файл образа во временный файл
        tmp_file_name = tempfile.mktemp()
        io_prnt.outLog(u'Серилизация файла образа [%s : %s : %s]' % (ImgFileName_, img_file_ext, img_file_type))
        ok, msg = img2img.convert(ImgFileName_, None,
                                  None, tmp_file_name, img_file_type, img_file_ext)
        # Все нормально?
        if not ok:
            io_prnt.outLog(msg)
            return None
        # Получить данные из временного файла
        tmp_file = open(tmp_file_name, 'rb').read()
        data = crunchImgData(tmp_file)
        ic_file.UnLink(tmp_file_name)
        return data
    except:
        io_prnt.outErr(u'Ошибка серилизации файла образа <%s> в строку.' % ImgFileName_)
        return None


def crunchImgData(ImgData_):
    """
    Нормализовать данные для записи в файл *.py.
    @param ImgData_: Данные образа.
    """
    try:
        return img2py.crunch_data(ImgData_, 0)
    except:
        return ic_crunch_data(ImgData_, 0)


def ic_crunch_data(data, compressed):
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
    fp = cStringIO.StringIO()
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
                for n in xrange(2, 5):
                    if data[i+n] not in octdigits:
                        break
                word = data[i:i+n]
                i += n
            elif data[i+1] == 'x':
                for n in xrange(2, 5):
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


def imageFromData(ImageData_):
    """
    Создание wx.Image из строки серилизованной картинки.
    @param ImageData_: Данные строки серилизованной картинки.
    """
    stream = cStringIO.StringIO(ImageData_)
    return ImageFromStream(stream)


def bitmapFromData(ImageData_):
    """
    Создание wx.Bitmap из строки серилизованной картинки.
    @param ImageData_: Данные строки серилизованной картинки.
    """
    image = imageFromData(ImageData_)
    return BitmapFromImage(image)


def iconFromData(ImageData_):
    """
    Создание wx.Icon из строки серилизованной картинки.
    @param ImageData_: Данные строки серилизованной картинки.
    """
    icon = EmptyIcon()
    icon.CopyFromBitmap(bitmapFromData(ImageData_))
    return icon
