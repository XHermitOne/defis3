#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль диалоговой формы отображения отладочной информации.
"""

import traceback
import wx

from . import view_debug_message_dlg_proto

from ic.log import log
from ic.utils import wxfunc

__version__ = (0, 1, 1, 1)


class icViewDebugMessageDlg(view_debug_message_dlg_proto.icViewDebugMsgDialogProto):
    """
    Диалоговая форма отображения отладочной информации.
    По кнопке <Дополнительно> открывается диалог просмотра
    локального (locals) и глобального (globals) пространства имен.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        view_debug_message_dlg_proto.icViewDebugMsgDialogProto.__init__(self, *args, **kwargs)

    def setErrorIcon(self):
        """
        Установить иконку ОШИБКИ.
        """
        bmp = wx.ArtProvider.GetBitmap(wx.ART_ERROR, size=wx.ART_CMN_DIALOG)
        self.icon_bitmap.SetBitmap(bmp)

    def setWarningIcon(self):
        """
        Установить иконку ПРЕДУПРЕЖДЕНИЯ.
        """
        bmp = wx.ArtProvider.GetBitmap(wx.ART_WARNING, size=wx.ART_CMN_DIALOG)
        self.icon_bitmap.SetBitmap(bmp)

    def setInfoIcon(self):
        """
        Установить иконку ИНФОРМАЦИИ.
        """
        bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, size=wx.ART_CMN_DIALOG)
        self.icon_bitmap.SetBitmap(bmp)

    def setMessage(self, message_text):
        """
        Установить сообщение.
        @param message_text: Текст сообщения.
        """
        if not isinstance(message_text, str):
            message_text = str(message_text)

        self.msg_textCtrl.SetValue(message_text)

    def setErrorMessage(self, message_text):
        """
        Установить сообщение об ОШИБКЕ.
        @param message_text: Текст сообщения.
        """
        self.setErrorIcon()
        text_colour = wxfunc.adaptSysThemeColour(dark_theme_colour=wx.RED)
        self.msg_textCtrl.SetForegroundColour(text_colour)
        self.setMessage(message_text=message_text)

    def setWarningMessage(self, message_text):
        """
        Установить ПРЕДУПРЕЖДАЮЩЕЕ сообщение.
        @param message_text: Текст сообщения.
        """
        self.setWarningIcon()
        text_colour = wxfunc.adaptSysThemeColour(dark_theme_colour=wx.YELLOW)
        self.msg_textCtrl.SetForegroundColour(text_colour)
        self.setMessage(message_text=message_text)

    def setInfoMessage(self, message_text):
        """
        Установить ИНФОРМАЦИОННОЕ сообщение.
        @param message_text: Текст сообщения.
        """
        self.setInfoIcon()
        text_colour = wxfunc.adaptSysThemeColour(dark_theme_colour=wx.GREEN)
        self.msg_textCtrl.SetForegroundColour(text_colour)
        self.setMessage(message_text=message_text)

    def onOkButtonClick(self, event):
        """
        Обработчик кнопки OK.
        """
        self.EndModal(wx.ID_OK)
        event.Skip()


def view_debug_error_dlg(parent=None, message_text=u''):
    """
    Показать сообшение об ОШИБКЕ в диалоге для отладки.
    @param parent: Родительское окно.
        Если не определено, то берется главное окно программы.
    @param message_text: Текст сообщения.
    @return: True/False.
    """
    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    try:
        dlg = icViewDebugMessageDlg(parent=parent)
        dlg.setErrorMessage(message_text=message_text)
        dlg.ShowModal()
        return True
    except:
        log.fatal(u'Ошибка вывода сообщения об ОШИБКЕ в диалоговом окне')
    return False


def view_debug_warning_dlg(parent=None, message_text=u''):
    """
    Показать ПРЕДУПРЕЖДАЮЩЕЕ сообшение в диалоге для отладки.
    @param parent: Родительское окно.
        Если не определено, то берется главное окно программы.
    @param message_text: Текст сообщения.
    @return: True/False.
    """
    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    try:
        dlg = icViewDebugMessageDlg(parent=parent)
        dlg.setWarningMessage(message_text=message_text)
        dlg.ShowModal()
        return True
    except:
        log.fatal(u'Ошибка вывода сообщения ПРЕДУПРЕЖДЕНИЯ в диалоговом окне')
    return False


def view_debug_info_dlg(parent=None, message_text=u''):
    """
    Показать ИНФОРМАЦИОННОГО сообшения в диалоге для отладки.
    @param parent: Родительское окно.
        Если не определено, то берется главное окно программы.
    @param message_text: Текст сообщения.
    @return: True/False.
    """
    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    try:
        dlg = icViewDebugMessageDlg(parent=parent)
        dlg.setInfoMessage(message_text=message_text)
        dlg.ShowModal()
        return True
    except:
        log.fatal(u'Ошибка вывода ИНФОРМАЦИОННОГО сообщения в диалоговом окне')
    return False


def view_debug_exception_dlg(parent=None, exception_msg_fmt=None):
    """
    Показать сообшение об КРИТИЧЕСКОЙ ОШИБКЕ (EXCEPTION) в диалоге для отладки.
    @param parent: Родительское окно.
        Если не определено, то берется главное окно программы.
    @param exception_msg_fmt: Формат для дополнения сообщения критической ошибки.
    @return: True/False.
    """
    exception_text = traceback.format_exc()

    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    try:
        dlg = icViewDebugMessageDlg(parent=parent)
        message_text = exception_msg_fmt % exception_text if exception_msg_fmt else exception_text
        dlg.setErrorMessage(message_text=message_text)
        dlg.ShowModal()
        return True
    except:
        log.fatal(u'Ошибка вывода сообщения об КРИТИЧЕСКОЙ ОШИБКЕ (EXCEPTION) в диалоговом окне')
    return False
