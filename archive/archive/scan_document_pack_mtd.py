#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resource module </mnt/defis/defis3/archive/archive/scan_document_pack.mtd>
File            </mnt/defis/defis3/archive/archive/scan_document_pack_mtd.py>
Description     <Resource module>
"""

import datetime
import os.path
import sqlalchemy
from ic import log
import ic
from ic.db import dbf
from ic.utils import strfunc
from ic import dlgfunc
from ic.utils import uuidfunc
from ic.utils import extfunc
from ic.utils import datetimefunc
from ic.engine import glob_functions
from ic.interfaces import icmanagerinterface

### RESOURCE_MODULE: /mnt/defis/defis3/archive/archive/scan_document_pack.mtd

### ---- Import external modules -----
### RESOURCE_MODULE_IMPORTS

#   Version
__version__ = (0, 0, 4, 1)

DBF_DEFAULT_ENCODE = 'cp866'

# Код КПП для ИП отсутствует, подменяем на КПП по умолчанию
DEFAULT_KPP_CODE = '---------'

# Формат автоматической генерации ИНН части кода если не указан
DEFAULT_INN_CODE_FMT = '%010d'

DEFAULT_DBF_DT_FMT = '%d.%m.%Y'
DEFAULT_DB_DT_FMT = '%Y-%m-%d'

DT_TODAY = datetime.date.today()

# Игнорируемые документы по признаку в поле CODF
# ВП - внутреннее перемещение
IGNORED_CODF = (u'ВП', u'АТ', u'ПП', u'АВ')
MT_IGNORED_CODF = (u'ВП', u'АС')


class icScanDocPackManager(icmanagerinterface.icWidgetManager):

    def onInit(self, event):
        pass
    
    def init(self):
        """
        Инициализация.
        """
        pass
    
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK

manager_class = icScanDocPackManager
