#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Редактор свойств.
"""

import sys
import datetime
import wx
import wx.propgrid

from ic.components import icwidget
from ic.components import icfont
from . import icDefInf

from ic.log import log
from ic.imglib import common as imglib

from ic.utils import resource
from ic.utils import ic_uuid
from ic.utils import coderror
from ic.dlg import ic_dlg
from ic.utils import ic_util

from .ExternalEditors import icedituserproperty
from .ExternalEditors import icpyscriptproperty

__version__ = (0, 0, 2, 3)

IGNORE_PROPERTIES = ('type', 'child', 'win1', 'win2', 'cell_attr', 'label_attr', 'cols')
BASE_PROPERTIES = tuple([attr for attr in icwidget.SPC_IC_SIMPLE.keys() if not attr.startswith('_') and
                         attr not in IGNORE_PROPERTIES])

VISUAL_PROPERTIES = ('flag', 'proportion', 'size', 'position', 'border', 'span')

DEFAULT_ENCODE = 'utf-8'

# Список пользовательских расширенных редакторов свойств
CUSTOM_PROPERTY_EDITORS = (icpyscriptproperty.icPyScriptPropertyEditor, )


class icPropertyEditorManager(wx.propgrid.PropertyGridManager):
    """
    Редактор свойств компонента.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        style = kwargs.get('style', wx.propgrid.PG_DEFAULT_STYLE)
        style = style | wx.propgrid.PG_SPLITTER_AUTO_CENTER | wx.propgrid.PG_TOOLBAR
        kwargs['style'] = style
        wx.propgrid.PropertyGridManager.__init__(self, *args, **kwargs)
        self.clear()

        self.Bind(wx.propgrid.EVT_PG_CHANGED, self.onPropGridChange)
        # self.Bind(wx.propgrid.EVT_PG_SELECTED, self.onPropGridSelected)

        #   Признак включения контроля полей значений свойств.
        self._valid_enable = True

        #   Указатель на ресурс
        self._resource = None
        #   Указатель на спецификацию
        self._spc = None

        #   Объект дерева ресурса
        self.res_tree = None

        #   Указатель на родительский ресурс
        self._parent_res = None

        #   Словарь строк помощи атрибутов спецификации
        self._property_hlp = dict()

        self.register_custom_editor()

    def register_custom_editor(self, *editor_classes):
        """
        Регистрация пользовательских редакторов свойств.
        @param editors_classes: Список классов пользовательских редакторов.
        """
        if not editor_classes:
            editor_classes = CUSTOM_PROPERTY_EDITORS
        #
        # Let's use some simple custom editor
        #
        # NOTE: Editor must be registered *before* adding a property that
        # uses it.
        if not getattr(sys, '_PropGridEditorsRegistered', False):
            for editor_class in editor_classes:
                if editor_class:
                    log.debug(u'Регистрация пользовательского редактора свойства <%s>' % editor_class.__name__)
                    editor_class.setPropertyEditManager(self)
                    self.RegisterEditor(editor_class)
                else:
                    log.warning(u'Не определен пользовательский редактор свойства в редакторе ресурса')
            # ensure we only do it once
            sys._PropGridEditorsRegistered = True

    def clear(self):
        """
        Очистить редактор от свойств.
        """
        self.Clear()
        # А тулбар все равно оставить!!!
        self.AddPage(u'Properties/Свойства', imglib.imgProperties)
        self.AddPage(u'Events/События', imglib.imgEvents)

    def getPropertyType(self, name, res=None):
        """
        Определить тип редактора атрибута по описанию ресурса.
        @param name: Имя атрибута.
        @param res: Редактируемый ресурс.
        @return: Тип редактора атрибута icDefInf.EDT_...
        """
        if res is None:
            res = self._resource

        #   Определяем тип свойства
        property_type = self.findPropertyType(name, res)
        if property_type is None:
            # Не нашли тип свойства в спецификациях
            # надо просигнализировать
            log.warning(u'''Не определен тип редактора атрибута/свойства <%s>.
            Тип установлен как <EDT_PY_SCRIPT>.''' % name)
            property_type = icDefInf.EDT_PY_SCRIPT
        return property_type

    def _get_combin_value_list(self, value, choice_dict):
        """
        Получить строковое представление значения
        @param value: Текущее значение.
        @param choice_dict: Словарь взможных значений.
        @return: Строковое представление значения.
        """
        str_value_lst = []
        for key, code in choice_dict.items():
            if code & value:
                str_value_lst.append(key)
        return str_value_lst

    def createWXProperty(self, name, value, property_type, spc=None):
        """
        Создать свойство wx по типу редактора.
        @param name: Имя свойства/атрибута.
        @param value: Значение свойства/атрибута.
        @param property_type: Тип редактора свойства.
        @param spc: Спецификация компонента.
        @return: wx.Property объект.
        """
        if spc is None:
            spc = self._spc if self._spc else self._resource

        wx_property = None
        if property_type == icDefInf.EDT_TEXTFIELD:
            # Текстовое поле
            if type(value) not in (str, unicode):
                value = str(value)
            wx_property = wx.propgrid.StringProperty(name, value=value)

        elif property_type == icDefInf.EDT_TEXTLIST:
            # Список в синтаксисе Python. Пример: ['1', '2', 'abc']
            value_list = []
            if type(value) in (list, tuple):
                for item in value:
                    if isinstance(item, str):
                        item = unicode(item, DEFAULT_ENCODE)
                    elif not isinstance(item, unicode):
                        item = str(item)
                    value_list.append(item)
            wx_property = wx.propgrid.ArrayStringProperty(name, value=value_list)

        elif property_type == icDefInf.EDT_TEXTDICT:
            # Словарь в синтаксисе Python.
            # value = str(value)
            # Привести словарь к структурному виду
            value = ic_util.StructToTxt(value)
            wx_property = wx.propgrid.LongStringProperty(name, value=value)

        elif property_type == icDefInf.EDT_DICT:
            # Словарь
            # value = str(value)
            # Привести словарь к структурному виду
            value = ic_util.StructToTxt(value)
            wx_property = wx.propgrid.LongStringProperty(name, value=value)

        elif property_type == icDefInf.EDT_IMPORT_NAMES:
            # Словарь импортируемых имен
            # value = str(value)
            # Привести словарь к структурному виду
            value = ic_util.StructToTxt(value)
            wx_property = wx.propgrid.LongStringProperty(name, value=value)

        elif property_type == icDefInf.EDT_NUMBER:
            # Числовое поле
            value = float(value) if value else 0.0
            wx_property = wx.propgrid.FloatProperty(name, value=value)

        elif property_type == icDefInf.EDT_CHOICE:
            # ComboBox
            choice_list = spc.get('__lists__', dict()).get(name, list())
            choice_list = [str(item) for item in choice_list]
            idx = choice_list.index(value) if value in choice_list else 0
            wx_property = wx.propgrid.EnumProperty(name, name, choice_list,
                                                   [i for i in range(len(choice_list))], idx)

        elif property_type == icDefInf.EDT_CHECK_BOX:
            # CheckBox
            if type(value) in (str, unicode):
                value = eval(value)
            value = bool(value)
            wx_property = wx.propgrid.BoolProperty(name, value=value)
            wx_property.SetAttribute('UseCheckbox', True)

        elif property_type == icDefInf.EDT_EXTERNAL:
            # Внешний редактор.
            log.warning(u'Свойство [%s]. Редактор свойства <Внешний редактор> не реализован' % name)

        elif property_type == icDefInf.EDT_COMBINE:
            # Редактор комбинированных свойств.
            choice_list = None
            codes = None
            value_list = []
            if name == 'style':
                if spc and '__styles__' in spc:
                    choice_list = spc['__styles__'].keys() if spc['__styles__'] else []
                    codes = [spc['__styles__'][key] for key in choice_list]
                else:
                    choice_list = []
                    codes = []
                styles = spc['__styles__'] if spc.get('__styles__', None) else {}
                value_list = self._get_combin_value_list(value, styles)
            elif name == 'flag':
                choice_list = icDefInf.ICSizerFlag.keys()
                codes = [icDefInf.ICSizerFlag[key] for key in choice_list]
                value_list = self._get_combin_value_list(value, icDefInf.ICSizerFlag)
            else:
                log.warning(u'Свойство [%s]. Редактор свойства <Редактор комбинированных свойств> не поддерживается' % name)
            if choice_list is not None and codes is not None:
                wx_property = wx.propgrid.MultiChoiceProperty(name, choices=choice_list, value=value_list)

        elif property_type == icDefInf.EDT_COLOR:
            # Редактор цветов wxColour.
            colour = None
            if type(value) in (list, tuple):
                colour = wx.Colour(*value)
            wx_property = wx.propgrid.ColourProperty(name, value=colour)

        elif property_type == icDefInf.EDT_FONT:
            # Редактор шрифтов wxFont.
            value = value if value else dict()
            font = icfont.icFont(value)
            wx_property = wx.propgrid.FontProperty(name, value=font)

        elif property_type == icDefInf.EDT_POINT:
            # Редактор координат точки wxPoint.
            if type(value) not in (str, unicode):
                value = str(value)
            wx_property = wx.propgrid.StringProperty(name, value=value)

        elif property_type == icDefInf.EDT_SIZE:
            # Редактор paзмеров wxSize.
            if type(value) not in (str, unicode):
                value = str(value)
            wx_property = wx.propgrid.StringProperty(name, value=value)

        elif property_type == icDefInf.EDT_PY_SCRIPT:
            # Редактор Python скриптов
            if value is None:
                value = str(value)
            elif isinstance(value, str):
                value = unicode(value, DEFAULT_ENCODE)
            elif isinstance(value, unicode):
                pass
            elif type(value) in (int, float, list, tuple, dict, bool):
                value = str(value)
            elif type(value) in (datetime.datetime,):
                # Если указывается время, то скорее всего это текущее время
                value = u'@datetime.datetime.now()'
            elif type(value) in (datetime.date,):
                # Если указывается день, то скорее всего это сегодняшний
                value = u'@datetime.date.today()'
            else:
                log.warning(u'Свойство [%s]. Редактор свойства <Редактор Python скриптов> для типа <%s> не реализован' % (name, value.__class__.__name__))
                value = u''
            # Захотелось по дополнительной кнопке генерировать текст функции
            # если ее нет и делать прокрутку на нее если она есть в модуле менеджера
            # ресурса. Создал расширенный редактор. Подключается после добавления
            # свойства в PropertyGrid
            wx_property = wx.propgrid.LongStringProperty(name, value=value)

        elif property_type == icDefInf.EDT_ADD_PROPERTY:
            # Редактор дополнительных свойств
            log.warning(u'Свойство [%s]. Редактор свойства <Редактор дополнительных свойств> не реализован' % name)

        elif property_type == icDefInf.EDT_NEW_PROPERTY:
            # Редактор для добавления дополнительного свойства
            log.warning(u'Свойство [%s]. Редактор свойства <Редактор для добавления дополнительного свойства> не реализован' % name)

        elif property_type == icDefInf.EDT_USER_PROPERTY:
            # Редактор пользовательского свойства,
            # определяемого компонентом
            if type(value) not in (str, unicode):
                value = str(value)
            wx_property = icedituserproperty.icEditUserProperty(name, value=value)
            wx_property.setPropertyEditManager(self)

        elif property_type == icDefInf.EDT_RO_TEXTFIELD:
            # Read-Only текстовое поле
            if type(value) not in (str, unicode):
                value = str(value)
            wx_property = wx.propgrid.StringProperty(name, value=value)
            wx_property.Enable(False)

        elif property_type == icDefInf.EDT_IMG:
            # Редактор изображений
            wx_property = wx.propgrid.ImageFileProperty(name)

        elif property_type == icDefInf.EDT_FILE:
            # Редактор выбора файла
            if type(value) not in (str, unicode):
                value = u''
            wx_property = wx.propgrid.FileProperty(name, value=value)

        elif property_type == icDefInf.EDT_DIR:
            # Редактор выбора директории
            if type(value) not in (str, unicode):
                value = u''
            wx_property = wx.propgrid.DirProperty(name, value=value)
        else:
            log.warning(u'Не поддерживаемы йтип свойства <%s>' % property_type)

        # Установить строку помощи для редактора свойства
        if wx_property:
            wx_property.SetHelpString(self._property_hlp.get(name, name))
        return wx_property

    def buildPropertyEditors(self, res=None):
        """
        Заполнение редакторами своиств.
        @param res: Ресурсное описание компонента.
        """
        self.Clear()

        self._resource = res

        if self._resource is None:
            return

        prop_page = self.AddPage(u'Properties/Свойства', imglib.imgProperties)
        # ---------------------------------------
        #   0 - Закладка базовых атрибутов
        prop_page.Append(wx.propgrid.PropertyCategory(u'1 - Basic/Основные'))

        properties = self.getBaseProperties(self._resource)
        for attr in properties:
            edt_type = self.getPropertyType(attr, self._resource)
            wx_property = self.createWXProperty(attr, res.get(attr, None), edt_type)
            if wx_property is not None:
                prop_page.Append(wx_property)

        # ---------------------------------------
        #   1 - Закладка визуальных атрибутов

        prop_page.Append(wx.propgrid.PropertyCategory(u'2 - Visual/Отображение'))

        properties = self.getVisualProperties(self._resource)
        for attr in properties:
            edt_type = self.getPropertyType(attr, self._resource)
            wx_property = self.createWXProperty(attr, res.get(attr, None), edt_type)
            if wx_property is not None:
                prop_page.Append(wx_property)

        # ----------------------------------------
        #   2 - Закладка специальных атрибутов
        prop_page.Append(wx.propgrid.PropertyCategory(u'3 - Special/Специальные'))

        properties = self.getSpecialProperties(self._resource)
        for attr in properties:
            edt_type = self.getPropertyType(attr, self._resource)
            wx_property = self.createWXProperty(attr, res.get(attr, None), edt_type)
            if wx_property is not None:
                prop_page.Append(wx_property)
                if edt_type == icDefInf.EDT_PY_SCRIPT:
                    # Связывать расширенный редактор со свойством можно только после добавления
                    # свойства
                    self.SetPropertyEditor(attr, icpyscriptproperty.icPyScriptPropertyEditor.__name__)

        events_page = self.AddPage(u'Events/События', imglib.imgEvents)

        # ----------------------------------------
        #   3 - Закладка обработчиков событий
        events = self.getEvens(self._resource)
        for attr in events:
            wx_property = self.createWXProperty(attr, res.get(attr, None), icDefInf.EDT_PY_SCRIPT)
            if wx_property is not None:
                events_page.Append(wx_property)
                # Связывать расширенный редактор со свойством можно только после добавления
                # свойства
                self.SetPropertyEditor(attr, icpyscriptproperty.icPyScriptPropertyEditor.__name__)

    def isIgnoreProperty(self, name):
        """
        Игнорировать атрибут?
        @param name: Имя атрибута.
        @return: True/False
        """
        global IGNORE_PROPERTIES
        return name.startswith('_') or name in IGNORE_PROPERTIES

    def isBaseProperty(self, name):
        """
        Является атрибут основным?
        @param name: Имя атрибута.
        @return: True/False
        """
        global BASE_PROPERTIES
        return name in BASE_PROPERTIES

    def isVisualProperty(self, name):
        """
        Является атрибут атрибутом отображения?
        @param name: Имя атрибута.
        @return: True/False
        """
        global VISUAL_PROPERTIES
        return name in VISUAL_PROPERTIES

    def isSpecialProperty(self, name):
        """
        Является атрибут специальным?
        @param name: Имя атрибута.
        @return: True/False
        """
        return not self.isVisualProperty(name) and not self.isBaseProperty(name) \
            and not self.isIgnoreProperty(name) and not self.isEvent(name)

    def isEvent(self, name, res=None):
        """
        Является атрибут событием?
        @param name: Имя атрибута.
        @return: True/False
        """
        if res is None:
            res = self._resource

        if '__events__' in res:
            events_attr = res['__events__'].keys()
        else:
            events_attr = []
        return name in events_attr

    def getBaseProperties(self, res):
        """
        Определить базовые свойства ресурса.
        @param res: Редактируемый ресурс.
        @return: Кортеж имен атрибутов основных свойств.
        """
        attr_list = [attr for attr in res.keys() if self.isBaseProperty(attr)]
        attr_list.sort()

        if 'name' in attr_list:
            attr_list.remove('name')
            # Имя в основных свойствах д.б. первым
            attr_list = ['name'] + attr_list
        return tuple(attr_list)

    def getVisualProperties(self, res):
        """
        Определить свойства отображения ресурса.
        @param res: Редактируемый ресурс.
        @return: Кортеж имен атрибутов свойств отображения.
        """
        attr_list = [attr for attr in res.keys() if self.isVisualProperty(attr)]
        attr_list.sort()
        return tuple(attr_list)

    def getSpecialProperties(self, res):
        """
        Определить специальные свойства ресурса.
        @param res: Редактируемый ресурс.
        @return: Кортеж имен атрибутов специальных свойств.
        """
        attr_list = [attr for attr in res.keys() if self.isSpecialProperty(attr)]
        attr_list.sort()
        return tuple(attr_list)

    def getEvens(self, res):
        """
        Определить события ресурса.
        @param res: Редактируемый ресурс.
        @return: Кортеж имен атрибутов событий.
        """
        if '__events__' in res:
            events_attr = res['__events__'].keys()
            events_attr.sort()
        else:
            events_attr = []
        return tuple(events_attr)

    def getResource(self):
        """
        Возвращает редактируемый ресурс.
        """
        return self._resource

    def getSpc(self):
        """
        Возвращает спецификацию.
        """
        return self._spc

    def getProperty(self, prop):
        """
        Возвращеет значение заданного свойства.
        """
        return self.getResource()[prop]

    def setResource(self, res, spc=None, parent_res=None):
        """
        Устанавливает ресурс на редактирование.
        @type res: C{dictionary}
        @param res: Ресурс, который будет редактироваться.
        @type spc: C{dictionary}
        @param spc: Спецификация ресурса. Используется для определения атрибутов, не
            описанных в спецификации. В редакторе они помечаются цветом.
        @type parent_res: C{dictionary}
        @param parent_res: Родительский ресурс.
        """
        self._spc = spc
        self._property_hlp = self.initPropertyHelp(self._spc)
        self._parent_res = parent_res

        if res is None:
            # Если ресурс пустой, то просто
            # очистить редактор от свойств
            self.clear()
        else:
            self.buildPropertyEditors(res)

    def onPropGridChange(self, event):
        """
        Обработчик изменения значения свойства.
        """
        prop = event.GetProperty()
        if prop:
            #   Если контроль прошел успешно, то сохраняем значение в ресурсном
            #   описании
            name = prop.GetName()
            str_value = prop.GetValueAsString()
            log.info(u'Свойство [%s] изменено на <%s>' % (name, str_value))
            value = self.convertPropertyValue(name, str_value, self._spc)
            if self.validate(name, value) == coderror.IC_CTRL_OK:
                self.setPropertyValue(name, str_value)
                self._refreshResTree(name, value)
            else:
                log.warning(u'Значение <%s> свойства [%s] не прошло валидацию' % (str_value, name))

    def isEnableValidate(self):
        """
        Возвращает признак разрешения контроля поля значений свойств
        ресурсного описания.
        """
        return self._valid_enable

    def enableValidate(self, bEnable):
        """
        Включает/отключает контроль.
        @type bEnable: C{bool}
        @param bEnable: Признак включения контроля значения свойств.
        """
        self._valid_enable = bEnable

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
        if not self.isEnableValidate():
            return coderror.IC_CTRL_OK
        ret = coderror.IC_CTRL_OK
        res = self.getResource()
        tree = self.getResTree()

        #   Проверяем на уникальность имени ресурса
        if name == 'name':
            lst = tree.GetChildNameList(tree.GetSelection())
            if value in lst:
                ic_dlg.icMsgBox(u'Контроль  значения',
                                u'Имя <%s> уже существует. Введите другое.' % value, self)
                ret = coderror.IC_CTRL_FAILED_IGNORE
            else:
                tree.SetItemText(tree.GetSelection(), res['type']+': '+value)
        else:
            #   Контроль в соответствии с типом атрибута
            typ = self.getPropertyType(name, res)
            cls = icDefInf.GetEditorClass(typ)
            ret = cls.Ctrl(value, attr=name, propEdt=self)
            if typ is None:
                ic_dlg.icMsgBox(u'Контроль  значения',
                                u'Не известный тип атрибута: <%s>' % value, self)
                ret = coderror.IC_CTRL_FAILED_IGNORE
            elif ret == coderror.IC_CTRL_FAILED:
                ic_dlg.icMsgBox(u'Контроль  значения',
                                u'Не корректный тип значения: <%s>. Свойство <%s>' % (value, name), self)
                ret = coderror.IC_CTRL_FAILED_IGNORE
            elif ret is None:
                ic_dlg.icMsgBox(u'Контроль  значения',
                                u'Ошибка записи значения: <%s> Свойство <%s>' % (value, name), self)
                ret = coderror.IC_CTRL_FAILED_IGNORE
            elif ret == coderror.IC_CTRL_FAILED_IGNORE:
                pass
        return ret

    def _refreshResTree(self, name, value, res_tree=None):
        """
        Некоторые свойства влияют на отображение дерева ресурсов.
        Обновление дерева ресурсов при установке свойств.
        @type name: C{string}
        @param name: Имя атрибута.
        @type value: C{string}
        @param value: Значение атрибута/свойства.
        """
        if res_tree is None:
            res_tree = self.getResTree()

        if res_tree:
            res_tree.ChangeSelGraphProperty(name, value)
        # -----------------------------------------------------------------------
        #   Раскрашиваем неактивные элементы серым цветом начиная со старого узла
        if name == 'activate':
            #   По состоянию родителя определяем изменять цвет текста
            #   или нет
            if type(value) in (str, unicode):
                value = eval(value)
            value = bool(value)
            res_tree.SetTextColor(res_tree.GetSelection(), value)

    def _prepare_eval(self, expr):
        """
        Подготовка выражения для выполнения eval.
        В случае если в выражении присутствуют символы перевода каретки,
        то при выполнении появляется исключение
        SyntaxError: unexpected character after line continuation character.
        Чтобы этого не происходило удаляются все символы новой строки/перевода каретки
        из исполняемого выражения.
        @param expr: Само выражение. Если не строка, то остается без изменений.
        @return: Подготовленное выражение.
        """
        if type(expr) in (str, unicode):
            expr = expr.strip()
            expr = expr.replace('\\n', '\n').replace('\\r', '\r')
        return expr

    def _convertValue(self, name, str_value, property_type, spc=None):
        """
        Преобразовать значение согласно типу редактора свойства.
        @param name: Имя атрибута.
        @param str_value: Значение в строковом представлении.
        @param property_type: Тип редактора свойства.
        @param spc: Спецификация компонента.
        @return: Сконвертированное значение свойства.
        """
        value = None
        if property_type == icDefInf.EDT_TEXTFIELD:
            # Текстовое поле
            value = str_value

        elif property_type == icDefInf.EDT_TEXTLIST:
            # Список в синтаксисе Python. Пример: ['1', '2', 'abc']
            value = str_value.split(', ')

        elif property_type == icDefInf.EDT_TEXTDICT:
            # Словарь в синтаксисе Python.
            # ВНИМАНИЕ! В случае если в выражении присутствуют символы перевода
            # каретки, то при выполнении появляется исключение
            # SyntaxError: unexpected character after line continuation character.
            # Чтобы этого не происходило удаляются все символы новой строки / перевода
            # каретки из исполняемого выражения.
            str_value = self._prepare_eval(str_value)
            value = eval(str_value)

        elif property_type == icDefInf.EDT_DICT:
            # Словарь
            # ВНИМАНИЕ! В случае если в выражении присутствуют символы перевода
            # каретки, то при выполнении появляется исключение
            # SyntaxError: unexpected character after line continuation character.
            # Чтобы этого не происходило удаляются все символы новой строки / перевода
            # каретки из исполняемого выражения.
            str_value = self._prepare_eval(str_value)
            value = eval(str_value)

        elif property_type == icDefInf.EDT_IMPORT_NAMES:
            # Словарь импортируемых имен
            # ВНИМАНИЕ! В случае если в выражении присутствуют символы перевода
            # каретки, то при выполнении появляется исключение
            # SyntaxError: unexpected character after line continuation character.
            # Чтобы этого не происходило удаляются все символы новой строки / перевода
            # каретки из исполняемого выражения.
            str_value = self._prepare_eval(str_value)
            value = eval(str_value)

        elif property_type == icDefInf.EDT_NUMBER:
            # Числовое поле
            if str_value.strip().isdigit():
                value = eval(str_value.strip())

        elif property_type == icDefInf.EDT_CHOICE:
            # ComboBox
            value = str_value

        elif property_type == icDefInf.EDT_CHECK_BOX:
            # CheckBox
            value = eval(str_value)

        elif property_type == icDefInf.EDT_EXTERNAL:
            # Внешний редактор.
            value = str_value

        elif property_type == icDefInf.EDT_COMBINE:
            # Редактор комбинированных свойств.
            if name == 'style':
                lst_value = [item.strip('"') for item in str_value.split(' ')]
                value = 0
                for v_name in lst_value:
                    value |= spc['__styles__'].get(v_name, 0)
            elif name == 'flag':
                lst_value = [item.strip('"') for item in str_value.split(' ')]
                value = 0
                for v_name in lst_value:
                    value |= icDefInf.ICSizerFlag.get(v_name, 0)
            else:
                log.warning(u'Преобразование типа <Редактор комбинированных свойств> для свойства [%s] не поддерживается' % name)

        elif property_type == icDefInf.EDT_COLOR:
            # Редактор цветов wxColour.
            value = eval(str_value)

        elif property_type == icDefInf.EDT_FONT:
            # Редактор шрифтов wxFont.
            value = dict()
            value_list = str_value.split('; ')
            value['type'] = 'Font'
            value['name'] = 'defaultFont'
            value['size'] = value_list[0]
            value['faceName'] = value_list[1]
            value['style'] = value_list[2]
            value['weight'] = value_list[3]
            value['underline'] = value_list[4]
            value['family'] = value_list[5]

        elif property_type == icDefInf.EDT_POINT:
            # Редактор координат точки wxPoint.
            value = eval(str_value)

        elif property_type == icDefInf.EDT_SIZE:
            # Редактор paзмеров wxSize.
            value = eval(str_value)

        elif property_type == icDefInf.EDT_PY_SCRIPT:
            # Редактор Python скриптов
            value = str_value

        elif property_type == icDefInf.EDT_ADD_PROPERTY:
            # Редактор дополнительных свойств
            log.warning(u'Преобразование типа <Редактор дополнительных свойств> не реализовано')

        elif property_type == icDefInf.EDT_NEW_PROPERTY:
            # Редактор для добавления дополнительного свойства
            log.warning(u'Преобразование типа <Редактор для добавления дополнительного свойства> не реализовано')

        elif property_type == icDefInf.EDT_USER_PROPERTY:
            # Редактор пользовательского свойства,
            # определяемого компонентом
            try:
                value = eval(str_value)
            except:
                # Если ошибка то оставить как есть и сообщить об ошибке
                value = str_value
                log.warning(u'Ошибка конвертации значения свойства <%s>' % name)

        elif property_type == icDefInf.EDT_RO_TEXTFIELD:
            # Read-Only текстовое поле
            value = str_value

        elif property_type == icDefInf.EDT_IMG:
            # Редактор изображений
            value = str_value

        elif property_type == icDefInf.EDT_FILE:
            # Редактор выбора файла
            value = str_value

        elif property_type == icDefInf.EDT_DIR:
            # Редактор выбора директории
            value = str_value

        else:
            log.warning(u'Не определен тип редактора')

        return value

    def findPropertyType(self, name, spc):
        """
        Поиск по спецификациям типа свойства/атрибута.
        @param name: Имя свойства/атрибута.
        @param spc: Спецификация.
        @return: Код типа свойства/атрибута или None, если не найдено
        """
        type_code = None
        # Поиск в текущей спецификации
        attr_types = spc.get('__attr_types__', {})
        for attr_type, attr_list in attr_types.items():
            if name in attr_list:
                type_code = attr_type

        event_types = spc.get('__events__', {})
        if type_code is None and name in event_types:
            # Обработчики событий - это скрипты
            type_code = icDefInf.EDT_PY_SCRIPT

        # Если не нашли, то искать в родительской спецификации
        if type_code is None and '__parent__' in spc:
            type_code = self.findPropertyType(name, spc['__parent__'])
        return type_code

    def convertPropertyValue(self, name, str_value, spc):
        """
        Преобразовать значение свойства к типу указанному в спецификации.
        @param name: Имя свойства/аттрибута.
        @param str_value: Значение в строковом представлении.
        @param spc: Спецификация компонента.
        """
        value = None
        if spc is None:
            spc = self._spc if self._spc else self._resource

        property_type = self.findPropertyType(name, spc)
        if property_type is None:
            # По умолчанию все не определенные атрибуты - скриптовые
            property_type = icDefInf.EDT_PY_SCRIPT
        value = self._convertValue(name, str_value, property_type, spc)
        return value

    def setPropertyValue(self, name, value, bConvert=True):
        """
        Установить значение свойства в ресурсе.
        @param name: Имя свойства/аттрибута.
        @param value: Значение свойства/аттрибута.
        @param bConvert: Произвести конвертацию строкового значения?
        """
        # ВНИМАНИЕ! Значение может задаваться в виде строки.
        # Если задается в виде строки, то возможно необходимо
        # сделать преобразование типа
        if bConvert and type(value) in (str, unicode):
            str_value = value
            value = self.convertPropertyValue(name, str_value, self._spc)
            log.info(u'Set string property [%s] value <%s - \'%s\'>' % (name, value, str_value))
        self._resource[name] = value
        # Синхронизировать ресурс с редактором ресурса
        resource.RefreshResUUID(self._resource, self.getParentResource(), ic_uuid.get_uuid())

    def setReadOnly(self, bEnable=True):
        """
        Установить редактор в режиме чтения.
        @param bEnable: Вкл./Выкл.
        """
        pass

    def isReadOnly(self):
        """
        Возвращает признак редактирования. True - только для чтения,
        False - редактирование.
        """
        return False

    def setResTree(self, res_tree):
        """
        Установить объект дерева ресурса.
        @type res_tree: C{icResTree.icResTree}
        @param res_tree: Указатель на дерево ресурса.
        """
        self.res_tree = res_tree

    def getResTree(self):
        """
        Объект дерева ресурса.
        """
        return self.res_tree

    def getParentResource(self):
        """
        Возвращает родительский ресурс.
        """
        return self._parent_res

    def onPropGridSelected(self, event):
        """
        Обработчик выделения свойства.
        """
        wx_property = event.GetProperty()
        if wx_property:
            property_name = wx_property.GetName()
            popup_win = icwidget.icShortHelpString(parent=self, text=property_name,
                                                   pos=())
        event.Skip()

    def initPropertyHelp(self, spc):
        """
        Инициализировать словарь строк помоши атрибутов спецификации компонента.
        @param spc: Спецификация компонента.
        @return: Словарь строк помощи:
            {
                'имя атрибута': u'Строка помощи', ...
            }
        """
        if spc is None:
            # Проверка на всякий случай
            spc = dict()

        attr_hlp = spc.get('__attr_hlp__', dict())
        if '__parent__' in spc:
            parent_attr_hlp = self.initPropertyHelp(spc['__parent__'])
            parent_attr_hlp.update(attr_hlp)
            attr_hlp = parent_attr_hlp
        return attr_hlp


def test():
    """
    Функция тестирования.
    """
    import copy
    from ic.utils import util
    from ic.components.user.ic_postgres_wrp import ic_class_spc as spc

    app = wx.PySimpleApp()
    frame = wx.Frame(None, -1)

    prop_edit = icPropertyEditorManager(frame)

    res = util.icSpcDefStruct(spc, copy.deepcopy(spc))
    prop_edit.setResource(res)

    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
