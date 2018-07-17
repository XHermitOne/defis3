#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Функции работы с XML файлами и XML представлениями.
"""

import os
import os.path
from ic.contrib import xmltodict
from ic.contrib import dicttoxml
from ic.log import log
from ic.convert import simple_dict2xml

__version__ = (0, 0, 1, 1)


def load_xml_content(xml_filename, is_change_keys=True):
    """
    Загрузить содержимое XML файла в словарно списковую структуру.
    @param xml_filename: Полное имя XML файла.
    @param is_change_keys: Произвести автоматическую замену ключей на короткие.
    @return: Словарно-списковая структура содержания XML файла.
        Или None в случае ошибки.
    """
    if not os.path.exists(xml_filename):
        log.warning(u'XML файл <%s> не найден' % xml_filename)
        return None

    xml_file = None
    try:
        xml_file = open(xml_filename, 'r')
        xml_txt = xml_file.read()
        xml_file.close()
    except:
        if xml_file:
            xml_file.close()
        log.fatal(u'Ошибка загрузки содержимого XML файла <%s>' % xml_filename)
        return None

    data = xmltodict.parse(xml_txt)
    if is_change_keys:
        data = change_keys_doc(data)
    return data


def change_keys_doc(xml_document):
    """
    Сократить ключи документа.
    @param xml_document: Содержание XML документа.
    @return: Содержание документа с короткими ключами.
    """
    result = dict()
    for key in xml_document.keys():
        # Взять только часть ключа с <:> и до конца
        new_key = key.split(':')[-1]
        if isinstance(xml_document[key], xmltodict.OrderedDict):
            result[new_key] = change_keys_doc(xml_document[key])
        elif isinstance(xml_document[key], list):
            result[new_key] = list()
            for doc_element in xml_document[key]:
                result[new_key].append(change_keys_doc(doc_element))
        else:
            result[new_key] = xml_document[key]
    return result


def save_xml_content(xml_filename, data, is_rewrite=True):
    """
    Записать словарно списковую структуру в XML файл.
    @param xml_filename: Полное имя XML файла.
    @param data: Словарно-списковая структура содержания XML файла.
    @param is_rewrite: Перезаписать результирующий файл, если необходимо?
    @return: True/False.
    """
    if os.path.exists(xml_filename) and not is_rewrite:
        log.warning(u'Запрет на перезапись. Файл <%s> уже существует.' % xml_filename)
        return False

    # Сама конвертация словаря в текст
    if isinstance(data, list):
        xml_txt = dicttoxml.dicttoxml(data, root=True,
                                      custom_root='root',
                                      ids=False, attr_type=False)
    elif isinstance(data, dict):
        root_key = data[data.keys()[0]]
        xml_txt = dicttoxml.dicttoxml(data, root=False,
                                      custom_root=root_key,
                                      ids=False, attr_type=False)
    else:
        log.warning(u'Не корректный тип данных <%s> для записи в XML файл' % type(data))
        return False

    xml_file = None
    try:
        xml_file = open(xml_filename, 'w')
        xml_file.write(xml_txt)
        xml_file.close()
        return True
    except:
        if xml_file:
            xml_file.close()
        log.fatal(u'Ошибка записи в файл <%s>' % xml_filename)
    return False


def save_simple_xml_content(xml_filename, data, is_rewrite=True, tag_filter=None):
    """
    Записать словарно списковую структуру в XML файл.
    Самая простая реализация.
    @param xml_filename: Полное имя XML файла.
    @param data: Словарно-списковая структура содержания XML файла.
    @param is_rewrite: Перезаписать результирующий файл, если необходимо?
    @param tag_filter: Словарь фильтра тегов,
        определяющий список и порядок дочерних тегов для
        каждого тега.
        Порядок тегов важен для XML, поэтому введен этот фильтр.
    @return: True/False.
    """
    if os.path.exists(xml_filename) and not is_rewrite:
        log.warning(u'Запрет на перезапись. Файл <%s> уже существует.' % xml_filename)
        return False

    xml_file = None
    try:
        # Начать запись
        xml_file = open(xml_filename, 'wt')
        xml_writer = simple_dict2xml.icSimpleDict2XmlWriter(data, xml_file)
        xml_writer.startDocument()
        xml_writer.startWrite(tag_filter=tag_filter)

        # Закончить запись
        xml_writer.endDocument()
        xml_file.close()
        return True
    except:
        if xml_file:
            xml_file.close()
        log.fatal(u'Ошибка записи в файл <%s>' % xml_filename)
    return False

