#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль класса главного узла дерева проекта.
"""

# Подключение библиотек
import wx
import sys
import os.path
import py_compile

from ic.log import log

from ic.imglib import common as imglib
from ic.utils import filefunc
from ic.utils import ic_res
from ic.dlg import ic_dlg
from ic.kernel import icexceptions
from ic.utils import ic_util
from ic.utils import impfunc

from ic.engine import glob_functions
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
    log.error(u'Ошибка импорта Winpdb', bForcePrint=True)

# import shlex
import subprocess

_ = wx.GetTranslation

__version__ = (0, 1, 1, 2)

# Константы
# Файл журнала зарегистрированных пользователей
PRJ_REG_JRN_FILE_NAME = './log/prj_reg_user_journal.ini'


class icPrjRoot(ImpNode.icPrjImportSys):
    """
    Главный класс проекта.
    """

    def __init__(self, parent=None):
        """
        Конструктор.
        """
        ImpNode.icPrjImportSys.__init__(self, parent)
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
        if not glob_functions.isVar('PRJ_ROOT') or glob_functions.getVar('PRJ_ROOT') is None:
            glob_functions.letVar('PRJ_ROOT', self)

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

        kernel = glob_functions.getKernel()
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
            
    def unlockResInResEditor(self, res_editor=None):
        """
        Разблокировать ресурс, который находится в редакторе ресурсов.
        @param res_editor: Редактор ресурса.
        """
        if res_editor is None:
            res_editor = self.getParent().res_editor
        if res_editor is None:
            log.warning('Don\'t define Resource Editor')
            return False

        res_name = res_editor.GetResName()
        if res_name:
            res_file_name = res_editor.GetResFileName()
            if res_file_name:
                res_file_ext = os.path.splitext(os.path.basename(res_file_name))[1][1:]
                res_file_name = os.path.splitext(os.path.basename(res_file_name))[0]
                return ic_res.unlockRes(res_name, res_file_name,
                                        res_file_ext, self.lock_dir)
        return False

    def unlockPyFileInIDE(self, py_filename):
        """
        Разблокировать модуль.
        @param py_filename: Имя модуля.
        """
        ide = self.getParent().getIDE()
        # Если файл не открыт в редакторе, то удалить блокировку
        if ide and not ide.isOpenedFile(py_filename):
            py_file_name = os.path.splitext(os.path.basename(py_filename))[0]
            py_file_ext = 'py'
            package_name = os.path.basename(os.path.dirname(py_filename))
            log.debug('UNLOCK PY FILE <%s> is open - %s' % (py_filename, ide.getAlreadyOpen()))
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
            if prj_dir not in sys.path:
                sys.path = impfunc.addImportPath(prj_dir)
        
    def Default(self):
        """
        Создать нужные папки по умолчанию.
        """
        self.description = u'Проект'
        self.prj_res_manager.newPrj(self.name, '')

        # Удалить все дочерние объекты
        self.children = []
        # и добавить по умолчанию
        self.addChild(prj_env.icPrjEnv(self))
        self.prj_security = prj_security.icPrjSecurity(self)
        self.addChild(self.prj_security)
        self.addChild(prj_report.icPrjReports(self))
        resources = prj_resource.icPrjResources(self)
        self.addChild(resources)

        db = resources.addChild(prj_resource.icPrjResources(resources))
        db.name = u'БД'
        tables = resources.addChild(prj_resource.icPrjResources(resources))
        tables.name = u'Таблицы'
        menus = resources.addChild(prj_resource.icPrjResources(resources))
        menus.name = u'Меню'
        systems = resources.addChild(prj_resource.icPrjResources(resources))
        systems.name = u'Системное'
        forms = resources.addChild(prj_resource.icPrjResources(resources))
        forms.name = u'Формы'
        meta = resources.addChild(prj_resource.icPrjResources(resources))
        meta.name = u'Метаданные'
        
        self.addChild(prj_module.icPrjModules(self))
        self.addChild(ImpNode.icPrjImportSystems(self))
        
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
        win_node = prj_resource.icPrjWinRes(frm_folder)
        win_node.template['name'] = win_node.name
        frm_folder.addChild(win_node)
        # 3. Сохранить созданные ресурсы
        win_node.save()
        security_node.save()
        return self.save()
        
    def onNodePopup(self, event):
        """
        Вызов всплывающего меню узла.
        """
        popup_menu = menuRootNode.icMenuRootNode(self)
        popup_menu.Popup(wx.GetMousePosition(), self._root.getParent())

    def _new_prj_init_file(self, prj_path):
        """
        Создать новый __init__.py файл проекта.
        """
        log.info(_('__init__.py is created in folder %s') % prj_path)
        return filefunc.copyFile(os.path.join(os.path.dirname(__file__),
                                               'prj__init__prototype.py'),
                                 os.path.join(prj_path, '__init__.py'), False)
        
    def newPrj(self):
        """
        Новый проект.
        """
        tree_prj = self.getParent()
        dir_prj_file_name = ic_dlg.icDirDlg(tree_prj, u'Создать проект',
                                            default_path=filefunc.getRootDir())
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
                tree_prj.ide.closeFile(None)
            
            # Инициализировать по умолчанию
            self.Default()
            # определить папку блокировок не уровне выше
            self.lock_dir = os.path.join(os.path.dirname(os.path.dirname(new_prj_file_name)), 'lock')
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
            glob_functions.initEnv(os.path.dirname(self.getPrjFileName()))
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
        self.addChild(prj_env.icPrjEnv(self))
        self.prj_security = prj_security.icPrjSecurity(self)
        self.prj_security.openUsers()
        self.prj_security.openRoles()
        self.addChild(self.prj_security)
        self.addChild(prj_report.icPrjReports(self))
        self.addChild(prj_resource.icPrjResources(self))
        self.addChild(prj_module.icPrjModules(self))
        self.addChild(ImpNode.icPrjImportSystems(self))

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

    def getPrjSubsys(self, prj_filename):
        """
        Имя проекта и имя проекта, подсистемой которого он является.
        @param prj_filename: Имя файла проекта.
        @return: Кортеж (имя проекта, имя подсистемы).
        """
        prj_dir = os.path.dirname(prj_filename)
        subsys_name = os.path.basename(prj_dir)
        prj_name = os.path.basename(os.path.dirname(prj_dir))
        return prj_name, subsys_name
        
    def login(self, username=None, password=None, prj_filename=None):
        """
        Открыть регистрацию программиста в режиме редактирования.
        @param username: Имя пользователя.
        @param password: Пароль. Если имя или пароль не указаны, то выводится
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
            result = glob_functions.getKernel().Login(username, password)
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
            self._prj_user = glob_functions.getKernel().getUser()
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
        
    def openPrj(self, prj_filename=None):
        """
        Открыть проект.
        """
        tree_prj = self.getParent()
        if prj_filename is None:
            prj_filename = ic_dlg.icFileDlg(tree_prj, u'Открыть проект',
                                            u'Файл проекта (*.pro)|*.pro',
                                            default_path=filefunc.getRootDir())

        if prj_filename and not os.path.exists(prj_filename):
            ic_dlg.icWarningBox(u'ВНИМАНИЕ!', u'Файл проекта <%s> не найден' % prj_filename)
            return

        if prj_filename and os.path.exists(prj_filename):
            # Проверка тот ли мы проект загрузили
            prj_name, sub_sys_name = self.getPrjSubsys(prj_filename)
            if prj_name != sub_sys_name:
                ic_dlg.icWarningBox(u'ВНИМАНИЕ!',
                                    u'Подключение подсистемы <%s> к проекту <%s>! Все изменения будут утеряны. Подсистема: <%s>, Проект: <%s>!' % (sub_sys_name,
                                    prj_name, sub_sys_name, prj_name), parent=tree_prj)
            self.delMyLocks()   # Удалить блокировки из старого проекта
            self.logout()

            # Определить окружение проекта
            # ВНИМАНИЕ! При инициализации окружения после открытия в контексте ядра
            # должен отразиться актуальный проект------------------------------+
            # Иначе дерево проекта для выбора паспорта не обновляется          |
            # Поэтому явно задаем корень проекта в окружении                   v
            glob_functions.initEnv(os.path.dirname(prj_filename), PrjName=prj_name, PRJ_ROOT=self)
            
            # Регистрация программиста
            if not self.login(prj_filename=prj_filename):
                return
            
            # Удалить все из дерева
            tree_prj.DeleteAllItems()
            # Закрыть все
            tree_prj.res_editor.CloseResource()
            if tree_prj.ide:
                tree_prj.ide.closeFile(None)

            # Построить дерево узлов по ресурсному файлу
            self.prj_res_manager.openPrj(prj_filename)
            self.imp_prj_file_name = prj_filename
            self._openDefault()
            # Сохранить время и размер до следующей синхронизации
            self.prj_res_time = filefunc.getMakeFileTime(prj_filename)
            self.prj_res_size = os.path.getsize(prj_filename)

            # определить папку блокировок
            self.lock_dir = os.path.join(os.path.dirname(os.path.dirname(prj_filename)), 'lock')
            log.info(u'Инициализация директория блокировок: <%s>' % self.lock_dir)
            self.delMyLocks()   # Удалить блокировки из вновь открытого проекта
            
            # Создание ресурсов
            for cur_res in self.prj_res_manager.getPrjRoot():
                self.buildPrjRes(self.getResources(),
                                 list(cur_res.values())[0], list(cur_res.keys())[0])

            # Создание дерева функционала
            self.getModules().buildPrjPy(os.path.dirname(prj_filename))
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

    def buildPrjRes(self, cur_folder, res_node, res_name, folder_class=None):
        """
        Построение всех узлов/ресурсов проекта.
        @param cur_folder: Текущая папка, в которую происходит добавление узлов.
        @param res_node: Ресурс, соответствующий этому узлу.
        @param res_name: Имя ресурса, соответствующего этому узлу.
        @param folder_class: Класс папки проекта.
        @return: Корневой, добавляемый узел.
        """
        cur_node = None
        if isinstance(res_node, list):
            # Обработка папки
            if folder_class is None:
                cur_node = prj_resource.icPrjResources(cur_folder)
            else:
                cur_node = folder_class(cur_folder)
            # Установить имя
            cur_node.name = res_name
            cur_folder.addChild(cur_node)
            for cur_res in res_node:
                # Обработка подпапок
                self.buildPrjRes(cur_node, list(cur_res.values())[0],
                                 list(cur_res.keys())[0], folder_class)
        else:
            from . import prj_prototype
            res_node_typ = res_node.strip()
            if res_node_typ in prj_prototype.nodeReg.keys():
                # Взять класс из реестра узлов
                # и создать объект узла
                cur_node = prj_prototype.nodeReg[res_node_typ](cur_folder)
                # Установить имя
                cur_node.name = res_name
                # Добавить узел в папку
                cur_folder.addChild(cur_node)
            else:
                log.warning(u'Invalid resource type <%s>' % res_node_typ)

        return cur_node
            
    def synchroPrj(self, bRefresh=False):
        """
        Синхронизация дерева проекта с изменениями другими программистами.
        @param bRefresh: указание принудительного обновления дерева проекта.
        """
        prj_file = self.getPrjFileName()
        if prj_file:
            cur_prj_res_time = filefunc.getMakeFileTime(prj_file)
            cur_prj_res_size = os.path.getsize(prj_file)
            if (cur_prj_res_time != self.prj_res_time) or \
               (cur_prj_res_size != self.prj_res_size) or \
               bRefresh:
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
                                         list(cur_res.values())[0], list(cur_res.keys())[0])
    
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
                    log.fatal(u'Ошибка синхронизации проекта <%s>' % self.name)

    def save(self):
        """
        Сохранить проект.
        """
        ok = self.prj_res_manager.savePrj()
        # Сохранить время и размер до следующей синхронизации
        self.prj_res_time = filefunc.getMakeFileTime(self.getPrjFileName())
        self.prj_res_size = os.path.getsize(self.getPrjFileName())
        return ok

    def rename(self, old_name, new_name):
        """
        Переименование проекта.
        @param old_name: Старое имя.
        @param new_name: Новое имя.
        """
        old_prj_file_name = self.getRoot().getPrjFileName()
        self.name = new_name
        self.prj_res_manager.prj_file_name = self.getRoot().getPrjFileName()
        self.prj_res_manager.setPrjRootName(new_name)

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
            return os.path.normpath(os.path.dirname(prj_file_name.strip()))
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
                                                   choices=choices, default_idx=selection)
        username = None
        if selected_idx >= 0:
            username = users_description_list[selected_idx][0]
        return username

    def _runPrjCmd(self, app_dir, prj_path, username=None):
        """
        Запуск проекта на исполнение.
        @param app_dir: Папка приложения.
        @param prj_path: Папка проекта.
        @param username: Имя пользователя, запускающего проект.
            Если не указано (None), то производиться выбор из списка пользователей,
            присутствующих в проекте.
        """
        import ic.utils.ic_exec as ic_exec

        # ic_exec.createRunApp(app_dir)
        
        # Коммандная строка
        dbg_mode_cmd = ''

        if username is None:
            username = self.choiceUsernameDlg()

        if username is None:
            log.warning(u'Не определен пользователь запуска проекта')
            return

        if self.debug_mode:
            dbg_mode_cmd = '-dbg'

        ic_engine_path = os.path.join(os.path.dirname(app_dir), 'ic', 'engine')
        if ic_util.isOSWindowsPlatform():
            cmd = '\"%s/python.exe\" \"%s/run.py\" -run %s \"%s/\" -s %s' % (sys.prefix, ic_engine_path,
                                                                             dbg_mode_cmd, prj_path, username)
        else:
            cmd = '%s %s/run.py -run %s %s/ -s %s' % (sys.executable, ic_engine_path, dbg_mode_cmd, prj_path, username)
            
        log.info(u'Запуск проекта <%s>' % cmd)
        ic_exec.runTask(cmd)
        
    def run(self):
        """
        Метод запуска на тестирование.
        """
        prj_path = os.path.dirname(self.getRoot().getPrjFileName())
        app_dir = os.path.dirname(prj_path)
        # Откомпилировать главный модуль
        if os.path.exists(os.path.join(app_dir, 'run.py')):
            py_compile.compile(os.path.join(app_dir, 'run.py'))

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
            p = os.path.normpath(p)     # .replace('\\', '/')
            filename = os.path.join(os.path.dirname(p), 'run.py')
            icp, icf = os.path.split(ic.__file__)
            dbg = os.path.join(icp, 'Scripts', 'debug.py')
            dbg2 = os.path.join(icp, 'Scripts', 'debug.bat')
            ppth = sys.executable
            ppth = ppth.replace('\\', '/')
            dbg = dbg.replace('\\', '/')
            ppth3 = os.path.join(sys.prefix, 'Scripts', 'winpdb_.pyw')
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
        ide = self.getParent().getIDE()
        if ide:
            imp_path = self.getRoot().getPrjFileName()

            if not imp_path:
                return False

            imp_path, fl = os.path.split(imp_path)
            imp_path = os.path.normpath(imp_path)   # .replace('\\', '/')
            py_file = os.path.join(os.path.dirname(imp_path), 'run.py')
            
            if not ide.selectFile(py_file):
                return ide.openFile(py_file, True, bReadonly=False)
            return True
        else:
            log.warning(u'Не определен IDE для редактирования модулей')

    def getResNamesByTypes(self, *res_types):
        """
        Список имен ресурсов в проекте по их типу.
        @param res_types: Кортеж строковых определение типа ресурса 'tab','frm',...
        @return: Возвращает список имен ресурсов заданных типов.
        """
        return self.prj_res_manager.getResNameListByTypes(*res_types)

    def getObjNamesByTypes(self, *res_types):
        """
        Список имен объектов в проекте по их типу ресурса.
        @param res_types: Кортеж строковых определение типа ресурса 'tab','frm',...
        @return: Возвращает список имен объектов.
        """
        cur_res_types = tuple(['.*\.' + res_type for res_type in res_types])
        return self.prj_res_manager.getObjNamesByResPattern(*cur_res_types)
       
    def getObjNamesInResources(self, res_types, obj_type):
        """
        Список имен объектов в проекте по типам ресурсов и типу объекта.
        """
        cur_res_types = list(['.*\.' + res_type for res_type in res_types])
        return [obj[1] for obj in self.prj_res_manager.getObjByResPatternANDType(cur_res_types, obj_type)]
        
    def getObjNamesInResourcesByTypes(self, res_types, obj_types):
        """
        Список имен объектов в проекте по типам ресурсов и типам объектов.
        """
        cur_res_types = list(['.*\.' + res_type for res_type in res_types])
        return [obj[1] for obj in self.prj_res_manager.getObjByResPatternANDTypes(cur_res_types, obj_types)]

    def getPrjTreeCtrl(self):
        return self.getParent()
