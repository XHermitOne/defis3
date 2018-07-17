#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль описания класса AUI панелей. Технология AUI.
"""

# --- Подключение библиотек ---
import wx
from wx.lib.agw import aui

from ic.kernel import io_prnt
from ic.utils import ic_file

from ic.components import icwidget
from ic.components import icResourceParser

# --- Основные константы ---
AUI_PANE_DIRECTIONS = ['Top', 'Right', 'Bottom', 'Left', 'Center']

# --- Спецификации ---
SPC_IC_AUIPANE = {'title': None,         # Заголовок
                  'control_res': None,   # Имя ресурса прикрепленного контрола
                  'control_name': None,  # Имя прикрепленного контрола
                  # Размеры
                  'min_size': (100, 100),   # Минимальный размер
                  'best_size': (150, 150),  # Размер панели
                  'max_size': (500, 500),   # Максимальный размер
                  # Кнопки управления
                  'maximize_button': True,  # Кнопка распахивания
                  'close_button': True,     # Кнопка закрытия
                  # Указание местаположения
                  'direction': 'Left',  # Направление
                  'layer': 0,           # Уравень/Слой
                  'pos': 0,             # Позиция
                  'row': 0,             # Строка
                  'visible': True,      # Видимость при старте
    
                  '__parent__': icwidget.SPC_IC_SIMPLE,
                  '__attr_hlp__': {'title': u'Заголовок',
                                   'control_res': u'Имя ресурса прикрепленного контрола',
                                   'control_name': u'Имя прикрепленного контрола',
                                   'min_size': u'Минимальный размер',
                                   'best_size': u'Размер панели',
                                   'max_size': u'Максимальный размер',
                                   'maximize_button': u'Кнопка распахивания',
                                   'close_button': u'Кнопка закрытия',
                                   'direction': u'Направление',
                                   'layer': u'Уравень/Слой',
                                   'pos': u'Позиция',
                                   'row': u'Строка',
                                   'visible': u'Видимость при старте',
                                   },
                  }


__version__ = (0, 0, 0, 2)


class icAUIPanePrototype:
    """
    AUI панель. Технология AUI.
    """

    def __init__(self, Parent_, Resource_):
        """
        Конструктор.
        @param: Parent_: Родительское окно.
        @param Resource_: Ресурс объекта.
        """
        self._Parent = Parent_
        
        self.name = Resource_['name']
        self.title = Resource_['title']
        # Кнопки управления
        self.maximize_button = Resource_['maximize_button']
        self.close_button = Resource_['close_button']
        # Местоположение
        self.direction = Resource_['direction']
        self.layer = Resource_['layer']
        self.row = Resource_['row']
        self.pos = Resource_['pos']
        self.min_size = Resource_['min_size']
        self.best_size = Resource_['best_size']
        self.max_size = Resource_['max_size']
        self.visible = Resource_['visible']
        # Контрол
        self.control_name = Resource_.get('control_name', None)
        self.control_subsys = None
        self.control_res = Resource_['control_res']
        # Теперь control_res должен быть паспорт
        if type(self.control_res) == tuple:
            self.control_name = self.control_res[0][1]
            self.control_subsys = self.control_res[0][4]
            self.control_res = self.control_res[0][3]
        
        # Прикрепленный объект
        self.control = self.createControl(self.control_name,
                                          self.control_res, self.control_subsys)
            
        #   Флаг, указывающий, что необходимо сохранять изменяющиеся
        #   параметры окна (позицию и размеры).
        self.saveChangeProperty = True

        #   Читаем из файла настроек пользователя
        self._loadUserProperty()

    def _loadUserProperty(self):
        """
        Загрузка атрибутов, которые может изменять пользователь.
        """
        _direction = self.LoadUserProperty('direction')
        if _direction is not None:
            self.direction = _direction
            
        _layer = self.LoadUserProperty('layer')
        if _layer is not None:
            self.layer = _layer
        
        _row = self.LoadUserProperty('row')
        if _row is not None:
            self.row = _row
        
        _pos = self.LoadUserProperty('pos')
        if _pos is not None:
            self.pos = _pos

        _best_size = self.LoadUserProperty('best_size')
        if _best_size is not None:
            self.best_size = _best_size
        
        _visible = self.LoadUserProperty('visible')
        if _visible is not None:
            self.visible = _visible
            
    def _saveUserProperty(self):
        """
        Сохранение атрибутов, которые может изменять пользователь.
        """
        aui_manager = self._Parent.getAUIManager()
        pane_info = aui_manager.GetPane(self.name)
        self.SaveUserProperty('direction', AUI_PANE_DIRECTIONS[pane_info.dock_direction-1])
        self.SaveUserProperty('layer', pane_info.dock_layer)
        self.SaveUserProperty('row', pane_info.dock_row)
        self.SaveUserProperty('pos', pane_info.dock_pos)
        self.SaveUserProperty('best_size', tuple(self.getControl().GetClientSize()))
        self.SaveUserProperty('visible', pane_info.IsShown())

    def ObjDestroy(self):
        """
        Вызывается при удалении объекта.
        """
        self._saveUserProperty()
        
    def createControl(self, Name_, ResFileName_, subsys=None):
        """
        Создание прикрепленного объекта.
        @param Name_: Имя объекта.
        @param ResFileName_: Имя файла ресурса объекта.
        """
        control = None
        try:
            res_name, res_ext = ic_file.SplitExt(ResFileName_)
            control = icResourceParser.icCreateObject(res_name,
                                                      res_ext[1:],
                                                      subsys=subsys,
                                                      parent=self._Parent)
            return control
        except:
            io_prnt.outErr(u'Ошибка создания прикрепленного к AUI панели объекта.')
            return None
        
    def getControl(self):
        """
        Прикрепленный объект.
        """
        return self.control

    def openControl(self, Name_, ResFileName_):
        """
        Отобразить/показать контрол и при необходимости создать.
        @param Name_: Имя объекта.
        @param ResFileName_: Имя файла ресурса объекта.
        """
        if self.control and self.control.name != Name_:
            self.control = self.createControl(Name_, ResFileName_)
            self.control_name = Name_
            self.control_res = ResFileName_
        aui_manager = self._Parent.getAUIManager()
        aui_manager.addPane(self)
        aui_manager.Update()

    def showControl(self, Control_):
        """
        Отобразить/показать контрол.
        """
        if Control_:
            self.control = Control_
        aui_manager = self._Parent.getAUIManager()
        aui_manager.addPane(self)
        aui_manager.Update()
