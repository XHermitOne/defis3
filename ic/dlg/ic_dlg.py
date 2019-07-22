#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль диалоговых функций пользователя.
"""

# Подключение пакетов
import hashlib
import _thread
import time
import os
import os.path
import traceback
import wx
import wx.lib.imagebrowser

from ic.log import log


__version__ = (1, 1, 1, 3)


def icFileDlg(parent=None, title='', wildcard_filter='', default_path=''):
    """
    Открыть диалог выбора файла для открытия/записи.
    @param parent: Ссылка на окно.
    @param title: Заголовок диалогового окна.
    @param wildcard_filter: Фильтр файлов.
        Например: All ZIP Files (*.zip)|*.zip
    @param default_path: Путь по умолчанию.
    @return: Возвращает полное имя выбранного файла или None в случае ошибки.
    """
    dlg = None
    win_clear = False
    try:
        if parent is None:
           parent = wx.Frame(None, -1, '')
           win_clear = True

        wildcard = wildcard_filter + '|All Files (*.*)|*.*'
        dlg = wx.FileDialog(parent, title, '', '', wildcard, wx.FD_OPEN)
        if default_path:
            dlg.SetDirectory(os.path.normpath(default_path))
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
           parent.Destroy()
    return None


def icDirDlg(parent=None, title='', default_path=''):
    """
    Диалог выбора каталога.
    @param parent: Ссылка на окно.
    @param title: Заголовок диалогового окна.
    @param default_path: Путь по умолчанию.
    @return: Возвращает путь каталога или None в случае ошибки.
    """
    result = ''
    dlg = None
    win_clear = False
    try:
        if parent is None:
           parent = wx.Frame(None, -1, '')
           win_clear = True

        dlg = wx.DirDialog(parent, title,
                           style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        # Установка пути по умолчанию
        if not default_path:
            default_path = os.getcwd()
        dlg.SetPath(default_path)
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.GetPath()
    except:
        log.fatal(u'Ошибка вызова диалога выбора директории')
        result = None

    if dlg:
        dlg.Destroy()
        dlg = None

    # Удаляем созданное родительское окно
    if win_clear:
        parent.Destroy()

    return result


def icImageDlg(parent=None, default_img_path=None):
    """
    Диалог выбора графических файлов.
    @param parent: Ссылка на родительское окно.
    @param default_img_path: Указание папки образа.
    @return: Возвращает полное имя выбранного файла.
    """
    dlg = None
    win_clear = False
    ret = None  # Возвращаемое значение
    try:
        if parent is None:
           parent = wx.Frame(None, -1, '')
           win_clear = True

        # Определить папку образов
        if not default_img_path or not os.path.exists(default_img_path):
            from ic.bitmap import bmpfunc
            default_img_path = bmpfunc.getImageLibDir()
        # Диалоговое окно выбора образа
        dlg = wx.lib.imagebrowser.ImageDialog(parent, default_img_path)
        dlg.CenterOnScreen()

        if dlg.ShowModal() == wx.ID_OK:
            ret = dlg.GetFile()
    except:
        log.fatal(u'Ошибка диалога выбора графического файла. Путь: <%s>' % default_img_path)
        
    if dlg:
        dlg.Destroy()
    # Удаляем созданное родительское окно
    if win_clear:
        parent.Destroy()
        
    return ret


def icColorDlg(parent=None, title='', default_colour=wx.BLACK):
    """
    Диалог выбора цвета
    @param parent: Ссылка на родительское окно.
    @param title: Заголовок диалогового окна.
    @param default_colour: Значение по умолчанию.
    @return: Возвращает выбранный цвет или default_colour.
    """
    dlg = None
    win_clear = False
    try:
        if parent is None:
           parent = wx.Frame(None, -1, '')
           win_clear = True

        dlg = wx.ColourDialog(parent, wx.ColourData().SetColour(default_colour))
        dlg.SetTitle(title)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            color = dlg.GetColourData().GetColour()
        else:
            color = default_colour
        dlg.Destroy()
        return color
    finally:
        if dlg:
            dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
           parent.Destroy()


def icTextEntryDlg(parent=None, title='', prompt_text='', default_value=''):
    """
    Диалог ввода строки.
    @param parent: Ссылка на окно.
    @param title: Заголовок диалогового окна.
    @param prompt_text: Текст диалога.
    @param default_value: Значение по умолчанию.
    @return: Возвращает введеную строку, если нажата отмена, то None.
    """
    dlg = None
    win_clear = False
    try:
        if parent is None:
           parent = wx.Frame(None, -1, '')
           win_clear = True

        dlg = wx.TextEntryDialog(parent, prompt_text, title)
        if default_value is None:
            default_value = ''
        dlg.SetValue(str(default_value))
        if dlg.ShowModal() == wx.ID_OK:
            txt = dlg.GetValue()
            return txt
    finally:
        if dlg:
            dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
            parent.Destroy()
    return None


def icAskDlg(title='', prompt_text='', style=wx.YES_NO | wx.ICON_QUESTION):
    """
    Диалог вопроса.
    @param title: Заголовок диалогового окна.
    @param prompt_text: Текст диалога.
    @param style: Стиль диалога.
    @return: Код нажатой кнопки (Например: wx.YES или wx.NO).
    """
    try:
        return wx.MessageBox(prompt_text, title, style=style)
    except:
        log.fatal()


def icAskBox(*args, **kwargs):
    """
    Диалог вопроса.
    """
    return icAskDlg(*args, **kwargs) == wx.YES


def icMsgBox(title='', prompt_text='', **kwargs):
    """
    Вывод сообщения.
    @param parent: Родительское окно.
    @param title: Заголовок диалогового окна.
    @param prompt_text: Текст диалога.
    @return: Код нажатой кнопки (Например: wx.YES или wx.NO).
    """
    try:
        return wx.MessageBox(prompt_text, title, style=wx.OK, **kwargs)
    except:
        log.fatal()


def icErrBox(title='', prompt_text='', **kwargs):
    """
    Вывод сообщения об ошибке.
    @param parent: Родительское окно.
    @param title: Заголовок диалогового окна.
    @param prompt_text: Текст диалога.
    @return: Код нажатой кнопки (Например: wx.YES или wx.NO).
    """
    try:
        return wx.MessageBox(prompt_text, title, style=wx.OK | wx.ICON_ERROR, **kwargs)
    except:
        log.fatal()


def icFatalBox(title='', prompt_text='', **kwargs):
    """
    Вывод сообщения об ошибке вместе с Traceback.
    @param parent: Родительское окно.
    @param title: Заголовок диалогового окна.
    @param prompt_text: Текст диалога.
    @return: Код нажатой кнопки (Например: wx.YES или wx.NO).
    """
    trace_txt = traceback.format_exc()
    txt = prompt_text + trace_txt
    return icErrBox(title, txt, **kwargs)


def icWarningBox(title='', prompt_text='', **kwargs):
    """
    Вывод сообщения об предупреждении.
    @param parent: Родительское окно.
    @param title: Заголовок диалогового окна.
    @param prompt_text: Текст диалога.
    @return: Код нажатой кнопки (Например: wx.YES или wx.NO).
    """
    try:
        return wx.MessageBox(prompt_text, title, style=wx.OK | wx.ICON_WARNING, **kwargs)
    except:
        log.fatal()


def icSingleChoiceDlg(parent=None, title='', prompt_text='', choices=[],
                      default_idx=-1):
    """
    Диалог выбора из списка.
    @param parent: Родительское окно.
    @param title: Заголовок диалогового окна.
    @param prompt_text: Текст диалога.
    @param choices: Список строк выбора.
    @param default_idx: Индекс строки, выбираемой по умолчанию.
        Если не указывается, то ничего по умолчанию не выбирает.
    @return: Выбранный текст или None, если нажата Cancel.
    """
    dlg = None
    win_clear = False
    try:
        if parent is None:
           parent = wx.Frame(None, -1, '')
           win_clear = True

        dlg = wx.SingleChoiceDialog(parent, prompt_text, title, choices, wx.CHOICEDLG_STYLE)
        if default_idx >= 0:
            dlg.SetSelection(default_idx)
        if dlg.ShowModal() == wx.ID_OK:
            txt = dlg.GetStringSelection()
            return txt

    finally:
        if dlg:
            dlg.Destroy()
        # Удаляем созданное родительское окно
        if win_clear:
            parent.Destroy()
    return None


def icSingleChoiceIdxDlg(parent=None, title='', prompt_text='', choices=[],
                         default_idx=-1):
    """
    Диалог выбора.
    @param parent: Родительское окно.
    @param title: Заголовок диалогового окна.
    @param prompt_text: Текст диалога.
    @param choices: Список выбора. Список строк.
    @param default_idx: Индекс строки, выбираемой по умолчанию.
        Если не указывается, то ничего по умолчанию не выбирает.
    @return: Выбранный индекс в списке выбора или -1, если нажата Cancel.
    """
    idx = -1
    dlg = None
    win_clear = False
    try:
        if parent is None:
           parent = wx.Frame(None, -1, '')
           win_clear = True

        dlg = wx.SingleChoiceDialog(parent, prompt_text, title,
                                    choices, wx.CHOICEDLG_STYLE)
        if default_idx >= 0:
            dlg.SetSelection(default_idx)

        if dlg.ShowModal() == wx.ID_OK:
            idx = dlg.GetSelection()
    finally:
        if dlg:
            dlg.Destroy()
        # Удаляем созданное родительское окно
        if win_clear:
            parent.Destroy()
    return idx


def icMultiChoiceDlg(parent=None, title='', prompt_text='', choices=()):
    """
    Диалог множественного выбора.
    @param parent: Родительское окно.
    @param title: Заголовок диалогового окна.
    @param prompt_text: Текст диалога.
    @param choices: Список выбора.Кортеж выбора в формате ((True/False,'Текст'),...).
    @return: Кортеж выбора в формате ((True/False,'Текст'),...).
    """
    dlg = None
    win_clear = False
    try:
        if parent is None:
           parent = wx.Frame(None, -1, '')
           win_clear = True

        choice_list = [row[1] for row in choices]
        dlg = wx.MultiChoiceDialog(parent, prompt_text, title, choice_list)
        # Установить выбор по умолчанию
        selections = [i for i, row in enumerate(choices) if row[0]]
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
            parent.Destroy()
    return None


class icProgressDlg(wx.ProgressDialog):
    """
    Класс диалогового окна прогресс бара.
    """

    def __init__(self, parent=None, title='', prompt_text='',
                 min_value=0, max_value=100, style=wx.PD_CAN_ABORT):
        """
        Конструктор. Создает и открывает прогресс бар.
        @param parent: Ссылка на окно.
        @param title: Заголовок диалогового окна.
        @param prompt_text: Текст диалога.
        @param min_value: Минимальное значение.
        @param max_value: Максимальное занчение.
        @param style: Стиль диалога.
        @return: Объект диалога.
        """
        # Атрибуты класса
        self._ProgressFrame = parent    # Фрейм прогресс бара
        self._MyFrame = False
        if self._ProgressFrame is None:
            self._ProgressFrame = wx.Frame(None, -1, '')
            self._MyFrame = True

        self._ProgressMIN = min_value    # Минимальное значение
        self._ProgressMAX = max_value    # Максимальное значение
        if self._ProgressMIN > self._ProgressMAX:
            tmp_value = self._ProgressMAX
            self._ProgressMAX = self._ProgressMIN
            self._ProgressMIN = tmp_value
        # Текущее значение счетчика
        self._current_value = 0
        try:
            # Вызов конструктор а предка
            wx.ProgressDialog.__init__(self, title, prompt_text,
                                       self._ProgressMAX - self._ProgressMIN,
                                       self._ProgressFrame, style | wx.PD_APP_MODAL)

            # Образмерить и отцентровать диалоговое окно
            self.SetSize(wx.Size(500, 130))
            self.CenterOnScreen()
        except:
            log.fatal(u'Ошибка создания диалогового окна прогресс-бара')

    def getMax(self):
        return self._ProgressMAX

    def getMin(self):
        return self._ProgressMIN

    def UpdateDlg(self, value=-1, new_prompt_text=''):
        """
        Обновить данные програсс бара.
        @param value: Значение.
        @param new_prompt_text: Текст диалога.
        """
        # Ограничение значения
        if value < self._ProgressMIN:
            value = self._ProgressMIN
        if value > self._ProgressMAX:
            value = self._ProgressMAX
        self.Update(value - self._ProgressMIN, new_prompt_text)

    def StepDlg(self, step_value=1, new_prompt_text=u''):
        """
        Обновить данные програсс бара с приращением.
        @param step_value: Значение приращения.
        @param new_prompt_text: Текст диалога.
        """
        self._current_value += step_value
        # Ограничение значения
        if self._current_value < self._ProgressMIN:
            self._current_value = self._ProgressMIN
        if self._current_value > self._ProgressMAX:
            self._current_value = self._ProgressMAX
        self.Update(self._current_value - self._ProgressMIN, new_prompt_text)

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


def icOpenProgressDlg(parent=None, title='', prompt_text='',
                      min_value=0, max_value=100, style=wx.PD_AUTO_HIDE):
    """
    Диалоговые функции прогресс бара.
    Создает и открывает прогресс бар.
    @param parent: Ссылка на окно.
    @param title: Заголовок диалогового окна.
    @param prompt_text: Текст диалога.
    @param min_value: Минимальное значение.
    @param max_value: Максимальное занчение.
    @param style: Стиль диалога.
    @return: Объект диалога.
    """
    try:
        global _PROGRESS_DLG
        _PROGRESS_DLG = icProgressDlg(parent, title, prompt_text, min_value, max_value, style)
    except:
        log.fatal(u'Ошибка открытия прогресс бара')
        _PROGRESS_DLG = None
    return _PROGRESS_DLG


def icUpdateProgressDlg(value=-1, new_prompt_text=''):
    """
    Диалоговые функции прогресс бара.
    Обновить данные програсс бара.
    @param value: Значение.
    @param new_prompt_text: Текст диалога.
    @return: Возвращает результат выполнения операции True/False.
    """
    try:
        global _PROGRESS_DLG
        if _PROGRESS_DLG is not None:
            _PROGRESS_DLG.UpdateDlg(value, new_prompt_text)
            return True
        return False
    except:
        log.fatal(u'Ошибка обновления прогресс бара')
        return False


def icStepProgressDlg(step_value=1, new_prompt_text=u''):
    """
    Диалоговые функции прогресс бара с приращением.
    Обновить данные програсс бара.
    @param step_value: Значение приращения.
    @param new_prompt_text: Текст диалога.
    @return: Возвращает результат выполнения операции True/False.
    """
    try:
        global _PROGRESS_DLG
        if _PROGRESS_DLG is not None:
            _PROGRESS_DLG.StepDlg(step_value, new_prompt_text)
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


def icStrComboBoxDlg(parent=None, title='', prompt_text='', choices=None, Default_=''):
    """
    Диалог выбора/редактирования строки.
    @param parent: Ссылка на окно.
    @param title: Заголовок диалогового окна.
    @param prompt_text: Текст диалога.
    @param choices: Список строк, позволяющих выбрать строку из уже существующих.
    @return: Строку введенную/выбранную пользователем.
    """
    dlg = None
    win_clear = False
    try:
        if choices is None:
            choices = []

        if parent is None:
           parent = wx.Frame(None, -1, '')
           win_clear = True

        dlg = icStrComboBoxDialog(parent, title, prompt_text, choices, Default_)
        if dlg.ShowModal() == wx.ID_OK:
            return dlg.GetEntryString()
        return Default_
    finally:
        if dlg:
            dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
            parent.Destroy()


class icStrComboBoxDialog(wx.Dialog):
    """
    Диалог выбора/редактирования строки.
    """
    def __init__(self, parent, title='', prompt_text='',
                 choices=None, default_value=''):
        """
        Конструктор.
        @param parent: Окно.
        @param title: Заголовок диалогового окна.
        @param prompt_text: Текст диалога.
        @param choices: Список строк, позволяющих выбрать строку из уже существующих.
        @param default_value: Значение по умолчанию.
        """
        try:
            if choices is None:
                choices = []

            wx.Dialog.__init__(self, parent, -1, title=title,
                               pos=wx.DefaultPosition, size=wx.Size(500, 150))

            self._text = wx.StaticText(self, -1, prompt_text, wx.Point(10, 10), wx.Size(-1, -1))
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
            self._combo_box = wx.ComboBox(self, 500, default_value, wx.Point(20, 30), wx.Size(460, -1),
                                          choices, wx.CB_DROPDOWN)
            # Редактируемая строка
            self._string = default_value
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


def icAboutDlg(parent=None, title='', prompt_text='', logo_bitmap=None):
    """
    О программе...
    @param parent: Ссылка на окно.
    @param title: Заголовок диалогового окна.
    @param prompt_text: Текст.
    @param logo_bitmap: Объект типа wx.Bitmap определяющий логотип.
    """
    dlg = None
    win_clear = False
    try:
        if parent is None:
           parent = wx.Frame(None, -1, '')
           win_clear = True

        dlg = icAboutDialog(parent, title, prompt_text, logo_bitmap)
        dlg.ShowModal()
    finally:
        if dlg:
            dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
           parent.Destroy()


class icAboutDialog(wx.Dialog):
    """
    Диалог 'О программе...'.
    """
    def __init__(self, parent, title='', prompt_text='', logo_bitmap=None):
        """
        Конструктор.
        @param parent: Окно.
        @param title: Заголовок диалогового окна.
        @param prompt_text: Текст.
        @param logo_bitmap: Объект типа wx.Bitmap определяющий логотип.
        """
        try:
            wx.Dialog.__init__(self, parent, -1, title=title,
                               pos=wx.DefaultPosition, size=wx.Size(500, 500))

            # Сайзер
            sizer = wx.BoxSizer(wx.VERTICAL)
            # Логотип
            self._logo = None
            if logo_bitmap is not None:
                self._logo = wx.StaticBitmap(self, -1, logo_bitmap, pos=wx.Point(10, 10))
                sizer.Add(self._logo, 10, wx.ALL, 5)
            # Текст
            self._text = wx.StaticText(self, -1, prompt_text)
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


def icLoginDlg(parent=None, title='', default_username='', reg_users=None):
    """
    Ввод пароля и имени пользователя.
    @param parent: Ссылка на окно.
    @param title: Заголовок диалогового окна.
    @param default_username: Имя пользователя заполняемое по умолчанию.
    @param reg_users: Список зарегестрированных пользователей.
    @return: Возвращает кортеж из 2-х строк.
        Первый элемент - пользхователь (LOGIN_USER_IDX).
        Второй элемент - пароль (LOGIN_PASSWORD_IDX).
    """
    dlg = None
    win_clear = False
    try:
        if parent is None:
            id_ = wx.NewId()
            parent = wx.Frame(None, id_, '')
            win_clear = True

        dlg = icLoginDialog(parent, title, default_username, reg_users)
        if dlg.ShowModal() == wx.ID_OK:
            result = (dlg.GetEntryUser(), dlg.GetEntryPassword(), dlg.GetEntryPasswordMD5())
            dlg.Destroy()
            # Удаляем созданное родительское окно
            if win_clear:
                parent.Destroy()
            return result
    finally:
        if dlg:
            dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
            parent.Destroy()
    return None


class icLoginDialog(wx.Dialog):
    """
    Диалоговое окно ввода пароля и имени пользователя.
    Диалог регистрации пользователя.
    """
    def __init__(self, parent_, title='', default_username='', reg_users=None):
        """
        Конструктор.
        @param parent_: Окно.
        @param title: Заголовок диалогового окна.
        """
        try:
            if not title:
                title = ''
                
            wx.Dialog.__init__(self, parent_, -1, title=title,
                               pos=wx.DefaultPosition, size=wx.Size(350, 150))

            from ic.PropertyEditor.images import editorimg
            icon_img = editorimg.shield.GetBitmap()
            if icon_img:
                icon = wx.Icon(icon_img)
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
            if reg_users is None:
                reg_users = []
            if default_username is None:
                default_username = ''
            self._user_edit = wx.ComboBox(self, id_,
                                          value=default_username,
                                          pos=(120, 10), size=(220, -1),
                                          choices=reg_users)
            id_ = wx.NewId()
            self._password_edit = wx.TextCtrl(self, id_, '',
                                              wx.Point(120, 40), wx.Size(220, -1),
                                              style=wx.TE_PASSWORD)

            self._user = default_username
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
        if key == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL)
        elif key == wx.WXK_RETURN:
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
        return hashlib.md5(self._password.encode()).hexdigest()


_BUSY_INFO = None


def BusyStart(prompt_text=''):
    """
    Занято/Ожидание.
    @param prompt_text: Текст диалога.
    """
    wx.BeginBusyCursor()    # Курсор
    global _BUSY_INFO
    if _BUSY_INFO is None:
        if prompt_text:
            _BUSY_INFO = wx.BusyInfo(prompt_text)  # Окно


def BusyStop():
    """
    Не занято.
    """
    global _BUSY_INFO
    if _BUSY_INFO:
        _BUSY_INFO = None
    wx.EndBusyCursor()  # Курсор


ic_wait_proccess_dlg = None


def WaitFunc(parent, prompt_text,
             function, function_args=(), function_kwargs={},
             img_frames=None):
    """
    Окно ожидания.
    @param parent: Ссылка на окно.
    @param prompt_text: Текст диалога.
    @param function: Функция, которую необходимо подождать.
    @param function_args: Аргументы функции.
    @param function_kwargs: Именованные аргументы функции.
    @param img_frames: Файлы-кадры.
    """
    global ic_wait_proccess_dlg
    
    wait_result = [None]
    if not img_frames:
        # Определить кадры по умолчанию
        wait_dir = os.path.join(os.path.dirname(__file__), 'Wait')
        img_frames = [wait_dir + 'Wait1.png',
                      wait_dir + 'Wait2.png',
                      wait_dir + 'Wait3.png',
                      wait_dir + 'Wait4.png',
                      wait_dir + 'Wait5.png',
                      wait_dir + 'Wait6.png',
                      wait_dir + 'Wait7.png',
                      wait_dir + 'Wait8.png',
                      wait_dir + 'Wait9.png',
                      wait_dir + 'Wait10.png',
                      wait_dir + 'Wait11.png',
                      wait_dir + 'Wait12.png',
                      wait_dir + 'Wait13.png',
                      wait_dir + 'Wait14.png',
                      wait_dir + 'Wait15.png']
    ic_wait_proccess_dlg = wait_box = icWaitBox(parent, prompt_text, img_frames)
    wait_box.SetResultList(wait_result)
    # Запустить функцию ожидания
    _thread.start_new(wait_box.Run, (function, function_args, function_kwargs))
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
    def __init__(self, parent, prompt_text, img_frames, style=0):
        """
        Конструктор.
        """
        if parent is None:
            style = wx.STAY_ON_TOP

        wx.Dialog.__init__(self, parent, -1, size=wx.Size(150, 34), style=style)

        from ic.bitmap import bmpfunc
        self._ani = [bmpfunc.createBitmap(frame_file_name) for frame_file_name in img_frames]
        self._cur_ani_state = 0     # Индекс состояния анимации
        self._max_ani_state = len(img_frames)
        self._delay = 0.3
        self._picture = wx.StaticBitmap(self, -1, self._ani[0])
        self._pic_size = (self._ani[0].GetWidth(), self._ani[0].GetHeight())
        self.msg = msg = wx.StaticText(self, -1, prompt_text)
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

    def SetResultList(self, result_list):
        self._result_list = result_list
        
    def NextState(self):
        """
        Сменить состояние.
        """
        self._cur_ani_state += 1
        if self._cur_ani_state >= self._max_ani_state:
            self._cur_ani_state = 0
        return self._cur_ani_state

    def DrawFrame(self, n_frame):
        """
        Отрисовка кадра.
        @param n_frame: Номер кадра.
        """
        frame_bmp = self._ani[n_frame]
        
        dc = wx.WindowDC(self._picture)
        # dc.BeginDrawing()
        dc.Clear()
        dc.DrawBitmap(frame_bmp, 0, 0, True)
        # dc.EndDrawing()
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

    def Run(self, function, function_args, function_kwargs):
        """
        Запуск ожидания функции.
        """
        self._running = True
        result = function(*function_args, **function_kwargs)
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
