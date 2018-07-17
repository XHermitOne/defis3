#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль описания класса ПРИЛОЖЕНИЯ.

@type SPC_IC_APP: C{dictionary}
@var SPC_IC_APP: Спецификация на ресурсное описание компонента icApp.
Описание ключей SPC_IC_APP:
    - B{name = 'main_win'}: Паспорт-идентификатор окна.
    - B{name = 'menubar'}: Паспорт-идентификатор главного меню.
    - B{name = 'on_startup'}: Скрипт, выполняемый при запуске.
    - B{name = 'on_stop'}: Скрипт, выполняемый при остановке.
    - B{name = 'behaviour'}: Ресурс, описывающий поведение системы.
"""

# --- Подключение пакетов ---
import wx

from . import ic_win
from . import icUser

from . import ic_popup 
import ic.utils.ic_res
import ic.utils.resource

import ic.utils.ic_file
import ic.utils.ic_util
from ic.kernel import io_prnt
from ic.kernel import icexceptions
from ic.utils import lock  # Модуль необходим для удаления файлов-блокировок
import ic.imglib.common as imglib
import ic.dlg.ic_dlg as ic_dlg
from . import ic_app
from ic.utils import ic_util


def GetPrjSubSysDirs(PrjDir_):
    """
    Получить список директорий подсистем вместе с проектом.
    Заполнение списка происходит по файлу *.pro.
    @param PrjDir_: Папка проекта.
    """
    root_prj_dir = ic.utils.ic_file.DirName(PrjDir_)
    pro_files = ic.utils.ic_file.GetFilesByExt(PrjDir_, '.pro')
    if pro_files:
        pro_file = pro_files[0]
        prj = ic.utils.ic_res.ReadAndEvalFile(pro_file)
        return [sub_sys['__py__'] for sub_sys in prj]
    return []


def GetSubSysDirs(PrjDir_):
    """
    Получить список директорий подсистем.
        Заполнение списка происходит по файлу *.pro.
    @param PrjDir_: Папка проекта.
    """
    root_prj_dir = ic.utils.ic_file.DirName(PrjDir_)
    pro_files = ic.utils.ic_file.GetFilesByExt(PrjDir_, '.pro')
    if pro_files:
        pro_file = pro_files[0]
        prj = ic.utils.ic_res.ReadAndEvalFile(pro_file)
        return [sub_sys['__py__'] for sub_sys in prj[1:]]
    return []


class icApp(ic_app.icWXApp):
    """
    Класс приложения(ДВИЖКА СИСТЕМЫ).
    """

    def __init__(self):
        """
        Конструктор.
        """

        # Главное меню
        self._MainMenu = None
        # Главное окно
        self._MainWindow = None
        # Основной сайзер размещения меню системы
        self._MainSizer = None
        
        # Имя файла ресурса
        self._ResFile = ''
        # Имя ДВИЖКА
        self._Name = ''

        # Флаг включения/выключения движка вцелом
        self._Enabled = True
    
        # Пользователь
        self._User = None
        
        ic_app.icWXApp.__init__(self)

    def OnInit(self):
        """
        Функция инициализации.
        """
        # после создания обекта приложения надо инициализировать поддержку
        # других форматов недокументированной функцией wx.InitAllImageHandlers()
        # wx.InitAllImageHandlers()
        imglib.img_init()

        return True

    def OnExit(self):
        """
        Функция выхода из системы.
        """
        # Удалить корректно все объекты таблиц
        from ic.engine import ic_user
        from ic.utils import resource
        
        lock.UnLockAllFile(ic_user.icGet('LOCK_DIR'))
        # Сохраняем локальное хранилище настроек 
        resource.icCloseLocalStorage()
        
        # Завершить работу
        self._User.Logout()
        # Выполнение обработчика события при старте движка
        io_prnt.outLog(u'Выход из системы.')
        ic_util.print_defis_logo()
        return True

    def Stop(self):
        """
        Остановка ДВИЖКА.
        """
        if self._MainWindow is not None:
            # Закрыть само главное окно
            self._MainWindow.Close()
        return ic_app.icWXApp.Stop(self)
       
    def Login(self, User_=None, Password_=None, DBMode_='-s'):
        """
        Регистрация пользователя в системе.
        @param User_: Имя пользователя.
        @param Password_: Пароль.
        @param DBMode_: Режим использования БД.
        """
        from ic.engine import ic_user

        ok = self._login_loop(User_, Password_, DBMode_)
        if ok:
            # self.run(self._User.getMainWinPsp(), self._User.getMenubarsPsp())
            # Удалить файлы блокировок при входе в систему
            lock.UnLockAllFile(ic_user.icGet('LOCK_DIR'))
            return True

        # Удалить файлы блокировок при входе в систему
        lock.UnLockAllFile(ic_user.icGet('LOCK_DIR'))
        
        return False

    def _login_loop(self, User_=None, Password_=None, DBMode_='-s'):
        """
        Цикл входа в систему.
        @param User_: Имя пользователя.
        @param Password_: Пароль.
        @param DBMode_: Режим использования БД.
        """
        login_ok = False
        login_manager = icUser.icLoginManager()
        User_, Password_ = login_manager._getAutoLogin(User_, Password_)
        bAuto = login_manager.IsAutoAuth()
        while not login_ok:
            user_data = login_manager.Login(User_, Password_, DBMode_)
            if user_data is None:
                break
            user_name = user_data[ic_dlg.LOGIN_USER_IDX]
            user_password = user_data[ic_dlg.LOGIN_PASSWORD_IDX]
            user_password_md5 = user_data[ic_dlg.LOGIN_PASSWORD_MD5_IDX]
            res = login_manager.GetUserResource(user_name)
            # Если пользователя с таким именем нет, просим пользователя еще раз ввести
            # логин и пароль
            if res is None:
                User_, Password_ = None, None
                ic_dlg.icMsgBox(u'Вход в систему', u'Неправильный пользователь или пароль. Доступ запрещен.')
            else:
                self._User = self.createObjBySpc(None, res)
                self._User.setLoginManager(login_manager)
                try:
                    login_ok = self._User.Login(user_name, user_password, DBMode_, bAutoLogin=bAuto)
                except icexceptions.LoginInvalidException:
                    bAuto = False
                    User_, Password_ = None, None
            
        return login_ok

    def run(self, MainWinPsp_=None, MenuBarsPsp_=None):
        """
        Запуск движка.
        @param MainWinPsp_: Паспорт главного окна.
        @param MenuBarsPsp_: Список паспортов горизонтальных меню.
        @return: Возвращает True, если все OK иначе - False.
        """
        if MainWinPsp_ is None:
            MainWinPsp_ = self._User.getMainWinPsp()
        if MenuBarsPsp_ is None:
            MenuBarsPsp_ = self._User.getMenubarsPsp()
        return self._run(MainWinPsp_, MenuBarsPsp_)

    def _run(self, MainWinPsp_=None, MenuBarsPsp_=None):
        """
        Запуск движка.
        @param MainWinPsp_: Паспорт главного окна.
        @param MenuBarsPsp_: Список паспортов горизонтальных меню.
        @return: Возвращает True, если все OK иначе - False.
        """
        # Проинициализировать внутренние данные
        self._MainMenu = None
        self._MainWindow = None

        # --- Создание главного окна ---
        if MainWinPsp_:
            try:
                self._MainWindow = self.Create(MainWinPsp_)
                self._MainWindow.showSplash()
                self._MainWindow.Enable(self._Enabled)
            except:
                io_prnt.outErr(u'Ошибка создания главного окна системы. Паспорт: <%s> тип паспорта: <%s>' % (MainWinPsp_,
                                                                                                             type(MainWinPsp_)))
                return False
        else:
            io_prnt.outWarning(u'Не определено окно в ресурсном описании пользователя')
            return False
        
        # --- Создание главного меню ---
        # С главном окне м.б. отключено создание главного меню
        if self._MainWindow.is_menubar:
            self._createMainMenu(MenuBarsPsp_)
            
            # --- Установить расположение меню ---
        
            if self._MainWindow and self._MainMenu:
                self._MainWindow.setMenuBar(self._MainMenu)
            
        # --- Показать окно ---
        self._MainWindow.OpenWin()
        self.SetTopWindow(self._MainWindow)
        return True

    def _createMainMenu(self, MenuBarsPsp_):
        """
        Создание/Сборка главного горизонтального меню.
        """
        for menubar_psp in MenuBarsPsp_:
            if menubar_psp:
                menubar = self.Create(menubar_psp, parent=self._MainWindow)
                if self._MainMenu is None:
                    self._MainMenu = menubar
                else:
                    self._MainMenu.appendMenuBar(menubar)
            else:
                io_prnt.outWarning(u'Не определено горизонтальное меню')
        return self._MainMenu

    def LoadPopupMenu(self, Name_, Owner_):
        """
        Загрузка всплывающих меню в системе должна производится ч/з эту функцию для последующего доступа объектов к этим менюхам.
        @param Name_: имя всплывающего меню.
        @param Owner_: объект-хозяин, к которому прикрепляется меню.
        @return: Возвращает ссылку на объект всплывающего меню.
        """
        popup = ic_popup.CreateICPopupMenu(Owner_, Name_, self._ResFile)
        # Зарегистрировать его
        if popup is not None:
            self._PopupMenus.append(popup) 
        return popup

    # --- Функции-свойства ---

    def GetMainWin(self):
        return self._MainWindow

    def GetToolBars(self):
        return self._ToolBars

    def GetToolBar(self, Name_):
        for toolbar in self._ToolBars:
            if toolbar.GetAlias() == Name_:
                return toolbar
        return None

    def GetPopupMenus(self):
        return self._PopupMenus

    def GetPopupMenu(self, Name_):
        for popup in self._PopupMenus:
            if popup.GetAlias() == Name_:
                return popup
        return None

    def SetEnabled(self, Enabled_):
        self._Enabled = Enabled_
        if self._MainWindow is not None:
            self._MainWindow.Enable(self._Enabled)

    def GetEnabled(self):
        return self._Enabled

    def GetResFile(self):
        return self._ResFile

    def getName(self):
        return self._Name

    def getUser(self):
        """
        Объект пользователя по управления доступом к ресурсам системы.
        """
        return self._User


def test():
    """
    Функция тестирования пакета движка системы
    """
    app = icApp()

    app.run(['resource.mnu'], ['r1'])
    # Запустить основной цикл
    app.MainLoop()


if __name__ == '__main__':
    test()
