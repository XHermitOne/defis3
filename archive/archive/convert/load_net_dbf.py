#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Функции загрузки файлов данных в виде DBF из сети.
"""

import os
import os.path
import datetime

from ic.log import log
from ic.dlg import ic_dlg
from . import load_net_config
from ic.utils import smbfunc
from ic.utils import filefunc

__version__ = (0, 1, 2, 1)


def download_all_dbf(urls=load_net_config.SMB_SRC_URLS,
                     file_patterns=load_net_config.DOWNLOAD_FILE_PATTERNS,
                     dst_path=load_net_config.DEST_PATH,
                     dst_file_ext=load_net_config.DEST_FILE_EXT,
                     bProgress=True):
    """
    Загрузить все файлы данных в виде DBF.
    @param urls: Список URL с которых необходимо произвести загрузку.
    @param file_patterns: Шаблоны загружаемых данных.
    @param dst_path: Результирующая локальная папка для загрузки.
    @param dst_file_ext: Поменять расширение файлов на указанное.
        Если None, то расширение меняться не будет.
    @param bProgress: Открыть прогрессбар загрузки.
    @return: True - Загрузка файлов прошла успешно.
        False - ошибка.
    """
    log.info(u'Запуск загрузки файлов')

    results = [False] * len(urls)
    try:
        if bProgress:
            ic_dlg.icOpenProgressDlg(title=u'Загрузка файлов',
                                     prompt_text=u'Загрузка файлов...',
                                     min_value=0, max_value=100)

        for i, url in enumerate(urls):
            smb_results = list()
            if url.startswith(u'smb://'):
                smb = smbfunc.smb_connect(url)
                for pattern in file_patterns:
                    # Список имен загружаемых файлов
                    filenames = smbfunc.smb_listdir_filename(url, pattern, smb=smb)

                    for filename in filenames:
                        if bProgress:
                            ic_dlg.icStepProgressDlg(new_prompt_text=u'Загрузка файла <%s>' % filename)

                        # Загрузка из samba ресурса
                        name, ext = os.path.splitext(filename)
                        base_filename = name + ext.upper().replace('.', '_') + dst_file_ext
                        new_filename = os.path.join(dst_path, base_filename)
                        result = smbfunc.smb_download_file_rename(download_urls=(url, ), filename=filename, dst_filename=new_filename)
                        log.debug(u'Загрузка файла <%s>...%s' % (filename, u'ДА' if result else u'НЕТ'))
                        smb_results.append(result)
                smbfunc.smb_disconnect(smb)
            else:
                # Загрузка из локальной папки
                for pattern in file_patterns:
                    # Список имен загружаемых файлов
                    filenames = filefunc.get_dir_filename_list(url, pattern)

                    for filename in filenames:
                        if bProgress:
                            ic_dlg.icStepProgressDlg(new_prompt_text=u'Загрузка файла <%s>' % filename)

                        name, ext = os.path.splitext(filename)
                        base_filename = name + ext.upper().replace('.', '_') + dst_file_ext
                        new_filename = os.path.join(dst_path, base_filename)
                        result = filefunc.copyFile(filename, new_filename)
                        log.debug(u'Копирование файла <%s> -> <%s> ... %s' % (filename, new_filename,  u'ДА' if result else u'НЕТ'))
                        smb_results.append(result)
            results[i] = all(smb_results)
    except:
        log.fatal(u'Ошибка загрузки файлов')

    if bProgress:
        ic_dlg.icCloseProgressDlg()

    return all(results)


def download_archive_files(archive_year=None, archive_month=None):
    """
    Загрузить архивные файлы за год.
    @param archive_year: Год загрузки. Если не указан, то берется текущий системный.
    @param archive_month: Месяц загрузки. Если не указан, то берется текущий системный.
    @return: True/False
    """
    if archive_year is None:
        archive_year = datetime.date.today().year
    if archive_month is None:
        archive_month = datetime.date.today().month

    if isinstance(archive_year, datetime.date) or isinstance(archive_year, datetime.datetime):
        archive_year = archive_year.year

    if isinstance(archive_month, datetime.date) or isinstance(archive_month, datetime.datetime):
        archive_month = archive_month.month

    urls = [url_fmt % archive_year for url_fmt in load_net_config.ARCH_SMB_URLS_FMT]
    return download_all_dbf(urls=urls, dst_file_ext='_%d.DBF' % archive_year)
