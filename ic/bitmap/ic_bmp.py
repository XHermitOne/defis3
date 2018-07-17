#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль управления файлами образов *.BMP, *.GIF, *.JPG и т.п.
"""

# Подключение библиотек
import os
import os.path
import wx
import wx.lib.throbber as throb

from ic.log import log
from . import icbitmap
from ic.utils import ic_file

import ic.imglib.common

__version__ = (0, 0, 2, 1)

DEFAULT_MASK_COLOUR = wx.LIGHT_GREY

# Размер картинок библиотеки по умолчанию
DEFAULT_LIB_BMP_SIZE = (16, 16)


# Функции
def getImageLibDir():
    """
    Каталог, где лежат картинки.
    """
    return os.path.abspath(os.path.dirname(ic.imglib.common.__file__))


def getImageFileType(ImgFileName_):
    """
    Определить тип файла образа по его расширению ( .jpg, ... ).
    """
    return icbitmap.icBitmapType(ImgFileName_)


def createLibraryBitmap(img_filename, bMask=False):
    """
    Создать объект Bitmap из файла img_filename.
    К имени файла добавляется путь библиотеки образов ic.imglib.common.
    @param img_filename: Краткое имя файла.
    @param bMask: Флаг создания маски по изображению.
        Фон д.б. DEFAULT_MASK_COLOUR.
    @return: Возвращает созданный объект или None в случае ошибки.
    """
    imglib_dir = getImageLibDir()
    full_img_filename = os.path.normpath(imglib_dir+'/'+img_filename)
    if os.path.exists(full_img_filename):
        return createBitmap(full_img_filename, bMask)
    return None


def createBitmap(ImgFileName_, MakeMask_=False):
    """
    Создать объект Bitmap из файла ImgFileName_.
    @param ImgFileName_: Имя файла.
    @param MakeMask_: Флаг создания маски по изображению.
        Фон д.б. DEFAULT_MASK_COLOUR.
    @return: Возвращает созданный объект или None в случае ошибки.
    """
    try:
        # Преобразовать относительные пути в абсолютные
        ImgFileName_ = ic_file.AbsolutePath(ImgFileName_)
        if (not ImgFileName_) or (not os.path.exists(ImgFileName_)):
            log.warning(u'Некорректное имя файла образа: <%s>' % ImgFileName_)
            return None
        bmp = wx.Bitmap(ImgFileName_, getImageFileType(ImgFileName_))
        if MakeMask_:
            # Создать маску и присоединить ее к битмапу
            phone_color = DEFAULT_MASK_COLOUR
            bmp.SetMask(wx.MaskColour(bmp, phone_color))
        return bmp
    except:
        log.fatal(u'Ошибка создания образа файла <%s>' % ImgFileName_)
        return None


def createEmptyBitmap(Width_, Height_, PhoneColor_):
    """
    Создать пустой битмап.
    @param Width_,Height_: Размер битмапа.
    @param PhoneColor_: Цвет фона.
    """
    try:
        # Пустой квадратик
        bmp = wx.EmptyBitmap(Width_, Height_)
        # Создать объект контекста устройства
        dc = wx.MemoryDC()
        # Выбрать объект для контекста
        dc.SelectObject(bmp)
        # Изменить фон
        dc.SetBackground(wx.Brush(PhoneColor_))
        dc.Clear()
        # Освободить объект
        dc.SelectObject(wx.NullBitmap)
        return bmp
    except:
        log.fatal()
        return None


def createAni(Parent_, Size_, Delay_, *FrameFileNames_):
    """
    Создание анимированного объекта.
    @param Parent_: Окно-родитель.
    @param Size_: Размер.
    @param Delay_: Задержка м/у кадрами в секундах.
    @param FrameFileNames_: Файлы-кадры.
    @return: Возвращает созданный объект или None в случае ошибки.
    """
    try:
        frames = [createBitmap(frame_file_name) for frame_file_name in FrameFileNames_]
        throbber = throb.Throbber(Parent_, -1, frames, size=Size_, frameDelay=Delay_)
        return throbber
    except:
        log.fatal(u'Ошибка создания анимированного объекта.')
        return None


def getSysImg(ImgName_):
    """
    Получить системный образ по имени.
    """
    if ImgName_ in ic.imglib.common.__dict__:
        return ic.imglib.common.__dict__[ImgName_]
    return None


def findBitmap(*img_filenames):
    """
    Поиск и создание объекта Bitmap по списку имен файлов картинок.
    @param img_filenames: Имена файлов, которые необходимо просмотреть.
    @return: Возвращает созданный объект Bitmap или
        None в случае если ни один из предложенных файлов не существует.
    """
    for img_filename in img_filenames:
        if os.path.exists(img_filename):
            return createBitmap(img_filename)
    return None
