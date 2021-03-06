#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль классов узлов дерева импортируемых систем.
"""

# --- Подключение библиотек ---
import os.path
import shutil
import wx

from ic.imglib import common as imglib

from ic.utils import filefunc
from ic.utils import resfunc
from ic.dlg import dlgfunc
from ic.log import log

from ic.interfaces import subsysinterface

from . import menuImpNode
from . import prj_node
from . import prj_module
from . import PrjRes
from ic.engine import glob_functions

__version__ = (0, 1, 1, 1)

_ = wx.GetTranslation

# --- Константы ---
# Функции, которые необходимы для работы подсистемы.
_SubSysFuncs = {'install': '''def install(RootPrjTree_):
    \"\"\"
    Функция, выполняющаяся при подключении импортируемой подсистемы.
    :param engine: Указатель на основной движок системы.
    \"\"\"
    pass
    ''',
                'deinstall': '''def deinstall(RootPrjTree_):
    \"\"\"
    Функция, выполняющаяся при отключении импортируемой подсистемы.
    :param engine: Указатель на основной движок системы.
    \"\"\"
    pass
    ''',
                'initialize': '''def inittialize(engine):
    \"\"\"
    Функция, выполняющаяся при инициализации импортируемой подсистемы.
    \"\"\"
    pass
    ''',
                'deinitialize': '''def deinittialize(engine):
    \"\"\"
    Функция, выполняющаяся при деинициализации импортируемой подсистемы.
    \"\"\"
    pass
    ''',
                'get_icon': '''def get_icon():
    \"\"\"
    Функция для определения образа импортируемой подсистемы.
    \"\"\"
    return None
    ''',
                }

ALL_PKL_FILES_MASK = ('*_pkl.src', '*_pkl.tab', '*_pkl.frm',
                      '*_pkl.mnu', '*_pkl.rol', '*_pkl.acc',
                      '*_pkl.mtd', '*_pkl.win', '*_pkl.odb')


class icPrjImportFolder(prj_node.icPrjFolder):
    """
    Папка внутри импортируемой подсистемы.
    """

    def __init__(self, parent=None):
        """
        Конструктор.
        """
        prj_node.icPrjFolder.__init__(self, parent)

        self.description = 'new_imp_folder'
        # Имя узла при добавлении в дерево проекта
        self.name = 'new_imp_folder'

    def onNodePopup(self, event):
        """
        Вызов всплывающего меню узла.
        """
        pass


class icPrjImportResources(icPrjImportFolder):
    """
    Папка ресурсов внутри импортируемой подсистемы.
    """

    def __init__(self, parent=None):
        """
        Конструктор.
        """
        icPrjImportFolder.__init__(self, parent)

        self.description = u'Ресурсы'
        # Имя узла при добавлении в дерево проекта
        self.name = u'Ресурсы'


class icPrjImportModules(prj_module.icPrjModules):
    """
    Папка модулей внутри импортируемой подсистемы.
    """
    def __init__(self, parent=None):
        """
        Конструктор.
        """
        prj_module.icPrjModules.__init__(self, parent)

        self.description = u'Модули'
        # Имя узла при добавлении в дерево проекта
        self.name = u'Модули'

    def onNodePopup(self, event):
        """
        Вызов всплывающего меню узла.
        """
        pass

    def edit(self):
        """
        Необходимо заблокировать редактирование этого узла.
        Т.к. импортированные системы не редактируются.
        """
        dlgfunc.openWarningBox(u'ВНИМАНИЕ!',
                               u'Редактирование импортированных систем не возможно.')


class icPrjImportSystems(icPrjImportFolder):
    """
    Папка импортируемых подсистем.
    """
    def __init__(self, parent=None):
        """
        Конструктор.
        """
        icPrjImportFolder.__init__(self, parent)
        self.img_extended = imglib.imgFolderOpen
        self.description = u'Подсистемы'
        self.name = u'Подсистемы'
        self.include_nodes = [icPrjImportSys]
        self.include_folder = None

        # Для доступа к редактору ресурсов и IDE
        self.res_editor = None
        self.ide = None

    def getIDE(self):
        """
        IDE проекта.
        """
        return self.ide

    def edit(self):
        """
        Необходимо заблокировать редактирование этого узла.
        Т.к. импортированные системы не редактируются.
        """
        dlgfunc.openWarningBox(u'ВНИМАНИЕ!',
                               u'Редактирование импортированных систем не возможно.')

    def setRoot(self, root):
        prj_node.icPrjNode.setRoot(self, root)
        self.res_editor = self.getRoot().getParent().res_editor
        self.ide = self.getRoot().getParent().getIDE()

    def getSubSytems(self):
        """
        Список объектов импортируемых подсистем.
        """
        return self.children

    def onNodePopup(self, event):
        """
        Вызов всплывающего меню узла.
        """
        popup_menu = menuImpNode.icMenuImpNode(self)
        popup_menu.Popup(wx.GetMousePosition(), self._root.getParent())

    def buildSubSystemsTree(self, sub_systems):
        """
        Построить дерево подсистемы в дереве проекта.

        :param sub_systems: Список указаний подсистем (<*.pro>[1:]).
        """
        for sub_sys in sub_systems:
            # Создать и инициализировать узел импортируемой системы
            imp_sys_node = icPrjImportSys(self)
            imp_sys_node.Default()
            imp_sys_node.name = sub_sys['name']
            # Путь к подсистеме
            sub_sys_dir = imp_sys_node.getPathInPrj()
            if os.path.exists(sub_sys_dir):
                try:
                    self.addChild(imp_sys_node)
                    # Построить дерево-содержание импортируемой подсистемы
                    imp_sys_node._is_build = False
                except:
                    log.error(u'Ошибка подключения подсистемы <%s>' % sub_sys_dir)
                    dlgfunc.openMsgBox(u'ОШИБКА', u'Ошибка подключения подсистемы <%s>' % sub_sys_dir)
            else:
                dlgfunc.openMsgBox(u'ОШИБКА', u'Не корректный путь к подсистеме <%s>' % sub_sys_dir)
                # Добавить узел не импортированной подсистемы
                not_imp_sys_node = icPrjNotImportSys(self)
                not_imp_sys_node.name = sub_sys['name']
                self.addChild(not_imp_sys_node)
                not_imp_sys_node._is_build = True

    def copySubSys(self, subsys_prj_filename):
        """
        Копирование подсистемы в текущий проект.

        :param subsys_prj_filename: Имя файла проекта подсистемы.
        :return: Возвращает новую директорию подсистемы или
            None в случае  ошибки.
        """
        sub_sys_dir = os.path.dirname(subsys_prj_filename)
        prj_dir = os.path.dirname(os.path.dirname(self.getRoot().getPrjFileName()))
        if (not os.path.isdir(sub_sys_dir)) or (not os.path.exists(sub_sys_dir)):
            dlgfunc.openMsgBox(u'ОШИБКА', u'Не корректный путь к подсистеме <%s>' % sub_sys_dir)
            return None
        if (not os.path.isdir(prj_dir)) or (not os.path.exists(prj_dir)):
            dlgfunc.openMsgBox(u'ОШИБКА', u'Не корректный путь к подсистеме <%s>' % prj_dir)
            return None
        return self._copySubSysDir(sub_sys_dir, prj_dir)

    def _copySubSysDir(self, subsys_dir, prj_dir):
        """
        Копирование директории подсистемы в текущий проект.

        :param subsys_dir: Папка подсистемы.
        :param prj_dir: Папка проекта.
        """
        if subsys_dir and prj_dir:
            log.info(u'Копирование подсистемы <%s> в <%s>' % (subsys_dir, prj_dir))
            # Просто скопировать одну папку в другую
            ok = filefunc.copyDir(src_dir=subsys_dir, dst_dir=prj_dir, bReWrite=True)
            # Кроме кодирования надо удалить все пикловсвие файлы из проекта
            # иначе бывает рассинхронизация с отредактированными ресурсами
            new_subsys_dir = os.path.join(prj_dir, os.path.basename(subsys_dir))
            filefunc.delAllFilesFilter(new_subsys_dir, *ALL_PKL_FILES_MASK)
            if ok:
                log.info(u'[+] Обновление подсистемы <%s> прошло успешно' % prj_dir)
                return new_subsys_dir
            else:
                log.warning(u'Ошибка копирования подсистемы <%s> в <%s>' % (subsys_dir, prj_dir))
        return None

    def refreshSubSystems(self):
        """
        Обновление подсистем.
        """
        sub_systems = self.getRoot().prj_res_manager.getImportSystems()
        prj_dir = os.path.dirname(os.path.dirname(self.getRoot().getPrjFileName()))
        try:
            dlgfunc.openProgressDlg(None, u'Обновление подсистем',
                                    u'Обновление подсистем', 0, len(sub_systems))
            for i_sub_sys in range(len(sub_systems)):
                sub_sys_dir = os.path.dirname(sub_systems[i_sub_sys]['path'])

                dlgfunc.updateProgressDlg(i_sub_sys, _('Refreshing') + ': ' + sub_sys_dir)
                if (not os.path.isdir(sub_sys_dir)) or (not os.path.exists(sub_sys_dir)):
                    dlgfunc.openMsgBox(u'ОШИБКА', u'Не корректный путь к подсистеме <%s>' % sub_sys_dir)
                    continue
                if (not os.path.isdir(prj_dir)) or (not os.path.exists(prj_dir)):
                    dlgfunc.openMsgBox(u'ОШИБКА', u'Не корректный путь к проекту <%s>' % prj_dir)
                    continue
                self._copySubSysDir(sub_sys_dir, prj_dir)

            # Обновить дерево пользовательских компонентов
            glob_functions.refreshImports()
            tree_prj = self.getParentRoot().getParent()
            tree_prj.res_editor.CloseResource()
            tree_prj.res_editor.InitObjectsInfo(bRefresh=True)

            dlgfunc.closeProgressDlg()
        except:
            log.error(u'Ошибка обновления подсистем')
            dlgfunc.closeProgressDlg()
            return False

        # Обновить дерево проекта
        self.getRoot().synchroPrj(True)
        return True

    def getSubSysPath(self, subsys_name):
        """
        Получить путь к импортируемой подсистеме по ее имени.

        :param subsys_name: Имя подсистемы.
        """
        sub_systems = self.getRoot().prj_res_manager.getImportSystems()
        sub_sys_names = [sub_sys['name'] for sub_sys in sub_systems]
        if subsys_name in sub_sys_names:
            i_sub_sys = sub_sys_names.index(subsys_name)
            return sub_systems[i_sub_sys]['path'].replace('\\', '/').strip()
        return None

    def unLinkSubSys(self, subsys_name):
        """
        Отключить импортированную подсистему.

        :param subsys_name: Имя подсистемы.
        """
        try:
            sub_sys_path = self.getSubSysPath(subsys_name)
            prj_dir = os.path.dirname(os.path.dirname(self.getRoot().getPrjFileName()))
            del_dir = os.path.join(prj_dir, os.path.basename(os.path.dirname(sub_sys_path)))
            log.info(u'Отключение подсистемы <%s>' % subsys_name)
            log.info(u'\tУдаление папки <%s>' % del_dir)
            # Сначала удалить из описания в фале *.pro
            ok = self.getRoot().prj_res_manager.delImpSubSys(subsys_name)
            # Затем удалить папку подсистемы
            if ok:
                shutil.rmtree(del_dir, True)
                self.delChildByName(subsys_name)
        except:
            log.fatal(u'Ошибка отключения импортированной подсистемы <%s>' % subsys_name)

    def getPrjTreeCtrl(self):
        return self.getParent().getPrjTreeCtrl()


class icPrjNotImportSys(prj_node.icPrjFolder, subsysinterface.ImportSubSysInterface):
    """
    Импортируемая подсистема, Но не подключенная по каким то причинам.
    """
    def __init__(self, parent=None):
        """
        Конструктор.
        """
        prj_node.icPrjFolder.__init__(self, parent)
        # Инсталяция
        subsysinterface.ImportSubSysInterface.__init__(self)

        self.description = u'Подсистема'
        self.name = 'new_import_sys'
        self.label = u'Подсистема'
        self.img = imglib.imgEdtPluginNot
        self.readonly = True
        # файл проекта импортируемой системы(в корневой папке)
        self.imp_prj_file_name = None
        self.lock_dir = None

        # Флаг, определяющий что дерево ресурсов и модулей подсистемы построенно
        self._is_build = False

    def getRoot(self):
        return self

    def isPrjRoot(self):
        """
        Подсистема является проектом?
        """
        return False

    def getParentRoot(self):
        return self.getParent().getRoot()

    def getPrjFileName(self):
        return os.path.join(os.path.dirname(os.path.dirname(self.getParentRoot().getPrjFileName())),
                            self.name.strip(), '%s.pro' % self.name.strip())

    def openPrjFile(self, prj_filename):
        """
        Открыть файл проекта.

        :param prj_filename: Имя файла проекта.
        :return: Готовую структуру проекта или None в случае ошибки.
        """
        if prj_filename.endswith('_pkl.pro'):
            # Определяем тип ресурса по окончанию имени файла
            return resfunc.loadResourcePickle(prj_filename)
        else:
            return resfunc.loadResourceText(prj_filename)

    def getPath(self):
        """
        Путь к импортируемой системе.
        """
        return os.path.dirname(self.imp_prj_file_name.strip())

    def getPathInPrj(self):
        """
        Путь импортируемой подсистемы внутри текущего проекта.

        :return: Полный путь до файла проекта подсистемы.
        """
        return os.path.dirname(self.getPrjFileName())

    def unlockResInResEditor(self, res_editor=None):
        """
        Заглушка.
        """
        pass

    def changeLink(self):
        """
        Изменить связь с импортируемой подсистемой.
        """
        # Сначала удалить подсистему
        sub_systems = self.getParent()
        sub_systems.unLinkSubSys(self.name)

        # Удалить объект из дерева
        tree_prj = self.getParentRoot().getParent()

        # Затем произвести запрос на подключение новой подсистемы.
        # и обновить дерево проекта
        self.newImpSys()
        ok = self.buildSubSysTree()

        # Добавить объект в отображаемом дереве
        if ok:
            # Сразу сохранить проект
            self.getParentRoot().save()
            # Построить ветку дерева,
            # соответствующую импортируемой подсистеме
            tree_prj.addBranchInParentSelection(self)
            # Удалить старую ветку
            tree_prj.delSelectionNode()

        # Обновление дерева проектов
        tree_prj.Refresh()

    def unLink(self):
        """
        Отключить импортируемую подсистему.
        """
        sub_systems = self.getParent()
        sub_systems.unLinkSubSys(self.name)

        # Удалить объект из дерева
        tree_prj = self.getParentRoot().getParent()
        if tree_prj:
            # Удалить ветку
            tree_prj.delSelectionNode()

            # Обновление дерева проектов
            tree_prj.Refresh()

    def onNodePopup(self, event):
        """
        Вызов всплывающего меню узла.
        """
        popup_menu = menuImpNode.icMenuNotImpSysNode(self)
        tree_ctrl = self.getParentRoot().getParent()
        popup_menu.Popup(wx.GetMousePosition(), tree_ctrl)

    def newImpSys(self):
        """
        Добавить новую подсистему в словарь.

        :return: Возвращает в случае неудачи None,
            в случае успеха сформированный список.
        """
        prj_data = None
        # диалог выбора файла *.pro
        prj_file_name = dlgfunc.getFileDlg(self.getParentRoot().getParent().getIDEFrame(),
                                         u'Выберите подсистему', u'Project file (*.pro)|*.pro',
                                           default_path=filefunc.getRootDir())
        if prj_file_name:
            # открыть файл *.pro
            prj_data = self.openPrjFile(prj_file_name)
            new_name = self.readPrjName(prj_data)
            if self.getParentRoot().prj_res_manager.isImpSubSys(new_name):
                dlgfunc.openMsgBox(u'ВНИМАНИЕ',
                                u'Подсистема с таким наименованием уже сеществует!')
                return None
            else:
                # Скопировать в папку текущего проекта
                prj_dir = self._Parent.copySubSys(prj_file_name)
                prj_filenames = [filename for filename in filefunc.getFilenamesByExt(prj_dir, '.pro') if not filename.startswith('_pkl.pro')]
                self.imp_prj_file_name = prj_filenames[0] if prj_filenames else None
                # добавить в список
                if self.imp_prj_file_name:
                    self.name = new_name
                    self.getParentRoot().prj_res_manager.newSubSys(self.name,
                                                                   prj_file_name, prj_data[0]['__py__'])
                    # Инициализировать
                    self.Default()
                    # И инсталлировать
                    self._install()

        return self.getParentRoot().prj_res_manager.getImportSystems()

    def readPrjName(self, prj_file=None):
        """
        Прочитать имя проекта из файла проекта.

        :param prj_file: Файл проекта.
            М.б. задан, как имя файла или как данные файла.
        :return: Имя проекта или None в случае ошибки.
        """
        if prj_file:
            if isinstance(prj_file, str):
                # Задано имя файла
                prj_data = self.openPrjFile(prj_file)
            else:
                prj_data = prj_file
            # Задано содержание файла
            prj_names = [key for key in prj_data[0].keys() if not key.startswith('_')]
            return prj_names[0]
        return None

    def buildSubSysTree(self, subsys_prj_filename=None):
        """
        Построить дерево подсистемы в дереве проекта.

        :param subsys_prj_filename: Файл проекта импортируемой подсистемы.
            Если None, то берется установленный файл.
        :return: Возвращает результат выполнения операции True/False.
        """
        # Если None, то берется установленный файл.
        if subsys_prj_filename is None:
            subsys_prj_filename = self.imp_prj_file_name
        if subsys_prj_filename:
            try:
                if not os.path.exists(subsys_prj_filename):
                    log.warning(u'Не найден файл проекта <%s> подсистемы' % subsys_prj_filename)
                    return False

                prj_manager = PrjRes.icPrjRes()
                prj_manager.openPrj(subsys_prj_filename)
                # Создание ресурсов
                for cur_res in prj_manager.getPrjRoot():
                    self.getParentRoot().buildPrjRes(self.getResources(),
                                                     list(cur_res.values())[0],
                                                     list(cur_res.keys())[0],
                                                     icPrjImportFolder)

                # Создание дерева функционала
                self.getModules().buildPrjPy(os.path.dirname(subsys_prj_filename))

                # Все узлы импортируемых подсистем открываются
                # только для проcмотра
                self.readonlyChildren(True)

                self._is_build = True
                return self._is_build
            except:
                log.fatal(u'Ошибка построения дерева проекта подсистемы <%s>' % subsys_prj_filename)
        return False

    def isBuild(self):
        """
        Дерево подсистемы построенно?
        """
        return self._is_build

    def Default(self):
        """
        Создать нужные папки по умолчанию.
        """
        # Удалить все дочерние объекты
        self.children = []
        # и добавить по умолчанию
        self.addChild(icPrjImportResources(self))
        self.addChild(icPrjImportModules(self))

    def getResources(self):
        """
        Папка ресурсов.
        """
        return self.children[0]

    def getModules(self):
        """
        Папка функционала.
        """
        return self.children[1]

    def getImpSystems(self):
        """
        Папка импортируемых подсистем.
        """
        return self.children[2]

    def _install(self):
        """
        Вспомогательные действия при инсталяции системы.
        """
        self.install(self.getParentRoot())
        if self.icon:
            self.img = self.icon

    def getPrjTreeCtrl(self):
        return self.getParentRoot().getPrjTreeCtrl()


class icPrjImportSys(icPrjNotImportSys):
    """
    Импортируемая подсистема.
    """
    def __init__(self, parent=None):
        """
        Конструктор.
        """
        icPrjNotImportSys.__init__(self, parent)
        # Инсталяция
        self.description = u'Подсистема'
        self.name = 'new_import_sys'
        self.label = u'Подлючить подсистему'
        self.img = imglib.imgEdtPlugin
        self.readonly = True
        # файл проекта импортируемой системы(в корневой папке)
        self.imp_prj_file_name = None
        self.lock_dir = None

        # Флаг, определяющий что дерево ресурсов и модулей подсистемы построенно
        self._is_build = False

    def edit(self):
        """
        Редактирование импортируемой системы/
        редактирование __init__.py файла.
        """
        ide = self.getParentRoot().getParent().getIDE()
        if ide:
            imp_path = self.getPath()
            if not imp_path:
                return False
            py_file = os.path.join(imp_path, '__init__.py')
            # Если в файле нет функций регистрации
            # импортируемой системы, то добавить их
            init_file = None
            try:
                init_file = open(py_file, 'rt')
                init_txt = init_file.read()
                init_file.close()
                for func_name in _SubSysFuncs:
                    ok = init_txt.find('def %s(' % func_name)
                    if ok < 0:
                        self._writeFunc(py_file, _SubSysFuncs[func_name])
            except:
                if init_file:
                    init_file.close()

            if not ide.selectFile(py_file):
                return ide.openFile(py_file, True, bReadonly=self.readonly)
            return True

    def _writeFunc(self, init_filename, function_body):
        """
        Запись функций в __init__ файл.
        """
        init_file = None
        try:
            init_file = open(init_filename, 'wt')
            init_file.write(function_body)
            init_file.close()
        except:
            if init_file:
                init_file.close()

    def unlockAllPyFilesInIDE(self):
        """
        Заглушка.
        """
        pass

    def refreshSubSys(self):
        """
        Обновить подсистему.
        """
        try:
            self._is_build = False

            sub_systems = self.getParent()
            prj_dir = os.path.dirname(os.path.dirname(sub_systems.getRoot().getPrjFileName()))
            sub_sys_dir = os.path.dirname(sub_systems.getSubSysPath(self.name))
            # Проверка входных данных
            if (not os.path.isdir(sub_sys_dir)) or (not os.path.exists(sub_sys_dir)):
                dlgfunc.openMsgBox(u'ОШИБКА', u'Не корректный путь к подсистеме <%s>' % sub_sys_dir)
                return
            if (not os.path.isdir(prj_dir)) or (not os.path.exists(prj_dir)):
                dlgfunc.openMsgBox(u'ОШИБКА', u'Не корректный путь к проекту <%s>' % prj_dir)
                return
            # Копировать подсистему в текущий проект
            sub_systems._copySubSysDir(sub_sys_dir, prj_dir)

            # Обновить дерево пользовательских компонентов
            glob_functions.refreshImports()
            tree_prj = self.getParentRoot().getParent()
            tree_prj.res_editor.CloseResource()
            tree_prj.res_editor.InitObjectsInfo(bRefresh=True)

            # Обновить дерево проекта
            sub_systems.getRoot().synchroPrj(True)
            return True
        except:
            log.error(u'Ошибка обновления подсистемы <%s>' % self.name)
            return False

    def onNodePopup(self, event):
        """
        Вызов всплывающего меню узла.
        """
        popup_menu = menuImpNode.icMenuImpSysNode(self)
        tree_ctrl = self.getParentRoot().getParent()
        popup_menu.Popup(wx.GetMousePosition(), tree_ctrl)
