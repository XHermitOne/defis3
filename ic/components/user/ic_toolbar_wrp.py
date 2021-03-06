#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Панель инструментов.
Класс пользовательского визуального компонента.

:type ic_user_name: C{string}
:var ic_user_name: Имя пользовательского класса.
:type ic_can_contain: C{list | int}
:var ic_can_contain: Разрешающее правило - список типов компонентов, которые
    могут содержаться в данном компоненте. -1 - означает, что любой компонент
    может содержатся в данном компоненте. Вместе с переменной ic_can_not_contain
    задает полное правило по которому определяется возможность добавления других 
    компонентов в данный комопнент. 
:type ic_can_not_contain: C{list}
:var ic_can_not_contain: Запрещающее правило - список типов компонентов,
    которые не могут содержаться в данном компоненте. Запрещающее правило
    начинает работать если разрешающее правило разрешает добавлять любой 
    компонент (ic_can_contain = -1).
"""

from ic.components import icwidget
import ic.components.icResourceParser as prs
from ic.imglib import common
from ic.PropertyEditor import icDefInf

from ic.engine import ictoolbar

#   Тип компонента
ic_class_type = icDefInf._icMenuType

#   Имя класса
ic_class_name = 'icToolBar'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'MenuToolBar',
                'name': 'default',
                '_uuid': None,
                'child': [],

                '__styles__': ic_class_styles,
                '__events__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type',
                                                            'description', 'title'],
                                   icDefInf.EDT_CHECK_BOX: ['float', 'orientation'],
                                   icDefInf.EDT_POINT: ['pos'],
                                   icDefInf.EDT_SIZE: ['size'],
                                   },

                '__parent__': ictoolbar.SPC_IC_TOOLBAR,
                }

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = '@common.imgEdtToolBar'
ic_class_pic2 = '@common.imgEdtToolBar'

#   Путь до файла документации
ic_class_doc = 'ic/doc/_build/html/ic.components.user.ic_toolbar_wrp.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['Tool']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 2)


class icMenuToolBar(icwidget.icSimple):
    pass
