#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Атрибут метакомпонента.

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
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf

import ic.utils.resource as resource

# --- Спецификация ---
SPC_IC_METAATTR = {'value': None,  # Значение атрибута
                   '__parent__': icwidget.SPC_IC_SIMPLE,
                   '__attr_hlp__': {'value': u'Значение атрибута',
                                    },
                   }

# --- Описание компонента для редактора ресурса ---
#   Тип компонента
ic_class_type = icDefInf._icServiceType

#   Имя класса
ic_class_name = 'icMetaAttr'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'MetaAttr',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                'child': [],
                '_uuid': None,

                '__events__': {},
                '__styles__': ic_class_styles,
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description'],
                                   },
                '__parent__': SPC_IC_METAATTR,
                }

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = '@common.imgEdtMetaAttr'
ic_class_pic2 = '@common.imgEdtMetaAttr'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.user.ic_metaattr_wrp.icMetaAttr-class.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 3)


class icMetaAttrPrototype:
    """
    Атрибут метакомпонента.
    """

    def __init__(self, Resource_):
        """
        Конструктор.
        @param Resource_: Ресурс описания.
        """
        self._value = None

    def defaultValue(self):
        """
        Инициализировать значение по умолчанию.
        """
        self._value = self.eval_attr('value')[1]
        return self._value

    def getValue(self):
        """
        Получить значение.
        """
        return self._value

    def setValue(self, Value_):
        """
        Установить значение.
        """
        self._value = Value_


class icMetaAttr(icwidget.icSimple, icMetaAttrPrototype):
    """
    Атрибут метакомпонента.
    """

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор.

        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно
        @type id: C{int}
        @param id: Идентификатор окна
        @type component: C{dictionary}
        @param component: Словарь описания компонента
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений
        @type evalSpace: C{dictionary}
        @type bCounter: C{bool}
        @param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        @type progressDlg: C{wx.ProgressDialog}
        @param progressDlg: Указатель на идикатор создания формы.
        """
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)
        icMetaAttrPrototype.__init__(self, component)

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        prs.icResourceParser(self, self.resource['child'], None, evalSpace=self.evalSpace,
                             bCounter=bCounter, progressDlg=progressDlg)
