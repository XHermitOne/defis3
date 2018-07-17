#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from ic.bitmap import ic_bmp
from ic.dlg import ic_dlg

from ic.utils import ic_file
from ic.utils import ic_exec

from . import prj_node

__version__ = (0, 0, 1, 1)

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
        self.img = ic_bmp.createLibraryBitmap('application-form.png')

    def edit(self):
        """ 
        Редактирование.
        """
        filename = self.getPath()
        if ic_file.Exists(filename):
            cmd = 'xrced --meta %s&' % filename
            ic_exec.icSysCmd(cmd)
        return True

    def create(self):
        """ 
        Функция создания.
        """
        cmd = 'xrced --meta&'
        ic_exec.icSysCmd(cmd)
        return True

    def getPath(self):
        return ic_file.NormPathUnix(self.getModulePath()+'/%s.xrc' % self.name)

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
            path = ic_file.DirName(self.getRoot().getPrjFileName())
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
        xrc_filename = self.getFullResFileName()
        yes = ic_dlg.icAskBox(u'Генерация Python модуля', u'Сгенерировать Python модуль из XRC файла <%s>?' % xrc_filename)
        if yes:
            py_filename = ic_file.Join(ic_file.DirName(xrc_filename),
                                       ic_file.BaseName(xrc_filename).replace('.', '_')+'.py')
            cmd = 'pywxrc --python --output %s %s' % (py_filename, xrc_filename)
            ic_exec.icSysCmd(cmd)
            msg = u'Сгенерирован файл <%s>' % py_filename
            ic_dlg.icMsgBox(u'Генерация Python модуля', msg)

            # Переоткрыть проект
            prj_root = self.getRoot()
            prj_root.openPrj(prj_root.getPrjFileName())
            # Обновление дерева проектов
            prj_root.getParent().Refresh()
