#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Контрол выбора элемента справочника в виде выпадающего дерева справочника.
"""

# --- Imports ---
import wx
import wx.combo

from . import icspravtreedatasource
import wx.lib.agw.customtreectrl as CT
from ic.components import icwidget
import wx.lib.platebtn as platebtn

from ic.utils import ic_util
from ic.kernel import io_prnt

# Version
__version__ = (0, 0, 0, 5)

DEFAULT_ENCODE = 'utf-8'


class BoxTree(CT.CustomTreeCtrl):

    def OnPaint(self, event):
        """
        Handles the wx.EVT_PAINT event.
        """

        dc = wx.PaintDC(self)
        self.PrepareDC(dc)

        if not self._anchor:
            return

        dc.SetFont(self._normalFont)
        dc.SetPen(self._dottedPen)

        align = self.HasFlag(CT.TR_ALIGN_WINDOWS)
        y = 20
        self.PaintLevel(self._anchor, dc, 0, y, align)


# Constants
SPC_IC_SPRAVTREECOMBOCTRL = {'sprav': None,      # Паспорт справочника-источника данных
                             'root_code': None,  # Код корневого элемента ветки справочника
                             'view_all': False,  # Показывать все элементы справочника
                             'level_enable': -1,  # Номер уровня с которого включаются элементы для выбора
                             'expand': True,      # Распахнуть

                             'get_label': None,  # Функция определения надписи элемента дерева
                             'find_item': None,  # Функция поиска элемента дерева
                             'is_choice_list': False,
                             'get_selected_code': None,  # Функция получения выбранного кода
                             'set_selected_code': None,  # Функция установки выбранного кода

                             '__parent__': icwidget.SPC_IC_WIDGET,
                             }


TREE_HIDDEN_ROOT_LABEL = '<hidden root>'
TREE_HIDDEN_ITEM_LABEL = '<hidden item>'

DEFAULT_ENABLE_ITEM_COLOUR = wx.BLACK
DEFAULT_DISABLE_ITEM_COLOUR = wx.Colour(128, 128, 128)


class icSpravTreeComboPopup(wx.combo.ComboPopup):
    """
    Выпадающее дерево справочника.
    """

    def Init(self):
        self.root_name = None
        self.value = None
        self.curitem = None

    def clear(self):
        pass
    
    def Create(self, parent):
        self.tree = CT.CustomTreeCtrl(parent, style=wx.TR_HIDE_ROOT
                                      | wx.TR_HAS_BUTTONS
                                      | wx.TR_SINGLE
                                      | wx.TR_LINES_AT_ROOT
                                      | wx.SIMPLE_BORDER)
        self.tree.Bind(wx.EVT_MOTION, self.OnMotion)
        self.tree.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)

    def GetControl(self):
        return self.tree

    def GetStringValue(self):
        if self.value:
            return self.tree.GetItemText(self.value)
        return ''

    def OnPopup(self):
        if self.value:
            self.tree.EnsureVisible(self.value)
            self.tree.SelectItem(self.value)

    def SetStringValue(self, value):
        # this assumes that item strings are unique...
        root = self.tree.GetRootItem()
        if not root:
            return
        found = self.FindItem(root, value)
        if found:
            self.value = found
            self.tree.SelectItem(found)

    def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        return wx.Size(minWidth, min(200, maxHeight))

    def FindItem(self, parentItem, text):
        """
        Найти дочерний элемент по лейблу.
        """
        item, cookie = self.tree.GetFirstChild(parentItem)
        while item:
            if self.tree.GetItemText(item) == text:
                return item
            if self.tree.ItemHasChildren(item):
                item = self.FindItem(item, text)
            item, cookie = self.tree.GetNextChild(parentItem, cookie)
        return wx.TreeItemId()

    def _get_root_label(self):
        """
        Имя корневого элемента.
        """
        if self.root_name:
            return self.root_name
        return TREE_HIDDEN_ROOT_LABEL

    def AddItem(self, value, parent=None, data=None):
        """
        Добавить элемент в дерево.
        """
        if not parent:
            root = self.tree.GetRootItem()
            if not root:
                root = self.tree.AddRoot(self._get_root_label())
            parent = root

        item = self.tree.AppendItem(parent, value)
        if data is not None:
            self.tree.SetPyData(item, data)
        return item

    def hasHiddenItem(self, parentItem):
        """
        Есть ли у элемента скрытые дочерние элементы?
        @return: True/False.
        """
        return self.FindItem(parentItem, TREE_HIDDEN_ITEM_LABEL).IsOk()

    def OnMotion(self, evt):
        """
        have the selection follow the mouse, like in a real combobox
        """
        item, flags = self.tree.HitTest(evt.GetPosition())
        if item and flags & wx.TREE_HITTEST_ONITEMLABEL:
            self.tree.SelectItem(item)
            self.curitem = item
        evt.Skip()

    def _isEnableItem(self, Item_):
        """
        Проверка на то что элемент дерева включен для выбора.
        """
        colour = self.tree.GetItemTextColour(Item_)
        # Если текст черный тогда его можно выбирать
        return colour == DEFAULT_ENABLE_ITEM_COLOUR

    def OnLeftDown(self, evt):
        """
        Обработчик выбора элемента дерева.
        """
        # do the combobox selection
        self.curitem = None
        item, flags = self.tree.HitTest(evt.GetPosition())
        if item and self._isEnableItem(item) and flags & wx.TREE_HITTEST_ONITEMLABEL:
            self.curitem = item
            self.value = item
            self.Dismiss()
        evt.Skip()

    def get_selected_sprav_code(self, AltCodeField_=None):
        """
        Получить выбранный код справочника.
        @param AltCodeField_: Поле хранения альтернативного кода.
        """
        item = self.curitem
        if item:
            data_item = self.tree.GetPyData(item)
            # ВНИМАНИЕ! Здесь необходимо проверять
            # есть ли прикрепленные к узлу данные
            # Проверка должна производиться только на None
            # иначе бывает глючит
            if data_item is not None:
                code = data_item.getCode()
                return code
            else:
                io_prnt.outWarning(u'Нет данных элемента дерева <%s>' % item)
        return None

    def set_selected_sprav_code(self, src, Code_, AltCodeField_=None):
        """
        Установить выбранный код справочника.
        @param Code_: Код справочника.
        @param AltCodeField_: Поле хранения альтернативного кода.
        """
        pref = Code_
        value = None
        if src:
            record = src.find_record(Code_)
            if record:
                value = record['name']
                self.curitem = self.find_tree_item(Code_)
                if self.curitem is None:
                    io_prnt.outWarning(u'Не найден элемент дерева справочника <%s> с кодом <%s>' % (self._get_root_label(),
                                                                                                    Code_))
                if AltCodeField_ is not None:
                    pref = record[AltCodeField_].strip() or pref
        return value, pref

    def find_tree_item(self, code, item=None):
        """
        Найти элемент дерева по коду справочника.
        @param code: Код справочника.
        @param item: Начальный элемент дерева,
            если None, то начинается поиск с корневого элемента.
        @return: Идентификатор элемента дерева,
            или None если не найдено.
        """
        if item is None:
            item = self.tree.GetRootItem()
        data = self.tree.GetPyData(item)
        # print item, data, data.getCode() if data is not None else ''
        if data is not None and data.getCode() == code:
            return item
        else:
            if self.tree.HasChildren(item):
                child, cookie = self.tree.GetFirstChild(item)

                while child and child.IsOk():
                    find_item = self.find_tree_item(code, child)
                    if find_item:
                        return find_item
                    child, cookie = self.tree.GetNextChild(item, cookie)
        return None


class icSpravTreeChoiceListComboPopup(icSpravTreeComboPopup):
    """
    Выпадающее дерево справочника c возможностью выбора произвольного списка
    элементов.
    """

    def Create(self, parent):
        self.parent = parent
        self.tree = BoxTree(parent, style=wx.TR_HIDE_ROOT
                            | wx.TR_HAS_BUTTONS
                            | wx.TR_SINGLE
                            | wx.TR_LINES_AT_ROOT
                            | wx.SIMPLE_BORDER)

        self.tree.Bind(wx.EVT_MOTION, self.OnMotion)
        self.tree.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.tree.Bind(CT.EVT_TREE_ITEM_CHECKED, self.OnChecked)
        self.tree.Bind(CT.EVT_TREE_ITEM_CHECKING, self.OnChecking)
        # Отобранные элементы
        self.check_items = []
        self.pref = u''
        self.tbtn = platebtn.PlateButton(self.tree, wx.ID_ANY, u'ок ', None, style=platebtn.PB_STYLE_SQUARE)
        self.tbtn.SetBackgroundColour(wx.LIGHT_GREY)
        self.tree.Bind(wx.EVT_BUTTON, self.OnOk)

    def OnOk(self, evt):
        cod = self._combo.get_selected_sprav_code('s1')
        self.Dismiss()

    def clear(self):
        self.pref = u''

    def AddItem(self, value, parent=None, data=None):
        """
        Добавить элемент в дерево.
        """
        if not parent:
            root = self.tree.GetRootItem()
            if not root:
                root = self.tree.AddRoot(self._get_root_label())
            parent = root

        item = self.tree.AppendItem(parent, value, ct_type=1)
        cod = value.split(u' ')[0]
        if cod and cod.strip() in self.pref.split(u','):
            self.check_items.append(item)
            item.Check(True)

        if data is not None:
            self.tree.SetPyData(item, data)
        return item

    def GetStringValue(self):
        txt = u','.join([self.tree.GetItemText(item).split(u' ')[0] for item in self.check_items])
        return txt

    def OnMotion(self, evt):
        self.tbtn.SetPosition((0, 0))
        evt.Skip()

    def OnChecking(self, evt):
        """
        Выбор элемента дерева.
        """
        item = evt.GetItem()
        if item and self._isEnableItem(item):
            evt.Skip()

    def OnChecked(self, evt):
        """
        Выбор элемента дерева.
        """
        item = evt.GetItem()
        if self.tree.IsItemChecked(item) and item not in self.check_items:
            self.check_items.append(item)
        elif item in self.check_items:
            self.check_items.remove(item)
            self.CheckChilds(item, False)

    def CheckChilds(self, item, checked):
        """
        Transverses the tree and checks/unchecks the items. Meaningful only for check items.
        """
        if not item:
            raise Exception("\nERROR: Invalid Tree Item. ")

        (child, cookie) = self.tree.GetFirstChild(item)

        if child in self.check_items:
            self.check_items.remove(child)

        torefresh = False
        if item.IsExpanded():
            torefresh = True

        while child:
            if child.GetType() == 1 and child.IsEnabled():
                self.tree.CheckItem2(child, checked, torefresh=torefresh)
            self.CheckChilds(child, checked)
            (child, cookie) = self.tree.GetNextChild(item, cookie)
            if child in self.check_items:
                self.check_items.remove(child)

    def OnLeftDown(self, evt):
        """
        Обработчик выбора элемента дерева.
        """
        self.tbtn.SetPosition((0, 0))
        evt.Skip()

    def get_selected_sprav_code(self, *arg, **kwarg):
        """
        Получить выбранный код справочника.
        @param AltCodeField_: Поле хранения альтернативного кода.
        """
        lst = [self.tree.GetPyData(item).getCode() for item in self.check_items]
        return u','.join(lst)

    def set_selected_sprav_code(self, src, Code_, AltCodeField_=None):
        """
        Установить выбранный код справочника.
        @param Code_: Код справочника.
        @param AltCodeField_: Поле хранения альтернативного кода.
        """
        self.check_items = []
        value = u''
        lst = []
        if src:
            for cod in Code_.split(','):
                cod = cod.strip()
                # self.curitem = self.find_tree_item(cod)
                record = src.find_record(cod)
                if record:
                    if AltCodeField_ is not None:
                        lst.append(record[AltCodeField_].strip() or cod)

        self.pref = u','.join(lst)
        return value, self.pref


TREE_CHOICE_LIST_POPUP = 1


class icSpravTreeComboCtrlPrototype(wx.combo.ComboCtrl):
    """
    Контрол выбора элемента справочника в виде выпадающего дерева справочника.

    ВНИМАНИЕ! Кеширование всех элементов справочника не происходит!!!
    Элементы справочника подгружаются по веткам.
    Поэтому этот контрол можно использовать для справочников с одним уровнем.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        self._level_enable = kwargs.pop('level_enable', -1)
        self._popup_type = kwargs.pop('popup_type', 0)
        self._complex_load = kwargs.pop('complex_load', -1)

        wx.combo.ComboCtrl.__init__(self, *args, **kwargs)
        # Ввод текста итерпретируется как задание строки поиска
        self.Bind(wx.EVT_TEXT_ENTER, self.onTextEnter)

        if self._popup_type == TREE_CHOICE_LIST_POPUP:
            self._combo_popup = icSpravTreeChoiceListComboPopup()
            self._combo_popup._combo = self
        else:
            self._combo_popup = icSpravTreeComboPopup()

        self.SetPopupControl(self._combo_popup)
        # При раскрывании элемента надо достраивать ветку дерева
        self._combo_popup.tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.onItemExpanded)

        # Текущий обрабатываемый элемент дерева данных
        self._cur_data_item = None

        self._oldCode = None
        self.view_code = None
        self.view_all = False
        self.root_code = None

        self._data_source = None
        self._label_func = None

        # Распахнуть дерево?
        self._expand = kwargs.pop('expand', True)

    def setSpravByPsp(self, sprav_psp):
        """
        Установить дерево справочника по его паспорту.
        @param sprav_psp: Паспорт справочника.
        """
        if not ic_util.is_pasport(sprav_psp):
            io_prnt.outWarning(u'Не корректное значение паспорта <%s>' % sprav_psp)
            return

        self.Clear()
        self.init(sprav_psp, self.view_code, self.view_all)

    def getSpravPsp(self):
        """
        Паспорт справочника-источника данных.
        """
        return None

    def setViewAll(self, view_all=True):
        """
        Установить просмотр всех элементов справочника.
        """
        self.view_all = view_all
        if self.view_all:
            sprav_psp = self.getSpravPsp()
            if sprav_psp:
                self.Clear()
                self.init(sprav_psp, self.view_code, self.view_all)
            else:
                io_prnt.outWarning(u'Не определен паспорт справочника контрола выбора')

    def viewAll(self):
        """
        Установить просмотр всех элементов справочника.
        """
        return self.setViewAll(view_all=True)

    setNSIPsp = setSpravByPsp

    def init(self, SpravPsp_=None, RootCode_=None, ViewAll_=False,
             complex_load=True):
        """
        Инициализация выпадающего дерева справочника.
        ВНИМАНИЕ! После создания объекта надо обязательно вызвать
        init метод для построения дерева справочника.
        @param SpravPsp_: Паспорт справочника-источника данных.
        @param RootCode_: Корневой элемент разрешенной ветки выбора.
        @param ViewAll_: Показывать все элементы справочника?
        @param complex_load: Комплесная загрузка всех данных справочника.
        """
        self.view_code = RootCode_
        self.view_all = ViewAll_
        self.root_code = None if self.view_all else self.view_code

        if SpravPsp_:
            self._data_source = icspravtreedatasource.icSpravTreeDataSource(SpravPsp_, self.root_code)
            self._combo_popup.root_name = self._data_source.getSpravDescription()

        if self._data_source:
            self._combo_popup.tree.DeleteAllItems()
            # Т.к. корневой элемент скрыт, то родитель у всех объектов
            # выставляется None
            if complex_load:
                self._addTree(self._data_source, None)
            else:
                self._addBranch(self._data_source, None)

            # Если определено распахивание, то рутовый уровень распахнуть
            if self._expand:
                self._combo_popup.tree.Expand(self._combo_popup.tree.GetRootItem())

    def clear(self):
        """
        Очистка внутренних переменных.
        """
        self._combo_popup.clear()

    # Очистка выбора
    clearSelect = wx.combo.ComboCtrl.Clear

    def getCurDataItem(self):
        """
        Текущий обрабатываемый элемент дерева данных
        """
        return self._cur_data_item

    def getDataSource(self):
        """
        Источник данных для контрола.
        """
        return self._data_source

    def getSprav(self):
        """
        Объект справочника.
        """
        if self._data_source:
            return self._data_source.getSprav()
        return None

    def getLevelEnable(self):
        """
        Уровень, с которого можно выбирать элементы.
        """
        return self._level_enable

    def set_label_func(self, func):
        """
        Устанавливает функцию вычисления текста элемента.
        """
        self._label_func = func

    def getLabelFunc(self, item_data=None):
        """
        Вычисление надписи элемента дерева.
        """
        if self._label_func:
            return self._label_func(item_data)

    def getLabel_s1(self, item_data):
        """
        Надпись в контроле, соответствующая данному элементу.
        """
        # По умолчанию надпис: Код+Наименование
        # if item_data._data[2]:
        #     cod = u'%s (%s)' % (item_data._data[2], item_data._data[0])
        # else:
        #     cod = item_data._data[0]
        # return u'%s %s' % (cod, item_data.getDescription())

        # Изменено для тупых пользователей: Наименование
        return item_data.getDescription()

    def getFindItemFunc(self, *args, **kwargs):
        """
        Получить функцию альтернативного поиска.
        """
        return None

    def getSelectedCodeFunc(self):
        """
        Получить функцию определения выбранного кода.
        """
        return None

    def setSelectedCodeFunc(self, *args, **kwargs):
        """
        Функция установки выбранного кода.
        """
        return None

    def _isNotSelectable(self, ViewCode_, CurCode_):
        """
        Проверка на элемент, который можно выбрать.
        """
        if ViewCode_:
            # Элементы проверяются только если
            # есть ограничение на выбор
            return self.view_all and ((CurCode_ == ViewCode_) or (ViewCode_ not in CurCode_))
        return False

    def _isDisabledItem(self, ViewCode_, LevelEnable_, DataSrcItem_):
        """
        Проверка элемента выключен он или нет.
        """
        if DataSrcItem_ is None:
            return True

        if ViewCode_:
            # Элементы проверяются только если
            # есть ограничение на выбор
            cur_code = DataSrcItem_.getCode()
            return self.view_all and ((cur_code == ViewCode_) or (ViewCode_ not in cur_code))
        elif LevelEnable_ > 0:
            level_idx = DataSrcItem_.getLevelIdx()
            return LevelEnable_ > level_idx
        return False

    def _addBranch(self, DataItem_, ParentItem_=None):
        """
        Добавить ветку дерева элементов.
        """
        children = DataItem_.getChildren()

        for child in children:
            # Установить текущий обрабатываемый элемент данных
            self._cur_data_item = child

            get_label_func = self.getLabelFunc(child)
            label = child.getLabel(get_label_func)
            code = child.getCode()

            # Т.к. корневой элемент скрыт, то родитель у всех объектов
            # выставляется None
            item = self._combo_popup.AddItem(label, parent=ParentItem_, data=child)
            if self._isDisabledItem(self.view_code, self.getLevelEnable(), child):
                self._combo_popup.tree.SetItemTextColour(item, DEFAULT_DISABLE_ITEM_COLOUR)
            else:
                self._combo_popup.tree.SetItemTextColour(item, DEFAULT_ENABLE_ITEM_COLOUR)

            if child.hasChildren():
                # Если есть дочерние элементы у текущего элемента,
                # то сделать фиктивный элемент.
                self._combo_popup.AddItem(TREE_HIDDEN_ITEM_LABEL, parent=item)

        self._cur_data_item = None

    def _addTree(self, DataItem_, ParentItem_=None):
        """
        Добавить все дерево элементов.
        """
        children = DataItem_.getChildren()

        for child in children:
            # Установить текущий обрабатываемый элемент данных
            self._cur_data_item = child

            get_label_func = self.getLabelFunc(child)
            label = child.getLabel(get_label_func)
            code = child.getCode()

            # Т.к. корневой элемент скрыт, то родитель у всех объектов
            # выставляется None
            item = self._combo_popup.AddItem(label, parent=ParentItem_, data=child)
            if self._isDisabledItem(self.view_code, self.getLevelEnable(), child):
                self._combo_popup.tree.SetItemTextColour(item, DEFAULT_DISABLE_ITEM_COLOUR)
            else:
                self._combo_popup.tree.SetItemTextColour(item, DEFAULT_ENABLE_ITEM_COLOUR)

            if child.hasChildren():
                # Если есть дочерние элементы у текущего элемента,
                # то сделать фиктивный элемент.
                # self._combo_popup.AddItem(TREE_HIDDEN_ITEM_LABEL, parent=item)
                self._addTree(child, ParentItem_=item)

        self._cur_data_item = None

    def onItemExpanded(self, event):
        """
        Обработчик раскрывания элементов дерева.
        """
        item = event.GetItem()

        # Если в дочерних элементах есть скрытые элементы, то
        # удалить скрытый элемент и достроить ветку дерева элементов
        if self._combo_popup.hasHiddenItem(item):
            # Удалить скрытый элемент
            self._combo_popup.tree.DeleteChildren(item)
            # Добавить ветку дерева
            data_item = self._combo_popup.tree.GetPyData(item)
            if data_item:
                self._addBranch(data_item, item)

        event.Skip()

    def findItem(self, FindStr_, RunFindItemFunc_=True, *args, **kwargs):
        """
        Найти элемент по строке поиска.
        @param FindStr_: Строка поиска.
        @param RunFindItemFunc_: Запустить альтернативную функцию поиска?
        @return: Возвращает элемент дерева источника данных.
        """
        if RunFindItemFunc_:
            kwargs['FindStr_'] = FindStr_
            result = self.getFindItemFunc(*args, **kwargs)
            if result:
                return result

        if self._data_source:
            return self._data_source.find(FindStr_)
        return None

    def onTextEnter(self, event):
        """
        Обработчик ввода текста в комбобоксе
        Ввод текста итерпретируется как задание строки поиска.
        """
        find_str = event.GetString()

        find_item_func = self.getFindItemFunc()
        if find_item_func:
            # Функция альтернативного поиска
            label = find_item_func
        else:
            # Произвести поиск
            label = self.findItem(find_str)

        code = self.getSelectedCode(Value_=label)
        data_item = self._data_source.findItemByCode(code)

        if label and not self._isDisabledItem(self.view_code, self.getLevelEnable(), data_item):
            self.SetValue(label)
        else:
            self.SetValue(u'')

        event.Skip()

    def getSelectedCode(self, SelectedCodeFunc_=None, Value_=None):
        """
        Получить выбранный код.
        @param SelectedCodeFunc_: Альтернативная функция полчения кода.
        @return: Возвращает выбранный код в виде строки или None,
            если код не выбран.
        """
        if SelectedCodeFunc_:
            return SelectedCodeFunc_

        return self.get_selected_sprav_code()

    def get_selected_sprav_code(self, AltCodeField_=None):
        """
        Получить выбранный код справочника.
        @param AltCodeField_: Поле хранения альтернативного кода.
        """
        return self._combo_popup.get_selected_sprav_code(AltCodeField_)

    def set_selected_sprav_code(self, Code_, AltCodeField_=None):
        """
        Установить выбранный код справочника.
        @param Code_: Код справочника.
        @param AltCodeField_: Поле хранения альтернативного кода.
        """
        self._oldCode = Code_
        value, pref = self._combo_popup.set_selected_sprav_code(self._data_source, Code_, AltCodeField_)
        if value or pref:
            str_value = ic_util.toUnicode(value, DEFAULT_ENCODE) if type(value) in (str, unicode) else u''
            return self.SetValue(str_value)
        else:
            return self.SetValue(u'')

    def setSelectedCode(self, Value_=None, RunSelectedCodeFunc_=True, *args, **kwargs):
        """
        Установить выбранный код.
        @param Value_: Значение установливаемого кода.
        @param RunSelectedCodeFunc_: Запустить альтернативную функцию установки кода.
        @return: Возвращает выбранный код в виде строки или None,
            если код не выбран.
        """
        if RunSelectedCodeFunc_:
            kwargs['Value_'] = Value_
            result = self.setSelectedCodeFunc(*args, **kwargs)
            if result:
                return result

        code = Value_
        self.set_selected_sprav_code(code)
        # label = self.findItem(code, True)
        #
        # if label:
        #     self.SetValue(label)
        # else:
        #     self.SetValue(u'')
        return True

    def getValue(self):
        """
        Значение контрола.
        """
        return self.getSelectedCode()
    
    def setValue(self, Value_):
        """
        Установка значения контрола.
        ВНИМАНИЕ! Значение может задаваться в виде строки,
        а может в виде словаря-записи справочника.
        """
        code = None
        if isinstance(Value_, str):
            code = Value_
        elif isinstance(Value_, unicode):
            code = Value_.encode(DEFAULT_ENCODE)
        elif isinstance(Value_, dict):
            code = Value_.get('cod', None)
        elif Value_ is None:
            code = None
            self._combo_popup.curitem = None
        else:
            io_prnt.outWarning(u'Не корректный тип <%s> значения контрола %s' % (type(Value_), self.__class__.__name__))
        return self.setSelectedCode(code)
    
    def getSelectedRecord(self):
        """
        Получить запись справочника в виде словаря, соответствующую
        выбранному элементу.
        """
        rec_dict = None
        code = self.getSelectedCode(self.getSelectedCodeFunc())
        if code:
            if self._data_source is not None:
                data_item = self._data_source.findItemByCode(code)
                if data_item is not None:
                    rec_dict = data_item.getRecDict()

        return rec_dict


def test_ctrl():
    """
    Тестовая функция.
    """
    app = wx.PySimpleApp()
    frame = wx.Frame(None)
    sprav_psp = (('Sprav', 'Regions', None, 'nsi_sprav.mtd', 'NSI'),)
    tree_combo_ctrl = icSpravTreeComboCtrlPrototype(sprav_psp, None, parent=frame, size=wx.Size(200, -1))
    button = wx.Button(frame, pos=wx.Point(10, 100))
    frame.Show()
    app.MainLoop()


def test():
    """
    Тестовая функция.
    """
    import ic
    ok_login = ic.Login('test', '', 'c:/defis/Registr/Registr', True)
    print('START SpravTreeComboCtrl TEST ... Login:', ok_login)
    if ok_login:
        sprav_psp = (('Sprav', 'StdCls', None, 'registr_nsi.mtd', 'Registr'),)

        frame = wx.Frame(None)

        tree_combo_ctrl = icSpravTreeComboCtrlPrototype(sprav_psp, None, True,
                                                        parent=frame, size=wx.Size(200, -1),
                                                        level_enable=1, popup_type=1)
        tree_combo_ctrl.set_label_func(tree_combo_ctrl.getLabel_s1)
        tree_combo_ctrl.set_selected_sprav_code(u'PA110020010,PA110020020,PA110020030', 's1')
        button = wx.Button(frame, pos=wx.Point(10, 100))
        frame.Show()
        ic.getKernel().MainLoop()
        ic.Logout()
        print('STOP SpravTreeComboCtrl TEST ... OK')


def over_test():
    """ Тестовая функция граничных значений."""
    import ic
    ok_login = ic.Login('test_user', '', 'c:/defis/NSI/NSI', True)
    print('START SpravTreeComboCtrl TEST ... Login:', ok_login)
    if ok_login:
        sprav_psp = (('Sprav', 'OrganPrinyat', None, 'nsi_sprav.mtd', 'NSI'),)
        frame = wx.Frame(None)

        tree_combo_ctrl = icSpravTreeComboCtrlPrototype(sprav_psp, None, True,
                                                        parent=frame, size=wx.Size(200, -1))
        button = wx.Button(frame, pos=wx.Point(10, 100))
        print('SELECTED CODE:', tree_combo_ctrl.getSelectedCode())

        frame.Show()
        ic.getKernel().MainLoop()
        ic.Logout()
        print('STOP SpravTreeComboCtrl TEST ... OK')


if __name__ == '__main__':
    test()
