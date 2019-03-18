#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Функции загрузки файлов данных в виде DBF из сети.
"""

import os
import os.path
import datetime

from ic.log import log
from . import load_net_config
from ic.utils import smbfunc

__version__ = (0, 1, 1, 2)


# Папки с данными для архива. Здесь указывается год-----------------------------------------V
ARCH_SMB_URLS_FMT = ('smb://xhermit@SAFE/Backup/daily.0/Nas_pvz/smb/sys_bucks/Nas_pvz/#RLZ/%d/ARHIV',
                     'smb://xhermit@SAFE/Backup/daily.0/Nas_pvz/smb/sys_bucks/Nas_pvz/#MTS/%d/ARHIV',
                     )


def download_all_dbf(urls=load_net_config.SMB_SRC_URLS,
                     file_patterns=load_net_config.DOWNLOAD_FILE_PATTERNS,
                     dst_path=load_net_config.DEST_PATH,
                     dst_file_ext=load_net_config.DEST_FILE_EXT):
    """
    Загрузить все файлы данных в виде DBF.
    @param urls: Список URL с которых необходимо произвести загрузку.
    @param file_patterns: Шаблоны загружаемых данных.
    @param dst_path: Результирующая локальная папка для загрузки.
    @param dst_file_ext: Поменять расширение файлов на указанное.
        Если None, то расширение меняться не будет.
    @return: True - Загрузка файлов прошла успешно.
        False - ошибка.
    """
    log.info(u'Запуск загрузки файлов')

    results = [False] * len(urls)
    try:
        for i, url in enumerate(urls):
            smb_results = list()
            if url.startswith(u'smb://'):
                smb = smbfunc.smb_connect(url)
                for pattern in file_patterns:
                    # Список имен загружаемых файлов
                    filenames = smbfunc.smb_listdir_filename(url, pattern, smb=smb)

                    for filename in filenames:
                        # Загрузка из samba ресурса
                        base_filename = os.path.splitext(filename)[0] + dst_file_ext
                        new_filename = os.path.join(dst_path, base_filename)
                        result = smbfunc.smb_download_file_rename(download_urls=(url, ), filename=filename, dst_filename=new_filename)
                        log.debug(u'Загрузка файла <%s>...%s' % (filename, u'ДА' if result else u'НЕТ'))
                        smb_results.append(result)
                smbfunc.smb_disconnect(smb)
                results[i] = all(smb_results)
            else:
                log.warning(u'Не поддерживаемый тип источника данных. URL <%s>' % url)
    except:
        log.fatal(u'Ошибка загрузки файлов')

    return all(results)


def download_archive_files(archive_year=None):
    """
    Загрузить архивные файлы за год.
    @param archive_year: Год загрузки. Если не указан, то берется текущий системный.
    @return: True/False
    """
    if archive_year is None:
        archive_year = datetime.date.today().year

    if isinstance(archive_year, datetime.date) or isinstance(archive_year, datetime.datetime):
        archive_year = archive_year.year

    urls = [url_fmt % archive_year for url_fmt in ARCH_SMB_URLS_FMT]
    return download_all_dbf(urls=urls, dst_file_ext='_%d.DBF' % archive_year)
