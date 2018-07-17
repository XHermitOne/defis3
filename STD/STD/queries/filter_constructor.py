#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Виджет конструктора фильтров.
"""

# Version
__version__ = (0, 0, 0, 3)

# Imports
import wx
from wx.lib.agw import hypertreelist
import ic
from ic.kernel import io_prnt
from ic.imglib import constructor_img as img_lib
from ic.components import icEvents
import copy
from . import filter_builder_env
from . import filter_builder_ctrl

# Constants
DEFAULT_ITEM_LABEL = ''


class icFilterConstructorTreeList(hypertreelist.HyperTreeList):
    """
    Контрол конструктора фильтров.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        kwargs['agwStyle'] = wx.TR_HAS_VARIABLE_ROW_HEIGHT | wx.TR_HAS_BUTTONS | wx.TR_FULL_ROW_HIGHLIGHT | wx.TR_DEFAULT_STYLE
        hypertreelist.HyperTreeList.__init__(self, *args, **kwargs)

        # По умолчанию тема Vista
        self.SetHilightFocusColour(wx.WHITE)
        self.SetHilightNonFocusColour(wx.WHITE)
        pen = wx.Pen(wx.WHITE)
        self.SetBorderPen(pen)
        # Окружение конструктора
        self.environment = None
        
        # Корневой элемент
        self.root = None
        
        # Текущий выбранный пользоватетем элемент
        self._selected_item = None

    def Clear(self):
        """
        Очистить все пункты.
        """
        if self.GetMainWindow():
            self._selected_item = None
            result = self.GetMainWindow().DeleteAllItems()
            if self.root:
                self.GetMainWindow().DeleteItemWindow(self.root)
            return result
        return None
        
    def setEnvironment(self, Env_=None):
        """
        Установить окружение для работы редактора.
        @param Env_: Окружение, словарно-списковая структура формата
        filter_builder_env.FILTER_ENVIRONMENT.
        """
        self.environment = Env_
        
    def getEditResult(self):
        """
        Получить результат редактирования.
        """
        return self._getFilterData()

    getFilterData = getEditResult
    
    def setEditResult(self, Result_):
        """
        Инициализация редактора по отредактированному значению.
        """
        self._addDefaultColumn()
        self.Clear()
        result = self._setFilterData(Result_)
        # Раскрыть дерево
        self.expandRoot()
        return result
        
    setFilterData = setEditResult

    def getColumnCount(self):
        """
        Количество колонок.
        """
        if self.GetMainWindow():
            return self.GetMainWindow().GetColumnCount()
        return -1
    
    _column_width = (75, 200, 100, 250, 250)

    def _addDefaultColumn(self):
        """
        Добавить колонки по умолчанию, если они не созданы.
        """
        cols = [u'Группа', u'Атрибут', u'Условие', u'Значение 1', u'Значение 2']
        if self.getColumnCount() <= 0:
            for i in range(5):
                self.AddColumn(cols[i], width=self._column_width[i])
        
    def expandRoot(self):
        """
        Раскрыть корневой элемент.
        """
        if self.root:
            self.Expand(self.root)
     
    def addGroup(self, item=None, bAutoExpand_=True):
        """
        Добавить группу в элемент.
        @return: Объект нового элемента дерева.
        """
        # ВНИМАНИЕ! Родителя у добавляемых контролов надо указывать self.GetMainWindow()
        logic_combobox = filter_builder_ctrl.icLogicLabelChoice(self.GetMainWindow(),
                                                                self.environment['logic'])
        logic_combobox.Select(0)

        add_button = filter_builder_ctrl.icBitmapButton(self.GetMainWindow(), -1,
                                                        bitmap=img_lib.plus_small,
                                                        size=(img_lib.plus_small.GetWidth()+4,
                                                              img_lib.plus_small.GetHeight()+4),
                                                        style=wx.NO_BORDER)
        self.Bind(wx.EVT_BUTTON, self.onAddButtonMouseClick, add_button)
        
        if item is None:
            # Если  элемент не указан, то установить корень
            self.root = self.AddRoot(DEFAULT_ITEM_LABEL, wnd=add_button)
            item = self.root
            new_item = self.root
        else:
            new_item = self.AppendItem(item, DEFAULT_ITEM_LABEL, wnd=add_button)
        self.SetPyData(new_item, 'group')   # Прописать тип элемента
        
        # Установить контролы на новом элементе
        self.SetItemWindow(new_item, logic_combobox, 1)
        # Автоматически раскрывать?
        if bAutoExpand_:
            if not self.IsExpanded(item):
                self.Expand(item)
        return new_item

    def delGroup(self, item=None):
        """
        Удалить группу, соответствующую элементу.
        """
        if item:
            if item == self.root:
                # Если удаляется корневой элемент, то
                # очистить все и создать корень по умолчанию
                pass
            else:
                parent = self.GetItemParent(item)
                prev_item = self.GetPrevSibling(item)
                self.Delete(item)
                if prev_item:
                    self.SelectItem(prev_item)
                elif parent:
                    self.SelectItem(parent)
                
    def addCompare(self, item=None, bAutoExpand_=True):
        """
        Добавить условие в элемент.
        @return: Объект нового элемента дерева.
        """
        # ВНИМАНИЕ! Родителя у добавляемых контролов надо указывать self.GetMainWindow()
        requisite_combobox = filter_builder_ctrl.icRequisiteLabelChoice(self.GetMainWindow(),
                                                                        self.environment['requisites'])
        requisite_combobox.Bind(icEvents.EVT_LABEL_CHANGE,
                                self.onRequisiteChangeComboBox)

        del_button = filter_builder_ctrl.icBitmapButton(self.GetMainWindow(), -1,
                                                        bitmap=img_lib.cross_small,
                                                        size=(img_lib.cross_small.GetWidth()+8,
                                                              img_lib.cross_small.GetHeight()+8),
                                                        style=wx.NO_BORDER)
        self.Bind(wx.EVT_BUTTON, self.onDelButtonMouseClick, del_button)
        
        new_item = self.AppendItem(item, DEFAULT_ITEM_LABEL, wnd=del_button)
        self.SetPyData(new_item, 'compare')     # Прописать тип элемента
        
        # Установить контролы на новом элементе
        self.SetItemWindow(new_item, requisite_combobox, 1)
        # Автоматически раскрывать?
        if bAutoExpand_:
            if not self.IsExpanded(item):
                self.Expand(item)
        return new_item
                
    def delCompare(self, item=None):
        """
        Удалить условие, соответствующее элементу.
        """
        if item:
            parent = self.GetItemParent(item)
            prev_item = self.GetPrevSibling(item)
            self.Delete(item)
            if prev_item:
                self.SelectItem(prev_item)
            elif parent:
                self.SelectItem(parent)
        
    def setFuncChoice(self, item, RequisiteComboBox_):
        """
        Установить в указанный элемент контрол выбора функций, 
            соответствующих выбранному реквизиту.
        """
        requisite = RequisiteComboBox_.getSelectedRequisite()
        func_lst = self._getFuncList(requisite['funcs'], self.environment)
        # Если в элементе уже существуют контролы, которые
        # зависят от выбранного реквизита, то удалить их
        for i_col in range(2, self.GetColumnCount()):
            item.DeleteWindow(i_col)
            
        # Добавить комбобокс выбора функции сравнения
        func_combobox = filter_builder_ctrl.icFuncLabelChoice(self.GetMainWindow(), func_lst)

        func_combobox.Bind(icEvents.EVT_LABEL_CHANGE, self.onFuncChangeComboBox)
        # Установить контролы на элементе
        self.SetItemWindow(item, func_combobox, 2)
        
    def setArgsEdit(self, item, FuncComboBox_):
        """
        Установить в указанный элемент контролы редактирования аргументов, 
            соответствующих выбранной функции.
        """
        func = FuncComboBox_.getSelectedFunc()
        args_lst = func['args']
        # Если в элементе уже существуют контролы, которые
        # зависят от выбранной функции сравнения, то удалить их
        for i_col in range(3, self.GetColumnCount()):
            item.DeleteWindow(i_col)
        # Добавить редакторы аргументов
        i_col = 3
        for arg in args_lst:
            if 'type' not in arg:
                if 'ext_edit' in arg and arg['ext_edit']:
                    if not arg['ext_edit']:
                        # Расширенный редактор не определен
                        arg_edit = filter_builder_ctrl.icCustomArgEdit(self.GetMainWindow(), arg)
                    else:
                        ext_args = ()
                        if 'ext_args' in arg and arg['ext_args']:
                            ext_args = arg['ext_args']
                        ext_kwargs = ()
                        if 'ext_kwargs' in arg and arg['ext_kwargs']:
                            ext_kwargs = arg['ext_kwargs']
                        # Расширенный редактор задается в явном виде
                        arg_edit = arg['ext_edit'](parent=self.GetMainWindow(),
                                                   id=wx.NewId(), *ext_args, **ext_kwargs)

                        requisite_combobox = self.GetItemWindow(item, 1)
                        requisite = requisite_combobox.getSelectedData() or {}
                        if requisite.get('type', None) == filter_builder_env.REQUISITE_TYPE_NSI:
                            # Для реквизита НСИ кроме создания редактора необходимо
                            # привязать его к правильному справочнику
                            psp = requisite.get('nsi_psp', None)
                            if psp:
                                arg_edit.setSpravByPsp(psp)
                            else:
                                io_prnt.outWarning(u'Не определен паспорт НСИ для реквизита <%s>' % requisite['requisite'])
                else:
                    # По умолчанию создаем редактор строк
                    arg_edit = filter_builder_ctrl.icStrArgEdit(self.GetMainWindow(), arg)
            else:
                if arg['type'] == filter_builder_env.REQUISITE_TYPE_STR:
                    arg_edit = filter_builder_ctrl.icStrArgEdit(self.GetMainWindow(), arg)
                elif arg['type'] in (filter_builder_env.REQUISITE_TYPE_INT,
                                     filter_builder_env.REQUISITE_TYPE_FLOAT,
                                     filter_builder_env.REQUISITE_TYPE_NUM):
                    arg_edit = filter_builder_ctrl.icNumArgEdit(self.GetMainWindow(), arg)
                else:
                    io_prnt.outLog(u'Не определен тип <%s> аргумента <%s>' % (arg['type'], arg))
                    return None
        
            # Установить контролы на элементе
            if arg_edit:
                arg_edit_size = wx.Size(self.GetColumnWidth(i_col), -1)
                arg_edit.SetSize(arg_edit_size)

            self.SetItemWindow(item, arg_edit, i_col)
            i_col += 1
        
    def _getFuncList(self, Funcs_, Env_):
        """
        Получить список функций сравнений.
        """
        func_lst = list()
        if Funcs_:
            for func in Funcs_:
                if type(func) in (str, unicode):
                    # Функция сравнения задана именем
                    func_lst.append(Env_['funcs'][func])
                else:
                    func_lst.append(func)
        else:
            io_prnt.outWarning(u'Конструктор фильтров. Не определен список функций сравнения')
        return func_lst
        
    def _findItemByCtrl(self, Ctrl_, Item_=None):
        """
        Найти какой пункт соответствует указанному контролу.
        """
        if Item_ is None:
            Item_ = self.root
        if Item_:
            col_count = self.getColumnCount()
            # Поискать по колонкам в текущем элементе
            for i in range(col_count):
                window = self.GetItemWindow(Item_, i)
                if window == Ctrl_:
                    # Нашли
                    return Item_
            if Item_.HasChildren():
                # Если не нашли в текущем элементе, то поискать в дочерних
                for child in Item_.GetChildren():
                    find_item = self._findItemByCtrl(Ctrl_, child)
                    if find_item:
                        return find_item
        # Не нашли
        return None
        
    def _getSelectedItem(self):
        """
        Выбранный пользователем элемент.
        """
        return self._selected_item
    
    def _setSelectedItem(self, Item_):
        """
        Установить выбранный пользователем элемент.
        """
        if self.GetMainWindow().GetRootItem():
            self._selected_item = Item_
            if self._selected_item:
                self.SelectItem(self._selected_item)
        
    def onAddButtonMouseClick(self, event):
        """ 
        Обработчик нажатия на кнопке добавления нового элемента.
        """
        add_button = event.GetEventObject()
        # Если нажали на кнопку, то выбрали соответствующий элемент
        tree_item = self._findItemByCtrl(add_button)
        self._setSelectedItem(tree_item)
            
        # Выпадающее меню
        menu = wx.Menu()
        
        id = wx.NewId()
        item = wx.MenuItem(menu, id, u'Добавить условие')
        bmp = img_lib.node_select_child
        item.SetBitmap(bmp)
        menu.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.onAddCompareMenuItem, id=id)
        
        id = wx.NewId()
        item = wx.MenuItem(menu, id, u'Добавить группу')
        bmp = img_lib.node_select
        item.SetBitmap(bmp)
        menu.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.onAddGroupMenuItem, id=id)
        
        if tree_item != self.root:
            menu.AppendSeparator()
            id = wx.NewId()
            item = wx.MenuItem(menu, id, u'Удалить группу')
            bmp = img_lib.node_delete_previous
            item.SetBitmap(bmp)
            menu.AppendItem(item)
            self.Bind(wx.EVT_MENU, self.onClearMenuItem, id=id)
        
        self.PopupMenu(menu)
        menu.Destroy()
        
        event.Skip()

    def onAddCompareMenuItem(self, event):
        """
        Добавить условие.
        """
        self.addCompare(self._getSelectedItem())
        event.Skip()
        
    def onAddGroupMenuItem(self, event):
        """
        Добавить группу.
        """
        self.addGroup(self._getSelectedItem())
        event.Skip()
        
    def onClearMenuItem(self, event):
        """
        Очистить все.
        """
        self.delGroup(self._getSelectedItem())
        event.Skip()

    def onDelButtonMouseClick(self, event):
        """
        Обработчик клика на кнопке удаления.
        """
        del_button = event.GetEventObject()
        # Если нажали на кнопку, то выбрали соответствующий элемент
        self._setSelectedItem(self._findItemByCtrl(del_button))
        
        self.delCompare(self._getSelectedItem())
        
        event.Skip()

    def onRequisiteChangeComboBox(self, event):
        """
        Смена реквизита в комбобоксе выбора реквизитов.
        """
        requisite_combobox = event.GetICObject()
        # Если выбираем реквизит, то надо сделать соответствующий элемент
        # дерева активным
        self._setSelectedItem(self._findItemByCtrl(requisite_combobox))
        
        self.setFuncChoice(self._getSelectedItem(), requisite_combobox)
        
        event.Skip()
        
    def onFuncChangeComboBox(self, event):
        """
        Смена функции сравнения в комбобоксе выбора функций.
        """
        func_combobox = event.GetICObject()
        # Если выбираем функцию сравнения, то надо сделать соответствующий элемент
        # дерева активным
        self._setSelectedItem(self._findItemByCtrl(func_combobox))
        
        self.setArgsEdit(self._getSelectedItem(), func_combobox)

        event.Skip()
        
    def setDefault(self):
        """
        Настроить конструктор по умолчанию.
        """
        self._addDefaultColumn()
        self.Clear()
        # Добавить корневой элемент
        self.addGroup()
        # Раскрыть дерево
        self.expandRoot()
       
    def clearTree(self):
        """
        Очистить дерево фильтра.
        """
        self.Clear()
        # Добавить корневой элемент
        self.addGroup()
        # Раскрыть дерево
        self.expandRoot()
    
    def _getFilterData(self, Item_=None, bAddPreSQL_=False):
        """
        Получить отредактированные данные.
        """
        if Item_ is None:
            Item_ = self.root
            
        item_data = {}
        
        # Добавить сам элемент
        type_item = self.GetPyData(Item_)
        if type_item == 'group':
            # Группа
            item_data['type'] = type_item
            logic_combobox = self.GetItemWindow(Item_, 1)
            item_data['name'] = logic_combobox.getSelectedData()['name']
            item_data['logic'] = item_data['name']
            item_data['children'] = []
        elif type_item == 'compare':
            # Сравнение
            item_data['type'] = type_item
            
            requisite_combobox = self.GetItemWindow(Item_, 1)
            requisite = requisite_combobox.getSelectedData() or {'name': None}
            item_data['requisite'] = requisite['name']
            
            func_combobox = self.GetItemWindow(Item_, 2)
            func = None
            if func_combobox:
                func = func_combobox.getSelectedData() or {'name': None}
                item_data['func'] = func['name']

            for i_col in range(3, self.GetColumnCount()):
                arg_edit = self.GetItemWindow(Item_, i_col)
                if arg_edit:
                    item_data['arg_'+str(i_col-2)] = arg_edit.getValue()

            # Дополнительная функция получения аргументов
            if 'get_args' in func:
                item_data['get_args'] = func['get_args']

            # Добавить в данные фильтра дополнительные данные для
            # последующей генерации SQL
            if bAddPreSQL_:
                kwargs = dict()
                kwargs['requisite'] = requisite
                if func:
                    args = func['args']
                    for i, arg in enumerate(args):
                        value = item_data['arg_'+str(i+1)]
                        kwargs[arg['name']] = value
                    compare_function = func['func']
                    if compare_function:   
                        item_data['__sql__'] = compare_function(**kwargs)
        else:
            io_prnt.outLog(u'Ошибка определения типа элемента конструктора фильтров <%s>' % type_item)
            return None
        
        # Добавить дочерние элементы
        for item in Item_.GetChildren():
            child = self._getFilterData(item, bAddPreSQL_)
            if self._is_valid_requisite(child):
                item_data['children'].append(child)
        return item_data
        
    def _is_valid_requisite(self, req):
        """
        """
        if not req:
            return False
        
        if req.get('type', None) == 'compare' and (req.get('func', None) and
           req.get('requisite', None)):
            return True
        elif req.get('type', None) == 'group':
            return True
        return False
        
    def _setFilterData(self, Data_, Item_=None):
        """
        Установить данные.
        Функция может запускаться только после инициализации окружения.
        """
        result = True
        
        if Item_ is None:
            self.Clear()
            
        if Data_['type'] == 'group':
            # Обработка группы
            grp_item = self.addGroup(Item_)
            
            logic_combobox = self.GetItemWindow(grp_item, 1)
            if logic_combobox:
                logic_combobox.selectByName(Data_['name'])            
                
            if 'children' in Data_:
                # Обработка дочерних элементов
                for child in Data_['children']:
                    result = result and self._setFilterData(child, grp_item)
                
        elif Data_['type'] == 'compare':
            # Обработка сравнения
            compare_item = self.addCompare(Item_)
            
            requisite_combobox = self.GetItemWindow(compare_item, 1)
            if requisite_combobox:
                requisite_combobox.selectByName(Data_['requisite'])
                self.setFuncChoice(compare_item, requisite_combobox)
                
            func_combobox = self.GetItemWindow(compare_item, 2)
            if func_combobox:
                func_combobox.selectByName(Data_['func'])
                self.setArgsEdit(compare_item, func_combobox)
                
            for i_col in range(3, self.GetColumnCount()):
                arg_edit = self.GetItemWindow(compare_item, i_col)
                if arg_edit:
                    arg_edit.setValue(Data_['arg_'+str(i_col-2)])
        else:
            io_prnt.outLog(u'Ошибка определения типа элемента конструктора фильтров <%s>' % Data_['type'])
            return False
        return result
     
    def setVistaTheme(self):
        """
        Установить тему Windows Vista.
        """
        self.EnableSelectionGradient(False)
        self.EnableSelectionVista(True)


def test():
    """
    Тестовая функция.
    """
    import copy
    mwin = ic.getKernel().GetContext().getMainWin()
    print('TEST filter constructor START ... ok')
    env = copy.deepcopy(filter_builder_env.FILTER_ENVIRONMENT)
    
    app = wx.PySimpleApp()
    dlg = wx.Dialog(mwin,-1)
    constructor = icFilterConstructorTreeList(dlg, -1)
    constructor.setEnvironment(env)
    constructor.setDefault()
    dlg.ShowModal()
    app.MainLoop()
    
    print('TEST filter constructor STOP ... ok')

if __name__ == '__main__':
    test()
