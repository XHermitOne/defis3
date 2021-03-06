#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Кнопка на панели инструментов.
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

import wx
from ic.components import icwidget
from ic.utils import util
import ic.components.icResourceParser as prs
from ic.imglib import common
from ic.PropertyEditor import icDefInf

import ic.engine.ictoolbar as ic_tool

#   Тип компонента
ic_class_type = icDefInf._icMenuType

#   Имя класса
ic_class_name = 'icTool'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'MenuTool',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,

                '__styles__': ic_class_styles,
                '__events__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type',
                                                            'description', 'item', 'hot_key',
                                                            'hint', 'image', 'help'],
                                   icDefInf.EDT_CHECK_BOX: ['enabled', 'checkable', 'checked', 'radio'],
                                   },
                '__parent__': ic_tool.SPC_IC_TOOL,
                }

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = '@common.imgEdtTBTool'
ic_class_pic2 = '@common.imgEdtTBTool'

#   Путь до файла документации
ic_class_doc = 'ic/doc/_build/html/ic.components.user.ic_tool_wrp.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 2)


class icMenuTool(icwidget.icSimple):
    pass
