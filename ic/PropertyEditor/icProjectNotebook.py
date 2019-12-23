#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль нотебука проекта.
"""

import wx
import os
import sys
import wx.lib.agw.flatnotebook as fnb

from ic.log import log
from ic.utils import impfunc

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

dir_name = os.path.split(dirName)[0]
if dir_name not in sys.path:
    sys.path = impfunc.addImportPath(dir_name)


__version__ = (0, 1, 1, 3)

_ = wx.GetTranslation


class icProjectNB(fnb.FlatNotebook):
    """
    Нотебук главного окна редактора проекта.
    """
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, *args, **kwargs):
        """
        Конструктор.

        :param parent: Родительское окно.
        :param pos: Позиция.
        :param size: Размер.
        """
        style = fnb.FNB_NODRAG | fnb.FNB_NO_X_BUTTON | fnb.FNB_VC71 | fnb.FNB_BACKGROUND_GRADIENT
        fnb.FlatNotebook.__init__(self, parent, *args, **kwargs)

        # Выставляем стили
        self.SetAGWWindowStyleFlag(style)
        # Цвет текста заголовка не активной страницы для контраста
        non_active_label_colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT)
        self.SetNonActiveTabTextColour(non_active_label_colour)
        
    def create_page(self, caption=u''):
        """
        Создать новую страницу нотебука.

        :param caption: Заголовок страницы.
        :return: Объект wx.Panel новой страницы нотебука.
        """
        page = wx.Panel(self)
        return page
        
    def add_project_page(self, page=None, title=u'Проект', *arg, **kwarg):
        """
        Добавляет страницу проекта, если ее нету.
        """
        self.AddPage(page or self.create_page(title), title)
    
    def add_property_page(self, page=None, title=u'Ресурс', *arg, **kwarg):
        """
        Добавляет страницу редактора ресурса.
        """
        self.AddPage(page or self.create_page(title), title)
        
    def setProjectEditor(self, edt):
        self._project_edt = edt

    def setResourceEditor(self, edt):
        self._res_edt = edt
            
    def init_notebook(self, prj_edt, res_edt, ifs):
        """
        Инициализация нотебука.

        :param prj_edt: Редактор проекта.
        :param res_edt: Редактор ресурса.
        :param ifs: Объект, реализующий интерфейс IDE.
        """
        prj_edt.type = 'PrjTree'
        self.add_project_page(prj_edt)
        self.add_property_page(res_edt)
    
        # Устанавливаем указатель на редакторы
        prj_edt.setResourceEditor(res_edt)
        self.setProjectEditor(prj_edt)
        self.setResourceEditor(res_edt)
        
        # Устанавливаем указатель на IDE
        if ifs is None:
            log.warning(u'Определяем объект IDE из редактора проекта')
            ifs = prj_edt.getIDE()

        if ifs is None:
            log.warning(u'Не определен объект, реализующий интерфейс IDE')
        res_edt.SetIDEInterface(ifs)
        # Устанавливаем указатель на панель групп
        res_edt.tree.SetPanelGroup(self)


def editor_main():
    app = wx.App()
    frm = wx.Frame(None, -1)
    nb = icProjectNB(frm)
    nb.add_project_page()
    nb.add_property_page()
    frm.Show()
    app.MainLoop()


if __name__ == '__main__':
    """
    Тестируем icProjectNotebook.
    """
    editor_main()
