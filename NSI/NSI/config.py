#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Конфигурационный файл.
"""

import os
import os.path
import datetime
import ic.config

# Вкл./Выкл. режима отладки
DEBUG_MODE = True
LOG_MODE = True

# Имя папки прфиля программы
PROFILE_DIRNAME = 'NSI'

DEFAULT_ENCODING = 'utf-8'

# Имя файла журнала
LOG_FILENAME = os.path.join(os.environ.get('HOME',
                                           os.path.join(os.path.dirname(__file__), 'log', 'log')),
                            ic.config.PROFILE_DIRNAME,
                            PROFILE_DIRNAME,
                            'nsi_%s.log' % datetime.date.today().isoformat())


DEFAULT_DATE_FMT = '%Y.%m.%d'

