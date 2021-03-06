#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс пользовательского визуального компонента.
Компонент древовидного представления данных.
Работает с простой словарно-списковой структурой:
[
    {
    'name':Имя узла,
    'img': Файл картинки узла,
    'img_exp': Файл картинки раскрытого узла,
    'checkable': Может отмечаться пользователем?
    'children':[...], Список словарей дочерних узлов
    '__type__': Тип узла: 0 - обычный, 1- Отмечаеемый, 2- Переключаемый
    '__record__':Данные, прикреплямые к узлу  в виде списка.
    },
    ...
]

ПРИМЕЧАНИЕ!!!
Обработчик нажатия клавиши на дереве цепляется через
wx.EVT_TREE_KEY_DOWN, а не wx.EVT_KEY_DOWN, как у других компонентов.
"""

import wx
import wx.gizmos as gizmos

import wx.lib.agw.hypertreelist as hypertreelist
from wx.lib.agw import customtreectrl

from . import img_lst
from ic.log import log
from ic.utils import strfunc
from ic.dlg import dlgfunc
from ic.bitmap import bmpfunc

#   Версия компонента
__version__ = (0, 1, 1, 1)

_ = wx.GetTranslation

DEFAULT_ENCODING = 'utf-8'


class icColTreeInfo(hypertreelist.TreeListColumnInfo):
    """

    """
    def __init__(self, input='', width=hypertreelist._DEFAULT_COL_WIDTH, flag=wx.ALIGN_LEFT,
                 image=-1, shown=True, colour=None, edit=False):
        """
        Конструктор.
        :param input:
        :param width:
        :param flag:
        :param image:
        :param shown:
        :param colour:
        :param edit:
        """
        if isinstance(input, str):
            self._text = input
            self._width = width
            self._flag = flag
            self._image = image
            self._selected_image = -1
            self._shown = shown
            self._edit = edit
            self._font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            if colour is None:
                self._colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)
        else:
            self._text = input._text
            self._width = input._width
            self._flag = input._flag
            self._image = input._image
            self._selected_image = input._selected_image
            self._shown = input._shown
            self._edit = input._edit
            self._colour = input._colour
            self._font = input._font


class icSmartTreeListCtrl(hypertreelist.HyperTreeList):
    """ 
    Описание пользовательского компонента.
    """
    def __init__(self, parent, id, position, size, style, labels, wcols=None, **kwargs):
        """ 
        Конструктор базового класса пользовательских компонентов.
        """
        if wx.VERSION < (2, 8, 11, 0, ''):
            hypertreelist.HyperTreeList.__init__(self, parent, id, position, size, style=style)
        else:
            hypertreelist.HyperTreeList.__init__(self, parent, id, position, size,
                                                 agwStyle=style, style=style)
            
        self.setVistaStyle()

        if 'foregroundColor' in kwargs:
            foregroundColor = kwargs['foregroundColor']
            if isinstance(foregroundColor, tuple):
                self.SetForegroundColour(wx.Colour(*foregroundColor))

        if 'backgroundColor' in kwargs:
            backgroundColor = kwargs['backgroundColor']
            if isinstance(backgroundColor, tuple):
                self.SetBackgroundColour(wx.Colour(*backgroundColor))
        
        self.tree = []
        
        # Последний выбранный элемент дерева
        self._last_selection = None
        # Последний найденный элемент
        # self._last_find_item = None
        # Последняя найденная колонка
        self._last_find_col_idx = 0

        # self.spravDict = {}
        isz = (16, 16)
        # Установка списка образов компонентов
        self._img_list = img_lst.icImgList(self, isz[0], isz[1])
        self.fldridx, self.fldropenidx = self._img_list.setImgIdx('FOLDER', bmpfunc.createLibraryBitmap('folder.png'), bmpfunc.createLibraryBitmap('open_folder.png'))
        self.fileidx = self._img_list.setImgIdx('NEW_DOC', bmpfunc.createLibraryBitmap('document.png'))[0]
        self.curidx = self._img_list.setImgIdx('PAGE_COMMENT', bmpfunc.createLibraryBitmap('book_open.png'))[0]
        # self.SetImageList(self._img_list.getImageList())
        self.AssignImageList(self._img_list.getImageList())
        
        self.labels = labels if labels is not None else []

        # Установки колонок
        self.SetMainColumn(0)   # the one with the tree in it...
        
        for indx, label in enumerate(self.labels):
            # Перевод подписей колонок в строковое представление
            if wcols and len(wcols) > indx:
                w = wcols[indx]
            else:
                w = hypertreelist._DEFAULT_COL_WIDTH
                
            colInfo = icColTreeInfo(label, w, wx.ALIGN_LEFT, -1, True, None, False)            
            self.AddColumnInfo(colInfo)
                
        #   Определяем корень
        self.titleRoot = u''
        if 'titleRoot' in kwargs and kwargs['titleRoot']:
            self.titleRoot = kwargs['titleRoot']
        self.imgRoot = None
        if 'imgRoot' in kwargs and kwargs['imgRoot']:
            self.imgRoot = kwargs['imgRoot']
        self.imgExpRoot = None
        if 'imgExpRoot' in kwargs and kwargs['imgExpRoot']:
            self.imgExpRoot = kwargs['imgExpRoot']
        
        self.root = self.AddRoot(self.titleRoot)

        if self.imgRoot is None:
            self.SetItemImage(self.root, self.fldridx, which=wx.TreeItemIcon_Normal)
            self.SetItemImage(self.root, self.fldropenidx, which=wx.TreeItemIcon_Expanded)
        else:
            root_img_idx = self._img_list.setImgIdx('ROOT', self.imgRoot, self.imgExpRoot)
            self.SetItemImage(self.root, root_img_idx[0], which=wx.TreeItemIcon_Normal)
            if root_img_idx[1] >= 0:
                self.SetItemImage(self.root, root_img_idx[1], which=wx.TreeItemIcon_Expanded)

        self.setCheckRadio()
        if 'hideHeader' in kwargs and kwargs['hideHeader']:
            self.hideHeader()

        #   Регистрация обработчиков событий
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.onItemExpanded)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.onItemCollapsed)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onSelectChanged)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onItemActivated)
        self.Bind(wx.EVT_TREE_KEY_DOWN, self.OnTreeListKeyDown)
        self.Bind(customtreectrl.EVT_TREE_ITEM_CHECKED, self.onItemChecked)

        self.textload = wx.StaticText(self._main_win, -1, label=_('Load data ...'), pos=(70,70))
        self.textload.Show(False)        
            
    def begin_load(self):
        self.Enable(False)
        self.textload.Show(True)

    def end_load(self):
        self.textload.Show(False)
        self.Enable()
        
    def setVistaStyle(self):
        """
        Установка стиля Vista. Стиль по умолчанию.
        """
        self.EnableSelectionVista(True)        

    def expandAllRoot(self):
        """
        Раскрыть всю ветку от корня.
        """
        return self.ExpandAll()
        
    def getSelectionName(self):
        """
        Имя выбранного узла.
        """
        selection_item = self.GetSelection()
        return self.GetItemText(selection_item)
    
    def addNode(self, root, res, level=0, start_level=0):
        """
        Добавить дочерние узлы, описанные словарем.
        """
        id_pic, id_exp_pic = self._getPicturesId(res)
        
        if len(self.labels) == 1 and len(res['__record__']) > 1:
            st = u'  ' + (str(res['__record__'][1]) or '')
        else:
            st = u''
        node_ct_type = int(res.get('checkable', 0)) if 'checkable' in res else res.get('__type__', 0)
        child = self.AppendItem(root, res['name']+st, ct_type=node_ct_type)
        self.SetItemImage(child, id_pic, which=wx.TreeItemIcon_Normal)
        self.SetItemImage(child, id_exp_pic, which=wx.TreeItemIcon_Expanded)
        self.SetItemData(child, (level+start_level, res))
        if '__record__' in res:
            self.setItemRecord(child, res['__record__'])
        
        # Обработка дочерних элементов
        if 'children' in res and res['children']:
            for node in res['children']:
                self.addNode(child, node, level+1, start_level)
            
    def _isChildrenRes(self, res):
        """
        Есть ли в описании ресурса описание дочерних элементов?
        :param res: Ресурс.
        :return: Возвращает True/False.
        """
        if 'children' in res and res['children']:
            return True
        return False
        
    def _getPicturesId(self, res):
        """
        Определение картинок для изобращения узла по ресурсу этого узла.
        :param res: Ресурс узла.
        :return: Кортеж из 2-х элементов - идентификаторов картинок.
        """
        # Если нет дочерних элементов в описании, тогда картинки-файлы
        if not self._isChildrenRes(res):
            default_img_idx = (self.fileidx, self.curidx)
        else:
            default_img_idx = (self.fldridx, self.fldropenidx)

        if 'img' in res and res['img']:
            img_exp = None
            if 'img_exp' in res and res['img_exp']:
                img_exp = res['img_exp']
            img_idx = self._img_list.setImgIdx(res.get('img_id', res['name']), res['img'], img_exp)
            return img_idx
        
        return default_img_idx
        
    def setItemRecord(self, item, record):
        """
        Установить список записи на узле.
        :param item: ID узла у которого устанавливается запись.
        :param record: Запись узла. Список.
        """
        if record and self.isList(record):
            for idx, value in enumerate(record[1:]):
                if not isinstance(value, str):
                    value = str(value)
                self.SetItemText(item, value, idx + 1)
        return item
        
    def getItemRecord(self, item):
        """
        Список записи на узле.
        :param item: ID узла у которого устанавливается запись.
        :return: Возвращает список строк записи узла.
            Или None в случае ошибки.
        """
        try:
            item_py_data = self.GetItemData(item)
            if item_py_data is None:
                return None
            res = item_py_data[1]
            if isinstance(res, dict) and '__record__' in res:
                return res['__record__']
        except:
            log.fatal(u'ОШИБКА компонента %s метода getItemRecord' % self.name)
        return None

    def getSelectionRecord(self):
        """
        Список записи выбранного узла.
        :return: Возвращает список строк записи узла.
            Или None в случае ошибки.
        """
        selection_item = self.GetSelection()
        return self.getItemRecord(selection_item)
        
    def setLabelCols(self, label_cols):
        """
        Установить надписи колонок.
        :param label_cols: Надписи колонок. Список строк.
        :return: Возвращает результат выполнения функции True/False.
        """
        try:
            col_count = self.GetColumnCount()
            for i_col, col_label in enumerate(label_cols):
                if i_col < col_count:
                    self.SetColumnText(i_col, col_label)
                else:
                    break
            return True
        except:
            log.fatal(u'ОШИБКА компонента %s метода setLabelCols' % self.name)
        return False
        
    def getElementName(self, res, indx):
        """
        Возвращает имя элемента списка.
        """
        return u'Элемент %s:' % str(indx)
        
    def isDict(self, res):
        """
        Признак словарного интерфейса.
        """
        return isinstance(res, dict)

    def isList(self, res):
        """
        Признак интерфейса последовательности.
        """
        return isinstance(res, list)
        
    def clearRoot(self):
        """
        Полностью очистить содержимо корневого элемента.
        """
        root = self.GetRootItem()
        return self.DeleteChildren(root)
        
    def GetCount(self):
        tree = self.GetMainWindow()
        return tree.GetCount()
    
    def loadTree(self, tree_data=None, bAutoSelect=True, bAutoExpand=True):
        """
        Заполняем дерево.
        
        :type tree_data: C{list}
        :param tree_data: Словарно-списковая структура, отображаемая в дереве.
        :type bAutoSelect: C{bool}
        :param bAutoSelect: Автоматически выбрать последний элемент.
        :type bAutoExpand: C{bool}
        :param bAutoExpand: Автоматически развернуть корневой элемент.
        """
        # Если включен автовыбор элемента
        # то сначала сбросить выделение всех элементов
        if bAutoSelect:
            self.UnselectAll()
            
        if tree_data is None:
            tree_data = self.tree
        else:
            self.tree = tree_data
        
        self.DeleteChildren(self.root)
        self.SetItemData(self.root, (-1, tree_data))
        
        if tree_data is not None:
            for node in tree_data:
                self.addNode(self.root, node)
        else:
            self._testTree()
            
        # Автовыбор элемента
        if bAutoSelect:
            if self._last_selection:
                self.selectItemPath(self._last_selection)
            else:
                if not self.IsSelected(self.root):
                    self.SelectItem(self.root)
                
        # Авторазворачивание верхнего уровня
        if bAutoExpand:
            try:
                self.Expand(self.root)
            except:
                pass

        self.end_load()
        
    def selectItemPath(self, item_path, item=None):
        """
        Выбрать элемент по пути.
        :param item_path: Путь до элемента.
        :param item: Текущий элемент поиска.
            Если None, то поиск начиниется с корня.
        """
        if item is None:
            item = self.root
        if item_path:
            cur_item = self.FindItem(item, item_path[0])
            # Есть дочерние элементы
            if item_path[1:]:
                self.Expand(cur_item)
            return self.selectItemPath(item_path[1:], cur_item)
        if not self.IsSelected(item):
            return self.SelectItem(item)
        return None
        
    def getItemPath(self, item, path=None):
        """
        Путь до элемента. Путь - список имен элементов.
        :param item: Элемент дерева.
        :param path: Текущий заполненный путь.
        """
        parent = self.GetItemParent(item)
        # Если есть родительский элемент, то вызвать рекурсивно
        if parent:
            if path is None:
                path = []
            path.insert(-1, self.GetItemText(item))
            return self.getItemPath(parent, path)
        return path
        
    def reFresh(self):
        """
        Обновление дерева.
        """
        return self.loadTree(self.GetItemData(self.root)[1])
    
    def getItemChildren(self, item=None):
        """
        Список дочерних элементов узла дерева.
        :param item: Узел/элемент дерева. Если None, то корневой элемент.
        :return: Список дочерних элементов узла дерева
            или None в случае ошибки.
        """
        try:
            # Определить узел
            if item is None:
                item = self.root
                
            # Список дочерних элементов
            children = []

            children_count = self.GetChildrenCount(item, False)
            for i in range(children_count):
                if i == 0:
                    child, cookie = self.GetFirstChild(item)
                else:
                    child, cookie = self.GetNextChild(item, cookie)
                if child.IsOk():
                    children.append(child)
            return children
        except:
            log.error(u'ОШИБКА компонента %s метода определения списка дочерних элементов' % self.name)
            return None
        
    def findItemColumnString(self, string, item=None, columns=None, column_idx=0, bILike=True):
        """
        Функция ищет подстроку в массиве данных.
        :type string: C{string}
        :param string: Строка поиска
        :type item: C{int}
        :param item: Элемент дерева, с которого начинается поиск.
        :type columns: C{list}
        :param columns: Список колонок записи каждого элемента, по которым ведется поиск.
        :type column_idx: C{int}
        :param column_idx: Индекс текущей колонки из списка колонок.
        :type bILike: C{bool}
        :param bILike: Признак поиска без учета регистра. Если False - то поиск ведется
        на точное соответствие.
        :return: Возвращает кортеж (номер элемента дерева, где найдена искомая строка,
        индекс номера колонки, где найдена искомая строка).
        """
        try:
            # Текущий элемент дерева
            if item is None:
                item = self.root
                
            cur_item_rec = self.getItemRecord(item)
            # Колонки
            if columns is None and cur_item_rec:
                columns = range(column_idx, len(cur_item_rec))
                
            # Поискать в текущем элементе
            if columns:
                for i, col in enumerate(columns[column_idx:]):
                    if cur_item_rec:
                        # Получить значение поля
                        if bILike:
                            # Без учета регистра?
                            value = strfunc.toUpper(str(cur_item_rec[col]))
                            find_str = strfunc.toUpper(string)
                            find_col_idx = i
                        else:
                            value = str(cur_item_rec[col])
                            find_str = string
                            find_col_idx = i
                        # Проверка на совпадение подстроки
                        if find_str in value:
                            return item, find_col_idx
                        
            # Обработка дочерних элементов
            children = self.getItemChildren(item)
            if children:
                for child in children:
                    result = self.findItemColumnString(string, child, columns, 0, bILike)
                    if result is not None:
                        # Если нашли в дочерних элементах, то вернуть результат
                        return result

            # Ну если и в дочерних узлах не нашли,
            # то вызвать поиск для следующего элемента
            next = self.GetNextSibling(item)
            if next:
                if next.IsOk():
                    result = self.findItemColumnString(string, next, columns, 0, bILike)
                    if result is not None:
                        return result
            
            # Если не нашли в следующих элементах,
            # тогда поискать в следующем элементе родительского элемента
            parent_item = item.GetParent()
            if parent_item:
                parent_next = self.GetNextSibling(parent_item)
                if parent_next:
                    if parent_next.IsOk():
                        result = self.findItemColumnString(string, parent_next, columns, 0, bILike)
                        if result is not None:
                            return result
            
            # Все равно не нашли
        except:
            log.fatal(u'ОШИБКА компонента %s метода поиска узла по строке' % self.name)
        return None
        
    def selectFindItemColumn(self, string, columns=None, bILike=True):
        """
        Поиск и выделение пункта по строке.
        :type string: C{string}
        :param string: Строка поиска
        :type columns: C{list}
        :param columns: Список колонок записи каждого элемента, по которым ведется поиск.
        :type bILike: C{bool}
        :param bILike: Признак поиска без учета регистра. Если False - то поиск ведется
            на точное соответствие.
        :return: Возвращает номер элемента дерева, где найдена искомая строка.
        """
        cur_item = self.GetSelection()
        cur_item.Expand()

        if not cur_item.IsOk():
            cur_item = None
        find_result = self.findItemColumnString(string, item=cur_item,
                                                columns=columns,
                                                column_idx=self._last_find_col_idx,
                                                bILike=bILike)

        if find_result is not None:
            item, find_col_idx = find_result
            self._last_find_col_idx = find_col_idx + 1
            self.SelectItem(item)
        else:
            if dlgfunc.getAskDlg(u'ПОИСК', u'Строка <%s> не найдена. Начать поиск сначала?' % string) == wx.YES:
                # Начать поиск сначала
                find_result = self.findItemColumnString(string, None, columns, 0, bILike)
                if find_result is not None:
                    item, find_col_idx = find_result
                    self._last_find_col_idx = find_col_idx + 1
                    self.SelectItem(item)
        return None
        
    def findItemString(self, string, item=None, bILike=True):
        """
        Функция ищет подстроку в массиве данных. Поиск производится по
        надписям элементов.
        :type string: C{string}
        :param string: Строка поиска
        :type item: C{int}
        :param item: Элемент дерева, с которого начинается поиск.
        :type bILike: C{bool}
        :param bILike: Признак поиска без учета регистра. Если False - то поиск ведется
        на точное соответствие.
        :return: Возвращает кортеж (номер элемента дерева, где найдена искомая строка,
        индекс номера колонки, где найдена искомая строка).
        """
        try:
            # Текущий элемент дерева
            if item is None:
                item = self.root

            label = item.GetText()
            # Поискать в текущем элементе
            if label:
                # Получить значение
                if bILike:
                    # Без учета регистра?
                    value = strfunc.toUpper(label)
                    find_str = strfunc.toUpper(string)
                else:
                    value = label
                    find_str = string
                # Проверка на совпадение подстроки
                if find_str in value:
                    return item
                        
            # Обработка дочерних элементов
            children = self.getItemChildren(item)
            if children:
                for child in children:
                    result = self.findItemString(string, child, bILike)
                    if result is not None:
                        # Если нашли в дочерних элементах, то вернуть результат
                        return result

            # Ну если и в дочерних узлах не нашли,
            # то вызвать поиск для следующего элемента
            next = self.GetNextSibling(item)
            if next and next.IsOk():
                result = self.findItemString(string, next, bILike)
                if result is not None:
                    return result
            
            # Если не нашли в следующих элементах,
            # тогда поискать в следующем элементе родительского элемента
            parent_item = item.GetParent()
            if parent_item and parent_item.IsOk():
                parent_next = self.GetNextSibling(parent_item)
                if parent_next and parent_next.IsOk():
                    result = self.findItemString(string, parent_next, bILike)
                    if result is not None:
                        return result
            
            # Все равно не нашли
        except:
            log.fatal(u'ОШИБКА компонента %s метода поиска узла по строке' % self.name)
        return None

    def _getNextItem4Find(self, item):
        """
        Получить следующий элемент для поиска.
        """
        if item.HasChildren():
            return item.GetChildren()[0]
        next_item = self.GetNextSibling(item)
        if next_item and next_item.IsOk():
            return next_item
        parent_item = item.GetParent()
        if parent_item:
            parent_next = self.GetNextSibling(parent_item)
            if parent_next and parent_next.IsOk():
                return parent_next
        return None
        
    def selectFindItem(self, string, bILike=True):
        """
        Поиск и выделение пункта по строке. Поиск производится по
        надписям элементов.
        :type string: C{string}
        :param string: Строка поиска
        :type bILike: C{bool}
        :param bILike: Признак поиска без учета регистра. Если False - то поиск ведется
            на точное соответствие.
        :return: Возвращает номер элемента дерева, где найдена искомая строка.
        """
        cur_item = self.GetSelection()

        if not cur_item.IsOk():
            cur_item = None
        else:
            # Начинать поиск со следующего элемента
            cur_item = self._getNextItem4Find(cur_item)
        find_item = self.findItemString(string, item=cur_item, bILike=bILike)

        if find_item is not None:
            self.SelectItem(find_item)
        else:
            if dlgfunc.getAskDlg(u'ПОИСК', u'Строка <%s> не найдена. Начать поиск сначала?' % string) == wx.YES:
                # Начать поиск сначала
                find_item = self.findItemString(string, None, bILike)
                if find_item is not None:
                    self.SelectItem(find_item)
        return None
        
    def isRootSelected(self):
        """
        Определить является ли корень выделенным.
        """
        return self.IsSelected(self.GetRootItem())
        
    # --- Обработчики событий ---
    def onItemExpanded(self, event):
        """
        Разворачивание узла.
        """
        pass
    
    def onItemCollapsed(self, event):
        """
        Сворачивание узла.
        """
        pass
        
    def onSelectChanged(self, event):
        """
        Изменение выделенного узла.
        """
        select_item = event.GetItem()
        self._last_selection = None
        if select_item:
            self._last_selection = self.getItemPath(select_item)
            
        # --- НАЧАЛО: БЛОК ИСПРАВЛЕНИЯ БАГИ ПОЯВЛЕНИЯ ВТОРОГО КУРСОРА В ДЕРЕВЕ ---
        if not self.HasFlag(wx.TR_MULTIPLE):
            selections = self.GetSelections()
            if len(selections) > 1:
                for selection in selections:
                    if selection != select_item:
                        selection.SetHilight(0)
                        self._main_win.RefreshLine(selection)
        # --- КОНЕЦ: БЛОК ИСПРАВЛЕНИЯ БАГИ ПОЯВЛЕНИЯ ВТОРОГО КУРСОРА В ДЕРЕВЕ ---
        
    def onItemActivated(self, event):
        """
        Активизация узла.
        """
        pass
        
    def onItemChecked(self, event):
        """
        Выбор узла.
        """
        item = event.GetItem()
        self.checkItemChildren(item, self.IsItemChecked(item))
        event.Skip()
        
    def OnTreeListKeyDown(self,event):
        """
        Нажатие клавиши на дереве.
        ВНИМАНИЕ!!!
        Обработчик нажатия клавиши на дереве цепляется через
        wx.EVT_TREE_KEY_DOWN, а не wx.EVT_KEY_DOWN, как у других компонентов.
        """
        pass
        
    def hideHeader(self):
        self._headerHeight = 0
        self.DoHeaderLayout()
    
    def setCheckRadio(self, selection=0):
        """
        Устанавливаем тип checkbox/radiobox картинок.
        """
        if selection == 0:
            self.SetImageListCheck(13, 13)
        else:
            il = wx.ImageList(16, 16)
            il.Add(bmpfunc.createLibraryBitmap('ui-check-box.png'))
            il.Add(bmpfunc.createLibraryBitmap('ui-check-box-uncheck.png'))
            il.Add(bmpfunc.createLibraryBitmap('ui-radio-button.png'))
            il.Add(bmpfunc.createLibraryBitmap('ui-radio-button-uncheck.png'))
            self.SetImageListCheck(16, 16, il)        
        
    def _testTree(self):
        """
        """
        print('TEST SIMPLE TREE LIST CTRL')
        for x in range(5):
            txt = 'Item %d' % x
            child = self.AppendItem(self.root, txt)
            self.SetItemText(child, txt + '(c1)')
            self.SetItemImage(child, self.fldridx, which=wx.TreeItemIcon_Normal)
            self.SetItemImage(child, self.fldropenidx, which=wx.TreeItemIcon_Expanded)
    
    def load_data(self, func, *arg, **kwarg):
        self.begin_load()
        self.tree = func(*arg, **kwarg)
    
    def view_data(self, *arg, **kwarg):
        self.loadTree(self.tree)

    def getItemCheckList(self, item=None):
        """
        Получить список выбранных элементов дерева.
        """
        if item is None:
            item = self.GetRootItem()

        check_list = []
        
        if item.HasChildren():
            for child in item.GetChildren():
                check_data = {'name': self.GetItemText(child),
                              '__record__': self.getItemRecord(child),
                              'check': self.IsItemChecked(child),
                              }
                if child.HasChildren():
                    check_data['children'] = self.getItemCheckList(child)
                check_list.append(check_data)                
        else:
            check_data = {'name': self.GetItemText(item),
                          '__record__': self.getItemRecord(child),
                          'check': self.IsItemChecked(item),
                          }
            return check_data
        
        return check_list        
    
    def checkItemChildren(self, item=None, bCheck=True):
        """
        Отметить все дочерние элементы.
        :param item: Указанный элемент дерева.
        :param bCheck: True - установить отметку, False - убрать отметку.
        """
        if item is None:
            item = self.GetRootItem()
            
        if item.HasChildren():
            for child in item.GetChildren():
                self.CheckItem(child, bCheck)
                self.checkItemChildren(child, bCheck)
        
    def loadData(self, function=None, *arg, **kwarg):
        """
        Функция загрузки данных.
        :param function: Функция загрузки данных, которая должна вернуть словарно-
            списковую структуру, описывающую дерево. 
        """
        from . import delayedres
        pr = delayedres.DelayedFunction(self.load_data, self.view_data, function, *arg, **kwarg)
        pr.start()
    
    def loadData2(self, function=None, view_func=None, *arg, **kwarg):
        """
        Функция загрузки данных.
        :param function: Функция загрузки данных, которая должна вернуть словарно-
            списковую структуру, описывающую дерево. 
        """
        from . import delayedres
        pr = delayedres.DelayedFunction(self.load_data, view_func or self.view_data, function, *arg, **kwarg)
        pr.start()
    
    #   Обработчики событий


def __load_data(tree=None):
    res0 = {'d1': {'__record__': [1, 2, 3, 4]},
            'd2': {'cc1': 'a1', 'cc2': 'a2', '__record__': [1, 2, 3, 4]},
            'd3': {'ee1': 'a1', 'ee2': 'a2', '__record__': [1, 2, 3, 4]},
            '__record__': [1, 2, 3, 4],
            }
     
    res1 = {'name': 'A2',
            'children': [],
            '__record__': ['1', 2, 3, 4],
            }

    res2 = {'name': 'A3',
            'children': [],
            '__record__': ['1', 2, 3, 4],
            }
    res3 = {'name': 'A4',
            'children': [res1, res2],
            '__type__': 1,
            '__record__': [u'Дополнительный код', 2, 3, 4],
            }
     
    res = [{'name': 'A1',
            'children': [res1, res2, res3],
            '__record__': [1, 2, 3, 4],
            }]

    return res


def __view_data(obj):
    obj.loadTree(obj.tree)
    

def test(par=0):
    """
    Тестируем пользовательский класс.
    :type par: C{int}
    :param par: Тип консоли.
    """
    app = wx.PySimpleApp()
    
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)
    tree = icSmartTreeListCtrl(win, -1, position=(10, 10), size=(200, 300),
                               style=wx.TR_DEFAULT_STYLE | wx.TR_HAS_BUTTONS,
                               labels=[u'col1', 'col2', u'Колонка 3'])
    tree.loadData(__load_data)

    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    """
    Тестируем пользовательский класс.
    """
    test()
