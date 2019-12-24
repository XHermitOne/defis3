#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Модуль переконвертации файла формата cPickle python3 в обычный текстовый файл.
"""

import os
import os.path
import sys
import pickle


def load_pickle_data(filename):
    """
    Загрузить данные из файла.

    :param filename: Полное имя файла.
    :return: Структура данных содержимого файла.
    """
    file_obj = None
    try:
        file_obj = open(filename, 'rb')
        body = pickle.load(file_obj)
        file_obj.close()
        return body
    except:
        if file_obj:
            file_obj.close()
        raise
    return None


def save_text_data(filename, data):
    """
    Сохранить данные в текстовый файл.

    :param filename: Полное имя файла.
    :param data: Структура записываемых данных.
    :return: True/False.
    """
    if os.path.exists(filename):
        print(u'Файл <%s> уже существует' % filename)
        return False

    file_obj = None
    try:
        file_obj = open(filename, 'wt')
        text = str(data)
        file_obj.write(text)
        file_obj.close()
        return True
    except:
        if file_obj:
            file_obj.close()
        raise
    return False


def run(filename):
    """
    Функция выполнения

    :param filename: Полное имя файла.
    :return:
    """
    print(u'Обработка файла <%s>...' % filename)
    filename = os.path.abspath(os.path.normpath(filename))
    print(u'...Обработка файла <%s>' % filename)

    if not os.path.exists(filename):
        print(u'Файл <%s> не существует' % filename)
        return

    body = load_pickle_data(filename)
    if body:
        os.remove(filename)
        save_text_data(filename, body)


if __name__ == '__main__':
    cmd_params = sys.argv[1:]
    run(cmd_params[0])
