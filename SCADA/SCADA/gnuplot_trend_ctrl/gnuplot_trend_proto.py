#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Компонент временного графика. Тренд.
Абстрактный класс.
Компонент реализован на базе утилиты gnuplot.
"""

import os.path
import wx
import datetime
import time
import uuid

from ic.log import log
from ic.utils import ic_file
from ic.utils import ic_time
from ic.bitmap import bmpfunc

from ic.components import icwidget
from . import gnuplot_manager

from SCADA.scada_proto import trend_proto

# Полное имя файла утилиты gnuplot
GNUPLOT_FILENAME = 'gnuplot'

# Папка размещения кадров трендов
DEFAULT_GNUPLOT_FRAME_PATH = os.path.join(ic_file.getProfilePath(), 'gnuplot')

# Минимальные размеры кадра
MIN_FRAME_WIDTH = 640
MIN_FRAME_HEIGHT = 480

# Типы файлов кадра
PNG_FILE_TYPE = 'PNG'
PDF_FILE_TYPE = 'PDF'

DATA_FILE_EXT = '.dat'

# Цена деления по умолчанию
DEFAULT_X_PRECISION = '01:00:00'
DEFAULT_Y_PRECISION = '1.0'

# --- Спецификация ---
SPC_IC_GNUPLOT_TREND = {'x_format': trend_proto.DEFAULT_X_FORMAT,   # Формат представления данных оси X
                        'y_format': trend_proto.DEFAULT_Y_FORMAT,   # Формат представления данных оси Y
                        'scene_min': ('00:00:00', 0.0),    # Минимальное значение видимой сцены тренда
                        'scene_max': ('12:00:00', 0.0),    # Максимальное значение видимой сцены тренда
                        'x_precision': DEFAULT_X_PRECISION,     # Цена деления сетки тренда по шкале X
                        'y_precision': DEFAULT_Y_PRECISION,     # Цена деления сетки тренда по шкале Y

                        '__parent__': icwidget.SPC_IC_WIDGET,
                        '__attr_hlp__': {'x_format': u'Формат представления данных оси X',
                                         'y_format': u'Формат представления данных оси Y',
                                         'scene_min': u'Минимальное значение видимой сцены тренда',
                                         'scene_max': u'Максимальное значение видимой сцены тренда',
                                         'x_precision': u'Цена деления сетки тренда по шкале X',
                                         'y_precision': u'Цена деления сетки тренда по шкале Y',
                                         },
                        }

# Версия
__version__ = (0, 1, 2, 1)


class icGnuplotTrendProto(wx.Panel, trend_proto.icTrendProto):
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

        # Цена деления
        self._x_precision = DEFAULT_X_PRECISION
        self._y_precision = DEFAULT_Y_PRECISION
        # Формат шкал
        self._x_format = trend_proto.DEFAULT_X_FORMAT
        self._y_format = trend_proto.DEFAULT_Y_FORMAT

        # Менеджер утилиты gnuplot
        self.__gnuplot_manager = gnuplot_manager.icGnuplotManager()
        self.__gnuplot_manager.enableGrid()
        self.__gnuplot_manager.enableLegend(False)
        self.__gnuplot_manager.enableXTime()
        self.__gnuplot_manager.enableXTextVertical()

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

    def setStartDT(self, new_dt):
        """
        Начальная дата-время тренда.
        @param new_dt: Новое значение.
        """
        self.start_datetime = self._convertDate(new_dt)
        self.setScene(min_x=self.start_datetime)

    def setStopDT(self, new_dt):
        """
        Конечная дата-время тренда.
        @param new_dt: Новое значение.
        """
        self.stop_datetime = self._convertDate(new_dt)
        self.setScene(max_x=self.stop_datetime)

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
        frame_filename = self.getFrameFileName(PNG_FILE_TYPE)
        self.del_frame(frame_filename)
        frame_filename = self.getFrameFileName(PDF_FILE_TYPE)
        self.del_frame(frame_filename)
        dat_filename = os.path.splitext(frame_filename)[0] + DATA_FILE_EXT
        ic_file.removeFile(dat_filename)
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
            self.__frame_filename = os.path.join(DEFAULT_GNUPLOT_FRAME_PATH, obj_uuid + file_ext)
        return self.__frame_filename

    def getCurScene(self):
        """
        Текущая сцена тренда - Границы окна сцены в данных предметной области.
        Представляется в виде кортежа (X1, Y1, X2, Y2)
        """
        return self._cur_scene

    def setDefaults(self):
        """
        Установить параметры по умолчанию.
        """
        if not os.path.exists(DEFAULT_GNUPLOT_FRAME_PATH):
            try:
                os.makedirs(DEFAULT_GNUPLOT_FRAME_PATH)
                log.info(u'Создана папка <%s>' % DEFAULT_GNUPLOT_FRAME_PATH)
            except:
                log.warning(u'Ошибка создания папки <%s>' % DEFAULT_GNUPLOT_FRAME_PATH)

    def del_frame(self, frame_filename=None):
        """
        Удалить файл кадра
        @param frame_filename: Имя файла кадра тренда.
        @return: True/False.
        """
        if frame_filename is None:
            frame_filename = self.getFrameFileName()

        return ic_file.removeFile(frame_filename)

    # Словарь замены форматов шкал
    _Fmt2GnuplotType = {'numeric': 'N',
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
        frame_filename = self.getFrameFileName(file_type)
        graph_filename = os.path.splitext(frame_filename)[0] + DATA_FILE_EXT
        # log.debug(u'Файл кадра: %s' % frame_filename)
        self.del_frame(frame_filename)

        dt_format = self._get_dt_format(x_format)
        self.__gnuplot_manager.setTimeFormat()
        self.__gnuplot_manager.setXFormat(dt_format)

        # Выставить сцену
        if scene is None:
            scene = self._cur_scene

        if scene[0] != scene[2] and scene[1] != scene[3]:
            self.__gnuplot_manager.setXRange(self._dt2str(scene[0], gnuplot_manager.DATETIME_GRAPH_DATA_FMT),
                                             self._dt2str(scene[2], gnuplot_manager.DATETIME_GRAPH_DATA_FMT))
            self.__gnuplot_manager.setYRange(float(scene[1]), float(scene[3]))

        if file_type == PNG_FILE_TYPE:
            self.__gnuplot_manager.setOutputPNG(background_color='black')
            self.__gnuplot_manager.setBorderColour('#A9A9A9')  # darkgray
            self.__gnuplot_manager.setGridColour('#A9A9A9')  # darkgray
            self.__gnuplot_manager.setXTextColour('#008B8B')  # darkcyan
            self.__gnuplot_manager.setYTextColour('#008B8B')  # darkcyan
        else:
            self.__gnuplot_manager.setOutputPDF()
            self.__gnuplot_manager.setBorderColour('black')
            self.__gnuplot_manager.setGridColour('black')
            self.__gnuplot_manager.setXTextColour('black')
            self.__gnuplot_manager.setYTextColour('black')
        self.__gnuplot_manager.setOutputFilename(frame_filename)

        if size is not None:
            width, height = size
            width = max(width, MIN_FRAME_WIDTH)
            height = max(height, MIN_FRAME_HEIGHT)
            if width > 0 and height > 0:
                if file_type == PNG_FILE_TYPE:
                    self.__gnuplot_manager.setOutputSizePNG(width, height)
                # else:
                #     self.__gnuplot_manager.setOutputSizePDF(width, height)

        if points is not None:
            points_lst = [dict(x=point[0] if isinstance(point[0], datetime.datetime) else float(point[0]),
                               point1=float(point[1])) for point in points]
            self.__gnuplot_manager.saveGraphData(graph_filename, points_lst, ('point1',))

        self.__gnuplot_manager.setPlot(graph_filename, 1)
        self.__gnuplot_manager.gen()

        if os.path.exists(frame_filename):
            return frame_filename
        else:
            log.warning(u'Файл кадра <%s> Gnuplot тренда не найден' % frame_filename)
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
        if frame_filename is None:
            frame_filename = self.getFrameFileName()

        if frame_filename and os.path.exists(frame_filename) and frame_filename.endswith(PNG_FILE_TYPE.lower()):
            bmp = bmpfunc.createBitmap(frame_filename)
            self.canvas.SetBitmap(bmp)
            self.canvas.Refresh()
            return True
        return False

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
                            self.set_frame()
                            not_empty = True
                        else:
                            log.warning(u'Пустые значения GnuplotTrend <%s>' % self.name)
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

            # log.debug(u'Адаптация сцены:')
            # log.debug(u'\tdata x: %s' % str(time_data))
            # log.debug(u'\tdata y: %s' % str(y_data))
            # log.debug(u'\tmin_value data x: %s' % min_value(time_data))
            # log.debug(u'\tmin data y: %s' % min_y)
            # log.debug(u'\tmax_value data x: %s' % max_value(time_data))
            # log.debug(u'\tmax data y: %s' % max_y)
            # log.debug(u'\ttime precision: %s' % str(self._x_precision))
            # log.debug(u'\ty precision: %s' % str(self._y_precision))
            # log.debug(u'\tmin time: %s' % str(scene_min_time))
            # log.debug(u'\tmin y: %s' % str(scene_min_y))
            # log.debug(u'\tmax time: %s' % str(scene_max_time))
            # log.debug(u'\tmax y: %s' % str(scene_max_y))

            self._cur_scene = (scene_min_time, scene_min_y, scene_max_time, scene_max_y)

            self.setStartDT(scene_min_time)
            self.setStopDT(scene_min_time)

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
        self._cur_scene = (self._cur_scene[0],
                           self._cur_scene[1],
                           max(self._cur_scene[2] + step * self._x_precision,
                               self._cur_scene[0] + self._x_precision),
                           self._cur_scene[3])

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
        self._cur_scene = (self._cur_scene[0],
                           self._cur_scene[1],
                           self._cur_scene[2],
                           max(self._cur_scene[3] + step * self._y_precision, self._y_precision))

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
        self._cur_scene = (self._cur_scene[0] + step * self._x_precision,
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
                           self._cur_scene[1] + step * self._y_precision,
                           self._cur_scene[2],
                           self._cur_scene[3] + step * self._y_precision)

        if redraw:
            self.draw(redraw=redraw)
        return True

    def moveSceneFirst(self, redraw=True):
        """
        Передвижение сцены по оси X на первое значение тренда.
        @param redraw: Произвести перерисовку кадра тренда?
        @return: True/False.
        """
        time_width = self._cur_scene[2] - self._cur_scene[0]
        graph_data = self.getPenData(pen_index=0)

        time_data = [point[0] for point in graph_data]
        min_timestamp = time.mktime(min(time_data).timetuple())
        x_precision_timestamp = self._x_precision.total_seconds() if isinstance(self._x_precision,
                                                                                datetime.timedelta) else time.mktime(self._x_precision.timetuple())

        scene_min_time = datetime.datetime.fromtimestamp(
            int(min_timestamp / x_precision_timestamp) * x_precision_timestamp)

        self._cur_scene = (scene_min_time,
                           self._cur_scene[1],
                           scene_min_time + time_width,
                           self._cur_scene[3])

        if redraw:
            self.draw(redraw=redraw)
        return True

    def moveSceneLast(self, redraw=True):
        """
        Передвижение сцены по оси Y на указанное количество цены деления.
        @param redraw: Произвести перерисовку кадра тренда?
        @return: True/False.
        """
        time_width = self._cur_scene[2] - self._cur_scene[0]
        graph_data = self.getPenData(pen_index=0)

        time_data = [point[0] for point in graph_data]
        max_timestamp = time.mktime(max(time_data).timetuple())
        x_precision_timestamp = self._x_precision.total_seconds() if isinstance(self._x_precision,
                                                                                datetime.timedelta) else time.mktime(self._x_precision.timetuple())
        scene_max_time = datetime.datetime.fromtimestamp(
            (int(max_timestamp / x_precision_timestamp) + 1) * x_precision_timestamp)

        self._cur_scene = (scene_max_time - time_width,
                           self._cur_scene[1],
                           scene_max_time,
                           self._cur_scene[3])

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
    panel = icGnuplotTrendProto(frame)
    panel.draw()
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
