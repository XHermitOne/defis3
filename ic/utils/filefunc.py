#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль функций пользователя для работы с файлами.
"""

# --- Подключение пакетов ---
import wx
import os
import os.path
import tempfile
import shutil   # Для реализации высокоуровневых функций работы с файлами
import sys
import time
import glob     # Для поиска файлов по маске/шаблону
import platform
import hashlib
import fnmatch
import pwd

from ic.log import log
from ic.dlg import dlgfunc

import ic.config

__version__ = (1, 2, 1, 1)

_ = wx.GetTranslation


# --- Функции пользователя ---
def getMakeFileTime(filename):
    """
    Время создания файла. Если файла не существует то 0.
    """
    if os.path.exists(filename):
        return os.path.getmtime(filename)
    return 0


def makeDirs(path):
    """
    Корректное создание каталогов по цепочке.
    """
    try:
        if not os.path.exists(path):
            return os.makedirs(path)
    except:
        log.fatal(u'Ошибка создания каталога <%s>' % path)


def changeExt(filename, new_ext):
    """
    Поменять у файла расширение.
    :param filename: Полное имя файла.
    :param new_ext: Новое расширение файла (Например: '.bak').
    :return: Возвращает новое полное имя файла.
    """
    try:
        new_name = os.path.splitext(filename)[0] + new_ext
        if os.path.isfile(new_name):
            os.remove(new_name)     # если файл существует, то удалить
        if os.path.exists(filename):
            os.rename(filename, new_name)
            return new_name
    except:
        log.fatal(u'Ошибка изменения расширения файла <%s> -> <%s>' % (filename, new_ext))
    return None


def copyFile(filename, new_filename, bRewrite=True):
    """
    Создает копию файла с новым именем.
    :param filename: Полное имя файла.
    :param new_filename: Новое имя файла.
    :param bRewrite: True-если новый файл уже существует, 
        то переписать его молча. False-если новый файл уже существует, 
        то выдать сообщение о подтверждении перезаписи файла.
    :return: Возвращает результат выполнения операции True/False.
    """
    try:
        # --- Проверка существования файла-источника ---
        if not os.path.exists(filename):
            msg = u'Копирование <%s> -> <%s>. Исходный файл <%s> не существует.' % (filename, new_filename, filename)
            log.warning(msg)
            dlgfunc.openWarningBox(u'ОШИБКА', msg)
            return False

        # --- Проверка копирования файла в самого себя ---
        if os.path.exists(filename) and filename == new_filename:
            log.warning(u'Копирование файла <%s> самого в себя' % filename)
            return False

        makeDirs(os.path.dirname(new_filename))

        # --- Проверка перезаписи уже существуещего файла ---
        # Выводить сообщение что файл уже существует?
        if not bRewrite:
            # Файл уже существует?
            if os.path.exists(new_filename):
                if dlgfunc.getAskDlg(u'КОПИРВАНИЕ',
                                   u'Файл <%s> уже существует. Переписать?' % new_filename) == wx.NO:
                    return False
        else:
            if os.path.exists(new_filename):
                os.remove(new_filename)

        # --- Реализация копирования файла ---
        if os.path.exists(filename) and os.path.exists(new_filename) and os.path.samefile(filename, new_filename):
            log.warning(u'Попытка скопировать файл <%s> самого в себя' % filename)
        else:
            shutil.copyfile(filename, new_filename)
        return True
    except:
        log.fatal(u'Ошибка копирования файла <%s> -> <%s>' % (filename, new_filename))
        return False


def createBAKFile(filename, bak_file_ext='.bak'):
    """
    Создает копию файла с новым расширением BAK.
    :param filename: Полное имя файла.
    :param bak_file_ext: Расширение BAK файла.
    :return: Возвращает результат выполнения операции True/False.
    """
    try:
        if not os.path.exists(filename):
            log.warning(u'Не найден файл <%s> для создания его резервной копии' % filename)
            return False

        bak_name = os.path.splitext(filename)[0] + bak_file_ext
        return copyFile(filename, bak_name)
    except:
        log.fatal(u'Ошибка создания BAK файла <%s>' % filename)
        return False


def getSubDirs(path):
    """
    Функция возвращает список поддиректорий.
    :param path: Дирeкторий.
    :return: В случае ошибки возвращает None.
    """
    try:
        if not os.path.exists(path):
            log.warning(u'Путь <%s> не найден для определения списка поддриекторий' % path)
            return list()
        dir_list = [os.path.join(path, cur_name) for cur_name in os.listdir(path)]
        dir_list = [cur_path for cur_path in dir_list if os.path.isdir(cur_path)]
        return dir_list
    except:
        log.fatal(u'Ошибка чтения списка поддиректорий <%s>' % path)
    return None


def getSubDirsFilter(path, dir_filters=('.svn', '.SVN', '.Svn')):
    """
    Функция возвращает список поддиректорий с отфильтрованными папками.
    :param path: Дирикторий.
    :param dir_filters: Список недопустимых имен папок.
    :return: В случае ошибки возвращает None.
    """
    try:
        if not os.path.exists(path):
            log.warning(u'Не найден путь <%s> для определения списка поддиректорий' % path)
            return list()

        dir_list = [os.path.join(path, path) for path in os.listdir(path)]
        dir_list = [path for path in dir_list if os.path.isdir(path)]
        dir_list = [d for d in dir_list if _pathFilter(d, dir_filters)]
        return dir_list
    except:
        log.fatal(u'Ошибка чтения списка поддиректорий <%s>' % path)
        return None


def getSubDirsFilterSVN(path):
    """
    Функция возвращает список поддиректорий с отфильтрованными папками Subversion.
    :param path: Дирикторий.
    :param filename_filter: Список недопустимых имен папок.
    :return: В случае ошибки возвращает None.
    """
    return getSubDirsFilter(path)


def getFilenames(path):
    """
    Функция возвращает список файлов в директории.
    :param path: Дирикторий.
    :return: В случае ошибки возвращает None.
    """
    try:
        if not os.path.exists(path):
            log.warning(u'Не найден путь <%s> для определения списка файлов директории' % path)
            return list()

        file_list = None
        file_list = [os.path.join(path, x.lower()) for x in os.listdir(path)]
        file_list = [x for x in file_list if os.path.isfile(x)]
        return file_list
    except:
        log.fatal(u'Ошибка чтения списка файлов <%s>' % path)
        return None


def getFilenamesByExt(path, ext):
    """
    Функция возвращает список всех файлов в директории с указанным расширением.
    :param path: Путь.
    :param ext: Расширение, например '.pro'.
    :return: В случае ошибки возвращает None.
    """
    try:
        path = getCurDirPrj(path)
        if not os.path.exists(path):
            log.warning(u'Путь <%s> не найден для определения списка файлов директории по расширению' % path)
            return list()

        if ext[0] != '.':
            ext = '.' + ext
        ext = ext.lower()
            
        file_list = None
        file_list = [os.path.join(path, file_name) for file_name in os.listdir(path)]
        file_list = [file_name for file_name in file_list if os.path.isfile(file_name) and
                     (os.path.splitext(file_name)[1].lower() == ext)]
        return file_list
    except:
        log.fatal(u'Ошибка чтения списка файлов <ext=%s, path=%s, list=%s>' % (ext, path, file_list))
        return None


def deleteFilesByExt(path, ext):
    """
    Функция УДАЛЯЕТ РЕКУРСИВНО В ПОДДИРЕКТОРИЯХ все файлы в директории с
    заданным расширением.
    :param path: Путь.
    :param ext: Расширение.
    :return: Возвращает результат выполнения операции True/False.
    """
    try:
        ok = True
        dir_list = os.listdir(path)
        for cur_item in dir_list:
            cur_file = path + cur_item
            if os.path.isfile(cur_file) and os.path.splitext(cur_file)[1] == ext:
                os.remove(cur_file)
            elif os.path.isdir(cur_file):
                ok = ok and deleteFilesByExt(cur_file, ext)
        return ok
    except:
        return False        


def getFileExt(filename):
    """
    Получить расширение файла с точкой.
    """
    return os.path.splitext(filename)[1]


def get_current_dir():
    """
    Текущая папка.
    Относительнай путь считается от папки defis.
    :return:
    """
    cur_dir = os.path.dirname(os.path.dirname(ic.config.__file__))
    log.debug(u'Текущая папка определена как <%s>' % cur_dir)
    return cur_dir


def getRelativePath(path):
    """
    Относительный путь.
    Относительнай путь считается от папки defis.
    :param path: Путь.
    """
    path = os.path.normpath(path)
    cur_dir = get_current_dir()
    return path.replace(cur_dir, '.').strip()


def getAbsolutePath(path):
    """
    Абсолютный путь.
    :param path: Путь.
    """
    try:
        cur_dir = get_current_dir()
        if path.startswith('..'):
            path = os.path.join(os.path.dirname(cur_dir), path[2 + len(os.path.sep):])
        elif path.startswith('.'):
            path = os.path.join(cur_dir, path[1 + len(os.path.sep):])
        path = os.path.normpath(path)
        return path
    except:
        log.fatal(u'Ошибка определения абсолютного пути <%s>' % path)
        return path


def get_relative_path(path, cur_dir=None):
    """
    Относительный путь. Путь приводится к виду Unix.
    :param path: Путь.
    :param cur_dir: Текущий путь.
    """
    if cur_dir is None:
        import ic.engine.glob_functions
        cur_dir = os.path.dirname(ic.engine.glob_functions.getVar('PRJ_DIR')).replace('\\', '/').lower()
    if cur_dir:
        path = path.replace('\\', '/').lower().strip()
        return path.replace(cur_dir, '.')
    return path


def getCurDirPrj(path=None):
    """
    Текущий путь. Определяется относительно PRJ_DIR.
    """
    # Нормализация текущего пути
    if path is None:
        try:
            import ic.engine.glob_functions
            prj_dir = ic.engine.glob_functions.getVar('PRJ_DIR')
            if prj_dir:
                path = os.path.dirname(prj_dir)
            else:
                path = getProfilePath()
        except:
            log.fatal(u'Ошибка определения пути <%s>' % path)
            path = os.getcwd()
    path = path.replace('\\', '/')
    if path[-1] != '/':
        path += '/'
    return path


def get_absolute_path(path, cur_dir=None):
    """ 
    Абсолютный путь. Путь приводится к виду Unix. 
    :param path: Путь.
    :param cur_dir: Текущий путь.
    """
    try:
        if not path:
            log.error(u'Не определен путь для приведения к абсолютному виду')
            return None

        if not isinstance(path, str):
            log.warning(u'Не корректный тип пути <%s : %s>' % (str(path), type(path)))
            return path

        # Нормализация текущего пути
        cur_dir = getCurDirPrj(cur_dir)

        # Коррекция самого пути
        path = os.path.abspath(path.replace('./', cur_dir).strip())
        return path
    except:
        log.fatal(u'Ошибка определения абсолютног пути <%s>. Текущая директория <%s>' % (path, cur_dir))
    return path


def getPathFile(path, filename):
    """
    Корректное представление общего имени файла.
    :param path: Путь.
    :param filename: Имя файла.
    """
    if not path:
        log.warning(u'Не определен путь для корректировки')
        return filename
    if not filename:
        log.warning(u'Не определено имя файла для корректировки')
        return filename

    path = os.path.normpath(path)
    filename = os.path.normpath(filename)
    relative_path = getRelativePath(path)
    # Этот путь уже присутствует в имени файла
    if filename.find(path) != -1 or filename.find(relative_path) != -1:
        return filename
    return os.path.join(relative_path, filename)


def normPathWin(path):
    """
    Приведение пути к виду Windows.
    """
    if not path:
        return ''
        
    if path.find(' ') > -1 and path[0] != '\'' and path[-1] != '\'':
        return '\'' + os.path.normpath(path).strip() + '\''
    else:
        return os.path.normpath(path).strip()


def normPathUnix(path):
    """
    Приведение пути к виду UNIX.
    """
    return os.path.normpath(path).replace('\\', '/').strip()


def isSamePathWin(path1, path2):
    """
    Проверка,  path1==path2.
    """
    return bool(normPathWin(path1).lower() == normPathWin(path2).lower())


def _pathFilter(path, filters):
    """
    Фильтрация путей.
    :return: Возвращает True если папок с указанными имена в фильтре нет в пути и
        False если наоборот.
    """
    path = os.path.normpath(path).replace('\\', '/')
    path_lst = path.split(os.path.sep)
    filter_result = True
    for cur_filter in filters:
        if cur_filter in path_lst:
            filter_result = False
            break
    return filter_result


def _addCopyDirWalk(args, cur_dir, cur_filenames):
    """
    Функция рекурсивного обхода при добавлении папок и файлов в существующую.
    :param cur_dir: Текущая обрабатываемая папка.
    :param CurName_: Имена файлов и папок в текущей обрабатываемой папке.
    """
    from_dir = args[0]
    to_dir = args[1]
    not_copy_filter = args[2]
    
    if _pathFilter(cur_dir, not_copy_filter):
        paths = [os.path.join(cur_dir, name) for name in cur_filenames if name not in not_copy_filter]
        for path in paths:
            to_path = path.replace(from_dir, to_dir)
            if not os.path.exists(to_path):
                # Копировать если результирующего файла/папки не существует
                if os.path.isfile(path):
                    # Скопировать файл
                    copyFile(path, to_path)
                elif os.path.isdir(path):
                    # Создать директорию
                    try:
                        os.makedirs(to_path)
                    except:
                        log.fatal(u'Ошибка создания папки <%s>' % to_path)
                        raise


def addCopyDir(src_dir, dst_dir, not_copy_filter=('.svn', '.SVN', '.Svn')):
    """
    Дополнить папку dst_dir файлами и папками из dst_dir
    :param src_dir: Папка/директория,  которая копируется.
    :param dst_dir: Папка/директория, в которую копируется dst_dir.
    :param not_copy_filter: Не копировать файлы/папки.
    """
    try:
        os.walk(src_dir, _addCopyDirWalk, (src_dir, dst_dir, not_copy_filter))
        return True
    except:
        log.fatal(u'Ошибка дополнения папки из <%s> в <%s>' % (src_dir, dst_dir))
        return False


def copyDir(src_dir, dst_dir, bReWrite=False, bAddDir=True):
    """
    Функция папку dst_dir в папку dst_dir со всеми внутренними поддиректориями
    и файлами.
    :param src_dir: Папка/директория,  которая копируется.
    :param dst_dir: Папка/директория, в которую копируется dst_dir.
    :param bReWrite: Указание перезаписи директории,
        если она уже существует.
    :param bAddDir: Указание производить дополнение папки,
        в случае ко когда копируемые файлы/папки существуют.
    :return: Функция возвращает результат выполнения операции True/False.
    """
    try:
        to_dir = os.path.join(dst_dir, os.path.basename(src_dir))
        if os.path.exists(to_dir) and bReWrite:
            log.info(u'Удаление папки <%s>' % to_dir)
            shutil.rmtree(to_dir, 1)
        if os.path.exists(to_dir) and bAddDir:
            return addCopyDir(src_dir, to_dir)
        else:
            log.info(u'Копировние папки <%s> в <%s>' % (src_dir, to_dir))
            shutil.copytree(src_dir, to_dir)
        return True
    except:
        log.fatal(u'Ошибка копирования папки из <%s> в <%s>' % (src_dir, dst_dir))
        return False


def cloneDir(src_dir, dst_dir, bReWrite=False):
    """
    Функция переносит все содержимое папки dst_dir в папку с новым именем dst_dir.
    :param src_dir: Папка/директория,  которая копируется.
    :param dst_dir: Новое имя папки/директории.
    :param bReWrite: Указание перезаписи директории, если она
        уже существует.
    :return: Функция возвращает результат выполнения операции True/False.
    """
    try:
        if os.path.exists(dst_dir) and bReWrite:
            shutil.rmtree(dst_dir, 1)
        os.makedirs(dst_dir)
        for sub_dir in getSubDirs(src_dir):
            shutil.copytree(sub_dir, dst_dir)
        for file_name in getFilenames(src_dir):
            copyFile(file_name, os.path.join(dst_dir, os.path.basename(file_name)))
        return True
    except:
        log.fatal(u'Ошибка клонирования папки из <%s> в <%s>' % (src_dir, dst_dir))
    return False


def isSubDir(dir1, dir2):
    """
    Функция проверяет, является ли директория dir1 поддиректорией dir2.
    :return: Возвращает True/False.
    """
    dir1 = os.path.abspath(dir1)
    dir2 = os.path.abspath(dir2)
    if dir1 == dir2:
        return True
    else:
        sub_dirs = [path for path in [os.path.join(dir2, name) for name in os.listdir(dir2)] if os.path.isdir(path)]
        for cur_sub_dir in sub_dirs:
            find = isSubDir(dir1, cur_sub_dir)
            if find:
                return find
    return False


def removeFile(filename=None):
    """
    Удалить файл.
    :param filename: Имя удаляемого файла.
    :return: True/False.
    """
    if os.path.exists(filename):
        try:
            os.remove(filename)
            log.info(u'Удален файл <%s>' % filename)
            return True
        except OSError:
            log.error(u'Ошибка удаления файла <%s>' % filename)
        except:
            log.fatal(u'Ошибка удаления файла <%s>' % filename)
    else:
        log.warning(u'Удаление. Файл <%s> не найден' % filename)
    return False


def genDefaultBakFileName():
    """
    Генерация имени бак файла по текущему времени.
    """
    return time.strftime('_%d_%m_%Y_%H_%M_%S.bak', time.localtime(time.time()))


def getFilesByMask(filename_mask):
    """
    Список файлов по маске.
    :param filename_mask: Маска файлов. Например C:\Temp\*.dbf.
    :return: Возвращает список строк-полных путей к файлам.
        В случае ошибки None.
    """
    try:
        if isinstance(filename_mask, str):
            dir_path = os.path.dirname(filename_mask)
            if os.path.exists(dir_path):
                filenames = glob.glob(pathname=filename_mask, recursive=False)
                return [os.path.abspath(file_name) for file_name in filenames]
            else:
                log.warning(u'Не найден путь <%s> для определения списка файлов по маске <%s>' % (dir_path, filename_mask))
        elif isinstance(filename_mask, tuple) or isinstance(filename_mask, list):
            filenames = list()
            for file_mask in filename_mask:
                filenames = glob.glob(pathname=filename_mask, recursive=False)
                filenames += [os.path.abspath(file_name) for file_name in filenames]
            return filenames
        else:
            log.warning(u'Не поддерживаемый тип аргумента в функции getFilesByMask')
    except:
        log.fatal(u'Ошибка определения списка файлов по маске <%s>' % str(filename_mask))
    return []


def copyToDir(filename, dst_dir, bRewrite=True):
    """
    Копировать файл в папку.
    :param filename: Имя файла.
    :param dst_dir: Папка в которую необходимо скопировать.
    :param bRewrite: True-если новый файл уже существует, 
        то переписать его молча. False-если новый файл уже существует, 
        то выдать сообщение о подтверждении перезаписи файла.
    :return: Возвращает результат выполнения операции True/False.
    """
    return copyFile(filename, os.path.join(dst_dir,
                                           os.path.basename(filename)), bRewrite)


def delAllFilesFilter(delete_dir, *mask_filters):
    """
    Удаление всех файлов из папки с фильтрацией по маске файла. Удаление
    рекурсивное по поддиректориям.
    :param delete_dir: Папка-источник.
    :param mask_filters: Список масок файлов которые нужно удалить.
        Например '*_pkl.tab'.
    """
    try:
        # Сначала обработка в поддиректориях
        subdirs = getSubDirs(delete_dir)
        if subdirs:
            for sub_dir in subdirs:
                delAllFilesFilter(sub_dir, *mask_filters)
        for file_mask in mask_filters:
            del_files = getFilesByMask(os.path.join(delete_dir, file_mask))
            for del_file in del_files:
                os.remove(del_file)
                log.info(u'Удаление файла <%s>' % del_file)
        return True
    except:
        log.fatal(u'Ошибка удаления файлов %s из папки <%s>' % (str(mask_filters), delete_dir))
        return None


def getPythonDir():
    """
    Папка в которую установлен Python.
    """
    return os.path.dirname(sys.executable)


def getPythonExe():
    """
    Полный путь к исполняемому интерпретатору Python.
    """
    return sys.executable


def getTempDir():
    """
    Временная директория
    """
    return os.environ['TMP']


def getTempFileName(prefix=None):
    """
    Генерируемое имя временного файла
    """
    return tempfile.mkdtemp(getTempDir(), prefix)


def getHomePath():
    """
    Путь к домашней директории.
    :return: Строку-путь до папки пользователя.
    """
    os_platform = platform.uname()[0].lower()
    if os_platform == 'windows':
        home_path = os.environ['HOMEDRIVE']+os.environ['HOMEPATH']
        home_path = home_path.replace('\\', '/')
    elif os_platform == 'linux':
        home_path = os.environ['HOME']
    else:
        log.warning(u'Не поддерживаемая ОС <%s>' % os_platform)
        return None
    return os.path.normpath(home_path)


def getProfilePath(bAutoCreatePath=True, profile_dirname=None):
    """
    Папка профиля программы DEFIS.
    :param bAutoCreatePath: Создать автоматически путь если его нет?
    :param profile_dirname: Явное указание папки профиля.
        Если не указано, то берется ic.config.PROFILE_DIRNAME.
    :return: Путь до ~/.defis
    """
    if profile_dirname is None:
        profile_dirname = ic.config.PROFILE_DIRNAME

    home_path = getHomePath()
    if home_path:
        profile_path = os.path.join(home_path, profile_dirname)
        if not os.path.exists(profile_path) and bAutoCreatePath:
            # Автоматическое создание пути
            try:
                os.makedirs(profile_path)
            except OSError:
                log.fatal(u'Ошибка создания пути профиля <%s>' % profile_path)
        return profile_path
    return '~/.defis'


def getPrjProfilePath(bAutoCreatePath=True, profile_dirname=None):
    """
    Папка профиля прикладного проекта.
    :param bAutoCreatePath: Создать автоматически путь если его нет?
    :param profile_dirname: Явное указание папки профиля.
        Если не указано, то берется ic.config.PROFILE_DIRNAME.
    :return: Путь до ~/.defis/имя_проекта/
    """
    profile_path = getProfilePath(bAutoCreatePath, profile_dirname=profile_dirname)
    from ic.engine import glob_functions

    prj_name = glob_functions.getPrjName()
    if prj_name:
        prj_profile_path = os.path.join(profile_path, prj_name)
    else:
        # Если в проект мы не вошли, то просто определяем папку профиля проекта
        # как папку профиля программы
        prj_profile_path = profile_path

    if not os.path.exists(prj_profile_path) and bAutoCreatePath:
        # Автоматическое создание пути
        try:
            os.makedirs(prj_profile_path)
        except OSError:
            log.fatal(u'Ошибка создания пути профиля проекта <%s>' % prj_profile_path)
    return prj_profile_path


def getProjectDir():
    """
    Папка проекта.
    :return: Папка проекта.
    """
    from ic.engine import glob_functions
    return glob_functions.getPrjDir()


def getRootProjectDir():
    """
    Корневая папка проекта, в которой находяться все папки подсистем проекта.
    :return: Корневая папка проекта, в которой находяться все папки подсистем проекта.
    """
    prj_dir = getProjectDir()
    return os.path.dirname(prj_dir)


def getHomeDir():
    """
    Папка HOME.
    """
    if sys.platform[:3].lower() == 'win':
        home_dir = os.environ['HOMEDRIVE']+os.environ['HOMEPATH']
        home_dir = home_dir.replace('\\', '/')
    else:
        home_dir = os.environ['HOME']
    return home_dir


def getRootDir():
    """
    Папка DEFIS.
    :return: Путь до папки DEFIS.
    """
    # Берем относительно имени файла
    package_path = os.path.dirname(__file__)
    if package_path:
        root_path = os.path.dirname(os.path.dirname(package_path))
    else:
        log.warning(u'Не определен путь к корневой папке всех проектов')
        return u''
    return root_path

def is_same_file_length(filename1, filename2):
    """
    Проверка что файл1 и файл2 совпадают.
    Проверка производиться по размеру файлу.
    :return: True/False.
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
    :param filename: Полное имя файла.
    :return: Контрольная сумма файла или None, если какая-либо ошибка.
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
    :param filename: Полное имя файла.
    :return: Контрольная сумма файла или None, если какая-либо ошибка.
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
    :param directory: Полный путь до директории.
    :param filename_pattern: Шаблон имен файлов. Если не определен, то беруться все файлы.
    :param sort_filename: Произвести автоматическую сортировку списка по имени файлов?
    :return: Список полных имен файлов или None в случае ошибки.
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
    :param path: Путь.
    :param username: Имя пользователя.
    """
    home_dir = get_home_path(username)
    return os.path.abspath(os.path.normpath(path.replace('~', home_dir)))


def fileList(src_dirname):
    """
    Список файлов в директории с полными путями.
    :param src_dirname: Исходная директория.
    :return: Список файлов.
    """
    return [norm_path(src_dirname + '/' + filename) for filename in os.listdir(norm_path(src_dirname))]


def norm_path(cur_path, delim=os.path.sep):
    """
    Удалить двойные разделител из пути.
    :type cur_path: C{string}
    :param cur_path: Путь
    :type delim: C{string}
    :param delim: Разделитель пути
    """
    cur_path = cur_path.replace('~', getHomeDir())
    dbl_delim = delim + delim
    while dbl_delim in cur_path:
        cur_path = cur_path.replace(dbl_delim, delim)
    return cur_path
