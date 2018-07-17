#!/usr/bin/env python
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

# --- Константы ---
_Clipboard = None

# --- Функции ---


def toClipboard(Obj_):
    """
    Положить объект в клипбоард.
    @param Obj_: Объект.
    """
    if type(Obj_) in (str, unicode):
        # Строку можно запихать непосредственно в клтпбоард.
        txt_data_clipboard = wx.TextDataObject()
        txt_data_clipboard.SetText(Obj_)
        wx.TheClipboard.Open()
        wx.TheClipboard.SetData(txt_data_clipboard)
        wx.TheClipboard.Close()
        # Очистить внутренний буфер
        global _Clipboard
        _Clipboard = None
        return True
    else:
        # Обычный объект просто запихнуть во внутренний буфер
        global _Clipboard
        _Clipboard = Obj_
        # Очистить системный клипбоард
        wx.TheClipboard.Open()
        wx.TheClipboard.Clear()
        wx.TheClipboard.Close()
        return True


def fromClipboard(Clear_=True):
    """
    Получить содержимое клипборда.
    @param Clear_: Признак того,  что после извлечения содержимое очищается.
    """
    global _Clipboard
    if _Clipboard:
        buff = _Clipboard
        if Clear_:
            clearClipboard()
        return buff
    else:
        txt_data_clipboard = wx.TextDataObject()
        wx.TheClipboard.Open()
        success = wx.TheClipboard.GetData(txt_data_clipboard)
        wx.TheClipboard.Close()
        if success:
            txt_data = txt_data_clipboard.GetText()
            if Clear_:
                clearClipboard()
            return txt_data
    return None


def clearClipboard():
    """
    Очистить клипбоард.
    """
    # Очистить внутренний буфер
    global _Clipboard
    _Clipboard = None
    # Очистить системный клипбоард
    wx.TheClipboard.Open()
    wx.TheClipboard.Clear()
    wx.TheClipboard.Close()


def emptyClipboard():
    """
    Проверка клипбоарда. Пустой или нет.
    @return: True-если клипбоард пустой.
        False-если в клипбоарде что-либо есть.
    """
    # Проверка внутреннего буфера
    global _Clipboard
    empty_my_buff = bool(_Clipboard==None)
    # Проверка системного клипборда
    txt_data_clipboard = wx.TextDataObject()
    wx.TheClipboard.Open()
    empty_sys_clipboard = not wx.TheClipboard.GetData(txt_data_clipboard)
    wx.TheClipboard.Close()
    #
    return bool(empty_my_buff and empty_sys_clipboard)
