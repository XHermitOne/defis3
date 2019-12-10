#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль функций для работы с клипбордом.
Системный клипбоард работает только со строками.
Поэтому если надо поместить значение в системный клтпбоард, 
то необходимо сначала представить его в виде строки, а
затем помещать его в клипбоард.
Обычные объекты помещаются во внутренний буфер программы.
"""

# --- Подключение пакетов ---
import wx

__version__ = (0, 1, 1, 2)

# --- Константы ---
CLIPBOARD = None


# --- Функции ---
def toClipboard(cur_object):
    """
    Положить объект в клипбоард.
    :param cur_object: Объект.
    """
    global CLIPBOARD
    if isinstance(cur_object, str):
        # Строку можно запихать непосредственно в клтпбоард.
        txt_data_clipboard = wx.TextDataObject()
        txt_data_clipboard.SetText(cur_object)
        wx.TheClipboard.Open()
        wx.TheClipboard.SetData(txt_data_clipboard)
        wx.TheClipboard.Close()
        # Очистить внутренний буфер
        CLIPBOARD = None
        return True
    else:
        # Обычный объект просто запихнуть во внутренний буфер
        CLIPBOARD = cur_object
        # Очистить системный клипбоард
        wx.TheClipboard.Open()
        wx.TheClipboard.Clear()
        wx.TheClipboard.Close()
        return True


def fromClipboard(bClear=True):
    """
    Получить содержимое клипборда.
    :param bClear: Признак того,  что после извлечения содержимое очищается.
    """
    global CLIPBOARD
    if CLIPBOARD:
        buff = CLIPBOARD
        if bClear:
            clearClipboard()
        return buff
    else:
        txt_data_clipboard = wx.TextDataObject()
        wx.TheClipboard.Open()
        success = wx.TheClipboard.GetData(txt_data_clipboard)
        wx.TheClipboard.Close()
        if success:
            txt_data = txt_data_clipboard.GetText()
            if bClear:
                clearClipboard()
            return txt_data
    return None


def clearClipboard():
    """
    Очистить клипбоард.
    """
    # Очистить внутренний буфер
    global CLIPBOARD
    CLIPBOARD = None
    # Очистить системный клипбоард
    wx.TheClipboard.Open()
    wx.TheClipboard.Clear()
    wx.TheClipboard.Close()


def emptyClipboard():
    """
    Проверка клипбоарда. Пустой или нет.
    :return: True-если клипбоард пустой.
        False-если в клипбоарде что-либо есть.
    """
    # Проверка внутреннего буфера
    global CLIPBOARD
    empty_my_buff = bool(CLIPBOARD==None)
    # Проверка системного клипборда
    txt_data_clipboard = wx.TextDataObject()
    wx.TheClipboard.Open()
    empty_sys_clipboard = not wx.TheClipboard.GetData(txt_data_clipboard)
    wx.TheClipboard.Close()
    #
    return bool(empty_my_buff and empty_sys_clipboard)
