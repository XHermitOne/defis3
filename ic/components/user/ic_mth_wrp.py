#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обертка для редактирования методов системы.
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

#Спецификация метода
SPC_IC_MTH={
    'name':'default',
    'type':'icMth',
    'description':'',
    'body':None,
    'parameters':'',
    }

#   Тип компонента
ic_class_type = None #icDefInf._icServiceType

#   Имя класса
ic_class_name = 'icMth'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT':0}

#   Спецификация на ресурсное описание класса
ic_class_spc = {'__events__': {},
                'type': 'Method',
                'name': 'default',
                '_uuid':None,
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type',
                                        'description',
                                        'parameters'],
                                  },
                '__parent__':SPC_IC_MTH,
                }
                    
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtMethod'
ic_class_pic2 = '@common.imgEdtMethod'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.user.ic_mth_wrp.icMethod-class.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0,0,0,1)

class icMethod(icwidget.icSimple):
    pass

