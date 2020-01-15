#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Абстрактный класс временного графика. Исторический тренд.

Класс организует интерфейс, который должны наследовать все тренды.
"""

import datetime
import wx

from ic.utils import datetimefunc
from ic.log import log

__version__ = (0, 1, 1, 2)

# Форматы используемые для отображения временной шкалы
DEFAULT_TIME_FMT = '%H:%M:%S'
DEFAULT_DATE_FMT = '%d.%m.%Y'
DEFAULT_DATETIME_FMT = '%d.%m.%Y-%H:%M:%S'
DEFAULT_DT_FORMATS = (DEFAULT_TIME_FMT,
                      DEFAULT_DATETIME_FMT,
                      DEFAULT_DATE_FMT)

# Формат шкал по умолчанию
DEFAULT_X_FORMAT = 'time'
DEFAULT_Y_FORMAT = 'numeric'

DEFAULT_X_FORMATS = ('time', 'date', 'datetime')
DEFAULT_Y_FORMATS = ('numeric', )


class icTrendProto(object):
    """
    Абстрактный класс временного графика. Исторический тренд.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        today = datetime.date.today()

        self.start_datetime = datetime.datetime.combine(today,
                                                        datetime.datetime.min.time())
        self.stop_datetime = datetime.datetime.combine(today+datetime.timedelta(days=1),
                                                       datetime.datetime.min.time())

    def _convertDate(self, dt):
        """
        Корректное преобразование типа даты в datetime.datetime.

        :param dt: Дата.
        :return: Дата-время.
        """
        new_dt = None
        if isinstance(dt, datetime.date):
            # Если дата задается datetime.date
            # то сделать перевод в datetime.datetime
            new_dt = datetime.datetime.combine(dt,
                                               datetime.datetime.min.time())
        elif isinstance(dt, wx.DateTime):
            new_dt = datetimefunc.wxdatetime2pydatetime(dt)
        elif dt is None:
            new_dt = datetime.datetime.now()
        elif isinstance(dt, datetime.datetime):
            new_dt = dt
        else:
            assert isinstance(dt, (datetime.datetime, datetime.date))
        return new_dt

    def _dt2str(self, dt_value=None, time_format=DEFAULT_X_FORMAT):
        """
        Преобразование datetime в строковый вид согласно формату.

        :param dt_value: Значение datetime.datetime или datetime.timedelta.
        :param time_format: Формат представления.
        :return: Отформатированная строка значений datetime.
        """
        if time_format == 'time':
            time_format = DEFAULT_TIME_FMT
        elif time_format == 'date':
            time_format = DEFAULT_DATE_FMT
        elif time_format == 'datetime':
            time_format = DEFAULT_DATETIME_FMT

        if isinstance(dt_value, datetime.datetime) or isinstance(dt_value, datetime.date):
            return dt_value.strftime(time_format)
        elif isinstance(dt_value, datetime.timedelta):
            return datetimefunc.strfdelta(dt_value, fmt='{H:02}h {M:02}m {S:02}s')
        else:
            log.warning(u'Не поддерживаемый тип временных значений <%s>' % dt_value.__class__.__name__)
        return ''

    def _str2dt(self, time_value=None, time_format=DEFAULT_X_FORMAT, bToTimeDelta=False):
        """
        Преобразование строкового представления значений
        временной шкалы в datetime вид.

        :param time_value: Строковое представление даты-вермени.
        :param time_format: Формат представления.
        :param bToTimeDelta: Преобразовать в datetime.timedelta?
        :return: datetime.datetime/datetime.timedelta, соответствующий строковому представлению.
        """
        if time_format == 'time':
            time_format = DEFAULT_TIME_FMT
            dt = datetime.datetime.strptime(time_value, time_format)
            if bToTimeDelta:
                return datetime.timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
        elif time_format == 'date':
            time_format = DEFAULT_DATE_FMT
            dt = datetime.datetime.strptime(time_value, time_format)
            if bToTimeDelta:
                return datetime.timedelta(days=dt.day)
        elif time_format == 'datetime':
            time_format = DEFAULT_DATETIME_FMT
            dt = datetime.datetime.strptime(time_value, time_format)
            if bToTimeDelta:
                return datetime.timedelta(days=dt.day,
                                          hours=dt.hour, minutes=dt.minute, seconds=dt.second)
        else:
            dt = datetime.datetime.strptime(time_value, time_format)
            if bToTimeDelta:
                return datetime.timedelta(days=dt.day,
                                          hours=dt.hour, minutes=dt.minute, seconds=dt.second)
        return dt

    def _get_dt_format(self, time_format=DEFAULT_X_FORMAT):
        """
        Привести к единому виду формат временных значений.

        :param time_format: Формат представления.
        :return: Формат
        """
        dt_format = time_format
        if time_format == 'time':
            dt_format = DEFAULT_TIME_FMT
        elif time_format == 'date':
            dt_format = DEFAULT_DATE_FMT
        elif time_format == 'datetime':
            dt_format = DEFAULT_DATETIME_FMT
        return dt_format

    def setStartDT(self, new_dt):
        """
        Начальная дата-время тренда.

        :param new_dt: Новое значение.
        """
        self.start_datetime = self._convertDate(new_dt)

    def getStartDT(self):
        """
        Начальная дата-время тренда.
        """
        return self.start_datetime

    def setStopDT(self, new_dt):
        """
        Конечная дата-время тренда.

        :param new_dt: Новое значение.
        """
        self.stop_datetime = self._convertDate(new_dt)

    def getStopDT(self):
        """
        Конечная дата-время тренда.
        """
        return self.stop_datetime

    def setDefaults(self):
        """
        Установить параметры по умолчанию.
        """
        pass

    def draw_empty(self):
        """
        Отрисовка пустого тренда.
        """
        log.warning(u'Не определен метод  отрисовки пустого тренда')

    def getPenData(self, pen_index=0):
        """
        Данные соответствующие перу.

        :param pen_index: Индекс пера. По умолчанию берется первое перо.
        :return: Список (Время, Значение)
        """
        pens = self.getPens()

        if pens and pen_index < len(pens):
            return pens[pen_index].getLineData()

        return list()

    def draw(self, redraw=True):
        """
        Основной метод отрисовки тренда.

        :param redraw: Принудительная прорисовка.
        """
        log.warning(u'Не определен метод отрисовки тренда')

    def getPens(self):
        """
        Список перьев тренда.
        """
        log.warning(u'Не определен метод получения перьев')
        return list()

    def setHistory(self, history):
        """
        Поменять источник данных для всех перьев тренда.

        :param history: Объект исторических данных - источника данных.
        :return: True/False.
        """
        pens = self.getPens()

        result = True
        for pen in pens:
            result = result and pen.setHistory(history)
        return result

    def zoomX(self, step=1, redraw=True):
        """
        Увеличить цену деления оси X в соответствии со шкалой настройки.

        :param step: Шаг по шкале настройки
            >0 - увеличение
            <0 - уменьшение
        :param redraw: Произвести перерисовку кадра тренда?
        :return: True/False.
        """
        log.warning(u'Не определен метод масштабирования тренда')
        return False

    def zoomY(self, step=1, redraw=True):
        """
        Увеличить цену деления оси Y в соответствии со шкалой настройки.

        :param step: Шаг по шкале настройки
            >0 - увеличение
            <0 - уменьшение
        :param redraw: Произвести перерисовку кадра тренда?
        :return: True/False.
        """
        log.warning(u'Не определен метод масштабирования тренда')
        return False

    def moveSceneX(self, step=1, redraw=True):
        """
        Передвижение сцены по оси X на указанное количество цены деления.

        :param step: Количество цен деления для передвижения
            >0 - увеличение
            <0 - уменьшение
        :param redraw: Произвести перерисовку кадра тренда?
        :return: True/False.
        """
        log.warning(u'Не определен метод движения тренда')
        return False

    def moveSceneY(self, step=1, redraw=True):
        """
        Передвижение сцены по оси Y на указанное количество цены деления.

        :param step: Количество цен деления для передвижения
            >0 - увеличение
            <0 - уменьшение
        :param redraw: Произвести перерисовку кадра тренда?
        :return: True/False.
        """
        log.warning(u'Не определен метод движения тренда')
        return False
