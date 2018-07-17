#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Функции работы с файлами на расшаренных ресурсах SAMBA.
"""

import os
import os.path
import smbclient
import urlparse

from ic.log import log
from ic.utils import ic_file

__version__ = (0, 0, 2, 2)

DEFAULT_WORKGROUP = 'WORKGROUP'


def smb_url_path_split(smb_url):
    """
    Корректная разбивка пути URL ресурса SMB на составляющие.
    Если в пути встречается символ <#> то библиотека парсинга URL воспринимает далее 
    стоящие символы как fragment. Это надо учитывать. 
    Для этого предназначена эта функция.
    @param smb_url: Объект ParseResult библиотеки urlparse.
    @return: Список составляющих пути к SMB ресурсу.
    """
    path_list = smb_url.path.split(os.path.sep)
    if smb_url.fragment:
        fragment_path_list = smb_url.fragment.split(os.path.sep)
        fragment_path_list[0] = u'#' + fragment_path_list[0]
        path_list += fragment_path_list
    return path_list


def smb_download_file(download_urls=None, filename=None, out_path=None, re_write=True):
    """
    Найти и загрузить файл.
    @param download_urls: Список путей поиска файла.
        Пример:
        ('smb://xhermit@SAFE/Backup/daily.0/Nas_pvz/smb/sys_bucks/Nas_pvz/NSI/',
         'smb://xhermit@TELEMETRIA/share/install/', ...
         )
        Параметр может задаваться строкой. В таком случае считаем что URL один.
    @param filename: Относительное имя файла.
        Например:
        '/2017/FDOC/RC001.DCM'
    @param out_path: Локальный путь для сохранения файла.
    @param re_write: Перезаписать локальный файл, если он уже существует?
    @return: True - Произошла загрузка, False - ничего не загружено.
    """
    if download_urls is None:
        log.warning(u'Не определены пути поиска файла на SMB ресурсах')
        return False
    elif isinstance(download_urls, str) or isinstance(download_urls, unicode):
        # У нас 1 URL
        download_urls = [download_urls]

    if out_path is None:
        out_path = ic_file.getPrjProfilePath()

    result = False
    smb = None
    for download_url in download_urls:
        try:
            url = urlparse.urlparse(download_url)
            download_server = url.hostname
            download_share = url.path.split(os.path.sep)[1]
            download_username = url.username
            download_password = url.password

            smb = smbclient.SambaClient(server=download_server,
                                        share=download_share,
                                        username=download_username,
                                        password=download_password,
                                        domain=DEFAULT_WORKGROUP)

            log.info(u'Установлена связь с SMB ресурсом')
            log.info(u'\tсервер <%s>' % download_server)
            log.info(u'\tпапка <%s>' % download_share)
            log.info(u'\tпользователь <%s>' % download_username)
            log.info(u'\tURL <%s>' % download_url)

            # Получить имена загружаемых файлов
            path_list = smb_url_path_split(url)
            if filename is None:
                filename = path_list[-1]
                log.debug(u'\tФайл: <%s>' % filename)
                path_list = path_list[2:]
            else:
                path_list = path_list[2:] + [filename]
            download_file = os.path.join(*path_list)

            log.info(u'Загрузка файла <%s>' % download_file)

            dst_filename = os.path.join(out_path, filename)
            if os.path.exists(dst_filename) and re_write:
                log.info(u'Удаление файла <%s>' % dst_filename)
                try:
                    os.remove(dst_filename)
                except:
                    log.fatal(u'Ошибка удаления файла <%s>' % dst_filename)
            dst_path = os.path.dirname(dst_filename)
            if not os.path.exists(dst_path):
                try:
                    os.makedirs(dst_path)
                    log.info(u'Создание папки <%s>' % dst_path)
                except:
                    log.fatal(u'Ошибка создания папки <%s>' % dst_path)

            # ВНИМАНИЕ! Найден глюк библиотеки smbclient:
            # В списке файлов могут пропадать файлы большого размера.
            # Поэтому проверку на существование файла в SMB ресурсе не производим
            # а сразу пытаемся его загрузить.
            try:
                smb.download(download_file, dst_filename)
                log.info(u'Файл <%s> загружен' % download_file)
                result = True
            except:
                log.warning(u'''При возникновении ошибки в smbclient'e
возможно проблема в самой библиотеке pysmbclient.
Решение:
    В файле /usr/local/lib/python2.7/dist-packages/smbclient.py
    в вызове функции subprocess.Popen() убрать параметр <shell=True> 
    или поставить в False.
                ''')
                log.fatal(u'SMB. Ошибка загрузки SMB файла <%s>' % download_file)
                result = False

            smb.close()
            smb = None
            break
        except:
            if smb:
                smb.close()
            log.fatal(u'Ошибка загрузки файла <%s> из SMB ресурса <%s>' % (filename, download_url))
            result = False

    return result


def smb_download_file_rename(download_urls=None, filename=None, dst_filename=None, re_write=True):
    """
    Найти и загрузить файл с переименованием.
    @param download_urls: Список путей поиска файла.
        Пример:
        ('smb://xhermit@SAFE/Backup/daily.0/Nas_pvz/smb/sys_bucks/Nas_pvz/NSI/',
         'smb://xhermit@TELEMETRIA/share/install/', ...
         )
        Параметр может задаваться строкой. В таком случае считаем что URL один.
    @param filename: Относительное имя файла.
        Например:
        '/2017/FDOC/RC001.DCM'
    @param dst_filename: Новое полное наименование для сохранения файла.
    @param re_write: Перезаписать локальный файл, если он уже существует?
    @return: True - Произошла загрузка, False - ничего не загружено.
    """
    # Сначала просто загрузим файл
    tmp_path = os.tmpnam()
    result = smb_download_file(download_urls, filename, tmp_path, re_write)

    if result:
        new_filename = None
        try:
            # Успешно загрузили
            # Перименование файла
            new_filename = os.path.join(tmp_path, filename)
            ic_file.icCopyFile(new_filename, dst_filename, re_write)

            # После копирования удаляем временную директорию
            ic_file.RemoveTreeDir(tmp_path, True)

            return True
        except:
            log.fatal(u'Ошибка переименования файла <%s> -> <%s>' % (new_filename, dst_filename))

    return False
