#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Компонент дерева фильтров.
"""

import wx

from ic.bitmap import ic_bmp
from ic.log import log
from ic.utils import util
from ic.utils import ic_uuid

from ic.components import icwidget
from ic.PropertyEditor import icDefInf

from STD.queries import filter_tree_ctrl

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icFilterTreeCtrl'

# Спецификация компонента
ic_class_spc = {'name': 'default',
                'type': 'FilterTreeCtrl',

                'save_filename': None,  # Имя файла хранения фильтров
                'get_env': None,  # Метод получения окружения
                'limit': None,  # Ограничение количества строк

                '__events__': {'get_env': (None, None, False)},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type', 'save_filename'],
                                   icDefInf.EDT_PY_SCRIPT: ['get_env'],
                                   icDefInf.EDT_NUMBER: ['limit'],
                                   },

                '__parent__': icwidget.SPC_IC_WIDGET,
                '__attr_hlp__': {'save_filename': u'Имя файла хранения фильтров',
                                 'get_env': u'Метод получения окружения',
                                 'limit': u'Ограничение количества строк',
                                 },
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('funnel--arrow.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('funnel--arrow.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = []

#   Версия компонента
__version__ = (0, 1, 1, 1)


class icFilterTreeCtrl(icwidget.icWidget,
                       filter_tree_ctrl.icFilterTreeCtrlProto):
    """
    Компонент дерева фильтров.
    """

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор.
        """
        self._widget_psp_uuid = None

        # Append for specification
        component = util.icSpcDefStruct(ic_class_spc, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        filter_tree_ctrl.icFilterTreeCtrlProto.__init__(self, parent, id)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        for key in [x for x in component.keys() if not x.startswith('__')]:
            setattr(self, key, component[key])

        self._filter_filename = self.getICAttr('save_filename')
        self._environment = self.getICAttr('get_env')
        self._limit = self.getICAttr('limit')

        # После того как определили окружение и
        # имя файла хранения фильтров можно загрузить фильтры
        self.loadFilters()
        # self.SetValue(self.getStrFilter())

    def getUUID(self):
        """
        Это уникальный идентификатор паспорта компонента.
        Не изменяемый в зависимости от редактирования т.к.
        паспорт не меняется.
        @return: UUID строка контрольной суммы паспорта.
        """
        if self._widget_psp_uuid:
            return self._widget_psp_uuid

        psp = self.GetPassport()
        if psp:
            psp = tuple(psp)[0]
        self._widget_psp_uuid = ic_uuid.get_passport_check_sum(psp, True)
        return self._widget_psp_uuid
