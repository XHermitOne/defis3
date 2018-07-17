#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Менеджер работы с библиотекой образов.
"""

# Подключение библиотек
# Функции необходимые для получения объектов из серилизованной строки
from wx import ImageFromStream, BitmapFromImage
from wx import EmptyIcon
import cStringIO

from ic.imglib import common

from . import icimg2py


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
        return self._body
    
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
            return BitmapFromImage(img)
        return None

    def getImage(self):
        """
        Объект wx.Image, соответствующий серилизованной картинке.
        """
        body = self.getBody()
        if body: 
            stream = cStringIO.StringIO(body)
            return ImageFromStream(stream)
        return None

    def getIcon(self):
        """
        Объект wx.Icon, соответствующий серилизованной картинке.
        """
        bmp = self.getBitmap()
        if bmp:
            icon = EmptyIcon()
            icon.CopyFromBitmap(bmp)
            return icon
        return None
