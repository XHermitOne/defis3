#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Компонент временного графика. Тренд.
Компонент реализован на утилите nixplot.
"""

import os.path
import wx
import datetime

from ic.PropertyEditor import icDefInf
from ic.components import icwidget
from ic.components import icResourceParser as prs

from ic.log import log
from ic.utils import util
from ic.bitmap import ic_bmp
from ic.utils import ic_time
from ic.utils import ic_file


# --- Спецификация ---
# Папка размещения кадров трендов
DEFAULT_NIXPLOT_FRAME_PATH = os.path.join(ic_file.getProfilePath(), 'nixplot')

# Форматы используемые для отображения временной шкалы
DEFAULT_TIME_FMT = '%H:%M:%S'
DEFAULT_DATE_FMT = '%d.%m.%Y'
DEFAULT_DATETIME_FMT = '%d.%m.%Y-%H:%M:%S'
DEFAULT_FORMATS = (DEFAULT_TIME_FMT,
                   DEFAULT_DATETIME_FMT,
                   DEFAULT_DATE_FMT)

# Минимальные размеры кадра
MIN_FRAME_WIDTH = 640
MIN_FRAME_HEIGHT = 480

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

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icNixplotTrend'

#   Описание стилей компонента
ic_class_styles = 0

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'NixplotTrend',
                'name': 'default',
                'child': [],
                'activate': True,
                '_uuid': None,

                '__styles__': ic_class_styles,
                '__events__': {},
                '__lists__': {'time_axis_fmt': list(DEFAULT_FORMATS)},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid',
                                                            ],
                                   },
                '__parent__': SPC_IC_NIXPLOT_TREND,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('diagramm.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('diagramm.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['TrendPen']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 2)


class icNixplotTrendProto(wx.Panel):
    """
    Базовый класс временного графика. Тренд.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        wx.Panel.__init__(self, *args, **kwargs)

        self.canvas = wx.StaticBitmap(self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
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

    # Словарь замены форматов шкал
    _Fmt2NixplotType = {'numeric': 'N',
                        'time': 'T',
                        'date': 'D',
                        'datetime': 'DT',
                        'exponent': 'E'}

    def _draw_frame(self, size=(0, 0), x_format='time', y_format='numeric', scene=None,
                    points=None):
        """
        Отрисовка кадра данных тренда.
        @param size: Размер кадра в точках.
        @param x_format: Формат шкалы X.
        @param y_format: Формат шкалы Y.
        @param scene: Границы окна сцены в данных предметной области.
        @param points: Список точек графика.
        @return: Имя файла отрисованного кадра или None в случае ошибки.
        """
        cmd = 'nixplot --PNG '
        obj_uuid = self.GetUUID() if hasattr(self, 'GetUUID') else 'frame'
        frame_filename = os.path.join(DEFAULT_NIXPLOT_FRAME_PATH, obj_uuid + '.png')

        if os.path.exists(frame_filename):
            try:
                os.remove(frame_filename)
                log.info(u'Удален файл кадра <%s>' % frame_filename)
            except OSError:
                log.warning(u'Ошибка удаления файла кадра <%s>' % frame_filename)
                return None

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
                scene_points_str = '%s/%s,%s/%s' % (DEFAULT_TIME_FMT % scene[0] if isinstance(scene[0], datetime.datetime) else float(scene[0]),
                                                    float(scene[1]),
                                                    DEFAULT_TIME_FMT % scene[2] if isinstance(scene[2], datetime.datetime) else float(scene[2]),
                                                    float(scene[3]))
                cmd += '--scene=%s ' % scene_points_str

        if points is not None:
            points_lst = list()
            for point in points:
                points_lst.append('%s/%s' % (DEFAULT_TIME_FMT % point[0] if isinstance(point[0], datetime.datetime) else float(point[0]),
                                             float(point[1])))
            if points_lst:
                points_str = ','.join(points_lst)
                cmd += '--pen0=%s ' % points_str

        log.info(u'Запуск комманды: <%s>' % cmd)
        os.system(cmd)
        if os.path.exists(frame_filename):
            return frame_filename
        else:
            log.warning(u'Файл кадра <%s> Nixplot тренда не найден' % frame_filename)
        return None

    def _draw_empty(self):
        """
        Отрисовка пустого тренда.
        """
        frame_filename = self._draw_frame(size=tuple(self.canvas.GetSize()))
        if frame_filename:
            bmp = ic_bmp.createBitmap(frame_filename)
            self.canvas.SetBitmap(bmp)
            self.canvas.Refresh()

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

    def draw(self, redraw=True):
        """
        Основной метод отрисовки тренда.
        @param redraw: Принудительная прорисовка.
        """
        pens = self.getPens()

        if pens:
            self.setDefaults()

            # Признак не пустого тренда
            not_empty = False
            for pen in pens:
                if pen:
                    line_data = pen.getLineData()
                    if line_data:
                        time_data = [point[0] for point in line_data]
                        time_float = matplotlib.dates.date2num(time_data)
                        y_data = [point[1] for point in line_data]
                        rgb_str = pen.getColourStr()

                        self.axes.plot(time_float, y_data, color=rgb_str)
                        if redraw:
                            self.figure.canvas.draw()
                        not_empty = True
                    else:
                        log.warning(u'Пустые значения NixplotTrend <%s>' % self.name)
                        not_empty = not_empty or False
                else:
                    log.warning(u'Не определено перо тренда <%s>' % self.name)
                    not_empty = False

            if not not_empty:
                # Если тренд пустой, то отрисовать пустой тренд
                self._draw_empty()
        else:
            # Если перья не определены то просто отобразить тренд
            self._draw_empty()

    def getPens(self):
        """
        Список перьев тренда.
        """
        return list()


class icNixplotTrend(icwidget.icWidget, icNixplotTrendProto):
    """
    Компонент временного графика. Тренд.
    Компонент реализован на утилите nixplot.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.

        - B{type='defaultType'}:
        - B{name='default'}:

    """
    component_spc = ic_class_spc

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор базового класса пользовательских компонентов.

        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type id: C{int}
        @param id: Идентификатор окна.
        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        @type bCounter: C{bool}
        @param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        @type progressDlg: C{wx.ProgressDialog}
        @param progressDlg: Указатель на идикатор создания формы.
        """
        component = util.icSpcDefStruct(self.component_spc, component, True)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if not x.startswith('__')]

        for key in lst_keys:
            setattr(self, key, component[key])

        #   !!! Конструктор наследуемого класса !!!
        #   Необходимо вставить реальные параметры конструкора.
        #   На этапе генерации их не всегда можно определить.
        icNixplotTrendProto.__init__(self, parent)

        #   Создаем дочерние компоненты
        self.childCreator(bCounter, progressDlg)

        self.draw()

    def childCreator(self, bCounter=False, progressDlg=None):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        return prs.icResourceParser(self, self.child, None, evalSpace=self.evalSpace,
                                    bCounter=bCounter, progressDlg=progressDlg)

    def getPens(self):
        """
        Список перьев тренда.
        """
        pens = self.get_children_lst()
        if not pens:
            log.warning(u'Не определены перья тренда <%s>' % self.name)
        return pens


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
