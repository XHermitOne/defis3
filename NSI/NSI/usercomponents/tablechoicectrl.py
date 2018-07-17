#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Контрол выбора элемента таблицы/запроса в виде выпадающего списка.

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
import ic.components.icwidget as icwidget
import ic.utils.util as util
from ic.dlg import ic_dlg
import ic.components.icResourceParser as prs
import ic.PropertyEditor.icDefInf as icDefInf
from ic.bitmap import ic_bmp

from ic.utils import coderror
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

import NSI.nsi_sys.ictablechoicectrl as parentModule

ICComboCtrlStyle = {'CB_SIMPLE': wx.CB_SIMPLE,
                    'CB_DROPDOWN': wx.CB_DROPDOWN,
                    'CB_READONLY': wx.CB_READONLY,
                    'CB_SORT': wx.CB_SORT,
                    }

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icTableChoiceCtrl'

#   Описание стилей компонента
ic_class_styles = ICComboCtrlStyle

# Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'TableChoiceCtrl',
                'name': 'default',
                'child': [],
                'activate': True,
                'init_expr': None,
                '_uuid': None,

                'table': None,  # Паспорт таблицы/запроса источника данных
                'code_field': '',     # Поле, которое является кодом записи
                'label_field': '',    # Поле, которое отображается в контроле
                'get_label': None,    # Код определения записи контрола, в случае сложного оформления записи
                'get_filter': None,   # Код дополнительной фильтрации данных таблицы/запроса
                'can_empty': True,  # Возможно выбирать пустое значение?

                'on_change': None,  # Обработчик изменения выбранного кода

                '__styles__': ic_class_styles,
                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_TEXTFIELD: ['description', 'code_field', 'label_field'],
                                   icDefInf.EDT_USER_PROPERTY: ['table'],
                                   icDefInf.EDT_CHECK_BOX: ['can_empty'],
                                   },
                '__events__': {'on_change': ('wx.EVT_COMBOBOX', 'onComboBox', False),
                               },
                '__parent__': parentModule.SPC_IC_TABLECHOICECTRL,
                '__attr_hlp__': {'table': u'Паспорт таблицы/запроса источника данных',
                                 'code_field': u'Поле, которое является кодом записи',
                                 'label_field': u'Поле, которое отображается в контроле',
                                 'get_label': u'Код определения записи контрола, в случае сложного оформления записи',
                                 'get_filter': u'Код дополнительной фильтрации данных таблицы/запроса',
                                 'can_empty': u'Возможно выбирать пустое значение?',
                                 'on_change': u'Обработчик изменения выбранного кода',
                                 },
                }


#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('ic_table_combobox.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('ic_table_combobox.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 2, 1)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('table',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('table',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('Table', 'Query'):
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!', u'Выбранный объект не является ТАБЛИЧНЫМ ОБЪЕКТОМ.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
        elif ret in (None, ''):
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('table',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icTableChoiceCtrl(parentModule.icTableChoiceCtrlProto, icwidget.icWidget):
    """
    Описание пользовательского компонента.

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

        parentModule.icTableChoiceCtrlProto.__init__(self,
                                                     parent, id,
                                                     size=self.size, pos=self.position, style=self.style)
        # Установить источник данных
        table_psp = self.getTablePsp()
        self.createTableSrcData(table_psp=table_psp)

        # Регистрация обработчиков
        self.Bind(wx.EVT_COMBOBOX, self.onComboBox)
        self.BindICEvt()

    def getTablePsp(self):
        """
        Паспорт табличного объекта-источника данных.
        """
        return self.getICAttr('table')

    def createTableSrcData(self, table_psp):
        """
        Создать табличный объект-источник данных по его паспорту.
        @param table_psp: Паспорт табличного объекта-источника данных.
        @return: табличный объект-источник данных.
        """
        table = self.GetKernel().Create(table_psp) if table_psp else None
        self.setTableSrcData(table)

    def getCodeField(self):
        """
        Поле кода элемента списка.
        """
        return self.getICAttr('code_field')

    def getLabelField(self):
        """
        Поле надписи элемента списка.
        """
        return self.getICAttr('label_field')

    def isLabelFunc(self):
        """
        Определена функция получения надписи элемента списка?
        @return: True/False.
        """
        return self.isICAttrValue('get_label')

    def getLabelFunc(self, *arg, **kwarg):
        """
        Получить функцию определения надписи элемента списка.
        """
        self.evalSpace['self'] = self
        self.evalSpace['args'] = arg
        self.evalSpace.update(kwarg)

        result = self.eval_attr('get_label')
        if result[0]:
            return result[1]
        return None

    def getFilterFunc(self, *arg, **kwarg):
        """
        Получить функцию дополнительной фильтрации элементов списка.
        """
        self.evalSpace['self'] = self
        self.evalSpace['args'] = arg
        self.evalSpace.update(kwarg)

        result = self.eval_attr('get_filter')
        if result[0]:
            return result[1]
        return None

    def isFilterFunc(self):
        """
        Определена функция дополнительной фильтрации табличных данных?
        @return: True/False.
        """
        return self.isICAttrValue('get_filter')

    def getCanEmpty(self):
        """
        Возможно выбирать пустое значение?
        """
        return self.getICAttr('can_empty')

    def onComboBox(self, event):
        """
        Обработчик выбора элемента.
        """
        # Вызвать обработчик родительского класса
        # ВНИМАНИЕ! Skip не выполняем.
        parentModule.icTableChoiceCtrlProto.onComboBox(self, None)
        # Вызов пользовательского обработчика
        # ВНИМАНИЕ! По окончании выполняется Skip.
        self.eval_event('on_change', event, bSkip=True)
