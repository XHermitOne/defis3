#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер работы с библиотекой образов.
"""

# Подключение библиотек
# Функции необходимые для получения объектов из серилизованной строки

import os
import os.path
import wx
import io

from ic.imglib import common
from ic.log import log

from . import icimg2py
from . import bmpfunc

__version__ = (0, 1, 1, 1)


class icImageLibraryPrototype:
    """
    Менеджер работы с библиотекой образов.
    """
    
    def __init__(self, children_images=None):
        """
        Крструктор.
        @param children_images: Список дочерних объектов образов 
        """
        if children_images is None:
            self._children = []
        else:
            self._children = children_images
            
        # Словарь соответствий наименование образа-объект образа
        self._children_dict = {}
        if self._children:
            self._children_dict = dict([(img.getName(), img) for img in self._children])

    def add(self, image):
        """
        Добавить образ в библиотеку.
        """
        if image is not None:
            self._children.append(image)
            # Сразу прописать в словаре
            self._children_dict[image.getName()] = image
        return self._children
    
    def getByIdx(self, idx):
        """
        Получить объект по индексу.
        """
        return self._children[idx]
        
    def getByName(self, image_name):
        """
        Получить объект образа по наименованию.
        """
        return self._children_dict.get(image_name, None)


class icImageLibManager:
    """
    Класс получения образа по имени файла.
    """

    def __init__(self, image_name=None):
        """
        Крструктор.
        @param image_name: Наименование образа.
        """
        self._img_name = image_name
        self._img_filename = None

    def getImageName(self):
        """
        Наименование образа.
        """
        return self._img_name

    def setImageName(self, image_name):
        """
        Наименование образа. Можно менять.
        """
        self._img_name = image_name

    def getFileName(self):
        """
        Имя файла образа.
        """
        return self._img_filename

    def getBaseFileName(self, img_filename=None):
        """
        Базовое имя файла образа.
        Используется как имя образа из папки ic/imglib/common.
        @param img_filename: Полное имя файла образа.
        """
        if img_filename is None:
            img_filename = self._img_filename
        return os.path.basename(img_filename) if img_filename else None

    def setFileName(self, img_filename=None):
        """
        Установить имя файла образа.
        @param img_filename: Полное имя файла образа.
        """
        if img_filename and os.path.exists(img_filename):
            self._img_filename = img_filename
            # ВНИМАНИЕ! Имя образа это его базовое наименование файла
            self._img_name = self.getBaseFileName()
        elif img_filename is None:
            self._img_filename = None
            self._img_name = None
        else:
            log.warning(u'Файл образа <%s> не найден' % img_filename)
            self._img_name = self.getBaseFileName(img_filename)

    def getBitmap(self):
        """
        Объект wx.Bitmap, соответствующий картинке.
        """
        if self._img_name:
            return bmpfunc.createLibraryBitmap(self._img_name)
        return None

    def getImage(self):
        """
        Объект wx.Image, соответствующий картинке.
        """
        bmp = self.getBitmap()
        if bmp:
            return bmp.ConvertToImage()
        return None

    def getIcon(self):
        """
        Объект wx.Icon, соответствующий картинке.
        """
        bmp = self.getBitmap()
        if bmp:
            icon = wx.Icon()
            icon.CopyFromBitmap(bmp)
            return icon
        return None


class icSerializedImagePrototype:
    """
    Класс образа как серилизованного ресурса.
    """
    def __init__(self, image_name, image_body=None):
        """
        Крструктор.
        @param image_name: Наименование образа.
        @param image_body: Серилизованный образ.
        """
        self._name = image_name
        self._body = image_body
        self._img_filename = None
        
    def getName(self):
        """
        Наименование образа.
        """
        return self._name
    
    def setName(self, image_name):
        """
        Наименование образа. Можно менять.
        """
        self._name = image_name
        
    def getBody(self):
        """
        Получить серилизованное представление образа.
        """
        img_filename = self.getFileName()
        if self._body is None and img_filename:
            # Если определено имя файла образа, но не инициализировать
            # серилизванное представление
            self._body = icimg2py.getImgFileData(img_filename)
        return self._body

    def getFileName(self):
        """
        Имя файла образа.
        """
        return self._img_filename

    def getBaseFileName(self):
        """
        Базовое имя файла образа.
        Используется как имя образа из папки ic/imglib/common.
        """
        return os.path.basename(self._img_filename) if self._img_filename else None

    def setFileName(self, img_filename=None):
        """
        Установить имя файла образа.
        @param img_filename: Полное имя файла образа.
        """
        if img_filename and os.path.exists(img_filename):
            self._img_filename = img_filename
        elif img_filename is None:
            self._img_filename = None
        else:
            log.warning(u'Файл образа <%s> не найден' % img_filename)

    def serialize(self, img_filename):
        """
        Серилизовать образ и вернуть его серилизованное значение.
        @param img_filename: Имя файла образа.
        """
        return icimg2py.getImgFileData(img_filename)
    
    def setSerialize(self, img_filename):
        """
        Серилизовать образ и установить в тело.
        @param img_filename: Имя файла образа.
        """
        self._body = self.serialize(img_filename)
        return self._body
    
    def getBitmap(self):
        """
        Объект wx.Bitmap, соответствующий серилизованной картинке.
        """
        img = self.getImage()
        if img:
            return wx.Bitmap(img)
        return None

    def getImage(self):
        """
        Объект wx.Image, соответствующий серилизованной картинке.
        """
        body = self.getBody()
        if body: 
            stream = io.BytesIO(body)
            return wx.Image(stream)
        return None

    def getIcon(self):
        """
        Объект wx.Icon, соответствующий серилизованной картинке.
        """
        bmp = self.getBitmap()
        if bmp:
            icon = wx.Icon()
            icon.CopyFromBitmap(bmp)
            return icon
        return None
