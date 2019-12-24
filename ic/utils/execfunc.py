#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль функций выполнения запросов и методов пользователя.

:var SELF_DOT_TAG: Символ, определяющий в методе кода ссылку на объект,
    который вызывает этот метод.
:var CODE_UNIT_TAG: Если строка начинается с этого символа ('@'),
    то это выполняемая функция (блок кода).
"""

# --- Подключение библиотек ---
import wx
import os
import sys
import subprocess
import locale

from . import toolfunc
from . import filefunc
from . import util

from ic.utils import impfunc
from ic.log import log

__version__ = (0, 1, 1, 2)

_ = wx.GetTranslation

# --- Основные константы ---
RES_MODULE = 'module'   # модуль,  в котором находится функция, строка
RES_METHOD = 'method'   # функция, блок кода

SELF_DOT_TAG = '_.'
SELF_TAG = '#'
CODE_UNIT_TAG = '@'

# --- Спецификации ---
# Спецификация словаря функции
SPC_IC_EXEC = {RES_MODULE: '',   # модуль,  в котором находится функция, строка
               RES_METHOD: '@',  # функция, блок кода
               }

# Спецификация функции системы
SPC_IC_FUNC = {'name': 'func1',     # код-имя функции, строка
               'type': 'icFunc',    # тип 'icFunc', строка
               'description': '',   # описание, строка
               'import': {},        # словарь, описывающий импортируемые имена для вычисления выражений
               'function': '@',         # сама функция, строка
               'len': -1,           # длина возвращаемого значения, целое
               'mask': '',          # шаблон возвращаемого значения, регулярное выражение
               'date': None,        # дата последнего изменения, строка
               }


def execute_method(function, self=None):
    """
    Выполнить метод.

    :param self: ссылка на объект, который вызывает эту функцию.
    :param function: словарь функции (см. документацию на ресурсные файлы).
    """
    try:
        if self is not None:
            try:
                name_space = self.GetContext()
            except:
                name_space = util.InitEvalSpace(locals())
        else:
            name_space = util.InitEvalSpace(locals())
        name_space['self'] = self
        
        ret = util.ic_eval(function, evalSpace=name_space)
        
        if ret[0]:
            return ret[1]
        else:
            return None
    except:
        log.fatal(u'Execute method error: %s' % function)
        return None


def execute_code(code_block, self=None):
    """
    Выполнить блок кода.

    :param self: ссылка на объект, который вызывает эту функцию.
    :param function: строка функции.
        Если строка начинается с символа '@', то это выполняемая функция.
    """
    try:
        # Проверка аргументов
        if isinstance(code_block, str):
            return code_block
        elif code_block[0] != CODE_UNIT_TAG:
            return code_block
        # Убрать признак блока кода
        code_block = code_block[1:]
        # Перед выполнением метода заменить тег, определяющий объект,
        # который вызвал эту функцию, на self
        if self is not None:
            code_block = code_block.replace(SELF_DOT_TAG, 'self.')
        # Выполнить
        return toolfunc.doEval(code_block, 0, locals(), globals())
    except:
        log.fatal(u'Ошибка выполнения блока кода')


def is_empty_method(function):
    """
    Проверка пустой словарь функции или нет.

    :param function: Словарь функции.
    :return: Истина - если словарь пустой (ни модуль, ни метод не определены).
             В противном случае - ложь.
    """
    try:
        find = True
        if (not function) or function == 'None':
            return True

        # Проверка модуля
        if RES_MODULE in function and function[RES_MODULE]:
            find = False
        else:
            # Проверка метода
            if RES_METHOD in function and function[RES_METHOD] != '' and \
               function[RES_METHOD] != CODE_UNIT_TAG and function[RES_METHOD] is not None:
                find = False
        return find
    except:
        log.fatal(u'Function: %s' % function)


def getNameFuncFromCode(code_block):
    """
    Получить имя функции из блока кода.

    :param code_block: Блок кода.
        Блок кода - строка в формате:
            @ИмяФункции(аргументы)
    """
    try:
        # Убрали @
        name_func = code_block[1:]
        i_find = name_func.find('(')
        # Если это константа, тогда вернуть ее имя
        if i_find == -1:
            return name_func
        return name_func[:i_find]
    except:
        return ''


def doSysCmd(command):
    """
    Функция выполняет команду системы.

    :param command: Строка системной команды.
    """
    log.debug(u'Выполнение команды: <%s>' % command)
    return os.system(command)


def exec_function(function):
    """
    Выполнить функцию и возвратить значение.

    :param function: Описание функции (См. спецификацию SPC_IC_FUNC).
    :return: Возвращает значение,  которое возвращает функция.
    """
    name_space = dict()
    try:
        name_space = util.ic_import(function['import'])
        return util.ic_eval(function['function'], -1, name_space)
    except:
        log.fatal()
        return None


def execFuncByName(function_name, functions):
    """
    Выполнить функцию и возвратить значение по его имени.

    :param function_name: Имя функции (См. fnc_fmt.doc).
    :param functions: Описание функций (См. fnc_fmt.doc) или 
        имя файла где оно храниться.
    :return: Возвращает значение,  которое возвращает функция.
    """
    try:
        if isinstance(functions, str):
            functions = util.readAndEvalFile(functions)
        return exec_function(functions[function_name])
    except:
        log.fatal()
        return None


def doMethod(method_str, name_space=None):
    """
    Вызов метода.

    :param method_str: Строковый вызов метода.
        Например 'NSI.method1(a1=3,s2=4)'.
    :param name_space: Пространство имен.
    """
    try:
        # Сначала разобрать строку
        method_name = method_str.split('{')[0]
        if name_space is None:
            name_space = locals()
        method_args_str = method_str[len(method_name):]
        method_args = {}
        if method_args_str:
            method_args = eval(method_args_str, name_space)

        sub_sys = None
        if method_name.find('.') != -1:
            method_name_split = method_name.split('.')
            sub_sys = method_name_split[0]
            method_name = method_name_split[1]

        from ic.utils import resource
        value = resource.method(method_name, sub_sys, name_space, **method_args)
        return value
    except:
        log.fatal(u'Execute method error: %s' % method_str)
        return None


_run_py_code = """import sys
import ic.engine.main
from os.path import dirname, abspath

if not sys.argv[1:]:
    path = dirname(abspath(__file__)).replace("\\\\",'/') 
    main_sys = path.split('/')[-1]
    args = ['-run', '-dbg', '%s/%s/' % (path, main_sys), '-s']
    ic.engine.main.main(args)
else:
    ic.engine.main.run()
"""


def createRunApp(prj_dir):
    """
    Создать если надо модуль запуска прикладной системы.

    :return: True/False.
    """
    run_py_file_name = os.path.join(filefunc.get_absolute_path(prj_dir), 'run.py')
    
    if not os.path.exists(run_py_file_name):
        run_py_file = None
        try:
            run_py_file = open(run_py_file_name, 'wt')
            run_py_file.write(_run_py_code)
            run_py_file.close()
            return True
        except:
            if run_py_file:
                run_py_file.close()
            raise
    return False
        
    
def runTask(command):
    """
    Запуск команды, как отдельной задачи.

    :type command: C{string}
    :param command: Комманда системы.
    """
    if toolfunc.isOSWindowsPlatform():
        return runTaskBAT(command)
    return runTaskSH(command)


def runTaskSH(command):
    """
    Запуск команды, как отдельной задачи с отдельной консолью в Linux.

    :type command: C{string}
    :param command: Комманда системы.
    """
    run_sh_name = filefunc.get_absolute_path('./run.sh')
    if os.path.isfile(run_sh_name):
        os.remove(run_sh_name)
    f = None
    try:
        f = open(run_sh_name, 'wt')
        f.write(command)
        f.close()
        f = None
        # Запуск исполняемого скрипта
        log.info(u'run task: %s' % run_sh_name)
        os.system('gnome-terminal -- \'%s\'' % run_sh_name)
    except:
        log.fatal(u'run task error: %s' % run_sh_name)
        if f:
            f.close()


def runTaskBAT(command):
    """
    Запуск команды, как отдельной задачи с отдельной консолью.

    :type command: C{string}
    :param command: Комманда системы.
    """
    run_bat_name = filefunc.get_absolute_path('./run.bat')
    if os.path.isfile(run_bat_name):
        os.remove(run_bat_name)
    f = None
    try:
        f = open(run_bat_name, 'wt')
        f.write(command)
        f.close()
        f = None
        # Запуск батника
        log.info(u'run task: %s' % run_bat_name)
        os.startfile(run_bat_name)
    except:
        log.fatal(u'Ошибка запуска командного файла: %s' % run_bat_name)
        if f:
            f.close()


def runProgramm(command, exec_mode=os.P_NOWAIT):
    """
    Запуск программы на выполнение.

    :type command: C{string}
    :param command: Комманда системы.
    :param exec_mode: Режим выполнения команды. См os режимы выполнения.
    :return: True/False.
    """
    try:
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
        log.info(u'Запуск программы: %s' % args)
        os.spawnve(exec_mode, args[0], args, os.environ)
        return True
    except:
        log.fatal(u'Ошибка запуска программы: %s' % command)
        return False


def runOSCommand(command, bWait=True):
    """
    Запуск команды OC.

    :type command: C{string}
    :param command: Комманда системы.
    :param bWait: Команда ожидания процесса.
    :return: True/False.
    """
    try:
        if bWait:
            os.system(command)
        else:
            # Если ожидание выключено, то скорее всего это программа
            return runProgramm(command)
        return True
    except:
        log.fatal(u'Ошибка запуска команды ОС: %s' % command)
        return False


def execFuncStr(function_str, name_space=None, bReImport=False, *args, **kwargs):
    """
    Выполнение строковой функции в формате: пакеты.модуль.функция(аргументы).

    :type function_str: C{string}
    :param function_str: Строковая функция.
    :type name_space: C{dictionary}
    :param name_space: Пространство имен.
    :type bReImport: C{bool}
    :param bReImport: Переимпортировать модуль функции?
    :return: Вовращает результат выполнения функции или None  в случае ошибки.
    """
    result = None
    try:
        # Выделить модуль функции
        func_import = function_str.split('(')[0].split('.')
        func_mod = '.'.join(func_import[:-1])
        # Подготовить пространство имен
        if name_space is None or not isinstance(name_space, dict):
            name_space = {}

        # Выполнение функции
        try:
            try:
                if bReImport:
                    impfunc.unloadSource(func_mod)
                import_str = 'import '+func_mod
                exec(import_str)
            except:
                log.fatal(u'Ошибка импорта модуля: %s' % import_str)
            name_space.update(locals())
            result = eval(function_str, globals(), name_space)
        except:
            log.fatal(u'Ошибка запуска модуля: %s' % (function_str, func_mod))
    except:
        log.fatal(u'Ошибка в функции ic_exec.execFuncStr, %s' % function_str)
    
    return result


def exec_code(code_block='', bReImport=False, name_space=None, kwargs=None):
    """
    Выполнить блок кода.

    :type code_block: C{string}
    :param code_block: Блок кода.
        Блок кода - строка в формате:
            ИмяПакета.ИмяМодуля.ИмяФункции(аргументы).
    :type bReImport: C{bool}
    :param bReImport: Переимпортировать модуль функции?
    :type name_space: C{dictionary}
    :param name_space: Пространство имен.
    :type kwargs: C{dictionary}
    :param kwargs: Дополнительные аргументы функции.
    """
    result = None

    # Подготовить пространство имен
    if name_space is None or not isinstance(name_space, dict):
        name_space = {}

    # Определяем флаг что блок кода производит вызов функции
    is_exec_func = '(' in code_block and ')' in code_block
    # Элементы импорта
    func_import = code_block.split('(')[0].split('.')
    # Имя модуля или функции для работы с импортированным объектом
    func_mod = '.'.join(func_import[:-1])

    if bReImport:
        impfunc.unloadSource(func_mod)

    # Импортирование модуля
    if func_mod:
        import_str = 'import ' + func_mod
        try:
            exec(import_str)
            log.info(u'Импорт функции/модуля <%s>' % import_str)
        except:
            log.fatal(u'Ошибка импорта <%s>' % import_str)
            raise

    # Добавить локальное пространство имен
    name_space.update(locals())

    if kwargs:
        if isinstance(kwargs, dict):
            name_space.update(kwargs)
        else:
            log.warning(u'Не поддерживаемый тип <%s> дополнительных аргументов функции <%s>' % (type(kwargs), code_block))

    # Выполнение функции
    if is_exec_func:
        try:
            result = eval(code_block, globals(), name_space)
        except:
            log.fatal(u'Ошибка выполнения выражения <%s>' % code_block)
            raise
    else:
        log.warning(u'Не определен вызов функции в блоке кода <%s>' % code_block)

    return result


def exec_sys_cmd(command, split_lines=False):
    """
    Выполнить системную команду и получить результат ее выполнения.

    :param command: Системная команда.
    :param split_lines: Произвести разделение на линии?
    :return: Если нет разделения по линиям, то возвращается текст который
        отображается в консоли.
        При разбитии по линиям возвращается список выводимых строк.
        В случае ошибки возвращается None.
    """
    try:
        cmd = command.strip().split(' ')
        console_encoding = locale.getpreferredencoding()
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        if split_lines:
            b_lines = process.stdout.readlines()
            lines = [line.decode(console_encoding).strip() for line in b_lines]
            return lines
        else:
            b_text = process.stdout.read()
            text = b_text.decode(console_encoding)
            return text
    except:
        log.fatal(u'Ошибка выполнения системной команды <%s>' % command)
    return None
