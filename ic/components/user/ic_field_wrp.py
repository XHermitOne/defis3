#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Поле таблицы.
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

from ic.db import icsqlalchemy

#   Тип компонента
ic_class_type = icDefInf._icDatasetType

#   Имя класса
ic_class_name = 'icField'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = {'type': icsqlalchemy.FIELD_TYPE,
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,

                'description': '',
                'default': None,
                'server_default': None,     # Значение по умолчанию, выполняемое на стороне сервера
                'label': '',
                'type_val': 'T',
                'unique': False,    # Уникальность значения поля в таблице
                'nullable': True,   # Поле может иметь значение NULL?
                'len': -1,
                'store': None,
                'dict': {},
                'field': None,
                'attr': 0,
                'idx': None,

                '__styles__': ic_class_styles,
                '__events__': {},
                '__brief_attrs__': ['name', 'type_val', 'description'],
                '__lists__': {'store': ['', ''],
                              'type_val': list(icsqlalchemy.FIELD_VALUES_ALL_TYPES),
                              'attr': [None, 0, 1, 2, 3],
                              },
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type',
                                                            'description', 'label',
                                                            'dict', 'field'],
                                   icDefInf.EDT_NUMBER: ['len'],
                                   icDefInf.EDT_CHECK_BOX: ['unique', 'nullable'],
                                   icDefInf.EDT_CHOICE: ['type_val', 'store',
                                                         'attr', 'idx'],
                                   },
                '__parent__': icsqlalchemy.SPC_IC_FIELD,
                '__attr_hlp__': {'default': u'Значение по умолчанию',
                                 'server_default': u'Значение по умолчанию, выполняемое на стороне сервера',
                                 'label': u'Надпись в формах',
                                 'type_val': u'Тип поля',
                                 'unique': u'Уникальность значения поля в таблице',
                                 'nullable': u'Поле может иметь значение NULL?',
                                 },
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtField'
ic_class_pic2 = '@common.imgEdtField'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.user.ic_field_wrp.icField-class.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 2)


class icField(icwidget.icSimple):
    pass
