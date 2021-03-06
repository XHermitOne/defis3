#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Компонент аварийного события SCADA системы.
"""

from ic.components import icwidget

from ic.utils import util
from ic.PropertyEditor import icDefInf

from ic.log import log

from ic.bitmap import bmpfunc

# --- Спецификация ---
SPC_IC_SCADA_ALARM = {
                    '__parent__': icwidget.SPC_IC_SIMPLE,
                    }


#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icSCADAAlarm'

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'SCADAAlarm',
                'name': 'default',
                'child': [],
                'activate': True,
                '_uuid': None,

                '__events__': {},
                '__lists__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid'],
                                   },
                '__parent__': SPC_IC_SCADA_ALARM,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('bell_error.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('bell_error.png')

#   Путь до файла документации
ic_class_doc = 'SCADA/doc/_build/html/SCADA.usercomponents.scada_alarm.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 2)


class icSCADAAlarm(icwidget.icSimple):
    """
    Компонент аварийного события SCADA системы.

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
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)
