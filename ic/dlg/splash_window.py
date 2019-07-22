#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль описания класса всплывающего окошка системы.
"""

# Подключение библиотек
import wx
import wx.adv
import os

from ic.bitmap import ic_bmp
from ic.bitmap import ic_color
from ic.log import log

__version__ = (0, 1, 2, 1)

# Задержка всплывающего окошка
SPLASH_DELAY = 2000

# Максимальный размер шрифта
MAX_FONT_SIZE = 72
# Используемый шрифт по умолчанию
DEFAULT_TEXT_FONT = 'Courier New'


def setStampedText(parent, prompt_text, font_name=DEFAULT_TEXT_FONT):
    """
    Функция выводит на фоне окна тесненный текст.
    @param parent: Окно.
    @param prompt_text: Строка текста.
    @param font_name: Шрифт.
    """
    try:
        if parent is None:
            return
        if not prompt_text:
            return
        # Определить шрифт для фонового текста
        try:
            text_font = wx.Font(MAX_FONT_SIZE, wx.FONTFAMILY_DEFAULT,
                                wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, font_name)
        except:
            txt_font_name = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT).GetFaceName()
            text_font = wx.Font(MAX_FONT_SIZE, wx.FONTFAMILY_DEFAULT,
                                wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, txt_font_name)

        # Определение цвета фона
        win_canvas = wx.ClientDC(parent)
        backgrnd_color = win_canvas.GetBackground().GetColour()
        # Центровка надписи
        canvas = wx.MemoryDC()
        canvas.SetFont(text_font)
        text_width, text_height = canvas.GetTextExtent(prompt_text)
        bmp = wx.Bitmap(text_width+2, text_height+2)
        canvas.SelectObject(bmp)
       
        # Непосредственно сама отрисовка
        # canvas.BeginDrawing()
        canvas.SetBackground(wx.Brush(backgrnd_color, wx.BRUSHSTYLE_SOLID))
        canvas.Clear()
        canvas.SetTextForeground(ic_color.IC_COLOR_BLACK)
        canvas.DrawText(prompt_text, 0, 0)
        canvas.SetTextForeground(ic_color.IC_COLOR_LIGHTGREY)
        canvas.DrawText(prompt_text, 2, 2)
        canvas.SetTextForeground(backgrnd_color)
        canvas.DrawText(prompt_text, 1, 1)
        # canvas.EndDrawing()

        # Копирование контекста устройства
        client_width, client_height = parent.GetClientSize()
        text_x = (client_width-text_width) / 2
        text_y = (client_height-text_height) / 2
        # win_canvas.BeginDrawing()
        win_canvas.Clear()
        win_canvas.Blit(text_x, text_y, text_width+2, text_height+2, canvas, 0, 0)
        # win_canvas.EndDrawing()
    except:
        log.fatal(u'Ошибка заполнения фона окна')


def showSplash(img_filename=''):
    """
    Функция выводит на экран всплывающее окошко системы.
    @param img_filename: Имя графического файла (BMP).
    """
    try:
        if (not img_filename) or (not os.path.exists(img_filename)):
            log.warning(u'Сплеш-окно <%s> не найдено!' % img_filename)
            return None

        wx.InitAllImageHandlers()
        # Создать объект
        splash = icSplashScreen(img_filename)
        # Отобразить его
        splash.Show()
        return splash
    except:
        log.fatal(u'Ошибка вывода сплеш-окна: <%s>' % img_filename)


class icSplashScreen(wx.adv.SplashScreen):
    """
    Класс всплывающего окошка системы.
    """

    def __init__(self, img_filename=''):
        """
        Конструктор.
        @param img_filename: Имя графического файла,
            отображаемого в окне.
        """
        try:
            bmp = ic_bmp.createBitmap(img_filename)
            wx.adv.SplashScreen.__init__(self, bmp,
                                         wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,
                                         SPLASH_DELAY, None, -1, wx.DefaultPosition, wx.DefaultSize,
                                         wx.SIMPLE_BORDER | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP)
        except:
            log.fatal(u'Ошибка создания всплывающего окна')


def showMsgWin(title=''):
    """
    Функция выводи на экран окно для сообщений
    """
    try:
        msg_win = icMsgWin(title)
        msg_win.Show(True)
        return msg_win
    except:
        log.fatal(u'Ошибка отображения окна <%s>' % title)
    return None


def closeMsgWin(msg_window):
    """
    Функция закрывает окно для сообщений системы.
    @param msg_window: Ссылка на объект окно сообщений.
    """
    if msg_window is not None:
        msg_window.Close(False)


def setMsgText(msg_window, msg_text):
    """
    Вывести сообщение в окне.
    @param msg_window: Ссылка на объект окно сообщений.
    @param msg_text: Текст сообщения.
    """
    try:
        if msg_window is not None:
            msg_window.setMsgText(msg_text)
    except:
        log.fatal(u'Ошибка вывода сообщения в окне')


class icMsgWin(wx.Frame):
    """
    Класс окна для сообщений.
    """

    def __init__(self, title):
        """
        Конструктор
        """
        # Вызов конструктора предка
        wx.Frame.__init__(self, id=wx.NewId(), name='MsgWin', parent=None,
                          pos=wx.DefaultPosition, size=wx.Size(500, 70),
                          style=wx.CAPTION | wx.BORDER | wx.SYSTEM_MENU, title=title)
        # Добавить
        self.msg_label = wx.StaticText(self, id=wx.NewId(), label='>',
                                       pos=wx.Point(0, 0), size=wx.Size(400, 20))

    def setMsgText(self, msg_text):
        """
        Вывести сообщение в окне.
        @param msg_text: Текст сообщения.
        """
        self.msg_label.SetLabel(msg_text)


def load_component_proccess(parent=None, frames=None):
    try:
        import ic.components.icResourceParser as prs
        import ic.dlg.ic_logo_dlg as ic_logo_dlg
        ic_logo_dlg.LoadProjectProccess(parent, u'Подождите',
                                        prs.GetComponentModulDict, tuple(), Frames_=frames)
    except:
        log.fatal(u'Ошибка загрузки сплеш-окна')

