#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс мнемосхемы.

Мнемосхема представляет собой панель с размещенными на ней
контролами-индикаторами и контролами-манипуляторами
параметров абстрактного технологического процесса.
В качестве фона мнемосхема использует SVG файл схемы.
В качестве контролов используются обычные контролы ввода-вывода.
Для позиционирования контролов на мнемосхеме используются компоненты-якоря,
которые определяют положение и размер контролов ввода вывода относительно
элементов SVG фона мнемосхемы.

ВНИМАНИЕ! Сама мнемосхема центруется на форме.
"""

import wx
import os
import os.path

from ic.log import log
from ..scada_proto import scada_form_manager
from ic.utils import filefunc
from ic.bitmap import bmpfunc

from ic.components import icwxpanel

# Version
__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_MNEMOSCHEME = {'engines': list(),
                      'scan_class': None,
                      'auto_run': False,
                      'svg_background': None,
                      'svg_width': 0.0,
                      'svg_height': 0.0,

                      '__parent__': icwxpanel.SPC_IC_PANEL,

                      '__attr_hlp__': {'engines': u'Список движков SCADA системы',
                                       'scan_class': u'Класс сканирования',
                                       'auto_run': u'Признак автозапуска и автоостанова всех движков при создании/закрытии окна',
                                       'svg_background': u'SVG файл фона мнемосхемы',
                                       'svg_width': u'Ширина SVG в исходных единицах измерения',
                                       'svg_height': u'Высота SVG в исходных единицах измерения',
                                       },
                      }

# Формат комманды запуска конвертации SVG -> PNG
SVG2PNG_CONVERT_CMD_FMT = 'convert -background none -resize %dx%d -extent %dx%d -gravity center %s %s'


class icMnemoSchemeProto(scada_form_manager.icSCADAFormManager):
    """
    Мнемосхема.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        scada_form_manager.icSCADAFormManager.__init__(self)

        # Полное имя файла фона мнемосхемы
        self._svg_background = None
        # Объект картинки для отображения фона
        self._background_bitmap = None

        # Размер SVG в исходных единицах измерения
        self._svg_size = (0.0, 0.0)

    def setSVGSize(self, svg_width, svg_height):
        """
        Установить размер SVG в исходных единицах измерения.

        :param svg_width: Ширина SVG в исходных единицах измерения
        :param svg_height: Высота SVG в исходных единицах измерения
        """
        self._svg_size = (svg_width, svg_height)

    def getSVGSize(self):
        """
        Размер SVG в исходных единицах измерения
        """
        return self._svg_size

    def setSVGBackground(self, svg_filename, bAutoDraw=True):
        """
        Установить фон мнемосхемы.

        :param svg_filename: Полное имя SVG файла фона мнемосхемы.
        :param bAutoDraw: Автоматически отрисовать на контексте мнемосхемы?
        :return: True - фон успешно установлен.
        """
        if not svg_filename:
            log.warning(u'Не определен SVG файл фона мнемосхемы')
            return False

        if not os.path.exists(svg_filename):
            log.warning(u'Не найден SVG файл фона мнемосхемы <%s>' % svg_filename)
            return False

        self._svg_background = svg_filename
        if bAutoDraw:
            self.drawBackground()

        return True

    def getAnchors(self):
        """
        Список якорей мнемосхемы.
        """
        log.warning(u'Не определен метод получения списка якорей мнемосхемы')
        return list()

    def getControls(self):
        """
        Список активных контролов мнемосхемы.
        """
        log.warning(u'Не определен метод получения списка контролов мнемосхемы')
        return list()

    def setControlPositions(self):
        """
        Метод расстановки и образмеривания контролов мнемосхемы согласно якорям.

        :return: True/False.
        """
        log.warning(u'Не определен метод расстановки и образмеривания контролов мнемосхемы')
        return False

    def drawBackground(self, bAutoRewrite=False):
        """
        Отрисовать фон мнемосхемы на контексте устройства.
        ВНИМАНИЕ! Для извлечения изображения из SVG файла
        используется внешняя утилита конвертации SVG -> PNG.
        А PNG уже отображается на контексте устройства.

        :param bAutoRewrite: Автоматически перезаписать промежуточный PNG файл.
        :return: True/False.
        """
        try:
            # Размер панели мнемосхемы
            width, height = self.GetSize()

            png_filename = os.path.join(filefunc.getPrjProfilePath(),
                                        '%s_background_%dx%d.png' % (self.getName(), width, height))
            svg_filename = os.path.join(filefunc.getPrjProfilePath(),
                                        os.path.basename(self._svg_background))
            # Сохранить SVG файл в HOME папке
            # Это сделано для того чтобы можно было на лету подменять мнемосхему
            if not os.path.exists(svg_filename) or not filefunc.is_same_file_length(svg_filename, self._svg_background):
                # Если файл поменялся, то перезаписать его в HOME папке
                filefunc.copyFile(self._svg_background, svg_filename)
                # и удалить все файлы PNG
                filefunc.delAllFilesFilter(filefunc.getPrjProfilePath(), '%s_background_*.png' % self.getName())

            if not os.path.exists(png_filename) or bAutoRewrite:
                # Запустить конвертацию файла
                cmd = SVG2PNG_CONVERT_CMD_FMT % (width, height, width, height, svg_filename, png_filename)
                log.debug(u'Запуск команды ковертации SVG -> PNG: <%s>' % cmd)
                os.system(cmd)
                if not os.path.exists(png_filename):
                    log.warning(u'Ошибка конвертации SVG -> PNG (<%s> -> <%s>)' % (svg_filename, png_filename))
                    return False

            self._background_bitmap = bmpfunc.createBitmap(png_filename)
            return True
        except:
            log.fatal(u'Ошибка отрисовки фона мнемосхемы')
        return False

    def getBackgroundBitmap(self):
        """
        Объект картинки для отображения фона.

        :return: Объект wx.Bitmap, соответствующий текущему фону мнемосхемы.
        """
        return self._background_bitmap
