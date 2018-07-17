#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль описания схемы БД на движке SQLAlchemy.
"""

from ic.interfaces import icsourceinterface

# Тип
SQLALCHEMY_SCHEME_TYPE = 'SQLAlchemyScheme'


class icSQLAlchemySchemeProto(icsourceinterface.icSourceInterface):
    """
    Схема БД на движке SQLAlchemy.
    """

    def __init__(self, resource=None):
        """
        Конструктор.
        @param resource: Ресурсное описание.
        """
        icsourceinterface.icSourceInterface.__init__(self, resource)
