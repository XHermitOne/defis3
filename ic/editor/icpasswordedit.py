#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль диалогового окна редактора паролей.
"""

# --- Подключение библиотек ---
import hashlib
import wx

from ic.dlg import dlgfunc
from ic.bitmap import bmpfunc
from ic.log import log

__version__ = (0, 1, 1, 1)

_ = wx.GetTranslation


# --- Функции ---
def open_password_edit_dlg(parent=None, prj=None, default=None):
    """
    Редактор пароля.
    :param parent: Ссылка на окно.
    :param prj: Объект проекта.
    :param default: Пароль по умолчанию.
    :return: Возвращает введенный пароль или None  в случае ошибки.
    """
    dlg = None
    win_clear = False
    try:
        if parent is None:
            id_ = wx.NewId()
            parent = wx.Frame(None, id_, '')
            win_clear = True

        dlg = icPasswordEditDialog(parent, prj, default)
        if dlg.ShowModal() in (wx.ID_OK, wx.ID_CANCEL):
            result = dlg.getPasswordCrc()
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


class icPasswordEditPanel(wx.Panel):
    """
    Класс панели редактирования пароля.
    """

    def __init__(self, parent_, prj=None):
        """
        Конструктор.
        :param parent_: Окно.
        :param prj: Объект проекта.
        """
        try:
            # Сохранить объект проекта, для последующего использования
            self._Prj = prj
            
            wx.Panel.__init__(self, parent_, wx.NewId())

            self._boxsizer = wx.BoxSizer(wx.VERTICAL)

            self._label1 = wx.StaticText(self, wx.NewId(), _('Password:'))
            
            self._password_edit1 = wx.TextCtrl(self, wx.NewId(), '', style=wx.TE_PASSWORD)
            
            self._label2 = wx.StaticText(self, wx.NewId(), _('Repeat password:'))

            self._password_edit2 = wx.TextCtrl(self, wx.NewId(), '', style=wx.TE_PASSWORD)
            
            self._boxsizer.Add(self._label1, 0, wx.ALL | wx.EXPAND, 5)
            self._boxsizer.Add(self._password_edit1, 0, wx.ALL | wx.EXPAND, 5)
            self._boxsizer.Add(self._label2, 0, wx.ALL | wx.EXPAND, 5)
            self._boxsizer.Add(self._password_edit2, 0, wx.ALL | wx.EXPAND, 5)
            
            self.SetSizer(self._boxsizer)
            self.SetAutoLayout(True)
            
            self._password_crc = None
        except:
            log.fatal(u'Ошибка создания объекта панели редактирования пароля')

    def setPasswordCrcDefault(self, password_crc):
        """
        Установить возвращаемое по умолчанию значение пароля md5.
        """
        self._password_crc = password_crc

        
class icPasswordEditDialog(wx.Dialog):
    """
    Класс диалогового окна редактирования пароля.
    """

    def __init__(self, parent_, prj=None, default=None):
        """
        Конструктор.
        :param parent_: Окно.
        :param prj: Объект проекта.
        :param default: Пароль md5 по умолчанию.
        """
        try:
            _title = u'Определение пароля'
            
            wx.Dialog.__init__(self, parent_, -1, title=_title,
                               pos=wx.DefaultPosition, size=wx.Size(300, 200))

            icon_img = bmpfunc.getSysImg('imgKey')
            if icon_img:
                icon = wx.Icon(icon_img)
                self.SetIcon(icon)

            self._boxsizer = wx.BoxSizer(wx.VERTICAL)
            
            self._button_boxsizer = wx.BoxSizer(wx.HORIZONTAL)
            
            # Кнопка -OK-
            id_ = wx.NewId()
            self._ok_button = wx.Button(self, id_, u'OK', size=wx.Size(60, -1))
            self.Bind(wx.EVT_BUTTON, self.onOK, id=id_)
            # Кнопка -Отмена-
            id_ = wx.NewId()
            self._cancel_button = wx.Button(self, id_, u'Отмена', size=wx.Size(60, -1))
            self.Bind(wx.EVT_BUTTON, self.onCancel, id=id_)

            self._button_boxsizer.Add(self._cancel_button, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
            self._button_boxsizer.Add(self._ok_button, 0, wx.ALIGN_CENTRE | wx.ALL, 10)

            self._password_edit_panel = icPasswordEditPanel(self, prj)
            # Если надо то установить редатируемый список паспортов
            if default:
                self._password_edit_panel.setPasswordCrcDefault(default)
            
            self._boxsizer.Add(self._password_edit_panel, 1, wx.EXPAND | wx.GROW, 0)
            self._boxsizer.Add(self._button_boxsizer, 0, wx.ALIGN_RIGHT, 10)

            self.SetSizer(self._boxsizer)
            self.SetAutoLayout(True)
        except:
            log.error(u'Ошибка создания объекта диалогового окна редактирования пароля')
        
    def onOK(self, event):
        """
        Обработчик нажатия кнопки -OK-.
        """
        password1_txt = self._password_edit_panel._password_edit1.GetValue()
        password2_txt = self._password_edit_panel._password_edit2.GetValue()
        password1_md5 = hashlib.md5(password1_txt.encode()).hexdigest()
        password2_md5 = hashlib.md5(password2_txt.encode()).hexdigest()
        if password1_md5 != password2_md5:
            dlgfunc.openMsgBox(u'ВНИМАНИЕ!',
                            u'Введенный пароль и подтверждение на совпадают. Введите еще раз.',
                               ParentWin_=self)
            self._password_edit_panel._password_edit1.SetValue('')
            self._password_edit_panel._password_edit2.SetValue('')
        else:
            if not password1_txt.strip():
                # Выбрана пустая строка
                self._password_edit_panel._password_crc = hashlib.md5(b'').hexdigest()
            else:
                self._password_edit_panel._password_crc = password1_md5
            self.EndModal(wx.ID_OK)

    def onCancel(self, event):
        """
        Обработчик нажатия кнопки -Отмена-.
        """
        self.EndModal(wx.ID_CANCEL)

    def getPasswordCrc(self):
        """
        Пароль.
        """
        return self._password_edit_panel._password_crc
