#!/usr/bin/env python
#  -*- coding: utf-8 -*-

"""
Конфигурационный файл.
"""

import os
import os.path
import datetime

# Вкл./Выкл. режима отладки
DEBUG_MODE = True
LOG_MODE = True

# Имя папки прфиля программы
PROFILE_DIRNAME = '.defis/NSI'

DEFAULT_ENCODING = 'utf-8'

# Имя файла журнала
LOG_FILENAME = '%s/%s/nsi_%s.log' % (os.environ.get('HOME', os.path.dirname(__file__)+'/log/log'),
                                     PROFILE_DIRNAME, datetime.date.today().isoformat())


DEFAULT_DATE_FMT = '%Y.%m.%d'

