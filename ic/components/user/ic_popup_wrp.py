#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Всплывающее меню.
Класс пользовательского визуального компонента.

@type ic_user_name: C{string}
@var ic_user_name: Имя пользовательского класса.
@type ic_can_contain: C{list | int}
@var ic_can_contain: Разрешающее правило - список типов компонентов, которые
    могут содержаться в данном компоненте. -1 - означает, что любой компонент
    может содержатся в данном компоненте. Вместе с переменной ic_can_not_contain
    задает полное правило по которому определяется возможность добавления других 
    компонентов в данный комопнент. 
@type ic_can_not_contain: C{list}
@var ic_can_not_contain: Запрещающее правило - список типов компонентов, 
    которые не могут содержаться в данном компоненте. Запрещающее правило
    начинает работать если разрешающее правило разрешает добавлять любой 
    компонент (ic_can_contain = -1).
"""

import wx
import ic.components.icwidget as icwidget
import ic.utils.util as util
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf
import copy
import ic.engine.ic_popup as ic_popup

#   Тип компонента
ic_class_type = icDefInf._icMenuType

#   Имя класса
ic_class_name = 'icPopupMenu'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание класса
SPC_IC_POPUPMENU = copy.deepcopy(ic_popup.SPC_IC_POPUPMENU)
SPC_IC_POPUPMENU['__parent__'] = icwidget.SPC_IC_SIMPLE

ic_class_spc = {'type': 'PopupMenu',
                'name': 'default',
                'child': [],

                '__styles__': ic_class_styles,
                '__events__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type',
                                                            'description', 'title', 'hot_key'],
                                   icDefInf.EDT_CHECK_BOX: ['title_readonly'],
                                   },
                '__parent__': SPC_IC_POPUPMENU,
                }

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = '@common.imgEdtMenu'
ic_class_pic2 = '@common.imgEdtMenu'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.user.ic_popup_wrp.icPopupMenu-class.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['Menu', 'MenuItem']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 2)


class icPopupMenu(icwidget.icSimple, wx.PopupWindow):
    pass
