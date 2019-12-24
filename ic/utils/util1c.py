#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
Сервисные функции программиста.
"""

import os
import os.path
import wx

import ic.utils.impfunc
from . import strfunc

__version__ = (0, 1, 2, 2)


def findValueIndexPath(cur_list, value, idx=None):
    """
    Функция позволяет найти значение в сложном списке списков и 
    возвращает кореж индексов-пути до этого элемента.
    """
    if idx is None:
        idx = []
    if isinstance(idx, tuple):
        idx = list(idx)
        
    if value in cur_list:
        idx = cur_list.index(value)
        idx.append(idx)
        return tuple(idx)
    else:
        # Поиск в подсписках
        idx.append(-1)
        for i, element in enumerate(cur_list):
            if isinstance(element, list):
                idx[-1] = i
                idx_lst = findValueIndexPath(element, value, tuple(idx))
                if idx_lst:
                    return idx_lst
    # Ничего найти не удалось
    return None


def get_idx_paths(data_list, parent_idx=None):
    """
    Список всех элементов в сложном списке списков с указанием индексов пути.

    :param data_list: Сложная списковая структура.
    :return: Список формата:
        [ (Значение, Кортеж индексного пути),
        ]
    """
    result = list()
    if isinstance(data_list, list):
        for i, value in enumerate(data_list):
            if isinstance(value, list):
                value_path = parent_idx + [i] if parent_idx else [i]
                result += get_idx_paths(value, value_path)
            else:
                value_path = list(parent_idx + list(findValueIndexPath(data_list, value)) if parent_idx else findValueIndexPath(data_list, value))
                result.append((value, value_path))

    return result


def print_idx_paths(data_list):
    """
    Распечатать список всех элементов в сложном списке списков
    с указанием индексов пути.

    :param data_list: Сложная списковая структура.
    """
    list_paths = get_idx_paths(data_list)
    for idx_path in list_paths:
        print('Value: <%s> Index path: %s' % (idx_path[0], idx_path[1]))


def getModuleDoc(module_filename):
    """
    Определить текст документации модуля.

    :param module_filename: Полное имя файла модуля.
    """
    module_name = None
    try:
        module_name = os.path.splitext(os.path.basename(module_filename))[0]
        # module = imp.load_source(module_name, module_filename)
        module = ic.utils.impfunc.loadSource(module_name, module_filename)
        if hasattr(module, '__doc__'):
            if wx.Platform == '__WXGTK__':
                return module.__doc__
            elif wx.Platform == '__WXMSW__':
                return str(module.__doc__, 'utf-8')
            else:
                return module.__doc__
    except:
        print('ERROR: In function \'util.getModuleDoc\'.Module file: %s Module name: %s' % (module_filename, module_name))
    return None


def genUID():
    """
    Функция генерации уникального идентификатора UID в формате
    XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX.
    """
    import pythoncom
    uid = pythoncom.CreateGuid()
    return str(uid)[1:-1]


def encodeText(text, src_codepage=None, dst_codepage='utf-8'):
    """
    Перекодировать текст из одной кодировки в другую.

    :param text: Сам текст.
    :param src_codepage: Кодировка исходного текста.
    :param dst_codepage: Кодировка результата.
    :return: Текст в нужной кодировке.
    """
    if (dst_codepage is None) or (dst_codepage.lower() == 'unicode'):
        if isinstance(text, str):
            # return str(text, src_codepage)
            return text
        # elif isinstance(text, unicode):
        #     return text
        return text

    if isinstance(text, str):
        if (src_codepage is not None) and (src_codepage.lower() != 'unicode'):
            txt = str(text, encoding=src_codepage)
        else:
            txt = str(text, encoding='utf-8')
    else:
        txt = str(text)
        
    return txt.encode(dst_codepage)


def splitName1CWord(Txt_):
    """
    Разделить текст имен объектов на слова как в 1С.
    Например:
    'ДокументСписокПередНачаломДобавления'->'Документ список перед началом добавления'.
    """
    # if isinstance(txt, str):
    #     return _splitName1CWordUNICODE(txt)
    if isinstance(Txt_, str):
        return _splitName1CWordUNICODE(Txt_)
    return Txt_


def _splitName1CWordUTF8(Txt_):
    result = ''
    if len(Txt_):
        result = Txt_[0]
        for symbol in Txt_[1:]:
            if symbol in strfunc.RU_REG_UPPER_LIST:
                symbol = ' ' + strfunc.RU_REG_LOWER_DICT[symbol]
            result += symbol
    return result


def _splitName1CWordUNICODE(Txt_):
    result = u''
    if len(Txt_):
        result = Txt_[0]
        for symbol in Txt_[1:]:
            if symbol in strfunc.U_RU_REG_UPPER_LIST:
                symbol = u' ' + strfunc.U_RU_REG_LOWER_DICT[symbol]
            result += symbol
    return result
