#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Виджеты используемые в редакторе фильтров.
"""

# Version
__version__ = (0, 0, 0, 2)

# Imports
import wx
import wx.combo
import wx.lib.platebtn

from ic.kernel import io_prnt
from ic.dlg import ic_dlg
from ic.bitmap import ic_bmp
from ic.components import icEvents

# Constants
DEFAULT_COMBO_SIZE = (200, -1)
DEFAULT_EDIT_SIZE = (100, -1)


class icCustomComboCtrl(wx.combo.ComboCtrl):
    """
    Абстрактный класс контрола вызова расширенного редактора.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        wx.combo.ComboCtrl.__init__(self, *args, **kwargs)
        # Нарисовать кнопку выбора
        self._drawCustomButton()
        
    def _drawCustomButton(self):
        """
        Создание кнопки вызова расширенного выбора.
        """
        # make a custom bitmap showing "..."
        bw, bh = 14, 16
        bmp = wx.EmptyBitmap(bw, bh)
        dc = wx.MemoryDC(bmp)

        # clear to a specific background colour
        bgcolor = wx.Colour(255, 254, 255)
        dc.SetBackground(wx.Brush(bgcolor))
        dc.Clear()

        # draw the label onto the bitmap
        label = "..."
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        tw, th = dc.GetTextExtent(label)
        dc.DrawText(label, (bw-tw)/2, (bw-tw)/2)
        del dc

        # now apply a mask using the bgcolor
        bmp.SetMaskColour(bgcolor)

        # and tell the ComboCtrl to use it
        self.SetButtonBitmaps(bmp, True)

    def DoSetPopupControl(self, popup):
        """
        Overridden from ComboCtrl to avoid assert since there is no ComboPopup.
        """
        pass
    
    def OnButtonClick(self):
        """
        Обработчик нажатия на кнопку расширенного выбора из списка.
        """
        pass

    def getValue(self):
        return self.GetValue()


class icCustomChoice(icCustomComboCtrl):
    """
    Класс контрола расширенного выбора из указанного списка.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        icCustomComboCtrl.__init__(self, *args, **kwargs)
        
        # Список выбора
        self.choice = []
        
        # Структура управления контролом
        self.filter_env = None
        
        # Индекс выбранного элемента
        self.choice_idx = -1
        
        # Данные выбора
        self.data = None

    def setData(self, Data_=None):
        """
        установить данные выбора.
        """
        if Data_ is None:
            self.data = []
        else:
            self.data = Data_
            choice = [element['description'] for element in self.data]
            self.setChoice(choice)
        return self.data
        
    def setChoice(self, Choice_=None):
        """
        Установить список выбора.
        """
        if Choice_ is None:
            self.choice = []
        else:
            self.choice = Choice_
        
    def OnButtonClick(self):
        """
        Обработчик нажатия на кнопку расширенного выбора из списка.
        """
        if self.choice:
            idx = ic_dlg.icSingleChoiceIdxDlg(self, u'ВЫБОР',
                                              u'Выберите один из следующих элементов', self.choice)
            self.choice_idx = idx
            if idx >= 0:
                self.SetValue(self.choice[idx])


class icArgExtendedEdit(icCustomComboCtrl):
    """
    Класс контрола расширенного редактора значения аргумента функции.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        icCustomComboCtrl.__init__(self, *args, **kwargs)

        # Значение по умолчанию
        self.default = None
        # Дополнительные данные для редактора
        self.data = None

        # Функция вызова расширенного редактора
        self.ext_edit_func = None

    def OnButtonClick(self):
        """
        Обработчик нажатия на кнопку расширенного выбора из списка.
        """
        if self.ext_edit_func:
            result = self.ext_edit_func(self, self.data, self.default)
            if result is not None:
                self.SetValue(str(result))

# Constants
DEFAULT_IMG_WIDTH = 16
DEFAULT_IMG_HEIGHT = 16


class icPlateButton(wx.lib.platebtn.PlateButton):
    """
    Нативные кнопки.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        wx.lib.platebtn.PlateButton.__init__(self, *args, **kwargs)


class icBitmapButton(wx.BitmapButton):
    """
    Нативные кнопки  с картинками.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        wx.BitmapButton.__init__(self, *args, **kwargs)
        self.SetBackgroundColour(wx.WHITE)


class icBitmapComboBox(wx.combo.BitmapComboBox):
    """
    Класс комбобокса с картинкой.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        wx.combo.BitmapComboBox.__init__(self, *args, **kwargs)
        
        self._cur_selected_item = -1
        
        self.items = None

        self.Bind(wx.EVT_COMBOBOX, self.onCombo, self)
     
    def Select(self, Item_):
        """
        Выбрать элемент  с индексом.
        """
        self._cur_selected_item = Item_
        return wx.combo.BitmapComboBox.Select(self, Item_)
    
    def onCombo(self, event):
        """
        Изменение выбора.
        """
        self._cur_selected_item = event.GetSelection()
        event.Skip()
        
    def getCurrentSelection(self):
        """
        Текущий выбранный элемент.
        """
        return self._cur_selected_item
        
    def appendItems(self, Items_):
        """
        Добавить список выбора комбобокса.
        @param Items_: Список пунктов выбора структуры:
        [{
            'name':'Наименование пункта',
            'description':'Описание пункта (появляется в компоненте)',
            'img': Образ пункта (м.б. задан строкой, которую нужно выполнить ic_eval),
            'data': Любые прикрепляемые к пункту данные
        },...]
        """
        if self.items is None:
            self.items = []
            
        self.items += list(Items_)
        
        # Перебрать элементы
        for item in list(Items_):
            name = item['name']
            description = item['description']
            img = None
            if 'img' in item:
                img = item['img']
                if img and (type(img) in (str, unicode)):
                    img = ic_bmp.getSysImg(img)
            if img is None:
                img = wx.EmptyBitmap(DEFAULT_IMG_WIDTH, DEFAULT_IMG_HEIGHT)
            
            self.Append(description, img, name)
  
    def getSelectedData(self):
        """
        Данные, соответствующие выбранному элементу.
        """
        selected = self.getCurrentSelection()
        if selected >= 0:
            return self.items[selected]
        return None
        
    def setItems(self, Items_):
        """
        Установить список выбора комбобокса.
        @param Items_: Список пунктов выбора структуры:
        [{
            'name':'Наименование пункта',
            'description':'Описание пункта (появляется в компоненте)',
            'img': Образ пункта (м.б. задан строкой, которую нужно выполнить ic_eval),
            'data': Любые прикрепляемые к пункту данные
        },...]        
        """
        self.Clear()
        self.items = None
        self.appendItems(Items_)
   
    def selectByName(self, Name_):
        """
        Выбрать элемент по его имени.
        @return: Индекс выбранного элемента.
        """
        item_names = [item['name'] for item in self.items]
        try:
            i = item_names.index(Name_)
        except:
            io_prnt.outLog(u'Элемент с именем <%s> среди <%s> не найден.' % (Name_, item_names))
            i = -1
        self.Select(i)
        return i


class icItemComboBox(wx.ComboBox):
    """
    Класс комбобокса итемов.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        wx.ComboBox.__init__(self, *args, **kwargs)
        
        self.items = None

    def appendItems(self, Items_):
        """
        Добавить пункты в выпадающий список.
        @param Items_:
        [{
            'name':'Наименование пункта',
            'description':'Описание пункта (появляется в компоненте)',
            'data': Любые прикрепляемые к пункту данные
        },...]        
        """
        if self.items is None:
            self.items = []
            
        self.items += list(Items_)
        
        for item in list(Items_):
            name = item['name']
            description = item['description']
            data = None
            if 'data' in item:
                data = item['data']
            
            self.Append(description, data)
        
    def getSelectedData(self):
        """
        Данные, соответствующие выбранному элементу.
        """
        selected = self.GetCurrentSelection()
        if selected >= 0:
            return self.items[selected]
        return None
    
    def setItems(self, Items_):
        """
        Установить пункты в выпадающий список.
        @param Items_:
        [{
            'name':'Наименование пункта',
            'description':'Описание пункта (появляется в компоненте)',
            'data': Любые прикрепляемые к пункту данные
        },...]        
        """
        self.Clear()
        self.items = None
        self.appendItems(Items_)
        
    def selectByName(self, Name_):
        """
        Выбрать элемент по его имени.
        @return: Индекс выбранного элемента.
        """
        item_names = [item['name'] for item in self.items]
        try:
            i = item_names.index(Name_)
        except:
            io_prnt.outLog(u'Элемент с именем <%s> среди <%s> не найден.' % (Name_, item_names))
            i = -1
        self.Select(i)
        return i


class icLogicOperationsComboBox(icBitmapComboBox):
    """
    Комбобокс выбора логической операции.
    """

    def __init__(self, parent, items=None):
        """
        Конструктор.
        """
        if items is None:
            from . import filter_builder_env
            items = filter_builder_env.DEFAULT_ENV_LOGIC_OPERATIONS
        style = wx.CB_READONLY | wx.CB_DROPDOWN
        icBitmapComboBox.__init__(self, parent, id=wx.NewId(),
                                  size=DEFAULT_COMBO_SIZE, style=style)
        self.appendItems(items)


class icRequisiteComboBox(icItemComboBox):
    """
    Комбобокс выбора реквизита.
    """

    def __init__(self, parent, requisites=None):
        """
        Конструктор.
        """
        style = wx.CB_READONLY | wx.CB_DROPDOWN
        icItemComboBox.__init__(self, parent, id=wx.NewId(),
                                size=DEFAULT_COMBO_SIZE, style=style)
        if requisites:
            self.appendItems(requisites)
            
    def getSelectedRequisite(self):
        """
        Структуры, соответствующая выбранному реквизиту.
        """
        selection = self.GetCurrentSelection()
        if selection >= 0:
            return self.items[selection]
        return None        


class icFuncComboBox(icBitmapComboBox):
    """
    Комбобокс выбора условий/функций сравнения реквизита со значением.
    """

    def __init__(self, parent, compare_funcs=None):
        """
        Конструктор.
        """
        style = wx.CB_READONLY | wx.CB_DROPDOWN
        icBitmapComboBox.__init__(self, parent, id=wx.NewId(),
                                  size=DEFAULT_COMBO_SIZE, style=style)
        if compare_funcs:
            self.appendItems(compare_funcs)
            
    def getSelectedFunc(self):
        """
        Структуры, соответствующая выбранной функции сравнения.
        """
        selection = self.getCurrentSelection()
        if selection >= 0:
            return self.items[selection]
        return None        
        
    
class icArgEdit(wx.TextCtrl):
    """
    Редактор абстрактного аргумента.
    """

    def __init__(self, parent, arg=None):
        """
        Конструктор.
        @param parent: Родительское окно.
        @param arg: Структура аргумента.
        """
        wx.TextCtrl.__init__(self, parent, id=wx.NewId(),
                             size=DEFAULT_EDIT_SIZE)
        
        tool_tip = None
        if 'description' in arg:
            tool_tip = arg['description']
        if tool_tip:
            self.SetToolTipString(self._to_unicode(tool_tip))
            
        default = None
        if 'default' in arg:
            default = arg['default']
        if default:
            self.SetValue(self._to_unicode(default))
            
    def _to_unicode(self, Value_):
        """
        Приведение значения любого типа к юникоду.
        """
        if isinstance(Value_, unicode):
            return Value_
        else:
            return unicode(str(Value_), 'utf8')
        
    getValue = wx.TextCtrl.GetValue
    setValue = wx.TextCtrl.SetValue


class icNumArgEdit(icArgEdit):
    """
    Редактор числового аргумента.
    """

    def __init__(self, parent, arg=None):
        """
        Конструктор.
        @param parent: Родительское окно.
        @param arg: Структура аргумента.
        """
        icArgEdit.__init__(self, parent, arg)


class icStrArgEdit(icArgEdit):
    """
    Редактор строкового аргумента.
    """

    def __init__(self, parent, arg=None):
        """
        Конструктор.
        @param parent: Родительское окно.
        @param arg: Структура аргумента.
        """
        icArgEdit.__init__(self, parent, arg)


class icCustomArgEdit(icCustomComboCtrl):
    """
    Редактор аргумента с расширенным редактором.
    """

    def __init__(self, parent, arg=None):
        """
        Конструктор.
        @param parent: Родительское окно.
        @param arg: Структура аргумента.
        """
        icCustomComboCtrl.__init__(self, parent, -1, size=wx.Size(-1, 20))


class icLabelChoice(wx.StaticText):
    """
    Абстрактный класс выбора элемента на базе статического текста.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        wx.StaticText.__init__(self, *args, **kwargs)
        
        # Текущий выбранный элемент
        self._cur_selected_item = -1
        
        # Формат представления элемента
        self._format = '%s'
        
        # Текст пустого выбора
        self._none_label_txt = '<...>'
        
        # Пункты выбора
        self.items = None
        
        # Вспомогательный словарь соответствия идентификаторов пунктов меню с
        # элементами выбора
        self._menuitem_item_dict = None
        
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseClick)
                
    def LabelChangeEvent(self):
        """
        Посылает сообщение <icEvents.EVT_LABEL_CHANGE>.
        """
        event = icEvents.icLabelChangeEvent(icEvents.icEVT_LABEL_CHANGE, self.GetId())
        event.SetICObject(self)
        return self.GetEventHandler().AddPendingEvent(event)
    
    def setItems(self, Items_):
        """
        Установить пункты.
        """
        self.items = Items_
        
    def Select(self, Item_):
        """
        Выбрать элемент.
        """
        if isinstance(Item_, int):
            self._cur_selected_item = Item_
            label_txt = self._format % self.items[self._cur_selected_item]['description']
        elif isinstance(Item_, dict):
            try:
                self._cur_selected_item = self.items.index(Item_)
                label_txt = self._format % self.items[self._cur_selected_item]['description']
            except ValueError:
                self._cur_selected_item = -1
                label_txt = self._none_label_txt
        else:
            self._cur_selected_item = -1
            label_txt = self._none_label_txt
        self.SetLabel(label_txt)
   
    def _createSelectMenu(self, Items_):
        """
        Создание меню выбора.
        """
        self._menuitem_item_dict = {}
        
        menu = wx.Menu()
        if Items_:
            for item in Items_:
                text = item['description'] if item['description'] else item['name']
                img = None
                if 'img' in item:
                    img = item['img']
            
                id = wx.NewId()
                menu_item = wx.MenuItem(menu, id, text)
                if img:
                    menu_item.SetBitmap(img)
                menu.AppendItem(menu_item)
                self.Bind(wx.EVT_MENU, self.onSelectMenuItem, id=id)
            
                self._menuitem_item_dict[id] = item
        else:
            io_prnt.outWarning(u'Конструктор фильтров. Не определены пункты для выбора функции')

        return menu
        
    def onMouseClick(self, event):
        """
        Обработчик клика мышкой на контроле.
        """
        old_selected = self.getCurrentSelection()
        
        menu = self._createSelectMenu(self.items)
        self.PopupMenu(menu)
        menu.Destroy()
        
        new_selected = self.getCurrentSelection()
        
        if old_selected != new_selected:
            self.LabelChangeEvent()
            
        event.Skip()
        
    def onSelectMenuItem(self, event):
        """
        Обработчик выбора пункта меню.
        """
        menu_item_id = event.GetId()
        selected_item = self._menuitem_item_dict[menu_item_id]
        self.Select(selected_item)
        
        self._menuitem_item_dict = None
        event.Skip()
        
    def getCurrentSelection(self):
        """
        Текущий выбранный элемент.
        """
        return self._cur_selected_item
        
    def getSelectedData(self):
        """
        Данные, соответствующие выбранному элементу.
        """
        selected = self.getCurrentSelection()
        if selected >= 0:
            return self.items[selected]
        return None

    def selectByName(self, Name_):
        """
        Выбрать элемент по его имени.
        @return: Индекс выбранного элемента.
        """
        item_names = [item['name'] for item in self.items]
        try:
            i = item_names.index(Name_)
        except:
            io_prnt.outLog(u'Элемент с именем <%s> среди <%s> не найден.' % (Name_, item_names))
            i = -1
        self.Select(i)
        return i
    
    def getLabelStrip(self):
        """
        Получить надпись без дополнительных форматных вставок.
        """
        return self.GetLabel().strip()


class icLogicLabelChoice(icLabelChoice):
    """
    Контрол выбора логики.
    """

    def __init__(self, parent, items=None):
        """
        Конструктор.
        """
        if items is None:
            from . import filter_builder_env
            items = filter_builder_env.DEFAULT_ENV_LOGIC_OPERATIONS
        icLabelChoice.__init__(self, parent, wx.NewId(), '<...>')
        self.SetForegroundColour(wx.Colour(128, 0, 0))
        if items:
            self.setItems(items)


class icRequisiteLabelChoice(icLabelChoice):
    """
    Контрол выбора реквизита.
    """

    def __init__(self, parent, requisites=None):
        """
        Конструктор.
        """
        icLabelChoice.__init__(self, parent, wx.NewId(), '<...>')
        self._format = '[%s]'
        self.SetForegroundColour(wx.Colour(0, 0, 128))
        if requisites:
            self.setItems(requisites)
            
    def getSelectedRequisite(self):
        """
        Структуры, соответствующая выбранному реквизиту.
        """
        selection = self.getCurrentSelection()
        if selection >= 0:
            return self.items[selection]
        return None        

    def getLabelStrip(self):
        """
        Получить надпись без дополнительных форматных вставок.
        """
        return self.GetLabel()[1:-1].strip()


class icFuncLabelChoice(icLabelChoice):
    """
    Контрол выбора функции.
    """        
    def __init__(self, parent, compare_funcs=None):
        """
        Конструктор.
        """
        icLabelChoice.__init__(self, parent, wx.NewId(), '<...>')
        self.SetForegroundColour(wx.Colour(0, 128, 0))
        if compare_funcs:
            self.setItems(compare_funcs)
        
    def getSelectedFunc(self):
        """
        Структуры, соответствующая выбранной функции сравнения.
        """
        selection = self.getCurrentSelection()
        if selection >= 0:
            return self.items[selection]
        return None        
        

from ic.components.user import icdatepickerctrl


class icDateArgExtEdit(icdatepickerctrl.icDatePickerCtrl):
    """
    Контрол расширенного редактора аргумента.
    Редакттор выбора даты.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        icdatepickerctrl.icDatePickerCtrl.__init__(self, *args, **kwargs)

        # Значение по умолчанию
        self.default = None
