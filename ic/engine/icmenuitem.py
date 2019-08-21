#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль описания компонента пункта выпадающего меню.

@type SPC_IC_MENUITEM: C{dictionary}
@var SPC_IC_MENUITEM: Спецификация на ресурсное описание компонента icMenuItem.
Описание ключей SPC_IC_MENUITEM:
    - B{name = 'description'}: Описание.
    - B{name = 'caption'}: Надпись.
    - B{name = 'hot_key'}: Горячая клавиша.
    - B{name = 'hint'}: Надпись, показываемая в статусной строке главного окна.
    - B{name = 'enabled'}: Вкл./выкл. пункт меню.
    - B{name = 'checkable'}: Признак помчаемого пункта меню.
    - B{name = 'checked'}: Признак метки.
    - B{name = 'radio'}: Признак переключаемого пункта меню.
    - B{name = 'image'}: Образ пункта меню.
    - B{name = 'help'}: Файл помощи.
    - B{name = 'onAction'}: Скрипт, выполняемый при щелчке/выборе пункта.
    - B{name = 'onCheckOn'}: Скрипт, выполняемый при отметке пункта.
    - B{name = 'onCheckOff'}: Скрипт, выполняемый при снятии метки пункта.
"""

# --- Подключение библиотек ---
import wx

import ic.utils.ic_res
import ic.utils.ic_exec
import ic.bitmap.ic_color as ic_color
import ic.utils.ic_util
import ic.utils.util
from ic.log import log
from ic.bitmap import bmpfunc
from . import user_manager

import ic

__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_MENUITEM = {'type': 'MenuItem',
                   'label': 'Item',   # Надпись
                   'description': '',
                   'active': True,    # Активация пункта меню
                   'hot_key': '',    # Горячая клавиша
                   'short_help': '',      # Всплывающая подсказка
                   'enabled': True,     # Вкл./выкл. пункт меню
                   'checkable': False,  # Признак помчаемого пункта меню
                   'checked': False,    # Признак метки
                   'radio': False,      # Признак переключаемого пункта меню
                   'image': '',     # Файл образа пункта меню
                   'bitmap': None,  # Паспорт образа пункта меню
                   'help': '',      # Файл помощи
                   'onAction': None,      # Блок кода на выбор пункта
                   'onCheckOn': None,     # Блок кода на пометку пункта
                   'onCheckOff': None,    # Блок кода на разметку пункта
                   }

# Символ разделителя в надписи пункта
# Если текст пункта меню равен этому символу, тогда это разделитель
MENU_SEPARATOR = '-'


class icMenuItem(wx.MenuItem):
    """
    Класс пункта меню.
    """

    def __init__(self, ParentMenu_, ItemName_, ItemStruct_, context=None):
        """
        Конструктор.
        """
        # Контекст
        self.context = context
        # --- Свойства класса ---
        # Имя (уникальное!!!)
        self._Name = ''
        # Команда, выполняющаяся при выборе пункта меню
        self._Action = dict()
        # Команда, выполняющаяся при отметке пункта меню
        self._CheckOn = dict()
        # Команда, выполняющаяся при разметке пункта меню
        self._CheckOff = dict()
        # Окно к которому прикриплен пункт меню
        self._Window = None
        # Родительское меню
        self._ParentMenu = None

        # Признак включенного пункта (ТОЛЬКО для пунктов РАДИО!)
        self._radio_checked = False
        # Предыдущий и следующий элемент группы Radio (ТОЛЬКО для пунктов РАДИО!)
        self._RadioPrev = None
        self._RadioNext = None
        # Информация о привязанном инструменте
        self._Toolbar = None
        self._ToolID = 0
        # Собственная метка, необходимая для обновления состояния
        # помечаемых и радио пунктов в всплывающем меню
        self._SelfChecked = 0

        try:
            self._ParentMenu = ParentMenu_
            item_id = wx.NewId()
            self._Name = ItemName_
            item_name = self._Name + str(item_id)
            item_hotkey = ''

            # Расширение структуры до спецификации
            ItemStruct_ = ic.utils.ic_util.SpcDefStruct(SPC_IC_MENUITEM, ItemStruct_)

            if 'hot_key' in ItemStruct_ and ItemStruct_['hot_key']:
                item_hotkey = ItemStruct_['hot_key']
            if 'label' in ItemStruct_ and ItemStruct_['label']:
                if ItemStruct_['label'] != MENU_SEPARATOR:
                    item_label = ItemStruct_['label']
                    if item_hotkey:
                        item_label = item_label + '\t' + item_hotkey
                else:
                    return
            item_checkable = False
            if 'checkable' in ItemStruct_ and ItemStruct_['checkable'] is not None:
                item_checkable = ItemStruct_['checkable']
            item_radio = False
            if 'radio' in ItemStruct_ and ItemStruct_['radio'] is not None:
                item_radio = ItemStruct_['radio']

            item_kind = wx.ITEM_NORMAL
            if item_checkable:
                item_kind = wx.ITEM_CHECK
            else:
                if item_radio:
                    item_kind = wx.ITEM_RADIO
            # Создать пункт
            wx.MenuItem.__init__(self, ParentMenu_, item_id, item_label,
                                 item_name, item_kind, None)
            # Инициализировать некоторые атрибуты
            self._Window = self._ParentMenu.GetWindow()
            if 'onAction' in ItemStruct_:
                self._Action = ItemStruct_['onAction']
            else:
                if 'action' in ItemStruct_:
                    self._Action = ItemStruct_['action']
            if 'onCheckOn' in ItemStruct_:
                self._CheckOn = ItemStruct_['onCheckOn']
            else:
                if 'check_on' in ItemStruct_:
                    self._CheckOn = ItemStruct_['check_on']
            if 'onCheckOff' in ItemStruct_:
                self._CheckOff = ItemStruct_['onCheckOff']
            else:
                if 'check_off' in ItemStruct_:
                    self._CheckOff = ItemStruct_['check_off']

            if 'bitmap' in ItemStruct_ and ItemStruct_['bitmap']:
                self.setBitmap(ItemStruct_['bitmap'])
            elif 'image' in ItemStruct_ and ItemStruct_['image']:
                self.SetImage(ItemStruct_['image'])

            item_hint = ''
            if 'short_help' in ItemStruct_ and ItemStruct_['short_help'] is not None:
                item_hint = ItemStruct_['short_help']
            self.SetHelp(item_hint)

            # --- Обработка РАДИО пунктов ---
            # Установка признака метки (ТОЛЬКО для РАДИО ПУНКТОВ!)
            self._radio_checked = item_kind == wx.ITEM_RADIO and self.is_checked()
            # Установить связи RADIO GROUP
            last_item = self._ParentMenu.GetLastItem()
            if last_item is not None:
                if last_item.GetKind() == wx.ITEM_RADIO:
                    self._RadioPrev = last_item
                    last_item.SetRadioNext(self)

            # Установить цвета

            # ВНИМАНИЕ! Цвета необходимо установливать до присоединения
            #            пункта к меню!

            if 'foreground_colour' in ItemStruct_ and ItemStruct_['foreground_colour'] is not None:
                if isinstance(ItemStruct_['foreground_colour'], tuple):
                    self.SetTextColour(wx.Colour(ItemStruct_['foreground_colour'][ic_color.I_RED],
                                                 ItemStruct_['foreground_colour'][ic_color.I_GREEN],
                                                 ItemStruct_['foreground_colour'][ic_color.I_BLUE]))
                else:
                    try:
                        self.SetTextColour(ItemStruct_['foreground_colour'])
                    except:
                        pass
            if 'background_colour' in ItemStruct_ and ItemStruct_['background_colour'] is not None:
                if isinstance(ItemStruct_['foreground_colour'], tuple):
                    self.SetBackgroundColour(wx.Colour(ItemStruct_['background_colour'][ic_color.I_RED],
                                                       ItemStruct_['background_colour'][ic_color.I_GREEN],
                                                       ItemStruct_['background_colour'][ic_color.I_BLUE]))
                else:
                    try:
                        self.SetBackgroundColour(ItemStruct_['background_colour'])
                    except:
                        pass

            # ---------------------------------
            # Добавить новый пункт выпадающего меню

            # ВНИМАНИЕ:
            #    Без добавления, пункты не будут отображаться в меню.

            self._ParentMenu.AppendItem(self)
            if self._Window:
                self._Window.Bind(wx.EVT_MENU, self.OnActionItem, id=self.GetID())
                self._Window.Bind(wx.EVT_MENU_HIGHLIGHT, self.OnHighlight, id=self.GetID())
                if item_kind == wx.ITEM_CHECK or item_kind == wx.ITEM_RADIO:
                    self._Window.Bind(wx.EVT_UPDATE_UI, self.OnUpdate, id=item_id)

            # Установить атрибуты пункта меню

            # ВНИМАНИЕ:
            #    Все атрибуты пункта необходимо менять после прсоединения
            #    к меню, иначе атрибуты не отобразятся в меню

            if self.IsCheckable():
                item_checked = False
                if 'checked' in ItemStruct_ and ItemStruct_['checked'] is not None:
                    item_checked = ItemStruct_['checked']
                self.Check(item_checked)
            item_enabled = True
            if 'enabled' in ItemStruct_ and ItemStruct_['enabled'] is not None:
                item_enabled = ItemStruct_['enabled']
            # Проверка на ограничение доступа к функциональному ресурсу
            if not user_manager.canAuthent(user_manager.ACCESS_USE, self._Name, user_manager.ACC_MENUITEM, False):
                item_enabled = False

            wx.MenuItem.Enable(self, item_enabled)

            self._SelfChecked = self.is_checked()
        except:
            log.fatal(u'Ошибка создания пункта меню <%s>' % self._Name)

    def GetContext(self):
        return None

    def SetImage(self, Image_):
        """
        Функция установки образов пункта меню.
        @param Image_: имя файла образа (BMP).
        """
        try:
            item_kind = self.GetKind()
            # для разделителя нельзя установить картинку
            if item_kind == wx.ITEM_SEPARATOR:
                return

            if Image_ and isinstance(Image_, str):
                eval_space = self.context or ic.utils.util.InitEvalSpace({'MENUITEM': self})
                ret, img = ic.utils.util.ic_eval(Image_, evalSpace=eval_space)
                if not ret:
                    img = Image_
            else:
                img = Image_
            if not img:
                return
            elif isinstance(img, str):
                # Задается имя файла образа
                img = bmpfunc.createBitmap(img)
            if img and (item_kind == wx.ITEM_CHECK or item_kind == wx.ITEM_NORMAL):
                # ВНИМАНИЕ:
                #    Картинки необходимо устанавливать до присоединения
                #    пункта к меню. Иначе она не будет отображаться!
                self.SetBitmap(img)
        except:
            log.fatal(u'Ошибка установки образа для пункта меню <%s>!' % Image_)

    def setBitmap(self, BmpPsp_):
        """
        Функция установки картинки пункта меню.
        @param BmpPsp_: Паспорт картинки.
        """
        try:
            item_kind = self.GetKind()
            # для разделителя нельзя установить картинку
            if item_kind == wx.ITEM_SEPARATOR:
                return

            # Паспорт не определен
            if not BmpPsp_:
                return

            bitmap_obj = ic.getKernel().Create(BmpPsp_)
            img = bitmap_obj.getBitmap()

            if img and (item_kind == wx.ITEM_CHECK or item_kind == wx.ITEM_NORMAL):
                # ВНИМАНИЕ:
                #    Картинки необходимо устанавливать до присоединения
                #    пункта к меню. Иначе она не будет отображаться!
                self.SetBitmap(img)
        except:
            log.fatal(u'Ошибка установки картинки %s для пункта меню %s' % (BmpPsp_, self.GetID()))

    def DoAction(self):
        """
        Выполнить действие,  привязанное к пункту меню.
        """
        self.ExecuteItem()

        kind = self.GetKind()
        # Синхронизировать изображение с инструментом
        if kind == wx.ITEM_CHECK or kind == wx.ITEM_RADIO:
            self.ToggleTool(self.is_checked())

        # Если пункт переключаемый,  то он выключил другой пункт
        if kind == wx.ITEM_RADIO and self._SelfChecked:
            self.ToggleOffRadioPrev()
            self.ToggleOffRadioNext()

    def OnActionItem(self, event):
        """
        Обработчик события выбора пункта меню.
        """
        try:
            if not ic.ic_mode.isRuntimeMode():
                # Если режим дизайнера, то ничего не делать
                return

            # Определить объект, который вызвал событие
            item_id = event.GetId()
            # Если это пункт меню,  тогда выполнить его
            if item_id == self.GetID():
                self.DoAction()
        except:
            log.fatal(u'Ошибка выполнения команды:')
        event.Skip()

    def ToggleOffRadio(self):
        """
        Переключить радио пункт.
        @return: Возвращает True в случае удачного выполнения операции или
            иначе False.
        """
        if self.GetKind() == wx.ITEM_RADIO and self._radio_checked:
            ic.utils.ic_exec.execute_method(self.GetCheckOffMethod(), self)
            self._radio_checked = False
            # Установить собственную метку
            self._SelfChecked = False
            return True
        return False

    def ToggleOffRadioPrev(self):
        """
        Выключить радио пункт.
        """
        if self._RadioPrev is not None:
            if self._RadioPrev.ToggleOffRadio():
                return
            self._RadioPrev.ToggleOffRadioPrev()

    def ToggleOffRadioNext(self):
        """
        Выключить радио пункт.
        """
        if self._RadioNext is not None:
            if self._RadioNext.ToggleOffRadio():
                return
            self._RadioNext.ToggleOffRadioNext()

    def OnHighlight(self, event):
        """
        Обработчик подсветки пункта меню.
        """
        # Если существуют в данной менюшке дочерние открытые меню,
        # тогда закрыть их, т.к. текущая меню получила фокус
        if self._ParentMenu is not None:
            if self._ParentMenu.GetChildOpenedMenu() is not None:
                self._ParentMenu.GetChildOpenedMenu().Close()
            # Закрыть предыдущую открытую дочернюю меню
            parent_parent_menu = self._ParentMenu.GetParentMenu()
            if parent_parent_menu is not None:
                if parent_parent_menu.GetChildOpenedMenu() is not None:
                    if parent_parent_menu.GetChildOpenedMenu() != self._ParentMenu:
                        parent_parent_menu.GetChildOpenedMenu().Close()
                # Установить связи подчинения открытых меню
                parent_parent_menu.SetChildOpenedMenu(self._ParentMenu)
            # Если менюшка прежде не открывалась, тогда выполнить метод на открытие
            if not self._ParentMenu.IsOpened():
                ic.utils.ic_exec.execute_method(self._ParentMenu.GetOpenMethod(), self)
            # Установить признак открытой меню
            self._ParentMenu.SetOpened()

        # Вызов стандартного обработчика события окна для отображения
        # строки помощи в статусной строке
        if self._Window is not None and self._Window.GetStatusBar() is not None:
            self._Window.SetStatusText(self.GetHelp())

    def OnUpdate(self, event):
        """
        Обработчик обновления.
        Необходим для обновления состояния пунктов всплывающего меню.
        """
        if self.is_checked() != self._SelfChecked:
            item_kind = self.GetKind()
            if item_kind == wx.ITEM_CHECK:
                self.Check(self._SelfChecked)
            elif item_kind == wx.ITEM_RADIO and self._SelfChecked:
                self.Check(self._SelfChecked)

    def LinkTool(self, Toolbar_, ToolID_):
        """
        Связать пункт меню с инструментом.
        @param Toolbar_: объект панели инструментов.
        @param ToolID_: идентификатор инструмента.
        """
        if Toolbar_ is None:
            return
        self._Toolbar = Toolbar_
        self._ToolID = ToolID_

    def ToggleTool(self, Toggle_):
        """
        Переключить инструмент,  связанный с пунктом меню.
        @param Toggle_: включить-True/выключить-False.
        """
        if self._Toolbar is not None:
            self._Toolbar.ToggleTool(self._ToolID, Toggle_)

    def ExecuteItem(self):
        """
        Выполнить действие,  привязанное к пункту меню.
        @param item: объект пункта меню.
        """
        try:
            item_kind = self.GetKind()
            ic.utils.ic_exec.execute_method(self.GetActionMethod(), self)

            # Если пункт меню отмечен как переключаемый, то ...
            if item_kind == wx.ITEM_CHECK or item_kind == wx.ITEM_RADIO:
                if self._SelfChecked:
                    result = ic.utils.ic_exec.execute_method(self.GetCheckOffMethod(), self)
                    # Проверка выполнения метода
                    if result is not None:
                        # Если метод запрещает переключение,
                        # то переключить пункт в старое положение
                        if not result:
                            self.Check(True)
                            self._SelfChecked = True
                        else:
                            self._SelfChecked = False
                    else:
                        self._SelfChecked = False
                else:
                    result = ic.utils.ic_exec.execute_method(self.GetCheckOnMethod(), self)
                    # Проверка выполнения метода
                    if result is not None:
                        # Если метод запрещает переключение,
                        # то переключить пункт в старое положение
                        if not result:
                            self.Check(False)
                            self._SelfChecked = False
                        else:
                            self._SelfChecked = True
                    else:
                        self._SelfChecked = True
        except:
            log.fatal(u'Ошибка выполнения обработчика пункта меню <%s>' % self.GetID())

    def is_checked(self):
        if self.IsCheckable():
            return self.IsChecked()
        return False

    # --- Функции-свойства ---
    def GetParentMenu(self):
        return self._ParentMenu

    def GetWindow(self):
        return self._Window

    def GetID(self):
        return self.GetId()

    def GetAlias(self):
        return self._Name

    def GetActionMethod(self):
        return self._Action

    def GetCheckOnMethod(self):
        return self._CheckOn

    def GetCheckOffMethod(self):
        return self._CheckOff

    def GetRadioPrev(self):
        return self._RadioPrev

    def SetRadioPrev(self, RadioPrev_):
        self._RadioPrev = RadioPrev_

    def GetRadioNext(self):
        return self._RadioNext

    def SetRadioNext(self, RadioNext_):
        self._RadioNext = RadioNext_

    def GetToolID(self):
        return self._ToolID

    def GetToolBar(self):
        return self._Toolbar

    def Enable(self, enable=True):
        """
        Включить/выключить пункт меню.
        @param enable: Флаг включения/выключения.
        """
        # Если вообще нельзя использовать этот пункт, то ничего и не делать
        if user_manager.canAuthent(user_manager.ACCESS_USE, self._Name, user_manager.ACC_MENUITEM, False):
            # Если есть связанный инструмент,  тогда отключить и его
            if self._Toolbar and self._ToolID:
                self._Toolbar.EnableTool(self._ToolID, enable)
            # Вызов метода предка
            wx.MenuItem.Enable(self, enable)
