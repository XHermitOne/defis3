#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль описания класса главного окна системы

@var DEFAULT_WIN_RES_FILE: Имя файла ресурса окна по умолчанию.
@var CUR_WIN_RES_FILE_NAME: Имя текущего открытого файла ресурсов окна.
@var CUR_WIN_RES_FILE: Образ ресурсного файла в памяти.
@var IC_WIN_WIDTH_MIN: Минимальная допустимая ширина окна.
@var IC_WIN_HEIGHT_MIN: Минимальная допустимая высота окна.

@type SPC_IC_WIN: C{dictionary}
@var SPC_IC_WIN: Спецификация на ресурсное описание компонента icMainWindow.
Описание ключей SPC_IC_WIN:
    - B{name = 'name'}: Имя.
    - B{name = 'description'}: Описание.
    - B{name = 'pos'}: Позиция.
    - B{name = 'size'}: Размер.
    - B{name = 'title_label'}: Заголовок.
    - B{name = 'title_readonly'}: Признак не изменяемого заголовка.
    - B{name = 'title_exp'}: Функция определения заголовка.
    - B{name = 'icon'}: Иконка.
    - B{name = 'phone_color'}: Цвет фона.
    - B{name = 'area_split'}: Разделение главного окна на зоны.
    - B{name = 'border'}: Вид бордюра.
    - B{name = 'sys_menu'}: Наличие типового меню.
    - B{name = 'min_button'}: Наличие кнопки сворачивания окна.
    - B{name = 'max_button'}: Наличие кнопки распахивания окна.
    - B{name = 'paint_func'}: Скрипт,  выполнямый при отрисовке окна.
    - B{name = 'splash'}: Всплывающая картинка-заставка.
    - B{name = 'on_org_open'}: Скрипт, выполнямый при открытии главного органайзера.
    - B{name = 'on_org_close'}: Скрипт, выполнямый при закрытии главного органайзера.
    - B{name = 'on_close'}: Скрипт, выполнямый при открытии главного окна.
"""

# --- Подключение библиотек ---
import os.path
import wx
from wx.lib.splitter import MultiSplitterWindow

import ic.imglib.common as common
import ic.utils.ic_res
import ic.utils.resource
import ic.utils.ic_file

import ic.bitmap.ic_color as ic_color
import ic.utils.ic_exec
from ic.utils import ic_mode
from ic.kernel import io_prnt
import ic.utils.ic_util
from . import ic_note
from ic.dlg import ic_splsh

from ic.kernel import icobject

# --- Основные константы ---
DEFAULT_WIN_RES_FILE = 'MENU/ic_win.win'

# Образ ресурсного файла в памяти
CUR_WIN_RES_FILE_NAME = ''
CUR_WIN_RES_FILE = None

IC_WIN_WIDTH_MIN = 100
IC_WIN_HEIGHT_MIN = 100

IC_WIN_NO_BORDER = 0        # Нет рамки
IC_WIN_SIMPLE_BORDER = 1    # Простая рамка
IC_WIN_DOUBLE_BORDER = 2    # Двойная рамка
IC_WIN_SUNKEN_BORDER = 3    # Вдавленная рамка
IC_WIN_RAISED_BORDER = 4    # Выпуклая рамка

# --- Описание ключей ---
RES_WIN_NAME = 'name'
RES_WIN_DESCRIPTION = 'description'

RES_WIN_POS = 'pos'     # <координата левого верхнего угла, кортеж>
RES_WIN_SIZE = 'size'   # <размер, кортеж>

RES_WIN_TITLE = 'title_label'   # <заголовок окна по умолчанию, строка>
RES_WIN_TITLEREADONLY = 'title_readonly'  # <флаг заголовка (статический или динамический), флаг>
RES_WIN_TITLEFUNC = 'title_exp'     # <выражение для формирования заголовка окна, словарь функции>
RES_WIN_TITLECOLOR = 'title_color'  # <цвет заголовка, кортеж (r.g.b)>

RES_WIN_ICON = 'icon'   # <файл иконки окна (*.ico), строка >

RES_WIN_PHONECOLOR = 'phone_color'  # <цвет фона окна, кортеж (r.g.b)>

RES_WIN_AREASPLIT = 'area_split'    # <Разделение главного окна на зоны, флаг>

RES_WIN_BORDER = 'border'   # <тип рамки, целое - код бордюра>

RES_WIN_SYSMENU = 'sys_menu'    # <признак наличия типового меню и кнопки закрытия, флаг>
RES_WIN_MIN = 'min_button'      # <признак кнопки свертки, флаг >
RES_WIN_MAX = 'max_button'      # <признак кнопки распахивания, флаг >
RES_WIN_PAINT = 'paint_func'    # <Функция отрисовки окна, словарь функции>
RES_WIN_SPLASH = 'splash'       # Приглашение к работе
RES_WIN_ORG_OPEN = 'on_org_open'    # Открытие органайзера
RES_WIN_ORG_CLOSE = 'on_org_close'  # Закрытие органайзера

RES_WIN_CLOSE = 'on_close'  # Закрытие окна
RES_WIN_OPEN = 'on_open'    # Открытие окна

# Спецификации:
SPC_IC_WIN = dict({RES_WIN_NAME: 'new_win',
                   RES_WIN_DESCRIPTION: '',
                   RES_WIN_POS: (-1, -1),
                   RES_WIN_SIZE: (-1, -1),
                   RES_WIN_TITLE: '',
                   RES_WIN_TITLEREADONLY: 1,
                   RES_WIN_TITLEFUNC: None,
                   RES_WIN_ICON: '',
                   RES_WIN_PHONECOLOR: None,
                   RES_WIN_BORDER: IC_WIN_SIMPLE_BORDER,
                   RES_WIN_AREASPLIT: False,
                   RES_WIN_SYSMENU: 1,
                   RES_WIN_MIN: 1,
                   RES_WIN_MAX: 1,
                   RES_WIN_PAINT: None,
                   RES_WIN_SPLASH: None,
                   RES_WIN_ORG_OPEN: None,
                   RES_WIN_ORG_CLOSE: None,
                   RES_WIN_CLOSE: None,     # Закрытие окна
                   RES_WIN_OPEN: None,      # Открытие окна
                   'alias': None,
                   'activate': 1,
                   'style': 0,
                   'init_expr': None,
                   'component_module': None,
                   'res_module': None,
                   'obj_module': None,
                   'is_menubar': True,        # Присутствует в главном окне меню?
                   'is_statusbar': True,      # Присутствует в главном окне статусная строка?
                   'content': None,           # Заполнить фрейм главного окна объектом ...
                   })


def CreateICWin(Name_, ResFile_=DEFAULT_WIN_RES_FILE, ParentWin_=None, Runner_=None):
    """
    Функция создает из ресурса окно по его имени.
    @param Name_: Имя-идентификатор окна прописанный в файле ресурса.
    @param ResFile_: Имя ресурсного файла.
    @param ParentWin_: Родительское окно (если нет, то None).
    @param Runner_: Родительский ДВИЖОК (если нет, то None).
    @return: Возвращает объект окна или None в случае ошибки.
    """
    try:
        win = None
        win_struct = LoadWinStruct(Name_, ResFile_)
        if win_struct == {}:
            io_prnt.outLog(u'Нет данных о таком окне!')
            return None
        win = icMainWindow(Name_, win_struct, ResFile_, ParentWin_, Runner_)
        return win
    except:
        if win is not None:
            MsgLastError(win, u'Ошибка создания окна!')
        io_prnt.outErr(u'Ошибка создания главного окна!')
        return win


def createMainWin(Name_, ResFile_=DEFAULT_WIN_RES_FILE, ParentWin_=None, Runner_=None):
    """
    Функция создает из ресурса окно по его имени.
    @param Name_: Имя-идентификатор окна прописанный в файле ресурса.
    @param ResFile_: Имя ресурсного файла.
    @param ParentWin_: Родительское окно (если нет, то None).
    @param Runner_: Родительский ДВИЖОК (если нет, то None).
    @return: Возвращает объект окна или None в случае ошибки.
    """
    try:
        from ic.components.user import ic_mainwin_wrp
        win = None
        win_struct = LoadWinStruct(Name_, ResFile_)
        if win_struct == {}:
            io_prnt.outLog(u'Нет данных о таком окне!')
            return None
        win = ic_mainwin_wrp.icMainWindow(None, component=win_struct)
        return win
    except:
        if win is not None:
            MsgLastError(win, u'Ошибка создания окна!')
        io_prnt.outErr(u'Ошибка создания главного окна!')
        return win


def OpenWinResFile(ResFileName_):
    """
    Загрузить информацию из файла ресурсов в память.
    @param ResFileName_: Имя ресурсного файла.
    @return: Возвращает словарь, который определен в файле.
    """
    CUR_WIN_RES_FILE_NAME = ResFileName_
    CUR_WIN_RES_FILE = ic.utils.ic_res.ReadAndEvalFile(ResFileName_)
    return CUR_WIN_RES_FILE


def CloseWinResFile():
    """
    Выгрузить информацию о файле ресурсов из памяти.
    """
    CUR_WIN_RES_FILE = None
    CUR_WIN_RES_FILE_NAME = ''


def LoadWinStruct(Name_, ResFile_=DEFAULT_WIN_RES_FILE):
    """
    Загрузить атрибуты компонента из файла ресурсов.
    @param Name_: Имя-идентификатор окна.
    @param ResFile_: Имя ресурсного файла.
    @return: Возвращает словарь, описывающий окно
        (см описание формата ресурсного файла окна).
    """
    return ic.utils.resource.icGetRes(Name_,
                                      ic.utils.ic_file.SplitExt(ResFile_)[1][1:],
                                      nameRes=ic.utils.ic_file.SplitExt(ResFile_)[0])

# --- Классы ---
# Индексы полей статусной строки
sbfLabel, sbfProcent, sbfProgress = range(3)


class icStatusBar(wx.StatusBar):
    """
    Статусная строка главного окна.
    """

    def __init__(self, ParentMainWin_):
        """
        Конструктор.
        @param ParentMainWin_: Родительское главное окно.
        """
        wx.StatusBar.__init__(self, ParentMainWin_, wx.NewId(),
                              style=wx.ST_SIZEGRIP | wx.FULL_REPAINT_ON_RESIZE)

        # Установить количество и ширины полей
        self.SetFieldsCount(3)
        self.SetStatusWidths([500, 30, -1])
    
        # Прогресс бар статусной строки
        self.progress_bar = None
        self._progress_range = (0, 0)
        self._progress_count = 0
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
       
    def OnSize(self, event):
        """
        Изменение размеров статусной строки.
        """
        width = event.GetSize()[0]
        self.SetStatusWidths([width/2, width/25, -1])
        event.Skip()
        
    def openProgressBar(self, Label_='', Min_=0, Max_=100):
        """
        Открыть прогресс бар статусной строки.
        @param Label_: Надпись статусной строки.
        @param Min_: Минимальное значение.
        @param Max_: Максимальное занчение.
        """
        self.SetStatusText(Label_, sbfLabel)
        if not self.progress_bar:
            self._progress_range = (Min_, Max_)
            self.SetStatusText('0%%', sbfProcent)
            self.progress_bar = wx.Gauge(self, -1,
                                         self._progress_range[1]-self._progress_range[0])
            rect = self.GetFieldRect(sbfProgress)
            self.progress_bar.SetDimensions(rect.x+1, rect.y+1, rect.width-2, rect.height-2)
        
    def closeProgressBar(self, Label_=''):
        """
        Закрыть прогресс бар.
        @param Label_: Надпись статусной строки.
        """
        self.SetStatusText(Label_, sbfLabel)
        self.SetStatusText('', sbfProcent)
        if self.progress_bar:
            self.progress_bar.SetValue(0)
            self.progress_bar.Destroy()
        self.progress_bar = None
        self._progress_range = (0, 0)
        self._progress_count = 0
        
    def updateProgressBar(self, Label_='', Value_=-1):
        """
        Обновить прогресс бар.
        @param Label_: Надпись статусной строки.
        @param Value_: Значение.
        """
        if Value_ == -1:
            # Высчитать очередное значение и запомнить его
            self._progress_count = max(self._progress_range[0],
                                       min(self._progress_range[1],
                                       self._progress_count+1))
            Value_ = self._progress_count
            
        self.SetStatusText(Label_, sbfLabel)
        if self._progress_range[1] > self._progress_range[0]:
            procent = ((Value_-self._progress_range[0])*100)/(self._progress_range[1]-self._progress_range[0])
        else:
            procent = 1
        self.SetStatusText('%d%%'%(procent), sbfProcent)
        if self.progress_bar:
            self.progress_bar.SetValue(Value_-self._progress_range[0])
            
    def getPregressBarCount(self):
        return self._progress_count


class icMainWindow(wx.Frame):
    """
    Класс окна системы.
    """

    def __init__(self, Name_, WinStruct_, ResFile_='', Parent_=None, Runner_=None):
        """
        Конструктор.
        @param Name_: Имя окна.
        @param WinStruct_: Словарь, описывающий окно.
        @param ResFile_: Имя ресурсного файла.
        @param Parent_: Родительское окно.
        @param Runner_: Родительский ДВИЖОК.
        """
        # --- Свойства класса ---
        # Иденитификатор числовой
        self._ID = 0
        # Имя
        self._Name = ''
        # Имя ресурсного файла
        self._ResFile = ''
        # Флаг разрешения/запрещения изменения заголовка окна
        self._TitleReadOnly = 1
        # Выражение для формирования заголовка окна
        self._TitleFunc = {}
        # Объект главного менеджера системных панелей
        self._MainNotebook = None
        # Функция вызываемая каждй раз при отрисовке главного окна.
        self._PaintFunc = None
        # Движок
        self._RunnerApp = Runner_
        # Открытие органайзера
        self._OnOrgOpen = None
        # Закрытие органайзера
        self._OnOrgClose = None

        # Закрытие окна
        self._OnClose = None
        # Открытие окна
        self._OnOpen = None
        # Уже открывалось окно?
        # Необходимо обработчик вызвать только один раз
        self._is_opened = False

        # --- Инициализация ---
        # Расширение структуры до спецификации
        WinStruct_ = ic.utils.ic_util.SpcDefStruct(SPC_IC_WIN, WinStruct_)

        # Содержит линейку меню? По умолчанию - да
        self.is_menubar = WinStruct_.get('is_menubar', True)

        # Содержит статусную строку? По умолчанию - да
        self.is_statusbar = WinStruct_.get('is_statusbar', True)

        self._ID = wx.NewId()
        self._Name = Name_
        if ResFile_ != '':
            self._ResFile = ResFile_

        left, top = 0, 0
        if RES_WIN_POS in WinStruct_ and WinStruct_[RES_WIN_POS] is not None:
            left = WinStruct_[RES_WIN_POS][0]
            top = WinStruct_[RES_WIN_POS][1]
        width, height = IC_WIN_WIDTH_MIN, IC_WIN_HEIGHT_MIN
        if RES_WIN_SIZE in WinStruct_ and WinStruct_[RES_WIN_SIZE] is not None:
            width = WinStruct_[RES_WIN_SIZE][0]
            height = WinStruct_[RES_WIN_SIZE][1]

        win_title = ''
        if RES_WIN_TITLEFUNC in WinStruct_ and \
           not ic.utils.ic_exec.IsEmptyMethod(WinStruct_[RES_WIN_TITLEFUNC]):
            win_title = ic.utils.ic_exec.ExecuteMethod(WinStruct_[RES_WIN_TITLEFUNC])
        else:
            if RES_WIN_TITLE in WinStruct_ and WinStruct_[RES_WIN_TITLE] is not None:
                win_title = WinStruct_[RES_WIN_TITLE]

        # Вызов конструктора предка
        wx.Frame.__init__(self, id=self._ID, name=self._Name, parent=Parent_,
                          pos=wx.Point(left, top), size=wx.Size(width, height), title=win_title,
                          style=wx.DEFAULT_FRAME_STYLE)

        # Вывести на экран окно приглашения к работе
        self._splash = None
        if RES_WIN_SPLASH in WinStruct_ and WinStruct_[RES_WIN_SPLASH]:
            self._splash = WinStruct_[RES_WIN_SPLASH]
                
        # --- Статусная строка ---
        if self.is_statusbar:
            self.status_bar = icStatusBar(self)
            self.SetStatusBar(self.status_bar)
            # Контекстное меню
            # Появляется только на статусной строке
            self.status_bar.Bind(wx.EVT_RIGHT_DOWN, self.onStatusBarRightMouseClick)
            self.status_bar.Bind(wx.EVT_LEFT_DCLICK, self.onStatusBarMouseDblClick)

        # Условия распахивания окна
        if width <= 0 and height <= 0:
            self.Maximize(True)     # Распахнуть окно

        # Установка дополнительных атрибутов окна
        # ...
        # Цвет фона окна
        if RES_WIN_PHONECOLOR in WinStruct_ and WinStruct_[RES_WIN_PHONECOLOR] is not None:
            phone_color = wx.Colour(WinStruct_[RES_WIN_PHONECOLOR][ic_color.I_RED],
                                    WinStruct_[RES_WIN_PHONECOLOR][ic_color.I_GREEN],
                                    WinStruct_[RES_WIN_PHONECOLOR][ic_color.I_BLUE])
        else:
            phone_color = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        # Установить цвет фона
        self.SetBackgroundColour(phone_color)

        # Установить иконку (если файл существует)
        if RES_WIN_ICON in WinStruct_ and WinStruct_[RES_WIN_ICON]:
            self.setIcon(WinStruct_[RES_WIN_ICON])

        # Установить параметры заголовка
        if RES_WIN_TITLEREADONLY in WinStruct_ and WinStruct_[RES_WIN_TITLEREADONLY] is not None:
            self._TitleReadOnly = WinStruct_[RES_WIN_TITLEREADONLY]
        if RES_WIN_TITLEFUNC in WinStruct_ and WinStruct_[RES_WIN_TITLEFUNC] is not None:
            self._TitleFunc = WinStruct_[RES_WIN_TITLEFUNC]
        
        # Установить параметры бордюра
        style = wx.CAPTION | wx.BORDER
        value = IC_WIN_SIMPLE_BORDER
        if RES_WIN_BORDER in WinStruct_ and WinStruct_[RES_WIN_BORDER] is not None:
            value = WinStruct_[RES_WIN_BORDER]
        if value == IC_WIN_NO_BORDER:
            style |= wx.NO_BORDER
        elif value == IC_WIN_SIMPLE_BORDER:
            style |= wx.SIMPLE_BORDER
        elif value == IC_WIN_DOUBLE_BORDER:
            style |= wx.DOUBLE_BORDER
        elif value == IC_WIN_SUNKEN_BORDER:
            style |= wx.SUNKEN_BORDER
        elif value == IC_WIN_RAISED_BORDER:
            style |= wx.RAISED_BORDER
        elif value == IC_WIN_RAISED_BORDER:
            style |= wx.RAISED_BORDER

        if RES_WIN_SYSMENU in WinStruct_ and WinStruct_[RES_WIN_SYSMENU]:
            style |= wx.SYSTEM_MENU
        if RES_WIN_MIN in WinStruct_ and WinStruct_[RES_WIN_MIN]:
            style |= wx.MINIMIZE_BOX
        if RES_WIN_MAX in WinStruct_ and WinStruct_[RES_WIN_MAX]:
            style |= wx.MAXIMIZE_BOX
  
        # Возможность изменения размеров
        style |= wx.RESIZE_BORDER
       
        # Установить стиль окна
        self.SetWindowStyle(style)

        # --- Области главного окна ---
        self._h_area_splitter = None
        self._v_area_splitter = None
        self.area_split = False
        if RES_WIN_AREASPLIT in WinStruct_:
            self.area_split = bool(WinStruct_[RES_WIN_AREASPLIT])
            
        # Панели главного окна
        self.left_panel = None
        self.right_panel = None
        self.top_panel = None
        self.bottom_panel = None
        self.central_panel = None

        # --- Объект-содержание главного окна ---
        content_psp = WinStruct_.get('content', None)
        if content_psp:
            self.content_obj = ic.getKernel().Create(content_psp, parent=self)
            io_prnt.outLog(u'Наполнение главного окна <%s>' % self.content_obj)
            self.setCentralPanel(self.content_obj)

        # Функция вызываемая каждй раз при отрисовке главного окна.
        if RES_WIN_PAINT in WinStruct_:
            self._PaintFunc = WinStruct_[RES_WIN_PAINT]
        # Обработчик отрисовки фона главного окна
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        # Обработчик закрытия главного окна
        if RES_WIN_CLOSE in WinStruct_:
            self._OnClose = WinStruct_[RES_WIN_CLOSE]

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # Обработчик открытия главного окна
        if RES_WIN_OPEN in WinStruct_:
            self._OnOpen = WinStruct_[RES_WIN_OPEN]

        self.Bind(wx.EVT_SHOW, self.OnOpen)
        # self.Bind(wx.EVT_LEFT_DCLICK, self.OnMouseDblClick)

        # СОбытия органайзера
        if RES_WIN_ORG_OPEN in WinStruct_:
            self._OnOrgOpen = WinStruct_[RES_WIN_ORG_OPEN]
        if RES_WIN_ORG_CLOSE in WinStruct_:
            self._OnOrgClose = WinStruct_[RES_WIN_ORG_CLOSE]

        # Запустить обработку переразмеривания всех дочерних компонентов
        # главного окна для корректного отображения
        self.SendSizeEvent()

    def showSplash(self):
        """
        Вывести на экран окно приглашения к работе.
        """
        # Вывести на экран окно приглашения к работе
        if self._splash:
            ic_splsh.ShowSplash(ic.utils.ic_file.AbsolutePath(self._splash))

    def getIconFilename(self):
        """
        Полное имя файла иконки.
        @return: Полное имя файла иконки.
            None если иконка не определена.
        """
        icon = self.resource.get(RES_WIN_ICON, None) if hasattr(self, 'resource') else None
        if icon and type(icon) in (str, unicode):
            return ic.utils.ic_file.AbsolutePath(icon)
        else:
            io_prnt.outWarning(u'Не определена иконка главного окна')
        return None

    def setIcon(self, Icon_):
        """
        Установить иконку.
        @param Icon_: Или имя файла *.ico или объект wx.Icon.
        """
        if type(Icon_) in (str, unicode):
            ico_file_name = ic.utils.ic_file.AbsolutePath(Icon_)
            # Установить иконку (если файл существует)
            if os.path.exists(ico_file_name):
                try:
                    icon = wx.Icon(ico_file_name, wx.BITMAP_TYPE_ICO)
                except:
                    io_prnt.outErr(u'Ошибка инициализации иконки <%s> главного окна. Файл не ICO формата.' % ico_file_name)
                    return None
            else:
                io_prnt.outWarning(u'Иконка главного окна <%s> не найдена' % ico_file_name)
                return None
        elif isinstance(Icon_, wx.Icon):
            icon = Icon_
        else:
            io_prnt.outWarning(u'Не обрабатываемый тип иконки <%s>' % Icon_)
            return None
        self.SetIcon(icon)
        return icon

    def OnPaint(self, event):
        """
        Обработчик отрисовки фона главного окна.
        """
        try:
            self.RefreshTitle()

            if self._PaintFunc:
                # Если главный органайзер не отображается в данный момент,
                # то выпольнить функцию отрисовки
                if (self._MainNotebook is None) or not self._MainNotebook.IsShown():
                    ic.utils.ic_exec.ExecuteMethod(self._PaintFunc, self)

            # ВНИМАНИЕ!!! НЕОБХОДИМО ОБЯЗАТЕЛЬНО СТАВИТЬ event.Skip()
            #   ИНАЧЕ УЖАСНО ГЛЮЧИТ!!!!
            
            bmp = None
            if bmp:
                dc = wx.PaintDC(self)
                dc.BeginDrawing()
                fx, fy = (2, 1)
                sx, sy = bmp.GetWidth(), bmp.GetHeight()
                cx, cy = self.GetClientSize()
            
                nx = cx/(sx*fx)+1
                ny = cy/(sy*fy)+1
            
                x0 = 10
                y0 = (cy - ny*sy*fy)/2
            
                for i in xrange(ny):
                    if i % 2:
                        d0 = (sx*fx)/2
                        nn = nx - 1
                    else:
                        d0 = 0
                        nn = nx
                    
                    for n in xrange(nn):
                        dc.DrawBitmap(common.imgDefis, x0 + d0 + n*sx*fx, y0 + i*sy*fy, True)
                    
                dc.EndDrawing()
        except:
            io_prnt.outErr(u'Ошибка отрисовки главного окна')

        if event:
            event.Skip()
           
    def OnSize(self, event):
        """
        Изменение размеров.
        """
        self.Refresh()
        event.Skip()

    def OnOpen(self, event):
        """
        Обработчик открытия главного окна.
        """
        # Если в режиме редактирования...
        if not ic_mode.isRuntimeMode():
            event.Skip()
            return

        try:
            ok = True
            if not ic.utils.ic_exec.IsEmptyMethod(self._OnOpen) and \
                not self._is_opened:
                ok = ic.utils.ic_exec.ExecuteMethod(self._OnOpen, self)
                self._is_opened = True
            if ok:  # Обычное открытие окна
                event.Skip()
            else:
                event.Continue = False
        except:
            io_prnt.outErr(u'Ошибка открытия главного окна')
            event.Skip()

    def OnClose(self, event):
        """
        Обработчик закрытия главного окна.
        """
        # Если в режиме редактирования,
        # то при закрытии окно не закрывать приложение
        if not ic_mode.isRuntimeMode():
            event.Skip()
            return
                        
        try:
            ok = True
            if not ic.utils.ic_exec.IsEmptyMethod(self._OnClose):
                ok = ic.utils.ic_exec.ExecuteMethod(self._OnClose, self)
            if ok:  # Обычное закрытие окна
                if self._MainNotebook:
                    self.DelOrg()
                self._destroyAreaSplitter()

                # Остановить основной цикл выполнения приложения
                if self._RunnerApp:
                    if issubclass(self._RunnerApp.__class__, wx.App):
                        self._RunnerApp.ExitMainLoop()
                event.Skip()
            else:
                event.Continue = False
        except:
            io_prnt.outErr(u'Ошибка закрытия главного окна')
            event.Skip()

    def onStatusBarMouseDblClick(self, event):
        """
        Обработчик двойного щелчка на статусной строке.
        По умолчанию открываем окно <О программе...>
        """
        from ic.dlg import about_box
        about_box.showAbout(parent=self)
        event.Skip()

    def onStatusBarRightMouseClick(self, event):
        """
        Обработчик вызова контекстного меню кликом
            правой мышки на главном окне.
        """
        popup_menu = wx.Menu()
        menuitem_id = wx.NewId()
        popup_menu.Append(menuitem_id, u'Запуск внешней программы')
        popup_menu.Bind(wx.EVT_MENU, self.onRunExternalProg, id=menuitem_id)
        mouse_pos = wx.GetMousePosition()
        self.PopupMenu(popup_menu, mouse_pos)
        event.Skip()

    def onRunExternalProg(self, event):
        """
        Запуск внешней программы из контекстного меню.
        """
        from . import ext_prg
        ext_prg.run_external_programm()
        event.Skip()

    def SetICTitle(self, Title_=''):
        """
        Установить заголовок.
        """
        if Title_ != '':
            if self._TitleReadOnly == 0:
                self.SetTitle(Title_)
        else:
            if self._TitleReadOnly == 0 and self._TitleFunc != {}:
                new_title = ic.utils.ic_exec.ExecuteMethod(self._TitleFunc, self)
                if new_title != '' and new_title is not None:
                    self.SetTitle(new_title)

    def SetTitleFunc(self, TitleFunc_):
        """
        Установить метод заполнения заголовка.
        @param TitleFunc_: Словарь функции метода заполнения заголовка.
        """
        self._TitleFunc = TitleFunc_

    def RefreshTitle(self):
        """
        Обновить заголовок.
        """
        try:
            if not ic.utils.ic_exec.IsEmptyMethod(self._TitleFunc):
                win_title = ic.utils.ic_exec.ExecuteMethod(self._TitleFunc)
                self.SetTitle(win_title)
                self.Refresh()
        except:
            io_prnt.outErr(u'Ошибка выполнения функции обновления заголовка главного окна.')

    def SetTitleReadOnly(self, TitleReadOnly_):
        """
        Установить Флаг разрешения/запрещения изменения заголовка окна.
        """
        self._TitleReadOnly = TitleReadOnly_

    def GetMainNotebook(self):
        """
        Определить главный органайзер.
        """
        return self._MainNotebook

    def OpenWin(self):
        """
        Открыть окно.
        """
        self.SetICTitle()
        self.Show(True)

    def CloseWin(self):
        """
        Закрыть окно.
        """
        self.Show(False)

    # --- Методы управления панелями главного окна ---
    def AddOrgPage(self, Page_, Title_, OpenExists_=False, Image_=None,
                   CanClose_=True, OpenScript_=None, CloseScript_=None, DefaultPage_=-1):
        """
        Добавить страницу.
        @param Page_: Страница-объект наследник wx.Window.
        @param Title_: Заголовок страницы.
        @param OpenExists_: Если страница уже создана-открыть ее.
        @param Image_: Файл образа или сам образ в заголовке страницы.
        @param CanClose_: Признак разрешения закрытия страницы при помощи
            стандартного всплывающего меню.
        @param OpenScript_: Блок кода открытия страницы при переключенни
            м/у страницами.
        @param CloseScript_: Блок кода закрытия страницы при переключенни
            м/у страницами.
        @param DefaultPage_: Индекс страницы,  открываемой по умолчанию.
            Если -1, то открывается текущая добавляемая страница.
        """
        if self.content_obj is not None:
            io_prnt.outWarning(u'Notebook главного окна заменен объектом-содержанием <%s>' % self.content_obj)
            return None
        try:
            # --- Объект главного менеджера системных панелей ---
            if self._MainNotebook is None:
                if self.area_split:
                    if self._h_area_splitter is None:
                        self._createAreaSplitter()
                    self._MainNotebook = ic_note.icMainNotebook(self._h_area_splitter)
                    self.setCentralPanel(self._MainNotebook)
                else:
                    self._MainNotebook = ic_note.icMainNotebook(self)
            # Добавить страницу
            return self._MainNotebook.addPage(Page_, Title_, OpenExists_,
                                              Image_, CanClose_, OpenScript_,
                                              CloseScript_, DefaultPage_)
        except:
            io_prnt.outErr(u'Ошибка добавления страницы в главное окно.')
            return None

    # Можно использовать и другое наименование метода
    AddPage = AddOrgPage

    def DelOrgPage(self, Index_):
        """
        Удалить страницу.
        @param Index_: Индекс страницы.
        """
        if self.content_obj is not None:
            io_prnt.outWarning(u'Notebook главного окна заменен объектом-содержанием <%s>' % self.content_obj)
            return None
        try:
            # --- Объект главного менеджера системных панелей ---
            if self._MainNotebook is None:
                return
            self._MainNotebook.deletePage(Index_)
            # Если страниц в органайзере больше нет, тогда удалить его из окна
            if self._MainNotebook.GetPageCount() == 0:
                self.DelOrg()
            return self._MainNotebook
        except:
            io_prnt.outErr(u'Ошибка удаления страницы из органайзера.')
            return None

    def DelOrg(self):
        """
        Удалить органайзер(Объект главного менеджера системных панелей).
        @return: Возвращает результат выполнения операции True/False.
        """
        if self.content_obj is not None:
            io_prnt.outWarning(u'Notebook главного окна заменен объектом-содержанием <%s>' % self.content_obj)
            return None
        try:
            if self.area_split:
                self.delCentralPanel()
            self._MainNotebook.deleteAllPages()
            self._MainNotebook.Close()
            self.RemoveChild(self._MainNotebook)
            self._MainNotebook.Destroy()
            self._MainNotebook = None
            self.Refresh()
            return True
        except:
            io_prnt.outErr(u'Ошибка удаления главного органайзера')
            return False

    def CloseOrgPages(self):
        """
        Закрыть все страницы органайзера(Объект главного менеджера системных панелей).
        @return: Возвращает результат выполнения операции True/False.
        """
        if self.content_obj is not None:
            io_prnt.outWarning(u'Notebook главного окна заменен объектом-содержанием <%s>' % self.content_obj)
            return None
        try:
            if self.area_split:
                self.delCentralPanel()
            self._MainNotebook.deleteAllPages()
            self.Refresh()
            return True
        except:
            io_prnt.outErr(u'Ошибка закрытия окон главного органайзера')
            return False

    def _createAreaSplitter(self):
        """
        Создать разделитель областей.
        @return: Объект главного вертикального разделителя или 
            None в случае ошибки.
        """
        try:
            if self.area_split:
                # Вертикальный сплиттер
                self._v_area_splitter = MultiSplitterWindow(self, style=wx.SP_LIVE_UPDATE)
                self._v_area_splitter.SetOrientation(wx.VERTICAL)
                # Горизонтальный сплиттер
                self._h_area_splitter = MultiSplitterWindow(self._v_area_splitter, style=wx.SP_LIVE_UPDATE)
                self._h_area_splitter.SetOrientation(wx.HORIZONTAL)
                self._insPanel(self._v_area_splitter, 1, self._h_area_splitter)

                # ВНИМАНИЕ!!!
                # Установить принудительно размер главного сплиттера,
                # а то объект не перерисовывается!!!
                self._v_area_splitter.SetSize(self.GetClientSize())
                
            return self._v_area_splitter
        except:
            io_prnt.outErr(u'Ошибка создания разделителя областей.')
            return None
        
    def _destroyAreaSplitter(self):
        """
        Удаление разделителя областей.
        """
        try:
            if self.area_split:
                if self._h_area_splitter:
                    h_win_count = len(self._h_area_splitter._windows)
                    for i in range(h_win_count):
                        self._delPanel(self._h_area_splitter, i)
                if self._v_area_splitter:
                    v_win_count = len(self._v_area_splitter._windows)
                    for i in range(v_win_count):
                        self._delPanel(self._v_area_splitter, i)
                    self._v_area_splitter.Destroy()
                    self.left_panel = None
                    self.right_panel = None
                    self.top_panel = None
                    self.bottom_panel = None
                    self.central_panel = None
            return True
        except:
            io_prnt.outErr(u'Ошибка удаления разделителя областей.')
            return False
        
    def _insPanel(self, Splitter_, Index_, Panel_):
        """
        Установить панель.
        @param Splitter_: Сплиттер, в который будет устанавливаться панель.
        @param Index_: Индекс в сплиттере.
        @param Panel_: Объект панели. Наследник от wx.Window.
        @return: Возвращает True/False.
        """
        try:
            if Splitter_ is None:
                return False
            
            win_count = len(Splitter_._windows)
            win = None
            if Index_ < win_count:
                win = Splitter_.GetWindow(Index_)
                
            if win:
                Splitter_.ReplaceWindow(win, Panel_)
            else:
                if Index_ >= win_count:
                    for i in range(win_count, Index_):
                        Splitter_.AppendWindow(wx.Panel(Splitter_, -1), 0)
                    Splitter_.AppendWindow(Panel_)
                else:
                    Splitter_.InsertWindow(Index_, Panel_, sashPos=-1)
                    
            return True
        except:
            io_prnt.outErr(u'Ошибка установки панели в разделитель областей.')
            return False

    def _delPanel(self, Splitter_, Index_):
        """
        Удалить из области панель с указанным индексом.
        @param Splitter_: Сплиттер, в который устанавленна панель.
        @param Index_: Индекс в сплиттере.
        @return: Возвращает True/False.
        """
        try:
            if Splitter_ is None:
                return False
                
            win_count = len(Splitter_._windows)
            win = None
            if Index_ < win_count:
                win = Splitter_.GetWindow(Index_)
                
            if win:
                Splitter_.DetachWindow(win)
                win.Destroy()
            return True
        except:
            io_prnt.outErr(u'Ошибка удаления панели из разделителя областей.')
            return False

    def getLeftPanel(self):
        """
        Левая панель.
        """
        if self.area_split:
            return self.left_panel
        return None

    def setLeftPanel(self, Panel_):
        """
        Установить левую панель.
        """
        if self._v_area_splitter is None or self._h_area_splitter is None:
            self._createAreaSplitter()

        self.left_panel = Panel_
        return self._insPanel(self._h_area_splitter, 0, self.left_panel)
        
    def delLeftPanel(self):
        """
        Удалить левую панель.
        """
        if self._v_area_splitter is None or self._h_area_splitter is None:
            self._createAreaSplitter()

        self.left_panel = None
        return self._delPanel(self._h_area_splitter, 0)
        
    def getRightPanel(self):
        """
        Правая панель.
        """
        if self.area_split:
            return self.right_panel
        return None
        
    def setRightPanel(self, Panel_):
        """
        Установить правую панель.
        """
        if self._v_area_splitter is None or self._h_area_splitter is None:
            self._createAreaSplitter()

        self.right_panel = Panel_
        return self._insPanel(self._h_area_splitter, 2, self.right_panel)
        
    def delRightPanel(self):
        """
        Удалить правую панель.
        """
        if self._v_area_splitter is None or self._h_area_splitter is None:
            self._createAreaSplitter()

        self.right_panel = None
        return self._delPanel(self._h_area_splitter, 2)
        
    def getTopPanel(self):
        """
        Верхняя панель.
        """
        if self.area_split:
            return self.top_panel
        return None
        
    def setTopPanel(self, Panel_):
        """
        Установить верхнюю панель.
        """
        if self._v_area_splitter is None or self._h_area_splitter is None:
            self._createAreaSplitter()

        self.top_panel = Panel_
        return self._insPanel(self._v_area_splitter, 0, self.top_panel)
        
    def delTopPanel(self):
        """
        Удалить верхнюю панель.
        """
        if self._v_area_splitter is None or self._h_area_splitter is None:
            self._createAreaSplitter()

        self.top_panel = None
        return self._delPanel(self._v_area_splitter, 0)
        
    def getBottomPanel(self):
        """
        Нижняя панель.
        """
        if self.area_split:
            return self.bottom_panel
        return None

    def setBottomPanel(self, Panel_):
        """
        Установить нижнюю панель.
        """
        if self._v_area_splitter is None or self._h_area_splitter is None:
            self._createAreaSplitter()

        self.bottom_panel = Panel_
        return self._insPanel(self._v_area_splitter, 2, self.bottom_panel)
        
    def delBottomPanel(self):
        """
        Удалить нижнюю панель.
        """
        if self._v_area_splitter is None or self._h_area_splitter is None:
            self._createAreaSplitter()

        self.bottom_panel = None
        return self._delPanel(self._v_area_splitter, 2)
        
    def getCentralPanel(self):
        """
        Центральная панель.
        """
        if self.area_split:
            return self.central_panel
        return None

    def setCentralPanel(self, Panel_):
        """
        Установить центральную панель.
        """
        if self._v_area_splitter is None or self._h_area_splitter is None:
            self._createAreaSplitter()

        self.central_panel = Panel_
        return self._insPanel(self._h_area_splitter, 1, self.central_panel)
        
    def delCentralPanel(self):
        """
        Удалить центральную панель.
        """
        if self._v_area_splitter is None or self._h_area_splitter is None:
            self._createAreaSplitter()

        self.central_panel = None
        return self._delPanel(self._h_area_splitter, 1)

    def setMenuBar(self, MenuBar_):
        """
        Установить горизонтальное меню.
        """
        try:
            self.SetMenuBar(MenuBar_)
            MenuBar_.Refresh()
        except:
            io_prnt.outErr(u'Ошибка установки горизонтального меню <%s> в главное окно.' % MenuBar_)
