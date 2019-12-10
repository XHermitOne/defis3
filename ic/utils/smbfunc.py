#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
Функции работы с файлами на расшаренных ресурсах SAMBA.

URL SMB ресурса задается в следующем формате:
smb://[[<domain>;]<username>[:<password>]@]<server>[:<port>][/[<share>[/[<path>]]]

Например:
smb://workgroup;user:password@server/share/folder/file.txt
"""

import os
import os.path
import tempfile
import fnmatch
import shutil
import smbclient
import urllib.parse
import locale
import datetime

from ic.log import log
from ic.utils import filefunc

__version__ = (0, 1, 3, 1)

DEFAULT_WORKGROUP = 'WORKGROUP'

ANONYMOUS_USERNAME = 'guest'


def smb_url_path_split(smb_url):
    """
    Корректная разбивка пути URL ресурса SMB на составляющие.
    Если в пути встречается символ <#> то библиотека парсинга URL воспринимает далее 
    стоящие символы как fragment. Это надо учитывать. 
    Для этого предназначена эта функция.
    :param smb_url: Объект ParseResult библиотеки urlparse.
    :return: Список составляющих пути к SMB ресурсу.
    """
    path_list = smb_url.path.split(os.path.sep)
    if smb_url.fragment:
        fragment_path_list = smb_url.fragment.split(os.path.sep)
        fragment_path_list[0] = u'#' + fragment_path_list[0]
        path_list += fragment_path_list
    return path_list


def get_smb_path_from_url(url):
    """
    Определить путь к SMB ресурсу по URL.
    :param url: URL samba ресурса.
    :return: Путь к samba ресурсу выбранный из URL.
    """
    url = urllib.parse.urlparse(url)
    path_list = smb_url_path_split(url)
    path_list = path_list[2:]
    smb_path = os.path.join(*path_list)
    return smb_path


def smb_download_file(download_urls=None, filename=None, out_path=None, re_write=True, smb=None):
    """
    Найти и загрузить файл.
    :param download_urls: Список путей поиска файла.
        Пример:
        ('smb://xhermit@SAFE/Backup/daily.0/Nas_pvz/smb/sys_bucks/Nas_pvz/NSI/',
         'smb://xhermit@TELEMETRIA/share/install/', ...
         )
        Параметр может задаваться строкой. В таком случае считаем что URL один.
    :param filename: Относительное имя файла.
        Например:
        '/2017/FDOC/RC001.DCM'
    :param out_path: Локальный путь для сохранения файла.
    :param re_write: Перезаписать локальный файл, если он уже существует?
    :param smb: Объект samba ресурса в случае уже открытого ресурса.
    :return: True - Произошла загрузка, False - ничего не загружено.
    """
    if download_urls is None:
        log.warning(u'Не определены пути поиска файла на SMB ресурсах')
        return False
    elif isinstance(download_urls, str):
        # У нас 1 URL
        download_urls = [download_urls]

    if out_path is None:
        out_path = filefunc.getPrjProfilePath()

    result = False
    do_close = False
    for download_url in download_urls:
        try:
            if smb is None:
                smb = smb_connect(download_url)
                do_close = True

            # Получить имена загружаемых файлов
            url = urllib.parse.urlparse(download_url)
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
    В файле /usr/local/lib/pythonX.X/dist-packages/smbclient.py
    в вызове функции subprocess.Popen() убрать параметр <shell=True> 
    или поставить в False.
                ''')
                log.fatal(u'SMB. Ошибка загрузки SMB файла <%s>' % download_file)
                result = False

            if do_close:
                smb_disconnect(smb)
            break
        except:
            if do_close:
                smb_disconnect(smb)
            log.fatal(u'Ошибка загрузки файла <%s> из SMB ресурса <%s>' % (filename, download_url))
            result = False

    return result


def smb_download_file_rename(download_urls=None, filename=None, dst_filename=None, re_write=True, smb=None):
    """
    Найти и загрузить файл с переименованием.
    :param download_urls: Список путей поиска файла.
        Пример:
        ('smb://xhermit@SAFE/Backup/daily.0/Nas_pvz/smb/sys_bucks/Nas_pvz/NSI/',
         'smb://xhermit@TELEMETRIA/share/install/', ...
         )
        Параметр может задаваться строкой. В таком случае считаем что URL один.
    :param filename: Относительное имя файла.
        Например:
        '/2017/FDOC/RC001.DCM'
    :param dst_filename: Новое полное наименование для сохранения файла.
    :param re_write: Перезаписать локальный файл, если он уже существует?
    :param smb: Объект samba ресурса в случае уже открытого ресурса.
    :return: True - Произошла загрузка, False - ничего не загружено.
    """
    # Сначала просто загрузим файл
    tmp_path = tempfile.mktemp()
    result = smb_download_file(download_urls, filename, tmp_path, re_write, smb)

    if result:
        new_filename = None
        try:
            # Успешно загрузили
            # Перименование файла
            new_filename = os.path.join(tmp_path, filename)
            filefunc.copyFile(new_filename, dst_filename, re_write)

            # После копирования удаляем временную директорию
            shutil.rmtree(tmp_path, True)

            return True
        except:
            log.fatal(u'Ошибка переименования файла <%s> -> <%s>' % (new_filename, dst_filename))

    return False


def smb_connect(url):
    """
    Соединиться с samba ресурсом.
    :param url: URL samba ресурса.
    :return: Объект SAMBA ресурса или None в случае ошибки.
    """
    smb = None
    try:
        smb_url = urllib.parse.urlparse(url)
        download_server = smb_url.hostname
        download_share = smb_url.path.split(os.path.sep)[1]
        # Если не указан пользователь, то осуществляем вход
        download_username = smb_url.username if smb_url.username else ANONYMOUS_USERNAME
        download_password = smb_url.password

        smb = smbclient.SambaClient(server=download_server,
                                    share=download_share,
                                    username=download_username,
                                    password=download_password,
                                    domain=DEFAULT_WORKGROUP)

        log.info(u'Установлена связь с SMB ресурсом')
        log.info(u'\tсервер <%s>' % download_server)
        log.info(u'\tпапка <%s>' % download_share)
        log.info(u'\tпользователь <%s>' % download_username)
        log.info(u'\tURL <%s>' % str(url))
    except:
        log.fatal(u'Ошибка соединения с samba ресурсом. URL <%s>' % str(url))
    return smb


def smb_disconnect(smb):
    """
    Закрыть соединение с samba ресурсом.
    :param smb: Объект SAMBA ресурса.
    :return: True/False.
    """
    try:
        if smb:
            log.info(u'Закрыто соединение с SMB ресурсом')
            smb.close()
            return True
    except:
        log.fatal(u'Ошибка закрытия соединения с samba ресурсом')
    return False


def smb_listdir_filename(url=None, filename_pattern=None, smb=None):
    """
    Список файлов SMB ресурса.
    :param url: URL samba ресурса.
    :param filename_pattern: Выбрать имена файлов по указанному шаблону.
        Шаблон файлов указывается как *.DBF например.
    :param smb: Объект samba ресурса в случае уже открытого ресурса.
    :return: Список имен файлов samba ресурса.
        Функция возвращает только имена файлов.
        Имена папок не включаются в список.
    """
    filenames = list()

    if url is None:
        log.warning(u'Не указан URL samba ресурса для определения списка файлов')
        return filenames

    smb_path = get_smb_path_from_url(url)
    # log.debug(u'Папка SMB ресурса <%s>' % smb_path)
    try:
        if smb is not None:
            # Ресурс уже открыт
            filenames = smb.listdir(smb_path)
        else:
            try:
                smb = smb_connect(url)
                filenames = smb.listdir(smb_path)
                smb_disconnect(smb)
            except:
                smb_disconnect(smb)
                log.fatal(u'Ошибка получения списка файлов samba ресурса. URL <%s>' % url)
    except:
        log.fatal(u'Ошибка получения списка файлов samba ресурса')

    # ВНИМАНИЕ! В библиотеке smbclient возможна ошибка
    # с получением корректных имен файлов:
    # В конец имени файла добавляется '                           N'
    # Здесь пытаемся нивелировать эту ошибку
    filenames = [filename.strip('                           N').strip() for filename in filenames]
    # log.debug(u'SMB. Список файлов %s' % str(filenames))
    if filename_pattern:
        filenames = [filename for filename in filenames if fnmatch.fnmatch(filename, filename_pattern)]
        # log.debug(u'SMB. Отфильтрованные файлы %s' % str(filenames))
    return filenames


DEFAULT_SMB_DATETIME_FMT = '%a %b %d %H:%M:%S %Y'

def _smb_to_datetime(str_datetime, bSetLocale=False):
    """
    Преобразовать время из строкового варианта в datetime.
    :param str_datetime: Время в строковом виде.
        Например 'Пн июл 29 17:23:39 2019 +07'.
    :param bSetLocale: Установить системную локаль?
    :return: datetime.datetime или None в случае ошибки.
    """
    if bSetLocale:
        # Для корректного преобразования времени необходимо установить системную локаль
        locale.setlocale(locale.LC_ALL, '')

    try:
        # Удаляем информацию о временной зоне
        str_datetime = str_datetime[:-str_datetime[::-1].index(' ') - 1]
        return datetime.datetime.strptime(str_datetime, DEFAULT_SMB_DATETIME_FMT)
    except:
        log.fatal(u'Ошибка преобразования <%s> к виду datetime' % str_datetime)
    return None


def get_smb_file_info(url=None, filename=None, smb=None, bToDateTime=True):
    """
    Получить всю информацию о файле в виде структуры.
    :param url: URL samba ресурса.
    :param filename: Имя файла. Напрмер /2019/TEST.DBF
    :param smb: Объект samba ресурса в случае уже открытого ресурса.
    :param bToDateTime: Преобразовать сразу время из строкового представления в datetime?
    :return: Словарь информации о файле:
        {
            'create_time': Время создания файла,
            'access_time': Время последнего доступа к файлу,
            'write_time': Время сохранения файла,
            'change_time': Время изменения файла,
            ...
        }
    """
    file_info = dict()
    try:
        if smb is not None:
            # Ресурс уже открыт
            file_info = smb.info(filename)
        else:
            try:
                smb = smb_connect(url)
                file_info = smb.info(filename)
                smb_disconnect(smb)
            except:
                smb_disconnect(smb)
                log.fatal(u'Ошибка получения информации о файле samba ресурса. URL <%s>' % url)
    except:
        log.fatal(u'Ошибка получения информации о файле <%s> samba ресурса' % filename)

    if bToDateTime:
        # Преобразуем сразу время из строкового представления в datetime
        # Для корректного преобразования времени необходимо установить локаль
        locale.setlocale(locale.LC_ALL, '')

        if 'create_time' in file_info:
            file_info['create_time'] = _smb_to_datetime(file_info['create_time'])
        if 'access_time' in file_info:
            file_info['access_time'] = _smb_to_datetime(file_info['access_time'])
        if 'write_time' in file_info:
            file_info['write_time'] = _smb_to_datetime(file_info['write_time'])
        if 'change_time' in file_info:
            file_info['change_time'] = _smb_to_datetime(file_info['change_time'])

    return file_info


def isdir_smb(url=None, path=None, smb=None):
    """
    Проверка на то что файловый объект является директорией.
    :param url: URL samba ресурса.
    :param path: Имя файлового объекта. Напрмер /2019/TEST.DBF
    :param smb: Объект samba ресурса в случае уже открытого ресурса.
    :return: True - Это директория. False - нет.
    """
    is_dir = None
    try:
        if smb is not None:
            # Ресурс уже открыт
            is_dir = smb.isdir(path)
        else:
            try:
                smb = smb_connect(url)
                is_dir = smb.isdir(path)
                smb_disconnect(smb)
            except:
                smb_disconnect(smb)
                log.fatal(u'Ошибка проверки наличия директории <%s> samba ресурса. URL <%s>' % (path, url))
    except:
        log.fatal(u'Ошибка проверки наличия директории <%s> samba ресурса' % path)

    return is_dir


def isfile_smb(url=None, path=None, smb=None):
    """
    Проверка на то что файловый объект является файлом.
    :param url: URL samba ресурса.
    :param path: Имя файлового объекта. Напрмер /2019/TEST.DBF
    :param smb: Объект samba ресурса в случае уже открытого ресурса.
    :return: True - Это файл. False - нет.
    """
    is_file = None
    try:
        if smb is not None:
            # Ресурс уже открыт
            is_file = smb.isfile(path)
        else:
            try:
                smb = smb_connect(url)
                is_file = smb.isfile(path)
                smb_disconnect(smb)
            except:
                smb_disconnect(smb)
                log.fatal(u'Ошибка проверки наличия файла <%s> samba ресурса. URL <%s>' % (path, url))
    except:
        log.fatal(u'Ошибка проверки наличия файла <%s> samba ресурса' % path)

    return is_file
