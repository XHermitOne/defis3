#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Файл настроек загрузки файлов по сети.
"""

# Маски загружаемых файлов
DOWNLOAD_FILE_PATTERNS = ('*.apx', '*.APX', '*.atg', '*.ATG', '*.asf', '*.ASF', '*.arh', '*.ARH', '*.att', '*.ATT', '*.akt', '*.AKT', '*.UP2', '*.up2')

DOWNLOAD_FILE_EXT_UPPER = ('APX', 'ATG', 'ASF', 'ARH', 'ATT', 'AKT', 'UP2')

SMB_SRC_BACKUP_URLS = ('smb://xhermit@SAFE/Backup/daily.0/Nas_pvz/smb/sys_bucks/Nas_pvz/#MTS/',
                       'smb://xhermit@SAFE/Backup/daily.0/Nas_pvz/smb/sys_bucks/Nas_pvz/#RLZ/')

SMB_SRC_URLS = ('/mnt/samba/Nas_pvz/#MTS/',
                '/mnt/samba/Nas_pvz/#RLZ/',
                # '/mnt/samba/_MAIL/Arxiv',
                )

# Папки с данными для архива. Здесь указывается год-----------------------------------------V
ARCH_SMB_URLS_FMT = ('smb://user@DAKOTA/Backup/nas1sys/Nas_pvz/#RLZ/%d/ARHIV',
                     'smb://user@DAKOTA/Backup/nas1sys/Nas_pvz/#MTS/%d/ARHIV',
                     # 'smb://xhermit@NAS1/sys$/_MAIL/Arxiv',
                     )

ARCH_1C_SMB_URLS_FMT = (#'smb://xhermit@NAS1/sys$/_MAIL/Arxiv/mts/%d',
                        'smb://xhermit@PDC/public/1c/archive/2022',
                        )

# ARCH_SMB_URLS_FMT = ('/mnt/samba/Nas_pvz/#RLZ/%d/ARHIV',
#                     '/mnt/samba/Nas_pvz/#MTS/%d/ARHIV',
#                     )

ARCHIVE_DIRNAME = 'ARHIV'

# Результирующая папка для загрузки
DEST_PATH = '/mnt/defis/defis3/archive/db'

# Расширение результирующего файла, после загрузки
DEST_FILE_EXT = '.DBF'

# Маски типов файлов документов по участкам
REALIZ_FILE_MASKS = 'R*.DBF'
ZATRATY_FILE_MASKS = ('Z?768*.DBF', )
MATERIAL_FILE_MASKS = 'M*.DBF'
OSN_FILE_MASK = 'O*.DBF'
AREND_FILE_MASKS = 'U*.DBF'
USLUGI_FILE_MASKS = ('Z?767*.DBF', )
USLUGI7603_FILE_MASKS = ('Z?769*.DBF', )

__version__ = (0, 2, 2, 1)
