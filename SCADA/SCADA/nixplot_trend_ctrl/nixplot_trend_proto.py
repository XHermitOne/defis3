#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Компонент временного графика. Тренд.
Абстрактный класс.
Компонент реализован на базе утилиты nixplot.
"""

import os.path
import wx
import datetime
import uuid

from ic.log import log
from ic.utils import ic_file
from ic.utils import ic_time
from ic.bitmap import ic_bmp

from ic.components import icwidget

# Полное имя файла утилиты nixplot
PACKAGE_PATH = os.path.dirname(__file__) if os.path.dirname(__file__) else '.'
NIXPLOT_FILENAME = os.path.join(PACKAGE_PATH, 'nixplot')

# Папка размещения кадров трендов
DEFAULT_NIXPLOT_FRAME_PATH = os.path.join(ic_file.getProfilePath(), 'nixplot')

# Форматы используемые для отображения временной шкалы
DEFAULT_TIME_FMT = '%H:%M:%S'
DEFAULT_DATE_FMT = '%d.%m.%Y'
DEFAULT_DATETIME_FMT = '%d.%m.%Y-%H:%M:%S'

# Минимальные размеры кадра
MIN_FRAME_WIDTH = 640
MIN_FRAME_HEIGHT = 480

# Типы файлов кадра
PNG_FILE_TYPE = 'PNG'
PDF_FILE_TYPE = 'PDF'

# --- Спецификация ---
SPC_IC_NIXPLOT_TREND = {'x_format': 'time',     # Формат представления данных оси X
                        'y_format': 'numeric',  # Формат представления данных оси Y
                        'scene_min': (0.0, 0.0),    # Минимальное значение видимой сцены тренда
                        'scene_max': (0.0, 0.0),    # Максимальное значение видимой сцены тренда
                        '__parent__': icwidget.SPC_IC_WIDGET,
                        '__attr_hlp__': {'x_format': u'Формат представления данных оси X',
                                         'y_format': u'Формат представления данных оси Y',
                                         'scene_min': u'Минимальное значение видимой сцены тренда',
                                         'scene_max': u'Максимальное значение видимой сцены тренда',
                                         },
                        }

# Версия
__version__ = (0, 1, 1, 1)


class icNixplotTrendProto(wx.Panel):
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

        self.start_datetime = None
        self.stop_datetime = None
        today = datetime.date.today()
        self.start_datetime = datetime.datetime.combine(today,
                                                        datetime.datetime.min.time())
        self.stop_datetime = datetime.datetime.combine(today+datetime.timedelta(days=1),
                                                       datetime.datetime.min.time())

        self.setDefaults()

        # Текущая сцена тренда - Границы окна сцены в данных предметной области.
        # Представляется в виде кортежа (X1, Y1, X2, Y2)
        self._cur_scene = None

        # ВНИМАНИЕ! Если необходимо удалить/освободить
        # ресуры при удалении контрола, то необходимо воспользоваться
        # событием wx.EVT_WINDOW_DESTROY
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)

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

        if scene is not None:
            if scene[0] != scene[2] and scene[1] != scene[3]:
                scene_points_str = '%s/%s,%s/%s' % (scene[0].strftime(DEFAULT_TIME_FMT) if isinstance(scene[0], datetime.datetime) else float(scene[0]),
                                                    float(scene[1]),
                                                    scene[2].strftime(DEFAULT_TIME_FMT) if isinstance(scene[2], datetime.datetime) else float(scene[2]),
                                                    float(scene[3]))
                cmd += '--scene=%s ' % scene_points_str

        if points is not None:
            points_lst = list()
            for point in points:
                points_lst.append('%s/%s' % (point[0].strftime(DEFAULT_TIME_FMT) if isinstance(point[0], datetime.datetime) else float(point[0]),
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
                            time_data = [point[0] for point in line_data]
                            y_data = [point[1] for point in line_data]
                            if redraw:
                                self._cur_scene = (min(time_data), min(y_data),
                                                   max(time_data), max(y_data))
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

    def getPens(self):
        """
        Список перьев тренда.
        """
        log.warning(u'Не определен метод получения перьев')
        return list()


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
