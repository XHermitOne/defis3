#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Контрол древовидного представления фильтров с индикаторами узлов.
"""

import copy
import uuid
import os.path
import wx
from wx.lib.agw import flatmenu

from ic.log import log
from ic.bitmap import ic_bmp
from ic.dlg import ic_dlg
from ic.utils import ic_file
from ic.engine import treectrl_manager
from ic.engine import stored_ctrl_manager


# import ic

# from . import filter_builder_env
from . import filter_choicectrl
from . import filter_indicator
from . import filter_generate

# from ic.PropertyEditor import select_component_menu


__version__ = (0, 1, 1, 1)

# Значения по умолчанию
DEFAULT_ROOT_LABEL = u'...'
DEFAULT_NODE_LABEL = u'Новый узел'
DEFAULT_NODE_IMAGE_FILENAME = 'document.png'

# Пустая запись, прикрепленная к узлу
EMPTY_NODE_RECORD = {'__filter__': None, '__indicator__': None, 'label': u''}


class icFilterTreeCtrlProto(wx.TreeCtrl,
                            filter_indicator.icFilterIndicator,
                            treectrl_manager.icTreeCtrlManager,
                            stored_ctrl_manager.icStoredCtrlManager):
    """
    Контрол древовидного представления фильтров с индикаторами узлов.
    Абстрактный класс.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор
        """
        wx.TreeCtrl.__init__(self, *args, **kwargs)

        filter_indicator.icFilterIndicator.__init__(self)

        # По умолчанию создаем корневой элемент
        self.AddRoot(DEFAULT_ROOT_LABEL)
        root_data = copy.deepcopy(EMPTY_NODE_RECORD)
        root_data['label'] = DEFAULT_ROOT_LABEL
        self.setItemData_tree(ctrl=self, data=root_data)

        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.onItemRightClick)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onItemDoubleClick)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onItemSelectChanged)
        # ВНИМАНИЕ! Если необходимо удалить/освободить
        # ресуры при удалении контрола, то необходимо воспользоваться
        # событием wx.EVT_WINDOW_DESTROY
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)

        self._uuid = None

        # Имя файла хранения фильтров.
        self._save_filename = None

        # Окружение фильтра
        self._environment = None

        # Ограничение количества строк фильтруемого объекта.
        self._limit = None
        # Количество строк при привышении лимита
        self._over_limit = None

        # Текущий фильтр выбранного элемента
        self._cur_item_filter = None

    def _canEditFilter(self):
        return True

    def onDestroy(self, event):
        """
        При удалении панели. Обработчик события.
        ВНИМАНИЕ! Если необходимо удалить/освободить
        ресуры при удалении контрола, то необходимо воспользоваться
        событием wx.EVT_WINDOW_DESTROY.
        """
        self.saveFilters()
        event.Skip()

    def getUUID(self):
        if not self._uuid:
            self._uuid = self._genUUID()
        return self._uuid

    def _genUUID(self):
        """
        Генерация UUID.
        @return: UUID.
        """
        return str(uuid.uuid4())

    def getCurItemFilter(self):
        """
        Текущий полный фильтр.
        """
        return self._cur_item_filter

    def onItemRightClick(self, event):
        """
        Обработчик клика правой кнопки.
        """
        menu = self.createPopupMenu()
        if menu:
            menu.Popup(wx.GetMousePosition(), self)
        # select_component_menu.popup_component_flatmenu(parent=self)
        event.Skip()

    def editRootFilter(self, root_item=None):
        """
        Редактирование фильтра корневого элемента.
        @param root_item: Корневой элемент.
            Если не определен, то берется автоматически.
        @return: True/False.
        """
        if root_item is None:
            root_item = self.GetRootItem()
        if not self.isRootTreeItem(ctrl=self, item=root_item):
            # Если не корневой элемент, то пропустить обработку
            return False

        try:
            item_data = self.getItemData_tree(ctrl=self, item=root_item)
            cur_filter = item_data.get('__filter__', None)
            cur_filter = filter_choicectrl.get_filter_choice_dlg(parent=self,
                                                                 environment=self._environment,
                                                                 cur_filter=cur_filter)
            if cur_filter:
                item_data['__filter__'] = cur_filter
                return True
        except:
            log.fatal(u'Ошибка настройки фильтра корневого элемента')
        return False

    def onItemDoubleClick(self, event):
        """
        Обработчик двойного клика на элементе дерева.
        """
        item = event.GetItem()
        self.editRootFilter(root_item=item)
        event.Skip()

    def OnChange(self, event):
        """
        Смена фильтра.
        """
        log.error(u'Не определена функция <OnChange> в компоненте <%s>' % self.__class__.__name__)

    def onItemSelectChanged(self, event):
        """
        Обработчик изменения выбора элемента дерева.
        """
        item = event.GetItem()
        self._cur_item_filter = self.buildItemFilter(item)

        # Передать обработку компоненту
        self.OnChange(event)

        event.Skip()

    def buildItemFilter(self, item):
        """
        Построение полного фильтра, соответствующего указанному элементу дерева.
        @param item: Элемент дерева.
        @return: Собранная структура фильтра, соответствующего указанному элементу дерева.
        """
        item_data_path = self.getItemPathData(tree_ctrl=self, item=item)
        log.debug(u'Путь до элемента %s' % str(item_data_path))

        filters = list()
        if item_data_path:
            filters = [data.get('__filter__', None) for data in item_data_path if data.get('__filter__', None)]
        else:
            log.warning(u'Не определены структурные данные элемента дерева')
        grp_filter = filter_generate.create_filter_group_AND(*filters)
        return grp_filter

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

            rename_menuitem_id = wx.NewId()
            bmp = ic_bmp.createLibraryBitmap('textfield_rename.png')
            menuitem = flatmenu.FlatMenuItem(menu, rename_menuitem_id, u'Переименовать',
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onRenameMenuItem, id=rename_menuitem_id)

            moveup_menuitem_id = wx.NewId()
            bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_MENU,
                                           (treectrl_manager.DEFAULT_ITEM_IMAGE_WIDTH,
                                            treectrl_manager.DEFAULT_ITEM_IMAGE_HEIGHT))
            menuitem = flatmenu.FlatMenuItem(menu, moveup_menuitem_id, u'Переместить выше',
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onMoveUpMenuItem, id=moveup_menuitem_id)
            menuitem.Enable(not self.isFirstTreeItem(ctrl=self, item=cur_item))

            movedown_menuitem_id = wx.NewId()
            bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_MENU,
                                           (treectrl_manager.DEFAULT_ITEM_IMAGE_WIDTH,
                                            treectrl_manager.DEFAULT_ITEM_IMAGE_HEIGHT))
            menuitem = flatmenu.FlatMenuItem(menu, movedown_menuitem_id, u'Переместить ниже',
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onMoveDownMenuItem, id=movedown_menuitem_id)
            menuitem.Enable(not self.isLastTreeItem(ctrl=self, item=cur_item))

            menu.AppendSeparator()

            add_menuitem_id = wx.NewId()
            bmp = wx.ArtProvider.GetBitmap(wx.ART_PLUS, wx.ART_MENU,
                                           (treectrl_manager.DEFAULT_ITEM_IMAGE_WIDTH,
                                            treectrl_manager.DEFAULT_ITEM_IMAGE_HEIGHT))
            menuitem = flatmenu.FlatMenuItem(menu, add_menuitem_id, u'Добавить',
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onAddMenuItem, id=add_menuitem_id)
            menuitem.Enable(self._canEditFilter())

            del_menuitem_id = wx.NewId()
            bmp = wx.ArtProvider.GetBitmap(wx.ART_MINUS, wx.ART_MENU,
                                           (treectrl_manager.DEFAULT_ITEM_IMAGE_WIDTH,
                                            treectrl_manager.DEFAULT_ITEM_IMAGE_HEIGHT))
            menuitem = flatmenu.FlatMenuItem(menu, del_menuitem_id, u'Удалить',
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onDelMenuItem, id=del_menuitem_id)
            menuitem.Enable(self._canEditFilter())

            filter_menuitem_id = wx.NewId()
            bmp = ic_bmp.createLibraryBitmap('filter.png')
            cur_filter = item_data.get('__filter__', None) if item_data else None
            label = u'Фильтр: %s' % filter_choicectrl.get_str_filter(cur_filter) if cur_filter else u'Фильтр'
            menuitem = flatmenu.FlatMenuItem(menu, filter_menuitem_id, label,
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onFilterMenuItem, id=filter_menuitem_id)
            menuitem.Enable(self._canEditFilter())

            indicator_menuitem_id = wx.NewId()
            bmp = ic_bmp.createLibraryBitmap('traffic-light.png')
            cur_indicator = item_data.get('__indicator__', None) if item_data else None
            label = u'Индикатор: %s' % self.getLabelIndicator(cur_indicator) if cur_indicator else u'Индикатор'
            menuitem = flatmenu.FlatMenuItem(menu, indicator_menuitem_id, label,
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onIndicatorMenuItem, id=indicator_menuitem_id)
            menuitem.Enable(self._canEditFilter())

            return menu
        except:
            log.fatal(u'Ошибка создания меню управления деревом фильтров')
        return None

    def renameItem(self, cur_item=None):
        """
        Переименовать узел.
        @return: True/False.
        """
        try:
            if cur_item is None:
                cur_item = self.GetSelection()
            if cur_item:
                cur_label = self.GetItemText(cur_item)
                label = ic_dlg.icTextEntryDlg(self, u'ПЕРЕИМЕНОВАНИЕ', u'Наименование',
                                              cur_label)

                if label:
                    bmp = None
                    # bmp = ic_bmp.createLibraryBitmap(DEFAULT_NODE_IMAGE_FILENAME)
                    data_record = self.getItemData_tree(ctrl=self, item=cur_item)
                    data_record['label'] = label
                    self.SetItemText(cur_item, label)
                    return self.setItemData_tree(ctrl=self, item=cur_item, data=data_record)
            else:
                log.warning(u'Текущий элемент дерева не определен')
        except:
            log.fatal(u'Ошибка переименования фильтра')
        return False

    def onRenameMenuItem(self, event):
        """
        Переименовать узел. Обработчик.
        """
        # log.debug(u'Добавить фильтр. Обработчик.')
        self.renameItem()
        # event.Skip()

    def moveUpItem(self, cur_item=None):
        """
        Переместить узел выше по списку.
        @return: True/False.
        """
        try:
            if cur_item is None:
                cur_item = self.GetSelection()

            return self.moveUpTreeItem(ctrl=self, item=cur_item)
        except:
            log.fatal(u'Ошибка перемещения узла выше по списку')
        return False

    def onMoveUpMenuItem(self, event):
        """
        Переместить узел выше по списку. Обработчик.
        """
        # log.debug(u'Переместить узел выше по списку. Обработчик.')
        self.moveUpItem()
        # event.Skip()

    def moveDownItem(self, cur_item=None):
        """
        Переместить узел ниже по списку.
        @return: True/False.
        """
        try:
            if cur_item is None:
                cur_item = self.GetSelection()

            return self.moveDownTreeItem(ctrl=self, item=cur_item)
        except:
            log.fatal(u'Ошибка перемещения узла ниже по списку')
        return False

    def onMoveDownMenuItem(self, event):
        """
        Переместить узел ниже по списку. Обработчик.
        """
        # log.debug(u'Переместить узел ниже по списку. Обработчик.')
        self.moveDownItem()
        # event.Skip()

    def addFilter(self, cur_item=None):
        """
        Добавить фильтр.
        @return: True/Falseю
        """
        try:
            if cur_item is None:
                cur_item = self.GetSelection()
            if cur_item:
                label = ic_dlg.icTextEntryDlg(self, u'ДОБАВЛЕНИЕ', u'Наименование',
                                              DEFAULT_NODE_LABEL)

                if label:
                    bmp = None
                    # bmp = ic_bmp.createLibraryBitmap(DEFAULT_NODE_IMAGE_FILENAME)
                    data_record = copy.deepcopy(EMPTY_NODE_RECORD)
                    data_record['label'] = label
                    new_item = self.appendChildItem_tree_ctrl(ctrl=self, parent_item=cur_item, label=label,
                                                              image=bmp, data=data_record, select=True)
                    return True
            else:
                log.warning(u'Текущий элемент дерева не определен')
        except:
            log.fatal(u'Ошибка добавления фильтра')
        return False

    def onAddMenuItem(self, event):
        """
        Добавить фильтр. Обработчик.
        """
        # log.debug(u'Добавить фильтр. Обработчик.')
        self.addFilter()
        # event.Skip()

    def delFilter(self, cur_item=None):
        """
        Удалить фильтр.
        @return: True/False.
        """
        try:
            if cur_item is None:
                cur_item = self.GetSelection()

            return self.deleteItem_tree_ctrl(ctrl=self, item=cur_item, ask=True)
        except:
            log.fatal(u'Ошибка удаления фильтра')
        return False

    def onDelMenuItem(self, event):
        """
        Удалить фильтр. Обработчик.
        """
        self.delFilter()
        # event.Skip()

    def editFilter(self, cur_item=None):
        """
        Редактировать фильтр.
        @return: True/False.
        """
        try:
            if cur_item is None:
                cur_item = self.GetSelection()
            item_data = self.getItemData_tree(ctrl=self, item=cur_item)
            cur_filter = item_data.get('__filter__', None)
            cur_filter = filter_choicectrl.get_filter_choice_dlg(parent=self,
                                                                 environment=self._environment,
                                                                 cur_filter=cur_filter)
            if cur_filter:
                item_data['__filter__'] = cur_filter
                return True
        except:
            log.fatal(u'Ошибка настройки фильтра')
        return False

    def onFilterMenuItem(self, event):
        """
        Настроить фильтр. Обработчик.
        """
        self.editFilter()
        # event.Skip()

    def editItemIndicator(self, cur_item=None):
        """
        Редактировать индикатор.
        @return: True/False.
        """
        try:
            if cur_item is None:
                cur_item = self.GetSelection()
            item_data = self.getItemData_tree(ctrl=self, item=cur_item)
            cur_indicator = item_data.get('__indicator__', None)
            cur_indicator = self.editIndicator(parent=self, indicator=cur_indicator)
            if cur_indicator:
                item_data['__indicator__'] = cur_indicator
                return True
        except:
            log.fatal(u'Ошибка настройки индикатора')
        return False

    def onIndicatorMenuItem(self, event):
        """
        Настроить индикаторы. Обработчик.
        """
        self.editItemIndicator()
        # event.Skip()

    def getCurRecords(self):
        """
        Код получения набора записей, соответствующих фильтру для индикаторов.
        """
        log.error(u'Не определена функция <getCurRecords> в компоненте <%s>' % self.__class__.__name__)

    def saveFilters(self, save_filename=None):
        """
        Сохранить сведения об фильтрах в файле.
        @param save_filename: Имя файла хранения фильтров.
            Если не определен, то генерируется по UUID.
        @return:
        """
        if save_filename is None:
            save_filename = self._save_filename

        if save_filename:
            save_filename = os.path.normpath(save_filename)
        else:
            widget_uuid = self.getUUID()
            save_filename = os.path.join(ic_file.getPrjProfilePath(),
                                         widget_uuid + '.dat')

        filter_tree_data = self.getTreeData(ctrl=self)
        return self.save_data_file(save_filename=save_filename, save_data=filter_tree_data)

    def loadFilters(self, save_filename=None):
        """
        Загрузить фильтры.
        @param save_filename: Имя файла хранения фильтров.
            Если не определен, то генерируется по UUID.
        """
        if save_filename is None:
            save_filename = self._save_filename

        if save_filename:
            save_filename = os.path.normpath(save_filename)
        else:
            widget_uuid = self.getUUID()
            save_filename = os.path.join(ic_file.getPrjProfilePath(),
                                         widget_uuid + '.dat')

        filter_tree_data = self.load_data_file(save_filename=save_filename)
        # Построить дерево
        return self.setTreeData(ctrl=self, tree_data=filter_tree_data, label='label')


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

