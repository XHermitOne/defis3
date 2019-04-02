#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Компонент временного графика. Тренд.
Абстрактный класс.
Компонент реализован на базе утилиты nixplot.

Тренд позволяет отображать данные только в пределах суток.
"""

import os.path
import wx
import datetime
import time
import uuid

from ic.log import log
from ic.utils import ic_file
from ic.utils import ic_time
from ic.bitmap import ic_bmp

from ic.components import icwidget

from SCADA.scada_proto import trend_proto

# Полное имя файла утилиты nixplot
PACKAGE_PATH = os.path.dirname(__file__) if os.path.dirname(__file__) else '.'
NIXPLOT_FILENAME = os.path.join(PACKAGE_PATH, 'nixplot')

# Папка размещения кадров трендов
DEFAULT_NIXPLOT_FRAME_PATH = os.path.join(ic_file.getProfilePath(), 'nixplot')

# Минимальные размеры кадра
MIN_FRAME_WIDTH = 640
MIN_FRAME_HEIGHT = 480

# Типы файлов кадра
PNG_FILE_TYPE = 'PNG'
PDF_FILE_TYPE = 'PDF'

# Возможные настройки шкал по умолчанию
DEFAULT_X_TUNES = ('00:00:10', '00:00:20', '00:00:30', '00:01:00', '00:05:00', '00:20:00', '00:30:00', '01:00:00')
DEFAULT_Y_TUNES = (1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0)

# Цена деления по умолчанию
DEFAULT_X_PRECISION = '01:00:00'
DEFAULT_Y_PRECISION = '1.0'

# --- Спецификация ---
SPC_IC_NIXPLOT_TREND = {'x_format': trend_proto.DEFAULT_X_FORMAT,   # Формат представления данных оси X
                        'y_format': trend_proto.DEFAULT_Y_FORMAT,   # Формат представления данных оси Y
                        'scene_min': ('00:00:00', 0.0),    # Минимальное значение видимой сцены тренда
                        'scene_max': ('12:00:00', 0.0),    # Максимальное значение видимой сцены тренда
                        'x_tunes': DEFAULT_X_TUNES,     # Возможные настройки шкалы X
                        'y_tunes': DEFAULT_Y_TUNES,     # Возможные настройки шкалы Y
                        'x_precision': DEFAULT_X_PRECISION, # Цена деления сетки тренда по шкале X
                        'y_precision': DEFAULT_Y_PRECISION, # Цена деления сетки тренда по шкале Y

                        '__parent__': icwidget.SPC_IC_WIDGET,
                        '__attr_hlp__': {'x_format': u'Формат представления данных оси X',
                                         'y_format': u'Формат представления данных оси Y',
                                         'scene_min': u'Минимальное значение видимой сцены тренда',
                                         'scene_max': u'Максимальное значение видимой сцены тренда',
                                         'x_tunes': u'Возможные настройки шкалы X',
                                         'y_tunes': u'Возможные настройки шкалы Y',
                                         'x_precision': u'Цена деления сетки тренда по шкале X',
                                         'y_precision': u'Цена деления сетки тренда по шкале Y',
                                         },
                        }

# Версия
__version__ = (0, 1, 2, 1)


class icNixplotTrendProto(wx.Panel, trend_proto.icTrendProto):
    """
    Базовый класс временного графика. Тренд.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        wx.Panel.__init__(self, *args, **kwargs)

        # ВНИМАНИЕ! У каждого тренда есть свой собственный идентификатор
        # для того чтобы не пересекались отображения с другими трендами
        self.__trend_uuid = str(uuid.uuid4())
        # Имя файла кадра
        self.__frame_filename = None

        self.canvas = wx.StaticBitmap(self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

        trend_proto.icTrendProto.__init__(self, *args, **kwargs)

        self.setDefaults()

        # Текущая сцена тренда - Границы окна сцены в данных предметной области.
        # Представляется в виде кортежа (X1, Y1, X2, Y2)
        self._cur_scene = None

        # Шкалы настройки
        self._x_tunes = DEFAULT_X_TUNES
        self._y_tunes = DEFAULT_Y_TUNES
        # Цена деления
        self._x_precision = DEFAULT_X_PRECISION
        self._y_precision = DEFAULT_Y_PRECISION
        # Формат шкал
        self._x_format = trend_proto.DEFAULT_X_FORMAT
        self._y_format = trend_proto.DEFAULT_Y_FORMAT

        # ВНИМАНИЕ! Если необходимо удалить/освободить
        # ресуры при удалении контрола, то необходимо воспользоваться
        # событием wx.EVT_WINDOW_DESTROY
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)

    def setScene(self, min_x=None, min_y=None, max_x=None, max_y=None):
        """
        Установить текущую сцену тренда.
        @param min_x: Минимальное значение по оси X.
        @param min_y: Минимальное значение по оси Y.
        @param max_x: Максимальное значение по оси X.
        @param max_y: Максимальное значение по оси Y.
        @return: Текущая сцена тренда.
        """
        # Адаптация сцены по данным
        if self._cur_scene is None:
            pen_data = self.getPenData(pen_index=0)
            self._cur_scene = self.adaptScene(pen_data)

        if self._cur_scene is None:
            # Адаптация закончилась безуспешно
            self._cur_scene = (datetime.datetime.now().replace(hour=0, minute=0, second=0), 0.0,
                               datetime.datetime.now().replace(hour=23, minute=59, second=59), 100.0)

        scene = list(self._cur_scene)
        if min_x:
            scene[0] = self._str2dt(min_x, self._x_format) if isinstance(min_x, str) else min_x
        if min_y:
            scene[1] = min_y
        if max_x:
            scene[2] = self._str2dt(max_x, self._x_format) if isinstance(max_x, str) else max_x
        if max_y:
            scene[3] = max_y
        self._cur_scene = tuple(scene)
        return self._cur_scene

    def setTunes(self, x_tunes=None, y_tunes=None):
        """
        Установить шкалы настройки.
        @param x_tunes: Шкала настройки по оси X.
            Если None, то шкала не устанавливается.
        @param y_tunes: Шкала настройки по оси Y.
            Если None, то шкала не устанавливается.
        @return: Кортеж (x_tunes, y_tunes) текущих шкал настройки.
        """
        if x_tunes is not None:
            self._x_tunes = x_tunes
        if y_tunes is not None:
            self._y_tunes = y_tunes
        return self._x_tunes, self._y_tunes

    def setFormats(self, x_format=None, y_format=None):
        """
        Установить форматы шкал.
        @param x_format: Формат шкалы оси X.
            Если None, то формат не устанавливается.
        @param y_format: Формат шкалы оси Y.
            Если None, то формат не устанавливается.
        @return: Кортеж (x_format, y_format) текущих форматов.
        """
        if x_format is not None:
            self._x_format = x_format
        if y_format is not None:
            self._y_format = y_format
        return self._x_format, self._y_format

    def setPrecisions(self, x_precision=None, y_precision=None):
        """
        Установить цену деления по осям.
        @param x_precision: Цена деления оси X.
            Если None, то цена деления не устанавливается.
        @param y_precision: Цена деления оси Y.
            Если None, то цена деления не устанавливается.
        @return: Кортеж (x_precision, y_precision) текущих цен деления.
        """
        if x_precision is not None:
            if isinstance(x_precision, str):
                # Цена деления задается строкой
                # необходимо правильно преобразовать
                x_precision = self._str2dt(x_precision, self._x_format, bToTimeDelta=True)
            self._x_precision = x_precision
        if y_precision is not None:
            if not isinstance(y_precision, float):
                y_precision = float(y_precision)
            self._y_precision = y_precision
        return self._x_precision, self._y_precision

    def onDestroy(self, event):
        """
        При удалении панели. Обработчик события.
        ВНИМАНИЕ! Если необходимо удалить/освободить
        ресуры при удалении контрола, то необходимо воспользоваться
        событием wx.EVT_WINDOW_DESTROY.
        """
        self.del_frame(self.getFrameFileName(PNG_FILE_TYPE))
        self.del_frame(self.getFrameFileName(PDF_FILE_TYPE))
        event.Skip()

    def getTrendUUID(self):
        """
        Идентификатор тренда-объекта.
        ВНИМАНИЕ! У каждого тренда есть свой собственный идентификатор
        для того чтобы не пересекались отображения с другими трендами
        """
        return self.__trend_uuid

    def getFrameFileName(self, file_type=PNG_FILE_TYPE):
        """
        Имя файла кадра.
        """
        file_ext = '.' + file_type.lower()
        if self.__frame_filename is None or not self.__frame_filename.endswith(file_ext):
            obj_uuid = self.getTrendUUID()
            self.__frame_filename = os.path.join(DEFAULT_NIXPLOT_FRAME_PATH, obj_uuid + file_ext)
        return self.__frame_filename

    def getCurScene(self):
        """
        Текущая сцена тренда - Границы окна сцены в данных предметной области.
        Представляется в виде кортежа (X1, Y1, X2, Y2)
        """
        return self._cur_scene

    def _convertDate(self, dt):
        """
        Корректное преобразование типа даты в datetime.datetime.
        @param dt: Дата.
        @return: Дата-время.
        """
        new_dt = None
        if isinstance(dt, datetime.date):
            # Если дата задается datetime.date
            # то сделать перевод в datetime.datetime
            new_dt = datetime.datetime.combine(dt,
                                               datetime.datetime.min.time())
        elif isinstance(dt, wx.DateTime):
            new_dt = ic_time.wxdatetime2pydatetime(dt)
        elif dt is None:
            new_dt = datetime.datetime.now()
        elif isinstance(dt, datetime.datetime):
            new_dt = dt
        else:
            assert isinstance(dt, (datetime.datetime, datetime.date))
        return new_dt

    def setStartDT(self, new_dt):
        """
        Начальная дата-время тренда.
        @param new_dt: Новое значение.
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
        @param new_dt: Новое значение.
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
        if not os.path.exists(DEFAULT_NIXPLOT_FRAME_PATH):
            try:
                os.makedirs(DEFAULT_NIXPLOT_FRAME_PATH)
                log.info(u'Создана папка <%s>' % DEFAULT_NIXPLOT_FRAME_PATH)
            except:
                log.warning(u'Ошибка создания папки <%s>' % DEFAULT_NIXPLOT_FRAME_PATH)

    def del_frame(self, frame_filename=None):
        """
        Удалить файл кадра
        @param frame_filename: Имя файла кадра тренда.
        @return: True/False.
        """
        if frame_filename is None:
            frame_filename = self.getFrameFileName()

        if os.path.exists(frame_filename):
            try:
                os.remove(frame_filename)
                log.info(u'Удален файл кадра тренда <%s>' % frame_filename)
                return True
            except OSError:
                log.error(u'Ошибка удаления файла кадра <%s>' % frame_filename)
        else:
            log.warning(u'Файл кадра тренда <%s> не найден' % frame_filename)
        return False

    # Словарь замены форматов шкал
    _Fmt2NixplotType = {'numeric': 'N',
                        'time': 'T',
                        'date': 'D',
                        'datetime': 'DT',
                        'exponent': 'E'}

    def draw_frame(self, size=(0, 0), x_format='time', y_format='numeric',
                   scene=None, points=None):
        """
        Отрисовка кадра данных тренда.
        @param size: Размер кадра в точках.
        @param x_format: Формат шкалы X.
        @param y_format: Формат шкалы Y.
        @param scene: Границы окна сцены в данных предметной области.
        @param points: Список точек графика.
        @return: Имя файла отрисованного кадра или None в случае ошибки.
        """
        try:
            if scene is None:
                scene = self._cur_scene

            return self._draw_frame(size=size, x_format=x_format, y_format=y_format,
                                    scene=scene, points=points, file_type=PNG_FILE_TYPE)
        except:
            log.fatal(u'Ошибка отрисовки кадра')
        return None

    def report_frame(self, size=(0, 0), x_format='time', y_format='numeric',
                     scene=None, points=None):
        """
        Отрисовка кадра данных тренда в виде отчета PDF.
        @param size: Размер кадра в точках.
        @param x_format: Формат шкалы X.
        @param y_format: Формат шкалы Y.
        @param scene: Границы окна сцены в данных предметной области.
        @param points: Список точек графика.
        @return: Имя файла отрисованного кадра или None в случае ошибки.
        """
        try:
            if scene is None:
                scene = self._cur_scene

            return self._draw_frame(size=size, x_format=x_format, y_format=y_format,
                                    scene=scene, points=points, file_type=PDF_FILE_TYPE)
        except:
            log.fatal(u'Ошибка отрисовки кадра в виде отчета')
        return None

    def _draw_frame(self, size=(0, 0), x_format='time', y_format='numeric', scene=None,
                    points=None, file_type=PNG_FILE_TYPE):
        """
        Отрисовка кадра данных тренда.
        @param size: Размер кадра в точках.
        @param x_format: Формат шкалы X.
        @param y_format: Формат шкалы Y.
        @param scene: Границы окна сцены в данных предметной области.
        @param points: Список точек графика.
        @return: Имя файла отрисованного кадра или None в случае ошибки.
        """
        cmd = '%s --%s ' % (NIXPLOT_FILENAME, file_type)

        frame_filename = self.getFrameFileName(file_type)
        # log.debug(u'Файл кадра: %s' % frame_filename)
        self.del_frame(frame_filename)

        cmd += '--out=%s ' % frame_filename

        xtype = self._Fmt2NixplotType.get(x_format, 'T')
        ytype = self._Fmt2NixplotType.get(y_format, 'N')
        cmd += '--xtype=%s --ytype=%s ' % (xtype, ytype)

        if size is not None:
            width, height = size
            width = max(width, MIN_FRAME_WIDTH)
            height = max(height, MIN_FRAME_HEIGHT)
            if width > 0 and height > 0:
                cmd += '--width=%s --height=%s ' % (width, height)

        # Выставить сцену
        if scene is None:
            scene = self._cur_scene

        if scene[0] != scene[2] and scene[1] != scene[3]:
            scene_points_str = '%s/%s,%s/%s' % (scene[0].strftime(trend_proto.DEFAULT_TIME_FMT) if isinstance(scene[0], datetime.datetime) else scene[0],
                                                float(scene[1]),
                                                scene[2].strftime(trend_proto.DEFAULT_TIME_FMT) if isinstance(scene[2], datetime.datetime) else scene[2],
                                                float(scene[3]))
            cmd += '--scene=%s ' % scene_points_str

        # Выставить цену деления
        # cmd += '--dx=%s ' % self._dt2str(self._x_precision, self._x_format)
        # cmd += '--dy=%s ' % str(self._y_precision)

        if points is not None:
            points_lst = list()
            for point in points:
                points_lst.append('%s/%s' % (point[0].strftime(trend_proto.DEFAULT_TIME_FMT) if isinstance(point[0], datetime.datetime) else float(point[0]),
                                             float(point[1])))
            if points_lst:
                points_str = ','.join(points_lst)
                cmd += '--pen0=%s ' % points_str

        log.info(u'Запуск комманды: <%s>' % cmd)
        os.system(cmd)
        if os.path.exists(frame_filename):
            self.set_frame(frame_filename)
            return frame_filename
        else:
            log.warning(u'Файл кадра <%s> Nixplot тренда не найден' % frame_filename)
        return None

    def draw_empty(self, size=None):
        """
        Отрисовка пустого тренда.
        """
        if size is None:
            # size = self.canvas.GetSize()
            size = self.GetSize()
        log.debug(u'Отрисовка пустого тренда. Размер %s' % str(size))
        frame_filename = self.draw_frame(size=tuple(size))
        self.set_frame(frame_filename)

    def set_frame(self, frame_filename=None):
        """
        Установить кадр.
        @param frame_filename: Полное имя файла кадра.
        @return: True/False.
        """
        if frame_filename and os.path.exists(frame_filename) and frame_filename.endswith(PNG_FILE_TYPE.lower()):
            bmp = ic_bmp.createBitmap(frame_filename)
            self.canvas.SetBitmap(bmp)
            self.canvas.Refresh()
            return True
        return False

    def getPenData(self, pen_index=0):
        """
        Данные соответствующие перу.
        @param pen_index: Индекс пера. По умолчанию берется первое перо.
        @return: Список (Время, Значение)
        """
        pens = self.getPens()

        if pens and pen_index < len(pens):
            return pens[pen_index].getLineData()

        return list()

    def draw(self, redraw=True, size=None):
        """
        Основной метод отрисовки тренда.
        @param redraw: Принудительная прорисовка.
        @param size: Размер.
        """
        if size is None:
            size = self.GetSize()

        pens = self.getPens()

        if pens:
            self.setDefaults()

            # Признак не пустого тренда
            not_empty = False
            for pen in pens:
                try:
                    if pen:
                        line_data = pen.getLineData()
                        if line_data:
                            # rgb_str = pen.getColourStr()
                            if redraw:
                                self.draw_frame(size=size, points=line_data,
                                                scene=self._cur_scene)
                            not_empty = True
                        else:
                            log.warning(u'Пустые значения NixplotTrend <%s>' % self.name)
                            not_empty = not_empty or False

                    else:
                        log.warning(u'Не определено перо тренда <%s>' % self.name)
                        not_empty = False
                except:
                    log.fatal(u'Ошибка отрисовки тренда')
                    not_empty = False

            if not not_empty:
                # Если тренд пустой, то отрисовать пустой тренд
                self.draw_empty(size=size)
        else:
            # Если перья не определены то просто отобразить тренд
            self.draw_empty(size=size)

    def adaptScene(self, graph_data=None):
        """
        Адаптировать текущую сцену для отображения по данным графика.
        @param graph_data: Список точек графика.
            [(x1, y1), (x2, y2), ... (xN, yN)]
        @return: Текущая сцена тренда.
        """
        if graph_data is None:
            graph_data = self.getPenData(pen_index=0)

        if not graph_data:
            log.warning(u'Не определены данные графика для адаптации сцены для отображения тренда')
        else:
            time_data = [point[0] for point in graph_data]
            y_data = [point[1] for point in graph_data]
            min_timestamp = time.mktime(min(time_data).timetuple())
            max_timestamp = time.mktime(max(time_data).timetuple())
            x_precision_timestamp = self._x_precision.total_seconds() if isinstance(self._x_precision, datetime.timedelta) else time.mktime(self._x_precision.timetuple())
            min_y = min(y_data)
            max_y = max(y_data)

            scene_min_time = datetime.datetime.fromtimestamp(int(min_timestamp / x_precision_timestamp) * x_precision_timestamp)
            scene_min_y = int(min_y / self._y_precision) * self._y_precision
            scene_max_time = datetime.datetime.fromtimestamp((int(max_timestamp / x_precision_timestamp) + 1) * x_precision_timestamp)
            scene_max_y = (int(max_y / self._y_precision) + 1) * self._y_precision

            # ВНИМАНИЕ! Тренд позволяет просматривать данные только в пределах суток
            # Поэтому мы ограничиваем максимальное значение временной шкалы
            limit_scene_time_max = scene_min_time.replace(hour=23, minute=59, second=59)
            if scene_max_time > limit_scene_time_max:
                scene_max_time = limit_scene_time_max

            log.debug(u'Адаптация сцены:')
            log.debug(u'\tmin data x: %s' % min(time_data))
            log.debug(u'\tmin data y: %s' % min_y)
            log.debug(u'\tmax data x: %s' % max(time_data))
            log.debug(u'\tmax data y: %s' % max_y)
            log.debug(u'\ttime precision: %s' % str(self._x_precision))
            log.debug(u'\ty precision: %s' % str(self._y_precision))
            log.debug(u'\tmin time: %s' % str(scene_min_time))
            log.debug(u'\tmin y: %s' % str(scene_min_y))
            log.debug(u'\tmax time: %s' % str(scene_max_time))
            log.debug(u'\tmax y: %s' % str(scene_max_y))

            self._cur_scene = (scene_min_time, scene_min_y, scene_max_time, scene_max_y)

        return self._cur_scene

    def zoomX(self, step=1, redraw=True):
        """
        Увеличить цену деления оси X в соответствии со шкалой настройки.
        @param step: Шаг по шкале настройки
            >0 - увеличение
            <0 - уменьшение
        @param redraw: Произвести перерисовку кадра тренда?
        @return: True/False.
        """
        try:
            prev_idx = self._x_tunes.index(self._x_precision)
        except:
            log.fatal(u'Ошибка определения цены деления <%s> на шкале настройки' % str(self._x_precision))
            prev_idx = 0
        next_idx = min(len(self._x_tunes), max(0, prev_idx + step))
        self._x_precision = self._x_tunes[next_idx]

        if redraw:
            self.draw(redraw=redraw)
        return True

    def zoomY(self, step=1, redraw=True):
        """
        Увеличить цену деления оси Y в соответствии со шкалой настройки.
        @param step: Шаг по шкале настройки
            >0 - увеличение
            <0 - уменьшение
        @param redraw: Произвести перерисовку кадра тренда?
        @return: True/False.
        """
        try:
            prev_idx = self._y_tunes.index(self._y_precision)
        except:
            log.fatal(u'Ошибка определения цены деления <%s> на шкале настройки' % str(self._y_precision))
            prev_idx = 0
        next_idx = min(len(self._y_tunes), max(0, prev_idx + step))
        self._y_precision = self._y_tunes[next_idx]

        if redraw:
            self.draw(redraw=redraw)
        return True

    def moveSceneX(self, step=1, redraw=True):
        """
        Передвижение сцены по оси X на указанное количество цены деления.
        @param step: Количество цен деления для передвижения
            >0 - увеличение
            <0 - уменьшение
        @param redraw: Произвести перерисовку кадра тренда?
        @return: True/False.
        """
        self._cur_scene = (self._cur_scene[0] + step*self._x_precision,
                           self._cur_scene[1],
                           self._cur_scene[2] + step * self._x_precision,
                           self._cur_scene[3])

        if redraw:
            self.draw(redraw=redraw)
        return True

    def moveSceneY(self, step=1, redraw=True):
        """
        Передвижение сцены по оси Y на указанное количество цены деления.
        @param step: Количество цен деления для передвижения
            >0 - увеличение
            <0 - уменьшение
        @param redraw: Произвести перерисовку кадра тренда?
        @return: True/False.
        """
        self._cur_scene = (self._cur_scene[0],
                           self._cur_scene[1] + step*self._y_precision,
                           self._cur_scene[2],
                           self._cur_scene[3] + step * self._y_precision)

        if redraw:
            self.draw(redraw=redraw)
        return True


def test():
    """
    Тестовая функция.
    """
    from ic import config

    log.init(config)

    app = wx.PySimpleApp()
    frame = wx.Frame(None, title='My Data')
    panel = icNixplotTrendProto(frame)
    panel.draw()
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
