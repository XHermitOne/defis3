#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Текстовый индикатор состояний.
"""

import wx

from ic.log import log
from ic.components import icwidget
from ic.components import icfont
from ic.PropertyEditor import icDefInf
from ic.utils import util
from ic.utils import  coderror
from ic.bitmap import ic_bmp

# Стили
ICStaticTextStyle = {'ALIGN_LEFT': wx.ALIGN_LEFT,
                     'ALIGN_RIGHT': wx.ALIGN_RIGHT,
                     'ALIGN_CENTRE': wx.ALIGN_CENTRE,
                     'ST_NO_AUTORESIZE': wx.ST_NO_AUTORESIZE}

# --- Спецификация ---
SPC_IC_TEXT_INDICATOR = {'style': wx.ALIGN_LEFT,
                         'position': (-1, -1),
                         'size': (70, 18),
                         'label': 'indicator',
                         'font': {},

                         'foregroundColor': (50, 50, 50),
                         'backgroundColor': None,

                         'get_indicator_label': None,
                         'get_indicator_fg': None,
                         'get_indicator_bg': None,

                         '__parent__': icwidget.SPC_IC_WIDGET,

                         '__attr_hlp__': {'label': u'Текст индикатора по умолчанию',
                                          'foregroundColor': u'Цвет текста индикатора по умолчанию',
                                          'backgroundColor': u'Цвет фона индикатора по умолчанию',
                                          'get_indicator_label': u'Метод/Словарь получения текста индикатора',
                                          'get_indicator_fg': u'Метод/Словарь получения цвета текста индикатора',
                                          'get_indicator_bg': u'Метод/Словарь получения цвета фона индикатора',
                                          },
                         }

#   Тип компонента. None, означает, что данный компонент убран из
#   редактора и остался только для совместимости со старыми проектами.
ic_class_type = icDefInf._icControlsType

#   Имя пользовательского класса
ic_class_name = 'icTextIndicator'

#   Описание стилей компонента
ic_class_styles = ICStaticTextStyle

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = {'type': 'TextIndicator',
                'name': 'default',
                'child': [],
                'activate': True,
                '_uuid': None,
                '__styles__': ic_class_styles,

                '__events__': {},
                '__lists__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid', 'label'],
                                   icDefInf.EDT_COLOR: ['foregroundColor', 'backgroundColor'],
                                   icDefInf.EDT_PY_SCRIPT: ['get_indicator_label',
                                                            'get_indicator_fg', 'get_indicator_bg'],
                                   },
                '__parent__': SPC_IC_TEXT_INDICATOR,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('three_tags.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('three_tags.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 1)


class icTextIndicator(icwidget.icWidget, wx.StaticText):
    """
    Текстовый индикатор состояний.
    """
    component_spc = ic_class_spc

    def __init__(self, parent, id, component, logType=0, evalSpace={},
                 bCounter=False, progressDlg=None):
        """
        Конструктор.

        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно
        @type id: C{int}
        @param id: Идентификатор окна
        @type component: C{dictionary}
        @param component: Словарь описания компонента
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений
        @type evalSpace: C{dictionary}
        """
        component = util.icSpcDefStruct(self.component_spc, component, True)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        pos = component['position']
        size = component['size']
        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        font = component['font']
        style = component['style']

        label = self.getDefaultLabel()
        wx.StaticText.__init__(self, parent, id, label, pos, size=size,
                               style=style, name=self.name)

        if fgr is not None:
            self.SetForegroundColour(wx.Colour(*fgr))

        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(*bgr))

        font_obj = icfont.icFont(font)
        self.SetFont(font_obj)

        # Текущее внутреннее значение
        self._value = None

    def getDefaultLabel(self):
        """
        Надпись по умолчанию.
        """
        return self.getICAttr('label')

    def getIndicatorLabel(self, value=None):
        """
        Получить текущую надпись индикатора, соответствующую значению.
        @param value: Текущее обрабатываемое значение.
        """
        try:
            context = self.GetContext()
            context['VALUE'] = value
            if self.isICAttrValue('get_indicator_label'):
                result = self.eval_attr('get_indicator_label')
                if result[0] == coderror.IC_EVAL_OK:
                    text_indicator = result[1]
                    if isinstance(text_indicator, dict):
                        # Если мы получаем словарь в виде результата,
                        # то необходимо по нему получить актуальное значение
                        default_label = self.getDefaultLabel()
                        new_text_indicator = text_indicator.get(value, default_label)
                        return new_text_indicator
                    elif type(text_indicator) in (str, unicode):
                        # Получили текст надписи в явном виде
                        return text_indicator
                    elif text_indicator is None:
                        log.warning(u'Не определена надпись индикатора')
                        return u''
                    else:
                        log.warning(u'Не корректный тип надписи индикатора <%s>' % text_indicator.__class__.__name__)
                    return str(text_indicator)
                else:
                    log.warning(u'Ошибка обработки получения надписи индикатора <%s>.' % self.getName())
            else:
                log.warning(u'Не определено выражение получения надписи индикатора <%s>.' % self.getName())
        except:
            log.fatal(u'Ошибка получения надписи индикатора <%s>.' % self.getName())
        return u''

    def setValue(self, value):
        """
        Установить данные в виджет.
        """
        self._value = value
        text_indicator = self.getIndicatorLabel(self._value)

        fg_indicator = self.getIndicatorFG(value)
        if fg_indicator is not None:
            self.SetForegroundColour(fg_indicator)
        else:
            sys_colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)
            self.SetForegroundColour(sys_colour)

        bg_indicator = self.getIndicatorBG(value)
        if bg_indicator is not None:
            self.self.SetBackgroundColour(bg_indicator)
        else:
            sys_colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWFRAME)
            self.SetBackgroundColour(sys_colour)

        return self.SetLabel(text_indicator)

    def getValue(self):
        """
        Получить данные из виджета.
        """
        return self._value

    def getIndicatorFG(self, value=None):
        """
        Получить текущий цвет текста индикатора, соответствующий значению.
        @param value: Текущее обрабатываемое значение.
        """
        try:
            context = self.GetContext()
            context['VALUE'] = value
            if self.isICAttrValue('get_indicator_fg'):
                result = self.eval_attr('get_indicator_fg')
                if result[0] == coderror.IC_EVAL_OK:
                    color_indicator = result[1]
                    if isinstance(color_indicator, dict):
                        # Если мы получаем словарь в виде результата,
                        # то необходимо по нему получить актуальное значение
                        default_color = self.resource.get('foregroundColor', None)
                        new_color_indicator = color_indicator.get(value, default_color)
                        return new_color_indicator
                    elif isinstance(color_indicator, wx.Colour):
                        # Получили цвет в явном виде
                        return color_indicator
                    elif isinstance(color_indicator, tuple) and len(color_indicator) == 3:
                        # Получили цвет в явном виде
                        return wx.Colour(*color_indicator)
                    else:
                        log.warning(u'Не корректный тип цвета текста индикатора <%s>' % color_indicator.__class__.__name__)
                else:
                    log.warning(u'Ошибка обработки получения цвета текста индикатора <%s>.' % self.getName())
        except:
            log.fatal(u'Ошибка получения цвета текста индикатора <%s>.' % self.getName())
        return None

    def getIndicatorBG(self, value=None):
        """
        Получить текущий цвет фона индикатора, соответствующий значению.
        @param value: Текущее обрабатываемое значение.
        """
        try:
            context = self.GetContext()
            context['VALUE'] = value
            if self.isICAttrValue('get_indicator_bg'):
                result = self.eval_attr('get_indicator_bg')
                if result[0] == coderror.IC_EVAL_OK:
                    color_indicator = result[1]
                    if isinstance(color_indicator, dict):
                        # Если мы получаем словарь в виде результата,
                        # то необходимо по нему получить актуальное значение
                        default_color = self.resource.get('backgroundColor', None)
                        new_color_indicator = color_indicator.get(value, default_color)
                        return new_color_indicator
                    elif isinstance(color_indicator, wx.Colour):
                        # Получили цвет в явном виде
                        return color_indicator
                    elif isinstance(color_indicator, tuple) and len(color_indicator) == 3:
                        # Получили цвет в явном виде
                        return wx.Colour(*color_indicator)
                    else:
                        log.warning(u'Не корректный тип цвета фона индикатора <%s>' % color_indicator.__class__.__name__)
                else:
                    log.warning(u'Ошибка обработки получения цвета фона индикатора <%s>.' % self.getName())
        except:
            log.fatal(u'Ошибка получения цвета фона индикатора <%s>.' % self.getName())
        return None


def test(par=0):
    """
    Тестируем класс icStaicText.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'icStaticText Test')
    win = wx.Panel(frame, -1)
    ctrl = icTextIndicator(win, -1, {'text': '@\'icStaticText\'+\'>>\'',
                                     'font': {'style': 'boldItalic', 'size': 14}})
    frame.Show(True)
    app.MainLoop()
    wx.GREY


if __name__ == '__main__':
    test()
