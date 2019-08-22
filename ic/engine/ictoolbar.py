#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль класса панели инструментов.
"""

# --- Подключение библиотек ---
import wx
import os.path

from ic.utils import execfunc
from ic.utils import toolfunc
from ic.bitmap import bmpfunc
from ic.log import log

from ic.kernel import icobject
from . import icmenuitem

__version__ = (0, 1, 1, 1)

# --- Основные константы ---
HORIZ_ORIENT = 1
VERT_ORIENT = 0
FLOAT_TOOLBAR = 1
NOFLOAT_TOOLBAR = 0

# Спецификации:
SPC_IC_TOOLBAR = {'description': '',
                  'title': '',  # Заголовок
                  'pos': (0, 0),  # Координаты размещения панели инструментов
                  'size': (-1, -1),  # Размеры панели инструментов
                  'orientation': HORIZ_ORIENT,  # Ориентация
                  'float': NOFLOAT_TOOLBAR,  # Признак плавающей панели инструментов
                  'child': [],  # Список инструментов
                  }

SPC_IC_TOOL = {'description': '',
               'item': '',  # Имя прикрепленного пункта меню.
               'short_help': '',  # <подсказка отображаемая в статусной строке, строка >,
               'enabled': 1,  # <признак включеного/выключенного инструмента, флаг (0/1)>,
               'checkable': 0,  # <признак помечаемого инструмента, флаг (0/1)>,
               'checked': 0,  # <признак отметки инструмента, флаг (0/1)>,
               'radio': 0,  # <признак переключаемого инструмента, флаг (0/1)>,
               'image': '',  # <файл значка инструмента, строка>,
               'help': '',  # <файл помощи по F1, строка>,
               'onAction': {},  # <действие при щелчке на инструмента, словарь функции>,
               'onCheckOn': {},  # <действие при отметке инструмента, словарь функции>,
               'onCheckOff': {},  # <действие при разметке инструмента, словарь функции>,
               }


def CreateICToolBar(Win_, MenuBar_, Name_, ToolbarData_):
    """
    Функция создает из ресурса панель инструментов.
    @param Win_  : окно,  в котором располагается панель инструментов.
    @param MenuBar_: объект горизонтального меню,  к которому прекрепляется 
                панель инструментов.
    @param Name_: имя панели инструментов.
    @param ToolbarData_: Данные о панели инструментов.
    @return: Возвращает ссылку на объект панели инструментов 
        или None в случае ошибки.
    """
    try:
        if not ToolbarData_:
            log.info(u'Данные о панели %s не найдены!' % Name_)
            return None
        return icToolBar(Win_, MenuBar_, Name_, ToolbarData_)
    except:
        log.fatal(u'Ошибка создания панели инструментов %s' % Name_)
    return None


def CreateICToolBars(Win_, MenuBar_, Names_, ToolbarData_):
    """
    Функция создает список панелей инструментов по списку имен.
    @param Win_  : окно,  в котором располагается панель инструментов.
    @param MenuBar_: объект горизонтального меню,  к которому прекрепляется 
                панель инструментов.
    @param Names_: Список имен панелей инструментов.
    @param ToolbarData_: имя ресурсного файла или 
        словарь данных панелей инструментов.
    @return: Возвращает список объектов панелей инструментов 
        или None в случае ошибки.
    """
    toolbars = []
    for toolbar_name in Names_:
        toolbars.append(CreateICToolBar(Win_, MenuBar_, toolbar_name, ToolbarData_))
    return toolbars


# --- Классы ---
class icToolBar(wx.ToolBar, icobject.icObject):
    """
    Класс панели инструментов.
    """

    def __init__(self, Win_, MainMenu_, Name_, ToolBarStruct_, ResData_=None):
        """
        Конструктор.
        """
        icobject.icObject.__init__(self, Name_)
        
        # --- Свойства класса ---
        # Имя объекта
        self._Name = ''
        # ИМя ресурсного файла
        self._ResData = ''
        # Окно к которому прикриплено меню
        self._Window = None
        # Меню,  к которой прикреплена панель инструментов
        self._MainMenu = None
        # Реестр всех инструментов (доступ можно производить по Id и по имени)
        self._register = {}
        # Функции пользователя (доступ можно производить по Id и по имени)
        # Действие при щелчке на инструменте
        self._tools_action = {}
        # Действия при отметке/разметке инструмента
        self._tools_check_on = {}
        self._tools_check_off = {}
        # Словарик связей инструментов с пунктами меню
        self._tool_item = {}
    
        try:
            # Расширение структуры до спецификации
            ToolBarStruct_ = toolfunc.defineSpcStruct(SPC_IC_TOOLBAR, ToolBarStruct_)

            self._Name = Name_
            self._ResData = ResData_
            self._Window = Win_
            self._MainMenu = MainMenu_
            
            top = 0
            left = 0
            if 'pos' in ToolBarStruct_ and ToolBarStruct_['pos']:
                left = ToolBarStruct_['pos'][0]
                top = ToolBarStruct_['pos'][1]
            pos = wx.Point(left, top)
            width = 0
            height = 0
            if 'size' in ToolBarStruct_ and ToolBarStruct_['size']:
                width = ToolBarStruct_['size'][0]
                height = ToolBarStruct_['size'][1]
            if width < 0 and height < 0:
                size = wx.Size(-1, 20)
            else:
                size = wx.Size(width, height)
            style = wx.TB_FLAT | wx.TB_DOCKABLE
            if 'orientation' in ToolBarStruct_ and ToolBarStruct_['orientation'] is not None and \
               ToolBarStruct_['orientation'] == VERT_ORIENT:
                style |= wx.TB_VERTICAL
            else:
                style |= wx.TB_HORIZONTAL
            title = ''
            if 'title' in ToolBarStruct_ and ToolBarStruct_['title'] is not None:
                title = ToolBarStruct_['title']

            # Вызов конструктора предка
            wx.ToolBar.__init__(self, self._Window, self._Window.GetId(),
                                pos, size, style, self._Name)

            # Установить размеры картинок по высоте панели инструментов
            self.SetToolBitmapSize(wx.Size(size[1]-4, size[1]-4))

            # По умолчанию панель инструментов не плавающая
            tool_float = 0
            if 'float' in ToolBarStruct_ and ToolBarStruct_['float'] is not None:
                tool_float = ToolBarStruct_['float']
            # Установить заголовок
            self.SetTitle(title)

            self.DoToolBar(ToolBarStruct_)
        except:
            log.fatal(u'Ошибка создания объекта панели инструментов %s!' % self._Name)

    def DoToolBar(self, ToolBarStruct_):
        """
        Создать инструменты в панели инструментов.
        @param ToolBarStruct_: Словарно-списковая структура, описывающия 
            панель инструментов (см формат файла ресурсов движка).
        @return: Возвращает указатель на объект панели инструментов 
            или None в случае ошибки.
        """
        try:
            toolbar_load = False
            toolbar_link = False

            # Перед загрузкой удалить все
            self.RemoveAll()

            for tool in ToolBarStruct_['child']:
                if 'item' in tool and tool['item']:
                    # Присоединить инструмент к пункту меню
                    toolbar_link = self.AddToLinkToolBar(tool)
                else:
                    # Загрузить инструмент как отдельный ресурс
                    toolbar_load = self.AddToLoadToolBar(tool)

            if toolbar_load or toolbar_link: 
                if self._Window:
                    self._Window.SetToolBar(self)
                # Активировать панель инструментов (ОБЯЗАТЕЛЬНО ПОСЛЕ СОЗДАНИЯ!!!)
                self.Realize()
            return self
        except:
            log.fatal(u'Ошибка загрузки панели инструментов')
        return None

    def AddToLoadToolBar(self, ToolItem_):
        """
        Догрузить панель инструментов.
        @param ToolItem_: Ресурс инструмента.
        @return: Возвращает указатель на объект панели инструментов 
            или None в случае ошибки.
        """
        try:
            # Проверка аргументов
            if not ToolItem_:
                return None
            # Загрузить структуру пункта
            # if isinstance(self._ResData, str):
            #    tool_struct = ic.utils.ic_res.loadObjStruct(ic.utils.ic_res.RES_IDX_TOOL, tool_name, self._ResData)
            # elif type(self._ResData)==DictType:
            #    tool_struct=self._ResData[tool_name]
            # else:
            #    log.info( 'Ошибка загрузки панели инструментов!')
            #    return None
            # Если инструмент с таким именем уже существует,  то не создавать его
            tool_name = ToolItem_['name']
            tool = self.FindToolByAlias(tool_name)
            if tool is None:
                # Проверка на ограничение доступа
                self.AppendTool(tool_name, tool)
            return self
        except:
            log.fatal(u'Ошибка загрузки панели инструментов %s' % self._Name)
        return None

    def AddToLinkToolBar(self, ToolItem_):
        """
        Создать инструменты в панели инструментов и связать их с существующими пунктами главного меню.
        @param ToolItem_: Ресурс инструмента.
        @return: Возвращает ссылку на панель инструментов 
            или None в случае ошибки.
        """
        try:
            # Проверка аргументов
            if not ToolItem_:
                return None

            item_name = ToolItem_['item']
            item = self._MainMenu.FindItemByAlias(item_name)
            # Если инструмент с таким именем уже существует,  то не создавать его
            tool = self.FindToolByAlias(item_name)
            if tool is None:
                # Проверка на ограничение доступа
                self.AppendToolByItem(item_name, item)
            return self
        except:
            log.fatal(u'Ошибка добавления инструментов в панель %s' % self._Name)
        return None

    def RemoveAll(self):
        """
        Удаление всех инструментов.
        """
        try:
            for tool_id in self._register:
                self.DeleteTool(tool_id)
            # очистить реестр
            self.ClearReg()
            # Очистка всех списков функций
            self._tools_action.clear()
            self._tools_check_on.clear()
            self._tools_check_off.clear()
        except:
            log.fatal(u'Ошибка удаления инструментов из панели %s!' % self._Name)

    def FindToolByAlias(self, Name_):
        """
        Найти объект по его имени.
        @param Name_: Имя-идентификатор инструмента.
        @return: Возвращает найденный объект или None в случае неудачного поиска.
        """
        if Name_ in self._register:
            return self._register[Name_]
        return None 

    def FindToolByID(self, ID_):
        """
        Найти объект по его ID.
        @param ID_: Номер-идентификатор инструмента.
        @return: Возвращает найденный объект или None в случае неудачного поиска.
        """
        if ID_ in self._register:
            return self._register[ID_]
        return None 

    def Register(self, Tool_, ID_, Name_=''):
        """
        Прописать в реестре.
        @param Tool_: Объект инструмента.
        @param ID_: Номер-идентификатор инструмента.
        @param Name_: Имя-идентификатор инструмента.
        """
        if ID_ in self._register:
            self._register[ID_] = Tool_
        if Name_ != '':
            if Name_ in self._register:
                self._register[Name_] = Tool_

    def ClearReg(self):
        """
        Очистка реестра.
        """
        if self._register != {}:
            self._register.clear()

    def AppendTool(self, ToolName_, ToolStruct_):
        """
        Добавить инструмент.
        @param ToolName_: Имя-идентификатор инструмента.
        @param ToolStruct_: Словарь, описывающий инструмент
            (см формат файла ресурса движка).
        @return: Возвращает инструмент или None в случае ошибки.
        """
        try:
            # Расширение структуры до спецификации
            ToolStruct_ = toolfunc.defineSpcStruct(SPC_IC_TOOL, ToolStruct_)
            # Добавить новый инструмент на панель
            tool = None
            tool_id = wx.NewId()
            if 'short_help' in ToolStruct_ and ToolStruct_['short_help'] is not None:
                tool_hint = ToolStruct_['short_help']
            else:
                tool_hint = ''
            if 'onAction' in ToolStruct_:
                tool_tools_action = ToolStruct_['onAction']
            else:
                tool_tools_action = {}
            if 'onCheckOn' in ToolStruct_:
                tool_tools_check_on = ToolStruct_['onCheckOn']
            else:
                tool_tools_check_on = {}
            if 'onCheckOff' in ToolStruct_:
                tool_tools_check_off = ToolStruct_['onCheckOff']
            else:
                tool_tools_check_off = {}
            
            # Если новый пункт не разделитель, тогда это обычный пункт
            if tool_hint == icmenuitem.MENU_SEPARATOR:
                # Новый пункт-разделитель
                self.AddSeparator()
            else:
                # Определить образ
                # (ЕСЛИ ОБРАЗА НЕТ, ТО ДОБАВЛЕНИЕ ИНСТРУМЕНТА НЕ ПРОИЗОЙДЕТ)
                if 'image' in ToolStruct_:
                    if ToolStruct_['image'] != '' and ToolStruct_['image'] is not None:
                        if os.path.isfile(ToolStruct_['image']):
                            tool_image = bmpfunc.createBitmap(ToolStruct_['image'])
                        else:
                            return None
                    else:
                        return None
                else:
                    return None

                if 'checkable' in ToolStruct_ and ToolStruct_['checkable'] is not None and \
                   ToolStruct_['checkable']:
                    tool = self.AddCheckTool(tool_id, tool_image, wx.NullBitmap, '', tool_hint)
                    # Добавить в список методов
                    if tool_tools_check_on != {}:
                        self._tools_check_on[tool_id] = tool_tools_check_on
                    if tool_tools_check_off != {}:
                        self._tools_check_off[tool_id] = tool_tools_check_off
                else:
                    if 'radio' in ToolStruct_ and ToolStruct_['radio'] is not None and \
                       ToolStruct_['radio']:
                        tool = self.AddRadioTool(tool_id, tool_image, wx.NullBitmap, '', tool_hint)
                    else:
                        # Создать простой инструмент
                        tool = self.AddSimpleTool(tool_id, tool_image, '', tool_hint)
                # Проверки на блокировку инструмента
                tool_enabled = 1
                if 'enabled' in ToolStruct_ and ToolStruct_['enabled'] is not None and \
                   not ToolStruct_['enabled']:
                    tool_enabled = 0
                # Проверка на ограничение доступа к функциональному ресурсу
                # if not ic_acc.icCanAuthent(ic_acc.ACCESS_USE, ToolName_, ic_acc.ACC_TOOLITEM, False):
                #     tool_enabled = 0
                tool.Enable(tool_enabled)
                
                # Добавить в список методов
                if tool_tools_action != {}:
                    self._tools_action[tool_id] = tool_tools_action
                # Установить обработчик
                self.Bind(wx.EVT_TOOL, self.OnToolClick, id=tool_id)
                # Прописать в реестре
                self.Register(tool, tool_id, ToolName_)
                return tool
        except:
            log.fatal(u'Ошибка создания инструмента %s!' % ToolName_)
        return None

    def AppendToolByItem(self, ItemName_, Item_):
        """
        Создать инструмент по пункту меню.
        @param ItemName_: Имя-идентификатор пункта меню.
        @param Item_: Объект пункта меню.
        @return: Возвращает указатель на инструмент или None в случае ошибки.
        """
        tool = None
        try:
            # Проверка аргументов
            if Item_ is None and ItemName_ != '':
                # Новый пункт-разделитель
                self.AddSeparator()
                return None
            elif Item_ is None:
                return None

            tool_kind = Item_.GetKind()
            # Если новый пункт не разделитель, тогда это обычный пункт
            if tool_kind != wx.ITEM_SEPARATOR:
                # Добавить новый инструмент на панель
                tool_id = wx.NewId()
                tool_hint = Item_.GetHelp()
                # Определить образ
                if tool_kind != wx.ITEM_RADIO:
                    tool_image = Item_.GetBitmap()
                else:
                    tool_image = wx.ArtProvider.GetBitmap(wx.ART_TICK_MARK, wx.ART_OTHER, (16, 16))

                if tool_kind == wx.ITEM_CHECK:
                    tool = self.AddCheckTool(tool_id, tool_image, wx.NullBitmap, '', tool_hint)
                    # Синхронизировать изображение
                    self.ToggleTool(tool_id, Item_.IsChecked())
                else:
                    if tool_kind == wx.ITEM_RADIO:
                        tool = self.AddRadioTool(tool_id, tool_image, wx.NullBitmap, '', tool_hint)
                        # Синхронизировать изображение
                        self.ToggleTool(tool_id, Item_.IsChecked())
                    else:
                        if tool_kind == wx.ITEM_NORMAL:
                            # Создать простой инструмент
                            tool = self.AddSimpleTool(tool_id, tool_image, '', tool_hint)
                # Проверки на блокировку инструмента
                tool_enabled = Item_.IsEnabled()
                # Проверка на ограничение доступа к функциональному ресурсу
                # if not ic_acc.icCanAuthent(ic_acc.ACCESS_USE, ItemName_, ic_acc.ACC_MENUITEM, False):
                #     tool_enabled = 0
                self.EnableTool(tool_id, tool_enabled)

                # Установить обработчик
                self.Bind(wx.EVT_TOOL, self.OnToolItemClick, id=tool_id)
                # Прописать в реестре
                self.Register(tool, tool_id, ItemName_)
                # Установить взаимную связь инструмента и пункта меню
                self._tool_item[tool_id] = Item_
                Item_.LinkTool(self, tool_id)
            else:
                # Новый пункт-разделитель
                self.AddSeparator()
                return None
            return tool 
        except:
            log.fatal(u'Ошибка создания инструмента %s по пункту меню' % ItemName_)
        return None

    def OnToolClick(self, event):
        """
        Обработчик нажатия кнопки инструмента (БЕЗ ПРИВЯЗКИ К ПУНКТУ МЕНЮ).
        """
        try:
            # Определить объект, который вызвал событие
            tool_id = event.GetId()
            tool_state = self.GetToolState(tool_id)
            # Если это инструмент, тогда выполнить его
            if tool_id in self._tools_action and self._tools_action[tool_id] is not None:
                # Выполнение метода
                execfunc.execute_method(self._tools_action[tool_id], self)
            if tool_state:
                if tool_id in self._tools_check_off and self._tools_check_off[tool_id] is not None:
                    # Выполнение метода
                    result = execfunc.execute_method(self._tools_check_on[tool_id], self)
                    # Проверка выполнения метода
                    if result is not None:
                        # Если метод запрещает переключение,
                        # то переключить пункт в старое положение
                        if not result:
                            self.ToggleTool(tool_id, False)
            else:
                if tool_id in self._tools_check_on and self._tools_check_on[tool_id] is not None:
                    # Выполнение метода
                    result = execfunc.execute_method(self._tools_check_off[tool_id], self)
                    # Проверка выполнения метода
                    if result is not None:
                        # Если метод запрещает переключение,
                        # то переключить пункт в старое положение
                        if not result:
                            self.ToggleTool(tool_id, True)
        except:
            log.fatal(u'Ошибка обработчика инструмента панели инструментов')
            event.Skip()

    def OnToolItemClick(self, event):
        """
        Обработчик нажатия кнопки инструмента (ПРИВЯЗАННОГО К ПУНКТУ МЕНЮ).
        """
        try:
            # Определить объект, который вызвал событие
            tool_id = event.GetId()
            if tool_id in self._tool_item and self._tool_item[tool_id] is not None:
                item = self._tool_item[tool_id]
            else:
                event.Skip()
                return
            
            if item.GetKind() != wx.ITEM_NORMAL:
                # Синхронизировать изображение
                item.Check(not item.IsChecked())

            # Выполнение действия
            item.DoAction()
        except:
            log.fatal(u'Ошибка обработчика кнопки панели инструментов')
            event.Skip()

    # --- Функции-свойства ---
    def GetWindow(self):
        """
        Определить окно.
        """
        return self._Window   

    def GetAlias(self):
        return self._Name

    def GetResFile(self):
        if isinstance(self._ResData, str):
            return self._ResData
        else:
            return ''

    def GetMainMenu(self):
        return self._MainMenu
