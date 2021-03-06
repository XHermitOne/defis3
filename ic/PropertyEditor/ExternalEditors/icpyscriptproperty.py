#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Редактор атрибута/свойства/события компонента в виде скрипта Python.
"""

import os.path
import wx
import wx.propgrid

from ic.log import log


__version__ = (0, 1, 1, 1)


class icPyScriptPropertyEditor(wx.propgrid.PGTextCtrlEditor):
    """
    Редактор атрибута/свойства/события компонента в виде скрипта Python.
    """
    property_edit_manager = None

    @classmethod
    def setPropertyEditManager(cls, manager):
        cls.property_edit_manager = manager

    def CreateControls(self, propGrid, property, pos, sz):
        """
        Создание дополнительных кнопок.

        :param propGrid:
        :param property:
        :param pos:
        :param sz:
        :return:
        """
        try:
            x, y = pos
            w, h = sz

            # Create the 'primary' editor control (textctrl in this case)
            tc = wx.TextCtrl(propGrid.GetPanel(), -1, '',
                             (x, y), (2048, h), wx.BORDER_NONE)

            # Create and populate buttons-subwindow
            buttons = wx.propgrid.PGMultiButton(propGrid, sz)

            # Add two regular buttons
            buttons.AddButton('..')
            buttons.AddButton('>')

            # Finally, move buttons-subwindow to correct position and make sure
            # returned wxPGWindowList contains our custom button list.
            buttons.Finalize(propGrid, pos)

            # We must maintain a reference to any editor objects we created
            # ourselves. Otherwise they might be freed prematurely. Also,
            # we need it in OnEvent() below, because in Python we cannot "cast"
            # result of wxPropertyGrid.GetEditorControlSecondary() into
            # PGMultiButton instance.
            self.buttons = buttons

            return wx.propgrid.PGWindowList(tc, buttons)
        except:
            log.fatal(u'Ошибка создания контролов редактора свойства Python <%s>' % self.__class__.__name__)

    def OnEvent(self, propGrid, prop, ctrl, event):
        """
        Обработка клика на дополнительных кнопках.

        :param propGrid:
        :param prop:
        :param ctrl:
        :param event:
        :return:
        """
        if event.GetEventType() == wx.wxEVT_COMMAND_BUTTON_CLICKED:
            buttons = self.buttons
            eventId = event.GetId()

            if eventId == buttons.GetButtonId(0):
                # Обработка первой кнопки
                # wx.LogDebug('First button pressed')
                return False  # Return false since value did not change
            if eventId == buttons.GetButtonId(1):
                # Обработка второй кнопки
                value = prop.GetValue()
                result = False
                if not value or value in (u'None', u''):
                    # log.debug(u'Редактируемое значение <%s : %s>' % (value, type(value)))
                    # Если значение не определено, то сгенерировать его
                    result = self.create_on_event(prop, prop.GetName())
                else:
                    # Если значение определено, то открыть модуль менеджера ресурса и промотать до функции - обработчика
                    result = self.find_on_event(prop, prop.GetName(), value)

                return result  # Return false since value did not change

        return wx.propgrid.PGTextCtrlEditor.OnEvent(self, propGrid, prop, ctrl, event)

    def create_on_event(self, property, property_name=None):
        """
        Сгенерировать обработчик в модуле менеджера ресурса.

        :param property: Объект редактируемого свойства.
        :param property_name: Наименование свойства.
        :return: True/False.
        """
        if property_name is None:
            property_name = property.GetName()

        if self.property_edit_manager is None:
            log.warning(u'Не определен менеджер редактора свойств')
            return False

        if self.property_edit_manager.res_tree is None:
            log.warning(u'Не определен объект дерева ресурса')
            return False

        # Основные управляющие объекты
        tree = self.property_edit_manager.res_tree
        res_editor = tree.GetResEditor()
        # Определяем имя выбранного объекта
        obj_item = res_editor.tree.lastSel
        obj_res = res_editor.tree.GetItemData(obj_item)
        obj_name = obj_res.get('name', u'')

        ide = res_editor.GetIDEInterface()

        func_name = property_name if property_name.startswith('on') else 'on_%s_%s' % (obj_name, property_name)

        py_filename = res_editor.file.replace('\\', '/')
        path, ext = os.path.os.path.splitext(py_filename)
        if tree:
            if ext != '.py':
                py_filename = res_editor.get_res_module_name(py_filename)

            # log.debug(u'Открыть файл <%s> функция <%s>' % (py_filename, func_name))
            # По расширению файла ресурса определяем способ вызова:
            # '.py' - вызываем метод интерфейса, в противном случае
            # функцию модуля ресусра
            if ext == '.py':
                ptFunc = '@GetWrapper(self).%s(event)' % func_name
            else:
                ptFunc = '@GetManager(self).%s(event)' % func_name

            property.SetValue(ptFunc)

            #   Если функции нет, то добавляем заготовку в
            #   текст модуля
            ide.insertEvtFuncToInterface(py_filename, func_name)

        return True

    def _find_and_goto_func(self, tree, ide, res_editor, property_value, signature='GetManager'):
        """
        Найти и перейти к функции...

        :return: True - Перешли, False - функция не найдена.
        """
        # signature = '%s(self).' % signature
        len_signature = len(signature)

        n1 = property_value.find(signature)
        n2 = property_value.find('(', n1 + len_signature)
        if 0 <= n1 < n2:
            func_name = property_value[n1 + len_signature: n2]
            path_filename, ext = os.path.splitext(res_editor.file)
            py_filename = res_editor.file if ext == '.py' else path_filename+'_'+ext[1:]+'.py'
            # log.debug(u'Поиск функции <%s> в модуле <%s>' % (func_name, py_filename))
            if tree and ide:
                ide.goToFunc(func_name, filename=py_filename)
                return True
            else:
                log.warning(u'Не определена IDE')
        return False

    def find_on_event(self, property, property_name=None, property_value=None):
        """
        Открыть модуль менеджера ресурса и промотать до функции - обработчика.

        :param property: Объект редактируемого свойства.
        :param property_name: Наименование свойства.
        :param property_value: Значение свойства.
        :return: True/False.
        """
        if self.property_edit_manager is None:
            log.warning(u'Не определен менеджер редактора свойств')
            return False

        if self.property_edit_manager.res_tree is None:
            log.warning(u'Не определен объект дерева ресурса')
            return False

        # Основные управляющие объекты
        tree = self.property_edit_manager.res_tree
        res_editor = tree.GetResEditor()
        ide = res_editor.GetIDEInterface()

        # Пытаемся найти обработчик в коде
        result = self._find_and_goto_func(tree, ide, res_editor, property_value, signature='@GetManager(self).')
        if not result:
            result = self._find_and_goto_func(tree, ide, res_editor, property_value, signature='GetWrapper().')

        return result
