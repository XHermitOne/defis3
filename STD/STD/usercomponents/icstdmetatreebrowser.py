#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Контрол управления деревом метакомпонентов.
"""

import wx
from ic.PropertyEditor import icDefInf
from ic.utils import coderror
from ic.dlg import dlgfunc
from ic.utils import util
from ic.bitmap import bmpfunc
from ic.components import icwidget
import ic.components.icResourceParser as prs

import STD.metastruct.std_metatree_browser as parentModule

from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icStdMetaTreeBrowser'

# Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'StdMetaTreeBrowser',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                'child': [],

                # 'metatree': None,    # Паспорт объекта описания мета-дерева

                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_TEXTFIELD: ['description'],
                                   # icDefInf.EDT_USER_PROPERTY: ['metatree'],
                                   },
                '__events__': {},
                '__parent__': parentModule.SPC_IC_STDMETATREEBROWSER,
                }


#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('node_magnifier.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('node_magnifier.png')

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


class icStdMetaTreeBrowser(parentModule.icStdMetaTreeBrowserProto, icwidget.icWidget):
    """
    Описание пользовательского компонента.

    :type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.

        - B{type='defaultType'}:
        - B{name='default'}:

    """
    component_spc = ic_class_spc

    def __init__(self, parent, id, component, logType=0, evalSpace=None,
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
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        parentModule.icStdMetaTreeBrowserProto.__init__(self, parent=parent)

