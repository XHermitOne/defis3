#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Контрол древовидного представления фильтров с индикаторами узлов.
"""

import wx
from wx.lib.agw import flatmenu

from ic.log import log
from ic.bitmap import ic_bmp
from ic.engine import treectrl_manager


# import ic

# from . import filter_builder_env


__version__ = (0, 1, 1, 1)

DEFAULT_ROOT_LABEL = u'...'


class icFilterTreeCtrlProto(wx.TreeCtrl,
                            treectrl_manager.icTreeCtrlManager):
    """
    Контрол древовидного представления фильтров с индикаторами узлов.
    Абстрактный класс.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор
        """
        wx.TreeCtrl.__init__(self, *args, **kwargs)

        # По умолчанию создаем корневой элемент
        self.AddRoot(DEFAULT_ROOT_LABEL)

        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.onItemRightClick)

    def onItemRightClick(self, event):
        """
        Обработчик клика правой кнопки.
        """
        menu = self.createPopupMenu()
        if menu:
            menu.Popup(event.GetPosition(), self)
        event.Skip()

    def createPopupMenu(self):
        """
        Создать всплывающее меню управления деревом фильтров.
        @return: Объект wx.Menu управления деревом фильтров.
        """
        try:
            item = self.GetSelection()
            if not item:
                log.warning(u'Не выбран элемент дерева')
                return None
            item_data = self.GetItemData(item)

            menu = flatmenu.FlatMenu()
            menuitem_id = wx.NewId()
            bmp = wx.ArtProvider.GetBitmap(wx.ART_PLUS, wx.ART_MENU, (16, 16))
            menuitem = flatmenu.FlatMenuItem(menu, menuitem_id, u'Добавить узел',
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            # self.Bind(wx.EVT_MENU, self.onAddItem, id=menuitem_id)
            return menu
        except:
            log.fatal(u'Ошибка создания меню управления деревом фильтров')
        return None


def test():
    """
    Тестовая функция.
    """
    import copy
    # mwin = ic.getKernel().GetContext().getMainWin()
    print('TEST filter tree START ... ok')
    # env = copy.deepcopy(filter_builder_env.FILTER_ENVIRONMENT)

    app = wx.PySimpleApp()
    dlg = wx.Dialog(None, -1)
    ctrl = icFilterTreeCtrlProto(dlg, -1)
    # ctrl.setEnvironment(env)
    # ctrl.setDefault()
    dlg.ShowModal()
    app.MainLoop()

    print('TEST filter tree STOP ... ok')


if __name__ == '__main__':
    test()

