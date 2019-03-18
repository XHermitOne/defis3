#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Файл настроек загрузки файлов по сети.
"""

# Маски загружаемых файлов
DOWNLOAD_FILE_PATTERNS = ('*.apx', '*.APX')

SMB_SRC_URLS = ('smb://xhermit@SAFE/Backup/daily.0/Nas_pvz/smb/sys_bucks/Nas_pvz/#MTS/',
                'smb://xhermit@SAFE/Backup/daily.0/Nas_pvz/smb/sys_bucks/Nas_pvz/#RLZ/')

ARCHIVE_DIRNAME = 'ARHIV'

# Результирующая папка для загрузки
DEST_PATH = '/mnt/defis/defis3/archive/db'

# Расширение результирующего файла, после загрузки
DEST_FILE_EXT = '.DBF'

__version__ = (0, 1, 1, 2)
