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

__version__ = (0, 1, 2, 1)


def createTxtFile(FileName_, Txt_=None):
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


def copyFile(sFileName, sNewFileName, bRewrite=True):
    """
    Создает копию файла с новым именем.
    @type sFileName: C{string}
    @param sFileName: Полное имя файла.
    @type sNewFileName: C{string}
    @param sNewFileName: Новое имя файла.
    @type bRewrite: C{bool}
    @param bRewrite: True-если новый файл уже существует,
        то переписать его молча. False-если новый файл уже существует,
        то не перезаписывать его а оставить старый.
    @return: Возвращает результат выполнения операции True/False.
    """
    try:
        # Проверка существования файла-источника
        if not os.path.isfile(sFileName):
            print('WARNING! File %s not exist for copy' % sFileName)
            return False

        # Проверка перезаписи уже существуещего файла
        if not bRewrite:
            print('WARNING! File %s exist and not rewrite' % sFileName)
            return False

        # Создать результирующую папку
        dir = os.path.dirname(sNewFileName)
        if not os.path.exists(dir):
            os.makedirs(dir)
        shutil.copyfile(sFileName, sNewFileName)
        return True
    except IOError:
        print('ERROR! Copy file %s I/O error' % sFileName)
        return False


def copyToDir(sFileName, sDestDir, bRewrite=True):
    """
    Копировать файл в папку.
    @type sFileName: C{string}
    @param sFileName: Имя файла.
    @type sDestDir: C{string}
    @param sDestDir: Папка в которую необходимо скопировать.
    @type bRewrite: C{bool}
    @param bRewrite: True-если новый файл уже существует,
        то переписать его молча. False-если новый файл уже существует,
        то не перезаписывать его а оставить старый.
    @return: Возвращает результат выполнения операции True/False.
    """
    return copyFile(sFileName,
                    os.path.normpath(sDestDir+'/'+os.path.basename(sFileName)), bRewrite)


def changeExt(sFileName, sNewExt):
    """
    Поменять у файла расширение.
    @type sFileName: C{string}
    @param sFileName_: Полное имя файла.
    @type sNewExt: C{string}
    @param sNewExt: Новое расширение файла (Например: '.bak').
    @return: Возвращает новое полное имя файла.
    """
    try:
        new_name = os.path.splitext(sFileName)[0]+sNewExt
        if os.path.isfile(new_name):
            os.remove(new_name)     # если файл существует, то удалить
        if os.path.exists(sFileName):
            os.rename(sFileName, new_name)
            return new_name
    except:
        print('ERROR! Change ext file %s' % sFileName)
        raise
    return None


def fileList(sDir):
    """
    Список файлов в директории с полными путями.
    @param sDir: Исходная директория.
    @return: Список файлов.
    """
    return [norm_path(sDir+'/'+filename) for filename in os.listdir(norm_path(sDir))]


def norm_path(sPath, sDelim=os.path.sep):
    """
    Удалить двойные разделител из пути.
    @type sPath: C{string}
    @param sPath: Путь
    @type sDelim: C{string}
    @param sDelim: Разделитель пути
    """
    sPath = sPath.replace('~', getHomeDir())
    dbl_delim = sDelim + sDelim
    while dbl_delim in sPath:
        sPath = sPath.replace(dbl_delim, sDelim)
    return sPath


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
            return None

        os.remove(filename)
        return True
    except OSError:
        log.fatal(u'Ошибка удаления файла <%s>' % filename)
    return False
