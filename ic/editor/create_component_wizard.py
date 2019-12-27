#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Мастер создания пользовательского компонента.
"""

import keyword
import os.path
import inspect
import wx
import wx.stc
import wx.propgrid

from ic.log import log

try:
    from . import create_component_wizard_proto
except ImportError:
    import create_component_wizard_proto

from ic.engine import glob_functions
from ic.engine import form_manager
from ic.PropertyEditor import icDefInf
from ic.utils import strfunc
from ic.utils import impfunc
from ic.utils import filefunc
from ic.utils import txtfunc
from ic.dlg import dlgfunc

__version__ = (0, 1, 1, 1)

DEFAULT_WIZARD_WIDTH = 800
DEFAULT_WIZARD_HEIGHT = 600

# Формат имени файла документации компонента подсистемы
DOC_FILENAME_FMT = '%s/doc/_build/html/%s.usercomponents.%s.html'

# Формат имени файла документации общесистемного компонента
DEFAULT_SYS_COMPONENT_DOC_FILENAME_FMT = 'ic/doc/_build/html/ic.components.user.%s.html'

# Стандартный шаблон модуля компонента
COMPONENT_MODULE_FMT = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
%s.

:author: %s
:copyright: %s
"""

import wx
import wx.aui

from ic.components import icwidget

from ic.utils import util
import ic.components.icResourceParser as prs
from ic.PropertyEditor import icDefInf
from ic.log import log
from ic.bitmap import bmpfunc

from ic.utils import coderror
from ic.dlg import dlgfunc
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

%s

# --- Спецификация компонента ---
#   Тип компонента
ic_class_type = '%s'

#   Имя класса
ic_class_name = 'ic%s'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = {'type': ic_class_type,
                'name': 'default',
                'activate': True,
                'init_expr': None,
                'child': [],
                '_uuid': None,

                %s
                
                %s
                
                '__styles__': ic_class_styles,
                '__events__': {%s
                               },
                '__lists__': {},
                '__attr_types__': {%s
                                   },
                '__parent__': %s,
                '__attr_hlp__': {%s
                                 },
                }
                    
#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('%s')
ic_class_pic2 = bmpfunc.createLibraryBitmap('%s')

#   Путь до файла документации
ic_class_doc = '%s'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 1)

# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    user_property_attrs = ic_class_spc.get('__attr_types__', dict()).get(icDefInf.EDT_USER_PROPERTY, [])
    if attr in user_property_attrs:
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    user_property_attrs = ic_class_spc.get('__attr_types__', dict()).get(icDefInf.EDT_USER_PROPERTY, [])
    if attr in user_property_attrs:
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt.GetPropertyGrid().GetView()
            if not ret[0][0] in ():
                dlgfunc.openWarningBox(u'ОШИБКА', 
                                       u'Выбранный объект не является ...', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    user_property_attrs = ic_class_spc.get('__attr_types__', dict()).get(icDefInf.EDT_USER_PROPERTY, [])
    if attr in user_property_attrs:
        return pspEdt.str_to_val_user_property(text, propEdt)


class ic%s(%s, icwidget.%s):
    """
    %s
    """
    # Спецификаци компонента
    component_spc = ic_class_spc
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор.

        :type parent: C{wx.Window}
        :param parent: Указатель на родительское окно
        :type id: C{int}
        :param id: Идентификатор окна
        :type component: C{dictionary}
        :param component: Словарь описания компонента
        :type logType: C{int}
        :param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        :param evalSpace: Пространство имен, необходимых для вычисления внешних выражений
        :type evalSpace: C{dictionary}
        :type bCounter: C{bool}
        :param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        :type progressDlg: C{wx.ProgressDialog}
        :param progressDlg: Указатель на идикатор создания формы.
        """
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.%s.__init__(self, parent, id, component, logType, evalSpace)
        %s.__init__(self)
        
        # Создание атрибутов
        self.createAttributes(component)
        
        # Создаем дочерние компоненты
        self.createChildren(bCounter=bCounter, progressDlg=progressDlg)
        
        # Дополнительный функционал инициализации

        # Связывание событий с обработчиками
        self.BindICEvt()
'''


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
                                    default=self.default_textCtrl.GetValue(),
                                    description=self.description_textCtrl.GetValue())
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
                                     func_name=self.func_name_textCtrl.GetValue(),
                                     description=self.description_textCtrl.GetValue())
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
                                        dict(label=u'По умолчанию', width=200),
                                        dict(label=u'Описание', width=600)))

        # Колонки списка событий компонента
        self.setColumns_list_ctrl(ctrl=self.event_listCtrl,
                                  cols=(dict(label=u'Наименование', width=200),
                                        dict(label=u'Событие', width=150),
                                        dict(label=u'Обработчик', width=200),
                                        dict(label=u'Описание', width=600)))

        # Создать редактор кода
        self.source_scintilla = wx.stc.StyledTextCtrl(parent=self.gen_wizPage)
        # Установить стиль редактора кода
        self.set_style_python_source_scintilla(self.source_scintilla)

        sizer = self.gen_wizPage.GetSizer()
        sizer.Add(self.source_scintilla, 1, wx.EXPAND | wx.ALL, 5)

    def set_style_python_source_scintilla(self, scintilla):
        """
        Стилизация редактора кода Scintilla для Python.

        :param scintilla: Объект контрола редактора стилизованного текста.
        """
        # Установка лексического анализа
        scintilla.SetLexer(wx.stc.STC_LEX_PYTHON)
        scintilla.SetKeyWords(0, ' '.join(keyword.kwlist))

        scintilla.SetProperty('fold', '1')
        scintilla.SetProperty('tab.timmy.whinge.level', '1')
        scintilla.SetMargins(0, 0)

        # Не видеть пустые пробелы в виде точек
        scintilla.SetViewWhiteSpace(False)

        # Установить ширину 'таба'
        scintilla.SetIndent(4)                 # Запрещенный размер отступа для wx
        scintilla.SetIndentationGuides(True)   # Показать направляющие
        scintilla.SetBackSpaceUnIndents(True)  # Отступы вместо удаления 1 пробел
        scintilla.SetTabIndents(True)          # Отступы клавиш табуляции
        scintilla.SetTabWidth(4)               # Запрещенный размер вкладки для wx
        scintilla.SetUseTabs(False)            # Используйте пробелы вместо вкладок, или

        # Установка поле для захвата маркеров папки
        scintilla.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        scintilla.SetMarginMask(2, wx.stc.STC_MASK_FOLDERS)
        scintilla.SetMarginSensitive(1, True)
        scintilla.SetMarginSensitive(2, True)
        scintilla.SetMarginWidth(1, 25)
        scintilla.SetMarginWidth(2, 12)

        # и теперь установите маркеры сгиба
        scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEREND,     wx.stc.STC_MARK_BOXPLUSCONNECTED,  'white', 'black')
        scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUSCONNECTED, 'white', 'black')
        scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_TCORNER,  'white', 'black')
        scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERTAIL,    wx.stc.STC_MARK_LCORNER,  'white', 'black')
        scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERSUB,     wx.stc.STC_MARK_VLINE,    'white', 'black')
        scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDER,        wx.stc.STC_MARK_BOXPLUS,  'white', 'black')
        scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPEN,    wx.stc.STC_MARK_BOXMINUS, 'white', 'black')

        # ---------------------------------------------
        # Сделаем несколько стилей, лексер определяет,
        # для чего используется каждый стиль, мы
        # просто нужно определить, как выглядит каждый стиль.
        # Этот набор адаптирован из примеров файлов свойств Scintilla.

        scintilla.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, 'fore:#000000,back:#FFFFFF,face:Courier New,size:9')
        scintilla.StyleClearAll()

        # Следующие спецификации стиля указывают только на отличия
        # от настроек по умолчанию.
        # Остальное остается без изменений.

        # Номера строк на полях
        scintilla.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER, 'back:#99A9C2,face:Arial Narrow,size:8')

        # Выделенная скобка
        scintilla.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT, 'fore:#00009D,back:#FFFF00')
        # Непревзойденная скобка
        scintilla.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD, 'fore:#00009D,back:#FF0000')
        # Руководство по отступам
        scintilla.StyleSetSpec(wx.stc.STC_STYLE_INDENTGUIDE, 'fore:#CDCDCD')
        # Стили Python
        scintilla.StyleSetSpec(wx.stc.STC_P_DEFAULT, 'fore:#000000')
        # Комментарии
        scintilla.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, 'fore:#008000')
        scintilla.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK, 'fore:#008000')
        # Числа
        scintilla.StyleSetSpec(wx.stc.STC_P_NUMBER, 'fore:#008080')
        # Строки и символы
        scintilla.StyleSetSpec(wx.stc.STC_P_STRING, 'fore:#800080')
        scintilla.StyleSetSpec(wx.stc.STC_P_CHARACTER, 'fore:#800080')
        # Ключевые слова
        scintilla.StyleSetSpec(wx.stc.STC_P_WORD, 'fore:#000080,bold')
        # Тройные кавычки
        scintilla.StyleSetSpec(wx.stc.STC_P_TRIPLE, 'fore:#000080')
        scintilla.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, 'fore:#000080')
        # Имена слассов
        scintilla.StyleSetSpec(wx.stc.STC_P_CLASSNAME, 'fore:#0000FF,bold')
        # Имена функций
        scintilla.StyleSetSpec(wx.stc.STC_P_DEFNAME, 'fore:#000000,bold')
        # Опреаторы
        scintilla.StyleSetSpec(wx.stc.STC_P_OPERATOR, 'fore:#800000,bold')
        # Идентификаторы. Я оставляю это как не смелый,
        # потому что все кажется быть идентификатором,
        # если он не соответствует вышеуказанным критериям
        scintilla.StyleSetSpec(wx.stc.STC_P_IDENTIFIER, 'fore:#000000')

        # Цвет каретки
        scintilla.SetCaretForeground('BLUE')
        # Выбор фона
        scintilla.SetSelBackground(1, '#66CCFF')

        scintilla.SetSelBackground(True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        scintilla.SetSelForeground(True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

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
                if str_value.startswith('ic'):
                    str_value = str_value[2:]
                    self.name_propertyGridItem.SetValue(str_value)
                module = 'ic%s.py' % str_value.lower()
                module_name = module[:-3]
                self.module_propertyGridItem.SetValue(module)
                prj_name = glob_functions.getPrjName()
                if prj_name is None:
                    # Если проект не определен, то считаем что это общесистемный компонент
                    doc_filename = DEFAULT_SYS_COMPONENT_DOC_FILENAME_FMT % module_name
                else:
                    doc_filename = DOC_FILENAME_FMT % (prj_name, prj_name, module_name)
                self.docfile_propertyGridItem.SetValue(doc_filename)
            elif name == 'author':
                copyright_text = '(C) %s Copyright' % str_value
                self.copyright_propertyGridItem.SetValue(copyright_text)
            elif name == 'parent_module':
                parent_module = impfunc.loadSource('parent_module', str_value)
                if parent_module is not None:
                    parent_classes = [module_name for module_name in dir(parent_module) if inspect.isclass(getattr(parent_module, module_name))]
                    choices = wx.propgrid.PGChoices(parent_classes)
                    self.parentclass_propertyGridItem.SetChoices(choices)

        # event.Skip()

    def onAddAttrToolClicked(self, event):
        """
        Обработчик добавления атрибута.
        """
        attr = edit_component_attr_dlg(parent=self)
        if attr is not None:
            row = (attr.get('name', u''), attr.get('editor', u''),
                   attr.get('default', u''), attr.get('description', u''))
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
                row = (attr.get('name', u''), attr.get('editor', u''),
                       attr.get('default', u''), attr.get('description', u''))
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
            row = (event_dict.get('name', u''), event_dict.get('event', u''),
                   event_dict.get('func_name', u''), event_dict.get('description', u''))
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
                row = (event_dict.get('name', u''), event_dict.get('event', u''),
                       event_dict.get('func_name', u''), event.get('description', u''))
                self.setRow_list_ctrl(ctrl=self.event_listCtrl,
                                      row_idx=self.getItemSelectedIdx(self.event_listCtrl),
                                      row=row)
        event.Skip()

    def gen_code(self, name=None, module=None, description=None,
                 author=None, copyright=None, parent_module=None,
                 parent_class=None, is_widget=None,
                 icon=None, doc_filename=None,
                 attributes=None, events=None):
        """
        Генерация кода по указанным атрибутам и событиям.

        :param name: Наименование компонента.
        :param module: Файл модуля класса компонента.
        :param description: Описание.
        :param author: Автор.
        :param copyright: Копирайт.
        :param parent_module: Модуль родительского класса.
        :param parent_class: Родительский класс.
        :param is_widget: Является ли компонент видимым (Виджетом)?
        :param icon: Файл иконки.
        :param doc_filename: Полное имя файла документа.
        :param attributes: Список словарей - описаний атрибутов компонента.
        :param events: Список словарей - описаний событий компонента.
        :return: Сгенерированный текст модуля компонента.
            Или None в случае ошибки.
        """
        if name is None:
            name = self.name_propertyGridItem.GetValueAsString()
        if module is None:
            module = self.module_propertyGridItem.GetValueAsString()
        if description is None:
            description = self.description_propertyGridItem.GetValueAsString()
        if author is None:
            author = self.author_propertyGridItem.GetValueAsString()
        if copyright is None:
            copyright = self.copyright_propertyGridItem.GetValueAsString()
        if parent_module is None:
            parent_module = self.parentmodule_propertyGridItem.GetValueAsString()
        if parent_class is None:
            parent_class = self.parentclass_propertyGridItem.GetValueAsString()
        if is_widget is None:
            is_widget = self.widget_propertyGridItem.GetValue()
        if icon is None:
            icon = self.icon_propertyGridItem.GetValueAsString()
        if doc_filename is None:
            doc_filename = self.docfile_propertyGridItem.GetValueAsString()
        if attributes is None:
            rows = self.getRows_list_ctrl(self.attr_listCtrl)
            attributes = [dict(name=row[0], editor=row[1],
                               default=row[2], description=row[3]) for row in rows]
        if events is None:
            rows = self.getRows_list_ctrl(self.event_listCtrl)
            events = [dict(name=row[0], event=row[1],
                           func_name=row[2], description=row[3]) for row in rows]

        try:
            return self._gen_code(name, module, description,
                                  author, copyright, parent_module,
                                  parent_class, is_widget, icon, doc_filename,
                                  attributes, events)
        except:
            log.fatal(u'Ошибка генерации кода компонента')
        return None

    def _gen_code(self, name='', module='', description='',
                 author='', copyright='', parent_module='',
                 parent_class='', is_widget=False, icon='', doc_filename='',
                 attributes=(), events=()):
        """
        Генерация кода по указанным атрибутам и событиям.

        :param name: Наименование компонента.
        :param module: Файл модуля класса компонента.
        :param description: Описание.
        :param author: Автор.
        :param copyright: Копирайт.
        :param parent_module: Модуль родительского класса.
        :param parent_class: Родительский класс.
        :param is_widget: Является ли компонент видимым (Виджетом)?
        :param icon: Файл иконки.
        :param doc_filename: Полное имя файла документа.
        :param attributes: Список словарей - описаний атрибутов компонента.
        :param events: Список словарей - описаний событий компонента.
        :return: Сгенерированный текст модуля компонента.
        """
        attributes_txt = '\n'.join(['%s: %s,' % (str(attr.get('name')),
                                                 str(attr.get('default'))) for attr in attributes])
        editors = [attr.get('editor') for attr in attributes]
        # Убирем повторение
        editors = [editor for i, editor in enumerate(editors) if editor not in editors[i+1:]]

        editors_txt = '\n'.join(['icDefInf.%s: %s,' % (editor,
                                                       ', '.join([str(attr.get('name')) for attr in attributes if attr.get('editor') == editor])) for editor in editors])
        events_txt = '\n'.join(['%s: %s,' % (str(evt.get('name')), 'None') for evt in events])
        bind_txt = '\n'.join(['\'%s\': (%s, %s, %s),' % (str(evt.get('name')),
                                                         str(evt.get('event') if evt.get('event') else None),
                                                         str(evt.get('func_name') if evt.get('func_name') else None),
                                                         str(bool(evt.get('event')))) for evt in events])
        attr_hlp_txt = '\n'.join(['\'%s\': u\'%s\'' % (attr.get('name'),
                                                       attr.get('description', '')) for attr in attributes + events])
        icon_filename = os.path.basename(icon)

        module_list = os.path.splitext(parent_module)[0].replace(filefunc.getRootDir(), '').split(os.path.sep)
        module_list = [pkg_name for pkg_name in module_list if pkg_name]
        prj_name = glob_functions.getPrjName()
        parent_package = '.'.join(module_list[1:-1]) if prj_name else '.'.join(module_list[:-1])
        parent_module_name = module_list[-1] if module_list else ''
        import_parent_module = 'from %s import %s' % (parent_package, parent_module_name)
        parent_class_txt = '%s.%s' % (parent_module_name, parent_class)
        parent_spc = '%s.ic_class_spc' % parent_module_name

        base_class_txt = 'icWidget' if is_widget else 'icSimple'

        code_txt = COMPONENT_MODULE_FMT % (description, author, copyright,
                                           import_parent_module,
                                           name, name,
                                           attributes_txt, events_txt,
                                           bind_txt, editors_txt,
                                           parent_spc,
                                           attr_hlp_txt,
                                           icon_filename, icon_filename,
                                           doc_filename,
                                           name, parent_class_txt,
                                           base_class_txt,
                                           description,
                                           base_class_txt,
                                           parent_class_txt)
        return code_txt

    def onCreateComponentWizardPageChanged(self, event):
        """
        Обработчик смены страницы визарда.
        """
        # Генерация кода по указанным атрибутам и событиям
        code_txt = self.gen_code()
        if code_txt:
            self.source_scintilla.SetValue(code_txt)
        event.Skip()

    def save(self, module=None, prj_name=None, bReWrite=False):
        """
        Сохранить сгенерированный файл модуля.

        :param module: Имя файла модуля.
            Если не определено, то вызвается диалог ввода имени модуля.
        :param prj_name: Имя проекта.
            Если не указывается, то считается что компонент общесистемный
            и сохранение производится в пакет ic.components.user
        :param bReWrite: В случае уже имеющегося файла перезаписать без предупреждения?
        :return: True/False.
        """
        if module is None:
            module = dlgfunc.getTextEntryDlg(parent=self, title=u'МОДУЛЬ КОМПОНЕНТА',
                                             prompt_text=u'Введите имя модуля компонента:')

        if module:
            if not module.endswith('.py'):
                module += '.py'

            if prj_name is None:
                prj_name = glob_functions.getPrjName()

            try:
                return self._save(module=module, prj_name=prj_name, bReWrite=bReWrite)
            except:
                log.fatal(u'Ошибка сохранения файла модуля <%s>' % module)
        else:
            log.warning(u'Не определено имя модуля для сохранения')
        return None

    def _save(self, module='default.py', prj_name=None, bReWrite=False):
        """
        Сохранить сгенерированный файл модуля.

        :param module: Имя файла модуля.
            Если не определено, то вызвается диалог ввода имени модуля.
        :param prj_name: Имя проекта.
            Если не указывается, то считается что компонент общесистемный
            и сохранение производится в пакет ic.components.user
        :param bReWrite: В случае уже имеющегося файла перезаписать без предупреждения?
        :return: True/False.
        """
        if prj_name:
            py_filename = os.path.join(filefunc.getRootDir(), prj_name, prj_name,
                                       'usercomponents', module)
        else:
            py_filename = os.path.join(filefunc.getRootDir(), 'ic', 'components',
                                       'user', module)
        code_txt = self.source_scintilla.GetValue()

        if bReWrite and os.path.exists(py_filename):
            filefunc.removeFile(py_filename)
        elif dlgfunc.openAskBox(parent=self, title=u'ВНИМАНИЕ',
                                prompt_txt=u'Файл <%s> уже существует. Заменить?' % py_filename):
            filefunc.removeFile(py_filename)
        else:
            return False

        return txtfunc.save_file_text(py_filename, code_txt)

    def onCreateComponentWizardFinished(self, event):
        """
        Обработчик окончания работы визарда.
        """
        # Сохранение сгенерированного кода в файл
        self.save(module=self.module_propertyGridItem.GetValueAsString())
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
