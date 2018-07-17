#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Основные константы/перечисления редактора ресурсов.
"""

import wx
from ic.utils import coderror
from .ExternalEditors import baseeditor
from .ExternalEditors import basefuncs

from ic.log import log

_ = wx.GetTranslation

# Список не графических компонентов
icNoWidgetObject = ['SimpleDataset', 'FileDataset', 'ODBCDataset',
                    'GridCell', 'Frame', 'Dialog', 'Group', 'DataLink',
                    'cell_attr', 'label_attr', 'Import']

# Список объектов, не наследованных от wx.Window
icNoWinObject = ['Group', 'DataLink', 'cell_attr',
                 'label_attr', 'Import', 'SizerSpace', 'BoxSizer',
                 'StaticBoxSizer', 'GridSizer', 'FlexGridSizer', 'GridBagSizer',
                 'ToolBarTool', 'Separator']
# Список объектов, которые могут иметь дополнительные свойства
icObjWithAddProperty = ['DataLink']

# Список объектов, которые не определяются спецификацией, а в описании компонента
# обычно присутствуют
icUnSpecAttr = ['flag', 'proportion', 'border',  'alias',  'span', 'activate',
                'show', 'init_expr']

#   Список атрибутов, которые исплоьзуются в качестве контейнеров
icContainerAttr = ['child', 'win1', 'win2', 'cols']

# Идентификаторы системных редакторов
# Пока оставлено для совместимости с предыдущим редактором свойств

# Текстовое поле
EDT_TEXTFIELD = 0
# Список в синтаксисе Python. Пример: ['1', 2, 'abc']
EDT_TEXTLIST = 20
# Словарь в синтаксисе Python.
EDT_TEXTDICT = 30
# Словарь
EDT_DICT = 35
# Словарь импортируемых имен
EDT_IMPORT_NAMES = 37
# Числовое поле
EDT_NUMBER = 40
# ComboBox
EDT_CHOICE = 1
# CheckBox
EDT_CHECK_BOX = 2
# Внешний редактор.
EDT_EXTERNAL = 4
# Редактор комбинированных свойств.
EDT_COMBINE = 7
# Редактор цветов wxColour.
EDT_COLOR = 8
# Редактор шрифтов wxFont.
EDT_FONT = 9
# Редактор координат точки wxPoint.
EDT_POINT = 10
# Редактор paзмеров wxSize.
EDT_SIZE = 11
# Редактор Python скриптов
EDT_PY_SCRIPT = 12
# Редактор дополнительных свойств
EDT_ADD_PROPERTY = 14
# Редактор для добавления дополнительного свойства
EDT_NEW_PROPERTY = 15
# Редактор пользовательского свойства, определяемого компонентом
EDT_USER_PROPERTY = 16
# Read-Only текстовое поле
EDT_RO_TEXTFIELD = 17
# Редактор изображений
EDT_IMG = baseeditor.icImageEdt.ID_Editor
# Редактор Выбора файла
EDT_FILE = baseeditor.icFileEdt.ID_Editor
# Редактор Выбора директории
EDT_DIR = baseeditor.icDirEdt.ID_Editor

# Словарь зарегестрированных редакторов, ключ - идентификатор редактора,
# значение класс, реализующий функции редактора
ic_reg_edt_class = {}


def RegEditorClasses(cls_lst):
    """
    Регистрирует список классов.
    """
    global ic_reg_edt_class
    for cls in cls_lst:
        ic_reg_edt_class[cls.ID_Editor] = cls


def GetEditorClass(id):
    """
    Возвращает по идентификатору внешнего редактора класс.
    @type id: C{int}
    @param id: Идентификатор внешнего редактора.
    """
    global ic_reg_edt_class
    if id in ic_reg_edt_class:
        return ic_reg_edt_class[id]
    else:
        log.warning(u'Не определен класс внешнего редактора <%s>' % id)
    return None
    
##########################################
#   Регестрируем внешние редакторы
##########################################
RegEditorClasses([baseeditor.icCheckBoxEdt,
                  baseeditor.icColorEdt,
                  baseeditor.icChoiceEdt,
                  baseeditor.icCombineEdt,
                  baseeditor.icDictEdt,
                  baseeditor.icFontEdt,
                  baseeditor.icNumberEdt,
                  baseeditor.icPointEdt,
                  baseeditor.icPyScriptEdt,
                  baseeditor.icSizeEdt,
                  baseeditor.icTextDictEdt,
                  baseeditor.icTextEdt,
                  baseeditor.icROTextEdt,
                  baseeditor.icTextListEdt,
                  baseeditor.icUserEdt,
                  # baseeditor.icImageEdt,
                  baseeditor.icFileEdt,
                  baseeditor.icDirEdt,
                  ])
    
id_dict = {'EDT_TEXTFIELD': EDT_TEXTFIELD,
           'EDT_TEXTDICT': EDT_TEXTDICT,
           'EDT_RO_TEXTFIELD': EDT_RO_TEXTFIELD,
           'EDT_DICT': EDT_DICT,
           'EDT_IMPORT_NAMES': EDT_IMPORT_NAMES,
           'EDT_NUMBER': EDT_NUMBER,
           'EDT_CHOICE': EDT_CHOICE,
           'EDT_CHECK_BOX': EDT_CHECK_BOX,
           'EDT_EXTERNAL': EDT_EXTERNAL,
           'EDT_COMBINE': EDT_COMBINE,
           'EDT_COLOR': EDT_COLOR,
           'EDT_FONT': EDT_FONT,
           'EDT_POINT': EDT_POINT,
           'EDT_SIZE': EDT_SIZE,
           'EDT_PY_SCRIPT': EDT_PY_SCRIPT,
           'EDT_ADD_PROPERTY': EDT_ADD_PROPERTY,
           'EDT_NEW_PROPERTY': EDT_NEW_PROPERTY,
           'EDT_USER_PROPERTY': EDT_USER_PROPERTY,
           'EDT_FILE': EDT_FILE,
           'EDT_DIR': EDT_DIR,
           }

# Словарь описания флагов (flag) сайзеров
ICSizerFlag = {'TOP': wx.TOP,
               'BOTTOM': wx.BOTTOM,
               'LEFT': wx.LEFT,
               'RIGHT': wx.RIGHT,
               'ALL': wx.ALL,
               'GROW': wx.GROW,
               'EXPAND': wx.EXPAND,
               'SHAPED': wx.SHAPED,
               'ALIGN_CENTER': wx.ALIGN_CENTER,
               'ALIGN_LEFT': wx.ALIGN_LEFT,
               'ALIGN_TOP': wx.ALIGN_TOP,
               'ALIGN_RIGHT': wx.ALIGN_RIGHT,
               'ALIGN_BOTTOM': wx.ALIGN_BOTTOM,
               'ALIGN_CENTER_VERTICAL': wx.ALIGN_CENTER_VERTICAL,
               'ALIGN_CENTER_HORIZONTAL': wx.ALIGN_CENTER_HORIZONTAL}


def strToVal(typ, text):
    """
    Функция преобразует строку в значение в зависимости от типа.
    @type typ: C{int}
    @param typ: Тип значения, к котророму необходимо преобразовать.
    @type text: C{string}
    @param text: Значение в строковом представлении.
    """
    old_typ = typ
    if type(typ) in (str, unicode) and (typ in id_dict):
        typ = id_dict[typ]
        
    if type(text) not in (str, unicode):
        return None
        
    value = text
    # Текст
    if typ in (EDT_TEXTFIELD, EDT_PY_SCRIPT, EDT_CHOICE):
        value = text
        
    # Список в синтаксисе Python. Пример: ['1', 2, 'abc']
    elif typ == EDT_TEXTLIST:
        try:
            value = eval(text)
        except:
            value = []
    # Словарь
    elif typ in (EDT_TEXTDICT, EDT_DICT, EDT_FONT, EDT_COMBINE):
        try:
            value = eval(text)
        except:
            value = {}
    # Числовое поле
    elif typ in (EDT_NUMBER, EDT_CHECK_BOX):
        try:
            value = eval(text)
        except:
            value = 0
    # Редактор цветов wxColour.
    elif typ == EDT_COLOR:
        try:
            value = eval(text)
        except:
            value = (0, 0, 0)

    # Редактор координат точки wxPoint.
    elif typ == EDT_POINT:
        try:
            value = eval(text)
        except:
            value = (-1,-1)

    # Редактор paзмеров wxSize.
    elif typ == EDT_SIZE:
        try:
            value = eval(text)
        except:
            value = (-1, -1)

    else:
        # Не определили тип редактора
        log.warning(u'Не определен тип редактора <%s>. Значение <%s>' % (typ, value))
            
    return value


def ctrlVal(typ, text):
    """
    Функция проверяет соответствие значения определенному типу.
    @type typ: C{int}
    @param typ: Тип значения, к котророму необходимо преобразовать.
    @type text: C{string}
    @param text: Значение в строковом представлении.
    @return: Код контроля. None означает синтаксическую ошибку.
    """
    if typ in (EDT_TEXTFIELD, EDT_PY_SCRIPT, EDT_CHOICE):
        value = text
    else:
        try:
            value = eval(text)
        except:
            log.error('eval(text): text=<%s>' % text)
            return None
        
    ret = coderror.IC_CTRL_FAILED
    # Текст
    if typ in (EDT_TEXTFIELD, EDT_PY_SCRIPT, EDT_CHOICE) and type(value) in (str, unicode):
        ret = coderror.IC_CTRL_OK
    # Список в синтаксисе Python. Пример: ['1', 2, 'abc']
    elif typ == EDT_TEXTLIST and isinstance(value, list):
        ret = coderror.IC_CTRL_OK
    # Словарь
    elif typ in (EDT_TEXTDICT, EDT_DICT, EDT_FONT) and isinstance(value, dict):
        ret = coderror.IC_CTRL_OK
    # Числовое поле
    elif typ in (EDT_NUMBER, EDT_CHECK_BOX, EDT_COMBINE) and type(value) in (int, float, bool):
        ret = coderror.IC_CTRL_OK
    # Редактор цветов wxColour.
    elif typ == EDT_COLOR and value is None:
        ret = coderror.IC_CTRL_OK
    elif typ == EDT_COLOR and ((type(value) == wx.Colour) or
                               (isinstance(value, tuple) and len(value) == 3)):
        ret = coderror.IC_CTRL_OK
    # Редактор координат точки wx.Point.
    elif typ == EDT_POINT and type(value) in (tuple, type(wx.Point(0, 0))) and len(value) == 2:
        ret = coderror.IC_CTRL_OK
    # Редактор размеров окон wx.Size.
    elif typ == EDT_SIZE and type(value) in (tuple, type(wx.Size(0, 0))) and len(value) == 2:
        ret = coderror.IC_CTRL_OK
    
    return ret
        
# -------------------------------------------------------------------------------
#   Группы объектов
#   Окна
_icWindowType = 0
#   Сайзеры
_icSizersType = 1
#   Controls
_icControlsType = 2
#   Составные компоненты
_icComboType = 3
#   Объекты данных
_icDatasetType = 4
#   Сервесные компоненты
_icServiceType = 5
#   Пользовательские компоненты
_icUserType = 6
#   Компоненты меню
_icMenuType = 7
_icMaxTypeId = _icMenuType

GroupsInfo = {_icWindowType: _('Windows'),
              _icSizersType: _('Sizers'),
              _icControlsType: _('Custom'),
              _icMenuType: _('Menu'),
              _icComboType: _('Combo'),
              _icServiceType: _('Service'),
              _icDatasetType: _('Data'),
              _icUserType: _('User')}


def ClearUserGroup():
    """
    Удаляем пользовательские группы из словаря групп.
    """
    global GroupsInfo
    lst = GroupsInfo.keys()
    for id in lst:
        if id > _icMaxTypeId:
            GroupsInfo.pop(id)


def RegComponentGroup(name):
    """
    Функция регистрации новой группы компонентов.
    @type name: C{string}
    @param name: Имя группы.
    @rtype: C{int}
    @return: Возвращает идентификатор новой ргуппы.
    """
    global GroupsInfo
    if name not in GroupsInfo.values():
        id = max(GroupsInfo.keys())+1
        GroupsInfo[id] = name
        return id
    else:
        log.warning('Group <%s> already register in GroupsInfo dict.' % name)


def GetGroupIdByName(name):
    """ Возвращает идентификатор группы по имени."""
    return filter(lambda x: x[1] == name, GroupsInfo.items())[0][0]

ObjectGroupsMenuStruct = []

# -------------------------------------------------------------------------------
#   Цвета текста активных и неактивных объектов
ACTIVATE_COLOR = (0, 0, 0)
DEACTIVATE_COLOR = (150, 150, 150)

#   Функции для арботы со стилями


def getStyleDict(style, allstyles):
    """
    Возвращает стиль компонента в виде словаря.
    @type style: C{long}
    @param style: Стиль компонента.
    @type allstyles: C{dictionary}
    @param allstyles: Словарь всех стилей компонента.
    @rtype: C{dictionary}
    @return: Стиль компонента.
        - B{Пример}:C{'wx.DEFAULT':1, 'wx.APP':0, ...}
    """
    return basefuncs.getStyleDict(style, allstyles)
