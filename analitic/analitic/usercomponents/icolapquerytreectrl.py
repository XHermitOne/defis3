#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Контрол управления деревом запросов к OLAP кубам OLAP сервера.
"""

import wx

from ic.log import log
from ic.bitmap import ic_bmp
from ic.utils import util

from ic.components import icwidget
from ic.PropertyEditor import icDefInf
from ic.components import icResourceParser as prs

from ..olap.ctrl import olap_query_tree_ctrl

#   Описание стилей компонента
ic_class_styles = {'TR_NO_BUTTONS': wx.TR_NO_BUTTONS,
                   'TR_HAS_BUTTONS': wx.TR_HAS_BUTTONS,
                   'TR_NO_LINES': wx.TR_NO_LINES,
                   'TR_LINES_AT_ROOT': wx.TR_LINES_AT_ROOT,
                   'TR_SINGLE': wx.TR_SINGLE,
                   'TR_MULTIPLE': wx.TR_MULTIPLE,
                   # 'TR_EXTENDED': wx.TR_EXTENDED,
                   'TR_HAS_VARIABLE_ROW_HEIGHT': wx.TR_HAS_VARIABLE_ROW_HEIGHT,
                   'TR_EDIT_LABELS': wx.TR_EDIT_LABELS,
                   'TR_HIDE_ROOT': wx.TR_HIDE_ROOT,
                   'TR_ROW_LINES': wx.TR_ROW_LINES,
                   'TR_FULL_ROW_HIGHLIGHT': wx.TR_FULL_ROW_HIGHLIGHT,
                   'TR_DEFAULT_STYLE': wx.TR_DEFAULT_STYLE,
                   'TR_TWIST_BUTTONS': wx.TR_TWIST_BUTTONS,
                   # 'TR_MAC_BUTTONS': wx.TR_MAC_BUTTONS
                   }

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icOLAPQueryTreeCtrl'

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'OLAPQueryTreeCtrl',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                'child': [],

                '__styles__': ic_class_styles,
                '__events__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type'],
                                   },
                '__parent__': olap_query_tree_ctrl.SPC_IC_OLAPQUERYTREECTRL,
                '__lists__': {},
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('wxtreectrl.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('wxtreectrl.png')

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


class icOLAPQueryTreeCtrl(icwidget.icWidget,
                          olap_query_tree_ctrl.icOLAPQueryTreeCtrlProto):
    """
    Контрол управления деревом запросов к OLAP кубам OLAP сервера.
    """
    component_spc = ic_class_spc

    def __init__(self, parent, id, component, logType=0, evalSpace=None,
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
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        olap_query_tree_ctrl.icOLAPQueryTreeCtrlProto.__init__(self, parent=parent, id=id)
        #   Создаем дочерние компоненты
        # if 'child' in component:
        #     self.childCreator(bCounter, progressDlg)
