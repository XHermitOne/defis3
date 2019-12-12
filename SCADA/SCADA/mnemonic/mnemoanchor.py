#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс якоря для прикрепления контролов к мнемосхеме.

Для позиционирования контролов на мнемосхеме используются компоненты-якоря,
которые определяют положение и размер контролов ввода вывода относительно
элементов SVG фона мнемосхемы.
"""

from ic.log import log

from ic.components import icwidget


# Version
__version__ = (0, 1, 1, 1)

# Указание направления смещения якоря относительно опорной точки
ANCHOR_DIRECTION_FROM_LEFT_TO_RIGHT = 1  # Слева направо
ANCHOR_DIRECTION_FROM_RIGHT_TO_LEFT = 2  # Справа налево
ANCHOR_DIRECTION_FROM_TOP_TO_BOTTOM = 4  # Сверху вниз
ANCHOR_DIRECTION_FROM_BOTTOM_TO_TOP = 8  # Снизу вверх

# --- Спецификация ---
SPC_IC_MNEMOANCHOR = {'svg_pos': (0.0, 0.0),
                      'svg_size': (-1, -1),
                      'style': ANCHOR_DIRECTION_FROM_LEFT_TO_RIGHT | ANCHOR_DIRECTION_FROM_TOP_TO_BOTTOM,
                      'min_size': (-1, -1),
                      'max_size': (-1, -1),
                      'attachment': None,
                      
                      '__parent__': icwidget.SPC_IC_SIMPLE,

                      '__attr_hlp__': {'svg_pos': u'Опорная позиция якоря в единицах измерения SVG',
                                       'svg_size': u'Размер ячейки якоря в единицах измерения SVG',
                                       'style': u'Указание направления смещения якоря относительно опорной точки',
                                       'min_size': u'Указание ограничения размера по минимуму в пикселях',
                                       'max_size': u'Указание ограничения размера по максимуму в пикселях',
                                       'attachment': u'Имя контрола мнемосхемы, прикрепленного к якорю',
                                       },
                      }

# ВНИМАНИЕ! Замечено, что при экспорте из LibreOffice Draw схемы в SVG файл
# смещается результирующие координаты. Для коррекции введено дополнительное смещение
# Значения подобраны экспериментальным путем
CORRECT_SVG_OFFSET_X = 1.7
CORRECT_SVG_OFFSET_Y = 1.65


class icMnemoAnchorProto(object):
    """
    Якорь мнемосхемы.
    """
    def __init__(self, mnemoscheme=None, pos=None, size=None,
                 direction=ANCHOR_DIRECTION_FROM_LEFT_TO_RIGHT | ANCHOR_DIRECTION_FROM_TOP_TO_BOTTOM,
                 min_size=None, max_size=None):
        """
        Конструктор.

        :param mnemoscheme: Объект мнемосхемы.
        :param pos: Опорная позиция якоря в единицах измерения SVG.
        :param size: Размер ячейки якоря в единицах измерения SVG.
        :param direction: Указание направления смещения якоря относительно опорной точки.
        :param min_size: Указание ограничения размера по минимуму в пикселях.
        :param max_size: Указание ограничения размера по максимуму в пикселях.
        """
        self._mnemoscheme = mnemoscheme
        self._position = pos
        self._size = size
        self._direction = direction
        self._min_size = min_size
        self._max_size = max_size

    def getAttachment(self):
        """
        Получить объект прикрепленного к якорю контрола.

        :return: Объект контрола, который может быть размещен на мнемосхеме
            или None в случае ошибки.
        """
        log.warning(u'Не определен метод получения объекта прикрепленного к якорю контрола')
        return None

    def layoutControl(self, ctrl=None):
        """
        Установить позицию и размер контрола в ссответствии с данным якорем.

        :param ctrl: Объект контрола.
        :return: True/False.
        """
        if ctrl is None:
            ctrl = self.getAttachment()

        if ctrl:
            try:
                # Расчет координат области якоря
                pix_left, pix_top, pix_right, pix_bottom = self.calc_rectangle()

                # Позиция контрола
                ctrl.SetPosition((pix_left, pix_top))
                # Размер контрола
                width = pix_right - pix_left
                height = pix_bottom - pix_top
                width = width if width > 0 else -1
                height = height if height > 0 else -1
                if width >= 0 and height >= 0:
                    ctrl.SetSize((width, height))

                return True
            except:
                log.fatal(u'Ошибка установки размера и позиции контрола в соответствии с якорем <%s>' % self.getName())
        else:
            log.warning(u'Не определен прикрепленный контрол к якорю <%s>' % self.getName())
        return False

    def calc_pix_position(self, svg_position=None):
        """
        Расчет позиции опорной точки в пикселях.

        :param svg_position: Позиция опорной точки по
        :return: Расчетная позиции опорной точки в пикселях или (0, 0) в случае ошибки.
        """
        if svg_position is None:
            svg_position = self._position

        if self._mnemoscheme is None:
            log.warning(u'Не определена мнемосхема для якоря <%s>' % self.getName())
            return 0, 0

        # Определяем необходимые для расчета размеры мнемосхемы
        svg_width, svg_height = self._mnemoscheme.getSVGSize()
        pix_width, pix_height = self._mnemoscheme.GetSize()

        # Расчитываем коэффициент масштабирования для ширины и высоты отдельно
        zoom_coef_width = float(svg_width) / float(pix_width)
        zoom_coef_height = float(svg_height) / float(pix_height)

        # Определяем коэффициент масштабирования
        zoom_coef = max(zoom_coef_width, zoom_coef_height)

        # Расчет
        svg_pos_x, svg_pos_y = svg_position
        if zoom_coef:
            pix_offset_x = round((float(pix_width) - float(svg_width) / zoom_coef) / 2.0)
            pix_offset_y = round((float(pix_height) - float(svg_height) / zoom_coef) / 2.0)
            pix_x = round((float(svg_pos_x) - CORRECT_SVG_OFFSET_X) / zoom_coef) + pix_offset_x
            pix_y = round((float(svg_pos_y) - CORRECT_SVG_OFFSET_Y) / zoom_coef) + pix_offset_y
            # log.debug(u'Расчетные значения:')
            # log.debug(u'\tРазмер в точках [%d x %d]' % (pix_width, pix_height))
            # log.debug(u'\tРазмер SVG [%f x %f]' % (float(svg_width), float(svg_height)))
            # log.debug(u'\tКоэффициент масштабирования [%f x %f] [%f]' % (zoom_coef_width, zoom_coef_height, zoom_coef))
            # log.debug(u'\tСмещение [%d x %d]' % (pix_offset_x, pix_offset_y))
            # log.debug(u'\tРезультирующая точка [%d x %d]' % (pix_x, pix_y))

            return pix_x, pix_y
        else:
            log.warning(u'Расчетный коэффициент масштабирования нулевой для мнемосхемы <%s>:' % self._mnemoscheme.getName())
            log.warning(u'\tПроверьте атрибуты svg_width и svg_height мнемосхемы <%s>' % self._mnemoscheme.getName())
            log.warning(u'\tОни не должны быть нулевые!')
        return 0, 0

    def calc_rectangle(self, svg_position=None, svg_size=None,
                       direction=ANCHOR_DIRECTION_FROM_LEFT_TO_RIGHT | ANCHOR_DIRECTION_FROM_TOP_TO_BOTTOM,
                       min_size=None, max_size=None):
        """
        Расчет координат области якоря.

        :param svg_position: Опорная позиция якоря в единицах измерения SVG.
        :param svg_size: Размер ячейки якоря в единицах измерения SVG.
        :param direction: Указание направления смещения якоря относительно опорной точки.
        :param min_size: Указание ограничения размера по минимуму в пикселях.
        :param max_size: Указание ограничения размера по максимуму в пикселях.
        :return: Расчтеные координаты прямоугольной области в пикселях или
            (0, 0, 0, 0) в случае ошибки.
        """
        if svg_position is None:
            svg_position = self._position
        if svg_size is None:
            svg_size = self._size
        if min_size is None:
            min_size = self._min_size
        if max_size is None:
            max_size = self._max_size

        # Расчет позиции опорной точки
        pix_position = self.calc_pix_position(svg_position)

        # Ставим позицию смещения в эту же точку
        svg_pos_x, svg_pos_y = svg_position
        svg_width, svg_height = svg_size
        svg_offset_x, svg_offset_y = svg_pos_x, svg_pos_y

        # Расчет второй точки с учетом направления смещения
        if direction & ANCHOR_DIRECTION_FROM_LEFT_TO_RIGHT:
            svg_offset_x = svg_pos_x + svg_width
        if direction & ANCHOR_DIRECTION_FROM_RIGHT_TO_LEFT:
            svg_offset_x = svg_pos_x - svg_width
        if direction & ANCHOR_DIRECTION_FROM_TOP_TO_BOTTOM:
            svg_offset_y = svg_pos_y + svg_height
        if direction & ANCHOR_DIRECTION_FROM_BOTTOM_TO_TOP:
            svg_offset_y = svg_pos_y - svg_height
        pix_offset_position = self.calc_pix_position(svg_position=(svg_offset_x, svg_offset_y))

        # Получаем координаты области
        pix_left = min(pix_position[0], pix_offset_position[0])
        pix_top = min(pix_position[1], pix_offset_position[1])
        pix_right = max(pix_position[0], pix_offset_position[0])
        pix_bottom = max(pix_position[1], pix_offset_position[1])

        # Производим ограничения по размерам
        if min_size:
            if min_size[0] > 0:
                pix_right = max(pix_right, pix_left + min_size[0])
            if min_size[1] > 0:
                pix_bottom = max(pix_bottom, pix_top + min_size[1])
        if max_size:
            if max_size[0] > 0:
                pix_right = min(pix_right, pix_left + max_size[0])
            if max_size[1] > 0:
                pix_bottom = min(pix_bottom, pix_top + max_size[1])

        # log.debug(u'2Размер области якоря [%d %d %d %d]' % (pix_left, pix_top, pix_right, pix_bottom))
        return pix_left, pix_top, pix_right, pix_bottom
