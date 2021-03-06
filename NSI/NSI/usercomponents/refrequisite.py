#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Реквизит.

Класс пользовательского компонента РЕКВИЗИТ ОБЪЕКТА-ССЫЛКА/СПРАВОЧНИКА.
"""

import wx
from ic.components import icwidget
from ic.utils import util
from ic.bitmap import bmpfunc
import ic.components.icResourceParser as prs
from ic.PropertyEditor import icDefInf

import NSI.nsi_sys.ref_requisite as parentModule
from ic.db import icsqlalchemy

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icRefRequisite'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'RefRequisite',
                'name': 'default',
                'child': [],
                'activate': True,
                'init_expr': None,
                '_uuid': None,

                # Свойства генерации поля хранения
                'type_val': 'T',  # Тип значения реквизита
                'len': None,  # Длина значения реквизита
                'field': None,  # Поле таблицы родительского компонента, в котором храниться значение реквизита
                'default': None,  # Значение по умолчанию

                # Свойства генерации контролов редактирования/просмотра
                'label': u'',  # Надпись реквизита
                               # Если надпись пустая, то берется вместо надписи описание (description)

                '__styles__': ic_class_styles,
                '__lists__': {'type_val': list(icsqlalchemy.FIELD_VALUES_ALL_TYPES)},
                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_TEXTFIELD: ['description', 'field', 'label'],
                                   icDefInf.EDT_CHOICE: ['type_val'],
                                   icDefInf.EDT_NUMBER: ['len'],
                                   },
                '__events__': {'set_value': (None, None, False),
                               'get_value': (None, None, False),
                               },
                '__parent__': parentModule.SPC_IC_REFREQUISITE,
                '__attr_hlp__': {'type_val': u'Тип значения реквизита',
                                 'len': u'Длина значения реквизита',
                                 'field': u'Поле таблицы родительского компонента, в котором храниться значение реквизита',
                                 'default': u'Значение по умолчанию',

                                 'set_value': u'Функционал, исполняемый при установке значения реквизита',
                                 'get_value': u'Функционал, исполняемый при получениии значения реквизита',

                                 'label': u'Надпись реквизита',
                                 },
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('tag-label-black.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('tag-label-black.png')

#   Путь до файла документации
ic_class_doc = 'NSI/doc/_build/html/NSI.usercomponents.refrequisite.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = None

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 2)


class icRefRequisite(parentModule.icRefRequisiteProto, icwidget.icSimple):
    """
    Класс пользовательского компонента РЕКВИЗИТ ОБЪЕКТА-ССЫЛКА/СПРАВОЧНИКА.

    :type component_spc: C{dictionary}
    :cvar component_spc: Спецификация компонента.

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

        parentModule.icRefRequisiteProto.__init__(self, parent)

        # Свойства компонента
        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        self.createAttributes(component)

        # Установить значение по умолчанию
        self.init_data()

    def getFieldName(self):
        """
        Имя поля реквизита таблицы, в которой храниться документ.
        """
        field_name = self.getICAttr('field')
        return field_name if field_name else self.getName()

    def getTypeValue(self):
        """
        Тип поля хранения реквизита.
        """
        return self.getICAttr('type_val')

    def getDefault(self):
        """
        Значение поля реквизита таблицы по умолчанию.
        """
        return self.eval_attr('default')[1]

    def getLabel(self):
        """
        Надпись реквизита.
        """
        return self.getICAttr('label')

    #   Обработчики событий
