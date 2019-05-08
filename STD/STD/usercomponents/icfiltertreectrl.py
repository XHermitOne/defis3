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

# Регистрация прав использования
from ic.kernel import icpermission
from ic.kernel.icaccesscontrol import ClassSecurityInfo

prm = icpermission.icPermission(id='tree_filter_edit', title='TreeObjFilterEdit',
                                description=u'Редактирование структурных фильтров',
                                component_type='STD')
icpermission.registerPermission(prm)

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
                'get_records': None,    # Код получения набора записей, соответствующих фильтру для индикаторов

                'onChange': None,  # Код смены фильтра

                '__events__': {'get_env': (None, None, False),
                               'onChange': (None, 'OnChange', False),
                               'get_records': (None, 'getCurRecords', False),
                               },
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type', 'save_filename'],
                                   icDefInf.EDT_PY_SCRIPT: ['get_env', 'onChange', 'get_records'],
                                   icDefInf.EDT_NUMBER: ['limit'],
                                   },

                '__parent__': icwidget.SPC_IC_WIDGET,
                '__attr_hlp__': {'save_filename': u'Имя файла хранения фильтров',
                                 'get_env': u'Метод получения окружения',
                                 'limit': u'Ограничение количества строк',
                                 'onChange': u'Код смены фильтра',
                                 'get_records': u'Код получения набора записей, соответствующих фильтру для индикаторов',
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
    security = ClassSecurityInfo()

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

        self._save_filename = self.getICAttr('save_filename')
        self._environment = self.getICAttr('get_env')
        self._limit = self.getICAttr('limit')

        # После того как определили окружение и
        # имя файла хранения фильтров можно загрузить фильтры
        self.loadFilters()
        # self.SetValue(self.getStrFilter())

    # Установка ограничения редактирования фильтров
    # Для этого в родительском классе заведены
    # функции <addFilter>, <delFilter>, <editFilter>, <editItemIndicator>
    security.declareProtected('tree_filter_edit', 'addFilter')
    security.declareProtected('tree_filter_edit', 'delFilter')
    security.declareProtected('tree_filter_edit', 'editFilter')
    security.declareProtected('tree_filter_edit', 'editItemIndicator')

    def _canEditFilter(self):
        return self.security.is_permission('tree_filter_edit', self.GetKernel().GetAuthUser().getPermissions())

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

    def OnChange(self, event):
        """
        Смена фильтра.
        """
        return self.eval_attr('onChange')

    def getCurRecords(self):
        """
        Код получения набора записей, соответствующих фильтру для индикаторов.
        """
        return self.eval_attr('get_records')
