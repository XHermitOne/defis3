#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Контрол древовидного представления фильтров с индикаторами узлов.
"""

import copy
import wx
from wx.lib.agw import flatmenu

from ic.log import log
from ic.bitmap import ic_bmp
from ic.engine import treectrl_manager
from ic.dlg import ic_dlg


# import ic

# from . import filter_builder_env
from . import filter_choicectrl

# from ic.PropertyEditor import select_component_menu


__version__ = (0, 1, 1, 1)

# Значения по умолчанию
DEFAULT_ROOT_LABEL = u'...'
DEFAULT_NODE_LABEL = u'Новый узел'
DEFAULT_NODE_IMAGE_FILENAME = 'document.png'

# Пустая запись, прикрепленная к узлу
EMPTY_NODE_RECORD = {'__filter__': None, '__indicator__': None}


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

        # Имя файла хранения фильтров.
        self._filter_filename = None

        # Окружение фильтра
        self._environment = None

        # Ограничение количества строк фильтруемого объекта.
        self._limit = None
        # Количество строк при привышении лимита
        self._over_limit = None

    def onItemRightClick(self, event):
        """
        Обработчик клика правой кнопки.
        """
        menu = self.createPopupMenu()
        if menu:
            menu.Popup(wx.GetMousePosition(), self)
        # select_component_menu.popup_component_flatmenu(parent=self)
        event.Skip()

    def createPopupMenu(self):
        """
        Создать всплывающее меню управления деревом фильтров.
        @return: Объект wx.Menu управления деревом фильтров.
        """
        try:
            cur_item = self.GetSelection()
            if not cur_item:
                log.warning(u'Не выбран элемент дерева')
                return None
            item_data = self.getItemData_tree(ctrl=self, item=cur_item)

            menu = flatmenu.FlatMenu()

            add_menuitem_id = wx.NewId()
            bmp = wx.ArtProvider.GetBitmap(wx.ART_PLUS, wx.ART_MENU,
                                           (treectrl_manager.DEFAULT_ITEM_IMAGE_WIDTH,
                                            treectrl_manager.DEFAULT_ITEM_IMAGE_HEIGHT))
            menuitem = flatmenu.FlatMenuItem(menu, add_menuitem_id, u'Добавить',
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onAddMenuItem, id=add_menuitem_id)

            del_menuitem_id = wx.NewId()
            bmp = wx.ArtProvider.GetBitmap(wx.ART_MINUS, wx.ART_MENU,
                                           (treectrl_manager.DEFAULT_ITEM_IMAGE_WIDTH,
                                            treectrl_manager.DEFAULT_ITEM_IMAGE_HEIGHT))
            menuitem = flatmenu.FlatMenuItem(menu, del_menuitem_id, u'Удалить',
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onDelMenuItem, id=del_menuitem_id)

            filter_menuitem_id = wx.NewId()
            bmp = ic_bmp.createLibraryBitmap('filter.png')
            cur_filter = item_data.get('__filter__', None) if item_data else None
            label = u'Фильтр: %s' % filter_choicectrl.get_str_filter(cur_filter) if cur_filter else u'Фильтр'
            menuitem = flatmenu.FlatMenuItem(menu, filter_menuitem_id, label,
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onFilterMenuItem, id=filter_menuitem_id)

            indicator_menuitem_id = wx.NewId()
            bmp = ic_bmp.createLibraryBitmap('traffic-light.png')
            menuitem = flatmenu.FlatMenuItem(menu, indicator_menuitem_id, u'Индикатор',
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onIndicatorMenuItem, id=indicator_menuitem_id)

            return menu
        except:
            log.fatal(u'Ошибка создания меню управления деревом фильтров')
        return None

    def onAddMenuItem(self, event):
        """
        Добавить фильтр. Обработчик.
        """
        # log.debug(u'Добавить фильтр. Обработчик.')
        try:
            cur_item = self.GetSelection()
            if cur_item:
                label = ic_dlg.icTextEntryDlg(self, u'ДОБАВЛЕНИЕ', u'Наименование',
                                              DEFAULT_NODE_LABEL)

                if label:
                    bmp = None
                    # bmp = ic_bmp.createLibraryBitmap(DEFAULT_NODE_IMAGE_FILENAME)
                    data_record = copy.deepcopy(EMPTY_NODE_RECORD)
                    new_item = self.appendChildItem_tree_ctrl(ctrl=self, parent_item=cur_item, label=label,
                                                              image=bmp, data=data_record, select=True)
            else:
                log.warning(u'Текущий элемент дерева не определен')
        except:
            log.fatal(u'Ошибка добавления фильтра')
        # event.Skip()

    def onDelMenuItem(self, event):
        """
        Удалить фильтр. Обработчик.
        """
        try:
            self.deleteItem_tree_ctrl(ctrl=self, ask=True)
        except:
            log.fatal(u'Ошибка удаления фильтра')
        # event.Skip()

    def onFilterMenuItem(self, event):
        """
        Настроить фильтр. Обработчик.
        """
        try:
            item_data = self.getSelectedItemData_tree(ctrl=self)
            cur_filter = item_data.get('__filter__', None)
            cur_filter = filter_choicectrl.get_filter_choice_dlg(parent=self,
                                                                 environment=self._environment,
                                                                 cur_filter=cur_filter)
            if cur_filter:
                item_data['__filter__'] = cur_filter
        except:
            log.fatal(u'Ошибка настройки фильтра')
        # event.Skip()

    def onIndicatorMenuItem(self, event):
        """
        Настроить индикаторы. Обработчик.
        """
        try:
            pass
        except:
            log.fatal(u'Ошибка настройки индикатора')
        # event.Skip()


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

