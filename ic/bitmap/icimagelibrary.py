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
from . import ic_bmp

__version__ = (0, 1, 1, 1)


class icImageLibraryPrototype:
    """
    Менеджер работы с библиотекой образов.
    """
    
    def __init__(self, ChildrenImg_=None):
        """
        Крструктор.
        @param ChildrenImg_: Список дочерних объектов образов 
        """
        if ChildrenImg_ is None:
            self._children = []
        else:
            self._children = ChildrenImg_
            
        # Словарь соответствий наименование образа-объект образа
        self._children_dict = {}
        if self._children:
            self._children_dict = dict([(img.getName(), img) for img in self._children])

    def add(self, Image_):
        """
        Добавить образ в библиотеку.
        """
        if Image_ is not None:
            self._children.append(Image_)
            # Сразу прописать в словаре
            self._children_dict[Image_.getName()] = Image_
        return self._children
    
    def getByIdx(self, Idx_):
        """
        Получить объект по индексу.
        """
        return self._children[Idx_]
        
    def getByName(self, ImgName_):
        """
        Получить объект образа по наименованию.
        """
        return self._children_dict.get(ImgName_, None)


class icImageLibManager:
    """
    Класс получения образа по имени файла.
    """

    def __init__(self, Name_=None):
        """
        Крструктор.
        @param Name_: Наименование образа.
        """
        self._img_name = Name_
        self._img_filename = None

    def getImageName(self):
        """
        Наименование образа.
        """
        return self._img_name

    def setImageName(self, Name_):
        """
        Наименование образа. Можно менять.
        """
        self._img_name = Name_

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
            return ic_bmp.createLibraryBitmap(self._img_name)
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
    def __init__(self, Name_, Body_=None):
        """
        Крструктор.
        @param Name_: Наименование образа.
        @param Body_: Серилизованный образ.
        """
        self._name = Name_
        self._body = Body_
        self._img_filename = None
        
    def getName(self):
        """
        Наименование образа.
        """
        return self._name
    
    def setName(self, Name_):
        """
        Наименование образа. Можно менять.
        """
        self._name = Name_
        
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

    def serialize(self, ImgFileName_):
        """
        Серилизовать образ и вернуть его серилизованное значение.
        @param ImgFileName_: Имя файла образа.
        """
        return icimg2py.getImgFileData(ImgFileName_)
    
    def setSerialize(self, ImgFileName_):
        """
        Серилизовать образ и установить в тело.
        @param ImgFileName_: Имя файла образа.
        """
        self._body = self.serialize(ImgFileName_)
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
