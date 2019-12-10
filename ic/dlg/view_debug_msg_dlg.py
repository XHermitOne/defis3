#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль диалоговой формы отображения отладочной информации.
"""

import traceback
import wx

from . import view_debug_message_dlg_proto
from . import view_debug_env_dlg

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

        # Пространства имен для просмотра
        self._locals = None
        self._globals = None

    def init(self, env_locals=None, env_globals=None):
        """
        Инициализация диалогового окна.
        :param env_locals: Словарь локального пространства имен (locals).
        :param env_globals: Словарь глобального пространства имен (globals).
        """
        self._locals = env_locals
        self._globals = env_globals

        # Если не определено пространство имен, то и не надо просматривать
        self.extend_button.Enable(bool(self._locals) or bool(self._globals))

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
        :param message_text: Текст сообщения.
        """
        if not isinstance(message_text, str):
            message_text = str(message_text)

        self.msg_textCtrl.SetValue(message_text)

    def setErrorMessage(self, message_text):
        """
        Установить сообщение об ОШИБКЕ.
        :param message_text: Текст сообщения.
        """
        self.setErrorIcon()
        text_colour = wxfunc.adaptSysThemeColour(dark_theme_colour=wx.RED)
        self.msg_textCtrl.SetForegroundColour(text_colour)
        self.setMessage(message_text=message_text)

    def setWarningMessage(self, message_text):
        """
        Установить ПРЕДУПРЕЖДАЮЩЕЕ сообщение.
        :param message_text: Текст сообщения.
        """
        self.setWarningIcon()
        text_colour = wxfunc.adaptSysThemeColour(dark_theme_colour=wx.YELLOW)
        self.msg_textCtrl.SetForegroundColour(text_colour)
        self.setMessage(message_text=message_text)

    def setInfoMessage(self, message_text):
        """
        Установить ИНФОРМАЦИОННОЕ сообщение.
        :param message_text: Текст сообщения.
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

    def onExtendButtonClick(self, event):
        """
        Обработчик кнопки Дополнительно.
        """
        view_debug_env_dlg.view_debug_namespace_dialog(parent=self,
                                                       env_locals=self._locals, env_globals=self._globals)
        event.Skip()


def view_debug_error_dlg(parent=None, message_text=u'',
                         env_locals=None, env_globals=None):
    """
    Показать сообшение об ОШИБКЕ в диалоге для отладки.
    :param parent: Родительское окно.
        Если не определено, то берется главное окно программы.
    :param message_text: Текст сообщения.
    :param env_locals: Словарь локального пространства имен (locals).
    :param env_globals: Словарь глобального пространства имен (globals).
    :return: True/False.
    """
    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    dlg = None
    try:
        dlg = icViewDebugMessageDlg(parent=parent)
        dlg.init(env_locals=env_locals, env_globals=env_globals)
        dlg.setErrorMessage(message_text=message_text)
        dlg.ShowModal()
        dlg.Destroy()
        return True
    except:
        log.fatal(u'Ошибка вывода сообщения об ОШИБКЕ в диалоговом окне')
        if dlg:
            dlg.Destroy()
    return False


def view_debug_warning_dlg(parent=None, message_text=u'',
                           env_locals=None, env_globals=None):
    """
    Показать ПРЕДУПРЕЖДАЮЩЕЕ сообшение в диалоге для отладки.
    :param parent: Родительское окно.
        Если не определено, то берется главное окно программы.
    :param message_text: Текст сообщения.
    :param env_locals: Словарь локального пространства имен (locals).
    :param env_globals: Словарь глобального пространства имен (globals).
    :return: True/False.
    """
    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    dlg = None
    try:
        dlg = icViewDebugMessageDlg(parent=parent)
        dlg.init(env_locals=env_locals, env_globals=env_globals)
        dlg.setWarningMessage(message_text=message_text)
        dlg.ShowModal()
        dlg.Destroy()
        return True
    except:
        log.fatal(u'Ошибка вывода сообщения ПРЕДУПРЕЖДЕНИЯ в диалоговом окне')
        if dlg:
            dlg.Destroy()
    return False


def view_debug_info_dlg(parent=None, message_text=u'',
                        env_locals=None, env_globals=None):
    """
    Показать ИНФОРМАЦИОННОГО сообшения в диалоге для отладки.
    :param parent: Родительское окно.
        Если не определено, то берется главное окно программы.
    :param message_text: Текст сообщения.
    :param env_locals: Словарь локального пространства имен (locals).
    :param env_globals: Словарь глобального пространства имен (globals).
    :return: True/False.
    """
    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    dlg = None
    try:
        dlg = icViewDebugMessageDlg(parent=parent)
        dlg.init(env_locals=env_locals, env_globals=env_globals)
        dlg.setInfoMessage(message_text=message_text)
        dlg.ShowModal()
        dlg.Destroy()
        return True
    except:
        log.fatal(u'Ошибка вывода ИНФОРМАЦИОННОГО сообщения в диалоговом окне')
        if dlg:
            dlg.Destroy()
    return False


def view_debug_exception_dlg(parent=None, exception_msg_fmt=None,
                             env_locals=None, env_globals=None):
    """
    Показать сообшение об КРИТИЧЕСКОЙ ОШИБКЕ (EXCEPTION) в диалоге для отладки.
    :param parent: Родительское окно.
        Если не определено, то берется главное окно программы.
    :param exception_msg_fmt: Формат для дополнения сообщения критической ошибки.
    :param env_locals: Словарь локального пространства имен (locals).
    :param env_globals: Словарь глобального пространства имен (globals).
    :return: True/False.
    """
    exception_text = traceback.format_exc()

    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    dlg = None
    try:
        dlg = icViewDebugMessageDlg(parent=parent)
        dlg.init(env_locals=env_locals, env_globals=env_globals)
        message_text = exception_msg_fmt % exception_text if exception_msg_fmt else exception_text
        dlg.setErrorMessage(message_text=message_text)
        dlg.ShowModal()
        dlg.Destroy()
        return True
    except:
        log.fatal(u'Ошибка вывода сообщения об КРИТИЧЕСКОЙ ОШИБКЕ (EXCEPTION) в диалоговом окне')
        if dlg:
            dlg.Destroy()
    return False
