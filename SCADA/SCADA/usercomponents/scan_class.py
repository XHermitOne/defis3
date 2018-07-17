#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Компонент класса сканирования тегов SCADA системы.

Классы сканирования определяют частоту обновления тегов и обработку событий.
"""

import time
from ic.components import icwidget

from ic.utils import util
from ic.PropertyEditor import icDefInf

from ic.log import log

from ic.bitmap import ic_bmp

# --- Спецификация ---
SPC_IC_SCAN_CLASS = {'tick': 60,

                     '__parent__': icwidget.SPC_IC_SIMPLE,

                     '__attr_hlp__': {'tick': u'Период сканирования в секундах',
                                      }

                     }


#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icScanClass'

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'ScanClass',
                'name': 'default',
                'child': [],
                'activate': True,
                '_uuid': None,

                '__events__': {},
                '__lists__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid'],
                                   icDefInf.EDT_NUMBER: ['tick'],
                                   },
                '__parent__': SPC_IC_SCAN_CLASS,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('file_start_workflow.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('file_start_workflow.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 1, 1)


class icScanClass(icwidget.icSimple):
    """
    Компонент класса сканирования тегов SCADA системы.

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
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if not x.startswith('__')]

        for key in lst_keys:
            setattr(self, key, component[key])

        # Время начала периода сканирования
        self._prev_time = None

    def isOverTick(self, cur_time=None):
        """
        Проверка на окончание текущего периода сканирования
        @param cur_time: Текущее проверяемое время.
            Если текущее время не определено, то берется time.time()
        @return: True - очередной период сканирования закончен/ False - период сканирования не закончен.
        """
        if cur_time is None:
            cur_time = time.time()

        if self._prev_time is None:
            # Если это первый запуск, то считаем что период закончился
            # и надо обновить данные
            self._prev_time = cur_time
            return True

        if (cur_time - self._prev_time) >= self.tick:
            # Т.к. очередной период сканирования закончен, то
            # запоминаем начало следующего периода сканирования
            self._prev_time = cur_time
            return True
        return False

    def getTick(self):
        """
        Значение периода сканирования в секундах.
        @return: Значение периода сканирования в секундах.
        """
        return self.tick
