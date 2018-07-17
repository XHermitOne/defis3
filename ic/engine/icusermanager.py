#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Менеджер управления пользователями системы.
"""


# --- Imports ---

import wx
import ic
from ic.bitmap import ic_bmp
from ic.kernel import io_prnt
from ic.dlg import ic_dlg
from ic.utils import ic_file
from ic.utils import util
from ic.utils import ic_res
from ic.utils import ini

from ic.engine import icusereditpanel

from ic.engine import ic_user

# Version
__version__ = (0, 0, 1, 2)


def runEditDlg():
    """
    Функция запуска на редактирование менеджера пользователей.
    """
    user_mngr = icUserManager()
    user_mngr.Edit()


class icUserEditDialog(wx.Dialog):
    """
    Диалоговое окно редактора пользователей.
    """

    def __init__(self, parent, UserRes_, Manager_=None):
        """
        Конструктор.
        """
        # менеджер управления файлами ресурса пользователя.
        self._manager = Manager_
        try:
            pre = wx.PreDialog()
            pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
            pre.Create(parent, -1,
                       title=u'Управление пользователями',
                       pos=wx.DefaultPosition, size=wx.Size(700, 350),
                       style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

            # This next step is the most important, it turns this Python
            # object into the real wrapper of the dialog (instead of pre)
            # as far as the wxPython extension is concerned.
            self.PostCreate(pre)

            from ic.imglib import newstyle_img
            icon_img = newstyle_img.getusers7Bitmap()
            if icon_img:
                icon = wx.IconFromBitmap(icon_img)
                self.SetIcon(icon)

            self._boxsizer = wx.BoxSizer(wx.VERTICAL)

            self._button_boxsizer = wx.BoxSizer(wx.HORIZONTAL)

            id_ = wx.NewId()
            self._ok_button = wx.Button(self, id_, u'OK', size=wx.Size(-1, -1))
            self.Bind(wx.EVT_BUTTON, self.OnOK, id=id_)

            id_ = wx.NewId()
            self._cancel_button = wx.Button(self, id_, u'Отмена', size=wx.Size(-1, -1))
            self.Bind(wx.EVT_BUTTON, self.OnCancel, id=id_)

            self._button_boxsizer.Add(self._ok_button, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
            self._button_boxsizer.Add(self._cancel_button, 0, wx.ALIGN_CENTRE | wx.ALL, 10)

            self._edit_panel_iface = icusereditpanel.icUserEditPanel(self)
            self._edit_panel = self._edit_panel_iface.getPanel()
            if self._manager:
                self.setManager(self._manager)
            self._edit_panel_iface.setData(UserRes_)

            self._boxsizer.Add(self._edit_panel, 1, wx.EXPAND | wx.GROW, 0)
            self._boxsizer.Add(self._button_boxsizer, 0, wx.ALIGN_RIGHT, 10)

            self.SetSizer(self._boxsizer)
            self.SetAutoLayout(True)
        except:
            io_prnt.outErr(u'Ошибка создания диалогового окна редактирования пользователей.')

    def OnOK(self, event):
        """
        Нажатие кнопки <ОК>.
        """
        self._edit_panel_iface.refreshData()
        self.EndModal(wx.ID_OK)

    def OnCancel(self, event):
        """
        Нажатие кнопки <Отмена>.
        """
        self._edit_panel_iface.setData()
        self.EndModal(wx.ID_CANCEL)

    def getData(self):
        """
        Получить отредактированные данные.
        """
        return self._edit_panel_iface.getData()

    def setManager(self, Manager_):
        """
        Установить менеджер управления файлами ресурса пользователя.
        """
        self._manager = Manager_
        # И установить менеджер у дочерних объектов
        self._edit_panel_iface.setManager(Manager_)


class icUserManager(object):
    """
    Менеджер управления пользователями системы.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        # Роли текущего проекта
        self._roles = None

    def Edit(self, parent=None, bRefreshPrj=True, path=None):
        """
        Открыть окно редактирования пользователей.
        """
        # Если ресурс уже не заблокирован
        rl = ic.resource_loader
        path = path or ic_user.icGet('PRJ_DIR')+'/users.acc'
        if not rl.is_lock_res(path):
            # Заблокировать ресурс
            # bAdd=False - признак того, что запись о блокировки при отсутствии объекта
            # добавлять не надо
            rl.lock_res(path)
            # Прочитать ресурс
            users_res = rl.load_res(path, bRefresh=True)

            result = self._edit(parent or ic_user.getMainWin(), users_res)
            if result is not None:
                # Если нажата <ОК>, то сохранить файл ресурсов
                rl.save_res(path, result)
                rl.save_file_res(path, result)
            # Снять блокировку
            rl.unlock_res(path)

            # Сохранить проект, для того чтобы дерево проекта обновилось
            # в режиме редактирования/конфигурирования
            if bRefreshPrj:
                self.refreshPrj()
        else:
            # Если ресурс заблокировн, то сообщить кем
            lock_rec = rl.get_lock_rec(path)
            ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                            u'Пользователи в настоящее время редактируются пользователем %s на компьютере %s' % (lock_rec['user'], lock_rec['computer']))

    def refreshPrj(self):
        """
        Обновить дерево проекта.
        """
        kernel = ic_user.getKernel()
        if kernel:
            prj_manager = kernel.getProjectResController()
            prj_manager.refreshPrj()

    def lockUserRes(self):
        """
        Блокировка ресурса пользователей.
        """
        return ic_res.lockRes(None, 'users', 'acc')

    def unlockUserRes(self):
        """
        Разблокировка ресурса пользователей.
        """
        return ic_res.unlockRes(None, 'users', 'acc')

    def _edit(self, ParentForm_=None, UserRes_=None):
        """
        Открыть окно редактирования пользователей.
        @param ParentForm_: Родительское окно.
        @param UserRes_: Структура, описывающая ползователей.
        """
        dlg = None
        result = None
        try:
            clear = False
            if ParentForm_ is None:
                id_ = wx.NewId()
                ParentForm_ = wx.Frame(None, id_, '')
                clear = True
            dlg = icUserEditDialog(ParentForm_, UserRes_, Manager_=self)
            if dlg.ShowModal() == wx.ID_OK:
                result = dlg.getData()
                dlg.Destroy()
                if clear:
                    ParentForm_.Destroy()
                return result
        except:
            io_prnt.outErr(u'Ошибка редактирования пользователей.')
        finally:
            if dlg:
                dlg.Destroy()

            if clear:
               ParentForm_.Destroy()

        return None

    def getRoles(self):
        """
        Роли проекта.
        """
        if self._roles is None:
            self._roles = self.readRoles(isSort_=True)
        return self._roles

    def readRoles(self, PrjDir_=None, isSort_=False):
        """
        Чтение ролей из папки проекта.
        @param PrjDir_: Папка проекта.
        @param isSort_: Сортировать роли по имени?
        """
        if PrjDir_ is None:
            PrjDir_ = ic_user.icGet('PRJ_DIR')
        role_files = ic_file.GetFilesByExt(PrjDir_, '.rol')
        # Отфильтровать pickle файлы
        role_files = [role_file for role_file in role_files if role_file[-8:].lower() != '_pkl.rol']

        result = []
        for role_file in role_files:
            role_data = util.readAndEvalFile(role_file)
            role_spc = role_data[role_data.keys()[0]]
            role_name = role_spc['name']
            role_description = role_spc.get('description', u'') or u''
            result.append((role_name, role_description))
        if isSort_:
            result.sort()
        return result

    def unregisterUser(self, CurDirPrj_=None):
        """
        Сброс блокирующих записей пользователей при некорректном завершении программы.
        @param CurDirPrj_: Текущая папка проекта.
        """
        try:
            if CurDirPrj_ is None:
                CurDirPrj_ = ic_file.getCurDirPrj()
            reg_user_journal_file_name = CurDirPrj_+'/log/reg_user_journal.ini'
            if ic_file.Exists(reg_user_journal_file_name):
                reg_user_journal = ini.INI2Dict(reg_user_journal_file_name)
                if reg_user_journal and 'CURRENT_USERS' in reg_user_journal:
                    users = [(True, usr) for usr in reg_user_journal['CURRENT_USERS'].keys()]
                    parent_win = ic_user.getMainWin()
                    selected_users = ic_dlg.icMultiChoiceDlg(parent_win,
                                                             u'Зарегистрированные пользователи',
                                                             u'Снятие регистрации пользователей',
                                                             tuple(users))
                    if selected_users:
                        for is_select, usr in selected_users:
                            if not is_select:
                                del reg_user_journal['CURRENT_USERS'][usr]
                        if not reg_user_journal['CURRENT_USERS']:
                            del reg_user_journal['CURRENT_USERS']
                        print(reg_user_journal)
                        # Сохранить изменения
                        return ini.Dict2INI(reg_user_journal,
                                            reg_user_journal_file_name, rewrite=True)
        except:
            io_prnt.outErr(u'Ошибка в функции управления регистрационной информацией пользователей.')
        return False


def test():
    """
    Функция тестиорвания.
    """
    from ic.components.user import ic_postgres_wrp as src
    prj_dir = 'C:/defis/Registr/Registr'
    res = {'admin': {'activate': 1, 'obj_module': None, 'runner': u"['work_runner']",
                     'legacy': None, 'on_login': u'', 'run_res': u"['work_runner.mnu']",
                     'style': 0, 'group': None, 'component_module': None, 'on_logout': None,
                     'access': [],
                     'menubars': [(('MenuBar', 'test_work_menu', None, 'test_work_menu.mnu', 'work_flow'),)],
                     'local_dir': None, 'type': u'User', 'res_module': None, 'description': None,
                     '_uuid': '551d580195e320ef56350e94f0542250', 'password': u'd41d8cd98f00b204e9800998ecf8427e',
                     'lock_time': ([], [], [], [], [], [], []), 'name': u'admin',
                     'roles': ['administrators'], 'alias': None, 'init_expr': None,
                     'main_win': (('MainWindow', 'work_main_win', None, 'work_main_win.win', 'work_flow'),)},
           u'tester': {'activate': 1, 'obj_module': None, 'on_login': None, 'style': 0, 'group': None,
                       'on_logout': None, 'menubars': [], 'local_dir': u'./#WRK', 'type': 'User',
                       'res_module': None, 'description': None, '_uuid': 'd900ff7aee13ed8f9c55b6e82d26b86f',
                       'component_module': None, 'password': u'd41d8cd98f00b204e9800998ecf8427e',
                       'lock_time': [[], [], [], [], [], [], []], 'name': u'tester', 'roles': [],
                       'alias': None, 'init_expr': None, 'main_win': None}}

    app = wx.PySimpleApp()
    form = wx.Frame(None)

    if ic.Login('test', '', prj_dir):
        try:
            print(ic.resource_loader.dbstore)
            ic.resource_loader.save_res('c:\\defis\\Registr/Registr/users1.acc', res)
            res1 = ic.resource_loader.load_res('D:\\defis\Registr\\Registr/users1.acc')
            user_mngr = icUserManager()
            user_mngr.Edit(form, False)

            form.Show()
        except :
            io_prnt.outErr()
        finally:
            ic.Logout()
    app.MainLoop()


def testDlg():
    """
    Функция тестиорвания.
    """
    res = ic_user.getKernel()._User.getUsersResource()

    user_mngr = icUserManager()
    user_mngr._edit(ic_user.getMainWin(), res)


def testEditDlg():
    """
    Функция тестиорвания.
    """
    user_mngr = icUserManager()
    user_mngr.Edit()


def testUnregUser():
    user_mngr = icUserManager()
    user_mngr.unregisterUser()


if __name__ == '__main__':
    test()
