#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Поле таблицы.
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
                '__events__': {'init': (None, None, False),
                               'ctrl': (None, None, False),
                               'del': (None, None, False),
                               'post_init': (None, None, False),
                               'post_ctrl': (None, None, False),
                               'post_del': (None, None, False),

                               'getvalue': (None, None, False),
                               'setvalue': (None, None, False),
                               },
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
ic_class_doc = 'ic/doc/_build/html/ic.components.user.ic_field_wrp.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 3)


class icField(icwidget.icSimple):
    pass
