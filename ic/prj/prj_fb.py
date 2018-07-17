#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import wx
import ic.imglib.common as imglib

from ic.utils import ic_file
from ic.utils import ic_exec
from ic.utils import filefunc
from ic import config
from ic.log import log

from . import prj_node

__version__ = (0, 0, 2, 3)

_ = wx.GetTranslation


def run_wxformbuilder(filename=None):
    """
    Запуск wxFormBuilder.
    @param filename: Файл открываемый в wxFormBuilder.
        Если не указан, то ничего не открывается.
    @return: True/False
    """
    cmd = None
    if os.path.exists('/bin/wxformbuilder') or os.path.exists('/usr/bin/wxformbuilder'):
        cmd = 'wxformbuilder %s&' % filename if filename else 'wxformbuilder &'
    else:
        alter_wxfb_path = filefunc.normal_path(config.ALTER_WXFORMBUILDER)
        if os.path.exists(alter_wxfb_path):
            cmd = '%s %s&' % (alter_wxfb_path, filename) if filename else '%s &' % alter_wxfb_path
        else:
            log.warning(u'Альтернативный путь запуска wxFormBuilder <%s> не найден' % alter_wxfb_path)

    if cmd:
        ic_exec.icSysCmd(cmd)


class PrjWXFormBuilderProject(prj_node.PrjNode):
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
            run_wxformbuilder(filename)
        return True

    def create(self):
        """ 
        Функция создания.
        """
        run_wxformbuilder()
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
