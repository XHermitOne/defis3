#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль диалогового окна редактора паролей.
"""

# --- Подключение библиотек ---
import md5
import wx

from ic.kernel import io_prnt

from ic.dlg import ic_dlg
from ic.bitmap import ic_bmp

_ = wx.GetTranslation

# --- Функции ---


def icPasswordEditDlg(Win_=None, Prj_=None, Default_=None):
    """
    Редактор пароля.
    @param Win_: Ссылка на окно.
    @param Prj_: Объект проекта.
    @param Default_: Пароль по умолчанию.
    @return: Возвращает введенный пароль или None  в случае ошибки.
    """
    dlg = None
    try:
        win_clear = False
        if Win_ is None:
            id_ = wx.NewId()
            Win_ = wx.Frame(None, id_, '')
            win_clear = True

        dlg = icPasswordEditDialog(Win_, Prj_, Default_)
        if dlg.ShowModal() in (wx.ID_OK, wx.ID_CANCEL):
            result = dlg.getPasswordMD5()
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


class icPasswordEditPanel(wx.Panel):
    """
    Класс панели редактирования пароля.
    """

    def __init__(self, parent_, Prj_=None):
        """
        Конструктор.
        @param parent_: Окно.
        @param Prj_: Объект проекта.
        """
        try:
            # Сохранить объект проекта, для последующего использования
            self._Prj = Prj_
            
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
            
            self._password_md5 = None
        except:
            io_prnt.outErr(u'Ошибка создания объекта панели редактирования пароля')

    def SetPasswordMD5Default(self, PasswordMD5_):
        """
        Установить возвращаемое по умолчанию значение пароля md5.
        """
        self._password_md5 = PasswordMD5_

        
class icPasswordEditDialog(wx.Dialog):
    """
    Класс диалогового окна редактирования пароля.
    """

    def __init__(self, parent_, Prj_=None, Default_=None):
        """
        Конструктор.
        @param parent_: Окно.
        @param Prj_: Объект проекта.
        @param Default_: Пароль md5 по умолчанию.
        """
        try:
            _title = u'Определение пароля'
            
            pre = wx.PreDialog()
            pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
            pre.Create(parent_,-1, title=_title,
                       pos=wx.DefaultPosition, size=wx.Size(300, 200))

            # This next step is the most important, it turns this Python
            # object into the real wrapper of the dialog (instead of pre)
            # as far as the wxPython extension is concerned.
            self.PostCreate(pre)

            icon_img = ic_bmp.getSysImg('imgKey')
            if icon_img:
                icon = wx.IconFromBitmap(icon_img)
                self.SetIcon(icon)

            self._boxsizer = wx.BoxSizer(wx.VERTICAL)
            
            self._button_boxsizer = wx.BoxSizer(wx.HORIZONTAL)
            
            # Кнопка -OK-
            id_ = wx.NewId()
            self._ok_button = wx.Button(self, id_, u'OK', size=wx.Size(60, -1))
            self.Bind(wx.EVT_BUTTON, self.OnOK, id=id_)
            # Кнопка -Отмена-
            id_ = wx.NewId()
            self._cancel_button = wx.Button(self, id_, u'Отмена', size=wx.Size(60, -1))
            self.Bind(wx.EVT_BUTTON, self.OnCancel, id=id_)

            self._button_boxsizer.Add(self._cancel_button, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
            self._button_boxsizer.Add(self._ok_button, 0, wx.ALIGN_CENTRE | wx.ALL, 10)

            self._password_edit_panel = icPasswordEditPanel(self, Prj_)
            # Если надо то установить редатируемый список паспортов
            if Default_:
                self._password_edit_panel.SetPasswordMD5Default(Default_)
            
            self._boxsizer.Add(self._password_edit_panel, 1, wx.EXPAND | wx.GROW, 0)
            self._boxsizer.Add(self._button_boxsizer, 0, wx.ALIGN_RIGHT, 10)

            self.SetSizer(self._boxsizer)
            self.SetAutoLayout(True)
        except:
            io_prnt.outErr(u'Ошибка создания объекта диалогового окна редактирования пароля')
        
    def OnOK(self, event):
        """
        Обработчик нажатия кнопки -OK-.
        """
        password1_txt = self._password_edit_panel._password_edit1.GetValue()
        password2_txt = self._password_edit_panel._password_edit2.GetValue()
        password1_md5 = md5.new(password1_txt).hexdigest()
        password2_md5 = md5.new(password2_txt).hexdigest()
        if password1_md5 != password2_md5:
            ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                            u'Введенный пароль и подтверждение на совпадают. Введите еще раз.',
                            ParentWin_=self)
            self._password_edit_panel._password_edit1.SetValue('')
            self._password_edit_panel._password_edit2.SetValue('')
        else:
            if not password1_txt.strip():
                # Выбрана пустая строка
                self._password_edit_panel._password_md5 = md5.new('').hexdigest()
            else:
                self._password_edit_panel._password_md5 = password1_md5
            self.EndModal(wx.ID_OK)

    def OnCancel(self, event):
        """
        Обработчик нажатия кнопки -Отмена-.
        """
        self.EndModal(wx.ID_CANCEL)

    def getPasswordMD5(self):
        """
        Пароль.
        """
        return self._password_edit_panel._password_md5
