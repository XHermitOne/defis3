#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс поддержки индикатора элементов дерева.

Индикатор представляет собой описание
пост обработки отфильтрованного набора записей
с целью изменения картинки/цвет текста/цвет фона
контролов индикации формы.
Описание индикатора это список состояний индикатора,
каждое из которого состоит из выражения проверки состояния и
описания картинки/цвета текста/цвета фона.

Формат описания индикатора фильтра:
[
    {
        'name': Наименование состояния,
        'image': Файл образа,
        'text_color': Кортеж (R, G, B) цвета текста,
        'background_color': Кортеж (R, G, B) цвета фона,
        'expression': Текст блока кода выражения проверки состояния,
    },
    ...
]


Выражение должно возвращать True/False.
True - индикатор в текущем состоянии и дальнейшая проверка не нужна.
False - индикатор не в текущем стостоянии,
происходит дальнейшая проверка других состояний.
Отсюда видно что сначала должны проверятся самые критичные состояния.
Т.е. они должные стоять в списке описаний состояний на первом месте,
а затем менее критичные.

При выполнении выражения в его окружении присутствует объект RECORDS.
RECORDS - список словарей записей отфильтрованных текущим фильтром.
"""

import os.path
import wx

from ic.log import log
from ic.bitmap import ic_bmp
from ic.utils import wxfunc

from . import indicator_constructor_dlg

__version__ = (0, 1, 3, 1)

UNKNOWN_STATE_NAME = u'Имя состояния не определено'


# Функции управления описанием индикаторов
def create_indicator():
    """
    Создание списка индикатора.
    @return: Пустой список индикатора.
    """
    return list()


def new_indicator_state(indicator=None,
                        name=UNKNOWN_STATE_NAME, img_filename=None,
                        text_color=None, background_color=None,
                        expression=None):
    """
    Добавить новое состояние в сприсок индикатора.
    @param indicator: Список индикатора.
    @param name: Наименование состояния.
    @param img_filename: Файл образа.
    @param text_color: Кортеж (R, G, B) цвета текста.
    @param background_color: Кортеж (R, G, B) цвета фона.
    @param expression: Текст блока кода выражения проверки состояния.
    @return: Измененный список индикатора.
    """
    if text_color is None:
        text_color = wxfunc.wxColour2RGB(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
    if background_color is None:
        background_color = wxfunc.wxColour2RGB(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

    if indicator is None:
        indicator = create_indicator()
    new_state = dict(name=name, image=img_filename,
                     text_color=text_color, background_color=background_color,
                     expression=expression)
    indicator.append(new_state)
    return indicator


def find_indicator_state(indicator, name):
    """
    Поиск состояния индикатора в списке индикатора по имени.
    @param indicator: Список индикатора.
    @param name: Наименование состояния.
    @return: Структура данных состояния или None если нет состояния с таким именем.
    """
    names = [state.get('name', None) for state in indicator]
    find_state = indicator[names.index(name)] if name in names else None
    return find_state


class icTreeItemIndicator(object):
    """
    Индикатор элемента дерева.
    """
    def __init__(self, indicator=None):
        """
        Конструктор.
        @param indicator: Описание текущего индикатора.
        """
        self._indicator = indicator

    def editIndicator(self, parent=None, indicator=None):
        """
        Редактировать индикатор фильтра.
        @param parent: Родительское окно.
        @param indicator: Описание текущего индикатора.
            Если не определен, то берется описание внутреннего индикатора.
        @return: Отредактированный индикатор фильтра.
        """
        if parent is None:
            app = wx.GetApp()
            parent = app.GetTopWindow()

        if indicator is None:
            indicator = self._indicator

        indicator = indicator_constructor_dlg.edit_indicator_constructor_dlg(parent=parent, indicator=indicator)

        return indicator

    def getIndicator(self):
        """
        Текущее описание индикатора фильтра.
        """
        return self._indicator

    def getLabelIndicator(self, indicator=None):
        """
        Представление списка индикатора в виде строки надписи.
        @param indicator: Описание текущего индикатора.
            Если не определен, то берется описание внутреннего индикатора.
        @return: Строка надписи индикатора.
        """
        if indicator is None:
            indicator = self._indicator

        label = u'<%s>' % u', '.join([state_indicator.get('name', UNKNOWN_STATE_NAME) for state_indicator in indicator])
        return label

    def getStateIndicator(self, records=None, indicator=None):
        """
        Определить сотояние индикатора по набору записей.
        @param records: Набор записей.
            Представляет собой словарей записей.
        @param indicator: Описание текущего индикатора.
            Если не определен, то берется описание внутреннего индикатора.
        @return: Словарь описания состояния:
            {
            'name': Наименование состояния,
            'image': Файл образа,
            'text_color': Кортеж (R, G, B) цвета текста,
            'background_color': Кортеж (R, G, B) цвета фона,
            }
            Если набор записей не соответствует ни одному из состояний,
            то возвращается None.
        """
        if indicator is None:
            indicator = self._indicator

        if records is None:
            records = list()

        RECORDS = records

        for state_indicator in indicator:
            state_name = state_indicator.get('name', UNKNOWN_STATE_NAME)
            expression = state_indicator.get('expression', None)
            exp_result = False
            if expression:
                try:
                    exp_result = eval(expression, globals(), locals())
                except:
                    log.error(u'Ошибка выполнения выражения:')
                    log.fatal(expression)
            else:
                log.warning(u'Не определено выражение состояния индикатора <%s>' % state_name)

            if exp_result:
                # Условие соответствует, возвращаем описание состояния
                return state_indicator
        # Ни одно из условий не подтвердилось
        return None

    def getStateIndicatorObjects(self, records=None, indicator=None):
        """
        Определить объекты сотояния индикатора по набору записей.
        @param records: Набор записей.
            Представляет собой словарей записей.
        @param indicator: Описание текущего индикатора.
            Если не определен, то берется описание внутреннего индикатора.
        @return: Кортеж объектов состояния:
            (
                Наименование состояния,
                wx.Bitmap образа состояния,
                wx.Colour цвета текста,
                wx.Colour цвета фона
            )
            Если набор записей не соответствует ни одному из состояний,
            то возвращается (None, None, None, None).
        """
        state_indicator = self.getStateIndicator(records=records, indicator=indicator)
        if state_indicator is None:
            return None, None, None, None

        # Имя
        name = state_indicator.get('name', UNKNOWN_STATE_NAME)

        # Образ
        image = None
        img_filename = state_indicator.get('image', None)
        if img_filename:
            if os.path.exists(img_filename):
                # Файл образа задан как абсолютное имя файла
                image = ic_bmp.createBitmap(img_filename)
            elif img_filename == os.path.basename(img_filename):
                # Файл образа задан как имя файла библиотеки
                image = ic_bmp.createLibraryBitmap(img_filename)
            else:
                log.warning(u'Не корректное имя файла образа <%s>' % img_filename)

        # Цвет текста
        rgb = state_indicator.get('text_color', None)
        text_colour = wx.Colour(tuple(rgb)) if rgb else None

        # Цвет фона
        rgb = state_indicator.get('background_color', None)
        background_colour = wx.Colour(tuple(rgb)) if rgb else None

        return name, image, text_colour, background_colour
