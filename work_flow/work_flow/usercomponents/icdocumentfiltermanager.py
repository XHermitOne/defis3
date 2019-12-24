#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Компонент менеджера управления фильтрацией и сортировкой документов.
"""

from ic.utils import util
from ic.bitmap import bmpfunc
from ic.PropertyEditor import icDefInf

import work_flow.doc_sys.document_filter_manager as parentModule

from . import icdocumentnavigatormanager

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icDocumentFilterManager'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'DocumentFilterManager',
                'name': 'default',
                'child': [],
                'activate': True,
                'init_expr': None,
                '_uuid': None,

                '__styles__': ic_class_styles,
                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_TEXTFIELD: ['description'],
                                   icDefInf.EDT_USER_PROPERTY: ['document', 'list_ctrl'],
                                   icDefInf.EDT_PY_SCRIPT: ['columns'],
                                   },
                '__events__': {},
                '__parent__': parentModule.SPC_IC_DOCUMENT_FILTER_MANAGER,
                '__attr_hlp__': {},
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('ic_box_doc_filter.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('ic_box_doc_filter.png')

#   Путь до файла документации
ic_class_doc = 'work_flow/doc/_build/html/work_flow.usercomponents.icdocumentfiltermanager.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = None

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 2)

# Функции редактирования
get_user_property_editor = icdocumentnavigatormanager.get_user_property_editor
property_editor_ctrl = icdocumentnavigatormanager.property_editor_ctrl
str_to_val_user_property = icdocumentnavigatormanager.str_to_val_user_property


class icDocumentFilterManager(icdocumentnavigatormanager.icDocumentNavigatorManager,
                              parentModule.icDocumentFilterManagerProto):
    """
    Компонент менеджера управления фильтрацией и сортировкой документов.

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
        component = util.icSpcDefStruct(self.component_spc, component)
        # icwidget.icSimple.__init__(self, parent, record_id, component, logType, eval_space)
        icdocumentnavigatormanager.icDocumentNavigatorManager.__init__(self, parent, id, component, logType, evalSpace)

        # Родительский класс icDocumentFilterManagerProto не имеет конструктора.
        # Вызывать конструктор не нужно
        # parentModule.icDocumentFilterManagerProto.__init__(self)
