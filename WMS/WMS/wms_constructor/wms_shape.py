#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Контрол фигур конструктора WMS объекта.
"""

import os
import os.path
import wx

from ic.bitmap import ic_bmp
from ic.log import log

__version__ = (0, 0, 0, 2)

PACKAGE_DIR = os.path.dirname(__file__)
if PACKAGE_DIR:
    DEFAULT_IMG_DIR = os.path.join(os.path.dirname(os.path.dirname(PACKAGE_DIR)), 'img')
else:
    DEFAULT_IMG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'img')

# Надпись/Наименование ящика по умолчанию
DEFAULT_BOX_LABEL = u'Составной паллет'


class icWMSShape(object):
    """
    Абстрактный класс фигуры, помещаемого в конструктор яруса.
    """

    def __init__(self, bmp=None, pos_x=0, pos_y=0,
                 width=0, height=0, tag=None):
        """
        Конструктор
        @param bmp: Изображение фигуры.
        @param pos_x: Позиция X в конструкторе.
        @param pos_y: Позиция Y в конструкторе.
        @param width: Ширина в конструкторе.
        @param height: Высота в конструкторе.
        @param tag: Дополнительные прикрепляемые данные к фигуре.
        """
        self.bmp = bmp
        # Размер фигуры
        self.size = (width, height)

        self.pos = (pos_x, pos_y)
        self.shown = True
        # Текст-ярлык, прикрепляемый к фигуре
        self.text = None
        self.fullscreen = False

        # Дополнительные прикрепляемы данные к фигуре
        self.tag = tag

    def setBitmap(self, bmp):
        """
        Установить изображение фигуры.
        @param bmp: Объект wx.Bitmap
        """
        self.bmp = bmp
        if self.bmp:
            self.size = self.bmp.GetSize()

    def HitTest(self, point):
        """
        Проверка на попадание точки в фигуру.
        @param point: Проверяемая точка.
        @return: True/False.
        """
        rect = self.GetRect()
        return rect.InsideXY(point.x, point.y)

    def GetRect(self):
        """
        Прямоугольная область фигуры.
        @return: wx.Rect объект, соответствующий фигуре.
        """
        return wx.Rect(self.pos[0], self.pos[1],
                       self.bmp.GetWidth(), self.bmp.GetHeight())

    def Draw(self, dc, op=wx.COPY):
        """
        Метод отрисовки.
        @param dc: Контекст отрисовки.
        @param op: Параметры отрисовки.
        """
        if self.bmp.Ok():
            memDC = wx.MemoryDC()
            memDC.SelectObject(self.bmp)

            dc.Blit(self.pos[0], self.pos[1],
                    self.bmp.GetWidth(), self.bmp.GetHeight(),
                    memDC, 0, 0, op, True)

            return True
        else:
            return False

    def getTag(self):
        """
        Прикрепленные данные к фигуре
        """
        return self.tag

    def getTagInfo(self):
        """
        Дополнительные данные о фигуре в текстовом виде.
        @return: Заполненный текст данными
        """
        return u'Бла-Бла-Бла\nБла-Бла-Бла\nБла-Бла-Бла\n'


class icWMSCellShape(icWMSShape):
    """
    Фигура, располагаемая по ячейкам конструктора.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор
        """
        icWMSShape.__init__(self, *args, **kwargs)

        # Ячейка, в которой находиться фигура
        self.cell = None

    def setCell(self, cell):
        """
        Установка фигуры на ячейку.
        ВНИМАНИЕ! Установка на занятую ячейку не возможна.
        @param cell: Объект ячейки.
        @return: True/False
        """
        if cell is None:
            # Если ячейка не определена
            log.warning(u'Ячейка не определена')
            return False
        elif cell and cell == self.cell:
            # Это таже самая ячейка
            log.warning(u'Это таже самая ячейка')
            return False
        elif cell and cell.shape is not None:
            # Если ячейка занята
            # поменять фигуры местами
            dst_shape = cell.shape
            src_cell = self.cell

            self.cell = cell
            self.cell.shape = self
            self.pos = self.cell.getPoint()
            self.size = self.cell.getSize()

            dst_shape.cell = src_cell
            src_cell.shape = dst_shape
            dst_shape.pos = src_cell.getPoint()
            dst_shape.size = src_cell.getSize()
        else:
            if self.cell:
                # Освободить предыдущую ячейку
                self.cell.shape = None
                self.cell = None

            self.cell = cell
            cell.shape = self
            self.pos = cell.getPoint()
            self.size = cell.getSize()
        return True


class icWMSBoxShape(icWMSCellShape):
    """
    Фигура ящика - паллета, помещаемого в ячейку.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор
        """
        icWMSCellShape.__init__(self, *args, **kwargs)

        if self.bmp is None:
            bmp_filename = os.path.join(DEFAULT_IMG_DIR, 'box.png')
            self.setBitmap(ic_bmp.createBitmap(bmp_filename))

    def getTagInfo(self):
        """
        Дополнительные данные о фигуре в текстовом виде.
        @return: Заполненный текст данными
        """
        if self.tag:
            if self.tag['nomenklature']['label'] is not None:
                # Обычный паллет
                txt = u'%s\n%s\n%s\t%s' % (self.tag['nomenklature']['label'],
                                           self.tag['row']['label'],
                                           self.tag['made_date']['label'],
                                           self.tag['made_date']['value'])
            else:
                # Составной паллет
                content = self.tag.get('content', dict())
                content_label = content.get('label', DEFAULT_BOX_LABEL)
                content_txt = u''
                if content:
                    content_txt = u'\n\t'.join(content.get('value', list()))
                txt = u'%s\n%s\n%s\n%s\t%s' % (content_label,
                                               content_txt,
                                               self.tag['row']['label'],
                                               self.tag['made_date']['label'],
                                               self.tag['made_date']['value'])

            return txt
        return u'Нет данных'
