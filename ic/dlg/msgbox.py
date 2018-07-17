#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Выводит окно сообщения.
Окно сообщения.
"""

import wx

def MsgBox (parent, mess, title = 'MsgBox', style = wx.OK | wx.ICON_INFORMATION ):
    """
    Окно сообщения.
    @type parent: C{wxWindow}
    @param parent: Родительское окно.
    @type mess: C{String}
    @param mess: Текст сообщения.
    @type title: C{String}
    @param title: Текст заголовка окна.
    @type style: C{long}
    @param style: Стиль окна сообщений. По умолчанию wxOK | wxICON_INFORMATION.

        Стили окна:
        - B{wxOK}: Выводит кнопку <OK>.
        - B{wxCANCEL}: Выводит кнопку  <Cancel>.
        - B{wxYES_NO}: Выводит кнопки <Yes> и <No>.
        - B{wxYES_DEFAULT}: Используется стиль wxYES_NO. Кнопка <Yes> выбрана по умолчанию.
        - B{wxNO_DEFAULT}: Стиль wxYES_NO, кнопка <No> по умолчанию.
        - B{wxCENTRE}: Сообщение центрируется (Не под Windows).
        - B{wxICON_EXCLAMATION}: Рядом с сообщением выводится <!>.
        - B{wxICON_HAND}: Выводися картинка об ошибке.
        - B{wxICON_ERROR}: Аналог wxICON_HAND.
        - B{wxICON_QUESTION}: Рядом с сообщением выводится <?>.
        - B{wxICON_INFORMATION}: Рядом с сообщением выводится <i>.
    """
    
    bCr = 0

    if parent == None:
       parent = wx.Frame(None, -1, '')
       bCr = 1

    ret = 0
    dlg = wx.MessageDialog(parent, mess, title, style)

    try:
        ret = dlg.ShowModal()
    finally:
        dlg.Destroy()

    #   Удаляем созданное родительское окно
    if bCr == 1:
        parent.Destroy()

    return ret

def Ask(parent, question, title=''):
    d = wx.MessageDialog(parent, question, title, wx.YES_NO | wx.ICON_QUESTION)
    answer = d.ShowModal()
    d.Destroy()
    return (answer == wx.ID_YES)

if __name__ == '__main__':
    app = wx.PySimpleApp()
    MsgBox(None, 'Test')
    app.MainLoop()

