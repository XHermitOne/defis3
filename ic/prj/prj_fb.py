#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import os.path
import wx

from ic.bitmap import bmpfunc
from ic.utils import filefunc
from ic.editor import wxfb_manager
from ic.dlg import dlgfunc
from ic.log import log

from . import prj_node
from . import prj_module

__version__ = (0, 1, 3, 1)

_ = wx.GetTranslation


class icPrjWXFormBuilderProject(prj_node.icPrjNode,
                                wxfb_manager.icWXFormBuilderManager):
    """
    Проект wxFormBuilder.
    """
    def __init__(self, parent=None):
        """ 
        Конструктор.
        """
        prj_node.icPrjNode.__init__(self, parent)
        self.description = u'Проект wxFormBuilder'
        self.name = 'new_fb_project'
        # self.img = imglib.imgDesigner
        self.img = bmpfunc.createLibraryBitmap('wxformbuilder.png')

        # Расширение файла
        self.ext = '.fbp'

    def edit(self):
        """ 
        Редактирование.
        """
        filename = self.getPath()
        if os.path.exists(filename):
            self.open_project(filename)
        return True

    def create(self, new_name=None):
        """ 
        Функция создания.

        :param new_name: Указание нового имени созданного узла.
        """
        self.create_project()
        return True

    def delete(self):
        """
        Удалить.
        """
        # Вызвать метод предка
        prj_node.icPrjNode.delete(self)
        # И в конце удалить файл ресурса, если он есть
        res_file_name = os.path.join(self.getModulePath(),
                                     self.name + self.ext)

        # Удалить файл
        if os.path.exists(res_file_name):
            # ВНИМАНИЕ! Файл удаляем, но оставляем его бекапную версию!!!
            filefunc.createBAKFile(res_file_name)
            os.remove(res_file_name)
        # Для синхронизации дерева проекта
        self.getRoot().save()

    def getPath(self):
        return os.path.join(self.getModulePath(), '%s%s' % (self.name, self.ext))

    def getModulePath(self):
        """ 
        Путь до модуля.
        """
        from . import prj_module

        path = ''
        # Если родитель -пакет, то дабывить его в путь
        if issubclass(self._Parent.__class__, prj_module.icPrjPackage):
            path = self._Parent.getPath()
        elif issubclass(self._Parent.__class__, prj_module.icPrjModules):
            path = os.path.dirname(self.getRoot().getPrjFileName())
        return path

    def unlockAllPyFiles(self):
        """ 
        Разблокировать все *.py файлы.
        """
        # Разблокировать себя
        pass

    def getModuleName(self):
        return self.name

    def getCopyModuleName(self):
        module_name = self.getPath()
        module_name = os.path.splitext(module_name)[0] + '.bak'
        return module_name

    def cut(self):
        """
        Вырезать.
        """
        module_name = self.getPath()
        filefunc.changeExt(module_name, '.bak')
        me_node = prj_node.icPrjNode.cut(self)
        self.delete()
        return me_node

    def copy(self):
        """
        Копировать.
        """
        module_name = self.getPath()
        copy_node = prj_node.icPrjNode.copy(self)
        copy_module_name = copy_node.getCopyModuleName()
        filefunc.copyFile(module_name, copy_module_name)
        return copy_node

    def paste(self, node):
        """
        Вставить.

        :param node: Вставляемый узел.
        """
        # Можно вставлять толко модули или другие пакеты
        if issubclass(node.__class__, prj_module.icPrjModule) or \
           issubclass(node.__class__, prj_module.icPrjPackage) or \
           issubclass(node.__class__, self.__class__):
            prj_node.icPrjNode.paste(self, node)

            mod_name = node.getModuleName()
            # Есть уже модуль с таким именем?
            if self.getRoot().prj_res_manager.isModByName(mod_name):
                dlgfunc.openMsgBox(u'ВНИМАНИЕ!',
                                u'Модуль <%s> уже существует!' % mod_name)
                return False
            # Добавить модуль в ресурс проекта
            mod_path = node.getModulePath()
            node.getRoot().prj_res_manager.addModule(mod_name, mod_path)
            module_file_name = os.path.join(mod_path, mod_name + self.ext)
            copy_module_file_name = node.getCopyModuleName()
            ok = False
            if os.path.exists(copy_module_file_name):
                ok = filefunc.copyFile(copy_module_file_name, module_file_name)
                os.remove(copy_module_file_name)
            # Для синхронизации дерева проекта
            node.getRoot().save()
            return ok
        else:
            log.warning(u'Не корректный тип <%s> для вставки узла' % node.__class__.__name__)
        return False

    def rename(self, old_name, new_name):
        """
        Переименование модуля.
        """
        mod_path = self.getModulePath()
        old_filename = os.path.join(mod_path, old_name + self.ext)
        self.name = new_name
        new_filename = os.path.join(mod_path, new_name + self.ext)
        if os.path.isfile(old_filename):
            os.rename(old_filename, new_filename)
        # Для синхронизации дерева проекта
        self.getRoot().save()
        return True
