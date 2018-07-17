#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Функции работы с файлами.
"""

import sys
import os
import os.path
import hashlib
import fnmatch
import pwd
from . import util

__version__ = (0, 0, 7, 1)


def createTxtFile(FileName_,Txt_=None):
    """
    Создать текстовый файл.
    @param FileName_: Имя создаваемого файла.
    @param Txt_: Текст по умолчанию записываемый в файл.
    @return: True/False.
    """
    Txt_ = util.encodeText(Txt_)
    f = None
    try:
        if os.path.exists(FileName_):
            os.remove(FileName_)
        f = open(FileName_, 'w')
        if Txt_:
            f.write(Txt_)
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


def get_home_path(UserName_=None):
    """
    Определить домашнюю папку пользователя.
    """
    if sys.platform[:3].lower() == 'win':
        home = os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'])
    else:
        if UserName_ is None:
            home = os.environ['HOME']
        else:
            user_struct = pwd.getpwnam(UserName_)
            home = user_struct.pw_dir
    return home


def normal_path(path, sUserName=None):
    """
    Нормировать путь.
    @param path: Путь.
    @param sUserName: Имя пользователя.
    """
    home_dir = get_home_path(sUserName)
    return os.path.abspath(os.path.normpath(path.replace('~', home_dir)))
