#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Контрол организации последовательности списка.
"""


import wx
import datetime
from ic.utils import util
from ic.bitmap import ic_bmp
from ic.components import icwidget as parentModule
from ic.PropertyEditor import icDefInf
from STD.controls import sequence_list_box_ctrl


#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icSequenceLstCtrl'

# Спецификация компонента
ic_class_spc = {'name': 'default',
                'type': 'SequenceListBox',
                '__attr_types__': {0: ['name', 'type'],
                                   },
                '__parent__': parentModule.SPC_IC_WIDGET,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('ui-flow.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('ui-flow.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = []

#   Версия компонента
__version__ = (0, 0, 0, 1)


class icSequenceListBox(sequence_list_box_ctrl.icSequenceListBox,
                        parentModule.icWidget):
    """
    Контрол организации последовательности списка.
    @type component_spc: C{dictionary}
    @cvar component_spc: Specification.
    """

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace = None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор.
        """
        # Append for specification
        component = util.icSpcDefStruct(ic_class_spc, component)
        parentModule.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        sequence_list_box_ctrl.icSequenceListBox.__init__(self, parent)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        for key in [x for x in component.keys() if not x.startswith('__')]:
            setattr(self, key, component[key])
