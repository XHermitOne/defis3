#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Контрол древовидного представления фильтров с индикаторами узлов.
"""

import copy
import uuid
import os.path
# import wx
from wx.lib.agw import flatmenu

# from ic.log import log
# from ic.bitmap import ic_bmp
from ic.dlg import ic_dlg
from ic.utils import filefunc
from ic.engine import treectrl_manager
from ic.engine import stored_ctrl_manager


# import ic

# from . import filter_builder_env
from . import filter_choicectrl
from ..controls.tree_item_indicator import *
from . filter_generate import *

# from ic.PropertyEditor import select_component_menu


__version__ = (0, 1, 3, 2)

# Значения по умолчанию
DEFAULT_ROOT_LABEL = u'...'
DEFAULT_NODE_LABEL = u'Новый узел'
DEFAULT_NODE_IMAGE_FILENAME = 'document.png'

# Пустая запись, прикрепленная к узлу
EMPTY_NODE_RECORD = {'__filter__': None, '__indicator__': None, 'label': u''}


# Функции управления структурой дерева фильтров
def empty_item(label=DEFAULT_NODE_LABEL):
    """
    Пустой узел.
    @param label: Надпись узла.
    @return: Структура пустого узла.
    """
    item_filter = copy.deepcopy(EMPTY_NODE_RECORD)
    item_filter['label'] = label
    return item_filter


def add_child_item_filter(filter_tree_data, child_item_filter=None):
    """
    Добавить узел как дочерний.
    @param filter_tree_data: Данные узла.
    @param child_item_filter: Данные дочернего узла.
        Если не определены, то создаются пустой узел.
    @return: Измененные данные узла.
    """
    if child_item_filter is None:
        child_item_filter = empty_item()

    if '__children__' not in filter_tree_data:
        filter_tree_data['__children__'] = list()
    filter_tree_data['__children__'].append(child_item_filter)
    return filter_tree_data


def new_item_filter(filter_tree_data, label=DEFAULT_NODE_LABEL):
    """
    Добавить новый фильтр к уже существующему узлу.
    @param filter_tree_data: Данные узла.
    @param label: Надпись узла.
    @return: Измененные данные узла.
    """
    if '__children__' not in filter_tree_data or filter_tree_data['__children__'] is None:
        filter_tree_data['__children__'] = list()

    item_filter = empty_item(label)
    return add_child_item_filter(filter_tree_data, item_filter)


def set_filter(filter_tree_data, item_filter=None):
    """
    Установить существующий фильтр узла.
    @param filter_tree_data: Данные узла.
    @param item_filter: Данные фильтра.
    @return: Измененные данные узла.
    """
    filter_tree_data['__filter__'] = item_filter
    return filter_tree_data


def set_indicator(filter_tree_data, item_indicator=None):
    """
    Установить существующий индикатор узла.
    @param filter_tree_data: Данные узла.
    @param item_indicator: Данные индикатора.
    @return: Измененные данные узла.
    """
    filter_tree_data['__indicator__'] = item_indicator
    return filter_tree_data


def get_filter(filter_tree_data):
    """
    Получить фильтр узла.
    @param filter_tree_data: Данные узла.
    @return: Структура фильтра узла.
    """
    return filter_tree_data['__filter__']


def get_indicator(filter_tree_data):
    """
    Получить индикатор узла.
    @param filter_tree_data: Данные узла.
    @return: Структура индикатора узла.
    """
    return filter_tree_data['__indicator__']


def set_label(filter_tree_data, label=u''):
    """
    Установить надпись узла.
    @param filter_tree_data: Данные узла.
    @param label: Надпись.
    @return: Измененные данные узла.
    """
    filter_tree_data['label'] = label
    return filter_tree_data


def find_label(filter_tree_data, label=u''):
    """
    Поиск узла по его надписи
    @param filter_tree_data: Данные узла.
    @param label: Надпись.
    @return: Данные искомого узла или None, если узел не найден.
    """
    if filter_tree_data.get('label', None) == label:
        return filter_tree_data
    if '__children__' in filter_tree_data and filter_tree_data['__children__']:
        for child in filter_tree_data['__children__']:
            find_result = find_label(child, label=label)
            if find_result:
                return find_result
    return None


class icFilterTreeCtrlProto(wx.TreeCtrl,
                            icTreeItemIndicator,
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
        # Флаг окончания полной инициализации контрола
        self._init_flag = False

        wx.TreeCtrl.__init__(self, *args, **kwargs)

        icTreeItemIndicator.__init__(self)

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

        self._uuid = None

        # Имя файла хранения фильтров.
        self._save_filename = None

        # Окружение фильтра
        self._environment = None

        # Ограничение количества строк фильтруемого объекта.
        self._limit = None
        # Количество строк при привышении лимита
        # self._over_limit = None

        # Текущий фильтр выбранного элемента
        self._cur_item_filter = None

    def _canEditFilter(self):
        return True

    def onDestroy(self, event):
        """
        При удалении панели. Обработчик события.
        ВНИМАНИЕ! Если необходимо удалить/освободить
        ресурсы при удалении контрола, то необходимо воспользоваться
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

    def getLimit(self):
        """
        Ограничение количества строк фильтруемого объекта.
        """
        return self._limit

    def setLimit(self, limit=0):
        """
        Установить ограничение количества строк фильтруемого объекта.
        @param limit: Ограничение по строкам. Если не определено, то ограничения нет.
        """
        self._limit = limit

    def getCurItemFilter(self):
        """
        Текущий полный фильтр.
        """
        if self._cur_item_filter is None:
            # Не определен полный фильтр
            # считаем что это фильтр корневого элемента
            self._cur_item_filter = self.getItemFilter()
        return self._cur_item_filter

    def getItemFilter(self, item=None):
        """
        Фильтр, прикрепленный к элементу.
        @param item: Текущий обрабатываемый элемент.
            Если None, то берется корневой элемент.
        @return: Структура фильтра или None если фильтр не определен.
        """
        if item is None:
            item = self.GetRootItem()

        item_data = self.getItemData_tree(ctrl=self, item=item)
        return item_data.get('__filter__', None) if item_data else None

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
        self.refreshRootItemTitle()

        # Для обновления списка объектов
        self._cur_item_filter = self.buildItemFilter(item)
        self.OnChange(event)

        # event.Skip()

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

    def _build_filters(self, cur_filters):
        """
        Внутренняя функция построения структуры фильтров.
        @param cur_filters: Текущий обрабатываемый список фильтров.
        @return: Собранная структура фильтра.
        """
        # Отфильтровать не включенные фильтры
        filters = [copy.deepcopy(cur_filter) for cur_filter in cur_filters if cur_filter.get('check', True)]

        # Обработка дочерних элементов производится сначала для исключения
        # пустых фильтров
        result_filters = list()
        for i, cur_filter in enumerate(filters):
            filter_type = cur_filter['type']
            children = cur_filter.get('children', list())
            children = self._build_filters(children)
            if children and filter_type == 'group':
                cur_filter['children'] = children
                result_filters.append(cur_filter)
            elif filter_type == 'compare':
                result_filters.append(cur_filter)

        return result_filters

    def buildItemFilter(self, item=None):
        """
        Построение полного фильтра, соответствующего указанному элементу дерева.
        @param item: Элемент дерева.
            Если не определен, то берется текущий выбранный элемент.
        @return: Собранная структура фильтра, соответствующего указанному элементу дерева.
        """
        if item is None:
            item = self.GetSelection()

        item_data_path = self.getItemPathData(tree_ctrl=self, item=item)
        # log.debug(u'Путь до элемента %s' % str(item_data_path))

        filters = list()
        if item_data_path:
            filters = [data.get('__filter__', None) for data in item_data_path if data.get('__filter__', None)]
            filters = self._build_filters(filters)
        else:
            log.warning(u'Не определены структурные данные элемента дерева')
        grp_filter = create_filter_group_AND(*filters)
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
            bmp = bmpfunc.createLibraryBitmap('textfield_rename.png')
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
            bmp = bmpfunc.createLibraryBitmap('filter.png')
            cur_filter = item_data.get('__filter__', None) if item_data else None
            label = u'Фильтр: %s' % filter_choicectrl.get_str_filter(cur_filter) if cur_filter else u'Фильтр'
            menuitem = flatmenu.FlatMenuItem(menu, filter_menuitem_id, label,
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onFilterMenuItem, id=filter_menuitem_id)
            menuitem.Enable(self._canEditFilter())

            indicator_menuitem_id = wx.NewId()
            bmp = bmpfunc.createLibraryBitmap('traffic-light.png')
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
                label = ic_dlg.getTextEntryDlg(self, u'ПЕРЕИМЕНОВАНИЕ', u'Наименование',
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

    def addFilterItem(self, cur_item=None):
        """
        Добавить фильтр.
        @return: True/False.
        """
        try:
            if cur_item is None:
                cur_item = self.GetSelection()
            if cur_item:
                label = ic_dlg.getTextEntryDlg(self, u'ДОБАВЛЕНИЕ', u'Наименование',
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
        self.addFilterItem()
        # event.Skip()

    def delFilterItem(self, cur_item=None):
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
        self.delFilterItem()
        # event.Skip()

    def editFilterItem(self, cur_item=None):
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

    def refreshRootItemTitle(self):
        """
        Обновить надпись корневого элемента в соответствии с выбранным фильтром.
        @return: True/False.
        """
        item = self.GetRootItem()
        item_data = self.getItemData_tree(ctrl=self, item=item)
        cur_filter = item_data.get('__filter__', None)
        label = filter_choicectrl.get_str_filter(cur_filter) if cur_filter else DEFAULT_ROOT_LABEL
        if not label:
            label = DEFAULT_ROOT_LABEL
        self.setRootTitle(tree_ctrl=self, title=label)
        return True

    def onFilterMenuItem(self, event):
        """
        Настроить фильтр. Обработчик.
        """
        self.editFilterItem()

        # После редактирования фильтра если это корневой элемент,
        # то поменять надпись корневого элемента
        cur_item = self.GetSelection()
        if self.isRootTreeItem(ctrl=self, item=cur_item):
            self.refreshRootItemTitle()

        # Для обновления списка объектов
        self._cur_item_filter = self.buildItemFilter(cur_item)
        self.OnChange(event)

        # event.Skip()

    def editIndicatorItem(self, cur_item=None):
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

    def getCurRecords(self, item_filter=None):
        """
        Код получения набора записей, соответствующих фильтру для индикаторов.
        @param item_filter: Описание фильтра элемента.
            Если None, то фильтрация не производится.
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
            save_filename = os.path.join(filefunc.getPrjProfilePath(),
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
            save_filename = os.path.join(filefunc.getPrjProfilePath(),
                                         widget_uuid + '.dat')

        filter_tree_data = self.load_data_file(save_filename=save_filename)
        # Построить дерево
        result = self.setTreeData(ctrl=self, tree_data=filter_tree_data, label='label')

        # Установить надпись корневого элемента как надпись фильтра
        root_filter = filter_tree_data.get('__filter__', dict())
        # log.debug(u'Фильтр: %s' % str(root_filter))
        str_filter = filter_choicectrl.get_str_filter(root_filter)
        root_label = str_filter if str_filter else DEFAULT_ROOT_LABEL
        self.setRootTitle(tree_ctrl=self, title=root_label)

        return result

    def acceptFilters(self):
        """
        Получить и установить дерево фильтров в контрол.
        """
        return self.loadFilters()

    def refreshIndicators(self, bVisibleItems=True, item=None, bRestoreDataset=True, bProgress=False):
        """
        Обновить индикаторы элементов дерева.
        @param bVisibleItems: Обновлять индикаторы видимых элементов дерева?
            Если нет, то обновляются индикаторы всех элементов.
        @param item: Текущий обрабатываемый элемент.
            Если None, то берется корневой элемент.
        @param bRestoreDataset: Восстановить датасет выбранного элемента?
        @param bProgress: Отображать прогресс диалог при обновлении?
        @return: True/False.
        """
        # log.debug(u'--- Обновление индикаторов ---')
        result = False
        try:
            if bProgress:
                if item is None:
                    item = self.GetRootItem()
                children_count = self.getItemChildrenCount(ctrl=self, item=item)
                ic_dlg.openProgressDlg(parent=self,
                                       title=u'ОБНОВЛЕНИЕ ИНДИКАТОРОВ',
                                       prompt_text=u'Обновление индикаторов...',
                                       min_value=0, max_value=children_count)
            # Сначала запоминаем выбранный элемент
            cur_item = self.GetSelection()
            # Обновляем все индикаторы
            result = self._refreshIndicators(bVisibleItems, item=item, bProgress=bProgress)

            if bRestoreDataset:
                # ВНИМАНИЕ! После обновления индикаторов необходимо восстановить
                # набор записей выбранного элемента
                cur_filter = self.buildItemFilter(item=cur_item)
                # log.debug(u'Фильтр элемента дерева фильтров %s' % str(cur_filter))
                self.getCurRecords(item_filter=cur_filter)
        except:
            log.fatal(u'Ошибка обновления индикаторов дерева фильтров')
        if bProgress:
            ic_dlg.closeProgressDlg()
        return result

    def _refreshIndicators(self, bVisibleItems=True, item=None, bProgress=False):
        """
        Обновить индикаторы элементов дерева.
        @param bVisibleItems: Обновлять индикаторы видимых элементов дерева?
            Если нет, то обновляются индикаторы всех элементов.
        @param item: Текущий обрабатываемый элемент.
            Если None, то берется корневой элемент.
        @param bProgress: Отображать прогресс диалог при обновлении?
        @return: True/False.
        """
        if item is None:
            item = self.GetRootItem()

        item_indicator = self.getItemIndicator(item=item)
        # log.debug(u'Индикатор элемента %s : %s' % (str(item_indicator), self.IsVisible(item)))
        if item_indicator:
            if bVisibleItems:
                if self.IsVisible(item):
                    self._refreshIndicator(item_indicator, item=item)
                else:
                    # Если обрабатываем только видимые элементы
                    # а текущий элемент не видим, то нет необходимости
                    # обрабатывать дочерние элементы
                    return True
            else:
                self._refreshIndicator(item_indicator, item=item)

        # Обработка дочерних элементов
        if self.IsExpanded(item):
            children = self.getItemChildren(ctrl=self, item=item)
            for child in children:
                self._refreshIndicators(bVisibleItems, item=child)
                if bProgress:
                    label = self.GetItemText(child)
                    ic_dlg.stepProgressDlg(new_prompt_text=u'Обновление индикатора... %s' % label)

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
        # ВНИМАНИЕ! Индикаторы обновляются по полному фильтру элемента
        cur_filter = self.buildItemFilter(item=item)
        records = self.getCurRecords(item_filter=cur_filter)

        # Затем получаем объекты индикатора
        name, bmp, txt_colour, bg_colour = self.getStateIndicatorObjects(records=records, indicator=indicator)

        # Устанавливаем параметры элемента
        if bmp:
            self.setItemImage_tree_ctrl(ctrl=self, item=item, image=bmp)

        if txt_colour:
            self.setItemForegroundColour(ctrl=self, item=item, colour=txt_colour)
        if bg_colour:
            self.setItemBackgroundColour(ctrl=self, item=item, colour=bg_colour)

        return True

    def onItemExpanded(self, event):
        """
        Обработчик развертывания элемента дерева.
        """
        # ВНИМАНИЕ! Индикацию дочерних элементов производить только в
        # случае когда произведена полная инициализация контрола
        if self._init_flag:
            item = event.GetItem()
            # log.debug(u'Развертывание элемента <%s> дерева фильтров' % str(item))
            self.refreshIndicators(item=item, bProgress=True)

        event.Skip()


def test():
    """
    Тестовая функция.
    """
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

