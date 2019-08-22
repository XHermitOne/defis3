#!/usr/bin/env python3
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
from ic.utils import filefunc

import ic.imglib.common

__version__ = (0, 1, 1, 2)

DEFAULT_MASK_COLOUR = wx.LIGHT_GREY

# Размер картинок библиотеки по умолчанию
DEFAULT_LIB_BMP_SIZE = (16, 16)

# Буфер картинок
USER_BITMAP_CACHE = {}


# Функции
def getImageLibDir():
    """
    Каталог, где лежат картинки.
    """
    return os.path.abspath(os.path.dirname(ic.imglib.common.__file__))


def getImageFileType(img_filename):
    """
    Определить тип файла образа по его расширению ( .jpg, ... ).
    """
    return getBitmapType(img_filename)


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
    full_img_filename = os.path.normpath(os.path.join(imglib_dir, img_filename))
    if os.path.exists(full_img_filename):
        return createBitmap(full_img_filename, bMask)
    else:
        log.warning(u'Не найден библиотечный файл образа <%s>' % full_img_filename)
    return None


def createBitmap(img_filename, bMask=False):
    """
    Создать объект Bitmap из файла img_filename.
    @param img_filename: Имя файла.
    @param bMask: Флаг создания маски по изображению.
        Фон д.б. DEFAULT_MASK_COLOUR.
    @return: Возвращает созданный объект или None в случае ошибки.
    """
    try:
        # Преобразовать относительные пути в абсолютные
        img_filename = filefunc.get_absolute_path(img_filename)
        if (not img_filename) or (not os.path.exists(img_filename)):
            log.warning(u'Не корректное имя файла образа: <%s>' % img_filename)
            return None
        bmp = wx.Bitmap(img_filename, getImageFileType(img_filename))
        if bMask:
            # Создать маску и присоединить ее к битмапу
            phone_color = DEFAULT_MASK_COLOUR
            bmp.SetMask(wx.Colour(bmp, phone_color))
        return bmp
    except:
        log.fatal(u'Ошибка создания образа файла <%s>' % img_filename)
    return None


def createEmptyBitmap(width, height, background_colour=None):
    """
    Создать пустой битмап.
    @param width: Ширина Bitmap.
    @param height: Высота битмапа.
    @param background_colour: Цвет фона. По умолчанию используется белый.
    @return: Пустой Bitmap заданного размера.
    """
    try:
        if background_colour is None:
            background_colour = wx.WHITE

        # Пустой квадратик
        bmp = wx.Bitmap(width, height)
        # Создать объект контекста устройства
        dc = wx.MemoryDC()
        # Выбрать объект для контекста
        dc.SelectObject(bmp)
        # Изменить фон
        dc.SetBackground(wx.Brush(background_colour))
        dc.Clear()
        # Освободить объект
        dc.SelectObject(wx.NullBitmap)
        return bmp
    except:
        log.fatal(u'Ошибка создания пустого Bitmap. Размер <%s x %s>' % (width, height))
    return None


def createAni(parent, size, freame_delay, *frame_filenames):
    """
    Создание анимированного объекта.
    @param parent: Окно-родитель.
    @param size: Размер.
    @param freame_delay: Задержка м/у кадрами в секундах.
    @param frame_filenames: Файлы-кадры.
    @return: Возвращает созданный объект или None в случае ошибки.
    """
    try:
        frames = [createBitmap(frame_file_name) for frame_file_name in frame_filenames]
        throbber = throb.Throbber(parent, -1, frames, size=size, frameDelay=freame_delay)
        return throbber
    except:
        log.fatal(u'Ошибка создания анимированного объекта.')
    return None


def getSysImg(image_name):
    """
    Получить системный образ по имени.
    """
    if image_name in ic.imglib.common.__dict__:
        return ic.imglib.common.__dict__[image_name]
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


def getBitmapType(filename):
    """
    Определить тип графического файла по его расширению (.jpg, .png и т.п.)
    """
    if filename == '':
        return None

    try:
        name, ext = os.path.splitext(filename)
        ext = ext[1:].upper()
        if ext == 'BMP':
            return wx.BITMAP_TYPE_BMP
        elif ext == 'GIF':
            return wx.BITMAP_TYPE_GIF
        elif ext == 'JPG' or ext == 'JPEG':
            return wx.BITMAP_TYPE_JPEG
        elif ext == 'PCX':
            return wx.BITMAP_TYPE_PCX
        elif ext == 'PNG':
            return wx.BITMAP_TYPE_PNG
        elif ext == 'PNM':
            return wx.BITMAP_TYPE_PNM
        elif ext == 'TIF' or ext == 'TIFF':
            return wx.BITMAP_TYPE_TIF
        elif ext == 'XBM':
            return wx.BITMAP_TYPE_XBM
        elif ext == 'XPM':
            return wx.BITMAP_TYPE_XPM
        elif ext == 'ICO':
            return wx.BITMAP_TYPE_ICO
        return None
    except:
        log.fatal('Ошибка определения типа графического файла')

    return None


def getUserBitmap(img_filename, subsys, dir='images'):
    """
    Функция возвращает объект картинки из пользовательской библиотеки.

    @type subsys: C{string}
    @param subsys: Имя подсистемы в которой ищется картинка.
    @type img_filename: C{string}
    @param img_filename: Имя картинки.
    @rtype: C{wx.Bitmap}
    @return: Объект картинки.
    """
    global USER_BITMAP_CACHE
    key = str(subsys) + os.path.sep + img_filename

    if key in USER_BITMAP_CACHE:
        return USER_BITMAP_CACHE[key]
    else:
        typ = getBitmapType(img_filename)

        if typ:
            import ic.utils.resource as resource
            path = resource.icGetResPath().replace('\\', '/')
            if not subsys:
                path = os.path.join(path, dir, img_filename)
            else:
                path = os.path.join(os.path.sep.join(path.split(os.path.sep)[:-1]), subsys, dir, img_filename)

            img = wx.Image(path, typ)
            bmp = img.ConvertToBitmap()
            USER_BITMAP_CACHE[key] = bmp
            return bmp
