#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wx
import os
import os.path

from ic.bitmap import bmpfunc
from ic.dlg import ic_dlg

from ic.utils import ic_file
from ic.utils import ic_exec

from . import prj_node

__version__ = (0, 1, 1, 1)

_ = wx.GetTranslation


class PrjXRCResource(prj_node.PrjNode):
    """
    Файл ресурса форм XRC.
    """

    def __init__(self, parent=None):
        """ 
        Конструктор.
        """
        prj_node.PrjNode.__init__(self, parent)
        self.description = u'XRC. Файл ресурса форм'
        self.name = 'new_xrc'
        self.img = bmpfunc.createLibraryBitmap('application-form.png')

        self.ext = '.xrc'

    def edit(self):
        """ 
        Редактирование.
        """
        filename = self.getPath()
        if os.path.exists(filename):
            cmd = 'xrced --meta %s&' % filename
            ic_exec.doSysCmd(cmd)
        return True

    def create(self, new_name=None):
        """ 
        Функция создания.
        @param new_name: Указание нового имени созданного узла.
        """
        cmd = 'xrced --meta&'
        ic_exec.doSysCmd(cmd)
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
        return os.path.normpath(os.path.join(self.getModulePath(), '%s%s' % (self.name, self.ext)))

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

    def extend(self):
        """
        Дополнительные инструменты узла.
        """
        # В данном случае запуск генерации модуля форм
        xrc_filename = self.getPath()
        yes = ic_dlg.icAskBox(u'Генерация Python модуля', u'Сгенерировать Python модуль из XRC файла <%s>?' % xrc_filename)
        if yes:
            py_filename = os.path.join(os.path.dirname(xrc_filename),
                                       os.path.basename(xrc_filename).replace('.', '_')+'.py')
            cmd = 'pywxrc --python --output %s %s' % (py_filename, xrc_filename)
            ic_exec.doSysCmd(cmd)
            msg = u'Сгенерирован файл <%s>' % py_filename
            ic_dlg.icMsgBox(u'Генерация Python модуля', msg)

            # Переоткрыть проект
            prj_root = self.getRoot()
            prj_root.openPrj(prj_root.getPrjFileName())
            # Обновление дерева проектов
            prj_root.getParent().Refresh()
