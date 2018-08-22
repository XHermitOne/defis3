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

from ic.utils import ic_file
from ic.utils import ic_res
from ic.dlg import ic_dlg
from ic.log import log

from ic.interfaces import subsysinterface

from . import menuImpNode
from . import prj_node
from . import prj_module
from . import PrjRes
from ic.engine import ic_user

__version__ = (0, 1, 1, 1)

_ = wx.GetTranslation

# --- Константы ---
# Функции, которые необходимы для работы подсистемы.
_SubSysFuncs = {'install': '''def install(RootPrjTree_):
    \"\"\"
    Функция, выполняющаяся при подключении импортируемой подсистемы.
    @param Runner_: Указатель на основной движок системы.
    \"\"\"
    pass
    ''',
                'deinstall': '''def deinstall(RootPrjTree_):
    \"\"\"
    Функция, выполняющаяся при отключении импортируемой подсистемы.
    @param Runner_: Указатель на основной движок системы.
    \"\"\"
    pass
    ''',
                'initialize': '''def inittialize(Runner_):
    \"\"\"
    Функция, выполняющаяся при инициализации импортируемой подсистемы.
    \"\"\"
    pass
    ''',
                'deinitialize': '''def deinittialize(Runner_):
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


class PrjImportFolder(prj_node.PrjFolder):
    """
    Папка внутри импортируемой подсистемы.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        prj_node.PrjFolder.__init__(self, Parent_)

        self.description = 'new_imp_folder'
        # Имя узла при добавлении в дерево проекта
        self.name = 'new_imp_folder'

    def onNodePopup(self, event):
        """
        Вызов всплывающего меню узла.
        """
        pass


class PrjImportResources(PrjImportFolder):
    """
    Папка ресурсов внутри импортируемой подсистемы.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        PrjImportFolder.__init__(self, Parent_)

        self.description = u'Ресурсы'
        # Имя узла при добавлении в дерево проекта
        self.name = u'Ресурсы'


class PrjImportModules(prj_module.PrjModules):
    """
    Папка модулей внутри импортируемой подсистемы.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        prj_module.PrjModules.__init__(self, Parent_)

        self.description = u'Модули'
        # Имя узла при добавлении в дерево проекта
        self.name = u'Модули'

    def onNodePopup(self, event):
        """
        Вызов всплывающего меню узла.
        """
        pass


class PrjImportSystems(PrjImportFolder):
    """
    Папка импортируемых подсистем.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        PrjImportFolder.__init__(self, Parent_)
        self.img_extended = imglib.imgFolderOpen
        self.description = u'Подсистемы'
        self.name = u'Подсистемы'
        self.include_nodes = [PrjImportSys]
        self.include_folder = None

        # Для доступа к редактору ресурсов и IDE
        self.res_editor = None
        self.ide = None

    def setRoot(self, Root_):
        prj_node.PrjNode.setRoot(self, Root_)
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

    def buildSubSystemsTree(self, SubSystems_):
        """
        Построить дерево подсистемы в дереве проекта.
        @param SubSystems_: Список указаний подсистем (<*.pro>[1:]).
        """
        for sub_sys in SubSystems_:
            # Создать и инициализировать узел импортируемой системы
            imp_sys_node = PrjImportSys(self)
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
                    ic_dlg.icMsgBox(u'ОШИБКА', u'Ошибка подключения подсистемы <%s>' % sub_sys_dir)
            else:
                ic_dlg.icMsgBox(u'ОШИБКА', u'Не корректный путь к подсистеме <%s>' % sub_sys_dir)
                # Добавить узел не импортированной подсистемы
                not_imp_sys_node = PrjNotImportSys(self)
                not_imp_sys_node.name = sub_sys['name']
                self.addChild(not_imp_sys_node)
                not_imp_sys_node._is_build = True

    def copySubSys(self, SubSysPrjFileName_):
        """
        Копирование подсистемы в текущий проект.
        @param SubSysPrjFileName_: Имя файла проекта подсистемы.
        @return: Возвращает новую директорию подсистемы или
            None в случае  ошибки.
        """
        sub_sys_dir = os.path.dirname(SubSysPrjFileName_)
        prj_dir = os.path.dirname(os.path.dirname(self.getRoot().getPrjFileName()))
        if (not os.path.isdir(sub_sys_dir)) or (not os.path.exists(sub_sys_dir)):
            ic_dlg.icMsgBox(u'ОШИБКА', u'Не корректный путь к подсистеме <%s>' % sub_sys_dir)
            return None
        if (not os.path.isdir(prj_dir)) or (not os.path.exists(prj_dir)):
            ic_dlg.icMsgBox(u'ОШИБКА', u'Не корректный путь к подсистеме <%s>' % prj_dir)
            return None
        return self._copySubSysDir(sub_sys_dir, prj_dir)

    def _copySubSysDir(self, SubSysDir_, PrjDir_):
        """
        Копирование директории подсистемы в текущий проект.
        @param SubSysDir_: Папка подсистемы.
        @param PrjDir_: Папка проекта.
        """
        if SubSysDir_ and PrjDir_:
            log.info(u'Копирование подсистемы <%s> в <%s>' % (SubSysDir_, PrjDir_))
            # Просто скопировать одну папку в другую
            ok = ic_file.CopyDir(Dir_=SubSysDir_, ToDir_=PrjDir_, ReWrite_=True)
            # Кроме кодирования надо удалить все пикловсвие файлы из проекта
            # иначе бывает рассинхронизация с отредактированными ресурсами
            new_subsys_dir = os.path.join(PrjDir_, os.path.basename(SubSysDir_))
            ic_file.delAllFilesFilter(new_subsys_dir, *ALL_PKL_FILES_MASK)
            if ok:
                log.info(u'[+] Обновление подсистемы <%s> прошло успешно' % PrjDir_)
                return new_subsys_dir
            else:
                log.warning(u'Ошибка копирования подсистемы <%s> в <%s>' % (SubSysDir_, PrjDir_))
        return None

    def refreshSubSystems(self):
        """
        Обновление подсистем.
        """
        sub_systems = self.getRoot().prj_res_manager.getImportSystems()
        prj_dir = os.path.dirname(os.path.dirname(self.getRoot().getPrjFileName()))
        try:
            ic_dlg.icOpenProgressDlg(None, u'Обновление подсистем',
                                     u'Обновление подсистем', 0, len(sub_systems))
            for i_sub_sys in range(len(sub_systems)):
                sub_sys_dir = os.path.dirname(sub_systems[i_sub_sys]['path'])

                ic_dlg.icUpdateProgressDlg(i_sub_sys, _('Refreshing') + ': ' + sub_sys_dir)
                if (not os.path.isdir(sub_sys_dir)) or (not os.path.exists(sub_sys_dir)):
                    ic_dlg.icMsgBox(u'ОШИБКА', u'Не корректный путь к подсистеме <%s>' % sub_sys_dir)
                    continue
                if (not os.path.isdir(prj_dir)) or (not os.path.exists(prj_dir)):
                    ic_dlg.icMsgBox(u'ОШИБКА', u'Не корректный путь к проекту <%s>' % prj_dir)
                    continue
                self._copySubSysDir(sub_sys_dir, prj_dir)

            # Обновить дерево пользовательских компонентов
            ic_user.refreshImports()
            tree_prj = self.getParentRoot().getParent()
            tree_prj.res_editor.CloseResource()
            tree_prj.res_editor.InitObjectsInfo(bRefresh=True)

            ic_dlg.icCloseProgressDlg()
        except:
            log.error(u'Ошибка обновления подсистем')
            ic_dlg.icCloseProgressDlg()
            return False

        # Обновить дерево проекта
        self.getRoot().synchroPrj(True)
        return True

    def getSubSysPath(self, SubSysName_):
        """
        Получить путь к импортируемой подсистеме по ее имени.
        @param SubSysName_: Имя подсистемы.
        """
        sub_systems = self.getRoot().prj_res_manager.getImportSystems()
        sub_sys_names = [sub_sys['name'] for sub_sys in sub_systems]
        if SubSysName_ in sub_sys_names:
            i_sub_sys = sub_sys_names.index(SubSysName_)
            return sub_systems[i_sub_sys]['path'].replace('\\', '/').strip()
        return None

    def unLinkSubSys(self, SubSysName_):
        """
        Отключить импортированную подсистему.
        @param SubSysName_: Имя подсистемы.
        """
        try:
            sub_sys_path = self.getSubSysPath(SubSysName_)
            prj_dir = os.path.dirname(os.path.dirname(self.getRoot().getPrjFileName()))
            del_dir = os.path.join(prj_dir, os.path.basename(os.path.dirname(sub_sys_path)))
            log.info(u'Отключение подсистемы <%s>' % SubSysName_)
            log.info(u'\tУдаление папки <%s>' % del_dir)
            # Сначала удалить из описания в фале *.pro
            ok = self.getRoot().prj_res_manager.delImpSubSys(SubSysName_)
            # Затем удалить папку подсистемы
            if ok:
                shutil.rmtree(del_dir, True)
                self.delChildByName(SubSysName_)
        except:
            log.fatal(u'Ошибка отключения импортированной подсистемы <%s>' % SubSysName_)

    def getPrjTreeCtrl(self):
        return self.getParent().getPrjTreeCtrl()


class PrjNotImportSys(prj_node.PrjFolder, subsysinterface.ImportSubSysInterface):
    """
    Импортируемая подсистема, Но не подключенная по каким то причинам.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        prj_node.PrjFolder.__init__(self, Parent_)
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

    def openPrjFile(self, PrjFileName_):
        """
        Открыть файл проекта.
        @param PrjFileName_: Имя файла проекта.
        @return: Готовую структуру проекта или None в случае ошибки.
        """
        if PrjFileName_.endswith('_pkl.pro'):
            # Определяем тип ресурса по окончанию имени файла
            return ic_res.LoadResourcePickle(PrjFileName_)
        else:
            return ic_res.LoadResourceText(PrjFileName_)

    def getPath(self):
        """
        Путь к импортируемой системе.
        """
        return os.path.dirname(self.imp_prj_file_name.strip())

    def getPathInPrj(self):
        """
        Путь импортируемой подсистемы внутри текущего проекта.
        @return: Полный путь до файла проекта подсистемы.
        """
        return os.path.dirname(self.getPrjFileName())

    def unlockResInResEditor(self, ResEditor_=None):
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
            tree_prj.AddBranchInParentSelection(self)
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
        @return: Возвращает в случае неудачи None,
            в случае успеха сформированный список.
        """
        prj_data = None
        # диалог выбора файла *.pro
        prj_file_name = ic_dlg.icFileDlg(self.getParentRoot().getParent().getIDEFrame(),
                                         u'Выберите подсистему', u'Project file (*.pro)|*.pro')
        if prj_file_name:
            # открыть файл *.pro
            prj_data = self.openPrjFile(prj_file_name)
            new_name = self.readPrjName(prj_data)
            if self.getParentRoot().prj_res_manager.isImpSubSys(new_name):
                ic_dlg.icMsgBox(u'ВНИМАНИЕ',
                                u'Подсистема с таким наименованием уже сеществует!')
                return None
            else:
                # Скопировать в папку текущего проекта
                prj_dir = self._Parent.copySubSys(prj_file_name)
                prj_filenames = [filename for filename in ic_file.GetFilesByExt(prj_dir, '.pro') if not filename.startswith('_pkl.pro')]
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

    def readPrjName(self, PrjFile_=None):
        """
        Прочитать имя проекта из файла проекта.
        @param PrjFile_: Файл проекта.
            М.б. задан, как имя файла или как данные файла.
        @return: Имя проекта или None в случае ошибки.
        """
        if PrjFile_:
            if isinstance(PrjFile_, str):
                # Задано имя файла
                prj_data = self.openPrjFile(PrjFile_)
            else:
                prj_data = PrjFile_
            # Задано содержание файла
            prj_names = [key for key in prj_data[0].keys() if not key.startswith('_')]
            return prj_names[0]
        return None

    def buildSubSysTree(self, SubSysPrjFileName_=None):
        """
        Построить дерево подсистемы в дереве проекта.
        @param SubSysPrjFileName_: Файл проекта импортируемой подсистемы.
            Если None, то берется установленный файл.
        @return: Возвращает результат выполнения операции True/False.
        """
        # Если None, то берется установленный файл.
        if SubSysPrjFileName_ is None:
            SubSysPrjFileName_ = self.imp_prj_file_name
        if SubSysPrjFileName_:
            try:
                if not os.path.exists(SubSysPrjFileName_):
                    log.warning(u'Не найден файл проекта <%s> подсистемы' % SubSysPrjFileName_)
                    return False

                prj_manager = PrjRes.icPrjRes()
                prj_manager.openPrj(SubSysPrjFileName_)
                # Создание ресурсов
                for cur_res in prj_manager.getPrjRoot():
                    self.getParentRoot().buildPrjRes(self.getResources(),
                                                     list(cur_res.values())[0],
                                                     list(cur_res.keys())[0],
                                                     PrjImportFolder)

                # Создание дерева функционала
                self.getModules().buildPrjPy(os.path.dirname(SubSysPrjFileName_))

                # Все узлы импортируемых подсистем открываются
                # только для проcмотра
                self.readonlyChildren(True)

                self._is_build = True
                return self._is_build
            except:
                log.fatal(u'Ошибка построения дерева проекта подсистемы <%s>' % SubSysPrjFileName_)
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
        self.addChild(PrjImportResources(self))
        self.addChild(PrjImportModules(self))

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


class PrjImportSys(PrjNotImportSys):
    """
    Импортируемая подсистема.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        PrjNotImportSys.__init__(self, Parent_)
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

            if not ide.SelectFile(py_file):
                return ide.OpenFile(py_file, True, readonly=self.readonly)
            return True

    def _writeFunc(self, InitFileName_, FuncBody_):
        """
        Запись функций в __init__ файл.
        """
        init_file = None
        try:
            init_file = open(InitFileName_, 'wt')
            init_file.write(FuncBody_)
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
                ic_dlg.icMsgBox(u'ОШИБКА', u'Не корректный путь к подсистеме <%s>' % sub_sys_dir)
                return
            if (not os.path.isdir(prj_dir)) or (not os.path.exists(prj_dir)):
                ic_dlg.icMsgBox(u'ОШИБКА', u'Не корректный путь к проекту <%s>' % prj_dir)
                return
            # Копировать подсистему в текущий проект
            sub_systems._copySubSysDir(sub_sys_dir, prj_dir)

            # Обновить дерево пользовательских компонентов
            ic_user.refreshImports()
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
