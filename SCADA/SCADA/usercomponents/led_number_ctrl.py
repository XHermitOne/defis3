#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Объект цифрового LED индикатора.
"""

import wx
from ic.components import icwidget
from ic.utils import util
from ic.PropertyEditor import icDefInf

from ic.log import log

from ic.bitmap import bmpfunc
import wx.lib.gizmos as parentModule


LED_NUMBER_CTRL_STYLE = {'LED_ALIGN_LEFT': parentModule.LED_ALIGN_LEFT,
                         'LED_ALIGN_RIGHT': parentModule.LED_ALIGN_RIGHT,
                         'LED_ALIGN_CENTER': parentModule.LED_ALIGN_CENTER,
                         'LED_ALIGN_MASK': parentModule.LED_ALIGN_MASK,
                         'LED_DRAW_FADED': parentModule.LED_DRAW_FADED,
                         }


SPC_IC_LEDNUMBERCTRL = {'draw_faded': True,
                        'foreground_colour': None,
                        'background_colour': None,
                        'default': u'---',

                        '__parent__': icwidget.SPC_IC_WIDGET,

                        '__attr_hlp__': {'draw_faded': 'Признак, будут ли неосвещенные сегменты отображаться с выцветшей версией цвета переднего плана',
                                         'foreground_colour': u'Цвет текста (По умолчанию зеленый)',
                                         'background_colour': u'Цвет фона (По умолчанию черный)',
                                         'default': u'Значение по умолчанию',
                                         },
                        }

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icLEDNumberCtrl'

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'LEDNumberCtrl',
                'name': 'default',
                'child': [],
                'activate': True,
                '_uuid': None,
                'style': parentModule.LED_ALIGN_LEFT,

                '__styles__': LED_NUMBER_CTRL_STYLE,
                '__events__': {},
                '__lists__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid', 'default'],
                                   icDefInf.EDT_CHECK_BOX: ['draw_faded'],
                                   icDefInf.EDT_COLOR: ['foreground_colour', 'background_colour'],
                                   },
                '__parent__': SPC_IC_LEDNUMBERCTRL,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('counter.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('counter.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 1)


class icLEDNumberCtrl(icwidget.icWidget, parentModule.LEDNumberCtrl):
    """
    Объект цифрового LED индикатора.

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
        parentModule.LEDNumberCtrl.__init__(self, parent,
                                            pos=self.getPos(),
                                            size=self.getSize(),
                                            style=self.getStyle())
        # Установка свойств
        self.SetDrawFaded(self.getDrawFaded())
        if self.foreground_colour:
            self.SetForegroundColour(self.foreground_colour)
        if self.background_colour:
            self.SetBackgroundColour(self.background_colour)
        if self.default:
            self.setValue(self.default)

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

    def getDrawFaded(self):
        """
        Признак, будут ли неосвещенные сегменты отображаться
        с выцветшей версией цвета переднего плана.
        """
        return self.draw_faded

    def setValue(self, value):
        """
        Установить значение контрола.

        :param value: Значение контрола.
            Значение может быть следующих типов: целое, вещественное и строка.
            В противном случае все остальное приводится к виду строки.
        :return: True/False.
        """
        if not isinstance(value, str):
            value = str(value)

        self.SetValue(value)
        return True
