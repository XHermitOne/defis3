#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Реквизит связи с объектом-ссылка/справочником системы NSI.
Класс пользовательского компонента РЕКВИЗИТ СВЯЗИ С ОБЪЕКТОМ-ССЫЛКА/СПРАВОЧНИКОМ.

:type ic_user_name: C{string}
:var ic_user_name: Имя пользовательского класса.
:type ic_can_contain: C{list | int}
:var ic_can_contain: Разрешающее правило - список типов компонентов, которые
    могут содержаться в данном компоненте. -1 - означает, что любой компонент
    может содержатся в данном компоненте. Вместе с переменной ic_can_not_contain
    задает полное правило по которому определяется возможность добавления других
    компонентов в данный комопнент.
:type ic_can_not_contain: C{list}
:var ic_can_not_contain: Запрещающее правило - список типов компонентов,
    которые не могут содержаться в данном компоненте. Запрещающее правило
    начинает работать если разрешающее правило разрешает добавлять любой
    компонент (ic_can_contain = -1).
"""

import wx
from ic.components import icwidget
from ic.utils import util
from ic.utils import coderror
from ic.dlg import dlgfunc
from ic.bitmap import bmpfunc
import ic.components.icResourceParser as prs
from ic.PropertyEditor import icDefInf

from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

import NSI.nsi_sys.ref_requisite as parentModule

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icRefNSIRequisite'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'RefNSIRequisite',
                'name': 'default',
                'child': [],
                'activate': 1,
                'init_expr': None,
                '_uuid': None,

                # Свойства генерации контролов редактирования/просмотра
                'label': u'',  # Надпись реквизита
                               # Если надпись пустая, то берется вместо надписи описание (description)

                # Свойства генерации полей хранения
                'field': None,  # Поле кода справочника

                'set_value': None,  # Функционал, исполняемый при установке значения реквизита
                'get_value': None,  # Функционал, исполняемый при получениии значения реквизита

                # Ссылка на объект справочника
                'nsi_psp': None,  # Справочник NSI
                'auto_set': True,  # Признак автоматического заполнения полей при редактировании

                '__styles__': ic_class_styles,
                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_TEXTFIELD: ['description', 'label', 'field'],
                                   icDefInf.EDT_CHECK_BOX: ['auto_set'],
                                   icDefInf.EDT_USER_PROPERTY: ['nsi_psp'],
                                   },
                '__events__': {'set_value': (None, None, False),
                               'get_value': (None, None, False),
                               },
                '__parent__': parentModule.SPC_IC_REFNSIREQUISITE,
                '__attr_hlp__': {'label': u'Надпись реквизита',

                                 'field': u'Поле кода справочника',

                                 'set_value': u'Функционал, исполняемый при установке значения реквизита',
                                 'get_value': u'Функционал, исполняемый при получениии значения реквизита',

                                 'nsi_psp': u'Справочник NSI',
                                 'auto_set': u'Признак автоматического заполнения полей при редактировании',
                                 },
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('tag-label.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('tag-label.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = None

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 1)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('nsi_psp',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('nsi_psp',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if ret[0][0] not in ('Sprav', 'RefObject'):
                dlgfunc.openWarningBox(u'ВНИМАНИЕ!', u'Выбранный объект не является СПРАВОЧНИКОМ NSI.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('nsi_psp',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icRefNSIRequisite(parentModule.icRefNSIRequisiteProto, icwidget.icSimple):
    """
    Класс пользовательского компонента РЕКВИЗИТ СВЯЗИ С ОБЪЕКТОМ-ССЫЛКА/СПРАВОЧНИКОМ.

    :type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.

        - B{type='defaultType'}:
        - B{name='default'}:

    """
    component_spc = ic_class_spc

    def __init__(self, parent, id, component, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор базового класса пользовательских компонентов.

        :type parent: C{wx.Window}
        :param parent: Указатель на родительское окно.
        :type id: C{int}
        :param id: Идентификатор окна.
        :type component: C{dictionary}
        :param component: Словарь описания компонента.
        :type logType: C{int}
        :param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        :param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        :type evalSpace: C{dictionary}
        :type bCounter: C{bool}
        :param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        :type progressDlg: C{wx.ProgressDialog}
        :param progressDlg: Указатель на идикатор создания формы.
        """
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        parentModule.icRefNSIRequisiteProto.__init__(self, parent)

        # Обязательные параметры для генерации таблицы
        self.type_val = 'T'
        self.len = None

        # Свойства компонента
        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if x.find('__') != 0]

        for key in lst_keys:
            setattr(self, key, component[key])

    def getFieldName(self):
        """
        Имя поля реквизита таблицы.
        """
        field_name = self.getICAttr('field')
        return field_name if field_name else self.getName()

    def getNSIPsp(self):
        """
        Справочник.
        """
        return self.getICAttr('nsi_psp')

    def getSprav(self):
        """
        Объект справочника.
        """
        if self.sprav is None:
            psp = self.getNSIPsp()
            if psp is None:
                assert None, 'Not define <nsi_psp> in NSIRequisite <%s>' % self.name
                return None
            self.sprav = self.GetKernel().Create(psp)
        return self.sprav

    def getLabel(self):
        """
        Надпись реквизита.
        """
        return self.getICAttr('label')

    #   Обработчики событий
