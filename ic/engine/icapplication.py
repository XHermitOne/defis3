#!/usr/bin/env python3
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
import os
import os.path
import wx

from . import user_manager

from . import icpopupmenu
import ic.utils.resfunc
import ic.utils.resource

import ic.utils.filefunc
import ic.utils.ic_util
from ic.kernel import icexceptions
from ic.utils import lock  # Модуль необходим для удаления файлов-блокировок
import ic.imglib.common as imglib
from ic.dlg import dlgfunc
from . import icwxapplication
from ic.utils import ic_util
from ic.log import log

__version__ = (0, 1, 1, 1)


def getPrjSubSysDirs(prj_dirname):
    """
    Получить список директорий подсистем вместе с проектом.
    Заполнение списка происходит по файлу *.pro.
    @param prj_dirname: Папка проекта.
    """
    root_prj_dir = os.path.dirname(prj_dirname)
    pro_files = ic.utils.filefunc.getFilenamesByExt(prj_dirname, '.pro')
    if pro_files:
        pro_file = pro_files[0]
        prj = ic.utils.resfunc.ReadAndEvalFile(pro_file)
        return [sub_sys['__py__'] for sub_sys in prj]
    return []


def getSubSysDirs(prj_dirname):
    """
    Получить список директорий подсистем.
        Заполнение списка происходит по файлу *.pro.
    @param prj_dirname: Папка проекта.
    """
    root_prj_dir = os.path.dirname(prj_dirname)
    pro_files = ic.utils.filefunc.getFilenamesByExt(prj_dirname, '.pro')
    if pro_files:
        pro_file = pro_files[0]
        prj = ic.utils.resfunc.ReadAndEvalFile(pro_file)
        return [sub_sys['__py__'] for sub_sys in prj[1:]]
    return []


class icApp(icwxapplication.icWXApp):
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
        self._res_filename = ''
        # Имя ДВИЖКА
        self._Name = ''

        # Флаг включения/выключения движка вцелом
        self._Enabled = True
    
        # Пользователь
        self._User = None
        
        icwxapplication.icWXApp.__init__(self)

    def OnInit(self):
        """
        Функция инициализации.
        """
        # после создания обекта приложения надо инициализировать поддержку
        # других форматов недокументированной функцией wx.InitAllImageHandlers()
        # wx.InitAllImageHandlers()
        imglib.init_img()

        return True

    def OnExit(self):
        """
        Функция выхода из системы.
        """
        # Удалить корректно все объекты таблиц
        from ic.engine import glob_functions
        from ic.utils import resource
        
        lock.UnLockAllFile(glob_functions.getVar('LOCK_DIR'))
        # Сохраняем локальное хранилище настроек 
        resource.icCloseLocalStorage()
        
        # Завершить работу
        self._User.Logout()
        # Выполнение обработчика события при старте движка
        log.info(u'Выход из системы.')
        ic_util.print_defis_logo()
        return True

    def Stop(self):
        """
        Остановка ДВИЖКА.
        """
        if self._MainWindow is not None:
            # Закрыть само главное окно
            self._MainWindow.Close()
        return icwxapplication.icWXApp.Stop(self)
       
    def Login(self, username=None, password=None, db_mode='-s'):
        """
        Регистрация пользователя в системе.
        @param username: Имя пользователя.
        @param password: Пароль.
        @param db_mode: Режим использования БД.
        """
        from ic.engine import glob_functions

        ok = self._login_loop(username, password, db_mode)
        if ok:
            # self.run(self._User.getMainWinPsp(), self._User.getMenubarsPsp())
            # Удалить файлы блокировок при входе в систему
            lock.UnLockAllFile(glob_functions.getVar('LOCK_DIR'))
            return True

        # Удалить файлы блокировок при входе в систему
        lock.UnLockAllFile(glob_functions.getVar('LOCK_DIR'))
        
        return False

    def _login_loop(self, username=None, password=None, db_mode='-s'):
        """
        Цикл входа в систему.
        @param username: Имя пользователя.
        @param password: Пароль.
        @param db_mode: Режим использования БД.
        """
        login_ok = False
        login_manager = user_manager.icLoginManager()
        username, password = login_manager._getAutoLogin(username, password)
        bAuto = login_manager.isAutoAuth()
        while not login_ok:
            user_data = login_manager.Login(username, password, db_mode)
            if user_data is None:
                break
            user_name = user_data[dlgfunc.LOGIN_USER_IDX]
            user_password = user_data[dlgfunc.LOGIN_PASSWORD_IDX]
            user_password_md5 = user_data[dlgfunc.LOGIN_PASSWORD_MD5_IDX]
            res = login_manager.getUserResource(user_name)
            # Если пользователя с таким именем нет, просим пользователя еще раз ввести
            # логин и пароль
            if res is None:
                username, password = None, None
                dlgfunc.openMsgBox(u'Вход в систему', u'Неправильный пользователь или пароль. Доступ запрещен.')
            else:
                self._User = self.createObjBySpc(None, res)
                self._User.setLoginManager(login_manager)
                try:
                    login_ok = self._User.Login(user_name, user_password, db_mode, bAutoLogin=bAuto)
                except icexceptions.LoginInvalidException:
                    bAuto = False
                    username, password = None, None
            
        return login_ok

    def run(self, mainwin_psp=None, menubars_psp=None):
        """
        Запуск движка.
        @param mainwin_psp: Паспорт главного окна.
        @param menubars_psp: Список паспортов горизонтальных меню.
        @return: Возвращает True, если все OK иначе - False.
        """
        if mainwin_psp is None:
            mainwin_psp = self._User.getMainWinPsp()
        if menubars_psp is None:
            menubars_psp = self._User.getMenubarsPsp()
        return self._run(mainwin_psp, menubars_psp)

    def _run(self, mainwin_psp=None, menubars_psp=None):
        """
        Запуск движка.
        @param mainwin_psp: Паспорт главного окна.
        @param menubars_psp: Список паспортов горизонтальных меню.
        @return: Возвращает True, если все OK иначе - False.
        """
        # Проинициализировать внутренние данные
        self._MainMenu = None
        self._MainWindow = None

        # --- Создание главного окна ---
        if mainwin_psp:
            try:
                self._MainWindow = self.Create(mainwin_psp)
                self._MainWindow.showSplash()
                self._MainWindow.Enable(self._Enabled)
            except:
                log.error(u'Ошибка создания главного окна системы. Паспорт: <%s> тип паспорта: <%s>' % (mainwin_psp,
                                                                                                        type(mainwin_psp)))
                return False
        else:
            log.warning(u'Не определено окно в ресурсном описании пользователя')
            return False
        
        # --- Создание главного меню ---
        # С главном окне м.б. отключено создание главного меню
        if self._MainWindow.is_menubar:
            self._createMainMenu(menubars_psp)
            
            # --- Установить расположение меню ---
        
            if self._MainWindow and self._MainMenu:
                self._MainWindow.setMenuBar(self._MainMenu)
            
        # --- Показать окно ---
        self._MainWindow.OpenWin()
        self.SetTopWindow(self._MainWindow)
        return True

    def _createMainMenu(self, menubars_psp):
        """
        Создание/Сборка главного горизонтального меню.
        @param menubars_psp: Список паспортов линеек горизонтальных меню для сборки.
        """
        # Сборка полного ресурса линейки горизонтального меню
        menubar_res = None
        for menubar_psp in menubars_psp:
            if menubar_psp:
                if menubar_res is None:
                    menubar_res = self.getResByPsp(menubar_psp)
                else:
                    ext_menubar_res = self.getResByPsp(menubar_psp)
                    menubar_res['child'] += ext_menubar_res['child']
            else:
                log.warning(u'Не определен паспорт горизонтального меню')

        # Создание объекта линейки горизонтального меню по собранному ресурсу
        menubar = self.createObjBySpc(parent=self._MainWindow, res=menubar_res)

        if self._MainMenu is None:
            self._MainMenu = menubar
        return self._MainMenu

    def loadPopupMenu(self, name, owner):
        """
        Загрузка всплывающих меню в системе должна производится ч/з эту функцию для последующего доступа объектов к этим менюхам.
        @param name: имя всплывающего меню.
        @param owner: объект-хозяин, к которому прикрепляется меню.
        @return: Возвращает ссылку на объект всплывающего меню.
        """
        popup = icpopupmenu.CreateICPopupMenu(owner, name, self._res_filename)
        # Зарегистрировать его
        if popup is not None:
            self._PopupMenus.append(popup) 
        return popup

    # --- Функции-свойства ---

    def getMainWin(self):
        return self._MainWindow

    def getToolBars(self):
        return self._ToolBars

    def getToolBar(self, name):
        for toolbar in self._ToolBars:
            if toolbar.GetAlias() == name:
                return toolbar
        return None

    def getPopupMenus(self):
        return self._PopupMenus

    def getPopupMenu(self, name):
        for popup in self._PopupMenus:
            if popup.GetAlias() == name:
                return popup
        return None

    def setEnabled(self, Enabled_):
        self._Enabled = Enabled_
        if self._MainWindow is not None:
            self._MainWindow.Enable(self._Enabled)

    def getEnabled(self):
        return self._Enabled

    def getResFilename(self):
        return self._res_filename

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
