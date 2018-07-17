#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль диалоговых функций пользователя.
"""

# Подключение пакетов
import md5
import thread
import time
import os
import os.path
import traceback
import wx
import wx.lib.imagebrowser

from ic.log import log


__version__ = (0, 1, 2, 1)


def icFileDlg(Win_=None, Title_='', Filter_='', DefaultPath_=''):
    """
    Открыть диалог выбора файла для открытия/записи.
    @param Win_: Ссылка на окно.
    @param Title_: Заголовок диалогового окна.
    @param Filter_: Фильтр файлов.
    @param DefaultPath_: Путь по умолчанию.
    @return: Возвращает полное имя выбранного файла.
    """
    dlg = None
    win_clear = False
    try:
        if Win_ is None:
           Win_ = wx.Frame(None, -1, '')
           win_clear = True

        wildcard = Filter_+'|All Files (*.*)|*.*'
        dlg = wx.FileDialog(Win_, Title_, '', '', wildcard, wx.OPEN)
        if DefaultPath_:
            dlg.SetDirectory(os.path.normpath(DefaultPath_))
        else:
            dlg.SetDirectory(os.getcwd())
        
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.GetPaths()[0]
        else:
            result = ''
        dlg.Destroy()
        return result
    finally:
        if dlg:
            dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
           Win_.Destroy()


def icDirDlg(Win_=None, Title_='', DefaultPath_=''):
    """
    Диалог выбора каталога.
    @param Win_: Ссылка на окно.
    @param Title_: Заголовок диалогового окна.
    @param DefaultPath_: Путь по умолчанию.
    """
    result = ''
    dlg = None
    win_clear = False
    try:
        if Win_ is None:
           Win_ = wx.Frame(None, -1, '')
           win_clear = True

        dlg = wx.DirDialog(Win_, Title_, style=wx.DD_DEFAULT_STYLE|wx.DD_NEW_DIR_BUTTON)
        # Установка пути по умолчанию
        if not DefaultPath_:
            DefaultPath_ = os.getcwd()
        dlg.SetPath(DefaultPath_)
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.GetPath()
        else:
            result = ''
    finally:
        if dlg:
            dlg.Destroy()
            dlg = None

        # Удаляем созданное родительское окно
        if win_clear:
           Win_.Destroy()
    return result


def icImageDlg(Parent_=None, DefaultImgDir_=None):
    """
    Диалог выбора графических файлов.
    @param Parent_: Ссылка на окно.
    @param DefaultImgDir_: Указание папки образа.
    @return: Возвращает полное имя выбранного файла.
    """
    dlg = None
    win_clear = False
    try:
        if Parent_ is None:
           Parent_ = wx.Frame(None, -1, '')
           win_clear = True

        # Определить папку образов
        if not DefaultImgDir_ or not os.path.exists(DefaultImgDir_):
            from ic.bitmap import ic_bmp
            DefaultImgDir_ = ic_bmp.getImageLibDir()
        # Диалоговое окно выбора образа
        dlg = wx.lib.imagebrowser.ImageDialog(Parent_, DefaultImgDir_)
        dlg.CenterOnScreen()

        ret = None      # Возвращаемое значение
        if dlg.ShowModal() == wx.ID_OK:
            ret = dlg.GetFile()
    except:
        log.fatal(u'Путь: <%s>' % DefaultImgDir_)
        
    if dlg:
        dlg.Destroy()
    # Удаляем созданное родительское окно
    if win_clear:
        Parent_.Destroy()
        
    return ret


def icColorDlg(Win_=None, Title_='', Default_=wx.BLACK):
    """
    Диалог выбора цвета
    @param Win_: Ссылка на окно.
    @param Title_: Заголовок диалогового окна.
    @param Default_: Значение по умолчанию.
    @return: Возвращает выбранный цвет или Default_.
    """
    dlg = None
    win_clear = False
    try:
        if Win_ is None:
           Win_ = wx.Frame(None, -1, '')
           win_clear = True

        dlg = wx.ColourDialog(Win_, wx.ColourData().SetColour(Default_))
        dlg.SetTitle(Title_)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            color = dlg.GetColourData().GetColour()
        else:
            color = Default_
        dlg.Destroy()
        return color
    finally:
        if dlg:
            dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
           Win_.Destroy()


def icTextEntryDlg(Win_=None, Title_='', Text_='', Default_=''):
    """
    Диалог ввода строки.
    @param Win_: Ссылка на окно.
    @param Title_: Заголовок диалогового окна.
    @param Text_: Текст диалога.
    @param Default_: Значение по умолчанию.
    @return: Возвращает введеную строку, если нажата отмена, то пустую строку.
    """
    dlg = None
    win_clear = False
    try:
        if Win_ is None:
           Win_ = wx.Frame(None, -1, '')
           win_clear = True

        dlg = wx.TextEntryDialog(Win_, Text_, Title_)
        if Default_ is None:
            Default_ = ''
        dlg.SetValue(str(Default_))
        if dlg.ShowModal() == wx.ID_OK:
            txt = dlg.GetValue()
            return txt
        return ''
    finally:
        if dlg:
            dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
            Win_.Destroy()


def icAskDlg(Title_='', Text_='', Style_=wx.YES_NO | wx.ICON_QUESTION):
    """
    Диалог вопроса.
    @param Title_: Заголовок диалогового окна.
    @param Text_: Текст диалога.
    @param Style_: Стиль диалога.
    @return: Код нажатой кнопки (Например: wx.YES или wx.NO).
    """
    try:
        return wx.MessageBox(Text_, Title_, style=Style_)
    except:
        log.fatal()


def icAskBox(*args, **kwargs):
    """
    Диалог вопроса.
    """
    return icAskDlg(*args, **kwargs) == wx.YES


def icMsgBox(Title_='', Text_='', **kwargs):
    """
    Вывод сообщения.
    @param ParentWin_: Родительское окно.
    @param Title_: Заголовок диалогового окна.
    @param Text_: Текст диалога.
    @return: Код нажатой кнопки (Например: wx.YES или wx.NO).
    """
    if 'ParentWin_' in kwargs:
        kwargs['parent'] = kwargs['ParentWin_']
        del kwargs['ParentWin_']
    try:
        return wx.MessageBox(Text_, Title_, style=wx.OK, **kwargs)
    except:
        log.fatal()


def icErrBox(Title_='', Text_='', **kwargs):
    """
    Вывод сообщения об ошибке.
    @param ParentWin_: Родительское окно.
    @param Title_: Заголовок диалогового окна.
    @param Text_: Текст диалога.
    @return: Код нажатой кнопки (Например: wx.YES или wx.NO).
    """
    if 'ParentWin_' in kwargs:
        kwargs['parent'] = kwargs['ParentWin_']
        del kwargs['ParentWin_']
    try:
        return wx.MessageBox(Text_, Title_, style=wx.OK | wx.ICON_ERROR, **kwargs)
    except:
        log.fatal()


def icFatalBox(Title_='', Text_='', **kwargs):
    """
    Вывод сообщения об ошибке вместе с Traceback.
    @param ParentWin_: Родительское окно.
    @param Title_: Заголовок диалогового окна.
    @param Text_: Текст диалога.
    @return: Код нажатой кнопки (Например: wx.YES или wx.NO).
    """
    if 'ParentWin_' in kwargs:
        kwargs['parent'] = kwargs['ParentWin_']
        del kwargs['ParentWin_']
    trace_txt = traceback.format_exc()
    txt = Text_ + trace_txt
    return icErrBox(Title_, txt, **kwargs)


def icWarningBox(Title_='', Text_='', **kwargs):
    """
    Вывод сообщения об предупреждении.
    @param ParentWin_: Родительское окно.
    @param Title_: Заголовок диалогового окна.
    @param Text_: Текст диалога.
    @return: Код нажатой кнопки (Например: wx.YES или wx.NO).
    """
    if 'ParentWin_' in kwargs:
        kwargs['parent'] = kwargs['ParentWin_']
        del kwargs['ParentWin_']
    try:
        return wx.MessageBox(Text_, Title_, style=wx.OK | wx.ICON_WARNING, **kwargs)
    except:
        log.fatal()


def icSingleChoiceDlg(Parent_=None, Title_='', Text_='', Choice_=[],
                      default_idx=-1):
    """
    Диалог выбора из списка.
    @param Parent_: Родительское окно.
    @param Title_: Заголовок диалогового окна.
    @param Text_: Текст диалога.
    @param Choice_: Список строк выбора.
    @param default_idx: Индекс строки, выбираемой по умолчанию.
        Если не указывается, то ничего по умолчанию не выбирает.
    @return: Выбранный текст или None, если нажата Cancel.
    """
    dlg = None
    win_clear = False
    try:
        if Parent_ is None:
           Parent_ = wx.Frame(None, -1, '')
           win_clear = True

        dlg = wx.SingleChoiceDialog(Parent_, Text_, Title_, Choice_, wx.CHOICEDLG_STYLE)
        if default_idx >= 0:
            dlg.SetSelection(default_idx)
        if dlg.ShowModal() == wx.ID_OK:
            txt = dlg.GetStringSelection()
            return txt
        return None

    finally:
        if dlg:
            dlg.Destroy()
        # Удаляем созданное родительское окно
        if win_clear:
            Parent_.Destroy()


def icSingleChoiceIdxDlg(Parent_=None, Title_='', Text_='', Choice_=[],
                         default_idx=-1):
    """
    Диалог выбора.
    @param Parent_: Родительское окно.
    @param Title_: Заголовок диалогового окна.
    @param Text_: Текст диалога.
    @param Choice_: Список выбора. Список строк.
    @param default_idx: Индекс строки, выбираемой по умолчанию.
        Если не указывается, то ничего по умолчанию не выбирает.
    @return: Выбранный индекс в списке выбора или -1, если нажата Cancel.
    """
    idx = -1
    dlg = None
    win_clear = False
    try:
        if Parent_ is None:
           Parent_ = wx.Frame(None, -1, '')
           win_clear = True

        dlg = wx.SingleChoiceDialog(Parent_, Text_, Title_,
                                    Choice_, wx.CHOICEDLG_STYLE)
        if default_idx >= 0:
            dlg.SetSelection(default_idx)

        if dlg.ShowModal() == wx.ID_OK:
            idx = dlg.GetSelection()
    finally:
        if dlg:
            dlg.Destroy()
        # Удаляем созданное родительское окно
        if win_clear:
            Parent_.Destroy()
    return idx


def icMultiChoiceDlg(Parent_=None, Title_='', Text_='', Choice_=()):
    """
    Диалог множественного выбора.
    @param Parent_: Родительское окно.
    @param Title_: Заголовок диалогового окна.
    @param Text_: Текст диалога.
    @param Choice_: Список выбора.Кортеж выбора в формате ((True/False,'Текст'),...).
    @return: Кортеж выбора в формате ((True/False,'Текст'),...).
    """
    dlg = None
    win_clear = False
    try:
        if Parent_ is None:
           Parent_ = wx.Frame(None, -1, '')
           win_clear = True

        choice_list = [row[1] for row in Choice_]
        dlg = wx.MultiChoiceDialog(Parent_, Text_, Title_, choice_list)
        # Установить выбор по умолчанию
        selections = [i for i, row in enumerate(Choice_) if row[0]]
        dlg.SetSelections(selections)
        
        if dlg.ShowModal() == wx.ID_OK:
            selections = dlg.GetSelections()
            result = [(bool(i in selections), txt) for i, txt in enumerate(choice_list)]
            return result
    finally:
        if dlg:
            dlg.Destroy()
        # Удаляем созданное родительское окно
        if win_clear:
            Parent_.Destroy()
    return None


class icProgressDlg(wx.ProgressDialog):
    """
    Класс диалогового окна прогресс бара.
    """

    def __init__(self, Win_=None, Title_='', Msg_='', Min_=0, Max_=100, Style_=wx.PD_CAN_ABORT):
        """
        Конструктор. Создает и открывает прогресс бар.
        @param Win_: Ссылка на окно.
        @param Title_: Заголовок диалогового окна.
        @param Msg_: Текст диалога.
        @param Min_: Минимальное значение.
        @param Max_: Максимальное занчение.
        @param Style_: Стиль диалога.
        @return: Объект диалога.
        """
        # Атрибуты класса
        self._ProgressFrame = Win_    # Фрейм прогресс бара
        self._MyFrame = False
        if self._ProgressFrame is None:
            self._ProgressFrame = wx.Frame(None, -1, '')
            self._MyFrame = True

        self._ProgressMIN = Min_    # Минимальное значение
        self._ProgressMAX = Max_    # Максимальное значение
        if self._ProgressMIN > self._ProgressMAX:
            tmp_value = self._ProgressMAX
            self._ProgressMAX = self._ProgressMIN
            self._ProgressMIN = tmp_value
        # Текущее значение счетчика
        self._current_value = 0
        try:
            # Вызов конструктор а предка
            wx.ProgressDialog.__init__(self, Title_, Msg_,
                                       self._ProgressMAX-self._ProgressMIN,
                                       self._ProgressFrame, Style_ | wx.PD_APP_MODAL)

            # Образмерить и отцентровать диалоговое окно
            self.SetSize(wx.Size(500, 130))
            self.CenterOnScreen()
        except:
            log.fatal(u'Ошибка создания диалогового окна прогресс-бара')

    def getMax(self):
        return self._ProgressMAX

    def getMin(self):
        return self._ProgressMIN

    def UpdateDlg(self, Value_=-1, NewMsg_=''):
        """
        Обновить данные програсс бара.
        @param Value_: Значение.
        @param NewMsg_: Текст диалога.
        """
        # Ограничение значения
        if Value_ < self._ProgressMIN:
            Value_ = self._ProgressMIN
        if Value_ > self._ProgressMAX:
            Value_ = self._ProgressMAX
        self.Update(Value_-self._ProgressMIN, NewMsg_)

    def StepDlg(self, step_value=1, new_msg=u''):
        """
        Обновить данные програсс бара с приращением.
        @param step_value: Значение приращения.
        @param new_msg: Текст диалога.
        """
        self._current_value += step_value
        # Ограничение значения
        if self._current_value < self._ProgressMIN:
            self._current_value = self._ProgressMIN
        if self._current_value > self._ProgressMAX:
            self._current_value = self._ProgressMAX
        self.Update(self._current_value - self._ProgressMIN, new_msg)

    # Закрыть прогресс бар
    def CloseDlg(self):
        """
        Закрыть прогресс бар.
        """
        self.Close()
        # Если фрейм диалогового окна создавался, то удалить его
        if self._MyFrame:
            self._ProgressFrame.Close()
            self._ProgressFrame.Destroy()
            self._ProgressFrame = None


_PROGRESS_DLG = None    # Сам диалог прогресс бара


def icOpenProgressDlg(Win_=None, Title_='', Msg_='', Min_=0, Max_=100, Style_=wx.PD_AUTO_HIDE):
    """
    Диалоговые функции прогресс бара.
    Создает и открывает прогресс бар.
    @param Win_: Ссылка на окно.
    @param Title_: Заголовок диалогового окна.
    @param Msg_: Текст диалога.
    @param Min_: Минимальное значение.
    @param Max_: Максимальное занчение.
    @param Style_: Стиль диалога.
    @return: Объект диалога.
    """
    try:
        global _PROGRESS_DLG
        _PROGRESS_DLG = icProgressDlg(Win_, Title_, Msg_, Min_, Max_, Style_)
    except:
        log.fatal(u'Ошибка открытия прогресс бара')
        _PROGRESS_DLG = None
    return _PROGRESS_DLG


def icUpdateProgressDlg(Value_=-1, NewMsg_=''):
    """
    Диалоговые функции прогресс бара.
    Обновить данные програсс бара.
    @param Value_: Значение.
    @param NewMsg_: Текст диалога.
    @return: Возвращает результат выполнения операции True/False.
    """
    try:
        global _PROGRESS_DLG
        if _PROGRESS_DLG is not None:
            _PROGRESS_DLG.UpdateDlg(Value_, NewMsg_)
            return True
        return False
    except:
        log.fatal(u'Ошибка обновления прогресс бара')
        return False


def icStepProgressDlg(step_value=1, new_msg=u''):
    """
    Диалоговые функции прогресс бара с приращением.
    Обновить данные програсс бара.
    @param step_value: Значение приращения.
    @param new_msg: Текст диалога.
    @return: Возвращает результат выполнения операции True/False.
    """
    try:
        global _PROGRESS_DLG
        if _PROGRESS_DLG is not None:
            _PROGRESS_DLG.StepDlg(step_value, new_msg)
            return True
        return False
    except:
        log.fatal(u'Ошибка обновления прогресс бара с приращением')
        return False


def icCloseProgressDlg():
    """
    Диалоговые функции прогресс бара.
    Закрыть прогресс бар.
    """
    try:
        global _PROGRESS_DLG
        if _PROGRESS_DLG is not None:
            # ВНИМАНИЕ! Необходимо сначала выставить прогрес бар до конечной точки
            # иначе диалоговое окно не закрывается
            _PROGRESS_DLG.UpdateDlg(_PROGRESS_DLG.getMax())
            _PROGRESS_DLG.CloseDlg()
            return True
        return False
    except:
        log.fatal(u'Ошибка закрытия прогресс бара')
        return False


def icStrComboBoxDlg(Win_=None, Title_='', Text_='', StrList_=None, Default_=''):
    """
    Диалог выбора/редактирования строки.
    @param Win_: Ссылка на окно.
    @param Title_: Заголовок диалогового окна.
    @param Text_: Текст диалога.
    @param StrList_: Список строк, позволяющих выбрать строку из уже существующих.
    @return: Строку введенную/выбранную пользователем.
    """
    dlg = None
    win_clear = False
    try:
        if StrList_ is None:
            StrList_ = []

        if Win_ is None:
           Win_ = wx.Frame(None, -1, '')
           win_clear = True

        dlg = icStrComboBoxDialog(Win_, Title_, Text_, StrList_, Default_)
        if dlg.ShowModal() == wx.ID_OK:
            return dlg.GetEntryString()
        return Default_
    finally:
        if dlg:
            dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
            Win_.Destroy()


class icStrComboBoxDialog(wx.Dialog):
    """
    Диалог выбора/редактирования строки.
    """
    def __init__(self, parent, Title_='', Text_='', StrList_=None, Default_=''):
        """
        Конструктор.
        @param parent: Окно.
        @param Title_: Заголовок диалогового окна.
        @param Text_: Текст диалога.
        @param StrList_: Список строк, позволяющих выбрать строку из уже существующих.
        """
        try:
            if StrList_ is None:
                StrList_ = []

            # Instead of calling wx.Dialog.__init__ we precreate the dialog
            # so we can set an extra style that must be set before
            # creation, and then we create the GUI object using the Create
            # method.
            pre = wx.PreDialog()
            pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
            pre.Create(parent, -1, title=Title_,
                       pos=wx.DefaultPosition, size=wx.Size(500, 150))

            # This next step is the most important, it turns this Python
            # object into the real wrapper of the dialog (instead of pre)
            # as far as the wxPython extension is concerned.
            self.PostCreate(pre)

            self._text = wx.StaticText(self, -1, Text_, wx.Point(10, 10), wx.Size(-1, -1))
            # Кнопка -OK-
            id_ = wx.NewId()
            self._ok_button = wx.Button(self, id_, u'OK', wx.Point(420, 80), wx.Size(60, -1))
            self.Bind(wx.EVT_BUTTON, self.OnOK, id=id_)
            # Кнопка -Отмена-
            id_ = wx.NewId()
            self._cancel_button = wx.Button(self, id_, u'Отмена', wx.Point(340, 80), wx.Size(60, -1))
            self.Bind(wx.EVT_BUTTON, self.OnCancel, id=id_)
            # Поле редактирования
            id_ = wx.NewId()
            self._combo_box = wx.ComboBox(self, 500, Default_, wx.Point(20, 30), wx.Size(460, -1),
                                          StrList_, wx.CB_DROPDOWN)
            # Редактируемая строка
            self._string = Default_
        except:
            log.fatal(u'Ошибка создания объекта диалогового окна выбора/редактирования строки')

    def OnOK(self, event):
        """
        Обработчик нажатия кнопки -OK-.
        """
        self._string = self._combo_box.GetValue()
        self.EndModal(wx.ID_OK)

    def OnCancel(self, event):
        """
        Обработчик нажатия кнопки -Отмена-.
        """
        self.EndModal(wx.ID_CANCEL)

    def GetEntryString(self):
        """
        Получить отредактированную строку.
        """
        return self._string


def icAboutDlg(Win_=None, Title_='', Text_='', Logo_=None):
    """
    О программе...
    @param Win_: Ссылка на окно.
    @param Title_: Заголовок диалогового окна.
    @param Text_: Текст.
    @param Logo_: Объект типа wx.Bitmap определяющий логотип.
    """
    dlg = None
    win_clear = False
    try:
        if Win_ is None:
           Win_ = wx.Frame(None, -1, '')
           win_clear = True

        dlg = icAboutDialog(Win_, Title_, Text_, Logo_)
        dlg.ShowModal()
    finally:
        if dlg:
            dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
           Win_.Destroy()


class icAboutDialog(wx.Dialog):
    """
    Диалог 'О программе...'.
    """
    def __init__(self, parent, Title_='', Text_='', Logo_=None):
        """
        Конструктор.
        @param parent: Окно.
        @param Title_: Заголовок диалогового окна.
        @param Text_: Текст.
        @param Logo_: Объект типа wx.Bitmap определяющий логотип.
        """
        try:
            # Instead of calling wx.Dialog.__init__ we precreate the dialog
            # so we can set an extra style that must be set before
            # creation, and then we create the GUI object using the Create
            # method.
            pre = wx.PreDialog()
            pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
            pre.Create(parent, -1, title=Title_,
                       pos=wx.DefaultPosition, size=wx.Size(500, 500))

            # This next step is the most important, it turns this Python
            # object into the real wrapper of the dialog (instead of pre)
            # as far as the wxPython extension is concerned.
            self.PostCreate(pre)

            # Сайзер
            sizer = wx.BoxSizer(wx.VERTICAL)
            # Логотип
            self._logo = None
            if Logo_ is not None:
                self._logo = wx.StaticBitmap(self, -1, Logo_, pos=wx.Point(10, 10))
                sizer.Add(self._logo, 10, wx.ALL, 5)
            # Текст
            self._text = wx.StaticText(self, -1, Text_)
            sizer.Add(self._text, 0, wx.ALL, 5)
            # Разделительная линия
            line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
            sizer.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP, 5)
            # Кнопка -OK-
            id_ = wx.NewId()
            self._ok_button = wx.Button(self, id_, u'OK')
            self.Bind(wx.EVT_BUTTON, self.OnOK, id=id_)
            sizer.Add(self._ok_button, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

            self.SetSizer(sizer)
            self.SetAutoLayout(True)
            sizer.Fit(self)
        except:
            log.fatal(u'Ошибка создания объекта диалогового окна выбора/редактирования строки')

    def OnOK(self, event):
        """
        Обработчик нажатия кнопки -OK-.
        """
        self.EndModal(wx.ID_OK)

#
LOGIN_USER_IDX = 0
LOGIN_PASSWORD_IDX = 1
LOGIN_PASSWORD_MD5_IDX = 2


def icLoginDlg(Win_=None, Title_='', DefaultUser_='', RegUsers_=None):
    """
    Ввод пароля и имени пользователя.
    @param Win_: Ссылка на окно.
    @param Title_: Заголовок диалогового окна.
    @param DefaultUser_: Имя пользователя заполняемое по умолчанию.
    @param RegUsers_: Список зарегестрированных пользователей.
    @return: Возвращает кортеж из 2-х строк.
        Первый элемент - пользхователь (LOGIN_USER_IDX).
        Второй элемент - пароль (LOGIN_PASSWORD_IDX).
    """
    dlg = None
    try:
        win_clear = False
        if Win_ is None:
            id_ = wx.NewId()
            Win_ = wx.Frame(None, id_, '')
            win_clear = True

        dlg = icLoginDialog(Win_, Title_, DefaultUser_, RegUsers_)
        if dlg.ShowModal() == wx.ID_OK:
            result = (dlg.GetEntryUser(), dlg.GetEntryPassword(), dlg.GetEntryPasswordMD5())
            dlg.Destroy()
            # Удаляем созданное родительское окно
            if win_clear:
                Win_.Destroy()
            return result
    finally:
        if dlg:
            dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
            Win_.Destroy()
    return None


class icLoginDialog(wx.Dialog):
    """
    Диалоговое окно ввода пароля и имени пользователя.
    Диалог регистрации пользователя.
    """
    def __init__(self, parent_, Title_='', DefaultUser_='', RegUsers_=None):
        """
        Конструктор.
        @param parent_: Окно.
        @param Title_: Заголовок диалогового окна.
        """
        try:
            if not Title_:
                Title_ = ''
                
            # Instead of calling wx.Dialog.__init__ we precreate the dialog
            # so we can set an extra style that must be set before
            # creation, and then we create the GUI object using the Create
            # method.
            pre = wx.PreDialog()
            pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
            pre.Create(parent_,-1, title=Title_,
                       pos=wx.DefaultPosition, size=wx.Size(350, 150))

            # This next step is the most important, it turns this Python
            # object into the real wrapper of the dialog (instead of pre)
            # as far as the wxPython extension is concerned.
            self.PostCreate(pre)
            from ic.PropertyEditor.images import editorimg
            icon_img = editorimg.shield.GetBitmap()
            if icon_img:
                icon = wx.IconFromBitmap(icon_img)
                self.SetIcon(icon)

            id_ = wx.NewId()
            self._text = wx.StaticText(self, id_, u'Пользователь:',
                                       wx.Point(10, 10), wx.Size(-1, -1))
            id_ = wx.NewId()
            self._text = wx.StaticText(self, id_, u'Пароль:',
                                       wx.Point(10, 40), wx.Size(-1, -1))

            # Кнопка -OK-
            id_ = wx.NewId()
            self._ok_button = wx.Button(self, id_, u'OK',
                                        wx.Point(280, 80), wx.Size(60, -1))
            self.Bind(wx.EVT_BUTTON, self.OnOK, id=id_)
            self.Bind(wx.EVT_KEY_DOWN, self.OnKey)
            # Кнопка -Отмена-
            id_ = wx.NewId()
            self._cancel_button = wx.Button(self, id_, u'Отмена',
                                            wx.Point(200, 80), wx.Size(60, -1))
            self.Bind(wx.EVT_BUTTON, self.OnCancel, id=id_)
            # Поля редактирования
            id_ = wx.NewId()
            if RegUsers_ is None:
                RegUsers_ = []
            if DefaultUser_ is None:
                DefaultUser_ = ''
            self._user_edit = wx.ComboBox(self, id_,
                                          value=DefaultUser_,
                                          pos=(120, 10), size=(220, -1),
                                          choices=RegUsers_)
            id_ = wx.NewId()
            self._password_edit = wx.TextCtrl(self, id_, '',
                                              wx.Point(120, 40), wx.Size(220, -1),
                                              style=wx.TE_PASSWORD)

            self._user = DefaultUser_
            self._password = ''
            # Установить фокус на первый управляющий элемент
            self._user_edit.SetFocus()
        except:
            log.fatal(u'Ошибка создания объекта диалогового окна ввода пароля и имени пользователя')

    def OnKey(self, event):
        """
        Обработчик нажатия клавиш клавиатуры.
        """
        key = event.GetKeyCode()
        if key == wx.K_ESCAPE:
            self.EndModal(wx.ID_CANCEL)
        elif key == wx.K_RETURN:
            self._user = self._get_user_name_from_combobox()
            self._password = self._password_edit.GetValue()
            self.EndModal(wx.ID_OK)

    def OnOK(self, event):
        """
        Обработчик нажатия кнопки -OK-.
        """
        self._user = self._get_user_name_from_combobox()
        self._password = self._password_edit.GetValue()
        self.EndModal(wx.ID_OK)

    def OnCancel(self, event):
        """
        Обработчик нажатия кнопки -Отмена-.
        """
        self.EndModal(wx.ID_CANCEL)

    def _get_user_name_from_combobox(self):
        """
        Выбрать имя пользователя из комбобокса.
        """
        value = self._user_edit.GetValue()
        # Значение имени пользователя может быть введено в виде: <имя> [(Описание)]
        if value:
            return value.split(' ')[0].strip() 
        return ''
    
    def GetEntryUser(self):
        """
        Получить введенного пользователя.
        """
        return self._user

    def GetEntryPassword(self):
        """
        Получить введенный пароль.
        """
        return self._password

    def GetEntryPasswordMD5(self):
        """
        Получить введенный пароль md5.
        """
        return md5.new(self._password).hexdigest()

_BUSY_INFO = None


def BusyStart(Msg_=''):
    """
    Занято/Ожидание.
    @param Msg_: Текст диалога.
    """
    wx.BeginBusyCursor()    # Курсор
    global _BUSY_INFO
    if _BUSY_INFO is None:
        if Msg_:
            _BUSY_INFO = wx.BusyInfo(Msg_)  # Окно


def BusyStop():
    """
    Не занято.
    """
    global _BUSY_INFO
    if _BUSY_INFO:
        _BUSY_INFO = None
    wx.EndBusyCursor()  # Курсор


ic_wait_proccess_dlg = None


def WaitFunc(Parent_, Msg_,
             Func_, FuncArgs_=(), FuncKW_={},
             Frames_=None):
    """
    Окно ожидания.
    @param Parent_: Ссылка на окно.
    @param Msg_: Текст диалога.
    @param Func_: Функция, которую необходимо подождать.
    @param FuncArgs_: Аргументы функции.
    @param FuncKW_: Именованные аргументы функции.
    @param Frames_: Файлы-кадры.
    """
    global ic_wait_proccess_dlg
    
    wait_result = [None]
    if not Frames_:
        # Определить кадры по умолчанию
        wait_dir = os.path.dirname(__file__)+'/Wait/'
        Frames_ = [wait_dir+'Wait1.png',
                   wait_dir+'Wait2.png',
                   wait_dir+'Wait3.png',
                   wait_dir+'Wait4.png',
                   wait_dir+'Wait5.png',
                   wait_dir+'Wait6.png',
                   wait_dir+'Wait7.png',
                   wait_dir+'Wait8.png',
                   wait_dir+'Wait9.png',
                   wait_dir+'Wait10.png',
                   wait_dir+'Wait11.png',
                   wait_dir+'Wait12.png',
                   wait_dir+'Wait13.png',
                   wait_dir+'Wait14.png',
                   wait_dir+'Wait15.png']
    ic_wait_proccess_dlg = wait_box = icWaitBox(Parent_, Msg_, Frames_)
    wait_box.SetResultList(wait_result)
    # Запустить функцию ожидания
    thread.start_new(wait_box.Run, (Func_, FuncArgs_, FuncKW_))
    wait_box.ShowModal()
    wait_box.Destroy()
    ic_wait_proccess_dlg = None
    return wait_result[0]


def wait_deco(f):
    def func(*arg, **kwarg):
        return WaitFunc(arg[0], u'Подождите   ', f, arg, kwarg)
    return func


def wait_noparent_deco(f):
    def func(*arg, **kwarg):
        return WaitFunc(None, u'Подождите   ', f, arg, kwarg)
    return func


def SetWaitBoxLabel(label):
    if ic_wait_proccess_dlg:
        sx, sy = ic_wait_proccess_dlg.GetSize()
        ic_wait_proccess_dlg.SetSize((len(label)*10 + 20, sy))
        ic_wait_proccess_dlg.CenterOnScreen()
        ic_wait_proccess_dlg.SetLabel(label)
        

class icWaitBox(wx.Dialog):
    def __init__(self, Parent_, Msg_, Frames_, style=0):
        """
        Конструктор.
        """
        if Parent_ is None:
            style = wx.STAY_ON_TOP
            
        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(Parent_, -1,
                   size=wx.Size(150, 34), style=style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)

        from ic.bitmap import ic_bmp
        self._ani = [ic_bmp.createBitmap(frame_file_name) for frame_file_name in Frames_]
        self._cur_ani_state = 0     # Индекс состояния анимации
        self._max_ani_state = len(Frames_)
        self._delay = 0.3
        self._picture = wx.StaticBitmap(self, -1, self._ani[0])
        self._pic_size = (self._ani[0].GetWidth(), self._ani[0].GetHeight())
        self.msg = msg = wx.StaticText(self, -1, Msg_)
        self._lastTime = time.clock()
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self._picture, 0, wx.CENTRE, 5)
        sizer.Add(msg, 0, wx.CENTRE, 5)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        self.CenterOnScreen()

        self._running = True    # Признак запущенной функции
        self._closed = False    # Признак закрытия окна
        self._result_list = None
        
        self.Bind(wx.EVT_UPDATE_UI, self.OnCheckClose)

    def DirectRefresh(self):
        """
        """
        evt = wx.PaintEvent(self.GetId())
        return self.GetEventHandler().ProcessEvent(evt)

    def SetResultList(self, ResultList_):
        self._result_list = ResultList_
        
    def NextState(self):
        """
        Сменить состояние.
        """
        self._cur_ani_state += 1
        if self._cur_ani_state >= self._max_ani_state:
            self._cur_ani_state = 0
        return self._cur_ani_state

    def DrawFrame(self, NFrame_):
        """
        Отрисовка кадра.
        @param NFrame_: Номер кадра.
        """
        frame_bmp = self._ani[NFrame_]
        
        dc = wx.WindowDC(self._picture)
        dc.BeginDrawing()
        dc.Clear()
        dc.DrawBitmap(frame_bmp, 0, 0, True)
        dc.EndDrawing()
        self._picture.Refresh()
        
    def OnCheckClose(self, event=None):
        """
        Проверка закрытия окна.
        """
        # 2 Варианта отрисовки не знаю какой лучше выбрать!!!
        # 2-й вроде немного по быстрее
        self.DrawFrame(self.NextState())    # Отрисовать очередной кадр
        time.sleep(self._delay)

        if not self._running and not self._closed:
            try:
                self.EndModal(wx.ID_OK)
            except:
                pass
            self._closed = True
            
        if event:
            event.Skip()

    def Run(self, Func_, Args_, KW_):
        """
        Запуск ожидания функции.
        """
        self._running = True
        result = Func_(*Args_, **KW_)
        self._running = False
        # Сбросить в результирующий список
        if isinstance(self._result_list, list):
            self._result_list[0] = result
            
    def SetLabel(self, label=None):
        """
        """
        if self.msg:
            self.DirectRefresh()
            if label:
                self.msg.SetLabel(label)
            evt = wx.PaintEvent(self.msg.GetId())
            self.msg.GetEventHandler().ProcessEvent(evt)
