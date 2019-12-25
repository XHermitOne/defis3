#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Объект, секторного индикатора/Спидометра.

:type ic_user_name: C{string}
:var ic_user_name: Имя пользовательского класса.
:type ic_can_contain: C{list | int}
:var ic_can_contain: Разрешающее правило - список типов компонентов, которые
    могут содержаться в данном компоненте. -1 - означает, что любой компонент
    может содержатся в данном компоненте. Вместе с переменной ic_can_not_contain
    задает полное правило по которому определяется возможность добавления других
    компонентов в данный комопнент.
:type ic_can_not_contain: C{list}
:var ic_can_not_contain: Запрещающее правило - список типов компонентов,
    которые не могут содержаться в данном компоненте. Запрещающее правило
    начинает работать если разрешающее правило разрешает добавлять любой
    компонент (ic_can_contain = -1).
    
:type ICSpeedmeterStyle: C{dictionary}
:var ICSpeedmeterStyle: Словарь специальных стилей компонента.
Описание ключей ICSpeedmeterStyle:

    - C{SM_ROTATE_TEXT): Отрисовка текста шкалы перпендикулярно радиусу.
    - C{SM_DRAW_SECTORS): Отрисовка полного круга поля.
    - C{SM_DRAW_PARTIAL_SECTORS): Отрисовка полосы по кругу поля.
    - C{SM_DRAW_HAND): Отрисовка стрелки.
    - C{SM_DRAW_SHADOW): Отрисовка тени стрелки.
    - C{SM_DRAW_PARTIAL_FILLER): Отрисовка следа за стрелкой.
    - C{SM_DRAW_SECONDARY_TICKS): Отрисовка минорной шкалы.
    - C{SM_DRAW_MIDDLE_TEXT): -.
    - C{SM_DRAW_MIDDLE_ICON): -.
    - C{SM_DRAW_GRADIENT): Градиентная заливка поля.
    - C{SM_DRAW_FANCY_TICKS): Отрисовка мажорной шкалы.
"""

import os.path
from math import pi     # Необходимо для расчета углов
import wx
from ic.components import icwidget
from ic.utils import util
from ic.PropertyEditor import icDefInf

from ic.log import log
from ic.utils import filefunc
from ic.components import icfont

import wx.lib.agw.speedmeter as parentModule
from ic.bitmap import bmpfunc

# --- Спецификация ---
ICSpeedmeterStyle = {'SM_ROTATE_TEXT': parentModule.SM_ROTATE_TEXT,
                     'SM_DRAW_SECTORS': parentModule.SM_DRAW_SECTORS,
                     'SM_DRAW_PARTIAL_SECTORS': parentModule.SM_DRAW_PARTIAL_SECTORS,
                     'SM_DRAW_HAND': parentModule.SM_DRAW_HAND,
                     'SM_DRAW_SHADOW': parentModule.SM_DRAW_SHADOW,
                     'SM_DRAW_PARTIAL_FILLER': parentModule.SM_DRAW_PARTIAL_FILLER,
                     'SM_DRAW_SECONDARY_TICKS': parentModule.SM_DRAW_SECONDARY_TICKS,
                     'SM_DRAW_MIDDLE_TEXT': parentModule.SM_DRAW_MIDDLE_TEXT,
                     'SM_DRAW_MIDDLE_ICON': parentModule.SM_DRAW_MIDDLE_ICON,
                     'SM_DRAW_GRADIENT': parentModule.SM_DRAW_GRADIENT,
                     'SM_DRAW_FANCY_TICKS': parentModule.SM_DRAW_FANCY_TICKS,
                     }


SPC_IC_SPEEDMETER = {'angle_range': [-45, 225],   # Указание сектора поля в градусах
                     'intervals': '[0, 1, 2, 3, 4]',   # Мажорная шкала в градусах,
                                                       # начиная с первой границы сектор поля
                     # Цвета секторов мажорной шкалы [wx.BLACK,....]
                     'interval_colors': '[wx.GREEN, wx.GREEN, wx.YELLOW, wx.RED]',
                     'ticks': "['0', '25', '50', '75', '100']",   # Надписи мажорной шкалы
                     'ticks_color': (0, 0, 0),    # Цвет шкалы
                     'second_ticks_count': 5,   # Количество штрихов минорной шкалы
                                                # внутри 1 деления мажорной шкалы
                     'ticks_font': None,    # Шрифт шкалы
                     'middle_txt': 'XXX',  # Текст в середине поля
                     'middle_txt_color': None,   # Цвет текста в середине поля
                     'middle_txt_font': None,   # Шрифт текста в центре поля
                     'middle_icon': None,   # Иконка в центре поля
                     'background': None,   # Цвет фона
                     'hand_color': (255, 0, 0),     # Цвет стрелки
                     'hand_style': 'Hand',  # Стиль стрелки
                     'shadow_color': None,  # Цвет тени
                     'external_arc': False,  # Делать окантовку поля?
                     'arc_color': None,     # Цвет окантовки
                     'direction': 'Advance',  # Напровление движения стрелки
                     'filler_color': (0, 96, 0),  # Цвет следа
                     'first_gradient_color': None,   # Первый цвет градиентной заливки
                     'second_gradient_color': None,  # Второй цвет градиентной заливки
                     'value': 0,    # Значение
                     '__parent__': icwidget.SPC_IC_WIDGET,
                     }

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icSpeedmeter'

#   Описание стилей компонента
ic_class_styles = ICSpeedmeterStyle

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'Speedmeter',
                'name': 'default',
                'child': [],
                'activate': True,
                '_uuid': None,
                'style': parentModule.SM_DRAW_HAND |
                         parentModule.SM_DRAW_PARTIAL_SECTORS |
                         parentModule.SM_DRAW_SECONDARY_TICKS |
                         parentModule.SM_DRAW_MIDDLE_TEXT |
                         parentModule.SM_ROTATE_TEXT,

                '__styles__': ic_class_styles,
                '__events__': {},
                '__lists__': {'hand_style': ['Hand', 'Arrow'],
                              'direction': ['Advance', 'Reverse']},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid',
                                                            'middle_txt'],
                                   icDefInf.EDT_COLOR: ['ticks_color', 'hand_color',
                                                        'middle_txt_color', 'background',
                                                        'shadow_color', 'arc_color', 'filler_color',
                                                        'first_gradient_color',
                                                        'second_gradient_color'],
                                   icDefInf.EDT_FONT: ['ticks_font', 'middle_txt_font'],
                                   icDefInf.EDT_TEXTLIST: ['angle_range'],
                                   icDefInf.EDT_NUMBER: ['second_ticks_count',
                                                         'value'],
                                   icDefInf.EDT_CHOICE: ['hand_style', 'direction'],
                                   icDefInf.EDT_CHECK_BOX: ['external_arc'],
                                   },
                '__parent__': SPC_IC_SPEEDMETER,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('dashboard.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('dashboard.png')

#   Путь до файла документации
ic_class_doc = 'SCADA/doc/_build/html/SCADA.usercomponents.speedmeter.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 3)


class icSpeedmeter(icwidget.icWidget, parentModule.SpeedMeter):
    """
    Объект, секторного индикатора/Спидометра..

    :type component_spc: C{dictionary}
    :cvar component_spc: Спецификация компонента.
        
        - B{type='defaultType'}:
        - B{name='default'}:

    """
    component_spc = ic_class_spc
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор базового класса пользовательских компонентов.

        :type parent: C{wx.Window}
        :param parent: Указатель на родительское окно.
        :type id: C{int}
        :param id: Идентификатор окна.
        :type component: C{dictionary}
        :param component: Словарь описания компонента.
        :type logType: C{int}
        :param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        :param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        :type evalSpace: C{dictionary}
        :type bCounter: C{bool}
        :param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        :type progressDlg: C{wx.ProgressDialog}
        :param progressDlg: Указатель на идикатор создания формы.
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
        parentModule.SpeedMeter.__init__(self, parent,
                                         pos=self.getPos(),
                                         size=self.getSize(),
                                         agwStyle=self.getStyle())
        # Установка свойств
        self.setDefault()
        
        #   Регистрация обработчиков событий
        # self.BindICEvt()
            
    def getPos(self):
        """
        Позиция.
        """
        x, y = self.getICAttr('position')
        return wx.Point(x, y)
        
    def getSize(self):
        """
        Размер компонента.
        """
        width, height = self.getICAttr('size')
        return wx.Size(width, height)

    def getStyle(self):
        """
        Стиль.
        """
        return self.getICAttr('style')
    
    def get_intervals(self):
        """
        Мажорная шкала в градусах.
        """
        self.evalSpace['self'] = self
        intervals = self.eval_attr('intervals')[1]
        log.debug(u'Speedmeter. Intervals <%s>' % intervals)
        if intervals is None:
            intervals = list()
        return intervals   
        
    def get_interval_colors(self):
        """
        Цвета секторов мажорной шкалы.
        """
        self.evalSpace['self'] = self
        interval_colors = self.eval_attr('interval_colors')[1]
        log.debug(u'Speedmeter. Interval colors <%s>' % interval_colors)
        if interval_colors is None:
            interval_colors = list()
        return interval_colors
        
    def get_ticks(self):
        """
        Надписи мажорной шкалы.
        """
        self.evalSpace['self'] = self
        ticks = self.eval_attr('ticks')[1]
        if ticks is None:
            ticks = list()
        return ticks
        
    def setDefault(self):
        """
        Установить все значения о умолчанию.
        """
        # ВНИМАНИЕ! Этот размер необходимо указывать т.к.
        # шкала контрола прорисовывается в зависимости от ClientSize
        self.SetClientSize(self.getSize())

        angle_range = self.angle_range
        if angle_range:
            self.setAngleRange(angle_range[0], angle_range[1])

        self.setIntervals(self.get_intervals())
        self.setIntervalColors(self.get_interval_colors())
        
        self.setTicks(self.get_ticks())
        self.setTicksColor(self.ticks_color)
        self.setTicksFont(self.ticks_font)
        self.setSecondTicksCount(self.second_ticks_count)
        
        self.setMiddleTxt(self.middle_txt)
        self.setMiddleTxtColor(self.middle_txt_color)
        self.setMiddleTxtFont(self.middle_txt_font)
        self.setMiddleIcon(self.middle_icon)
        
        self.setHandColor(self.hand_color)
        self.setHandStyle(self.hand_style)
        
        self.setBackgroundColor(self.background)
        
        self.setExternalArc(self.external_arc)
        self.setArcColor(self.arc_color)
        
        self.setShadowColor(self.shadow_color)
        self.setFillerColor(self.filler_color)
        
        self.setFirstGradientColor(self.first_gradient_color)
        self.setSecondGradientColor(self.second_gradient_color)

        self.setDirection(self.direction)
        
        self.setValue(self.value)
        
    def setAngleRange(self, start_degree, end_degree):
        """
        Установить сектор поля.

        :param start_degree: Начальная граница сектора в градусах.
        :param end_degree: Конечная граница в градусах.
        """
        # Перевод в радианы
        start_rad = (float(start_degree) * pi) / 180.0
        end_rad = (float(end_degree) * pi) / 180.0
        return self.SetAngleRange(start_rad, end_rad)
        
    def setIntervals(self, intervals):
        """
        Установка мажорной шкалы в градусах.
        """
        if intervals:
            # intervals = map(lambda interval: (float(interval)*pi)/180,list(intervals))
            # intervals = [(float(interval)*pi) / 180.0 for interval in list(intervals)]
            # intervals = intervals
            return self.SetIntervals(intervals)
        
    def setIntervalColors(self, interval_colors):
        """
        Установка цветов секторов мажорной шкалы.
        """
        if interval_colors:
            self.SetIntervalColours(interval_colors)

    def setTicks(self, ticks):
        """
        Надписи мажорной шкалы.
        """
        if ticks:
            # ticks=map(lambda tick: str(tick),ticks)
            str_ticks = [str(tick) for tick in ticks]
            self.SetTicks(str_ticks)
            
    def setTicksColor(self, colour):
        """
        Цвет шкалы.
        """
        if colour:
            wx_colour = wx.Colour(*colour)
            self.SetTicksColour(wx_colour)

    def setTicksFont(self, font):
        """
        Шрифт текста мажорной шкалы.
        """
        if font:
            fnt = icfont.icFont(font)
            self.SetTicksFont(fnt)
        
    def setSecondTicksCount(self, ticks_count):
        """
        Установить количество штрихов минорной шкалы внутри одного деления мажорной.
        """
        int_ticks_count = int(ticks_count)
        if int_ticks_count >= 0:
            self.SetNumberOfSecondaryTicks(int_ticks_count)

    def setMiddleTxt(self, text):
        """
        Текст в центре поля.
        """
        if text is not None:
            self.SetMiddleText(str(text))
            
    def setMiddleTxtColor(self, colour):
        """
        Цвет текста в центре поля.
        """
        if colour:
            wx_colour = wx.Colour(*colour)
            self.SetMiddleTextColour(wx_colour)
            
    def setMiddleTxtFont(self, font):
        """
        Шрифт текста в центре поля.
        """
        if font:
            fnt = icfont.icFont(font)
            self.SetMiddleTextFont(fnt)
            
    def setMiddleIcon(self, ico_filename):
        """
        Иконка в центре поля.

        :param ico_filename: Имя файла *.ico.
        """
        if ico_filename:
            ico_file_name = filefunc.get_absolute_path(ico_filename)
            if os.path.exists(ico_file_name):
                icon = wx.Icon(ico_file_name, wx.BITMAP_TYPE_ICO)
                icon.SetWidth(24)
                icon.SetHeight(24)
                if icon.Ok():
                    self.SetMiddleIcon(icon)
                else:
                    log.warning(u'Компонент Speedmeter. Некорректная иконка <%s>' % ico_file_name)
            else:
                log.warning(u'Компонент Speedmeter. Файл иконки <%s> не существует' % ico_file_name)
        
    def setHandColor(self, colour):
        """
        Цвет стрелки.
        """
        if colour:
            wx_colour = wx.Colour(*colour)
            self.SetHandColour(wx_colour)
        
    def setHandStyle(self, hand_style):
        """
        Стиль стрелки.
        """
        if hand_style:
            self.SetHandStyle(hand_style)
            
    def setBackgroundColor(self, colour):
        """
        Цвет фона.
        """
        if colour:
            wx_colour = wx.Colour(*colour)
            self.SetSpeedBackground(wx_colour)
    
    def setExternalArc(self, is_external_arc=True):
        """
        Установить окантовку поля.
        """
        self.DrawExternalArc(bool(is_external_arc))
        
    def setArcColor(self, colour):
        """
        Цвет окантовки.
        """
        if colour:
            wx_colour = wx.Colour(*colour)
            self.SetArcColour(wx_colour)
        
    def setShadowColor(self, colour):
        """
        Цвет тени.
        """
        if colour:
            wx_colour = wx.Colour(*colour)
            self.SetShadowColour(wx_colour)
        
    def setFillerColor(self, colour):
        """
        Цвет следа.
        """
        if colour:
            wx_colour = wx.Colour(*colour)
            self.SetFillerColour(wx_colour)

    def setFirstGradientColor(self, colour):
        """
        Первый цвет градиентной заливки.
        """
        if colour:
            wx_colour = wx.Colour(*colour)
            self.SetFirstGradientColour(wx_colour)
        
    def setSecondGradientColor(self, colour):
        """
        Втоорой цвет градиентной заливки.
        """
        if colour:
            wx_colour = wx.Colour(*colour)
            self.SetSecondGradientColour(wx_colour)
            
    def setDirection(self, direction):
        """
        Направление.
        """
        if direction:
            self.SetDirection(direction)
            
    setValue = parentModule.SpeedMeter.SetSpeedValue

    #   Обработчики событий


def test():
    """
    Функция тестирования.
    """
    import copy
    from ic import config

    log.init(config)

    app = wx.PySimpleApp()
    # Внимание!
    # Это отключает ошибку
    # wx._core.PyAssertionError: C++ assertion "m_window" failed at ../src/gtk/dcclient.cpp(2043)
    # in DoGetSize(): GetSize() doesn't work without window
    app.SetAssertMode(wx.PYAPP_ASSERT_SUPPRESS)

    frame = wx.Frame(None)
    panel = wx.Panel(frame)

    sizer = wx.BoxSizer()

    res = copy.deepcopy(ic_class_spc)
    speedmeter = icSpeedmeter(panel, component=res)

    sizer.Add(speedmeter, 1, wx.EXPAND | wx.GROW)

    panel.SetSizer(sizer)
    sizer.Layout()

    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
