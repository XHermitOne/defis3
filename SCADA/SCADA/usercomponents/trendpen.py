#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Компонент пера временного графика. Перо тренда.
"""

import wx

from math import pi     # Необходимо для расчета углов

from ic.PropertyEditor import icDefInf
from ic.components import icwidget

from ic.utils import util
from ic.log import log
from ic.bitmap import ic_bmp
from ic.dlg import ic_dlg

from ic.utils import coderror
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt


# --- Спецификация ---
DEFAULT_RGB_STR_COLOUR = '#0000FF'

SPC_IC_TRENDPEN = {'colour': (0, 0, 255),   # Цвет пера
                   'legend': None,          # Надпись в легенде
                   'tag_name': None,        # Имя тега источника данных
                   'history': None,         # Оъект источника исторических данных
                   '__parent__': icwidget.SPC_IC_SIMPLE,
                   '__attr_hlp__': {'colour': u'Цвет пера',
                                    'legend': u'Надпись в легенде',
                                    'tag_name': u'Имя тега источника данных',
                                    'history': u'Объект источника исторических данных',
                                    },
                   }

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icTrendPen'

#   Описание стилей компонента
ic_class_styles = 0

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'TrendPen',
                'name': 'default',
                'child': [],
                'activate': True,
                '_uuid': None,

                '__styles__': ic_class_styles,
                '__events__': {},
                '__lists__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid',
                                                            'tag_name'],
                                   icDefInf.EDT_COLOR: ['colour'],
                                   icDefInf.EDT_USER_PROPERTY: ['history'],
                                   },
                '__parent__': SPC_IC_TRENDPEN,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('chart_line_edit.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('chart_line_edit.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 1, 2)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('history',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('history',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('SQLWideHistory',):
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                                u'Выбранный объект не является Источником исторических данных.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
        elif ret in (None, ''):
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('history',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icTrendPenProto(object):
    """
    Базовый класс пера временного графика. Перо тренда.
    По сути перо тренда - ето источник данных для графика.
    """

    def getLegend(self):
        """
        Надпись в легенде.
        """
        return u''

    def getColour(self):
        """
        Цвет пера.
        """
        return wx.Colour(0, 0, 255)

    def getColourStr(self):
        """
        Цвет пера в строковом виде RGB. Например #FF0000.
        """
        wx_colour = self.getColour()
        if wx_colour:
            return wx_colour.GetAsString(wx.C2S_HTML_SYNTAX).encode('ascii')
        return DEFAULT_RGB_STR_COLOUR

    def getLineData(self):
        """
        Получить данные линий.
        @return: Список точек.
        """
        data = get_test_data()
        return data


class icTrendPen(icwidget.icSimple, icTrendPenProto):
    """
    Компонент пера временного графика. Перо тренда.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.

        - B{type='defaultType'}:
        - B{name='default'}:

    """
    component_spc = ic_class_spc

    # Реестр зарегистрированных объектов исторических данных
    history_registry = dict()

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
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if not x.startswith('__')]

        for key in lst_keys:
            setattr(self, key, component[key])

        #   !!! Конструктор наследуемого класса !!!
        #   Необходимо вставить реальные параметры конструкора.
        #   На этапе генерации их не всегда можно определить.
        icTrendPenProto.__init__(self)

        # Паспорт текущего объекта исторических данных
        self.current_history_psp = None

    def getLegend(self):
        """
        Надпись в легенде.
        """
        legend = self.getICAttr('legend')
        return u'' if legend is None else legend

    def getColour(self):
        """
        Цвет пера.
        """
        colour = self.getICAttr('colour')
        return wx.Colour(*colour) if colour else icTrendPenProto.getColour(self)

    def getHistoryPsp(self):
        """
        Паспорт объекта исторических данных - источника данных.
        """
        if self.current_history_psp is None:
            return self.getICAttr('history')
        return self.current_history_psp

    def getHistory(self):
        """
        Объект исторических данных - источника данных.
        @return: Объект или None в случае ошибки.
        """
        psp = self.getHistoryPsp()
        if psp and psp in self.history_registry:
            return self.history_registry[psp]
        history_obj = self.GetKernel().Create(psp)
        self.history_registry[psp] = history_obj
        return history_obj

    def setHistory(self, history):
        """
        Установить объект исторических данных - источника данных.
        @param history: Объект исторических данных - источника данных.
        @return: True/False.
        """
        if history is None:
            log.warning(u'Не определен объект исторических данных')
            return False

        try:
            psp = history.GetPassport()
            if not isinstance(psp, tuple):
                psp = tuple(psp)
            self.current_history_psp = psp
            if psp not in self.history_registry:
                self.history_registry[psp] = history
            return True
        except:
            log.fatal(u'Ошибка установки объекта исторических данных для пера тренда.')
        return False

    def getTagName(self):
        """
        Имя тега.
        """
        return self.getICAttr('tag_name')

    def getLineData(self):
        """
        Получить данные линий.
        @return: Список точек.
        """
        history_obj = self.getHistory()
        data = list
        if history_obj:
            tag_name = self.getTagName()
            trend = self.parent
            start_dt = trend.getStartDT()
            stop_dt = trend.getStopDT()
            data = history_obj.get_tag_data(tag_name=tag_name,
                                            start_dt=start_dt,
                                            stop_dt=stop_dt)
        return data


def get_test_data():
    """
    Тестовые данные точек.
    """
    import time
    import datetime
    import random
    now = datetime.datetime.now()
    data = [(now+datetime.timedelta(minutes=i), random.randint(0, 10)) for i in range(10)]
    print('DBG', data)
    return data
