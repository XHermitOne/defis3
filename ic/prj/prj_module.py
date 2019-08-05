#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль классов узлов модулей проекта.
"""

# Подключение библиотек
import wx
from wx.lib.agw import flatmenu
import os
import os.path
import shutil
# import imp
import ic.utils.impfunc
from ic.imglib import common as imglib
from ic.utils import ic_file
from ic.utils import ic_res
from ic.utils import util
from ic.dlg import ic_dlg
from ic.editor import ext_python_editor
from ic.log import log
from ic.editor import wxfb_manager

from . import prj_node
from . import prj_resource
from . import prj_fb
from . import prj_xrc
from . import prj_wxcp

__version__ = (0, 1, 3, 1)

_ = wx.GetTranslation

# Управлене функционалом системы
# Сигнатура интерфейсного модуля
INTERFACE_MODULE_SIGNATURE = '###BEGIN SPECIAL BLOCK'
# Сигнатура ресурсонго модуля
RESOURCE_MODULE_SIGNATURE = '### RESOURCE_MODULE:'
# Сигнатура модуля шаблона
TEMPLATE_MODULE_SIGNATURE = '### TEMPLATE_MODULE:'
# Сигнанура модуля библиотки образов
IMAGE_MODULE_SIGNATURE = '# --- Image Library File ---'
# Сигнанура модуля прототипа форм сгенерированнх wxFormBuilder
WXFB_MODULE_SIGNATURE = '## Python code generated with wxFormBuilder'
# Сигнатура модуля прототипа форм сгенерированного pywxrc утилитой (из XRC ресурса)
XRC_MODULE_SIGNATURE = '# This file was automatically generated by pywxrc.'


class PrjModules(prj_node.PrjFolder):
    """
    Функционал.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        prj_node.PrjFolder.__init__(self, Parent_)
        self.img_extended = imglib.imgFolderOpen
        self.description = u'Модули'
        self.name = u'Модули'
        self.include_nodes = [PrjModule,
                              prj_fb.PrjWXFormBuilderProject,
                              prj_xrc.PrjXRCResource,
                              prj_wxcp.PrjWXCrafterProject,
                              prj_resource.PrjTabRes, prj_resource.PrjDBRes,
                              prj_resource.PrjFrmRes, prj_resource.PrjWinRes,
                              prj_resource.PrjMenuRes, prj_resource.PrjTemplate,
                              prj_resource.PrjMethod]
        self.include_folder = PrjPackage

    def onNodePopup(self, event):
        """
        Вызов всплывающего меню узла.
        """
        from . import menuModNode

        popup_menu = menuModNode.icMenuModNode(self)
        popup_menu.Popup(wx.GetMousePosition(), self._root.getParent())

    def _getPrjFileList(self, Path_):
        """
        Получить отсортированный список файлов и подпапок по пути.
        Порядок сортировки: Сначала папки отсортированные по имени,
        затем файлы отсортированные по имени.
        @param Path_: Текущая папка-пакет.
        @return:
        """
        # Обработка подпапок
        file_list = [os.path.join(Path_, cur_file) for cur_file in os.listdir(Path_)]
        dir_list = [file_name for file_name in file_list if self.isPackage(file_name)]
        dir_list.sort()
        # Обработка списка файлов
        py_file_list = [file_name for file_name in file_list if self.isFBP(file_name) or
                        self.isXRC(file_name) or
                        self.isWXCP(file_name) or
                        self.isModule(file_name) or
                        self.isInterfaceModule(file_name) or
                        self.isResourceModule(file_name)]
        py_file_list.sort()

        # Объединить два отсортированных списка
        all_path_list = dir_list + py_file_list
        return all_path_list

    def buildPrjPy(self, Path_):
        """
        Построение всех узлов/py-модулей проекта.
        @param Path_: Текущая папка-пакет/py-модуль.
        """
        # Обработка подпапок
        all_path_list = self._getPrjFileList(Path_)
        for py_path in all_path_list:
            self.buildPyTree(self, py_path)

    def _findModuleSignature(self, ModuleName_, Signature_):
        """
        Проверка есть ли в модуле сигнатура?
        @param ModuleName_: Имя модуля.
        @param Signature_: Текст сигнатуры.
        @return: Возвращает True/False.
        """
        find = False
        module_file = None
        try:
            module_file = open(ModuleName_, 'rt')
            text = module_file.read()
            module_file.close()
            return text.find(Signature_) != -1
        except:
            log.fatal(u'Ошибка поиска сигнатуры <%s> в модуле <%s>.' % (Signature_, ModuleName_))
            if module_file:
                module_file.close()
            return False
        
    def isModule(self, FileName_):
        """
        Проверка является ли файл модулм проекта.
        @param FileName_: Имя файла.
        @return: Возвращает True/False.
        """
        return os.path.isfile(FileName_) and \
            (os.path.splitext(FileName_)[1] == '.py' and
             os.path.basename(FileName_) != '__init__.py') and \
            (not self._findModuleSignature(FileName_, INTERFACE_MODULE_SIGNATURE))

    def isFBP(self, sFileName):
        """ 
        Проверка является ли файл модулм проекта wxformbuilder.
        @param sFileName: Имя файла.
        @return: Возвращает True/False.
        """
        return os.path.isfile(sFileName) and \
            (os.path.splitext(sFileName)[1] == '.fbp')

    def isWXCP(self, sFileName):
        """
        Проверка является ли файл модулем проекта wxCrafter.
        @param sFileName: Имя файла.
        @return: Возвращает True/False.
        """
        return os.path.isfile(sFileName) and \
            (os.path.splitext(sFileName)[1] == '.wxcp')

    def isXRC(self, sFileName):
        """
        Проверка является ли файл XRC ресурсом форм.
        @param sFileName: Имя файла.
        @return: Возвращает True/False.
        """
        return os.path.isfile(sFileName) and \
            (os.path.splitext(sFileName)[1] == '.xrc') and \
            not sFileName.endswith('_forms_bitmaps.xrc')
        #                                ^
        # Исключаем файл ресурсов картинок, генерируемые wxCrafter

    def isInterfaceModule(self, FileName_):
        """
        Проверка является ли файл интерфейсным модулем проекта.
        @param FileName_: Имя файла.
        @return: Возвращает True/False.
        """
        return os.path.isfile(FileName_) and \
            (os.path.splitext(FileName_)[1] == '.py' and \
             os.path.basename(FileName_) != '__init__.py') and \
            self._findModuleSignature(FileName_, INTERFACE_MODULE_SIGNATURE)
            
    def isResourceModule(self, FileName_):
        """
        Проверка является ли файл ресурсным модулем проекта.
        @param FileName_: Имя файла.
        @return: Возвращает True/False.
        """
        return os.path.isfile(FileName_) and \
            (os.path.splitext(FileName_)[1] == '.py' and \
             os.path.basename(FileName_) != '__init__.py') and \
            self._findModuleSignature(FileName_, RESOURCE_MODULE_SIGNATURE)
            
    def isImageModule(self, FileName_):
        """
        Проверка является ли файл модулем библиотеки образов проекта.
        @param FileName_: Имя файла.
        @return: Возвращает True/False.
        """
        return os.path.isfile(FileName_) and \
            (os.path.splitext(FileName_)[1] == '.py' and \
            os.path.basename(FileName_) != '__init__.py') and \
            self._findModuleSignature(FileName_, IMAGE_MODULE_SIGNATURE)

    def isFBModule(self, FileName_):
        """
        Проверка является ли файл модулем форм wxFormBuilder.
        @param FileName_: Имя файла.
        @return: Возвращает True/False.
        """
        return os.path.isfile(FileName_) and \
            (os.path.splitext(FileName_)[1] == '.py' and
             os.path.basename(FileName_) != '__init__.py') and \
            self._findModuleSignature(FileName_, WXFB_MODULE_SIGNATURE)

    def isXRCModule(self, FileName_):
        """
        Проверка является ли файл модулем форм,
        сгенерированных утилитой pywxrc (из XRC ресурса).
        @param FileName_: Имя файла.
        @return: Возвращает True/False.
        """
        return os.path.isfile(FileName_) and \
            (os.path.splitext(FileName_)[1] == '.py' and
             os.path.basename(FileName_) != '__init__.py') and \
            self._findModuleSignature(FileName_, XRC_MODULE_SIGNATURE)

    def isTemplateModule(self, FileName_):
        """
        Проверка является ли файл модулем шаблона проекта.
        @param FileName_: Имя файла.
        @return: Возвращает True/False.
        """
        return os.path.isfile(FileName_) and \
            (os.path.splitext(FileName_)[1] == '.py' and \
            os.path.basename(FileName_) != '__init__.py') and \
            self._findModuleSignature(FileName_, TEMPLATE_MODULE_SIGNATURE)
            
    def isPackage(self, Dir_):
        """
        Проверка является ли директория пакетом проекта.
        @param Dir_: Указание директории.
        @return: Возвращает True/False.
        """
        is_dir = os.path.isdir(Dir_)
        is_in_prj = False
        is_init_file = False
        if is_dir:
            is_in_prj = ic_file.IsSubDir(Dir_, os.path.dirname(self.getRoot().getPrjFileName()))
            is_init_file = os.path.exists(os.path.join(Dir_, '__init__.py'))
        is_sub_sys = False
        return is_dir and is_in_prj and is_init_file and (not is_sub_sys)
        
    def buildPyTree(self, CurPackage_, Path_):
        """
        Построение всех узлов/py-модулей проекта.
        @param CurPackage_: Узел пакета, в который происходит добавление.
        @param Path_: Текущая папка-пакет/py-модуль.
        """
        if self.isPackage(Path_):
            # Это пакет
            cur_node = PrjPackage(CurPackage_)
            # Установить имя
            name = os.path.split(Path_)[1]
            cur_node.name = name
            CurPackage_.addChild(cur_node)
            # Обработка подпапок
            all_path_list = self._getPrjFileList(Path_)
            for py_path in all_path_list:
                self.buildPyTree(cur_node, py_path)

        elif self.isTemplateModule(Path_):
            # Это модуль шаблона
            cur_node = PrjTemplateModule(CurPackage_)
            # Установить имя
            name = os.path.splitext(os.path.split(Path_)[1])[0]
            cur_node.name = name
            CurPackage_.addChild(cur_node)
            
        elif self.isInterfaceModule(Path_):
            # Это интерфейсный модуль
            cur_node = PrjInterfaceModule(CurPackage_)
            # Установить имя
            name = os.path.splitext(os.path.split(Path_)[1])[0]
            cur_node.name = name
            CurPackage_.addChild(cur_node)
            
        elif self.isResourceModule(Path_):
            # Это ресурсный модуль
            cur_node = PrjResourceModule(CurPackage_)
            # Установить имя
            name = os.path.splitext(os.path.split(Path_)[1])[0]
            cur_node.name = name
            CurPackage_.addChild(cur_node)
            
        elif self.isImageModule(Path_):
            # Это модуль библиотеки образов
            cur_node = PrjImageModule(CurPackage_)
            # Установить имя
            name = os.path.splitext(os.path.split(Path_)[1])[0]
            cur_node.name = name
            CurPackage_.addChild(cur_node)

        elif self.isFBModule(Path_):
            # Это модуль форм wxFormBuilder
            cur_node = PrjFBModule(CurPackage_)
            # Установить имя
            name = os.path.splitext(os.path.split(Path_)[1])[0]
            cur_node.name = name
            CurPackage_.addChild(cur_node)

        elif self.isXRCModule(Path_):
            # Это модуль форм, сгенерированных утилитой pywxrc (из XRC ресурса).
            cur_node = PrjXRCModule(CurPackage_)
            # Установить имя
            name = os.path.splitext(os.path.split(Path_)[1])[0]
            cur_node.name = name
            CurPackage_.addChild(cur_node)

        elif self.isModule(Path_):
            # Это модуль
            cur_node = PrjModule(CurPackage_)
            # Установить имя
            name = os.path.splitext(os.path.split(Path_)[1])[0]
            cur_node.name = name
            CurPackage_.addChild(cur_node)

        elif self.isFBP(Path_):
            # Это FBP файл
            cur_node = prj_fb.PrjWXFormBuilderProject(CurPackage_)
            # Установить имя
            name = os.path.splitext(os.path.split(Path_)[1])[0]
            cur_node.name = name
            CurPackage_.addChild(cur_node)

        elif self.isXRC(Path_):
            # Это XRC файл
            cur_node = prj_xrc.PrjXRCResource(CurPackage_)
            # Установить имя
            name = os.path.splitext(os.path.split(Path_)[1])[0]
            cur_node.name = name
            CurPackage_.addChild(cur_node)

        elif self.isWXCP(Path_):
            # Это WXCP файл
            cur_node = prj_wxcp.PrjWXCrafterProject(CurPackage_)
            # Установить имя
            name = os.path.splitext(os.path.split(Path_)[1])[0]
            cur_node.name = name
            CurPackage_.addChild(cur_node)
        else:
            log.warning(u'Не определен тип модуля <%s>' % Path_)

    def edit(self):
        """
        Редактирование пакета(редактирование __init__.py файла).
        """
        ide = self.getRoot().getParent().getIDE()
        if ide:
            py_file = os.path.join(os.path.dirname(self.getRoot().getPrjFileName()),
                                   '__init__.py')
            # Если файл не открыт, то открыть его
            if not ide.SelectFile(py_file):
                return ide.OpenFile(py_file, True, readonly=self.readonly)
            return True
        else:
            log.warning(u'Не определен IDE для редактирования модуля')
            
    def unlockAllPyFiles(self):
        """
        Разблокировать все *.py файлы.
        """
        for child in self.children:
            child.unlockAllPyFiles()

    def getPath(self):
        """
        Путь к папке модулей/проекта.
        """
        return os.path.dirname(self.getRoot().getPrjFileName())


class PrjPackage(prj_node.PrjFolder):
    """
    Пакет модулей.
    """
    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        prj_node.PrjFolder.__init__(self, Parent_)
        self.img = imglib.imgPackageClose
        self.img_extended = imglib.imgPackageOpen
        self.description = u'Пакет'
        self.name = u'package'
        self.include_nodes = [PrjModule,
                              prj_fb.PrjWXFormBuilderProject,
                              prj_xrc.PrjXRCResource,
                              prj_wxcp.PrjWXCrafterProject,
                              prj_resource.PrjTabRes, prj_resource.PrjDBRes,
                              prj_resource.PrjFrmRes, prj_resource.PrjWinRes,
                              prj_resource.PrjMenuRes, prj_resource.PrjTemplate,
                              prj_resource.PrjMethod]
        self.include_folder = PrjPackage

    def onNodePopup(self, event):
        """
        Вызов всплывающего меню узла.
        """
        from . import menuModNode

        popup_menu = menuModNode.icMenuModNode(self)
        popup_menu.Popup(wx.GetMousePosition(), self._root.getParent())

    def create(self, new_name=None):
        """
        Создание пакета.
        @param new_name: Указание нового имени созданного узла.
        """
        # Ввести наименование при создании
        if not new_name:
            new_name = ic_dlg.icTextEntryDlg(self.getPrjTreeCtrl(), title=u'НАИМЕНОВАНИЕ',
                                             prompt_text=u'Введите наименование пакета', default_value=self.name)
        if new_name:
            self.name = new_name

        try:
            # Создание пакета ведет к созданию пакета Python.
            path = self.getPath()
            ok = self.getRoot().prj_res_manager.addPackage(path)
            self.getRoot().save()
            return ok
        except:
            log.fatal(u'Ошибка создания пакета <%s>' % self.name)
            return False
        
    def rename(self, OldName_, NewName_):
        """
        Переименование пакета.
        """
        old_path = self.getPath()
        self.name = NewName_
        new_path = self.getPath()
        if os.path.isdir(old_path):
            os.rename(old_path, new_path)
        # Для синхронизации дерева проекта
        self.getRoot().save()
        return True
        
    def getPath(self, CurPath_=None):
        """
        Путь пакета.
        """
        if CurPath_ is None:
            CurPath_ = self.name
        if issubclass(self._Parent.__class__, PrjPackage):
            CurPath_ = os.path.join(self._Parent.getPath(), CurPath_)
        elif issubclass(self._Parent.__class__, PrjModules):
            CurPath_ = ic_file.AbsolutePath(os.path.join('.', self.getRoot().name, CurPath_),
                                            os.path.split(os.path.dirname(self.getRoot().getPrjFileName()))[0])
        # log.debug(u'Путь до пакета <%s>' % CurPath_)
        return CurPath_
            
    def getModuleName(self):
        """
        Имя __init__ файла.
        """
        return '__init__'
        
    def edit(self):
        """
        Редактирование пакета(редактирование __init__.py файла).
        """
        ide = self.getRoot().getParent().getIDE()
        if ide:
            pack_dir = self.getPath()
            py_file = os.path.join(pack_dir, '__init__.py')
            # Сначала разблокировать все модули
            self.getRoot().unlockAllPyFilesInIDE()
            if not ide.SelectFile(py_file):
                # Заблокировать файл
                parent_pack = os.path.basename(os.path.dirname(pack_dir))
                ic_res.lockRes(self.name, parent_pack, 'py',
                               self.getRoot().lock_dir)
                return ide.OpenFile(py_file, True, readonly=self.readonly)
            return True
        else:
            log.warning(u'Не определен IDE для редактирования модуля')

    def unlockAllPyFiles(self):
        """
        Разблокировать все *.py файлы.
        """
        # Разблокировать себя
        py_file = os.path.join(self.getPath(), '__init__.py')
        self.getRoot().unlockPyFileInIDE(py_file)
        # Разблокировать все дочерние файлы/пакеты
        for child in self.children:
            child.unlockAllPyFiles()

    def delete(self):
        """
        Удалить пакет.
        """
        # Затем удалить из дерева
        prj_node.PrjNode.delete(self)
        # И в конце удалить папку пакета, если она есть
        package = self.getPath()
        # Выгрузить из редакторов
        self.getRoot().getParent().getIDE().CloseFile(os.path.join(package, '__init__.py'))

        # Удалить все блокировки
        self.getRoot().unlockAllPyFilesInIDE()

        if os.path.exists(package):
            shutil.rmtree(package, 1)
        # Для синхронизации дерева проекта
        self.getRoot().save()
            
    def cut(self):
        """
        Вырезать.
        """
        py_file = os.path.join(self.getPath(), '__init__.py')
        copy_py_file = self.getCopyModuleName()
        ic_file.icCopyFile(py_file, copy_py_file)
        me_node = prj_node.PrjNode.cut(self)
        self.delete()
        return me_node
        
    def copy(self):
        """
        Копировать.
        """
        py_file = os.path.join(self.getPath(), '__init__.py')
        copy_node = prj_node.PrjNode.copy(self)
        copy_py_file = copy_node.getCopyModuleName()
        ic_file.icCopyFile(py_file, copy_py_file)
        return copy_node
        
    def paste(self, Node_):
        """
        Вставить.
        @param Node_: Вставляемый узел.
        """
        # Можно вставлять толко модули или другие пакеты
        if issubclass(Node_.__class__, PrjModule) or \
           issubclass(Node_.__class__, PrjPackage):
            prj_node.PrjNode.paste(self, Node_)

            mod_name = Node_.getModuleName()
            mod_path = Node_.getPath()
            # Есть уже модуль с таким именем?
            if self.getRoot().prj_res_manager.isModByName(mod_name):
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!', 
                                u'Модуль <%s> уже существует!' % mod_name)
                return False
            # Добавить модуль в ресурс проекта
            Node_.getRoot().prj_res_manager.addModule(mod_name, mod_path)
            module_file_name = os.path.join(mod_path, mod_name+'.py')
            copy_module_file_name = Node_.getCopyModuleName()
            ok = False
            if os.path.exists(copy_module_file_name):
                ok = ic_file.icCopyFile(copy_module_file_name, module_file_name)
                os.remove(copy_module_file_name)
            
            # Для синхронизации дерева проекта
            Node_.getRoot().save()
            return ok
        return False

    def getCopyModuleName(self):
        return os.path.join(self.getPath(), '__init__.bak')


class PrjModule(prj_node.PrjNode):
    """
    Модуль/Функционал.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        prj_node.PrjNode.__init__(self, Parent_)
        self.description = u'Модуль'
        self.name = 'new_module'
        self.img = imglib.imgEdtModule

        # Расширение файла модуля
        self.ext = '.py'

    def getModuleName(self):
        return self.name
        
    def getModulePath(self):
        """
        Путь до модуля.
        """
        module_path = ''
        # Если родитель - пакет, то дабывить его в путь
        if issubclass(self._Parent.__class__, PrjPackage):
            module_path = self._Parent.getPath()
        elif issubclass(self._Parent.__class__, PrjModules):
            module_path = os.path.dirname(self.getRoot().getPrjFileName())
        # log.debug(u'Путь до модуля <%s>' % module_path)
        return module_path
        
    def getPath(self):
        return os.path.normpath(self.getModulePath())
        
    def getFullModuleFileName(self):
        return os.path.join(self.getPath(), self.getModuleName()+self.ext)
        
    def create(self, new_name=None):
        """
        Функция создания модуля.
        @param new_name: Указание нового имени созданного узла.
        """
        # Ввести наименование при создании
        if not new_name:
            new_name = ic_dlg.icTextEntryDlg(self.getPrjTreeCtrl(), title=u'НАИМЕНОВАНИЕ',
                                             prompt_text=u'Введите наименование модуля', default_value=self.name)
        if new_name:
            self.name = new_name

        mod_name = self.getModuleName()
        mod_path = self.getModulePath()
        # Есть уже модуль с таким именем?
        if self.getRoot().prj_res_manager.isModByName(mod_name):
            ic_dlg.icMsgBox(u'ВНИМАНИЕ!', 
                            u'Модуль <%s> уже существует!' % mod_name)
            return False
        # Добавить модуль в ресурс проекта
        self.getRoot().prj_res_manager.addModule(mod_name, mod_path)
        module_file_name = os.path.join(mod_path, mod_name+self.ext)
        ok = ic_res.CreatePyFile(module_file_name)
        # Для синхронизации дерева проекта
        self.getRoot().save()
        return ok
        
    def rename(self, OldName_, NewName_):
        """
        Переименование модуля.
        """
        old_path = self.getModulePath()
        old_py_file = os.path.join(old_path, OldName_+self.ext)
        self.name = NewName_
        new_path = self.getModulePath()
        new_py_file = os.path.join(new_path, NewName_+self.ext)
        if os.path.isfile(old_py_file):
            os.rename(old_py_file, new_py_file)
            # Закрыть модуль для редактирования
            ide = self.getRoot().getParent().getIDE()
            ide.CloseFile(old_py_file)
            # И опять открыть
            self.edit()
        # Для синхронизации дерева проекта
        self.getRoot().save()
        return True

    def edit(self):
        """
        Редактирование модуля.
        """
        # Определяем имя модуля
        py_dir = self.getModulePath()
        py_file = self.getFullModuleFileName()
        log.info(u'Редактирование модуля python <%s>' % py_file)

        # Определяем IDE
        ide = self.getRoot().getParent().getIDE()
        if ide:
            # Сначала разблокировать все модули
            self.getRoot().unlockAllPyFilesInIDE()
            if ide.IsOpenedFile(py_file):
                ide.CloseFile(py_file)
            else:
                parent_pack = os.path.basename(py_dir)
                # Если модуль заблокирован,
                # тогда открыть его только для просмотра
                if ic_res.isLockRes(self.name, parent_pack, 'py',
                                    self.getRoot().lock_dir):
                    lock_rec = ic_res.getLockResRecord(self.name, parent_pack,
                                                       'py', self.getRoot().lock_dir)

                    lock_user = lock_rec.get('user', u'Не определен') if lock_rec else u'Не определен'
                    lock_computer = lock_rec.get('computer', u'Не определен') if lock_rec else u'Не определен'
                    ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                                    u'Ресурс <%s> заблокирован пользователем <%s>. Компьютер: <%s>.' % (self.name, 
                                                                                                        lock_user,
                                                                                                        lock_computer))
                    self.readonly = True
                else:
                    # Заблокировать файл
                    ic_res.lockRes(self.name, parent_pack, 'py',
                                   self.getRoot().lock_dir)
                
            # Условие открытия в редакторе ресурса
            if self.isResClass(py_file):
                self.getRoot().getParent().res_editor.SetResource(self.name,
                                                                  py_dir, self.name, 'py', bEnable=True)

            return ide.OpenFile(py_file, True, readonly=self.readonly)
        else:
            log.warning(u'Не определен IDE для редактирования модуля')

        return False

    def onNodePopup(self, event):
        """
        Вызов всплывающего меню узла.
        """
        from . import menuModNode

        if not self.readonly:
            popup_menu = menuModNode.icMenuModNode(self)
            popup_menu.Popup(wx.GetMousePosition(), self._root.getParent())

    def unlockAllPyFiles(self):
        """ 
        Разблокировать все *.py файлы.
        """
        # Разблокировать себя
        py_file = os.path.join(self.getModulePath(),
                               self.getModuleName()+self.ext)
        self.getRoot().unlockPyFileInIDE(py_file)
            
    def delete(self):
        """
        Удалить модуль.
        """
        # ВОЗМОЖНО ЭТОТ МОДУЛЬ ПРОПИСАН КАК РЕСУРС!!!
        # Сначала удалить из файла *.pro
        self.getRoot().prj_res_manager.delRes(self.name, 'py')
        # Затем удалить из дерева
        prj_node.PrjNode.delete(self)

        module_name = os.path.join(self.getModulePath(), self.name+self.ext)

        # Выгрузить из редакторов
        self.getRoot().getParent().getIDE().CloseFile(module_name)
        res_file_name = self.getRoot().getParent().res_editor.GetResFileName()
        if res_file_name and ic_file.SamePathWin(module_name, res_file_name):
            self.getRoot().getParent().res_editor.CloseResource()
            
        # Удалить все блокировки
        self.getRoot().unlockAllPyFilesInIDE()

        # И в конце удалить папку пакета, если она есть
        if os.path.exists(module_name):
            # ВНИМАНИЕ! Удаляем файл, но оставляем его бекапную версию
            # для возможного восстановления!
            ic_file.icCreateBAKFile(module_name)
            os.remove(module_name)
        # Для синхронизации дерева проекта
        self.getRoot().save()

    def cut(self):
        """
        Вырезать.
        """
        module_name = os.path.join(self.getModulePath(),
                                   self.name+self.ext)
        ic_file.icChangeExt(module_name, '.bak')
        me_node = prj_node.PrjNode.cut(self)
        self.delete()
        return me_node
        
    def copy(self):
        """
        Копировать.
        """
        module_name = os.path.join(self.getModulePath(),
                                   self.name+self.ext)
        copy_node = prj_node.PrjNode.copy(self)
        copy_module_name = copy_node.getCopyModuleName()
        ic_file.icCopyFile(module_name, copy_module_name)
        return copy_node
        
    def paste(self, Node_):
        """
        Вставить.
        @param Node_: Вставляемый узел.
        """
        # Можно вставлять толко модули или другие пакеты
        if issubclass(Node_.__class__, PrjModule) or \
           issubclass(Node_.__class__, PrjPackage):
            prj_node.PrjNode.paste(self, Node_)

            mod_name = Node_.getModuleName()
            mod_path = Node_.getPath()
            # Есть уже модуль с таким именем?
            if self.getRoot().prj_res_manager.isModByName(mod_name):
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!', 
                                u'Модуль <%s> уже существует!' % mod_name)
                return False
            # Добавить модуль в ресурс проекта
            Node_.getRoot().prj_res_manager.addModule(mod_name, mod_path)
            module_file_name = os.path.join(mod_path, mod_name+self.ext)
            copy_module_file_name = Node_.getCopyModuleName()
            ok = False
            if os.path.exists(copy_module_file_name):
                ok = ic_file.icCopyFile(copy_module_file_name, module_file_name)
                os.remove(copy_module_file_name)
            # Для синхронизации дерева проекта
            Node_.getRoot().save()
            return ok
        return False
        
    def isResClass(self, ModuleFileName_):
        """
        Проверка, является ли указанный модуль ресурсным классом.
        @param ModuleFileName_: Имя файла модуля.
        @return: Возвращает True/False.
        """
        ok = False
        module_lines = None
        module_file = None
        try:
            module_file = open(ModuleFileName_, 'rt')
            module_lines = module_file.readlines()
            module_file.close()
            module_lines = [line[:-1].strip() for line in module_lines]
        except:
            if module_file:
                module_file.close()
        if module_lines:
            ok = INTERFACE_MODULE_SIGNATURE in module_lines
        return ok
        
    def getCopyModuleName(self):
        return os.path.join(self.getPath(), self.name+'.bak')
  
    def getPopupHelpText(self):
        """
        Получить текст всплывающей помощи.
        """
        module_filename = u''
        try:
            module_filename = os.path.join(self.getModulePath(),
                                           self.name+self.ext)
            module_name = os.path.splitext(os.path.basename(module_filename))[0]
            # module = imp.load_source(module_name, module_filename)
            module = ic.utils.impfunc.loadSource(module_name, module_filename)
            if hasattr(module, '__doc__'):
                if wx.Platform == '__WXGTK__':
                    return module.__doc__.strip()
                elif wx.Platform == '__WXMSW__':
                    return str(module.__doc__.strip())
            return None
        except:
            err_txt = u'Ошибка импорта модуля <%s>' % module_filename
            log.error(err_txt)
            return err_txt


class PrjInterfaceModule(PrjModule):
    """
    Интерфейсный модуль.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        PrjModule.__init__(self, Parent_)
        self.description = _('Interface module')
        self.name = 'IInterface'
        self.img = imglib.imgEdtInterface

    def getFullResFileName(self):
        """
        Полное имя файла ресурса.
        """
        return os.path.normpath(os.path.join(self.getModulePath(),
                                             self.getModuleName()+self.ext))
        
    def getViewer(self, parent):
        """
        Просмотрщик узла.
        """
        from . import icresviewer
        return icresviewer.icResPrjNodeViewer(parent, self)
        
    def getMyRes(self):
        """
        Получить ресурс узла.
        """
        module = ic.utils.impfunc.reloadSource('interface_module', self.getFullResFileName())
        return {module.ic_class_name: module.resource}
    

class PrjTemplateModule(PrjModule):
    """
    Модуль шаблона.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        PrjModule.__init__(self, Parent_)
        self.description = u'Модуль шаблона'
        self.name = 'CTemplate'
        self.img = imglib.imgEdtTemplate


class PrjResourceModule(PrjModule):
    """
    Ресурсный модуль.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        PrjModule.__init__(self, Parent_)
        self.description = u'Модуль ресурса'
        self.name = 'res_module'
        self.img = imglib.imgEdtResModule


class PrjImageModule(PrjModule):
    """
    Модуль библиотеки образов.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        PrjModule.__init__(self, Parent_)
        self.description = u'Модуль библиотеки образов'
        self.name = 'img_module'
        self.img = imglib.imgEdtImgModule

    def getViewer(self, parent):
        """
        Просмотрщик узла.
        """
        from . import icimgmoduleviewer
        return icimgmoduleviewer.icImgModulePrjNodeViewer(parent, self)

    def edit(self):
        """
        Редактирование модуля.
        """
        ic_dlg.icWarningBox(u'ПРЕДУПРЕЖДЕНИЕ',
                            u'''Редактирование модуля библиотеки образов запрещено.
Модули библиотеки образов генерируются в редакторе библиотеки образов.''')


class PrjFBModule(PrjModule, wxfb_manager.icWXFormBuilderManager):
    """
    Модуль форм wxFormBuilder.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        PrjModule.__init__(self, Parent_)
        self.description = u'Модуль форм wxFormBuilder'
        self.name = 'fb_module'
        self.img = imglib.imgForm

        # self.readonly = True

    def edit(self):
        """
        Редактирование модуля.
        """
        ic_dlg.icWarningBox(u'ПРЕДУПРЕЖДЕНИЕ',
                            u'''Редактирование модуля форм wxFormBuilder запрещено.
Модули форм генерируются в среде wxFormBuilder.''')

    def onNodePopup(self, event):
        """
        Вызов всплывающего меню узла.
        """
        if not self.readonly:
            popup_menu = flatmenu.FlatMenu()
            ctrl = self._root.getParent()

            popup_menuitem_id = wx.NewId()
            item = flatmenu.FlatMenuItem(popup_menu, popup_menuitem_id,
                                         u'Удалить модуль формы', u'Удалить модуль формы',
                                         normalBmp=imglib.imgTrash)
            popup_menu.AppendItem(item)
            ctrl.Bind(wx.EVT_MENU, self.onDelFormModuleMenuItem, id=popup_menuitem_id)

            popup_menu.AppendSeparator()

            popup_menuitem_id = wx.NewId()
            item = flatmenu.FlatMenuItem(popup_menu, popup_menuitem_id,
                                         u'Сгенерировать модуль формы...', u'Сгенерировать модуль формы...',
                                         normalBmp=imglib.imgPy)
            popup_menu.AppendItem(item)
            ctrl.Bind(wx.EVT_MENU, self.onGenFormModuleMenuItem, id=popup_menuitem_id)

            popup_menuitem_id = wx.NewId()
            item = flatmenu.FlatMenuItem(popup_menu, popup_menuitem_id,
                                         u'Адаптация модуля форм wxFormBuilder', u'Адаптация модуля форм wxFormBuilder',
                                         normalBmp=imglib.imgConvert)
            popup_menu.AppendItem(item)
            ctrl.Bind(wx.EVT_MENU, self.onAdaptFormModuleMenuItem, id=popup_menuitem_id)

            popup_menu.Popup(wx.GetMousePosition(), ctrl)

    def onDelFormModuleMenuItem(self, event):
        """
        Удаление модуля формы.
        """
        self.delete()
        event.Skip()

    def onGenFormModuleMenuItem(self, event):
        """
        Запуск генерации модуля формы.
        """
        from ic.utils import py_gen

        fb_py_module_filename = self.getFullModuleFileName()
        py_gen.genPyForm_by_wxFBModule(fb_py_module_filename)

        prj_root = self.getRoot()
        prj_root.openPrj(prj_root.getPrjFileName())
        prj_root.getParent().Refresh()
        event.Skip()

    def onAdaptFormModuleMenuItem(self, event):
        """
        Запуск адаптации модуля формы wxFormBuilder.
        """
        fb_py_module_filename = self.getFullModuleFileName()
        result = self.adaptation_form_py(fb_py_module_filename)
        if not result:
            ic_dlg.icWarningBox(u'ОШИБКА', u'Ошибка адаптации модуля формы wxFormBuilder')
        else:
            ic_dlg.icMsgBox(u'АДАПТАЦИЯ', u'Адаптация модуля <%s> прошла успешно' % fb_py_module_filename)
        event.Skip()


class PrjXRCModule(PrjModule):
    """
    Модуль форм, сгенерированных утилитой pywxrc (из XRC ресурса).
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        PrjModule.__init__(self, Parent_)
        self.description = u'Модуль форм, сгенерированных утилитой pywxrc (из XRC ресурса)'
        self.name = 'xrc_module'
        self.img = imglib.imgForm

        # self.readonly = True

    def edit(self):
        """
        Редактирование модуля.
        """
        ic_dlg.icWarningBox(u'ПРЕДУПРЕЖДЕНИЕ',
                            u'''Редактирование модуля форм, сгенерированных утилитой pywxrc (из XRC ресурса), запрещено.
Модули форм генерируются средствами дизайнера XRC файла.''')

    def onNodePopup(self, event):
        """
        Вызов всплывающего меню узла.
        """
        if not self.readonly:
            popup_menu = flatmenu.FlatMenu()
            ctrl = self._root.getParent()

            popup_menuitem_id = wx.NewId()
            item = flatmenu.FlatMenuItem(popup_menu, popup_menuitem_id,
                                         u'Удалить модуль формы', u'Удалить модуль формы',
                                         normalBmp=imglib.imgTrash)
            popup_menu.AppendItem(item)
            ctrl.Bind(wx.EVT_MENU, self.onDelFormModuleMenuItem, id=popup_menuitem_id)

            popup_menu.Popup(wx.GetMousePosition(), ctrl)

    def onDelFormModuleMenuItem(self, event):
        """
        Удаление модуля формы.
        """
        self.delete()
        event.Skip()
