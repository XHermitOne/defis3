#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль описаний типов полей компонента таблицы.
"""

from ic.log import log

try:
    import sqlalchemy
    import sqlalchemy.orm

    from sqlalchemy import *
    from sqlalchemy.sql.functions import *

    sqlalchemy_field_type_Integer = sqlalchemy.Integer
    sqlalchemy_field_type_Float = sqlalchemy.Float
    sqlalchemy_field_type_String = sqlalchemy.String
    sqlalchemy_field_type_Text = sqlalchemy.Text
    sqlalchemy_field_type_Binary = sqlalchemy.Binary if hasattr(sqlalchemy, 'Binary') else sqlalchemy.BINARY
    sqlalchemy_field_type_DateTime = sqlalchemy.DateTime
    sqlalchemy_field_type_PickleType = sqlalchemy.PickleType
    sqlalchemy_field_type_BigInteger = sqlalchemy.BigInteger
    sqlalchemy_field_type_Boolean = sqlalchemy.Boolean
except ImportError:
    log.error('SQLAlchemy import error')
    sqlalchemy_field_type_Integer = None
    sqlalchemy_field_type_Float = None
    sqlalchemy_field_type_String = None
    sqlalchemy_field_type_Text = None
    sqlalchemy_field_type_Binary = None
    sqlalchemy_field_type_DateTime = None
    sqlalchemy_field_type_PickleType = None
    sqlalchemy_field_type_BigInteger = None
    sqlalchemy_field_type_Boolean = None

from ic.components import icwidget

__version__ = (0, 1, 1, 2)

# Типы полей
FIELD_TYPE = 'Field'
LINK_TYPE = 'Link'

MULTIPLE_JOIN_TAG = 0
RELATED_JOIN_TAG = 1

# Типы данных полей
TEXT_FIELD_TYPE = 'T'
DATE_FIELD_TYPE = 'D'
INT_FIELD_TYPE = 'I'
FLOAT_FIELD_TYPE = 'F'
DATETIME_FIELD_TYPE = 'DateTime'
BINARY_FIELD_TYPE = 'Binary'
PICKLE_FIELD_TYPE = 'PickleType'
BIGINT_FIELD_TYPE = 'BigInteger'
BOOLEAN_FIELD_TYPE = 'Boolean'
FIELD_VALUES_ALL_TYPES = (TEXT_FIELD_TYPE,
                          DATE_FIELD_TYPE,
                          INT_FIELD_TYPE,
                          FLOAT_FIELD_TYPE,
                          DATETIME_FIELD_TYPE,
                          BINARY_FIELD_TYPE,
                          PICKLE_FIELD_TYPE,
                          BIGINT_FIELD_TYPE,
                          BOOLEAN_FIELD_TYPE)

# Спецификация поля
SPC_IC_FIELD = {'type': FIELD_TYPE,
                'name': 'default_field',

                'description': '',
                'default': None,
                'server_default': None,     # Значение по умолчанию, выполняемое на стороне сервера
                'label': '',
                'type_val': TEXT_FIELD_TYPE,
                'unique': False,    # Уникальность значения поля в таблице
                'nullable': True,   # Поле может иметь значение NULL?
                'len': -1,
                'store': None,
                'dict': {},
                'field': None,
                'attr': 0,
                'idx': None,

                '__parent__': icwidget.SPC_IC_SIMPLE,
                '__attr_hlp__': {'server_default': u'Значение по умолчанию, выполняемое на стороне сервера',
                                 'label': u'Надпись в формах',
                                 'unique': u'Уникальность значения поля в таблице',
                                 'nullable': u'Поле может иметь значение NULL?',
                                 'type_val': u'Тип хранимого значения',
                                 'len': u'Длина хранимого значения',
                                 },
                }

# Спецификация связи
SPC_IC_LNK = {'type': LINK_TYPE,
              'name': 'default_lnk',

              'description': '',
              'lnk_type': 'phisical',   # Жесткая/логическая связь
              'table': None,
              'del_cascade': False,
              'field': None,

              '__parent__': icwidget.SPC_IC_SIMPLE,
              '__attr_hlp__': {'lnk_type': u'Жесткая/логическая связь',
                               },
              }

