#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль класса главного узла дерева проекта.
"""

# Подключение библиотек
import wx
import sys
import os.path
import ic.imglib.common as imglib

from ic.log import log

import ic.utils.ic_file as ic_file
import ic.utils.ic_res as ic_res
import ic.dlg.ic_dlg as ic_dlg
from ic.kernel import icexceptions
from ic.utils import ic_util

import ic.engine.ic_user as ic_user
import ic.utils.ic_mode as ic_mode

from . import PrjRes
from . import menuRootNode
from . import ImpNode

from . import prj_env
from . import prj_report
from . import prj_security
from . import prj_resource
from . import prj_module
try:
    import winpdb
except:
    log.error(u'Winpdb import Error')

import shlex
import subprocess

_ = wx.GetTranslation

__version__ = (0, 0, 2, 2)

# Константы
# Файл журнала зарегистрированных пользователей
PRJ_REG_JRN_FILE_NAME = './log/prj_reg_user_journal.ini'


class PrjRoot(ImpNode.PrjImportSys):
    """
    Главный класс проекта.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        ImpNode.PrjImportSys.__init__(self, Parent_)
        self.img = imglib.imgEdtPrj
        self.description = u'Проект'
        self.name = 'new_prj'
        # Проект и является корнем
        self._root = self
        # Проект открыт?
        self._is_opened_prj = False
        
        # Ресурс проекта
        self.prj_res_manager = PrjRes.icPrjRes()
        # Папка блокировок
        self.lock_dir = None
        # Текущее время создания файла ресурса проекта (для синхронизации проектов)
        self.prj_res_time = 0
        # Текущий размер файла ресурса проекта (для синхронизации проектов)
        self.prj_res_size = 0
        
        # Признак того что надо отображать всплывающие подсказки о ресурсах, модулях
        # и компонентах
        self.show_popup_help = False
        
        # Сразу зарегестрировать этот объект в хранилище переменных
        if not ic_user.icIs('PRJ_ROOT') or ic_user.icGet('PRJ_ROOT') is None:
            ic_user.icLet('PRJ_ROOT', self)

        # Режим отладки
        self.debug_mode = ic_mode.isDebugMode()
        
        # Система разграничения прав доступа
        self._prj_user = None
        self.prj_security = None

    def exit(self):
        """
        Выход из проекта. Вызывается при закрытии IDE.
        """
        # Удалить все блокировки при выходе из редактора
        log.info('PROJECT EXIT')
        ic_util.print_defis_logo()

        kernel = ic_user.getKernel()
        if kernel:
            kernel.stop()
        self.logout()
        self.delMyLocks()
        
    def delMyLocks(self):
        """
        Удалить все блокировки.
        """
        # Удалить за собой все блокировки
        self.unlockResInResEditor()
        log.info(u'DELETE ALL PROJECT LOCKS <%s>' % self.lock_dir)
        if self.lock_dir:
            ic_res.delAllLockRes(self.lock_dir)
            
    def unlockResInResEditor(self, ResEditor_=None):
        """
        Разблокировать ресурс, который находится в редакторе ресурсов.
        @param ResEditor_: Редактор ресурса.
        """
        if ResEditor_ is None:
            ResEditor_ = self.getParent().res_editor
        if ResEditor_ is None:
            log.warning('Don\'t define Resource Editor')
            return False

        res_name = ResEditor_.GetResName()
        if res_name:
            res_file_name = ResEditor_.GetResFileName()
            if res_file_name:
                res_file_ext = os.path.splitext(os.path.basename(res_file_name))[1][1:]
                res_file_name = os.path.splitext(os.path.basename(res_file_name))[0]
                return ic_res.unlockRes(res_name, res_file_name,
                                        res_file_ext, self.lock_dir)
        return False

    def unlockPyFileInIDE(self, PyFileName_):
        """
        Разблокировать модуль.
        @param PyFileName_: Имя модуля.
        """
        ide = self.getParent().ide
        # Если файл не открыт в редакторе, то удалить блокировку
        if ide and not ide.IsOpenedFile(PyFileName_):
            py_file_name = os.path.splitext(os.path.basename(PyFileName_))[0]
            py_file_ext = 'py'
            package_name = os.path.basename(os.path.dirname(PyFileName_))
            log.debug('UNLOCK PY FILE <%s> is open - %s' % (PyFileName_, ide.GetAlreadyOpen()))
            return ic_res.unlockRes(py_file_name, package_name,
                                    py_file_ext, self.lock_dir)
        return False
        
    def unlockAllPyFilesInIDE(self):
        """
        Разблокировать все модули, не загруженные в редакторе.
        """
        modules = self.getModules()
        return modules.unlockAllPyFiles()
        
    def _install(self):
        """
        Действия, необходимые при инициализации проекта в редакторе.
        """
        # Добавить путь проекта в общую переменную путей поиска для
        # импорта модулей
        if self.getPrjFileName():
            prj_dir = os.path.dirname(self.getPrjFileName())
            ic_file.PATH.append(prj_dir)
        
    def Default(self):
        """
        Создать нужные папки по умолчанию.
        """
        self.description = u'Проект'
        self.prj_res_manager.newPrj(self.name, '')

        # Удалить все дочерние объекты
        self.children = []
        # и добавить по умолчанию
        self.addChild(prj_env.PrjEnv(self))
        self.prj_security = prj_security.PrjSecurity(self)
        self.addChild(self.prj_security)
        self.addChild(prj_report.PrjReports(self))
        resources = prj_resource.PrjResources(self)
        self.addChild(resources)

        db = resources.addChild(prj_resource.PrjResources(resources))
        db.name = u'БД'
        tables = resources.addChild(prj_resource.PrjResources(resources))
        tables.name = u'Таблицы'
        menus = resources.addChild(prj_resource.PrjResources(resources))
        menus.name = u'Меню'
        systems = resources.addChild(prj_resource.PrjResources(resources))
        systems.name = u'Системное'
        forms = resources.addChild(prj_resource.PrjResources(resources))
        forms.name = u'Формы'
        meta = resources.addChild(prj_resource.PrjResources(resources))
        meta.name = u'Метаданные'
        
        self.addChild(prj_module.PrjModules(self))
        self.addChild(ImpNode.PrjImportSystems(self))
        
        # По умолчанию создать дополнительные ресурсы
        self._newResources()

    def _newResources(self):
        """
        Создание ресурсов по умолчанию при создании проекта.
        """
        # 1. Создать пользователя
        security_node = self.children[1]
        security_node.createUser('admin')
        security_node.createRole('administrators')
        # 2. Создать главное окно
        frm_folder = self.getResources().getChild(u'Формы')
        win_node = prj_resource.PrjWinRes(frm_folder)
        win_node.template['name'] = win_node.name
        frm_folder.addChild(win_node)
        # 3. Сохранить созданные ресурсы
        win_node.save()
        security_node.save()
        return self.save()
        
    def onNodePopup(self,event):
        """
        Вызов всплывающего меню узла.
        """
        popup_menu = menuRootNode.icMenuRootNode(self)
        popup_menu.Popup(wx.GetMousePosition(), self._root.getParent())

    def _new_prj_init_file(self, PrjPath_):
        """
        Создать новый __init__.py файл проекта.
        """
        log.info(_('__init__.py is created in folder %s') % PrjPath_)
        return ic_file.icCopyFile(os.path.dirname(__file__)+'/prj__init__prototype.py',
                                  PrjPath_+'/__init__.py', False)
        
    def newPrj(self):
        """
        Новый проект.
        """
        tree_prj = self.getParent()
        dir_prj_file_name = ic_dlg.icDirDlg(tree_prj, _('Create project'))
        if dir_prj_file_name:
            prj_name = os.path.basename(dir_prj_file_name)
            new_prj_file_name = os.path.join(dir_prj_file_name, prj_name, prj_name+'.pro')
            # Установить имя проекта по имени файла
            self.name = os.path.splitext(os.path.split(new_prj_file_name)[1])[0]
            # Запомнить файл проекта
            self.prj_res_manager.setResFileName(new_prj_file_name)
            self.imp_prj_file_name = new_prj_file_name
            # Установить в дереве корень
            tree_prj = self.getParent()
            tree_prj.DeleteAllItems()
            # Закрыть все
            tree_prj.res_editor.CloseResource()
            if tree_prj.ide:
                tree_prj.ide.CloseFile(None)
            
            # Инициализировать по умолчанию
            self.Default()
            # определить папку блокировок не уровне выше
            self.lock_dir = os.path.dirname(os.path.dirname(new_prj_file_name))+'/lock'
            log.debug(u'Initilize LOCK DIR: <%s>' % self.lock_dir)
            self.delMyLocks()
            # и сразу сохранить
            ok = self.save()
            # НЕ СОЗДАВАТЬ ПАПКУ ПРОЕКТА ПАКЕТОМ
            # ИНАЧЕ НЕ ИМПОРТИРУЮТСЯ КОМПОНЕНТЫ!!!

            # Когда уже все определено сделать дополнительные
            # действия по инсталяции проекта в редакторе
            self._install()
            
            self.logout()
            # Определить окружение проекта
            ic_user.InitEnv(os.path.dirname(self.getPrjFileName()))
            self.login('admin', '')
            
            tree_prj.setRoot()
            return ok
        return False

    def _openDefault(self):
        """
        Инициализация основных узлов проекта при открытиии.
        """
        self.description = u'Проект'
        self.name = self.prj_res_manager.getPrjRootName()

        # Удалить все дочерние объекты
        self.children = []
        # и добавить по умолчанию
        self.addChild(prj_env.PrjEnv(self))
        self.prj_security = prj_security.PrjSecurity(self)
        self.prj_security.openUsers()
        self.prj_security.openRoles()
        self.addChild(self.prj_security)
        self.addChild(prj_report.PrjReports(self))
        self.addChild(prj_resource.PrjResources(self))
        self.addChild(prj_module.PrjModules(self))
        self.addChild(ImpNode.PrjImportSystems(self))

    def getResources(self):
        """
        Папка/узел ресурсов.
        """
        return self.children[3]

    def getModules(self):
        """
        Папка/узел функционала.
        """
        return self.children[4]

    def getImpSystems(self):
        """
        Папка/узел импортируемых подсистем.
        """
        return self.children[5]

    def getPrjSubsys(self, PrjFileName_):
        """
        Имя проекта и имя проекта, подсистемой которого он является.
        @param PrjFileName_: Имя файла проекта.
        @return: Кортеж (имя проекта, имя подсистемы).
        """
        prj_dir = os.path.dirname(PrjFileName_)
        subsys_name = os.path.basename(prj_dir)
        prj_name = os.path.basename(os.path.dirname(prj_dir))
        return prj_name, subsys_name
        
    def login(self, User_=None, Password_=None, prj_filename=None):
        """
        Открыть регистрацию программиста в режиме редактирования.
        @param User_: Имя пользователя.
        @param Password_: Пароль. Если имя или пароль не указаны, то выводится
        окно входа в систему.
        @param prj_filename: Имя файла проекта, который пытаемся открыть.
            Необходимо для снятия блокировки пользователя.
        """
        # ВНИМАНИЕ!
        # Меняется проект, меняется и файл ресурса ограничения доступа
        # поэтому объект управления правами пользователей необходимо
        # создавать каждый раз заново при открытии проекта
        result = False
        try:
            result = ic_user.getKernel().Login(User_, Password_)
        except icexceptions.LoginInvalidException:
            ic_dlg.icMsgBox(u'Вход в систему', u'Неправильный пользователь или пароль. Доступ запрещен.')
        except icexceptions.LoginErrorException:
            if ic_dlg.icAskBox(u'Вход в систему',
                               u'Пользователь уже зарегистрирован в системе. Снять регистрацию пользователя?'):
                from ic.engine import icusermanager
                user_mngr = icusermanager.icUserManager()
                tree_ctrl = self.getParent()
                pro_file_name = prj_filename
                if not os.path.exists(pro_file_name):
                    pro_file_name = ic_dlg.icFileDlg(tree_ctrl,
                                                     u'Удаление регистрационной информации о пользователе из проекта',
                                                     _('Project file (*.pro)|*.pro'))
                if pro_file_name:
                    prj_dir = os.path.dirname(os.path.dirname(pro_file_name))
                    if os.path.exists(prj_dir):
                        user_mngr.unregisterUser(prj_dir)
        except icexceptions.LoginDBExclusiveException:
            ic_dlg.icMsgBox(u'Вход в систему',
                            u'БД открыта в монопольном режиме другим пользователем. Вход в систему запрещен.')
        except icexceptions.LoginWorkTimeException:
            ic_dlg.icMsgBox(u'Вход в систему',
                            u'Попытка входа в систему в не регламентированное время пользователем. Вход в систему запрещен.')
        except:
            log.fatal(u'Ошибка регистрации пользователя')
            
        if result:
            from ic.kernel import icsettings
            icsettings.setProjectSettingsToEnvironment(self.name, ReDefine_=True)
        if result:
            self._prj_user = ic_user.getKernel().getUser()
        else:
            self._prj_user = None
            
        return result        
        
    def logout(self):
        """
        Закрыть регистрацию программиста в режиме редактирования.
        """
        if self._prj_user:
            self._prj_user.Logout()
            # Меняется проект, меняется и файл ресурса ограничения доступа
            self._prj_user = None
        
    def openPrj(self, PrjFileName_=None):
        """
        Открыть проект.
        """
        tree_prj = self.getParent()
        if PrjFileName_ is None:
            prj_file = ic_dlg.icFileDlg(tree_prj, _('Open project'),
                                        _('Project file (*.pro)|*.pro'))
        else:
            prj_file = PrjFileName_
            
        if prj_file and os.path.exists(prj_file):
            # Проверка тот ли мы проект загрузили
            prj_name, sub_sys_name = self.getPrjSubsys(prj_file)
            if prj_name != sub_sys_name:
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                                u'Load subsystem <%s> to project <%s>! After load all changes will lost. subsys: <%s>, project: <%s>!' % (sub_sys_name,
                                prj_name, sub_sys_name, prj_name), tree_prj)
            self.delMyLocks()   # Удалить блокировки из старого проекта
            self.logout()

            # Определить окружение проекта
            # ВНИМАНИЕ! При инициализации окружения после открытия в контексте ядра
            # должен отразиться актуальный проект------------------------------+
            # Иначе дерево проекта для выбора паспорта не обновляется          |
            # Поэтому явно задаем корень проекта в окружении                   v
            ic_user.InitEnv(ic_file.DirName(prj_file), PrjName=prj_name, PRJ_ROOT=self)
            
            # Регистрация программиста
            if not self.login(prj_filename=prj_file):
                return
            
            # Удалить все из дерева
            tree_prj.DeleteAllItems()
            # Закрыть все
            tree_prj.res_editor.CloseResource()
            if tree_prj.ide:
                tree_prj.ide.CloseFile(None)

            # Построить дерево узлов по ресурсному файлу
            self.prj_res_manager.openPrj(prj_file)
            self.imp_prj_file_name = prj_file
            self._openDefault()
            # Сохранить время и размер до следующей синхронизации
            self.prj_res_time = ic_file.GetMakeFileTime(prj_file)
            self.prj_res_size = ic_file.GetFileSize(prj_file)

            # определить папку блокировок
            self.lock_dir = ic_file.DirName(ic_file.DirName(prj_file))+'/lock'
            log.debug(u'Init LOCK DIR: <%s>' % self.lock_dir)
            self.delMyLocks()   # Удалить блокировки из вновь открытого проекта
            
            # Создание ресурсов
            for cur_res in self.prj_res_manager.getPrjRoot():
                self.buildPrjRes(self.getResources(),
                                 cur_res.values()[0], cur_res.keys()[0])

            # Создание дерева функционала
            self.getModules().buildPrjPy(os.path.dirname(prj_file))
            # Создание дерева импортируемых систем
            self.getImpSystems().buildSubSystemsTree(self.prj_res_manager.getImportSystems())

            # Когда уже все определено сделать дополнительные
            # действия по инсталяции проекта в редакторе
            self._install()

            # Обновить дерево пользовательских компонентов
            tree_prj.res_editor.InitObjectsInfo()
            # Установить в дереве корень
            tree_prj.setRoot(self)
            
            self._is_opened_prj = True
            
    def isOpened(self):
        """
        Открыт проект?
        """
        return self._is_opened_prj

    def buildPrjRes(self, CurFolder_, ResNode_,ResName_, FolderClass_=None):
        """
        Построение всех узлов/ресурсов проекта.
        @param CurFolder_: Текущая папка, в которую происходит добавление узлов.
        @param ResNode_: Ресурс, соответствующий этому узлу.
        @param ResName_: Имя ресурса, соответствующего этому узлу.
        @param FolderClass_: Класс папки проекта.
        @return: Корневой, добавляемый узел.
        """
        cur_node = None
        if isinstance(ResNode_, list):
            # Обработка папки
            if FolderClass_ is None:
                cur_node = prj_resource.PrjResources(CurFolder_)
            else:
                cur_node = FolderClass_(CurFolder_)
            # Установить имя
            cur_node.name = ResName_
            CurFolder_.addChild(cur_node)
            for cur_res in ResNode_:
                # Обработка подпапок
                self.buildPrjRes(cur_node, cur_res.values()[0],
                                 cur_res.keys()[0], FolderClass_)
        else:
            from . import prj_prototype
            res_node_typ = ResNode_.strip()
            if res_node_typ in prj_prototype.nodeReg.keys():
                # Взять класс из реестра узлов
                # и создать объект узла
                cur_node = prj_prototype.nodeReg[res_node_typ](CurFolder_)
                # Установить имя
                cur_node.name = ResName_
                # Добавить узел в папку
                CurFolder_.addChild(cur_node)
            else:
                log.warning(u'Invalid resource type <%s>' % res_node_typ)

        return cur_node
            
    def synchroPrj(self, Refresh_=False):
        """
        Синхронизация дерева проекта с изменениями другими программистами.
        @param Refresh_: указание принудительного обновления дерева проекта.
        """
        prj_file = self.getPrjFileName()
        if prj_file:
            cur_prj_res_time = ic_file.GetMakeFileTime(prj_file)
            cur_prj_res_size = ic_file.GetFileSize(prj_file)
            if (cur_prj_res_time != self.prj_res_time) or \
               (cur_prj_res_size != self.prj_res_size) or \
               Refresh_:
                # Нужно синхронизировать
                try:
                    # Удалить все из дерева
                    tree_prj = self.getParent()
                    tree_prj.DeleteAllItems()
    
                    # Построить дерево узлов по ресурсному файлу
                    self.prj_res_manager.openPrj(prj_file)
                    self._openDefault()

                    # Создание ресурсов
                    for cur_res in self.prj_res_manager.getPrjRoot():
                        self.buildPrjRes(self.getResources(),
                                         cur_res.values()[0], cur_res.keys()[0])
    
                    # Создание дерева функционала
                    self.getModules().buildPrjPy(os.path.dirname(prj_file))
                    # Создание дерева импортируемых систем
                    self.getImpSystems().buildSubSystemsTree(self.prj_res_manager.getImportSystems())
    
                    # Установить в дереве корень
                    tree_prj.setRoot(self)

                    # Сохранить время и размер до следующей синхронизации
                    self.prj_res_time = cur_prj_res_time
                    self.prj_res_size = cur_prj_res_size
                except:
                    log.error(u'Synhronization tree/file project error: <%s>' % self.name)

    def save(self):
        """
        Сохранить проект.
        """
        ok = self.prj_res_manager.savePrj()
        # Сохранить время и размер до следующей синхронизации
        self.prj_res_time = ic_file.GetMakeFileTime(self.getPrjFileName())
        self.prj_res_size = ic_file.GetFileSize(self.getPrjFileName())
        return ok

    def rename(self, OldName_, NewName_):
        """
        Переименование проекта.
        @param OldName_: Старое имя.
        @param NewName_: Новое имя.
        """
        old_prj_file_name = self.getRoot().getPrjFileName()
        self.name = NewName_
        self.prj_res_manager.prj_file_name = self.getRoot().getPrjFileName()
        self.prj_res_manager.setPrjRootName(NewName_)

        if os.path.exists(old_prj_file_name):
            # Если существовал старый файл проекта, то переименовать его
            os.rename(old_prj_file_name,self.getPrjFileName())
            
        # Для синхронизации дерева проекта
        self.getRoot().save()

    def getPrjFileName(self):
        """
        Генерация имени файла проекта.
        """
        if self.getRoot().prj_res_manager and self.getRoot().prj_res_manager.prj_file_name:
            return self.getRoot().prj_res_manager.prj_file_name.strip()
        return ''

    def getPath(self):
        """
        Путь.
        """
        prj_file_name = self.getPrjFileName()
        if prj_file_name:
            return ic_file.NormPathUnix(os.path.dirname(prj_file_name.strip()))
        return None
     
    def isPrjRoot(self):
        """
        Подсистема является проектом?
        """
        return True
    
    def getParentRoot(self):
        return self

    def choiceUsernameDlg(self, parent=None):
        """
        Вызов диалога выбора имени пользователя текущего проекта.
        @param parent: Родительское окно. Если не указано, то берется getPrjTreeCtrl().
        @return: Имя выбранного пользователя или None если нажата <Отмена>.
        """
        if parent is None:
            parent = self.getPrjTreeCtrl()
        users_description = self.prj_security.usr_res_manager.getUserNameDescriptionDict() if self.prj_security else dict()
        users_description_list = sorted(users_description.items())
        choices = [description if description else username for username, description in users_description_list]
        # По умолчанию выбираем Администратора проекта
        usernames = [user[0] for user in users_description_list]
        selection = usernames.index('admin') if 'admin' in usernames else -1
        selected_idx = ic_dlg.icSingleChoiceIdxDlg(parent, u'ПОЛЬЗОВАТЕЛЬ',
                                                   u'Выберите пользователя',
                                                   Choice_=choices, default_idx=selection)
        username = None
        if selected_idx >= 0:
            username = users_description_list[selected_idx][0]
        return username

    def _runPrjCmd(self, AppDir_, PrjPath_, username=None):
        """
        Запуск проекта на исполнение.
        @param AppDir_: Папка приложения.
        @param PrjPath_: Папка проекта.
        @param username: Имя пользователя, запускающего проект.
            Если не указано (None), то производиться выбор из списка пользователей,
            присутствующих в проекте.
        """
        import ic.utils.ic_exec as ic_exec

        ic_exec.CreateRunApp(AppDir_)
        
        # Коммандная строка
        dbg_mode_cmd = ''

        if username is None:
            username = self.choiceUsernameDlg()

        if username is None:
            log.warning(u'Не определен пользователь запуска проекта')
            return

        if self.debug_mode:
            dbg_mode_cmd = '-dbg'

        if ic_util.isOSWindowsPlatform():
            cmd = '\"%s/python.exe\" \"%s/run.py\" -run %s \"%s/\" -s %s' % (sys.prefix, AppDir_,
                                                                             dbg_mode_cmd, PrjPath_, username)
        else:
            cmd = '%s %s/run.py -run %s %s/ -s %s' % (sys.executable, AppDir_, dbg_mode_cmd, PrjPath_, username)
            
        log.info(u'RUN PROJECT: <%s>' % cmd)
        ic_exec.RunTask(cmd)
        
    def run(self):
        """
        Метод запуска на тестирование.
        """
        prj_path = os.path.dirname(self.getRoot().getPrjFileName())
        app_dir = os.path.dirname(prj_path)
        # Откомпилировать главный модуль
        if os.path.exists(os.path.join(app_dir, 'run.py')):
            ic_file.CompileFile(os.path.join(app_dir, 'run.py'))

        # Коммандная строка
        self._runPrjCmd(app_dir, prj_path)

    def debug(self):
        """
        Запуск проекта в режиме отладки.
        """
        self._debugWinPDB()

    def _debugWinPDB(self):
        try:
            import ic
            p, fl = os.path.split(self.getRoot().getPrjFileName())
            p = p.replace('\\', '/')
            filename = '%s/run.py' % '/'.join(p.split('/')[:-1])
            icp, icf = os.path.split(ic.__file__)
            dbg = '%s/Scripts/debug.py' % icp
            dbg2 = '%s/Scripts/debug.bat' % icp
            ppth = '%s/python' % sys.prefix 
            ppth = ppth.replace('\\', '/')
            dbg = dbg.replace('\\', '/')
            ppth3 = sys.prefix + '/Scripts/winpdb_.pyw'
            if wx.Platform != '__WXMSW__':
                p = subprocess.Popen(['python', dbg, filename])
            else:
                os.spawnl(os.P_NOWAIT, ppth, ppth, dbg, filename)
        except ImportError:
            wx.MessageBox(u'It requires Windpdb package (http://winpdb.org).')

    def edit(self):
        """
        Редактирование модуля - точки входа в систему -
        редактирование run.py файла.
        """
        ide = self.getParent().ide
        if ide:
            imp_path = self.getRoot().getPrjFileName()

            if not imp_path:
                return False

            imp_path, fl = os.path.split(imp_path)
            imp_path = imp_path.replace('\\', '/')
            py_file = '%s/run.py' % '/'.join(imp_path.split('/')[:-1])
            
            if not ide.SelectFile(py_file):
                return ide.OpenFile(py_file, True, readonly=False)
            return True

    def _debugWinPDB_old(self):
        """
        Отладка в WinPDB.
        """
        import ic.utils.ic_exec as ic_exec
        import sys
        
        python_exe = sys.executable
        winpdb_module = '%s%sLib%ssite-packages%swinpdb.py' % (sys.prefix,
                                                               ic_file.PATH_SEPARATOR,
                                                               ic_file.PATH_SEPARATOR,
                                                               ic_file.PATH_SEPARATOR)
        
        if os.path.exists(winpdb_module):
            # Если установлен WinPDB
            prj_path = os.path.dirname(self.getRoot().getPrjFileName())
            defis_dir = os.path.dirname(os.path.dirname(prj_path))
        
            ic_exec.CreateRunApp(defis_dir)
            
            # Коммандная строка
            cmd = '\'%s\' \'%s\' -c -t \'%s/run.py\' -run \'%s/\' -s' % (python_exe, winpdb_module,
                                                                         defis_dir, prj_path)
            
            log.info('DEBUG PROJECT: <%s>' % cmd)
            ic_exec.RunTaskBAT(cmd)
        
    def getResNamesByTypes(self, *Types_):
        """
        Список имен ресурсов в проекте по их типу.
        @param Types_: Кортеж строковых определение типа ресурса 'tab','frm',...
        @return: Возвращает список имен ресурсов заданных типов.
        """
        return self.prj_res_manager.getResNameListByTypes(*Types_)

    def getObjNamesByTypes(self, *Types_):
        """
        Список имен объектов в проекте по их типу ресурса.
        @param Types_: Кортеж строковых определение типа ресурса 'tab','frm',...
        @return: Возвращает список имен объектов.
        """
        res_types = tuple(['.*\.'+res_type for res_type in Types_])
        return self.prj_res_manager.getObjNamesByResPattern(*res_types)
       
    def getObjNamesInResources(self, ResTypes_, ObjType_):
        """
        Список имен объектов в проекте по типам ресурсов и типу объекта.
        """
        res_types = list(['.*\.'+res_type for res_type in ResTypes_])
        return [obj[1] for obj in self.prj_res_manager.getObjByResPatternANDType(res_types, ObjType_)]
        
    def getObjNamesInResourcesByTypes(self, ResTypes_, ObjTypes_):
        """
        Список имен объектов в проекте по типам ресурсов и типам объектов.
        """
        res_types = list(['.*\.'+res_type for res_type in ResTypes_])
        return [obj[1] for obj in self.prj_res_manager.getObjByResPatternANDTypes(res_types, ObjTypes_)]

    def getPrjTreeCtrl(self):
        return self.getParent()
