#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль сервисных функций программиста
"""

# Подключение библиотек
import sys
from types import *
import os.path
import wx
import hashlib

from encodings import aliases

try:
    import win32api
    import win32con
    import regutil
except ImportError:
    pass

try:
    from . import DevId
except:
    pass

from ic.log import log
from . import util
from . import strfunc

_ = wx.GetTranslation

__version__ = (0, 1, 2, 1)


def defineSpcStruct(spc, struct):
    """
    Дополняет структуру описания объекта до требований спецификации.
    @type spc: C{dictionary}.
    @param spc: Словарь описания спецификации.
    @type struct: C{dictionary}.
    @param struct: Словарь описания структуры.
    @rtype: C{dictionary}.
    @return: Дополненная структура.
    """
    try:
        def_struct = util.icSpcDefStruct(spc, struct)
        # Коррекция типов
        for name, value in def_struct.items():
            if name in spc and isinstance(def_struct['name'], str) and not isinstance(spc['name'], str):
                try:
                    # Возможно это не строка
                    def_value = eval(value)
                except:
                    # Нет наверно это строка
                    def_value = value
                def_struct[name] = def_value
        return def_struct
    except:
        return struct


def getAttrValue(attr_name, spc):
    """
    Получить нормированное значение свойства из спецификации.
    @param attr_name: Имя атрибута.
    @param spc: Спецификация.
    """
    try:
        # Нормализация по типам
        if isinstance(spc[attr_name], str):
            try:
                # Возможно это не строка
                value = eval(spc[attr_name])
            except:
                # Нет это все таки строка
                value = spc[attr_name]
            spc[attr_name] = value
        return spc[attr_name]
    except:
        log.fatal(u'Ошибка получения нормированного значения свойства из спецификации')
    return None


def getStrInQuotes(value):
    """
    Если value - строка то обрамляет ее одинарными кавычками, если нет,
    то просто преобразует в строку.
    """
    if isinstance(value, str):
        return '\'%s\'' % value
    else:
        return str(value)


# Наполнитель позиций при отображении вложенности пунктов
# в компоненте списка
PADDING = '    '


def StructToTxt(struct, level=0):
    """
    Перевод словарно-списковой структуры в форматированный текст.
    @param struct : словарно-списковая структура.
    @param level: уровень вложенности (д.б. 0).
    """
    txt = ''
    try:
        obj_type = type(struct)
        if obj_type == list:
            txt = txt + '\n' + level * PADDING + '[\n'
            for obj in struct:
                txt += level * PADDING
                txt += StructToTxt(obj, level + 1)
                txt += ',\n'
            if len(struct) != 0:
                txt = txt[:-2]
            txt = txt + '\n' + level * PADDING + ']'
        elif obj_type == dict:
            txt = txt + '\n' + level * PADDING + '{\n'
            keys = struct.keys()
            values = struct.values()
            for key in keys:
                txt = txt + level * PADDING + '\'' + key + '\':'
                txt += StructToTxt(struct[key], level + 1)
                txt += ',\n'
            if len(keys) != 0:
                txt = txt[:-2]
            txt = txt + '\n' + level * PADDING + '}'
        elif obj_type == str:
            # Появляется косяк с разделителем папок в именах путей
            # Проверка на кавычки
            txt = txt + '\'' + struct.replace('\'',
                                              '\\\'').replace('\'',
                                                              '\\\'').replace('\r',
                                                                              '\\r').replace('\n',
                                                                                             '\\n').replace('\t',
                                                                                                            '\\t') + '\''
        else:
            txt = txt + str(struct)

        # Убрать первый перевод каретки
        if txt[0] == '\n' and (not level):
            txt = txt[1:]
    except:
        log.fatal(u'Ошибка Level <%d>' % level)
    return txt


def delKeyInDictTree(struct, key):
    """
    Функция удаляет из словаря рекурсивно все указанные ключи.
    @param struct: Непосредственно словарь или список.
    @param key: Ключ, который необходимо удалить.
    """
    # Если это у нас словарь, то ...
    if isinstance(struct, dict):
        try:
            # Сначала удаляем ключ на этом уровне.
            del struct[key]
        except:
            pass
        # Затем спускаемся на уровень ниже и обрабатываем
        for item in struct.values():
            delKeyInDictTree(item, key)
    # а если список, то перебираем элементы
    elif isinstance(struct, list):
        for item in struct:
            delKeyInDictTree(item, key)
    # а если не то и не другое, то ничего с ним не делать
    else:
        return


def setKeyInDictTree(struct, key, value):
    """
    Функция устанавливает значенеи ключа в словаре рекурсивно.
    @param struct: Непосредственно словарь или список.
    @param key: Ключ, который необходимо установить.
    @param value: Значение ключа.
    """
    # Если это у нас словарь, то ...
    if isinstance(struct, dict):
        try:
            # Сначала устанавливаем ключ на этом уровне.
            struct[key] = value
        except:
            pass
        # Затем спускаемся на уровень ниже и обрабатываем
        for item in struct.values():
            setKeyInDictTree(item, key, value)
    # а если список, то перебираем элементы
    elif isinstance(struct, list):
        for item in struct:
            setKeyInDictTree(item, key, value)
    # а если не то и не другое, то ничего с ним не делать
    else:
        return


def doEval(code_block, log_type=-1,
           local_namespace=None, global_namespace=None, message=''):
    """
    Функция выполняет предобработку вычисляемого выражения, вычисляет с
    использование стандартной, функции eval(...), а также обрабатывает исключения. 
    В качестве локального пространства имен используется словарь LocalSpace. 
    В качестве глобального пространства имен берется словарь GlobalSpace.
    @type code_block: C{string}
    @param code_block: Вычисляемое выражение.
    @type log_type: C{int}
    @param log_type: Тип лога (0 - консоль, 1- файл, 2- окно лога)
    @param local_namespace: Пространство имен, необходимых для вычисления выражения
    @type local_namespace: C{dictionary}
    @param global_namespace: Глобальное пространство имен.
    @type global_namespace: C{dictionary}
    """
    if local_namespace is None:
        local_namespace = {}

    ret_val = util.ic_eval(code_block, log_type, local_namespace, message, global_namespace)
    # Проверка правильно ли выполнена операция
    if ret_val[0] == 1:
        return ret_val[1]
    return None


def setFilesToGlob(*args):
    """
    Поместить структуры, хранящиеся в файлах в глобальное пространство имен.
    @param args: Имена файлов и имена структур в глобальном пространстве состояний
        передаются в формате:
            (ИмяСтруктуры1, ИмяФайла1), (ИмяСтруктуры2, ИмяФайла2),...
    """
    try:
        for cur_arg in args:
            if os.path.isfile(cur_arg[1]):
                tmp_buff = util.readAndEvalFile(cur_arg[1])
                globals()[cur_arg[0]] = tmp_buff
            else:
                log.warning(u'Не найден файл <%s>' % cur_arg[1])
        return True
    except:
        log.fatal(u'Ошибка размещения файлов в глобальном пространстве имен')
    return False


def recodeText(text, old_codepage, new_codepage):
    """
    Перекодировать из одной кодировки в другую.
    @param text: Строка.
    @param old_codepage: Кодовая страница строки.
    @param new_codepage: Новая кодовая страница строки.
    @return: Перекодированная строка.
    """
    if new_codepage.upper() == 'UNICODE':
        # Кодировка в юникоде.
        return text

    if new_codepage.upper() == 'OCT' or new_codepage.upper() == 'HEX':
        # Закодировать строку в восьмеричном/шестнадцатеричном виде.
        return toOctHexString(text, new_codepage)

    string = text
    if isinstance(text, str):
        if old_codepage.upper() != 'UNICODE':
            string = text
    elif isinstance(text, bytes):
        string = text.decode(new_codepage)

    return string


def toOctHexString(text, to_code):
    """
    Закодировать строку в восьмеричном/шестнадцатеричном виде.
    Символы с кодом < 128 не кодируются.
    @param text:
    @param to_code: Кодировка 'OCT'-восьмеричное представление.
                            'HEX'-шестнадцатеричное представление.
    @return: Возвращает закодированную строку.
    """
    try:
        if to_code.upper() == 'OCT':
            fmt = '\\%o'
        elif to_code.upper() == 'HEX':
            fmt = '\\x%x'
        else:
            # Ошибка аргументов
            log.warning('Argument error in toOctHexString.')
            return None
        # Перебор строки по символам
        ret_str = ''
        for char in text:
            code_char = ord(char)
            # Символы с кодом < 128 не кодируются.
            if code_char > 128:
                ret_str += fmt % code_char
            else:
                ret_str += char
        return ret_str
    except:
        log.fatal()
        return None


def recodeListStr(list_data, old_codepage, new_codepage):
    """
    Перекодировать все строки в списке рекурсивно в другую кодировку.
    Перекодировка производится также внутри вложенных словарей и кортежей.
    @param list_data: Сам список.
    @param old_codepage: Кодовая страница строки.
    @param new_codepage: Новая кодовая страница строки.
    @return: Возвращает преобразованный список.
    """
    lst = []
    # Перебор всех элементов списка
    for i in range(len(list_data)):
        if isinstance(list_data[i], list):
            # Елемент - список
            value = recodeListStr(list_data[i], old_codepage, new_codepage)
        elif isinstance(list_data[i], dict):
            # Елемент списка - словарь
            value = recodeDictStr(list_data[i], old_codepage, new_codepage)
        elif isinstance(list_data[i], tuple):
            # Елемент списка - кортеж
            value = recodeTupleStr(list_data[i], old_codepage, new_codepage)
        elif isinstance(list_data[i], str):
            value = recodeText(list_data[i], old_codepage, new_codepage)
        else:
            value = list_data[i]
        lst.append(value)
    return lst


def recodeDictStr(dict_data, old_codepage, new_codepage):
    """
    Перекодировать все строки в словаре рекурсивно в другую кодировку.
    Перекодировка производится также внутри вложенных словарей и кортежей.
    @param dict_data: Сам словарь.
    @param old_codepage: Кодовая страница строки.
    @param new_codepage: Новая кодовая страница строки.
    @return: Возвращает преобразованный словарь.
    """
    keys_ = dict_data.keys()
    # Перебор всех ключей словаря
    for cur_key in keys_:
        value = dict_data[cur_key]
        # Нужно ключи конвертировать?
        if strfunc.isRUSText(cur_key):
            new_key = recodeText(cur_key, old_codepage, new_codepage)
            del dict_data[cur_key]
        else:
            new_key = cur_key
            
        if isinstance(value, list):
            # Елемент - список
            dict_data[new_key] = recodeListStr(value, old_codepage, new_codepage)
        elif isinstance(value, dict):
            # Елемент - cловарь
            dict_data[new_key] = recodeDictStr(value, old_codepage, new_codepage)
        elif isinstance(value, tuple):
            # Елемент - кортеж
            dict_data[new_key] = recodeTupleStr(value, old_codepage, new_codepage)
        elif isinstance(value, str):
            dict_data[new_key] = recodeText(value, old_codepage, new_codepage)

    return dict_data


def recodeTupleStr(Tuple_, StringCP_, NewCP_):
    """
    Перекодировать все строки в кортеже рекурсивно в другую кодировку.
    Перекодировка производится также внутри вложенных словарей и кортежей.
    @param Tuple_: Сам кортеж.
    @param StringCP_: Кодовая страница строки.
    @param NewCP_: Новая кодовая страница строки.
    @return: Возвращает преобразованный кортеж.
    """
    # Перевести кортеж в список
    lst = list(Tuple_)
    # и обработать как список
    list_ = recodeListStr(lst, StringCP_, NewCP_)
    # Обратно перекодировать
    return tuple(list_)


def recodeStructStr(struct, old_codepage, new_codepage):
    """
    Перекодировать все строки в структуре рекурсивно в другую кодировку.
    @param struct: Сруктура (список, словарь, кортеж).
    @param old_codepage: Кодовая страница строки.
    @param new_codepage: Новая кодовая страница строки.
    @return: Возвращает преобразованную структру.
    """
    if isinstance(struct, list):
        # Список
        cur_struct = recodeListStr(struct, old_codepage, new_codepage)
    elif isinstance(struct, dict):
        # Словарь
        cur_struct = recodeDictStr(struct, old_codepage, new_codepage)
    elif isinstance(struct, tuple):
        # Кортеж
        cur_struct = recodeTupleStr(struct, old_codepage, new_codepage)
    elif isinstance(struct, str):
        # Строка
        cur_struct = recodeText(struct, old_codepage, new_codepage)
    else:
        # Тип не определен
        cur_struct = struct
    return cur_struct


def getHDDSerialNo():
    """
    Определить серийный номер HDD.
    """
    try:
        hdd_info = DevId.GetHDDInfo()
        return hdd_info[2]
    except:
        # Ошибка определения серийного номера HDD.
        log.fatal('Ошибка определения серийного номера HDD')
    return ''


def getRegValue(reg_key, reg_value=None):
    """
    Взять информацию из реестра относительно данного проекта.
    @param reg_key: Ключ реестра.
    @param reg_value: Имя значения из реестра.
    """
    hkey = None
    try:
        hkey = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, reg_key)
        value = win32api.RegQueryValueEx(hkey, reg_value)
        win32api.RegCloseKey(hkey)
        return value[0]
    except:
        if hkey:
            win32api.RegCloseKey(hkey)
        # Ошибка определения информации из реестра.
        # ic.log.ic_log.icWin32Err()
        log.fatal(u'Ошибка получения значения из реестра')
    return None


def findChildResByName(children_res, child_name):
    """
    Поиск ресурсного описания дочернего объекта по имени.
    @param children_res: Список ресурсов-описаний дечерних объектов.
    @return child_name: Имя искомого дочернего объекта.
    @return: Индекс ресурсного описания в списке, если 
        описания с таким именем не найдено, то возвращается -1.
    """
    try:
        return [child['name'] for child in children_res].index(child_name)
    except ValueError:
        return -1


def getFuncListInModule(module_obj=None):
    """
    Получить список имен функций в модуле.
    @param module_obj: Объект модуля.
        Для использования модуль д.б. импортирован.
    @return: Возвращает список кортежей:
        [(имя функции, описание функции, объект функции),...]
    """
    if module_obj:
        return [(func_name, module_obj.__dict__[func_name].__doc__, module_obj.__dict__[func_name]) for func_name in [f_name for f_name in module_obj.__dict__.keys() if type(module_obj.__dict__[f_name]) == FunctionType]]
    return None


def isOSWindowsPlatform():
    """
    Функция определения ОС.
    @return: True-если ОС-Windows и False во всех остальных случаях.
    """
    return bool(sys.platform[:3].lower() == 'win')


def get_encodings_list():
    """
    Список возможных кодировок.
    """
    try:
        encode_list = [str(code).lower() for code in aliases.aliases.values()]
        # Удалить дубликаты
        result = list()
        for code in encode_list:
            if code not in result:
                result.append(code)
        result.sort()
        return result
    except:
        return ['utf_8', 'utf_16', 'cp1251', 'cp866', 'koi8_r']


def encode_unicode_struct(struct, code_page='utf-8'):
    """
    Перекодировать все строки unicode структуры в  указанную кодировку.
    """
    return recodeStructStr(struct, 'UNICODE', code_page)


def get_check_summ(value):
    """
    Посчитать контрольную сумму переменной.
    @param value: Переменная, которая м.б. представлена в виде строки.
    @return: Возвращает md5 контрольную сумму или None в случае ошибки.
    """
    check_summ = None
    try:
        val = str(value)
        check_summ = hashlib.md5(val).hexdigest()
    except:
        log.fatal(u'Ошибка определения контрольной суммы')
    return check_summ


def is_pasport(passport):
    """
    Проверка является ли структура паспортом.
    @param passport: Проверяемая структура.
    @return: True/False.
    """
    if (isinstance(passport, tuple) or isinstance(passport, list)) and len(passport):
        return len(passport[0]) == 5
    else:
        from ic.kernel import icobject
        return isinstance(passport, icobject.icObjectPassport)
    return False


def get_tree_lst_length(tree_data):
    """
    Подсчет всех элементов дерева.
    @param tree_data: Данные дерева. Дерево представлено как список списков.
    @return: Количество элементов дерева.
    """
    result = 0
    for tree_element in tree_data:
        if not isinstance(tree_element, list):
            result += 1
        else:
            children_len = get_tree_lst_length(tree_element)
            result += children_len
    return result


def get_tree_length(tree_data, children_key='children'):
    """
    Подсчет всех элементов дерева. Элементы дерева - словари.
    Дочерние элементы находятся по ключу <children_key>.
    @param tree_data: Данные дерева. Дерево представлено как список списков.
    @param children_key: Ключ дочерних элементов.
    @return: Количество элементов дерева.
    """
    result = 0
    for tree_element in tree_data:
        result += 1
        if isinstance(tree_element, dict):
            children_len = get_tree_length(tree_element[children_key], children_key) if tree_element.get(children_key, None) else 0
            result += children_len
    return result


def print_defis_logo(text_colour=None):
    """
    Печать лого DEFIS в текстовом виде.
    """
    import ic

    if text_colour is None:
        text_colour = '\x1b[33m'

    version = '.'.join([str(v) for v in ic.__version__])
    copyright = ic.__copyright__.replace(u'Copyright', u'').strip()
    defis_logo_txt = strfunc.DEFIS_LOGO_TXT % (version, copyright)
    for line in defis_logo_txt.splitlines():
        log.print_color_txt(line, text_colour)
