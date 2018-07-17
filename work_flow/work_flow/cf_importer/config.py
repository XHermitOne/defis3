#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Конфигурационный файл.
"""

import os.path
import datetime

# Вкл./Выкл. режима отладки
DEBUG_MODE = True
LOG_MODE = True

# Имя папки прфиля программы
PROFILE_DIRNAME = '.defis'

DEFAULT_ENCODING = 'utf-8'

# Имя файла журнала
LOG_FILENAME = os.path.join(os.environ.get('HOME',
                                           os.path.join(os.path.dirname(__file__), 'log', 'log')),
                            PROFILE_DIRNAME,
                            'cf_importer_%s.log' % datetime.date.today().isoformat())

DEFAULT_CF_DIRNAME = os.path.join(os.environ.get('HOME',
                                                 os.path.join(os.path.dirname(__file__), 'cf')),
                                  PROFILE_DIRNAME, 'cf')
