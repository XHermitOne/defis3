#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
Функции работы с файлами.
"""

import sys
import os
import os.path
import hashlib
import fnmatch
import shutil
import pwd

from . import util
from ic.log import log

__version__ = (0, 1, 2, 2)


def createTxtFile(filename, txt=None):
    """
    Создать текстовый файл.
    @param filename: Имя создаваемого файла.
    @param txt: Текст по умолчанию записываемый в файл.
    @return: True/False.
    """
    txt = util.encodeText(txt)
    f = None
    try:
        if os.path.exists(filename):
            os.remove(filename)
        f = open(filename, 'w')
        if txt:
            f.write(txt)
        f.close()
        return True
    except:
        if f:
            f.close()
            f = None
        raise
    return False


def is_same_file_length(filename1, filename2):
    """
    Проверка что файл1 и файл2 совпадают.
    Проверка производиться по размеру файлу.
    @return: True/False.
    """
    if os.path.exists(filename1) and os.path.exists(filename2):
        file_size1 = os.path.getsize(filename1)
        file_size2 = os.path.getsize(filename2)
        if file_size1 != file_size2:
            return file_size1 == file_size2
        else:
            # Если размер файлов одинаков, то проверяем дополнительно контрольную сумму
            file1_check_sum = get_file_md5(filename1)
            file2_check_sum = get_file_md5(filename2)
            return file1_check_sum == file2_check_sum
    return False


def get_check_sum_file(filename):
    """
    Определение контрольной суммы файла.
        ВНИМАНИЕ! Для файлов большого размера скорее всего не применима функция,
        т.к. медленная.
    @param filename: Полное имя файла.
    @return: Контрольная сумма файла или None, если какая-либо ошибка.
    """
    if not os.path.exists(filename):
        print(u'File <%s> not found')
        return None

    f = None
    try:
        f = open(filename, 'rb')
        file_data = f.read()
        f.close()
        return hashlib.md5(file_data).hexdigest()
    except:
        if f:
            f.close()
            f = None
        raise
    return None


def get_file_md5(filename):
    """
    Вычисление контрольной суммы большого файла.
    Взято с http://yushakov.com/code-work/piton/vychislenie-kontrolnoj-summy-dlya-bolshogo-fajla/
    @param filename: Полное имя файла.
    @return: Контрольная сумма файла или None, если какая-либо ошибка.
    """
    md5_obj = hashlib.md5()

    f = None
    try:
        f = open(filename, 'rb')
        data = f.read(1024)
        while data:
            md5_obj.update(data)
            data = f.read(1024)
        f.close()
    except:
        if f:
            f.close()
            f = None
        return None
    return md5_obj.hexdigest()


def get_dir_filename_list(directory, filename_pattern=None, sort_filename=False):
    """
    Получить список имен файлов в папке по шаблону.
    @param directory: Полный путь до директории.
    @param filename_pattern: Шаблон имен файлов. Если не определен, то беруться все файлы.
    @param sort_filename: Произвести автоматическую сортировку списка по имени файлов?
    @return: Список полных имен файлов или None в случае ошибки.
    """
    if not os.path.exists(directory):
        # Папка не существует
        return None

    filenames = os.listdir(directory)
    # Получить имена файлов
    filenames = fnmatch.filter(filenames, filename_pattern)
    if sort_filename:
        filenames.sort()

    full_filenames = [os.path.join(directory, filename) for filename in filenames]
    return full_filenames


def get_home_path(username=None):
    """
    Определить домашнюю папку пользователя.
    """
    if sys.platform[:3].lower() == 'win':
        home = os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'])
    else:
        if username is None:
            home = os.environ['HOME']
        else:
            user_struct = pwd.getpwnam(username)
            home = user_struct.pw_dir
    return home


def normal_path(path, username=None):
    """
    Нормировать путь.
    @param path: Путь.
    @param username: Имя пользователя.
    """
    home_dir = get_home_path(username)
    return os.path.abspath(os.path.normpath(path.replace('~', home_dir)))


def copyFile(filename, new_filename, bRewrite=True):
    """
    Создает копию файла с новым именем.
    @type filename: C{string}
    @param filename: Полное имя файла.
    @type new_filename: C{string}
    @param new_filename: Новое имя файла.
    @type bRewrite: C{bool}
    @param bRewrite: True-если новый файл уже существует,
        то переписать его молча. False-если новый файл уже существует,
        то не перезаписывать его а оставить старый.
    @return: Возвращает результат выполнения операции True/False.
    """
    try:
        # Проверка существования файла-источника
        if not os.path.isfile(filename):
            print('WARNING! File %s not exist for copy' % filename)
            return False

        # Проверка перезаписи уже существуещего файла
        if not bRewrite:
            print('WARNING! File %s exist and not rewrite' % filename)
            return False

        # Создать результирующую папку
        dir = os.path.dirname(new_filename)
        if not os.path.exists(dir):
            os.makedirs(dir)
        shutil.copyfile(filename, new_filename)
        return True
    except IOError:
        print('ERROR! Copy file %s I/O error' % filename)
        return False


def copyToDir(filename, dst_dirname, bRewrite=True):
    """
    Копировать файл в папку.
    @type filename: C{string}
    @param filename: Имя файла.
    @type dst_dirname: C{string}
    @param dst_dirname: Папка в которую необходимо скопировать.
    @type bRewrite: C{bool}
    @param bRewrite: True-если новый файл уже существует,
        то переписать его молча. False-если новый файл уже существует,
        то не перезаписывать его а оставить старый.
    @return: Возвращает результат выполнения операции True/False.
    """
    return copyFile(filename,
                    os.path.normpath(dst_dirname + '/' + os.path.basename(filename)), bRewrite)


def changeExt(filename, new_ext):
    """
    Поменять у файла расширение.
    @type filename: C{string}
    @param sFileName_: Полное имя файла.
    @type new_ext: C{string}
    @param new_ext: Новое расширение файла (Например: '.bak').
    @return: Возвращает новое полное имя файла.
    """
    try:
        new_name = os.path.splitext(filename)[0] + new_ext
        if os.path.isfile(new_name):
            os.remove(new_name)     # если файл существует, то удалить
        if os.path.exists(filename):
            os.rename(filename, new_name)
            return new_name
    except:
        print('ERROR! Change ext file %s' % filename)
        raise
    return None


def fileList(src_dirname):
    """
    Список файлов в директории с полными путями.
    @param src_dirname: Исходная директория.
    @return: Список файлов.
    """
    return [norm_path(src_dirname + '/' + filename) for filename in os.listdir(norm_path(src_dirname))]


def norm_path(cur_path, delim=os.path.sep):
    """
    Удалить двойные разделител из пути.
    @type cur_path: C{string}
    @param cur_path: Путь
    @type delim: C{string}
    @param delim: Разделитель пути
    """
    cur_path = cur_path.replace('~', getHomeDir())
    dbl_delim = delim + delim
    while dbl_delim in cur_path:
        cur_path = cur_path.replace(dbl_delim, delim)
    return cur_path


def getHomeDir():
    """
    Папка HOME.
    @return: Строку-путь до папки пользователя.
    """
    return get_home_path()


def getProfilePath(profile_dirname=u''):
    """
    Папка сохраненных параметров программы.
        Находиться в HOME/{{PROFILE_DIRNAME}}.
        Функция сразу провеяет если этой папки нет,
        то создает ее.
    @param profile_dirname: Имя папки профиля. Если не определена то берется домашняя папка.
    """
    home_dir = getHomeDir()

    profile_path = os.path.normpath(os.path.join(home_dir, profile_dirname))
    if not os.path.exists(profile_path):
        os.makedirs(profile_path)
    return profile_path


def removeFile(filename):
    """
    Удалить файл.
    @param filename: Полное имя файла.
    @return: True - файл успешно удален / False - ошибка удаления файла.
    """
    try:
        if not os.path.exists(filename):
            log.warning(u'Удаление: файл <%s> не существует' % filename)
            return False

        os.remove(filename)
        return True
    except OSError:
        log.fatal(u'Ошибка удаления файла <%s>' % filename)
    return False
