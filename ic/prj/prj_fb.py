#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import os.path
import wx

from ic.imglib import common as imglib
from ic.utils import ic_file
from ic.editor import wxfb_manager

from . import prj_node

__version__ = (0, 1, 2, 1)

_ = wx.GetTranslation


class PrjWXFormBuilderProject(prj_node.PrjNode,
                              wxfb_manager.icWXFormBuilderManager):
    """
    Проект wxFormBuilder.
    """

    def __init__(self, parent=None):
        """ 
        Конструктор.
        """
        prj_node.PrjNode.__init__(self, parent)
        self.description = u'Проект wxFormBuilder'
        self.name = 'new_fb_project'
        self.img = imglib.imgDesigner

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
        @param new_name: Указание нового имени созданного узла.
        """
        self.create_project()
        return True

    def delete(self):
        """
        Удалить.
        """
        # Вызвать метод предка
        prj_node.PrjNode.delete(self)
        # И в конце удалить файл ресурса, если он есть
        res_file_name = os.path.join(self.getModulePath(),
                                     self.name + self.ext)

        # Удалить файл
        if os.path.exists(res_file_name):
            # ВНИМАНИЕ! Файл удаляем, но оставляем его бекапную версию!!!
            ic_file.icCreateBAKFile(res_file_name)
            os.remove(res_file_name)
        # Для синхронизации дерева проекта
        self.getRoot().save()

    def getPath(self):
        # return ic_file.NormPathUnix(self.getModulePath()+'/%s.fbp' % self.name)
        return os.path.join(self.getModulePath(), '%s.fbp' % self.name)

    def getModulePath(self):
        """ 
        Путь до модуля.
        """
        from . import prj_module

        path = ''
        # Если родитель -пакет, то дабывить его в путь
        if issubclass(self._Parent.__class__, prj_module.PrjPackage):
            path = self._Parent.getPath()
        elif issubclass(self._Parent.__class__, prj_module.PrjModules):
            path = os.path.dirname(self.getRoot().getPrjFileName())
        return path

    def unlockAllPyFiles(self):
        """ 
        Разблокировать все *.py файлы.
        """
        # Разблокировать себя
        pass
