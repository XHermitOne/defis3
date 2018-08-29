#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер для управления документами на форме.
"""

from ic.log import log
from ic.engine import form_manager

from . import document_filter_manager

# Версия
__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_DOCUMENT_FORM_MANAGER = {'__parent__': document_filter_manager.SPC_IC_DOCUMENT_FILTER_MANAGER,
                                }


class icDocumentFormManagerProto(document_filter_manager.icDocumentFilterManagerProto,
                                 form_manager.icFormManager):
    """
    Прототип компонента менеджера управления документами на форме/панели.
    """
