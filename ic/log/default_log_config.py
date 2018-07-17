#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Конфигурация для логирования по умолчанию.
"""

import os
import os.path
import datetime

# Режим отладки
DEBUG_MODE = True

# Режим журналирования
LOG_MODE = True

# Кодировка консоли по умолчанию
DEFAULT_ENCODING = 'utf-8'

# Имя папки прфиля программы
PROFILE_DIRNAME = '.defis'

# Имя файла журнала
LOG_FILENAME = os.path.join(os.environ.get('HOME',
                                           os.path.join(os.path.dirname(__file__), 'log')),
                            PROFILE_DIRNAME,
                            'defis_%s.log' % datetime.date.today().isoformat())
