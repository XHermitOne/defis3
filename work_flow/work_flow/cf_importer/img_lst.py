#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Список образов, ориентированный на образы компонентов.
"""

import wx

from ic.log import log

__version__ = (0, 0, 0, 2)


class icImgList:
    """
    Список образов, ориентированный на образы комопнентов.
    """
    def __init__(self, parent, img_width, img_height):
        """ 
        Конструктор.
        """
        self._Parent = parent
        # Вызов консктруктора предка
        self._img_lst = wx.ImageList(img_width, img_height)
        # Используемые образы компонентов
        self._ImgIdx = {}
        # Используемые образы компонентов
        self._ImgExtendedIdx = {}
       
    def getImageList(self):
        return self._img_lst

    def setImgIdx(self, id, img, img_ext=None):
        """ 
        Установить компонент для редактирования.
        @param id: Идентификатор объекта асоциированного с образом.
        """
        # Если тип компонента не зарегистрирован, то зарегистрировать его
        if id not in self._ImgIdx:
            # Образ типа компонента
            self._ImgIdx[id] = self.setImg(img)
            if img_ext:
                self._ImgExtendedIdx[id] = self.setImg(img_ext)
            else:
                self._ImgExtendedIdx[id] = -1
        
        return self._ImgIdx[id], self._ImgExtendedIdx[id]

    def getImgIdx(self, id):
        """ 
        Получить данные о компоненте для редактирования.
        @param id: Идентификатор объекта асоциированного с образом.
        """
        if id in self._ImgIdx:
            return self._ImgIdx[id]
        return -1

    def getImgExtendedIdx(self, id):
        """ 
        Получить данные о компоненте для редактирования.
        @param id: Идентификатор объекта асоциированного с образом.
        """
        if id in self._ImgExtendedIdx:
            return self._ImgExtendedIdx[id]
        return -1

    def getImgIdxTuple(self, id):
        """
        Получить сразу два идентификатора в виде кортежа.
        @param id: Идентификатор объекта асоциированного с образом.
        """
        return self.getImgIdx(id), self.getImgExtendedIdx(id)
    
    def setImg(self, img, img_idx=-1):
        """
        Добавить картинку компонента в список образов.
        @param img: Имя файла образа компонента или сам образ.
        @param img_idx: Указание на какое место поместить картинку.
        @return: Возвращает индекс соответствующий этому образу.
        """
        # Заменять картинку в списке не надо
        if img_idx < 0:
            # Добавить в список образ
            if isinstance(img, str):
                # Указание файла
                from . import default_node_img
                return self._img_lst.Add(default_node_img.getbrightnessBitmap())
            elif issubclass(img.__class__, wx.Bitmap):
                # Указание непосредственно картинки
                return self._img_lst.Add(img)
        # Надо заменить картинку на img_idx
        else:
            # Заменить в списке образ
            if isinstance(img, str):
                # Указание файла
                from . import default_node_img
                return self.ReplaceImg(img_idx, default_node_img.getbrightnessBitmap())
            elif issubclass(img.__class__, wx.Bitmap):
                # Указание непосредственно картинки
                return self.ReplaceImg(img_idx, img)
        return -1

    def ReplaceImg(self, img_idx, img):
        """
        Заменить образ в списке образов.
        @param img_idx: Индекс заменяемого образа.
        @param img: Сам wx.Bitmap образ.
        @return: Функция возвращает новый индекс образа.
        """
        try:
            self._img_lst.Replace(img_idx, img)
        except:
            log.fatal(u'%s from %s %s ' % (img_idx, self._img_lst.GetImageCount(), img))
        return img_idx
