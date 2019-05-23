#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Контрол управления деревом запросов к OLAP кубам OLAP сервера.
"""

import uuid
import copy
import os.path
import wx
import wx.gizmos
from wx.lib.agw import flatmenu

from ic.log import log
from ic.bitmap import ic_bmp
from ic.dlg import ic_dlg
from ic.utils import ic_file

from ic.engine import treectrl_manager
from ic.engine import stored_ctrl_manager
from ic.components import icwidget

from STD.controls import tree_item_indicator
from analitic.olap.cubes import edit_cubes_olap_srv_request_dlg

__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_OLAPQUERYTREECTRL = {'save_filename': None,  # Имя файла хранения запросов
                            'onChange': None,  # Код смены запроса
                            'olap_server': None,    # OLAP сервер

                            '__parent__': icwidget.SPC_IC_WIDGET,
                            '__attr_hlp__': {'save_filename': u'Имя файла хранения запросов',
                                             'onChange': u'Код смены запроса',
                                             'olap_server': u'OLAP сервер',
                                             },
                            }

# Значения по умолчанию
DEFAULT_ROOT_LABEL = u'...'
DEFAULT_NODE_LABEL = u'Новый узел'
DEFAULT_NODE_IMAGE_FILENAME = 'table.png'

# Пустая запись, прикрепленная к узлу
EMPTY_NODE_RECORD = {'__request__': None, '__indicator__': None, 'label': u''}


class icOLAPQueryTreeCtrlProto(wx.TreeCtrl,
                               tree_item_indicator.icTreeItemIndicator,
                               treectrl_manager.icTreeCtrlManager,
                               stored_ctrl_manager.icStoredCtrlManager):
    """
    Контрол управления деревом запросов к OLAP кубам OLAP сервера.
    Абстрактный класс.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        wx.TreeCtrl.__init__(self, *args, **kwargs)

        tree_item_indicator.icTreeItemIndicator.__init__(self)

        # По умолчанию создаем корневой элемент
        self.AddRoot(DEFAULT_ROOT_LABEL)
        root_data = copy.deepcopy(EMPTY_NODE_RECORD)
        root_data['label'] = DEFAULT_ROOT_LABEL
        self.setItemData_tree(ctrl=self, data=root_data)

        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.onItemRightClick)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onItemDoubleClick)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onItemSelectChanged)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.onItemExpanded)
        # ВНИМАНИЕ! Если необходимо удалить/освободить
        # ресурсы при удалении контрола, то необходимо воспользоваться
        # событием wx.EVT_WINDOW_DESTROY
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)

        # OLAP сервер
        self._OLAP_server = None

        self._uuid = None

        # Имя файла хранения дерева запросов
        self._save_filename = None

        # Текущий запрос выбранного элемента
        self._cur_item_request = None

    def setOLAPServer(self, olap_server):
        """
        Установить OLAP сервер.
        @param olap_server: OLAP сервер.
        """
        self._OLAP_server = olap_server

    def getOLAPServer(self):
        """
        Объект OLAP сервера.
        """
        return self._OLAP_server

    def _canEditOLAPRequest(self):
        return True

    def onDestroy(self, event):
        """
        При удалении панели. Обработчик события.
        ВНИМАНИЕ! Если необходимо удалить/освободить
        ресурсы при удалении контрола, то необходимо воспользоваться
        событием wx.EVT_WINDOW_DESTROY.
        """
        self.saveRequests()
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

    def getCurItemRequest(self):
        """
        Текущий полный запрос.
        """
        if self._cur_item_request is None:
            # Не определен полный запрос
            # считаем что это запрос корневого элемента
            self._cur_item_request = self.getItemRequest()
        return self._cur_item_request

    def getItemRequest(self, item=None):
        """
        Запрос, прикрепленный к элементу.
        @param item: Текущий обрабатываемый элемент.
            Если None, то берется корневой элемент.
        @return: Структура запроса или None если запрос не определен.
        """
        if item is None:
            item = self.GetRootItem()

        item_data = self.getItemData_tree(ctrl=self, item=item)
        return item_data.get('__request__', None) if item_data else None

    def getItemIndicator(self, item=None):
        """
        Индикатор, прикрепленный к элементу.
        @param item: Текущий обрабатываемый элемент.
            Если None, то берется корневой элемент.
        @return: Структура индикатора или None если индикатор не определен.
        """
        if item is None:
            item = self.GetRootItem()

        item_data = self.getItemData_tree(ctrl=self, item=item)
        return item_data.get('__indicator__', None) if item_data else None

    def onItemRightClick(self, event):
        """
        Обработчик клика правой кнопки.
        """
        menu = self.createPopupMenu()
        if menu:
            menu.Popup(wx.GetMousePosition(), self)
        # select_component_menu.popup_component_flatmenu(parent=self)
        event.Skip()

    def editRootRequest(self, root_item=None):
        """
        Редактирование запроса корневого элемента.
        @param root_item: Корневой элемент.
            Если не определен, то берется автоматически.
        @return: True/False.
        """
        if root_item is None:
            root_item = self.GetRootItem()
        if not self.isRootTreeItem(ctrl=self, item=root_item):
            # Если не корневой элемент, то пропустить обработку
            return False

        return self.editRequestItem(root_item)

    def onItemDoubleClick(self, event):
        """
        Обработчик двойного клика на элементе дерева.
        """
        item = event.GetItem()
        self.editRootRequest(root_item=item)
        self.refreshRootItemTitle()

        # Для обновления списка объектов
        self._cur_item_request = self.getItemRequest(item)
        self.OnChange(event)

        # event.Skip()

    def OnChange(self, event):
        """
        Смена запроса.
        """
        log.error(u'Не определена функция <OnChange> в компоненте <%s>' % self.__class__.__name__)

    def onItemSelectChanged(self, event):
        """
        Обработчик изменения выбора элемента дерева.
        """
        item = event.GetItem()
        self._cur_item_request = self.getItemRequest(item)

        # Передать обработку компоненту
        self.OnChange(event)

        event.Skip()

    def createPopupMenu(self):
        """
        Создать всплывающее меню управления деревом запросов.
        @return: Объект wx.Menu управления деревом запросов.
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
            menuitem.Enable(self._canEditOLAPRequest())

            del_menuitem_id = wx.NewId()
            bmp = wx.ArtProvider.GetBitmap(wx.ART_MINUS, wx.ART_MENU,
                                           (treectrl_manager.DEFAULT_ITEM_IMAGE_WIDTH,
                                            treectrl_manager.DEFAULT_ITEM_IMAGE_HEIGHT))
            menuitem = flatmenu.FlatMenuItem(menu, del_menuitem_id, u'Удалить',
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onDelMenuItem, id=del_menuitem_id)
            menuitem.Enable(self._canEditOLAPRequest())

            request_menuitem_id = wx.NewId()
            bmp = ic_bmp.createLibraryBitmap('table_lightning.png')
            # cur_request = item_data.get('__request__', None) if item_data else None
            label = u'Запрос: %s' % item_data.get('label', DEFAULT_ROOT_LABEL) if item_data else u'Запрос'
            menuitem = flatmenu.FlatMenuItem(menu, request_menuitem_id, label,
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onRequestMenuItem, id=request_menuitem_id)
            menuitem.Enable(self._canEditOLAPRequest())

            indicator_menuitem_id = wx.NewId()
            bmp = ic_bmp.createLibraryBitmap('traffic-light.png')
            cur_indicator = item_data.get('__indicator__', None) if item_data else None
            label = u'Индикатор: %s' % self.getLabelIndicator(cur_indicator) if cur_indicator else u'Индикатор'
            menuitem = flatmenu.FlatMenuItem(menu, indicator_menuitem_id, label,
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onIndicatorMenuItem, id=indicator_menuitem_id)
            menuitem.Enable(self._canEditOLAPRequest())

            return menu
        except:
            log.fatal(u'Ошибка создания меню управления деревом запросов')
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
            log.fatal(u'Ошибка переименования запроса')
        return False

    def onRenameMenuItem(self, event):
        """
        Переименовать узел. Обработчик.
        """
        # log.debug(u'Добавить запрос. Обработчик.')
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

    def addRequestItem(self, cur_item=None):
        """
        Добавить OLAP запрос.
        @return: True/False.
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
            log.fatal(u'Ошибка добавления запроса')
        return False

    def onAddMenuItem(self, event):
        """
        Добавить запрос. Обработчик.
        """
        # log.debug(u'Добавить запрос. Обработчик.')
        self.addRequestItem()
        # event.Skip()

    def delRequestItem(self, cur_item=None):
        """
        Удалить запрос.
        @return: True/False.
        """
        try:
            if cur_item is None:
                cur_item = self.GetSelection()

            return self.deleteItem_tree_ctrl(ctrl=self, item=cur_item, ask=True)
        except:
            log.fatal(u'Ошибка удаления запроса')
        return False

    def onDelMenuItem(self, event):
        """
        Удалить запрос. Обработчик.
        """
        self.delRequestItem()
        # event.Skip()

    def editRequestItem(self, cur_item=None):
        """
        Редактировать запрос.
        @return: True/False.
        """
        try:
            if cur_item is None:
                cur_item = self.GetSelection()
            item_data = self.getItemData_tree(ctrl=self, item=cur_item)
            cur_request = item_data.get('__request__', None)
            cur_request = edit_cubes_olap_srv_request_dlg.edit_cubes_olap_srv_request_dlg(parent=self,
                                                                                          olap_srv=self.getOLAPServer(),
                                                                                          olap_srv_request=cur_request)
            if cur_request:
                item_data['__request__'] = cur_request
                return True
        except:
            log.fatal(u'Ошибка настройки запроса')
        return False

    def refreshRootItemTitle(self):
        """
        Обновить надпись корневого элемента в соответствии с выбранным запросом.
        @return: True/False.
        """
        item = self.GetRootItem()
        item_data = self.getItemData_tree(ctrl=self, item=item)
        label = item_data.get('label', None)
        if not label:
            label = DEFAULT_ROOT_LABEL
        self.setRootTitle(tree_ctrl=self, title=label)
        return True

    def onRequestMenuItem(self, event):
        """
        Настроить запрос. Обработчик.
        """
        self.editRequestItem()

        # После редактирования запроса если это корневой элемент,
        # то поменять надпись корневого элемента
        cur_item = self.GetSelection()
        if self.isRootTreeItem(ctrl=self, item=cur_item):
            self.refreshRootItemTitle()

        # Для обновления списка объектов
        self._cur_item_filter = self.getItemRequest(cur_item)
        self.OnChange(event)

        # event.Skip()

    def editRequestIndicatorItem(self, cur_item=None):
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
        self.editIndicatorItem()
        # event.Skip()

    def saveRequests(self, save_filename=None):
        """
        Сохранить сведения об запросах в файле.
        @param save_filename: Имя файла хранения дерева запросов.
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

        request_tree_data = self.getTreeData(ctrl=self)
        return self.save_data_file(save_filename=save_filename, save_data=request_tree_data)

    def loadRequests(self, save_filename=None):
        """
        Загрузить запросы.
        @param save_filename: Имя файла хранения дерева запросов.
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

        request_tree_data = self.load_data_file(save_filename=save_filename)
        # Построить дерево
        result = self.setTreeData(ctrl=self, tree_data=request_tree_data, label='label')

        # Установить надпись корневого элемента как надпись запроса
        if request_tree_data is None:
            request_tree_data = copy.deepcopy(EMPTY_NODE_RECORD)
        str_request = request_tree_data.get('label', DEFAULT_ROOT_LABEL)
        root_label = str_request if str_request else DEFAULT_ROOT_LABEL
        self.setRootTitle(tree_ctrl=self, title=root_label)

        return result

    def refreshIndicators(self, bVisibleItems=True, item=None):
        """
        Обновить индикаторы элементов дерева.
        @param bVisibleItems: Обновлять индикаторы видимых элементов дерева?
            Если нет, то обновляются индикаторы всех элементов.
        @param item: Текущий обрабатываемый элемент.
            Если None, то берется корневой элемент.
        @return: True/False.
        """
        try:
            return self._refreshIndicators(bVisibleItems, item=item)
        except:
            log.fatal(u'Ошибка обновления индикаторов дерева запросов')
        return False

    def _refreshIndicators(self, bVisibleItems=True, item=None):
        """
        Обновить индикаторы элементов дерева.
        @param bVisibleItems: Обновлять индикаторы видимых элементов дерева?
            Если нет, то обновляются индикаторы всех элементов.
        @param item: Текущий обрабатываемый элемент.
            Если None, то берется корневой элемент.
        @return: True/False.
        """
        if item is None:
            item = self.GetRootItem()

        item_indicator = self.getItemIndicator(item=item)
        # log.debug(u'Индикатор элемента %s : %s' % (str(item_indicator), self.IsVisible(item)))
        if item_indicator:
            if bVisibleItems:
                if self.IsVisible(item):
                    self.refreshIndicator(item_indicator, item=item)
                else:
                    # Если обрабатываем только видимые элементы
                    # а текущий элемент не видим, то нет необходимости
                    # обрабатывать дочерние элементы
                    return True
            else:
                self.refreshIndicator(item_indicator, item=item)

        # Обработка дочерних элементов
        if self.IsExpanded(item):
            children = self.getItemChildren(ctrl=self, item=item)
            for child in children:
                self._refreshIndicators(bVisibleItems, item=child)

        return True

    def refreshIndicator(self, indicator, item=None):
        """
        Обновить индикатор элемента дерева.
        @param indicator: Структура описания индикатора.
        @param item: Текущий обрабатываемый элемент.
            Если None, то берется корневой элемент.
        @return: True/False.
        """
        try:
            # log.debug(u'Обновление индикатора %s' % str(indicator))
            return self._refreshIndicator(indicator=indicator, item=item)
        except:
            log.fatal(u'Ошибка обновления индикатора элемента дерева')
        return False

    def _refreshIndicator(self, indicator, item=None):
        """
        Обновить индикатор элемента дерева.
        @param indicator: Структура описания индикатора.
        @param item: Текущий обрабатываемый элемент.
            Если None, то берется корневой элемент.
        @return: True/False.
        """
        if not indicator:
            # Индикатор не определен. Обновлять не надо
            return False

        if item is None:
            item = self.GetRootItem()

        # Сначала получаем набор записей узла, соответствующую элементу
        cur_request = self.getItemRequest(item=item)
        records = self.getCurRecords(item_filter=cur_request)

        # Затем получаем объекты индикатора
        name, bmp, txt_colour, bg_colour = self.getStateIndicatorObjects(records=records, indicator=indicator)

        # Устанавливаем параметры элемента
        if bmp:
            self.setItemImage_tree_ctrl(ctrl=self, item=item, image=bmp)

        if txt_colour:
            self.setItemForegroundColour(ctrl=self,item=item, colour=txt_colour)
        if bg_colour:
            self.setItemBackgroundColour(ctrl=self,item=item, colour=bg_colour)

        return True

    def onItemExpanded(self, event):
        """
        Обработчик развертывания элемента дерева.
        """
        item = event.GetItem()
        self.refreshIndicators(item=item)
