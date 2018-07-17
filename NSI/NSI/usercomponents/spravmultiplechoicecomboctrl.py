#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Контрол множественного выбора элементов справочника в стандартном виде
выбора справочника через диалоговую форму выбора/поиска справочника
с помощью метода Hlp объекта справочника.

@type ic_user_name: C{string}
@var ic_user_name: Имя пользовательского класса.
@type ic_can_contain: C{list | int}
@var ic_can_contain: Разрешающее правило - список типов компонентов, которые
    могут содержаться в данном компоненте. -1 - означает, что любой компонент
    может содержатся в данном компоненте. Вместе с переменной ic_can_not_contain
    задает полное правило по которому определяется возможность добавления других
    компонентов в данный комопнент.
@type ic_can_not_contain: C{list}
@var ic_can_not_contain: Запрещающее правило - список типов компонентов,
    которые не могут содержаться в данном компоненте. Запрещающее правило
    начинает работать если разрешающее правило разрешает добавлять любой
    компонент (ic_can_contain = -1).
"""

import wx
from ic.PropertyEditor import icDefInf
from ic.utils import coderror
from ic.dlg import ic_dlg
from ic.utils import util
from ic.bitmap import ic_bmp
from ic.components import icwidget
import ic.components.icResourceParser as prs

import NSI.nsi_sys.icspravmultiplechoicecomboctrl as parentModule

from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

ICComboCtrlStyle = {'CB_SIMPLE': wx.CB_SIMPLE,
                    'CB_DROPDOWN': wx.CB_DROPDOWN,
                    'CB_READONLY': wx.CB_READONLY,
                    'CB_SORT': wx.CB_SORT,
                    }

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icSpravMultipleChoiceComboCtrl'

#   Описание стилей компонента
ic_class_styles = ICComboCtrlStyle

# Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'SpravMultipleChoiceComboCtrl',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                'child': [],

                'sprav': None,         # Паспорт справочника-источника данных
                'view_fields': None,    # Список отображаемых полей
                'search_fields': None,  # Список полей для поиска
                'on_select': None,      # Обработчик изменения комбобокса

                '__styles__': ic_class_styles,
                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_TEXTFIELD: ['description'],
                                   icDefInf.EDT_USER_PROPERTY: ['sprav'],
                                   icDefInf.EDT_TEXTLIST: ['view_fields', 'search_fields'],
                                   icDefInf.EDT_PY_SCRIPT: ['on_select'],
                                   },
                '__events__': {},
                '__parent__': parentModule.SPC_IC_SPRAVMULTIPLECHOICECOMBOCTRL,
                '__attr_hlp__': {'sprav': u'Паспорт справочника-источника данных',
                                 'view_fields': u'Список отображаемых полей',
                                 'search_fields': u'Список полей для поиска',
                                 'on_select': u'Обработчик изменения комбобокса',
                                 },
                }


#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('ic_nsi_combo_ctrl.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('ic_nsi_combo_ctrl.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 2)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('sprav',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('sprav',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('Sprav',):
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                                u'Выбранный объект не является Справочником.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
        elif ret in (None, ''):
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('sprav',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icSpravMultipleChoiceComboCtrl(parentModule.icSpravMultipleChoiceComboCtrlProto, icwidget.icWidget):
    """
    Контрол множественного выбора элементов справочника в стандартном виде
    выбора справочника через диалоговую форму выбора/поиска справочника
    с помощью метода Hlp объекта справочника.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.

        - B{type='defaultType'}:
        - B{name='default'}:

    """
    component_spc = ic_class_spc

    def __init__(self, parent, id, component, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор базового класса пользовательских компонентов.

        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type id: C{int}
        @param id: Идентификатор окна.
        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        @type bCounter: C{bool}
        @param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        @type progressDlg: C{wx.ProgressDialog}
        @param progressDlg: Указатель на идикатор создания формы.
        """
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        parentModule.icSpravMultipleChoiceComboCtrlProto.__init__(self, parent, id,
                                                                  size=self.size, pos=self.position, style=self.style)

        # Установить справочник
        sprav_psp = self.getSpravPsp()
        sprav = self.GetKernel().Create(sprav_psp) if sprav_psp else None
        self.setSprav(sprav)
        # Установить отображаемые поля и поля поиска
        self.setViewFieldnames(self.getViewFieldnames())
        self.setSearchFieldnames(self.getSearchFieldnames())

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

        self.BindICEvt()

    def getSpravPsp(self):
        """
        Паспорт справочника.
        """
        return self.getICAttr('sprav')

    def getViewFieldnames(self):
        """
        Имена отображаемых полей.
        """
        return self.getICAttr('view_fields')

    def getSearchFieldnames(self):
        """
        Имена полей для поиска.
        """
        return self.getICAttr('search_fields')

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        prs.icResourceParser(self, self.resource['child'], None, evalSpace=self.evalSpace,
                             bCounter=bCounter, progressDlg=progressDlg)

    def OnSelect(self, event):
        """
        Обработчик изменения комбобокса.
        """
        self.evalSpace['self'] = self
        self.evalSpace['evt'] = event
        self.evalSpace['event'] = event
        self.evalSpace['SPRAV'] = self.getSprav()
        self.evalSpace['SPRAV_CODES'] = self.getCodes()

        self.eval_attr('on_select')
        if event:
            event.Skip()

    def OnButtonClick(self):
        """
        Overridden from ComboCtrl, called when the combo button is clicked.
        """
        prev_selected_codes = self.getCodes()
        selected_code = self.choiceSprav()
        if selected_code not in prev_selected_codes:
            self.OnSelect(event=None)
