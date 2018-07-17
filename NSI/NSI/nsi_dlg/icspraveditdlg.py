#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Диалог редактирования справочника.
"""

import sys
import wx
import wx.propgrid
import ic
from ic import log
from ic.dlg import ic_dlg
from ic.utils import ic_time
from ic import ic_bmp
from ic.utils import ic_str
from ic.utils import coderror
from ic.db import icsqlalchemy
from . import nsi_dialogs_proto
from . import iceditcodeproperty

# Для расширенного управления контролами формы
from ic.engine import form_manager

# Version
__version__ = (0, 0, 2, 3)

# Не редактируемые поля таблицы справочника
NOT_EDITABLE_FIELDS = ('type', 'count', 'access')

# Текст фиктивного элемента дерева
TREE_ITEM_LABEL = u'...'


class icSpravRecEditDlg(nsi_dialogs_proto.icSpravRecEditDlgProto):
    """
    Диалоговое окно редактирования записи справочника.
    """
    
    def __init__(self, nsi_sprav=None, record=None, *args, **kwargs):
        """
        Конструктор.
        @param nsi_sprav: Объект справочника, запись которого редактируется.
        @param record: Словарь редактируемой записи.
        """
        nsi_dialogs_proto.icSpravRecEditDlgProto.__init__(self, *args, **kwargs)
        # ВНИМАНИЕ! В wxFormBuilder глюк/баг. Поэтому необходимо здесь указывать
        # поэтому надо здесь указывать привязку к обработчику события
        self.record_propertyGrid.Bind(wx.propgrid.EVT_PG_CHANGED, self.onRecordPropertyGridChanged)

        self.sprav = nsi_sprav
        # Первоначальная запись
        self.record = record
        # Отредактированная запись
        self.edit_record = record
        if self.edit_record is None:
            self.edit_record = dict()

        self.init()
        
    def getSprav(self):
        """
        Объект справочника, запись которого редактируется.
        """
        return self.sprav
    
    def getRecord(self):
        """
        Словарь редактируемой записи.
        """
        if self.record is None:
            self.record = dict()
        return self.record

    def _createProperty(self, **field):
        """
        Создать объект свойства по описанию поля.
        @param field:
        @return: Объект свойства.
        """
        label = field['label'] if field['label'] else (field['description'] if field['description'] else field['name'])
        default_value = field['default']
        if field['name'] == 'cod':
            # Проверка на соответствие типа
            if not isinstance(default_value, str) and not isinstance(default_value, unicode):
                try:
                    default_value = str(default_value)
                except:
                    default_value = u''
            property = iceditcodeproperty.icEditCodeProperty(label=label, name=field['name'], value=default_value)
            property.setSprav(self.sprav)            
            property.setPropertyGrid(self.record_propertyGrid)
        elif field['type_val'] == icsqlalchemy.TEXT_FIELD_TYPE:
            # Проверка на соответствие типа
            if not isinstance(default_value, str) and not isinstance(default_value, unicode):
                try:
                    default_value = str(default_value)
                except:
                    default_value = u''
            # Просто текстовое поле
            property = wx.propgrid.StringProperty(label=label, name=field['name'], value=default_value)
        elif field['type_val'] == icsqlalchemy.FLOAT_FIELD_TYPE:
            # Проверка на соответствие типа
            if not isinstance(default_value, float):
                try:
                    default_value = float(default_value)
                except:
                    default_value = 0.0
            property = wx.propgrid.FloatProperty(label=label, name=field['name'], value=default_value)
        elif field['type_val'] == icsqlalchemy.INT_FIELD_TYPE:
            # Проверка на соответствие типа
            if not isinstance(default_value, int):
                try:
                    default_value = int(default_value)
                except:
                    default_value = 0
            property = wx.propgrid.IntProperty(label=label, name=field['name'], value=default_value)
        elif field['type_val'] == icsqlalchemy.DATE_FIELD_TYPE:
            py_date = ic_time.strDateFmt2DateTime(default_value)
            wx_date = ic_time.pydate2wxdate(py_date)
            property = wx.propgrid.DateProperty(label=label, name=field['name'], value=wx_date)
        elif field['type_val'] == icsqlalchemy.DATETIME_FIELD_TYPE:
            wx_date = ic_time.pydate2wxdate(default_value)
            property = wx.propgrid.DateProperty(label=label, name=field['name'], value=wx_date)
        else:
            # Если тип не определен то просто посмотреть в текстовом виде
            # Проверка на соответствие типа
            if not isinstance(default_value, str) and not isinstance(default_value, unicode):
                try:
                    default_value = str(default_value)
                except:
                    default_value = u''
            property = wx.propgrid.StringProperty(label=label, name=field['name'], value=default_value)
            property.Enable(False)
            
        return property

    def getSpravTabResource(self):
        """
        Определить ресурс таблицы справочника.
        """
        sprav = self.getSprav()
        if sprav is None:
            log.warning(u'Не определен объект справочника для редактирования')
            return None
        storage = sprav.getStorage()
        sprav_tab = storage.getSpravTabClass()
        sprav_tab_res = sprav_tab.getResource()
        return sprav_tab_res
        
    def init(self):
        """
        Функция инициализации диалогового окна.
        """
        sprav_tab_res = self.getSpravTabResource()
        tab_fields = [field for field in sprav_tab_res['child'] if field['name'] not in NOT_EDITABLE_FIELDS]

        rec = self.getRecord()
        for field_spc in tab_fields:
            field_name = field_spc['name']
            if field_spc:
                property = self._createProperty(**field_spc)
                property.SetValue(rec[field_name])
            else:
                # Просто добавить как редактирование строки
                property = wx.propgrid.StringProperty(field_name, value=rec[field_name])
            self.record_propertyGrid.Append(property)

    def getEditRecord(self):
        """
        Получить отредактированную запись в виде словаря.
        """
        return self.edit_record

    def validate(self, name, value):
        """
        Контроль значений свойств.
        @type name: C{string}
        @param name: Имя атрибута.
        @type value: C{string}
        @param value: Проверяемое значение.
        @rtype: C{int}
        @return: Возвращает код проверки.
        """
        return coderror.IC_CTRL_OK

    def convertPropertyValue(self, name, str_value, property_type):
        """
        Преобразовать значение свойства к типу указанному в спецификации.
        @param name: Имя свойства/аттрибута.
        @param str_value: Значение в строковом представлении.
        @param property_type: Код типа значения. 
            Код типа значения поля таблицы справочника.
        """
        value = None

        if property_type == icsqlalchemy.TEXT_FIELD_TYPE:
            # Текстовое поле
            value = str_value
        elif property_type == icsqlalchemy.INT_FIELD_TYPE:
            # Целое
            if str_value.strip().isdigit():
                value = int(str_value.strip())
        elif property_type == icsqlalchemy.FLOAT_FIELD_TYPE:
            # Вещественное
            if str_value.strip().isdigit():
                value = float(str_value.strip())
        elif property_type == icsqlalchemy.DATE_FIELD_TYPE:
            # Тестовое представление даты
            value = str_value
        elif property_type == icsqlalchemy.DATETIME_FIELD_TYPE:
            # Дата/время
            value = ic_time.strDateTimeFmt2DateTime(str_value.strip())
        else:
            log.warning(u'Не обрабатываемый тип <%s> редактора поля' % property_type)
            value = str_value
        return value

    def findSpravTabFieldSpc(self, field_name):
        """
        Получить спецификацию поля таблицы справочника по имени.
        @param field_name: Имя поля.
        """
        sprav_tab_res = self.getSpravTabResource()
        for field_spc in sprav_tab_res['child']:
            if field_name == field_spc['name']:
                return field_spc
        return None
        
    def onRecordPropertyGridChanged(self, event):
        """
        Обработчик изменения значения поля редактируемой записи
        """
        property = event.GetProperty()
        if property:
            name = property.GetName()
            str_value = property.GetValueAsString()
            log.debug(u'Свойство [%s]. Новое значение <%s>' % (name, str_value))
            
            field_spc = self.findSpravTabFieldSpc(name)
            value = self.convertPropertyValue(name, str_value, field_spc['type_val'])
            if self.validate(name, value) == coderror.IC_CTRL_OK:
                self.edit_record[name] = value
            else:
                log.warning(u'Значение <%s> свойства [%s] не прошло валидацию' % (str_value, name))
        
        event.Skip()

    def onCancelButtonClick(self, event):
        """
        Обработчик кнопки <Отмена>.
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        Обработчик кнопки <OK>.
        """
        log.debug(u'Отредактированная запись <%s>' % self.getEditRecord())
        self.EndModal(wx.ID_OK)
        event.Skip()


class icSpravEditDlg(nsi_dialogs_proto.icSpravEditDlgProto,
                     form_manager.icFormManager):
    """
    Диалоговое окно редактирования справочника.
    """

    def __init__(self, nsi_sprav=None, *args, **kwargs):
        """
        Конструктор.
        @param nsi_sprav: Объект справочника, запись которого редактируется.
        """
        nsi_dialogs_proto.icSpravEditDlgProto.__init__(self, *args, **kwargs)

        self.sprav = nsi_sprav
        
        # Найденые коды, соответствующие строке поиска
        self.search_codes = list()
        # Текущий найденный код в списке найденных кодов
        self.search_code_idx = 0
        # Признак необходимости обновить список искомых кодов
        self.not_actual_search = False

        self.init()
        
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.onSpravTreeItemExpanded)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.onSpravTreeItemCollapsed)
        
    def init(self):
        """
        Функция инициализации диалогового окна.
        """
        # self.init_images()
        self.init_ctrl()
        self.set_sprav_tree()

    def init_images(self):
        """
        Инициализация образов контролов.
        """
        # <wx.Tool>
        bmp = ic_bmp.createLibraryBitmap('magnifier-left.png')
        tool_id = self.search_tool.GetId()
        # ВНИМАНИЕ! Для смены образа инструмента не надо использовать
        # метод инструмента <tool.SetNormalBitmap(bmp)> т.к. НЕ РАБОТАЕТ!
        # Для этого вызываем метод панели инструметнтов
        # <toolbar.SetToolNormalBitmap(tool_id, bmp)>
        self.search_toolBar.SetToolNormalBitmap(tool_id, bmp)
        # Внимание! После изменения образов инструментов
        # у панели инструментов надо вызвать <Realize>
        self.search_toolBar.Realize()        

        bmp = ic_bmp.createLibraryBitmap('plus.png')
        tool_id = self.add_tool.GetId()
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)

        bmp = ic_bmp.createLibraryBitmap('pencil.png')
        tool_id = self.edit_tool.GetId()
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)
        
        bmp = ic_bmp.createLibraryBitmap('minus.png')
        tool_id = self.del_tool.GetId()
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)

        # Внимание! После изменения образов инструментов
        # у панели инструментов надо вызвать <Realize>
        self.ctrl_toolBar.Realize()        

    def get_tab_editable_fields(self):
        """
        Список ресурсных описаний редактируемых полей таблицы справочника.
        """
        tab = self.sprav.getTable()
        fields = [field for field in tab.getResource()['child'] if field['name'] not in NOT_EDITABLE_FIELDS]
        return fields
    
    def init_ctrl(self):
        """
        Инициализация контролов.
        """
        # Добавление колонок
        self.recs_listCtrl.ClearAll()
        # Определить поля таблицы справочника
        fields = self.get_tab_editable_fields()
        
        for i, field in enumerate(fields):
            col_name = field['label'] if field['label'] else (field['description'] if field['description'] else field['name'])
            self.recs_listCtrl.InsertColumn(i, col_name, 
                                            width=wx.LIST_AUTOSIZE_USEHEADER)
           
    def set_sprav_tree_item(self, parent_item, record):
        """
        Установить элемент дерева справочника.
        @param parent_item: Родительский элемент дерева.
        @param record: Запись справочника, ассоциируемая с элементом.
        """
        # Запись в виде словаря
        rec_dict = self.sprav.getStorage()._getSpravFieldDict(record)
        name = ic_str.toUnicode(rec_dict['name'])
        # В случае многострочных наименования выделять только первую строку
        name = [line.strip() for line in name.split(u'\n')][0]
        item = self.sprav_treeCtrl.AppendItem(parent_item, name)
        self.sprav_treeCtrl.SetPyData(item, rec_dict)
        
        code = rec_dict['cod']
        if self.sprav.isSubCodes(code):
            # Есть подкоды. Для отображения + в контроле дерева
            # необходиом добавить фиктивный элемент
            self.sprav_treeCtrl.AppendItem(item, TREE_ITEM_LABEL)
        
    def set_sprav_tree(self):
        """
        Установить данные дерева справочника.
        """
        # Добавить корневой элемент дерева справочника
        sprav_res = self.sprav.GetResource() 
        sprav_title = sprav_res['description'] if sprav_res['description'] else sprav_res['name']
        # В случае многострочных наименования выделять только первую строку
        sprav_title = [line.strip() for line in sprav_title.split(u'\n')][0]

        self.root = self.sprav_treeCtrl.AddRoot(sprav_title)
        
        if self.sprav.isEmpty():
            # Справочник пустой. Заполнять не надо
            return
        
        self.set_sprav_level_tree(self.root)

        # Установить данные списка
        self.set_sprav_list(self.root)

        # Развернуть корневой элемент
        self.sprav_treeCtrl.Expand(self.root)
        
    def set_sprav_level_tree(self, parent_item, sprav_code=None, do_sort=True):
        """
        Добавить уровень дерева справочника.
        @param parent_item: Элемент дерева, в который происходит добавление.
        @param sprav_code: Код справочнка, ассоциируемый с элементом дерева.
        """
        # Добавить первый уровень дерева справочника
        sprav_storage = self.sprav.getStorage()
        level_data = sprav_storage.getLevelTable(sprav_code)
        # Отсортировать
        if do_sort and isinstance(level_data, list):
            level_data.sort()

        for record in level_data:
            self.set_sprav_tree_item(parent_item, record)

    def add_sprav_list_row(self, record, is_col_autosize=True):
        """
        Добавить новую строку в список справочника.
        @param record: Запись справочника асоциированая со строкой списка.
        @param is_col_autosize: Произвести после добавления строки
            автоматическое переразмеривание колонок?
        """
        fields = self.get_tab_editable_fields()
        list_item = -1
        for i, field in enumerate(fields):
            value = ic_str.toUnicode(record[field['name']])
            # В случае многострочных наименования выделять только первую строку
            value = [line.strip() for line in value.split(u'\n')][0]

            if i == 0:
                list_item = self.recs_listCtrl.InsertStringItem(sys.maxint, value, i)
                self._list_ctrl_dataset.append(record)
            else:
                self.recs_listCtrl.SetStringItem(list_item, i, value)                    
        
        if is_col_autosize:
            # Переразмерить колонки
            for i, field in enumerate(fields):
                self.recs_listCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
        
    def set_sprav_list(self, tree_item=None):
        """
        Установить данные списка справочника.
        @param tree_item: Элемент дерева, для которого необходимо
            отобразить список.
            Если не определен, то считаем что это корневой элемент.
        """
        if tree_item is None:
            tree_item = self.root
            
        self.recs_listCtrl.DeleteAllItems()
        # Список записей выбранного уровня справочника
        self._list_ctrl_dataset = list()
        
        child_item, cookie = self.sprav_treeCtrl.GetFirstChild(tree_item)
        while child_item.IsOk():
            record = self.sprav_treeCtrl.GetPyData(child_item)

            self.add_sprav_list_row(record, False)
            
            child_item, cookie = self.sprav_treeCtrl.GetNextChild(tree_item, cookie)

        # Переразмерить колонки
        fields = self.get_tab_editable_fields()
        for i in range(len(fields)):
            self.recs_listCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)

    def find_tree_child_item(self, item_text, cur_item=None):
        """
        Поиск дочернего элемента дерева по тексту.
        @param item_text: Текст элемента дерева.
        """
        if cur_item is None:
            cur_item = self.root
            
        find_item = None
        child_item, cookie = self.sprav_treeCtrl.GetFirstChild(cur_item)
        while child_item.IsOk():
            if item_text == self.sprav_treeCtrl.GetItemText(child_item):
                find_item = child_item
                break
            child_item, cookie = self.sprav_treeCtrl.GetNextChild(cur_item, cookie)
        return find_item

    def is_not_init_level_tree(self, item):
        """
        Проверка. Проинициализирована/Подгружена ветка элемента дерева?
        @param item: Элемент дерева.
        @return: True/False.
        """
        find_item = self.find_tree_child_item(TREE_ITEM_LABEL, item)
        return bool(find_item)

    def init_level_tree(self, item):
        """
        Проинициализировать ветку элемента дерева.
        @param item: Элемент дерева.
        """
        find_item = self.find_tree_child_item(TREE_ITEM_LABEL, item)
        if find_item:
            self.sprav_treeCtrl.Delete(find_item)

        # Заполнение пустого уровня
        if not self.sprav_treeCtrl.ItemHasChildren(item):
            record = self.sprav_treeCtrl.GetPyData(item)
            code = record['cod']
            self.set_sprav_level_tree(item, code)
        
    def refresh_sprav_tree_item(self, parent_item, sprav_code=None, sprav_record=None):
        """
        Обновить элемент дерева справочника.
        @param parent_item: Родительский элемент дерева.
        @param sprav_code: Код справочнка, ассоциируемый с элементом дерева.
        @param sprav_record: Запись справочника, ассоциируемая с элементом дерева.
        """
        find_item = self.find_sprav_tree_item(parent_item, sprav_code)
        if find_item:
            self.sprav_treeCtrl.SetPyData(find_item, sprav_record)
            self.sprav_treeCtrl.SetItemText(find_item, sprav_record['name'])

    def refresh_sprav_list_item(self, sprav_code=None, sprav_record=None):
        """
        Обновить элемент списка справочника.
        @param sprav_code: Код справочнка, ассоциируемый с элементом дерева.
        @param sprav_record: Запись справочника, ассоциируемая с элементом дерева.
        """
        find_idx = self.find_sprav_list_item(sprav_code)
        if find_idx:
            self._list_ctrl_dataset[find_idx] = sprav_record

            fields = self.get_tab_editable_fields()
            for i, field in enumerate(fields):
                value = ic_str.toUnicode(sprav_record[field['name']])
                self.recs_listCtrl.SetStringItem(find_idx, i, value)                    

    def del_sprav_tree_item(self, parent_item, sprav_code=None):
        """
        Удалить элемент дерева справочника.
        @param parent_item: Родительский элемент дерева.
        @param sprav_code: Код справочнка, ассоциируемый с элементом дерева.
        """
        find_item = self.find_sprav_tree_item(parent_item, sprav_code)
        if find_item:
            self.sprav_treeCtrl.Delete(find_item)

    def del_sprav_list_item(self, sprav_code=None):
        """
        Удалить элемент списка справочника.
        @param sprav_code: Код справочнка, ассоциируемый с элементом дерева.
        """
        find_idx = self.find_sprav_list_item(sprav_code)
        if find_idx:
            del self._list_ctrl_dataset[find_idx]
            self.recs_listCtrl.DeleteItem(find_idx)                    

    def add_sprav_tree_item(self, parent_item, new_record):
        """
        Добавить элемент дерева справочника.
        @param parent_item: Родительский элемент дерева.
        @param new_record: Новая добавляемая запись.
        """
        item = self.sprav_treeCtrl.AppendItem(parent_item, new_record['name'])
        self.sprav_treeCtrl.SetPyData(item, new_record)

    def add_sprav_list_item(self, new_record=None):
        """
        Добавить элемент списка справочника.
        @param new_record: Новая добавляемая запись.
        """
        self.add_sprav_list_row(new_record)

    def find_sprav_tree_item(self, parent_item, sprav_code=None):
        """
        Поиск элемента дерева справочника по коду справочника.
        @param parent_item: Родительский элемент дерева.
        @param sprav_code: Код справочнка, ассоциируемый с элементом дерева.
        @return: Найденный элемент дерева или None, если элемент не найден. 
        """
        # Поискать код в текущем элементе
        record = self.sprav_treeCtrl.GetPyData(parent_item)
        if record:
            if sprav_code == record['cod']:
                return parent_item
        
        # Поиск в дочерних элементах
        find_result = None
        child_item, cookie = self.sprav_treeCtrl.GetFirstChild(parent_item)
        while child_item.IsOk():
            record = self.sprav_treeCtrl.GetPyData(child_item)
            if record:
                if sprav_code == record['cod']:
                    find_result = child_item
                    break
            child_item, cookie = self.sprav_treeCtrl.GetNextChild(parent_item, cookie)
        
        # На этом уровне ничего не нашли
        # необходимо спуститься на уровень ниже
        if not find_result:
            child_item, cookie = self.sprav_treeCtrl.GetFirstChild(parent_item)
            while child_item.IsOk():
                self.init_level_tree(child_item)
                find_result = self.find_sprav_tree_item(child_item, sprav_code)
                if find_result:
                    break
                child_item, cookie = self.sprav_treeCtrl.GetNextChild(parent_item, cookie)
            
        return find_result

    def find_sprav_list_item(self, sprav_code=None):
        """
        Найти элемент списка справочника по коду.
        @param sprav_code: Код справочнка, ассоциируемый с элементом дерева.
        @return: Индекс найденного элемента списка или None, 
            если ничего не найдено.
        """
        find_result = None
        for idx, record in enumerate(self._list_ctrl_dataset):
            if sprav_code == record['cod']:
                find_result = idx
                break
        return find_result

    def select_sprav_tree_item(self, sprav_code, parent_item=None):
        """
        Найти и выбрать элемент дерева справочника по коду справочника.
        @param sprav_code: Код справочнка, ассоциируемый с элементом дерева.
        @return: Найденный элемент дерева или None, если элемент не найден. 
        """
        if parent_item is None:
            parent_item = self.root
        
        item = self.find_sprav_tree_item(parent_item, sprav_code)
        if item:
            self.sprav_treeCtrl.SelectItem(item)
            return item
        return None        
        
    def onSpravTreeItemCollapsed(self, event):
        """
        Обработчик сворачивания элемента дерева справочника.
        """
        event.Skip()

    def onSpravTreeItemExpanded(self, event):
        """
        Обработчик разворачивания элемента дерева справочника.
        """
        item = event.GetItem()
        self.init_level_tree(item)
            
        event.Skip()

    def onSpravTreeSelChanged(self, event):
        """
        Обработчик изменения выбора элемента дерева.
        """
        item = event.GetItem()

        self.init_level_tree(item)
        # Установить данные списка
        self.set_sprav_list(item)
        
        event.Skip()

    def onEditToolClicked(self, event):
        """
        Обработчик инструмента редактирования записи справочника.
        """
        rec_idx = self.recs_listCtrl.GetFirstSelected()
        if rec_idx != -1:
            record = self._list_ctrl_dataset[rec_idx]
            edit_rec = edit_record_sprav_dlg(parent=self, nsi_sprav=self.sprav, 
                                           record=record)
            if edit_rec:
                # Обновить запись в справочнике
                self.sprav.updateRec(edit_rec['cod'], edit_rec)
                self.refresh_sprav_tree_item(self.sprav_treeCtrl.GetSelection(), 
                                             edit_rec['cod'], edit_rec)
                self.refresh_sprav_list_item(edit_rec['cod'], edit_rec)
                
        event.Skip()

    def onDelToolClicked(self, event):
        """
        Обработчик инструмента удаления записи справочника.
        """
        rec_idx = self.recs_listCtrl.GetFirstSelected()
        if rec_idx != -1:
            record = self._list_ctrl_dataset[rec_idx]
            del_code = record['cod']
            if ic_dlg.icAskBox(u'УДАЛЕНИЕ', u'Удаление записи справочника <%s>. Вы уверены?' % record['name']):
                self.sprav.delRec(del_code)
                self.del_sprav_tree_item(self.sprav_treeCtrl.GetSelection(),
                                         del_code)
                self.del_sprav_list_item(del_code)
        event.Skip()

    def onAddToolClicked(self, event):
        """
        Обработчик инструмента добавления новой записи справочника.
        """
        # Заполнение записи значениями по умолчанию
        tab = self.sprav.getTable()
        default_record = tab.getDefaultRecDict()
        # Установить код по умолчанию
        parent_rec = self.sprav_treeCtrl.GetPyData(self.sprav_treeCtrl.GetSelection())
        struct_parent_code = self.sprav.StrCode2ListCode(parent_rec['cod']) if parent_rec else list()
        struct_parent_code = [sub_code for sub_code in struct_parent_code if sub_code]
        level = self.sprav.getLevelByIdx(len(struct_parent_code))
        struct_code = struct_parent_code
        if level:
            struct_code += ['0' * level.getCodLen()]            
        default_record['cod'] = ''.join(struct_code)
        
        add_rec = edit_record_sprav_dlg(parent=self, nsi_sprav=self.sprav, 
                                        record=default_record)
        if add_rec:
            # Контроль существующего кода
            if not self.sprav.isCod(add_rec['cod']):
                self.sprav.addRec(add_rec['cod'], add_rec)
                self.add_sprav_tree_item(self.sprav_treeCtrl.GetSelection(),
                                         add_rec)
                self.add_sprav_list_item(add_rec)
            else:
                msg = u'Код <%s> уже присутствует в справочнике <%s>' % (add_rec['cod'], self.sprav.getDescription())
                log.warning(msg)
                ic_dlg.icWarningBox(u'ОШИБКА', msg)
            
        event.Skip()

    def onSearchToolClicked(self, event):
        """
        Обработчик инструмента поиска по наименованию записи справочника.
        """
        search_txt = self.search_textCtrl.GetValue()
        if search_txt:
            do_find = True
            if self.not_actual_search:
                search_codes = self.sprav.getStorage().search(search_txt)
                if search_codes:
                    self.search_codes = search_codes
                    self.search_codes.sort()
                    self.search_code_idx = 0                    
                else:
                    ic_dlg.icWarningBox(u'ПРЕДУПРЕЖДЕНИЕ', u'Не найдены записи, соответствующие строке поиска')
                    do_find = False
                self.not_actual_search = False
            else:
                # Если не надо обновлять список найденных кодов, то просто
                # искать следующий код в списке
                self.search_code_idx += 1
                if self.search_code_idx >= len(self.search_codes):
                    self.search_code_idx = 0
                    
            if do_find:
                find_code = self.search_codes[self.search_code_idx]
                self.select_sprav_tree_item(find_code)
        else:
            ic_dlg.icWarningBox(u'ПРЕДУПРЕЖДЕНИЕ', u'Не выбрана строка поиска')
            
        event.Skip()        

    def find_word_in_records(self, find_word, start_row=None, start_col=None):
        """
        Поиск слова в текущем списке записей справочника.
        @param find_word: Искомое слово.
        @param start_row: Начальная строка для начала поиска.
            Если не указана, то берется первая.
        @param start_col: Начальная колонка для начала поиска.
            Если не указана, то берется первая.
        @return: Индекс записи, индекс поля, где найдено слово. 
            Или None если ничего не найдено.
        """
        if start_row is None:
            start_row = 0
        if start_col is None:
            start_col = 0

        find_word = find_word.lower()
        fields = self.get_tab_editable_fields()
        for i_row, row in enumerate(self._list_ctrl_dataset[start_row:]):
            if i_row == 0:
                for i_col, field in enumerate(fields[start_col:]):
                    field_name = field['name']
                    value = ic_str.toUnicode(row[field_name]).lower()
                    if find_word in value:
                        log.debug(u'Найдено соответствие %s <%s> в <%s>'  % (field_name, find_word, value))
                        return start_row+i_row, start_col+i_col
            else:
                for i_col, field in enumerate(fields):
                    field_name = field['name']
                    value = ic_str.toUnicode(row[field_name]).lower()
                    if find_word in value:
                        log.debug(u'Найдено соответствие в поле %s <%s> : <%s>'  % (field_name, find_word, value))
                        return start_row+i_row, i_col
        log.warning(u'Не найдено <%s> в списке. Поиск окончен.' % find_word)
        return None

    def findWordInRecordsListCtrl(self, start_row=None):
        """
        Процедура поиска слова в списке текущих записей.
        @param start_row: Начальная строка поиска. Если не определено,
            то поиск производится с текущей выбранной строки.
        """
        cur_row = start_row
        if cur_row is None:
            cur_row = self.getItemSelectedIdx(self.recs_listCtrl)

        # log.debug(u'Текущая выбранная строка <%d>' % cur_row)
        find_word = self.find_textCtrl.GetValue()
        find_result = self.find_word_in_records(find_word, start_row=cur_row + 1)

        do_find = find_result is not None

        if do_find:
            find_row, find_col = find_result
            self.selectItem_list_ctrl(self.recs_listCtrl, find_row)
        else:
            msg = u'Не найдено поисковое слово. Начать поиск с начала?'
            if ic_dlg.icAskBox(u'ВНИМАНИЕ', msg):
                self.findWordInRecordsListCtrl(-1)

    def onFindToolClicked(self, event):
        """
        Обработчик инструмента поиска записи справочника по ключевому слову.
        """
        find_txt = self.find_textCtrl.GetValue()
        if find_txt:
            self.findWordInRecordsListCtrl()
        else:
            ic_dlg.icWarningBox(u'ПРЕДУПРЕЖДЕНИЕ', u'Не выбрана строка поиска')
            
        event.Skip()        
        
    def onSearchText(self, event):
        """
        Обработчик изменения строки поиска.
        """
        search_txt = event.GetString()
        log.debug(u'Change search text <%s>' % search_txt)
        self.not_actual_search = True
        event.Skip()
        
    def onOkButtonClick(self, event):
        """
        Обработчик кнопки <OK>.
        """
        self.EndModal(wx.ID_OK)
        event.Skip()
        
        
def edit_sprav_dlg(parent=None, nsi_sprav=None):
    """
    Вызов формы редактирования справочника.
    @param parent: Родительское окно.
    @param nsi_sprav: Объект редактируемого справочника.
    @return: True/False.
    """
    if parent is None:
        app = wx.GetApp()
        main_win = app.GetTopWindow()
        parent = main_win

    dlg = icSpravEditDlg(nsi_sprav=nsi_sprav, parent=parent)
    # dlg.init()
    result = dlg.ShowModal() == wx.ID_OK
    dlg.Destroy()
    return result


def edit_record_sprav_dlg(parent=None, nsi_sprav=None, record=None):
    """
    Вызов формы редактирования записи справочника.
    @param parent: Родительское окно.
    @param nsi_sprav: Объект редактируемого справочника.
    @param record: Словарь редактируемой записи.
    @return: Отредактированный словарь записи или None в случае ошибки.
    """
    if parent is None:
        app = wx.GetApp()
        main_win = app.GetTopWindow()
        parent = main_win

    dlg = icSpravRecEditDlg(nsi_sprav=nsi_sprav, record=record, parent=parent)
    # dlg.init()
    result = dlg.ShowModal()
    
    edit_record = None
    if result == wx.ID_OK:
        edit_record = dlg.getEditRecord()
    dlg.Destroy()
    return edit_record
    
    
def test():
    """
    Функция тестирования.
    """
    from ic import config

    log.init(config)

    app = wx.PySimpleApp()
    dlg = icSpravRecEditDlg(parent=None)
    dlg.ShowModal()
    app.MainLoop()


if __name__ == '__main__':
    test()
