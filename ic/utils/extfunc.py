#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Дополниетельные сервисные функции.
"""

# --- Imports ---
import sys
import sysconfig
import os
import os.path
import pwd
import stat
import getpass
import shutil
import traceback
import struct

try:
    from ic.utils import strfunc
except:
    print(u'Import error ic_str module')

try:
    from ic.log import log
except:
    print(u'Import error ic_str module')
    log = None

__version__ = (0, 1, 2, 1)


DEFAULT_ENCODING = 'utf-8'


def who_am_i():
    """
    Имя залогиненного пользователя.
    """
    return getpass.getuser()


def is_root_user():
    """
    Проверить текущий пользователь - root?
    @return: Функция возвращает True/False.
    """
    return bool(who_am_i().lower() == 'root')


def check_python_library_version(lib_name, lib_version, compare='=='):
    """
    Проверка установлена ли библиотека указанной версии.
    @param lib_name: Имя библиотеки, например 'wx'.
    @param lib_version: Версия библиотеки, например '2.8.8.1'.
    @param compare: Оператор сравнения.
    @return: Возвращает True/False.
    """
    import_cmd = 'import '+str(lib_name)
    try:
        exec(import_cmd)
        import_lib = eval(lib_name)
    except ImportError:
        # Нет такой библиотеки
        print(u'Check Library Error:', lib_name)
        return False

    if compare == '==':
        # Проверка на сравнение
        print('Python Library:', lib_name, 'Version:', import_lib.__version__)
        return bool(import_lib.__version__ == lib_version)
    elif compare in ('>=', '=>'):
        # Проверка на больше или равно
        print('Python Library:', lib_name, 'Version:', import_lib.__version__)
        return version_compare_greate_equal(import_lib.__version__, lib_version)
    else:
        print('Not supported compare:', compare)
    return False


def version_compare_greate_equal(version1, version2, delimiter='.'):
    """
    Сравнение версий на Version1_>=version2.
    @param version1: Версия 1. В строковом виде. Например '2.8.9.2'.
    @param version2: Версия 2. В строковом виде. Например '2.8.10.1'.
    @param delimiter: Разделитель. Например точка.
    """
    ver1 = tuple([int(sub_ver) for sub_ver in version1.split(delimiter)])
    ver2 = tuple([int(sub_ver) for sub_ver in version2.split(delimiter)])
    len_ver2 = len(ver2)
    for i, sub_ver1 in enumerate(ver1):
        if i >= len_ver2:
            return True
        sub_ver2 = ver2[i]
        if sub_ver1 < sub_ver2:
            return False
        elif sub_ver1 > sub_ver2:
            return True
    return True


def check_python_labraries(**kwargs):
    """
    Проверка установленных библиотек Python.
    """
    result = True
    for lib_name, lib_ver in kwargs.items():
        result = result and check_python_library_version(lib_name, lib_ver)
    return result


def check_linux_package(package_name, version=None, compare='=='):
    """
    Проверка установленного пакета Linux.
    @param package_name: Имя пакета, например 'libgnomeprintui'
    @param version: Версия пакета. Если None, то версия не проверяется.\
    @param compare: Метод проверки версии.
    @return: True-пакет установлен, False-не установлен, 
        None-система пакетов не определена.
    """
    if is_deb_linux():
        print('This Linux is Debian')
        return check_deb_linux_package(package_name, version, compare)
    else:
        print('This linux is not Debian')
    return None


def check_deb_linux_package(package_name, version=None, compare='=='):
    """
    Проверка установленного пакета Linux.
    @param package_name: Имя пакета, например 'libgnomeprintui'
    @param version: Версия пакета. Если None, то версия не проверяется.\
    @param compare: Метод проверки версии.
    @return: True-пакет установлен, False-не установлен, 
        None-система пакетов не определена.
    """
    cmd = None
    try:
        cmd = 'dpkg-query --list | grep \'ii \' | grep \'%s\'' % package_name
        result = os.popen3(cmd)[1].readlines()
        return bool(result)
    except:
        print('Check Debian installed package Error', cmd)
        raise
    return None    


def check_deb_package_install(package_name):
    """
    Проверка установленн ли пакет DEB.
    @param package_name: Имя пакета, например 'libgnomeprintui'
    @return: True-пакет установлен, False-не установлен, 
        None-система пакетов не определена.
    """
    return check_deb_linux_package(package_name)


def get_uname(option='-a'):
    """
    Результат выполнения команды uname.
    """
    cmd = None
    try:
        cmd = 'uname %s' % option
        return os.popen3(cmd)[1].readline()
    except:
        print('Uname Error', cmd)
        raise
    return None    


def get_linux_name():
    """
    Определить название Linux операционной системы и версии.
    """
    try:
        if os.path.exists('/etc/issue'):
            # Обычно Debian/Ubuntu Linux
            cmd = 'catalog /etc/issue'
            return os.popen3(cmd)[1].readline().replace('\\n', '').replace('\\l', '').strip()
        elif os.path.exists('/etc/release'):
            # Обычно RedHat Linux
            cmd = 'catalog /etc/release'
            return os.popen3(cmd)[1].readline().replace('\\n', '').replace('\\l', '').strip()
    except:
        print('Get linux name ERROR')
        raise
    return None


DEBIAN_LINUX_NAMES = ('Ubuntu', 'Debian', 'Mint', 'Knopix')


def is_deb_linux():
    """
    Проверка является ли дистрибутив c системой пакетов Debian.
    @return: Возвращает True/False.
    """
    linux_name = get_linux_name()
    print('Linux name:', linux_name)
    return bool([name for name in DEBIAN_LINUX_NAMES if name in linux_name])


def is_deb_linux_uname():
    """
    Проверка является ли дистрибутив c системой пакетов Debian.
    Проверка осуществляется с помощью команды uname.
    ВНИМАНИЕ! Это не надежный способ.
    Функция переписана.
    @return: Возвращает True/False.
    """
    uname_result = get_uname()
    return ('Ubuntu' in uname_result) or ('Debian' in uname_result)


def get_dist_packages_path():
    """
    Путь к папке 'dist-packages' или 'site_packages' 
    (в зависимости от дистрибутива) Python.
    """
    python_stdlib_path = sysconfig.get_path('stdlib')
    site_packages_path = os.path.normpath(os.path.join(python_stdlib_path, 'site-packages'))
    dist_packages_path = os.path.normpath(os.path.join(python_stdlib_path, 'dist-packages'))
    if os.path.exists(site_packages_path):
        return site_packages_path
    elif os.path.exists(dist_packages_path):
        return dist_packages_path
    return None


def create_pth_file(pth_filename, path):
    """
    Создание *.pth файла в папке site_packages.
    @param pth_filename: Не полное имя pth файла, например 'ic.pth'.
    @param path: Путь который указывается в pth файле.
    @return: Возвращает результат выполнения операции True/False.
    """
    pth_file = None
    try:
        dist_packages_path = get_dist_packages_path()
        pth_file_name = os.path.join(dist_packages_path, pth_filename)
        pth_file = open(pth_file_name, 'wt')
        pth_file.write(path)
        pth_file.close()
        pth_file = None
        
        # Установить права на PTH файл
        try:
            os.chmod(pth_file_name, stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)
        except:
            print(u'ERROR! Chmod function in create_pth_file')
        print('Create PTH file:', pth_file_name, 'path:', path)
        return True
    except:
        if pth_file:
            pth_file.close()
            pth_file = None
        raise
    return False


def unzip_to_dir(zip_filename, dst_dir, bOverwrite=True, bConsole=False):
    """
    Распаковать *.zip архив в папку.
    @param zip_filename: Полное имя *.zip архива.
    @param dst_dir: Указание папки, в которую будет архив разворачиваться.
    @param bOverwrite: Перезаписать существующие файлы без запроса?
    @param bConsole: Вывод в консоль?
    @return: Возвращает результат выполнения операции True/False.
    """
    try:
        overwrite = ''
        if bOverwrite:
            overwrite = '-o'
        unzip_cmd = 'unzip %s %s -d %s' % (overwrite, zip_filename, dst_dir)
        if bConsole:
            os.system(unzip_cmd)
            return None
        else:
            return os.popen3(unzip_cmd)
    except:
        print('Unzip Error', unzip_cmd)
        raise
    return None


def targz_extract_to_dir(tar_filename, dst_dir, bConsole=False):
    """
    Распаковать *.tar архив в папку.
    @param tar_filename: Полное имя *.tar архива.
    @param dst_dir: Указание папки, в которую будет архив разворачиваться.
    @param bConsole: Вывод в консоль?
    @return: Возвращает результат выполнения операции True/False.
    """
    tar_extract_cmd = None
    try:
        tar_extract_cmd = 'tar --extract --verbose --directory=%s --file=%s' % (dst_dir, tar_filename)
        print('Tar extract command:', tar_extract_cmd, os.path.exists(tar_filename))
        if bConsole:
            os.system(tar_extract_cmd)
            return None
        else:
            return os.popen3(tar_extract_cmd)
    except:
        print('Tar Extract Error', tar_extract_cmd)
        raise
    return None


def deb_pkg_install(deb_filename):
    """
    Установить deb пакет.
    @param deb_filename: Полное имя *.deb пакета.
    @return: Возвращает результат выполнения операции True/False.
    """
    deb_install_cmd = None
    try:
        deb_install_cmd = 'dpkg --install %s' % deb_filename
        print('DEB package install command:', deb_install_cmd, os.path.exists(deb_filename))
        return os.popen3(deb_install_cmd)
    except:
        print('DEB package install Error', deb_install_cmd)
        raise
    return None


def deb_pkg_uninstall(deb_package_name):
    """
    Деинсталлировать DEB пакет.
    @param deb_package_name: Имя пакета. Например dosemu.
    @return: Возвращает результат выполнения операции True/False.
    """
    deb_uninstall_cmd = None
    try:
        if check_deb_package_install:
            deb_uninstall_cmd = 'dpkg --remove %s' % deb_package_name
            print('DEB package uninstall command:', deb_uninstall_cmd)
            return os.popen3(deb_uninstall_cmd)
        else:
            print('WARNING: Package %s not installed' % deb_package_name)
    except:
        print('DEB package uninstall Error', deb_uninstall_cmd)
        raise
    return None


def get_home_path(username=None):
    """
    Определить домашнюю папку.
    """
    if sys.platform[:3].lower() == 'win':
        home = os.environ['HOMEDRIVE']+os.environ['HOMEPATH']
        home = home.replace('\\', '/')
    else:
        if username is None:
            home = os.environ['HOME']
        else:
            user_struct = pwd.getpwnam(username)
            home = user_struct.pw_dir
    return home


def get_login():
    """
    Имя залогинненного пользователя.
    """
    username = os.environ['USERNAME']
    if username != 'root':
        return username
    else:
        return os.environ['SUDO_USER']
        

def dir_dlg(title='', default_path=''):
    """
    Диалог выбора каталога.
    @param title: Заголовок диалогового окна.
    @param default_path: Путь по умолчанию.
    """
    import wx
    app = wx.GetApp()
    result = ''
    dlg = None
    
    if app:
        try:
            main_win = app.GetTopWindow()

            dlg = wx.DirDialog(main_win, title,
                               style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)

            # Установка пути по умолчанию
            if not default_path:
                default_path = os.getcwd()
            dlg.SetPath(default_path)
            if dlg.ShowModal() == wx.ID_OK:
                result = dlg.GetPath()
            else:
                result = ''
        finally:
            if dlg:
                dlg.Destroy()
                dlg = None

    return result


def file_dlg(title='', filename_filter='', default_path=''):
    """
    Открыть диалог выбора файла для открытия/записи.
    @param title: Заголовок диалогового окна.
    @param filename_filter: Фильтр файлов.
    @param default_path: Путь по умолчанию.
    @return: Возвращает полное имя выбранного файла.
    """
    import wx
    app = wx.GetApp()
    result = ''
    dlg = None
    
    if app:
        try:
            main_win = app.GetTopWindow()

            wildcard = filename_filter + '|All Files (*.*)|*.*'
            dlg = wx.FileDialog(main_win, title, '', '', wildcard, wx.FD_OPEN)
            if default_path:
                dlg.SetDirectory(normpath(default_path, get_login()))
            else:
                dlg.SetDirectory(os.getcwd())
        
            if dlg.ShowModal() == wx.ID_OK:
                result = dlg.GetPaths()[0]
            else:
                result = ''
            dlg.Destroy()
        finally:
            if dlg:
                dlg.Destroy()

    return result


def get_dosemu_dir(username=None):
    """
    Определить папку установленного dosemu.
    """
    home = get_home_path(username)
    dosemu_dir = os.path.join(home, '.dosemu')
    if os.path.exists(dosemu_dir):
        return dosemu_dir
    else:
        return dir_dlg(u'Не найдена папка dosemu')
        
    return None


def check_dir(dirname):
    """
    Проверить папку, если ее нет то она создается.
    """
    norm_dir = normpath(dirname, get_login())
    if not os.path.exists(norm_dir):
        try:
            os.makedirs(norm_dir)
            return True
        except:
            print('ERROR! Make directory', norm_dir)
            return False
    else:
        return True


def save_file_text(filename, txt=''):
    """
    Запись текста в файл.
    @param filename; Имя файла.
    @param txt: Записываемый текст.
    @return: True/False
    """
    # if isinstance(txt, str):
    #    # Если передается текст в юникоде,
    #    #  то автоматом перекодировать в UTF-8
    #    txt = txt.encode(DEFAULT_ENCODING)

    file_obj = None
    try:
        file_obj = open(filename, 'wt')
        file_obj.write(txt)
        file_obj.close()
        return True
    except:
        if file_obj:
            file_obj.close()
        print('Save text file', filename, 'ERROR')
        print(traceback.format_exc())
    return False


def load_file_text(filename, code_page='utf-8',
                   to_unicode=False):
    """
    Чтение текстового файла.
    @param filename; Имя файла.
    @param code_page: Кодовая страница файла
        (для преобразования в Unicode).
    @paran to_unicode: Преобразовать сразу в Unicode?
    @return: Текст файла.
    """
    if not os.path.exists(filename):
        print(u'File <%s> not found' % filename)
        return ''

    f = None
    try:
        f = open(filename, 'rt')
        txt = f.read()
        f.close()
    except:
        if f:
            f.close()
        print(u'Load text file <%s>' % filename)
        return ''

    # if to_unicode:
    #    return unicode(txt, code_page)
    return txt


def load_file_unicode(filename, code_page=None):
    """
    Чтение текстового файла сразу в виде unocode.
    Определение содовой страницы происходит автоматически.
    @param filename; Имя файла.
    @param code_page: Кодовая страница файла.
        Если не определена, то пробуем определить ее.
    @return: Текст файла в unicode.
    """
    body_text = load_file_text(filename)
    if not code_page:
        code_page = strfunc.get_codepage(body_text)
    return str(body_text)   # , code_page)


def recode_text_file(txt_filename, new_filename=None, src_codepage=None, dst_codepage='utf-8'):
    """
    Перекодировать текстовый файл из одной кодирровки в другую.
    @param txt_filename: Полное наименование текстового файла.
    @param new_filename: Полное наименование результирующего текстового файла.
        Если не определено, то берется исходное имя файла.
    @param src_codepage: Исходная кодировка.
        Если None, то пробуем определить исходную кодировку файла.
    @param dst_codepage: Результирующая кодировка.
        По умолчанию utf-8.
    @return: True - удачно перекодировали. False - ошибка.
    """
    if not os.path.exists(txt_filename):
        print(u'Файл <%s> не найден' % txt_filename)
        return False

    if not new_filename:
        new_filename = txt_filename

    txt_unicode = load_file_unicode(txt_filename, src_codepage)

    if txt_unicode and isinstance(txt_unicode, str):
        txt_str = txt_unicode   # .encode(dst_codepage)
        if os.path.exists(new_filename):
            try:
                os.remove(new_filename)
            except:
                print(u'Ошибка удаления файла <%s>' % new_filename)
                return False
        return save_file_text(new_filename, txt_str)
    return False


def copy_file_to(src_filename, dst_path, bReWrite=True):
    """
    Копировать файл в указанную папку.
    @param src_filename: Имя файла-источника.
    @param dst_path: Папка-назначение.
    @param bReWrite: Перезаписать файл, если он уже существует?
    """
    try:
        dst_path = normpath(dst_path, get_login())
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        dst_file_name = os.path.join(dst_path, os.path.basename(src_filename))
        if bReWrite:
            if os.path.exists(dst_file_name):
                os.remove(dst_file_name)
        shutil.copyfile(src_filename, dst_file_name)
        return True
    except:
        return False


def set_chown_login(path):
    """
    Установить владельца файла/папки залогиненного пользователя.
    """
    if not os.path.exists(path):
        return False
    username = get_login()
    user_struct = pwd.getpwnam(username)
    uid = user_struct.pw_uid
    gid = user_struct.pw_gid
    path = normpath(path, username)
    return os.chown(path, uid, gid)


def set_public_chmod(path):
    """
    Установить свободный режим доступа (0x777) к файлу/папке.
    """
    path = normpath(path, get_login())
    if os.path.exists(path):
        return os.chmod(path, stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)
    return False


def set_public_chmode_tree(path):
    """
    Установить свободный режим доступа (0x777) к файлу/папке рекурсивно.
    """
    path = normpath(path, get_login())
    result = set_public_chmod(path)
    if os.path.isdir(path):
        for f in os.listdir(path):
            pathname = os.path.join(path, f)
            set_public_chmode_tree(pathname)
    return result


def sym_link(link_path, linkname, username=None, bOverwrite=True):
    """
    Создать символическую ссылку.
    @param link_path: На что ссылается ссылка.
    @param linkname: Имя ссылки.
    @param username: Имя пользователя.
    @param bOverwrite: Перезаписать ссылку, если она существует?
    """ 
    username = username
    if username is None:
        username = get_login()
    link_path = normpath(link_path, username)
    link_name = normpath(linkname, username)
    
    if os.path.exists(link_name) and bOverwrite:
        # Перезаписать?
        os.remove(link_name)
    try:
        return os.symlink(link_path, link_name)
    except:
        print('ERROR! Create symbolic link:', link_name, '->', link_path)
        raise
    return None


def get_options(arguments=None):
    """
    Преобразование параметров командной строки в словарь python.
    Параметры командной строки в виде --ключ=значение.
    @param arguments: Список строк параметров.
    @return: Словарь значений или None в случае ошибки.
    """
    if arguments is None:
        arguments = sys.argv[1:]
        
    opts = {}
    args = []
    while arguments:
        if arguments[0][:2] == '--':
            if '=' in arguments[0]:
                # поиск пар “--name=value”
                i = arguments[0].index('=')
                # ключами словарей будут имена параметров
                opts[arguments[0][:i]] = arguments[0][i + 1:]
            else:
                # поиск “--name”
                # ключами словарей будут имена параметров
                opts[arguments[0]] = True
        else:
            args.append(arguments[0])
        arguments = arguments[1:]
    return opts, args
    
    
def normpath(path, username=None):
    """
    Нормировать путь.
    @param path: Путь.
    @param username: Имя пользователя.
    """
    home_dir = get_home_path(username)
    return os.path.abspath(os.path.normpath(path.replace('~', home_dir)))


def isLinuxPlatform():
    """
    ОС linux?
    """
    return sys.platform.lower().startswith('lin')


def isWindowsPlatform():
    """
    ОС windows?
    """
    return sys.platform.lower().startswith('win')


def getPlatform():
    """
    ОС
    """
    return sys.platform


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


def copyToDir(filename, dst_dir, bRewrite=True):
    """
    Копировать файл в папку.
    @type filename: C{string}
    @param filename: Имя файла.
    @type dst_dir: C{string}
    @param dst_dir: Папка в которую необходимо скопировать.
    @type bRewrite: C{bool}
    @param bRewrite: True-если новый файл уже существует,
        то переписать его молча. False-если новый файл уже существует,
        то не перезаписывать его а оставить старый.
    @return: Возвращает результат выполнения операции True/False.
    """
    return copyFile(filename, os.path.join(dst_dir, os.path.basename(filename)), bRewrite)


def changeExt(filename, new_ext):
    """
    Поменять у файла расширение.
    @type filename: C{string}
    @param filename: Полное имя файла.
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
        print('ERROR! Cange ext file %s' % filename)
        raise
    return None


def parseCmd(command):
    """
    Распарсить команду.
    @type command: c{string}
    @param command: Строковое представление команды.
    @return: Список [<Комманда>,<Аргумент1>,<Аргумент2>,..]
    """
    parse_args = command.strip().split(' ')
    args = []
    i = 0
    while i < len(parse_args):
        parse_arg = parse_args[i]
        if parse_arg[0] == '"' and parse_arg[-1] != '"':
            while parse_arg[-1] != '"' and i < len(parse_args):
                i += 1
                parse_arg += ' '+parse_args[i]
        # Стереть """
        if parse_arg[0] == '"':
            parse_arg = parse_arg[1:]
        if parse_arg[-1] == '"':
            parse_arg = parse_arg[:-1]

        args.append(parse_arg)
        i += 1
    return args


def getComputerName():
    """
    Имя компютера. Без перекодировки.
    @return: Получить имя компьютера в сети.
        Имя компьютера возвращается в utf-8 кодировке.
    """
    import socket
    comp_name = socket.gethostname()
    if isWindowsPlatform():
        # Если win то поменять кодировку c cp1251 на utf-8
        comp_name = str(comp_name)  # , 'cp1251').encode('utf-8')
    return comp_name


def getComputerNameLAT():
    """
    Имя компютера. Все русские буквы заменяются латиницей.
    @return: Получить имя компьютера в сети.
    """
    comp_name = None
    if 'COMPUTERNAME' in os.environ:
        comp_name = os.environ['COMPUTERNAME']
    else:
        import socket
        comp_name = socket.gethostname()

    # ВНИМАНИЕ! Имена компьютеров должны задаваться только латиницей
    # Под Win32 можно задать имя компа русскими буквами и тогда
    # приходится заменять все на латиницу.
    if isinstance(comp_name, str):
        if isWindowsPlatform():
            comp_name = str(comp_name)  # , 'cp1251')
            comp_name = rus2lat(comp_name)
    return comp_name


def _rus2lat(text, translate_dict):
    """
    Перевод русских букв в латинские по словарю замен.
    @param text: Русский текст.
    @param translate_dict: Словарь замен.
    """
    # if not isinstance(text, unicode):
    #    # Привести к юникоду
    #    text = unicode(text, 'utf-8')

    txt_list = list(text)
    txt_list = [translate_dict.setdefault(ch, ch) for ch in txt_list]
    return ''.join(txt_list)


RUS2LATDict = {u'а': 'a', u'б': 'b', u'в': 'v', u'г': 'g', u'д': 'd', u'е': 'e', u'ё': 'yo', u'ж': 'j',
               u'з': 'z', u'и': 'idx', u'й': 'y', u'к': 'k', u'л': 'l', u'м': 'm', u'н': 'n', u'о': 'o', u'п': 'p',
               u'р': 'r', u'с': 's', u'т': 't', u'у': 'u', u'ф': 'f', u'х': 'h', u'ц': 'c', u'ч': 'ch',
               u'ш': 'sh', u'щ': 'sch', u'ь': '', u'ы': 'y', u'ъ': '', u'э': 'e', u'ю': 'yu', u'я': 'ya',
               u'А': 'A', u'Б': 'B', u'В': 'V', u'Г': 'G', u'Д': 'D', u'Е': 'E', u'Ё': 'YO', u'Ж': 'J',
               u'З': 'Z', u'И': 'I', u'Й': 'Y', u'К': 'K', u'Л': 'L', u'М': 'M', u'Н': 'N', u'О': 'O', u'П': 'P',
               u'Р': 'R', u'С': 'S', u'Т': 'T', u'У': 'U', u'Ф': 'F', u'Х': 'H', u'Ц': 'C', u'Ч': 'CH',
               u'Ш': 'SH', u'Щ': 'SCH', u'Ь': '', u'Ы': 'Y', u'Ъ': '', u'Э': 'E', u'Ю': 'YU', u'Я': 'YA'}


def rus2lat(text):
    """
    Перевод русских букв в латинские.
    """
    return _rus2lat(text, RUS2LATDict)


def norm_path(path, delim=os.path.sep):
    """
    Удалить двойные разделител из пути.
    @type path: C{string}
    @param path: Путь
    @type delim: C{string}
    @param delim: Разделитель пути
    """
    path = path.replace('~', getHomeDir())
    dbl_delim = delim + delim
    while dbl_delim in path:
        path = path.replace(dbl_delim, delim)
    return path


def getHomeDir():
    """
    Папка HOME.
    @return: Строку-путь до папки пользователя.
    """
    if isWindowsPlatform():
        home_dir = os.environ['HOMEDRIVE']+os.environ['HOMEPATH']
        home_dir = home_dir.replace('\\', '/')
    else:
        home_dir = os.environ['HOME']
    return os.path.normpath(home_dir)


def text_file_append(txt_filename, text, cr='\n'):
    """
    Добавить строки в текстовый файл.
    @param txt_filename: Имя текстового файла.
    @param text: Добавляемый текст.
    @param cr: Символ возврата каретки.
    @return: True/False.
    """
    txt_filename = normpath(txt_filename, get_login())
    if os.path.exists(txt_filename):
        f = None
        try:
            f = open(txt_filename, 'rt')
            txt = f.read()
            txt += cr
            txt += text
            print('Text file append <%s> in <%s>' % (text, txt_filename))
            f.close()
            f = None
            f = open(txt_filename, 'wt')
            f.write(txt)
            f.close()
            f = None
            return True
        except:
            print('Text file append in <%s>' % txt_filename)
            if f:
                f.close()
                f = None
    else:
        print('File <%s> not exists' % txt_filename)
    return False


def text_file_replace(txt_filename, old_string, new_string, bAutoAdd=True, cr='\n'):
    """
    Замена строки в текстовом файле.
    @param txt_filename: Имя текстового файла.
    @param old_string: Старая строка.
    @param new_string: Новая строка.
    @param bAutoAdd: Признак автоматического добавления новой строки.
    @param cr: Символ возврата каретки.
    @return: True/False.
    """
    txt_filename = normpath(txt_filename, get_login())
    if os.path.exists(txt_filename):
        f = None
        try:
            f = open(txt_filename, 'rt')
            txt = f.read()
            txt = txt.replace(old_string, new_string)
            if bAutoAdd and (new_string not in txt):
                txt += cr
                txt += new_string
                print('Text file append <%s> in <%s>' % (new_string, txt_filename))
            f.close()
            f = None
            f = open(txt_filename, 'wt')
            f.write(txt)
            f.close()
            f = None
            return True
        except:
            print('Text file replace in <%s>' % txt_filename)
            if f:
                f.close()
                f = None
    else:
        print('File <%s> not exists' % txt_filename)
    return False


def text_file_find(txt_filename, find_string):
    """
    Поиск строки в текстовом файле.
    @param txt_filename: Имя текстового файла.
    @param find_string: Сирока поиска.
    @return: True/False.
    """
    txt_filename = normpath(txt_filename, get_login())
    if os.path.exists(txt_filename):
        f = None
        try:
            f = open(txt_filename, 'rt')
            txt = f.read()
            result = find_string in txt
            f.close()
            f = None
            return result
        except:
            print('Find <%s> in text file <%s>' % (find_string, txt_filename))
            if f:
                f.close()
                f = None
    else:
        print('File <%s> not exists' % txt_filename)
    return False


def text_file_subreplace(txt_filename, sub_string, new_string, bAutoAdd=True, cr='\n'):
    """
    Замена строки в текстовом файле с поиском подстроки.
    @param txt_filename: Имя текстового файла.
    @param sub_string: Под строка  выявления строки замены.
    @param new_string: Новая строка.
    @param bAutoAdd: Признак автоматического добавления новой строки.
    @param cr: Символ возврата каретки.
    @return: True/False.
    """
    txt_filename = normpath(txt_filename, get_login())
    if os.path.exists(txt_filename):
        f = None
        try:
            f = open(txt_filename, 'rt')
            lines = f.readlines()
            is_replace = False
            for i, line in enumerate(lines):
                if sub_string in line:
                    lines[i] = new_string
                    is_replace = True
                    print('Text file replace <%s> -> <%s> in <%s>' % (line, new_string, txt_filename))
            if bAutoAdd and not is_replace:
                lines += [cr]
                lines += [new_string]
                print('Text file append <%s> in <%s>' % (new_string, txt_filename))
            f.close()
            f = None
            f = open(txt_filename, 'wt')
            f.writelines(lines)
            f.close()
            f = None
            return True
        except:
            print('Text file sub replace in <%s>' % txt_filename)
            if f:
                f.close()
                f = None
    else:
        print('File <%s> not exists' % txt_filename)
    return False


def text_file_subdelete(txt_filename, sub_string):
    """
    Удаление строки в текстовом файле с поиском подстроки.
    @param txt_filename: Имя текстового файла.
    @param sub_string: Под строка  выявления строки удаления.
    @return: True/False.
    """
    txt_filename = normpath(txt_filename, get_login())
    if os.path.exists(txt_filename):
        f = None
        try:
            result_lines = []
            f = open(txt_filename, 'rt')
            lines = f.readlines()
            for line in lines:
                if sub_string not in line:
                    result_lines.append(line)
                else:
                    print('Text file delete line <%s> from <%s>' % (line, txt_filename))
            f.close()
            f = None
            f = open(txt_filename, 'wt')
            f.writelines(result_lines)
            f.close()
            f = None
            return True
        except:
            print('Text file sub delete in <%s>' % txt_filename)
            if f:
                f.close()
                f = None
    else:
        print('File <%s> not exists' % txt_filename)
    return False


def exec_sys_command(command):
    """
    Функция выполнения команды ОС.
    @param command: Текст команды.
    """
    try:
        os.system(command)
        print('Execute command: %s' % command)
    except:
        print('ERROR. Execute command: %s' % command)
        raise


def targz_install_python_package(targz_package_filename=None):
    """
    Установить Python пакет в виде tar.gz архива.
    @param targz_package_filename: Имя файла архива поставки Python пакета.
    @return: True/False.
    """
    if not targz_package_filename:
        print('Not define TARGZ python package file.')
        return False

    if not os.path.exists(targz_package_filename):
        print('Not exists <%s> python package file.' % targz_package_filename)
        return False

    print('Start install python package. TarGz filename <%s>' % targz_package_filename)

    pkg_dir = os.path.dirname(targz_package_filename)
    set_public_chmod(pkg_dir)
    targz_extract_to_dir(targz_package_filename, pkg_dir)

    targz_basename = os.path.splitext(os.path.basename(targz_package_filename))[0]
    setup_dir = os.path.normpath(os.path.join(pkg_dir, targz_basename))
    setup_filename = os.path.normpath(os.path.join(setup_dir, 'setup.py'))
    if os.path.exists(setup_filename):
        cmd = 'cd %s; sudo %s setup.py install' % (setup_dir, sys.executable)
        print('Install <%s> library. Command <%s>' % (targz_basename, cmd))
        os.system(cmd)
        # Удалить после инсталляции распакованный архив
        if os.path.exists(setup_dir):
            cmd = 'sudo rm -R %s' % setup_dir
            print('Delete setup directory <%s>. Command <%s>' % (setup_dir, cmd))
            os.system(cmd)
        return True
    else:
        print('WARNING. Don\'t exist setup.py file <%s>' % setup_filename)
    return False


def checkPingHost(host_name):
    """
    Проверка связи с хостом по пингу (ping).
    @param host_name: Имя хоста.
    @return: True - связь с хостом есть. False - сбой связи.
    """
    response = os.system('ping -c 1 %s' % host_name)
    return response == 0


def loadBinaryFile(filename):
    """
    Загрузить данные бинарного файла.
    @param filename: Полное имя загружаемого файла.
    @return: Бинарные данные файла.
    """
    if os.path.exists(filename):
        data = open(filename, 'rb').read()
        return bytearray(data)
    else:
        print('WARNING. Don\'t exist file <%s>' % filename)
    return None


def read_text_file_lines(txt_filename):
    """
    Прочитать текстовый файл как список строк.
    @param txt_filename: Полное имя текстового файла.
    @return: Список строк файла.
    """
    if not os.path.exists(txt_filename):
        # Если файла не существует, то создать его
        if log:
            log.warning(u'Файл <%s> не существует.' % txt_filename)
        else:
            print(u'Файл <%s> не существует.' % txt_filename)

        f = None
        try:
            f = open(txt_filename, 'wt')
            f.close()
            if log:
                log.info(u'Создан текстовый файл <%s>' % txt_filename)
            else:
                print(u'Создан текстовый файл <%s>' % txt_filename)
        except:
            if f:
                f.close()
            if log:
                log.fatal(u'Ошибка создания текстового файла <%s>' % txt_filename)
            else:
                print(u'Ошибка создания текстового файла <%s>' % txt_filename)
        return list()

    f = None
    lines = list()
    try:
        f = open(txt_filename, 'rt')
        lines = f.readlines()
        lines = [filename.strip() for filename in lines]
        f.close()
        f = None
    except:
        if f:
            f.close()
        if log:
            log.fatal(u'Ошибка чтения текстового файла <%s>' % txt_filename)
        else:
            print(u'Ошибка чтения текстового файла <%s>' % txt_filename)
    return list(lines)


def append_text_file_line(line, txt_filename=None):
    """
    Записать линию в текстовый файл.
    @param line: Линия в виде строки.
    @param txt_filename: Полное имя текстового файла.
    @return: True/False.
    """
    f = None
    try:
        f = open(txt_filename, 'at+')
        f.write(str(line))
        # Добавить перевод на новую строку
        f.write('\n')
        f.close()
        return True
    except:
        if f:
            f.close()
        if log:
            log.fatal(u'Ошибка записи линии в текстовый файл <%s>' % txt_filename)
        else:
            print(u'Ошибка записи линии в текстовый файл <%s>' % txt_filename)
    return False


def is_float_str(txt):
    """
    Определить является ли строка числом с плавающей запятой.
    @param txt: Анализируемая строка.
    @return: True/False
    """
    try:
        float(txt)
        return True
    except ValueError:
        return False


def is_int_str(txt):
    """
    Определить является ли строка целым числом.
    @param txt: Анализируемая строка.
    @return: True/False
    """
    return txt.isdigit()


def is_None_str(txt):
    """
    Определить является ли строка None.
    @param txt: Анализируемая строка.
    @return: True/False
    """
    return txt.strip() == 'None'


def wise_type_translate_str(txt):
    """
    Преобразование типа из строки к реальному типу.
    @param txt: Анализируемая строка.
    @return: Значение строки реального типа.
        Например:
            txt = 'None' - Результат None
            txt = '099' - Результат 99
            txt = '3.14' - Результат 3.14
            txt = 'XYZ' - Результат 'XYZ'
    """
    if is_None_str(txt):
        return None
    elif is_int_str(txt):
        return int(txt)
    elif is_float_str(txt):
        return float(txt)
    # Не можем преобразовать в какой либо вид
    # Значит это строка
    return txt


def test():
    """
    Функция тестирования.
    """
    result = get_options(['--dosemu=/home/user/.dosemu', '--option2', 'aaaa'])
    print('TEST>>>', result)


if __name__ == '__main__':
    test()
