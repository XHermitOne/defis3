#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Функции загрузки файлов данных в виде DBF из сети.
"""

from ic.log import log
from . import load_net_config

__version__ = (0, 1, 1, 1)


def download_all_dbf(urls=load_net_config.SMB_SRC_URLS,
                     file_patters=load_net_config.DOWNLOAD_FILE_PATTERNS,
                     dst_path=load_net_config.DEST_PATH,
                     dst_file_ext=load_net_config.DEST_FILE_EXT):
    """
    Загрузить все файлы данных в виде DBF.
    @param urls: Список URL с которых необходимо произвести загрузку.
    @param file_patters: Шаблоны загружаемых данных.
    @param dst_path: Результирующая локальная папка для загрузки.
    @param dst_file_ext: Поменять расширение файлов на указанное.
        Если None, то расширение меняться не будет.
    @return: True - Загрузка файлов прошла успешно.
        False - ошибка.
    """
    return False
