#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Мастер создания пользовательского компонента.
"""

import wx
import wx.stc

from ic.log import log

try:
    from . import create_component_wizard_proto
except ImportError:
    import create_component_wizard_proto

from ic.engine import glob_functions
from ic.engine import form_manager
from ic.PropertyEditor import icDefInf
from ic.utils import strfunc

__version__ = (0, 1, 1, 1)

DEFAULT_WIZARD_WIDTH = 800
DEFAULT_WIZARD_HEIGHT = 600

DOC_FILENAME_FMT = '%s/doc/_build/html/%s.usercomponents.%s.html'


class icEditComponentAttrDlg(create_component_wizard_proto.icEditAttrDialogProto):
    """
    Диалоговое окно редактирования атрибута компонента.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.

        :param args:
        :param kwargs:
        """
        create_component_wizard_proto.icEditAttrDialogProto.__init__(self, *args, **kwargs)

        self.edit_attr_value = dict()

    def init(self, name=u'', editor=u'', default=u''):
        """
        Инициализировать окно.

        :param name: Наименование атрибута.
        :param editor: Редактор атрибута.
        :param default: Значение по умолчанию.
        :return: True/False.
        """
        self.name_textCtrl.SetValue(name)
        self.default_textCtrl.SetValue(default)

        # Установить элементы выбора списка редакторов
        choices = [u''] + icDefInf.PROPERTY_EDITOR_NAMES
        self.editor_choice.SetItems(choices)
        n = choices.index(editor) if editor in choices else 0
        self.editor_choice.SetSelection(n)
        return True

    def onCancelButtonClick(self, event):
        """
        Обработчик кнопки <Отмена>.
        """
        self.edit_attr_value = dict()
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        Обработчик кнопки <ОК>.
        """
        self.edit_attr_value = dict(name=self.name_textCtrl.GetValue(),
                                    editor=self.editor_choice.GetStringSelection(),
                                    default=self.default_textCtrl.GetValue())
        self.EndModal(wx.ID_CANCEL)
        event.Skip()


def edit_component_attr_dlg(parent=None, name=u'attr_name', editor=u'', default=u''):
    """
    Функция вызова окна редактирования атрибута компонента.

    :param parent: Родительское окно.
        Если не определено, то берется главное окно.
    :param name: Наименование атрибута.
    :param editor: Редактор атрибута.
    :param default: Значение по умолчанию.
    :return: Словарь отредактированных данных или None если нажата <Отмена>.
    """
    try:
        if parent is None:
            parent = glob_functions.getMainWin()

        dlg = icEditComponentAttrDlg(parent=parent)
        dlg.init(name=name, editor=editor, default=default)
        dlg.ShowModal()
        result = dlg.edit_attr_value if dlg.edit_attr_value else None
        dlg.Destroy()
        return result
    except:
        log.fatal(u'Ошибка вызова окна редактирования атрибута компонента <%s>' % name)
    return None


class icEditComponentEventDlg(create_component_wizard_proto.icEditEventDialogProto):
    """
    Диалоговое окно редактирования событий компонента.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.

        :param args:
        :param kwargs:
        """
        create_component_wizard_proto.icEditEventDialogProto.__init__(self, *args, **kwargs)

        self.edit_event_value = dict()

    def init(self, name=u'', event=u'', func_name=u''):
        """
        Инициализировать окно.

        :param name: Наименование атрибута.
        :param event: Событие.
        :param func_name: Имя функции-обработчика.
        :return: True/False.
        """
        self.name_textCtrl.SetValue(name)
        self.func_name_textCtrl.SetValue(func_name)

        self.event_checkBox.SetValue(bool(event))
        # Установить элементы выбора списка редакторов
        evt_names = [evt_name for evt_name in dir(wx) if evt_name.startswith('EVT_')]
        evt_names.sort()
        choices = [u''] + evt_names
        self.event_choice.SetItems(choices)
        n = choices.index(event) if event in choices else 0
        self.event_choice.SetSelection(n)
        return True

    def onCancelButtonClick(self, event):
        """
        Обработчик кнопки <Отмена>.
        """
        self.edit_event_value = dict()
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        Обработчик кнопки <ОК>.
        """
        self.edit_event_value = dict(name=self.name_textCtrl.GetValue(),
                                     event=self.event_choice.GetStringSelection() if self.event_checkBox.GetValue() else None,
                                     func_name=self.func_name_textCtrl.GetValue())
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onEventCheckBox(self, event):
        """
        Обработчик включения/выключения события.
        """
        check = event.IsChecked()

        if not check:
            self.event_choice.SetSelection(0)
        self.event_choice.Enable(check)

        event.Skip()

    def onEventNameText(self, event):
        """
        Обработчик изменения текста наименования события.
        """
        new_name = event.GetString().lower()
        event_name = self.event_choice.GetStringSelection()
        event_name = event_name.replace('EVT_', '').lower() if event_name else 'Do'
        func_name = 'on%s%s' % (strfunc.lower_symbols2_upper(new_name),
                                strfunc.lower_symbols2_upper(event_name))
        self.func_name_textCtrl.SetValue(func_name)
        event.Skip()


def edit_component_event_dlg(parent=None, name=u'event_name', event=u'', func_name=u''):
    """
    Функция вызова окна редактирования атрибута компонента.

    :param parent: Родительское окно.
        Если не определено, то берется главное окно.
    :param name: Наименование атрибута.
    :param event: Событие.
    :param func_name: Имя функции-обработчика.
    :return: Словарь отредактированных данных или None если нажата <Отмена>.
    """
    try:
        if parent is None:
            parent = glob_functions.getMainWin()

        dlg = icEditComponentEventDlg(parent=parent)
        dlg.init(name=name, event=event, func_name=func_name)
        dlg.ShowModal()
        result = dlg.edit_event_value if dlg.edit_event_value else None
        dlg.Destroy()
        return result
    except:
        log.fatal(u'Ошибка вызова окна редактирования события компонента <%s>' % name)
    return None


class icCreateComponentWizard(create_component_wizard_proto.icCreateComponentWizardProto,
                              form_manager.icFormManager):
    """
    Мастер создания пользовательского компонента.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.

        :param args:
        :param kwargs:
        """
        create_component_wizard_proto.icCreateComponentWizardProto.__init__(self, *args, **kwargs)

        # Редактор кода
        self.source_scintilla = None

        self.init()

    def init(self):
        """
        Инициализация контролов страниц визарда.

        :return:
        """
        # Установить имена редакторов свойств
        self.name_propertyGridItem.SetName('name')
        self.module_propertyGridItem.SetName('module')
        self.description_propertyGridItem.SetName('description')
        self.author_propertyGridItem.SetName('author')
        self.copyright_propertyGridItem.SetName('copyright')
        self.parentmodule_propertyGridItem.SetName('parent_module')
        self.parentclass_propertyGridItem.SetName('parent_class')
        self.icon_propertyGridItem.SetName('icon')
        self.docfile_propertyGridItem.SetName('doc_filename')

        # Колонки списка атрибутов компонента
        self.setColumns_list_ctrl(ctrl=self.attr_listCtrl,
                                  cols=(dict(label=u'Наименование', width=200),
                                        dict(label=u'Редактор', width=150),
                                        dict(label=u'По умолчанию', width=200)))

        # Колонки списка событий компонента
        self.setColumns_list_ctrl(ctrl=self.event_listCtrl,
                                  cols=(dict(label=u'Наименование', width=200),
                                        dict(label=u'Событие', width=150),
                                        dict(label=u'Обработчик', width=200)))

        # Создать редактор кода
        self.source_scintilla = wx.stc.StyledTextCtrl(parent=self.gen_wizPage)
        sizer = self.gen_wizPage.GetSizer()
        sizer.Add(self.source_scintilla, 1, wx.EXPAND | wx.ALL, 5)

    def onAttrPropertyGridChanged(self, event):
        """
        Обработчик изменения основного атрибута компонента в редакторе.
        """
        prop = event.GetProperty()
        if prop:
            name = prop.GetName()
            str_value = prop.GetValueAsString()
            log.debug(u'Изменение свойства <%s : %s>' % (name, str_value))

            if name == 'name':
                module_name = str_value.lower()
                module = '%s.py' % module_name
                self.module_propertyGridItem.SetValue(module)
                prj_name = glob_functions.getPrjName()
                doc_filename = DOC_FILENAME_FMT % (prj_name, prj_name, module_name)
                self.docfile_propertyGridItem.SetValue(doc_filename)
            elif name == 'author':
                copyright_text = '(C) %s Copyright' % str_value
                self.copyright_propertyGridItem.SetValue(copyright_text)

        # event.Skip()

    def onAddAttrToolClicked(self, event):
        """
        Обработчик добавления атрибута.
        """
        attr = edit_component_attr_dlg(parent=self)
        if attr is not None:
            row = (attr.get('name', u''), attr.get('editor', u''), attr.get('default', u''))
            self.appendRow_list_ctrl(ctrl=self.attr_listCtrl, row=row)
        event.Skip()

    def onDelAttrToolClicked(self, event):
        """
        Обработчик удаления атрибута.
        """
        self.removeRow_list_ctrl(ctrl=self.attr_listCtrl)
        event.Skip()

    def onEditAttrToolClicked(self, event):
        """
        Обработчик редактирования атрибута.
        """
        row = self.getRow_list_ctrl(ctrl=self.attr_listCtrl)
        if row:
            name, editor, default = row
            attr = edit_component_attr_dlg(parent=self, name=name, editor=editor, default=default)
            if attr is not None:
                row = (attr.get('name', u''), attr.get('editor', u''), attr.get('default', u''))
                self.setRow_list_ctrl(ctrl=self.attr_listCtrl,
                                      row_idx=self.getItemSelectedIdx(self.attr_listCtrl),
                                      row=row)
        event.Skip()

    def onAddEventToolClicked(self, event):
        """
        Обработчик добавления события.
        """
        event_dict = edit_component_event_dlg(parent=self)
        if event_dict is not None:
            row = (event_dict.get('name', u''), event_dict.get('event', u''), event_dict.get('func_name', u''))
            self.appendRow_list_ctrl(ctrl=self.event_listCtrl, row=row)
        event.Skip()

    def onDelEventToolClicked(self, event):
        """
        Обработчик удаления события.
        """
        self.removeRow_list_ctrl(ctrl=self.event_listCtrl)
        event.Skip()

    def onEditEventToolClicked(self, event):
        """
        Обработчик редактирования события.
        """
        row = self.getRow_list_ctrl(ctrl=self.event_listCtrl)
        if row:
            name, event_name, func_name = row
            event_dict = edit_component_event_dlg(parent=self, name=name, event=event_name, func_name=func_name)
            if event_dict is not None:
                row = (event_dict.get('name', u''), event_dict.get('event', u''), event_dict.get('func_name', u''))
                self.setRow_list_ctrl(ctrl=self.event_listCtrl,
                                      row_idx=self.getItemSelectedIdx(self.event_listCtrl),
                                      row=row)
        event.Skip()

    def onCreateComponentWizardPageChanged(self, event):
        """
        Обработчик смены страницы визарда.
        """
        # Генерация кода по указанным атрибутам и событиям
        event.Skip()

    def onCreateComponentWizardFinished(self, event):
        """
        Обработчик окончания работы визарда.
        """
        # Сохранение сгенерированного кода в файл
        event.Skip()


def show_create_component_wizard(parent=None):
    """
    Функция отображения мастера создания компонента.

    :param parent: Родительское окно для визарда.
    :return: True/False.
    """
    try:
        if parent is None:
            parent = wx.GetApp().GetTopWindow()
        wizard = icCreateComponentWizard(parent=parent)
        # Установить размер визарда по первой странице
        wizard.FitToPage(wizard.base_wizPage)
        # Запустить визард
        wizard.RunWizard(wizard.base_wizPage)
        return True
    except:
        log.fatal(u'Ошибка мастера создания компонента')
    return False


def test():
    """
    Функция тестирования.

    :return:
    """
    app = wx.PySimpleApp()
    frame = wx.Frame(parent=None)
    show_create_component_wizard(parent=frame)
    app.MainLoop()


if __name__ == '__main__':
    test()
