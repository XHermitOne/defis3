#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль описания класса всплывающего окошка системы.
"""

# Подключение библиотек
import wx
import os

import ic.bitmap.ic_bmp as ic_bmp
from ic.kernel import io_prnt
import ic.bitmap.ic_color as ic_color

# Задержка всплывающего окошка
SPLASH_DELAY = 2000

# Максимальный размер шрифта
MAX_FONT_SIZE = 72
# Используемый шрифт по умолчанию
DEFAULT_TEXT_FONT = 'Courier New'


def icStampedText(Win_, Text_, FontName_=DEFAULT_TEXT_FONT):
    """
    Функция выводит на фоне окна тесненный текст.
    @param Win_: Окно.
    @param Text_: Строка текста.
    @param FontName_: Шрифт.
    """
    try:
        if Win_ is None:
            return
        if not Text_:
            return
        # Определить шрифт для фонового текста
        try:
            text_font = wx.Font(MAX_FONT_SIZE, wx.DEFAULT,
                                wx.NORMAL, wx.BOLD, False, FontName_)
        except:
            txt_font_name = wx.SystemSettings_GetSystemFont(wx.SYS_DEFAULT_GUI_FONT).GetFaceName()
            text_font = wx.Font(MAX_FONT_SIZE, wx.DEFAULT,
                                wx.NORMAL, wx.BOLD, False, txt_font_name)

        # Определение цвета фона
        win_canvas = wx.ClientDC(Win_)
        backgrnd_color = win_canvas.GetBackground().GetColour()
        # Центровка надписи
        canvas = wx.MemoryDC()
        canvas.SetFont(text_font)
        text_width, text_height = canvas.GetTextExtent(Text_)
        bmp = wx.EmptyBitmap(text_width+2, text_height+2)
        canvas.SelectObject(bmp)
       
        # Непосредственно сама отрисовка
        canvas.BeginDrawing()
        canvas.SetBackground(wx.Brush(backgrnd_color, wx.SOLID))
        canvas.Clear()
        canvas.SetTextForeground(ic_color.IC_COLOR_BLACK)
        canvas.DrawText(Text_, 0, 0)
        canvas.SetTextForeground(ic_color.IC_COLOR_LIGHTGREY)
        canvas.DrawText(Text_, 2, 2)
        canvas.SetTextForeground(backgrnd_color)
        canvas.DrawText(Text_, 1, 1)
        canvas.EndDrawing()

        # Копирование контекста устройства
        client_width, client_height = Win_.GetClientSize()
        text_x = (client_width-text_width) / 2
        text_y = (client_height-text_height) / 2
        win_canvas.BeginDrawing()
        win_canvas.Clear()
        win_canvas.Blit(text_x, text_y, text_width+2, text_height+2, canvas, 0, 0)
        win_canvas.EndDrawing()

    except:
        io_prnt.outErr(u'Ошибка заполнения фона окна.')


def ShowSplash(GraphFile_=''):
    """
    Функция выводит на экран всплывающее окошко системы.
    @param GraphFile_: Имя графического файла (BMP).
    """
    try:
        if (not GraphFile_) or (not os.path.exists(GraphFile_)):
            io_prnt.outWarning(u'Сплеш-окно <%s> не найдено!' % GraphFile_)
            return None

        wx.InitAllImageHandlers()
        # Создать объект
        splash = icSplashScreen(GraphFile_)
        # Отобразить его
        splash.Show()
        return splash
    except:
        io_prnt.outErr(u'Ошибка вывода сплеш-окна: <%s>' % GraphFile_)


class icSplashScreen(wx.SplashScreen):
    """
    Класс всплывающего окошка системы.
    """

    def __init__(self, GraphFile_=''):
        """
        Конструктор.
        @param GraphFile_: Имя графического файла,
            отображаемого в окне.
        """
        try:
            bmp = ic_bmp.createBitmap(GraphFile_)
            wx.SplashScreen.__init__(self, bmp,
                                     wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,
                                     SPLASH_DELAY, None, -1, wx.DefaultPosition, wx.DefaultSize,
                                     wx.SIMPLE_BORDER | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP)
        except:
            io_prnt.outErr(u'Ошибка создания всплывающего окошка.')


def ShowMsgWin(Title_=''):
    """
    Функция выводи на экран окно для сообщений
    """
    try:
        msg_win = icMsgWin(Title_)
        msg_win.Show(True)
        return msg_win
    except:
        return None


def CloseMsgWin(MsgWin_):
    """
    Функция закрывает окно для сообщений системы.
    @param MsgWin_: Ссылка на объект окно сообщений.
    """
    if MsgWin_ is not None:
        MsgWin_.Close(False)


def SetMsgText(MsgWin_, Text_):
    """
    Вывести сообщение в окне.
    @param MsgWin_: Ссылка на объект окно сообщений.
    @param Text_: Текст сообщения.
    """
    try:
        if MsgWin_ is not None:
            MsgWin_.SetMsgText(Text_)
    except:
        raise


class icMsgWin(wx.Frame):
    """
    Класс окна для сообщений.
    """

    def __init__(self, Title_):
        """
        Конструктор
        """
        # Вызов конструктора предка
        wx.Frame.__init__(self, id=wx.NewId(), name='MsgWin', parent=None,
                          pos=wx.DefaultPosition, size=wx.Size(500, 70),
                          style=wx.CAPTION | wx.BORDER | wx.SYSTEM_MENU, title=Title_)
        # Добавить
        self.msg_label = wx.StaticText(self, id=wx.NewId(), label='>',
                                       pos=wx.Point(0, 0), size=wx.Size(400, 20))

    def SetMsgText(self, Text_):
        """
        Вывести сообщение в окне.
        @param Text_: Текст сообщения.
        """
        self.msg_label.SetLabel(Text_)


def load_component_proccess(parent=None, Frames_=None):
    try:
        import ic.components.icResourceParser as prs
        import ic.dlg.ic_logo_dlg as ic_logo_dlg
        ic_logo_dlg.LoadProjectProccess(parent, u'Подождите',
                                        prs.GetComponentModulDict, tuple(), Frames_=Frames_)
    except:
        io_prnt.outErr(u'Ошибка загрузки сплеш-окна')

